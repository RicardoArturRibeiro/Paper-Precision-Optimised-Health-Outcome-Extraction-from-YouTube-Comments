#!/usr/bin/env python3
"""
ABSA Complete Pipeline — Google Colab Version
===============================================
Single script: runs GPT-4o + GPT-4.1 ABSA coding, then analyses results.

INSTRUCTIONS FOR GOOGLE COLAB:
1. Upload this file + absa_sample.csv to your Colab session
2. In a cell, run:  !pip install openai
3. In the next cell, paste your API key:
      import os
      os.environ["OPENAI_API_KEY"] = "sk-proj-..."
4. In the next cell, run:  !python absa_colab.py

The script has resume support — if it disconnects, re-run and it picks up.
"""

import csv
import json
import os
import sys
import time
from collections import defaultdict, Counter

# ============================================================
# CONFIGURATION
# ============================================================
API_KEY = os.environ.get("OPENAI_API_KEY", "")
SAMPLE_PATH = "absa_sample.csv"
RESULTS_DIR = "absa_results"
FULL_CORPUS_SIZE = 209661

csv.field_size_limit(sys.maxsize)
os.makedirs(RESULTS_DIR, exist_ok=True)

try:
    from openai import OpenAI
except ImportError:
    print("Installing openai...")
    os.system("pip install openai")
    from openai import OpenAI


# ============================================================
# ABSA PROMPT
# ============================================================
SYSTEM_PROMPT = """You are an expert health informatics coder performing Aspect-Based Sentiment Analysis (ABSA) on YouTube comments from metabolic health channels.

These channels discuss Therapeutic Carbohydrate Restriction (TCR) — ketogenic, low-carb, carnivore, and intermittent fasting approaches.

For each comment, you must determine:

1. **health_related**: Is this comment related to health in any way? (true/false)
   - true: mentions any health topic, condition, symptom, treatment, diet effect, body change, medication, lab result, etc.
   - false: purely about video quality, gratitude without health context, off-topic, political, spam, etc.

2. **health_aspects**: If health_related is true, list ALL health aspects mentioned. For each aspect, provide:
   - **aspect**: The health aspect category. Use these categories:
     - weight_change (weight loss/gain, body composition)
     - blood_sugar (HbA1c, glucose, insulin, diabetes management)
     - energy_mood (energy levels, mood, mental clarity, brain fog)
     - pain_inflammation (joint pain, chronic pain, inflammation)
     - cardiovascular (blood pressure, cholesterol, heart health)
     - digestive (IBS, gut health, bloating, acid reflux)
     - skin (acne, eczema, psoriasis, skin health)
     - sleep (sleep quality, insomnia)
     - medication (starting/stopping/changing medication)
     - autoimmune (autoimmune conditions, RA, lupus, MS)
     - mental_health (anxiety, depression, ADHD)
     - cancer (any cancer-related mentions)
     - hormonal (thyroid, PCOS, fertility, menopause)
     - neurological (epilepsy, seizures, neuropathy, Alzheimer's)
     - general_wellbeing (general health improvement, "feeling better", vitality)
     - diet_adherence (difficulty/ease of following diet, cravings, sustainability)
     - other_health (any health aspect not covered above)
   - **sentiment**: The sentiment toward this health aspect:
     - "positive": improvement, benefit, success (e.g., "lost 30 lbs", "A1C dropped to 5.2")
     - "negative": worsening, harm, failure, side effect (e.g., "my cholesterol went up dangerously", "felt terrible")
     - "neutral": factual mention without clear positive/negative valence (e.g., "I have diabetes", "started keto 3 months ago")
     - "mixed": both positive and negative mentioned for this aspect (e.g., "lost weight but cholesterol went up")
   - **confidence**: How confident are you in this coding? (high/medium/low)

3. **overall_health_sentiment**: If health_related is true, what is the OVERALL health sentiment of the comment?
   - "positive": predominantly reporting health improvements
   - "negative": predominantly reporting health problems or intervention failure
   - "neutral": health-related but no clear positive/negative direction
   - "mixed": significant positive AND negative health content

IMPORTANT RULES:
- Code what the comment ACTUALLY says, not what you infer
- Third-person reports ("my mom lost weight") count — mark them
- Questions about health ("will keto help my diabetes?") are neutral, not positive
- Gratitude TO the creator ("thank you doctor") is NOT health-related unless it mentions a specific health outcome
- "I feel great" in a health context = positive general_wellbeing
- Be conservative: if you're unsure about sentiment, use "neutral"

Respond with a JSON array with one object per comment, in the same order as the input."""


FEW_SHOT_EXAMPLES = """EXAMPLES:

Comment: "I lost 30 pounds in 3 months on keto and my A1C went from 9.1 to 5.4! My doctor was shocked."
→ {"health_related": true, "health_aspects": [{"aspect": "weight_change", "sentiment": "positive", "confidence": "high"}, {"aspect": "blood_sugar", "sentiment": "positive", "confidence": "high"}], "overall_health_sentiment": "positive"}

Comment: "Great video as always Dr. Berg! Keep up the good work!"
→ {"health_related": false, "health_aspects": [], "overall_health_sentiment": null}

Comment: "I tried carnivore for 6 weeks and my LDL went through the roof. My doctor is very concerned."
→ {"health_related": true, "health_aspects": [{"aspect": "cardiovascular", "sentiment": "negative", "confidence": "high"}], "overall_health_sentiment": "negative"}

Comment: "I have type 2 diabetes and I'm thinking about trying this approach. Has anyone had experience?"
→ {"health_related": true, "health_aspects": [{"aspect": "blood_sugar", "sentiment": "neutral", "confidence": "high"}], "overall_health_sentiment": "neutral"}

Comment: "Lost a lot of weight which is great but my sleep has gotten worse since starting keto"
→ {"health_related": true, "health_aspects": [{"aspect": "weight_change", "sentiment": "positive", "confidence": "high"}, {"aspect": "sleep", "sentiment": "negative", "confidence": "high"}], "overall_health_sentiment": "mixed"}

Comment: "This is just big pharma propaganda. Wake up people!"
→ {"health_related": false, "health_aspects": [], "overall_health_sentiment": null}

Comment: "My HbA1c worsened after going back to carbs"
→ {"health_related": true, "health_aspects": [{"aspect": "blood_sugar", "sentiment": "negative", "confidence": "high"}], "overall_health_sentiment": "negative"}"""


# ============================================================
# PART 1: MODEL RUNNER
# ============================================================
def load_sample():
    sample = []
    with open(SAMPLE_PATH, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample.append(row)
    print(f"Loaded {len(sample)} comments from {SAMPLE_PATH}")
    return sample


def build_batch_prompt(comments):
    lines = []
    for i, c in enumerate(comments):
        text = c['comment_text'][:1000]
        lines.append(f'Comment {i+1} (ID: {c["sample_id"]}): "{text}"')
    return "\n\n".join(lines) + "\n\nProvide your JSON array response with one object per comment, in order."


def run_model(model_name, sample, batch_size=10):
    client = OpenAI(api_key=API_KEY)
    safe_name = model_name.replace('-', '_').replace('.', '_')
    output_path = os.path.join(RESULTS_DIR, f"absa_{safe_name}.jsonl")

    # Resume support: skip already-completed IDs
    completed_ids = set()
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get('health_related') is not None:
                        completed_ids.add(str(obj.get('sample_id', '')))
                except:
                    pass
        if completed_ids:
            print(f"  Resuming: {len(completed_ids)} already done")

    remaining = [s for s in sample if s['sample_id'] not in completed_ids]
    if not remaining:
        print(f"  All {len(sample)} comments already processed!")
        return output_path

    remaining_batches = (len(remaining) + batch_size - 1) // batch_size
    print(f"  Processing {len(remaining)} comments in {remaining_batches} batches...")

    errors_total = 0
    for batch_idx in range(0, len(remaining), batch_size):
        batch = remaining[batch_idx:batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1
        user_prompt = build_batch_prompt(batch)

        retries = 0
        max_retries = 3
        while retries < max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": FEW_SHOT_EXAMPLES + "\n\nNow code these comments:\n\n" + user_prompt}
                    ],
                    temperature=0.0,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )

                content = response.choices[0].message.content.strip()
                parsed = json.loads(content)

                # Handle various JSON wrapper formats
                if isinstance(parsed, dict):
                    if 'results' in parsed:
                        parsed_list = parsed['results']
                    elif 'comments' in parsed:
                        parsed_list = parsed['comments']
                    else:
                        for v in parsed.values():
                            if isinstance(v, list):
                                parsed_list = v
                                break
                        else:
                            parsed_list = [parsed]
                elif isinstance(parsed, list):
                    parsed_list = parsed
                else:
                    parsed_list = [parsed]

                with open(output_path, 'a') as f:
                    for i, result in enumerate(parsed_list):
                        if i < len(batch):
                            result['sample_id'] = batch[i]['sample_id']
                            result['channel'] = batch[i]['channel']
                            result['comment_text'] = batch[i]['comment_text'][:200]
                            result['model'] = model_name
                            f.write(json.dumps(result) + '\n')

                done = len(completed_ids) + batch_idx + len(batch)
                pct = done / len(sample) * 100
                if batch_num % 5 == 0 or batch_num == remaining_batches:
                    print(f"    [{model_name}] Batch {batch_num}/{remaining_batches} — {pct:.0f}%")
                break

            except Exception as e:
                retries += 1
                print(f"    Batch {batch_num} error ({retries}/{max_retries}): {str(e)[:120]}")
                if retries < max_retries:
                    time.sleep(5 * retries)
                else:
                    errors_total += len(batch)
                    print(f"    SKIPPING batch {batch_num}")
                    with open(output_path, 'a') as f:
                        for c in batch:
                            f.write(json.dumps({
                                'sample_id': c['sample_id'], 'channel': c['channel'],
                                'comment_text': c['comment_text'][:200], 'model': model_name,
                                'health_related': None, 'health_aspects': [],
                                'overall_health_sentiment': None, 'error': str(e)[:200]
                            }) + '\n')

        time.sleep(0.5)

    print(f"\n  ✓ {model_name} DONE → {output_path}")
    if errors_total > 0:
        print(f"    ⚠ {errors_total} comments had errors (re-run to retry)")
    return output_path


# ============================================================
# PART 2: ANALYSIS
# ============================================================
def load_results(filename):
    results = {}
    errors = 0
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, 'r') as f:
        for line in f:
            try:
                obj = json.loads(line)
                sid = str(obj.get('sample_id', ''))
                if sid and obj.get('health_related') is not None:
                    results[sid] = obj
                else:
                    errors += 1
            except:
                errors += 1
    print(f"  {filename}: {len(results)} valid, {errors} errors/skipped")
    return results


def compute_agreement(gpt4o, gpt41):
    common_ids = set(gpt4o.keys()) & set(gpt41.keys())
    print(f"\n{'='*70}")
    print(f"INTER-MODEL AGREEMENT ANALYSIS")
    print(f"{'='*70}")
    print(f"GPT-4o valid: {len(gpt4o)}")
    print(f"GPT-4.1 valid: {len(gpt41)}")
    print(f"Common IDs: {len(common_ids)}")

    if not common_ids:
        print("\n⚠ NO COMMON VALID RESULTS")
        return set(), 0

    agree_health = both_health = 0
    for sid in common_ids:
        h4o = gpt4o[sid].get('health_related', False)
        h41 = gpt41[sid].get('health_related', False)
        if h4o == h41: agree_health += 1
        if h4o and h41: both_health += 1

    print(f"\n--- Health-Related Classification ---")
    print(f"Agreement: {agree_health}/{len(common_ids)} ({agree_health/len(common_ids)*100:.1f}%)")
    print(f"Both health-related: {both_health}")

    h4o_yes = sum(1 for sid in common_ids if gpt4o[sid].get('health_related'))
    h41_yes = sum(1 for sid in common_ids if gpt41[sid].get('health_related'))
    print(f"GPT-4o health-related: {h4o_yes} ({h4o_yes/len(common_ids)*100:.1f}%)")
    print(f"GPT-4.1 health-related: {h41_yes} ({h41_yes/len(common_ids)*100:.1f}%)")

    agree_sentiment = 0
    matrix = defaultdict(lambda: defaultdict(int))
    for sid in common_ids:
        if gpt4o[sid].get('health_related') and gpt41[sid].get('health_related'):
            s4o = gpt4o[sid].get('overall_health_sentiment', 'unknown')
            s41 = gpt41[sid].get('overall_health_sentiment', 'unknown')
            matrix[s4o][s41] += 1
            if s4o == s41: agree_sentiment += 1

    if both_health > 0:
        print(f"\n--- Sentiment Agreement (among {both_health} both-health) ---")
        print(f"Agreement: {agree_sentiment}/{both_health} ({agree_sentiment/both_health*100:.1f}%)")
        labels = ['positive', 'negative', 'neutral', 'mixed']
        print(f"\n{'':15s}", end='')
        for l in labels: print(f"{'4.1-'+l:>12s}", end='')
        print()
        for l4o in labels:
            print(f"4o-{l4o:11s}", end='')
            for l41 in labels: print(f"{matrix[l4o][l41]:>12d}", end='')
            print()

    return common_ids, both_health


def sentiment_distributions(gpt4o, gpt41, common_ids):
    print(f"\n{'='*70}")
    print(f"SENTIMENT DISTRIBUTIONS")
    print(f"{'='*70}")

    for name, results in [("GPT-4o", gpt4o), ("GPT-4.1", gpt41)]:
        overall = Counter()
        health_count = non_health = 0
        for sid in common_ids:
            r = results.get(sid, {})
            if r.get('health_related'):
                health_count += 1
                overall[r.get('overall_health_sentiment', 'unknown')] += 1
            else:
                non_health += 1

        total = len(common_ids)
        print(f"\n--- {name} (n={total}) ---")
        print(f"  Not health: {non_health} ({non_health/total*100:.1f}%)")
        print(f"  Health:     {health_count} ({health_count/total*100:.1f}%)")
        if health_count > 0:
            for s in ['positive', 'negative', 'neutral', 'mixed']:
                c = overall.get(s, 0)
                print(f"    {s:10s}: {c:4d} ({c/health_count*100:.1f}%)")

        # Aspect breakdown
        asp_sent = defaultdict(Counter)
        asp_tot = Counter()
        for sid in common_ids:
            for a in results.get(sid, {}).get('health_aspects', []):
                if isinstance(a, dict):
                    asp_sent[a.get('aspect','?')][a.get('sentiment','?')] += 1
                    asp_tot[a.get('aspect','?')] += 1
        if asp_tot:
            print(f"\n  {'Aspect':<22s} {'Tot':>5s} {'Pos':>5s} {'Neg':>5s} {'Neu':>5s} {'Mix':>4s}")
            print(f"  {'-'*50}")
            for asp, t in sorted(asp_tot.items(), key=lambda x: -x[1]):
                print(f"  {asp:<22s} {t:>5d} {asp_sent[asp].get('positive',0):>5d} "
                      f"{asp_sent[asp].get('negative',0):>5d} {asp_sent[asp].get('neutral',0):>5d} "
                      f"{asp_sent[asp].get('mixed',0):>4d}")


def consensus_analysis(gpt4o, gpt41, common_ids):
    print(f"\n{'='*70}")
    print(f"CONSENSUS ANALYSIS (both models agree)")
    print(f"{'='*70}")

    cons = Counter()
    cons_health = cons_non = disagree_h = disagree_s = 0
    for sid in common_ids:
        h4o = gpt4o.get(sid, {}).get('health_related', False)
        h41 = gpt41.get(sid, {}).get('health_related', False)
        if not h4o and not h41:
            cons_non += 1
        elif h4o and h41:
            s4o = gpt4o[sid].get('overall_health_sentiment', '')
            s41 = gpt41[sid].get('overall_health_sentiment', '')
            if s4o == s41:
                cons[s4o] += 1
                cons_health += 1
            else:
                disagree_s += 1
        else:
            disagree_h += 1

    total = len(common_ids)
    print(f"\n  Total: {total}")
    print(f"  Both NOT health: {cons_non} ({cons_non/total*100:.1f}%)")
    print(f"  Both health + AGREE sentiment: {cons_health} ({cons_health/total*100:.1f}%)")
    print(f"  Both health, DISAGREE sentiment: {disagree_s}")
    print(f"  Disagree on health classification: {disagree_h}")

    if cons_health > 0:
        print(f"\n  Consensus sentiment (n={cons_health}):")
        for s in ['positive', 'negative', 'neutral', 'mixed']:
            c = cons.get(s, 0)
            print(f"    {s:10s}: {c:4d} ({c/cons_health*100:.1f}%)")

    # Negative aspect detail
    neg_asp = Counter()
    neg_ex = defaultdict(list)
    for sid in common_ids:
        r4o, r41 = gpt4o.get(sid, {}), gpt41.get(sid, {})
        if r4o.get('health_related') and r41.get('health_related'):
            a4o = {a['aspect']: a['sentiment'] for a in r4o.get('health_aspects', []) if isinstance(a, dict)}
            a41 = {a['aspect']: a['sentiment'] for a in r41.get('health_aspects', []) if isinstance(a, dict)}
            for asp in set(a4o) & set(a41):
                if a4o[asp] == 'negative' and a41[asp] == 'negative':
                    neg_asp[asp] += 1
                    if len(neg_ex[asp]) < 3:
                        neg_ex[asp].append(r4o.get('comment_text', '')[:150])

    if neg_asp:
        print(f"\n  Consensus-NEGATIVE aspects:")
        for asp, c in sorted(neg_asp.items(), key=lambda x: -x[1]):
            print(f"    {asp}: {c}")
            for ex in neg_ex[asp][:2]:
                print(f'      → "{ex}..."')


def extrapolation(gpt4o, gpt41, common_ids):
    print(f"\n{'='*70}")
    print(f"EXTRAPOLATION TO FULL CORPUS ({FULL_CORPUS_SIZE:,} comments)")
    print(f"{'='*70}")

    sentiments = Counter()
    health_count = 0
    for sid in common_ids:
        h4o = gpt4o.get(sid, {}).get('health_related', False)
        h41 = gpt41.get(sid, {}).get('health_related', False)
        if h4o or h41:
            health_count += 1
            s4o = gpt4o.get(sid, {}).get('overall_health_sentiment', '')
            s41 = gpt41.get(sid, {}).get('overall_health_sentiment', '')
            sentiments[s4o if s4o == s41 else s41] += 1

    n = len(common_ids)
    if n == 0: return
    hr = health_count / n

    print(f"\n  Sample: {n} | Health rate: {hr*100:.1f}%")
    print(f"  Est. health in corpus: ~{int(FULL_CORPUS_SIZE * hr):,}")

    if health_count > 0:
        print(f"\n  Projected sentiment:")
        for s in ['positive', 'negative', 'neutral', 'mixed']:
            c = sentiments.get(s, 0)
            r = c / health_count
            print(f"    {s:10s}: {c:4d} ({r*100:.1f}%) → ~{int(FULL_CORPUS_SIZE*hr*r):,} in corpus")

        pos, neg = sentiments.get('positive', 0), sentiments.get('negative', 0)
        print(f"\n  {'='*50}")
        print(f"  ★ POSITIVE-TO-NEGATIVE RATIO: {pos/neg:.1f}:1" if neg > 0 else f"  ★ No negative health comments found")
        pos_r = pos/health_count*100
        neg_r = neg/health_count*100
        print(f"  Among health-related: {pos_r:.1f}% positive, {neg_r:.1f}% negative")
        print(f"  {'='*50}")


def save_summary_csv(gpt4o, gpt41, common_ids):
    path = os.path.join(RESULTS_DIR, "absa_merged_summary.csv")
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['sample_id', 'channel', 'comment_excerpt',
                     'gpt4o_health', 'gpt4o_sentiment', 'gpt4o_aspects',
                     'gpt41_health', 'gpt41_sentiment', 'gpt41_aspects',
                     'consensus_health', 'consensus_sentiment'])
        for sid in sorted(common_ids, key=lambda x: int(x)):
            r4o, r41 = gpt4o.get(sid, {}), gpt41.get(sid, {})
            a4o = '; '.join(f"{a['aspect']}({a['sentiment']})" for a in r4o.get('health_aspects',[]) if isinstance(a,dict))
            a41 = '; '.join(f"{a['aspect']}({a['sentiment']})" for a in r41.get('health_aspects',[]) if isinstance(a,dict))
            h4o, h41 = r4o.get('health_related',False), r41.get('health_related',False)
            s4o, s41 = r4o.get('overall_health_sentiment',''), r41.get('overall_health_sentiment','')
            w.writerow([sid, r4o.get('channel',''), r4o.get('comment_text','')[:150],
                        h4o, s4o, a4o, h41, s41, a41,
                        'yes' if h4o and h41 else ('no' if not h4o and not h41 else 'disagree'),
                        s4o if s4o == s41 else 'disagree'])
    print(f"\n✓ Merged summary → {path}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    assert API_KEY, "Set your API key: os.environ['OPENAI_API_KEY'] = 'sk-proj-...'"

    sample = load_sample()

    # --- PART 1: Run both models ---
    print(f"\n{'='*60}")
    print("PART 1: RUNNING ABSA MODELS")
    print(f"{'='*60}")

    print(f"\n▶ GPT-4o")
    run_model("gpt-4o", sample)

    print(f"\n▶ GPT-4.1")
    run_model("gpt-4.1", sample)

    # --- PART 2: Analysis ---
    print(f"\n\n{'='*60}")
    print("PART 2: ANALYSIS")
    print(f"{'='*60}")

    # Auto-detect result files
    gpt4o_file = gpt41_file = None
    for fn in os.listdir(RESULTS_DIR):
        if 'gpt_4o' in fn and fn.endswith('.jsonl'): gpt4o_file = fn
        elif ('gpt_4_1' in fn or 'gpt_41' in fn) and fn.endswith('.jsonl'): gpt41_file = fn

    gpt4o = load_results(gpt4o_file)
    gpt41 = load_results(gpt41_file)

    common_ids, both_health = compute_agreement(gpt4o, gpt41)

    if common_ids:
        sentiment_distributions(gpt4o, gpt41, common_ids)
        consensus_analysis(gpt4o, gpt41, common_ids)
        extrapolation(gpt4o, gpt41, common_ids)
        save_summary_csv(gpt4o, gpt41, common_ids)
        print(f"\n{'='*60}")
        print("ALL DONE! Download absa_results/ folder for your records.")
        print(f"{'='*60}")
    else:
        print("\n⚠ No valid results to analyse.")
