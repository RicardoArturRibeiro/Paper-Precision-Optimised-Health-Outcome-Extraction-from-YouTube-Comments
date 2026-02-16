# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 3 - Health-Related N-gram Extraction
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script extracts bigrams and trigrams from the corpus to discover
# multi-word health terms and outcome phrases. These patterns will inform
# the keyword lists for the ontology.
#
# Outputs:
# 1. Console output with n-gram analysis (copy/paste to Claude)
# 2. CSV files with health-related bigrams and trigrams
# 3. Outcome phrase patterns for each Research Objective
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 3 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk scikit-learn -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from datetime import datetime
import warnings

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk import ngrams

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Google Colab specific
from google.colab import drive

# Configure settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 200)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 3 - Health-Related N-gram Extraction")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & Configuration
# ==============================================================================

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    """Load the corpus with multiple fallback strategies."""
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
        {'name': 'Python engine latin-1', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'latin-1'}}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:60]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)

if df is None:
    raise FileNotFoundError("Could not load corpus. Check file path.")

print(f"\nTotal comments loaded: {len(df):,}")


# ==============================================================================
# CELL 4: Text Preprocessing
# ==============================================================================

print("\n" + "=" * 70)
print("2. TEXT PREPROCESSING")
print("=" * 70)

def clean_text_for_ngrams(text):
    """
    Clean text while preserving important health-related patterns.
    Less aggressive than LDA preprocessing to keep context.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Standardize common health terms
    text = re.sub(r'\ba1c\b', 'a1c', text)
    text = re.sub(r'\bhba1c\b', 'a1c', text)
    text = re.sub(r'\bt2d\b', 'type 2 diabetes', text)
    text = re.sub(r'\bt2dm\b', 'type 2 diabetes', text)
    text = re.sub(r'\btype 2\b', 'type 2 diabetes', text)
    text = re.sub(r'\bbp\b', 'blood pressure', text)
    text = re.sub(r'\bibs\b', 'irritable bowel syndrome', text)
    text = re.sub(r'\bnafld\b', 'fatty liver', text)
    text = re.sub(r'\bnash\b', 'fatty liver', text)
    text = re.sub(r'\bpcos\b', 'polycystic ovary syndrome', text)
    text = re.sub(r'\bif\b', 'intermittent fasting', text)

    # Keep important punctuation for sentence boundaries
    text = re.sub(r'[^\w\s\'-]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

print("🔄 Cleaning text...")
df['clean_text'] = df['comment_text'].apply(clean_text_for_ngrams)
print("✅ Text cleaning complete")


# ==============================================================================
# CELL 5: Define Health-Related Seed Terms for Filtering
# ==============================================================================

print("\n" + "=" * 70)
print("3. DEFINING HEALTH-RELATED SEED TERMS")
print("=" * 70)

# These terms will be used to filter n-grams to health-relevant ones
health_seeds = {
    # Body parts & systems
    'body', 'blood', 'brain', 'heart', 'liver', 'kidney', 'gut', 'stomach',
    'skin', 'joint', 'muscle', 'nerve', 'eye', 'hair', 'nail', 'bone',

    # Symptoms & feelings
    'pain', 'ache', 'tired', 'fatigue', 'energy', 'sleep', 'mood', 'anxiety',
    'depression', 'stress', 'fog', 'focus', 'memory', 'hungry', 'craving',
    'bloat', 'inflammation', 'swelling', 'headache', 'migraine',

    # Measurements & markers
    'weight', 'pound', 'lbs', 'kg', 'glucose', 'sugar', 'insulin', 'a1c',
    'cholesterol', 'triglyceride', 'ldl', 'hdl', 'pressure', 'level',

    # Conditions & diseases
    'diabetes', 'diabetic', 'prediabetes', 'cancer', 'disease', 'syndrome',
    'arthritis', 'thyroid', 'autoimmune', 'gout', 'fibromyalgia', 'pcos',
    'hypertension', 'obesity', 'overweight',

    # Outcomes & changes
    'lost', 'lose', 'dropped', 'reversed', 'cured', 'healed', 'improved',
    'better', 'worse', 'gone', 'away', 'normal', 'healthy', 'sick',

    # Diet & intervention terms
    'diet', 'fasting', 'keto', 'carnivore', 'carb', 'low', 'high',

    # Negation & outcome indicators
    'no', 'not', 'never', 'without', 'free', 'off', 'stopped', 'quit'
}

print(f"Defined {len(health_seeds)} health-related seed terms for filtering")


# ==============================================================================
# CELL 6: Extract Bigrams
# ==============================================================================

print("\n" + "=" * 70)
print("4. EXTRACTING BIGRAMS")
print("=" * 70)

# Minimal stopwords to preserve context
minimal_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                     'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
                     'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
                     'did', 'will', 'would', 'could', 'should', 'may', 'might',
                     'this', 'that', 'these', 'those', 'it', 'its'}

def extract_ngrams(text, n=2):
    """Extract n-grams from text."""
    tokens = text.split()
    # Filter very short tokens
    tokens = [t for t in tokens if len(t) > 1]
    return list(ngrams(tokens, n))

print("🔄 Extracting bigrams from all comments...")
all_bigrams = []
for text in df['clean_text']:
    if text:
        all_bigrams.extend(extract_ngrams(text, 2))

print(f"Total bigrams extracted: {len(all_bigrams):,}")

# Count bigrams
bigram_counts = Counter(all_bigrams)

# Filter to health-related bigrams (at least one word matches a seed)
health_bigrams = {}
for bigram, count in bigram_counts.items():
    word1, word2 = bigram
    # Check if either word contains a health seed
    is_health = False
    for seed in health_seeds:
        if seed in word1 or seed in word2:
            is_health = True
            break

    # Also check if neither word is just a stopword
    if is_health and word1 not in minimal_stopwords and word2 not in minimal_stopwords:
        health_bigrams[bigram] = count

# Sort by frequency
health_bigrams_sorted = sorted(health_bigrams.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- Top 80 Health-Related Bigrams ---\n")
for i, (bigram, count) in enumerate(health_bigrams_sorted[:80], 1):
    print(f"{i:3}. {bigram[0]} {bigram[1]}: {count:,}")


# ==============================================================================
# CELL 7: Extract Trigrams
# ==============================================================================

print("\n" + "=" * 70)
print("5. EXTRACTING TRIGRAMS")
print("=" * 70)

print("🔄 Extracting trigrams from all comments...")
all_trigrams = []
for text in df['clean_text']:
    if text:
        all_trigrams.extend(extract_ngrams(text, 3))

print(f"Total trigrams extracted: {len(all_trigrams):,}")

# Count trigrams
trigram_counts = Counter(all_trigrams)

# Filter to health-related trigrams
health_trigrams = {}
for trigram, count in trigram_counts.items():
    word1, word2, word3 = trigram
    # Check if any word contains a health seed
    is_health = False
    for seed in health_seeds:
        if seed in word1 or seed in word2 or seed in word3:
            is_health = True
            break

    # Filter out if all words are stopwords
    non_stop = [w for w in trigram if w not in minimal_stopwords]
    if is_health and len(non_stop) >= 2:
        health_trigrams[trigram] = count

# Sort by frequency
health_trigrams_sorted = sorted(health_trigrams.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- Top 60 Health-Related Trigrams ---\n")
for i, (trigram, count) in enumerate(health_trigrams_sorted[:60], 1):
    print(f"{i:3}. {' '.join(trigram)}: {count:,}")


# ==============================================================================
# CELL 8: Extract Outcome Patterns
# ==============================================================================

print("\n" + "=" * 70)
print("6. EXTRACTING OUTCOME PATTERNS")
print("=" * 70)

# Define outcome pattern seeds
outcome_patterns = {
    'positive_change': ['lost', 'reversed', 'cured', 'healed', 'improved',
                        'better', 'gone', 'away', 'normal', 'dropped', 'down'],
    'negation_positive': ['no more', 'no longer', 'not anymore', 'never again',
                          'don\'t have', 'went away', 'is gone', 'are gone',
                          'got rid', 'free of', 'off my'],
    'quantity_change': ['lost', 'dropped', 'down', 'went from', 'reduced']
}

# Search for specific outcome phrases in the corpus
print("🔄 Searching for outcome patterns...")

outcome_examples = {
    'weight_loss': [],
    'blood_sugar': [],
    'pain_relief': [],
    'energy_gain': [],
    'disease_reversal': [],
    'symptom_gone': []
}

# Patterns to search
search_patterns = [
    (r'lost \d+ (pound|lb|kg)', 'weight_loss'),
    (r'dropped \d+ (pound|lb|kg)', 'weight_loss'),
    (r'down \d+ (pound|lb|kg)', 'weight_loss'),
    (r'(a1c|glucose|blood sugar).{0,30}(dropped|down|normal|improved)', 'blood_sugar'),
    (r'(no more|no longer).{0,20}(pain|ache|hurt)', 'pain_relief'),
    (r'pain.{0,20}(gone|away|disappeared|stopped)', 'pain_relief'),
    (r'(more|increased|so much).{0,10}energy', 'energy_gain'),
    (r'energy.{0,20}(back|returned|improved)', 'energy_gain'),
    (r'reversed.{0,20}(diabetes|diabetic|type 2)', 'disease_reversal'),
    (r'(cured|healed).{0,20}(diabetes|fatty liver|condition)', 'disease_reversal'),
    (r'off.{0,10}(medication|insulin|metformin|statin)', 'disease_reversal'),
    (r'(brain fog|inflammation|bloating|headache).{0,20}(gone|away|stopped)', 'symptom_gone'),
    (r'(no more|no longer).{0,20}(brain fog|inflammation|bloating|headache)', 'symptom_gone')
]

# Sample comments for pattern matching
sample_size = min(50000, len(df))
sample_df = df.sample(n=sample_size, random_state=42)

for _, row in sample_df.iterrows():
    text = str(row['comment_text']).lower()
    for pattern, category in search_patterns:
        if re.search(pattern, text):
            if len(outcome_examples[category]) < 20:  # Keep max 20 examples each
                outcome_examples[category].append(text[:300])

print("\n--- Outcome Pattern Examples ---\n")
for category, examples in outcome_examples.items():
    print(f"\n📌 {category.upper().replace('_', ' ')} ({len(examples)} examples found):")
    for ex in examples[:3]:
        print(f"  • {ex[:150]}...")


# ==============================================================================
# CELL 9: Research Objective Specific N-grams
# ==============================================================================

print("\n" + "=" * 70)
print("7. RESEARCH OBJECTIVE SPECIFIC N-GRAMS")
print("=" * 70)

# Define RO-specific seed terms
ro_seeds = {
    'RO1': {  # Subjective Well-Being
        'seeds': ['energy', 'tired', 'fatigue', 'sleep', 'mood', 'anxiety',
                  'depression', 'brain', 'fog', 'focus', 'pain', 'ache',
                  'inflammation', 'gut', 'bloat', 'skin', 'craving', 'hungry',
                  'headache', 'migraine', 'joint', 'digest'],
        'bigrams': [],
        'trigrams': []
    },
    'RO2': {  # Tool-Mediated Validation
        'seeds': ['weight', 'pound', 'lost', 'glucose', 'sugar', 'a1c',
                  'insulin', 'cholesterol', 'triglyceride', 'ldl', 'hdl',
                  'pressure', 'liver', 'kidney', 'blood', 'level', 'test'],
        'bigrams': [],
        'trigrams': []
    },
    'RO3': {  # Disease Specificity
        'seeds': ['diabetes', 'diabetic', 'prediabetes', 'cancer', 'disease',
                  'syndrome', 'arthritis', 'thyroid', 'autoimmune', 'gout',
                  'fibromyalgia', 'pcos', 'hypertension', 'alzheimer', 'dementia',
                  'stroke', 'heart', 'fatty', 'nafld', 'ibs', 'crohn', 'colitis'],
        'bigrams': [],
        'trigrams': []
    }
}

# Filter bigrams and trigrams by RO
for bigram, count in health_bigrams_sorted[:500]:
    bigram_str = f"{bigram[0]} {bigram[1]}"
    for ro, data in ro_seeds.items():
        for seed in data['seeds']:
            if seed in bigram[0] or seed in bigram[1]:
                data['bigrams'].append((bigram_str, count))
                break

for trigram, count in health_trigrams_sorted[:500]:
    trigram_str = ' '.join(trigram)
    for ro, data in ro_seeds.items():
        for seed in data['seeds']:
            if seed in trigram[0] or seed in trigram[1] or seed in trigram[2]:
                data['trigrams'].append((trigram_str, count))
                break

# Display RO-specific n-grams
for ro, data in ro_seeds.items():
    print(f"\n{'='*50}")
    print(f"📌 {ro} N-GRAMS")
    print(f"{'='*50}")

    # Remove duplicates while preserving order
    seen_bi = set()
    unique_bigrams = []
    for item in data['bigrams']:
        if item[0] not in seen_bi:
            seen_bi.add(item[0])
            unique_bigrams.append(item)

    seen_tri = set()
    unique_trigrams = []
    for item in data['trigrams']:
        if item[0] not in seen_tri:
            seen_tri.add(item[0])
            unique_trigrams.append(item)

    print(f"\nTop Bigrams ({len(unique_bigrams)} unique):")
    for phrase, count in unique_bigrams[:20]:
        print(f"  • {phrase}: {count:,}")

    print(f"\nTop Trigrams ({len(unique_trigrams)} unique):")
    for phrase, count in unique_trigrams[:15]:
        print(f"  • {phrase}: {count:,}")


# ==============================================================================
# CELL 10: Export Results
# ==============================================================================

print("\n" + "=" * 70)
print("8. EXPORTING RESULTS")
print("=" * 70)

# Export 1: All health bigrams
bigrams_df = pd.DataFrame([
    {'bigram': f"{b[0]} {b[1]}", 'frequency': c}
    for b, c in health_bigrams_sorted[:500]
])
bigrams_df.to_csv(f'{OUTPUT_DIR}Phase2_Script3_health_bigrams.csv', index=False)
print(f"✅ Exported: Phase2_Script3_health_bigrams.csv ({len(bigrams_df)} bigrams)")

# Export 2: All health trigrams
trigrams_df = pd.DataFrame([
    {'trigram': ' '.join(t), 'frequency': c}
    for t, c in health_trigrams_sorted[:500]
])
trigrams_df.to_csv(f'{OUTPUT_DIR}Phase2_Script3_health_trigrams.csv', index=False)
print(f"✅ Exported: Phase2_Script3_health_trigrams.csv ({len(trigrams_df)} trigrams)")

# Export 3: RO-specific n-grams
ro_ngrams = []
for ro, data in ro_seeds.items():
    for phrase, count in data['bigrams'][:50]:
        ro_ngrams.append({'RO': ro, 'type': 'bigram', 'phrase': phrase, 'frequency': count})
    for phrase, count in data['trigrams'][:30]:
        ro_ngrams.append({'RO': ro, 'type': 'trigram', 'phrase': phrase, 'frequency': count})

ro_ngrams_df = pd.DataFrame(ro_ngrams)
ro_ngrams_df.to_csv(f'{OUTPUT_DIR}Phase2_Script3_RO_ngrams.csv', index=False)
print(f"✅ Exported: Phase2_Script3_RO_ngrams.csv")

# Export 4: Outcome examples
outcome_data = []
for category, examples in outcome_examples.items():
    for ex in examples:
        outcome_data.append({'category': category, 'example': ex})
outcome_df = pd.DataFrame(outcome_data)
outcome_df.to_csv(f'{OUTPUT_DIR}Phase2_Script3_outcome_examples.csv', index=False)
print(f"✅ Exported: Phase2_Script3_outcome_examples.csv")


# ==============================================================================
# CELL 11: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("9. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 3 - N-GRAM EXTRACTION RESULTS
============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. EXTRACTION STATISTICS
------------------------
Total bigrams extracted: {len(all_bigrams):,}
Health-related bigrams: {len(health_bigrams):,}
Total trigrams extracted: {len(all_trigrams):,}
Health-related trigrams: {len(health_trigrams):,}

2. TOP 50 HEALTH-RELATED BIGRAMS
--------------------------------""")

for i, (bigram, count) in enumerate(health_bigrams_sorted[:50], 1):
    print(f"{i:2}. {bigram[0]} {bigram[1]}: {count:,}")

print(f"""

3. TOP 40 HEALTH-RELATED TRIGRAMS
---------------------------------""")

for i, (trigram, count) in enumerate(health_trigrams_sorted[:40], 1):
    print(f"{i:2}. {' '.join(trigram)}: {count:,}")

print(f"""

4. RO1 (SUBJECTIVE WELL-BEING) KEY PHRASES
------------------------------------------""")
seen = set()
for phrase, count in ro_seeds['RO1']['bigrams'][:25]:
    if phrase not in seen:
        seen.add(phrase)
        print(f"  • {phrase}: {count:,}")

print(f"""

5. RO2 (TOOL-MEDIATED VALIDATION) KEY PHRASES
---------------------------------------------""")
seen = set()
for phrase, count in ro_seeds['RO2']['bigrams'][:25]:
    if phrase not in seen:
        seen.add(phrase)
        print(f"  • {phrase}: {count:,}")

print(f"""

6. RO3 (DISEASE SPECIFICITY) KEY PHRASES
----------------------------------------""")
seen = set()
for phrase, count in ro_seeds['RO3']['bigrams'][:25]:
    if phrase not in seen:
        seen.add(phrase)
        print(f"  • {phrase}: {count:,}")

print(f"""

7. OUTCOME PATTERN COUNTS
-------------------------""")
for category, examples in outcome_examples.items():
    print(f"  {category}: {len(examples)} examples found")

print(f"""

8. FILES EXPORTED
-----------------
- Phase2_Script3_health_bigrams.csv (500 bigrams)
- Phase2_Script3_health_trigrams.csv (500 trigrams)
- Phase2_Script3_RO_ngrams.csv (RO-specific phrases)
- Phase2_Script3_outcome_examples.csv (example comments)

9. KEY MULTI-WORD TERMS FOR ONTOLOGY
------------------------------------
Based on this analysis, consider adding these multi-word terms:

RO1 Keywords to Add:
- brain fog, joint pain, back pain, knee pain
- sleep better, more energy, no more pain
- skin tag, gut health, mental health

RO2 Keywords to Add:
- blood sugar, blood pressure, blood test
- lost weight, lose weight, weight loss
- cholesterol level, insulin level, glucose level
- fatty liver, liver function

RO3 Keywords to Add:
- type 2 diabetes, heart disease, heart attack
- fatty liver disease, kidney disease
- autoimmune disease, thyroid disease

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 3 Complete")
print("=" * 70)
