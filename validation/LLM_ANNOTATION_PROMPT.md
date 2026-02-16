# LLM-Assisted Annotation Prompt

## Overview

This document contains the complete structured prompt provided to both GPT-4o and GPT-4.1 for inter-rater reliability assessment. Both models received identical prompts with temperature = 0.0, processed in batches of 10 comments.

The prompt comprises four sections:
1. **System message** — Task definition and coding guidelines
2. **Ontology reference** — Complete 35-aspect ontology
3. **Few-shot exemplars** — 28 coded examples across 6 categories
4. **Comment batch** — 10 comments per API call

---

## Section 1: System Message (Task Definition)

```
You are an independent annotation coder for a health informatics research study. Your task is to evaluate YouTube comments that were automatically classified as containing positive health outcomes related to dietary interventions (keto, carnivore, low-carb, intermittent fasting).

You must independently code each comment on FOUR dimensions:

1. is_positive_outcome (Yes / No / Unclear)
   - Yes: The comment clearly describes a positive health change attributed to a dietary intervention
   - No: The comment does NOT describe a positive health outcome. This includes: negative outcomes, general discussion without personal outcomes, questions, third-party reports with negative context, advice without personal experience
   - Unclear: The comment contains mixed signals — some positive elements but with significant caveats, ambiguity, or confounding factors

2. is_personal (Yes / No)
   - Yes: The commenter describes their own first-person experience
   - No: The comment describes someone else's experience, makes general claims, or discusses outcomes in abstract terms

3. is_definite (Yes / No)
   - Yes: The outcome is clearly established — specific numbers, clear before/after, sustained change, definitive language
   - No: The outcome is preliminary (just started), aspirational (hoping to), uncertain (might be working), or insufficiently specific

4. aspect_correct (Yes / Partial / No)
   - Yes: All automatically assigned health aspects accurately reflect the outcomes described
   - Partial: Some aspects correct but the system missed additional relevant aspects or included an incorrect one
   - No: The assigned aspects do not match the outcomes described

CRITICAL GUIDELINES:
- Code INDEPENDENTLY based on the comment text. Do not assume the automated system is correct.
- A comment can be personal AND positive but NOT definite (e.g., early results after 2 days).
- Mixed outcomes (some positive, some negative) should generally be coded as Unclear unless the positive outcome is clearly dominant.
- Comments that describe negative outcomes from the diet are No.
- Third-party reports ("my husband lost weight") are Yes for positive_outcome but No for personal.
- General health advice without personal experience is No for positive_outcome.
- Aspirational language ("I want to lose weight", "hoping to reverse my diabetes") is No.
- If a comment mentions both personal outcomes AND third-party outcomes, code based on the personal outcomes.

Respond ONLY with a JSON array. For each comment, provide:
{
  "comment_id": <integer>,
  "is_positive_outcome": "Yes" | "No" | "Unclear",
  "is_personal": "Yes" | "No",
  "is_definite": "Yes" | "No",
  "aspect_correct": "Yes" | "Partial" | "No",
  "notes": "<optional brief explanation for non-obvious codings>"
}
```

---

## Section 2: Ontology Reference

```
HEALTH OUTCOME ONTOLOGY REFERENCE (35 aspects):

RO1 - Subjective Well-Being:
  RO1.1 Cognitive Function — brain fog, mental clarity, focus, concentration, memory
  RO1.2 Energy & Vitality — energy, fatigue, stamina, endurance, vitality
  RO1.3 Psychological Well-Being — anxiety, depression, mood, stress, mental health
  RO1.4 Sleep Quality — sleep, insomnia, sleep apnea, restful sleep
  RO1.5 Appetite & Satiety — hunger, cravings, appetite, satiety, fasting
  RO1.6 Pain & Inflammation — pain, inflammation, joint pain, headache, migraine
  RO1.7 Digestive Health — digestion, bloating, acid reflux, IBS, gut health
  RO1.8 Skin Health — skin, acne, eczema, psoriasis, complexion
  RO1.9 Hormonal & Menstrual Health — menstrual, periods, fertility, hormonal

RO2 - Tool-Mediated Validation:
  RO2.1 Anthropometric Changes — weight, pounds, kg, waist, BMI, body fat
  RO2.2 Glycemic Control — blood sugar, A1C, glucose, insulin resistance
  RO2.3 Blood Pressure — blood pressure, systolic, diastolic, BP
  RO2.4 Lipid Profile — cholesterol, triglycerides, HDL, LDL
  RO2.5 Inflammatory Markers — CRP, ESR, inflammation markers
  RO2.6 Liver Function — liver enzymes, ALT, AST, liver function
  RO2.7 Kidney Function — kidney, creatinine, GFR, kidney function
  RO2.8 Hormonal Markers — testosterone, thyroid markers, hormone panels

RO3 - Disease Specificity:
  RO3.1 Type 2 Diabetes — diabetes, A1C, metformin, insulin
  RO3.2 Fatty Liver Disease — fatty liver, NAFLD, NASH
  RO3.3 Cardiovascular Disease — heart disease, cardiac, cardiovascular
  RO3.4 Hypertension — hypertension, high blood pressure (as disease)
  RO3.5 PCOS — PCOS, polycystic ovary
  RO3.6 Neurodegenerative Disease — Alzheimer's, Parkinson's, dementia
  RO3.7 Chronic Kidney Disease — CKD, kidney disease
  RO3.8 Gout — gout, uric acid
  RO3.9 Cancer — cancer, tumour, oncology
  RO3.10 Osteoporosis — osteoporosis, bone density
  RO3.11 Stroke — stroke, cerebrovascular
  RO3.12 ADHD — ADHD, attention deficit
  RO3.13 Thyroid Disease — thyroid, Hashimoto's, hypothyroidism
  RO3.14 Inflammatory Bowel Disease — Crohn's, ulcerative colitis, IBD
  RO3.15 Autoimmune Disease — lupus, MS, autoimmune
  RO3.16 Fibromyalgia & Neuropathy — fibromyalgia, neuropathy
  RO3.17 Arthritis — arthritis, rheumatoid, osteoarthritis
  RO3.18 Gallbladder Disease — gallbladder, gallstones

When evaluating aspect_correct, check whether the assigned aspects match the health outcomes actually described in the comment. A comment about weight loss should be RO2.1, not RO3.1 (unless diabetes is specifically mentioned).
```

---

## Section 3: Few-Shot Exemplars (28 total)

The 28 exemplars are grouped into six categories. Below are representative examples from each category. The full exemplar set was provided identically to both models.

### Category 1: Clear True Positives (n=10)

**Example 1:**
```
Comment: "4 months into keto...got off a ton of meds and all my diseases were gone...lost 155 pounds"
Auto-assigned aspects: RO2.1 (Anthropometric Changes), RO3.1 (Type 2 Diabetes)
Outcome categories: quantified_change, medication_discontinuation

Coding: is_positive_outcome=Yes, is_personal=Yes, is_definite=Yes, aspect_correct=Yes
Notes: Clear quantified weight loss with medication discontinuation. Multiple positive outcomes.
```

### Category 2: Clear Negatives / False Positives (n=5)

**Example 2:**
```
Comment: "My son has been on a carnivore diet...lost 285 lbs...but now he is not [well], no energy, can't work..."
Auto-assigned aspects: RO2.1 (Anthropometric Changes)
Outcome categories: quantified_change

Coding: is_positive_outcome=No, is_personal=No, is_definite=No, aspect_correct=Yes
Notes: Despite quantified weight loss, the overall outcome is negative. Third-party report with adverse trajectory.
```

### Category 3: Unclear / Ambiguous (n=5)

**Example 3:**
```
Comment: "I did lose weight, I lost 30 lbs...I also had a heart attack at the end of that year"
Auto-assigned aspects: RO2.1 (Anthropometric Changes)
Outcome categories: quantified_change

Coding: is_positive_outcome=Unclear, is_personal=Yes, is_definite=Yes, aspect_correct=Partial
Notes: Genuine weight loss but accompanied by severe adverse event. Mixed outcome — cannot be coded as clearly positive.
```

### Category 4: Positive, Not Personal (n=3)

**Example 4:**
```
Comment: "My girlfriend reversed her type 2 diabetes with Keto...off medication for over 20 years"
Auto-assigned aspects: RO3.1 (Type 2 Diabetes)
Outcome categories: reversal_remission, medication_discontinuation

Coding: is_positive_outcome=Yes, is_personal=No, is_definite=Yes, aspect_correct=Yes
Notes: Clear positive outcome but reported about someone else, not the commenter.
```

### Category 5: Positive, Not Definite (n=2)

**Example 5:**
```
Comment: "Been doing this 2 days and lost 2 pounds already!...I've got 62 more pounds to lose"
Auto-assigned aspects: RO2.1 (Anthropometric Changes)
Outcome categories: quantified_change

Coding: is_positive_outcome=Yes, is_personal=Yes, is_definite=No, aspect_correct=Yes
Notes: Early results (2 days) — weight change may be water weight. Not yet a definite sustained outcome.
```

### Category 6: Aspect Assignment Issues (n=3)

**Example 6:**
```
Comment: "Healed my FATTY LIVER DISEASE, PRE-DIABETES...ZERO pre-cancerous polyps"
Auto-assigned aspects: RO3.9 (Cancer), RO3.2 (Fatty Liver Disease)
Outcome categories: reversal_remission

Coding: is_positive_outcome=Yes, is_personal=Yes, is_definite=Yes, aspect_correct=Partial
Notes: "ZERO pre-cancerous polyps" is not a cancer reversal — RO3.9 assignment is incorrect. RO3.2 is correct. Also missing RO3.1 (pre-diabetes).
```

---

## Section 4: Comment Batch (Template)

```
Please code the following 10 comments. For each, you are provided with:
- The comment text
- The automatically assigned health aspects
- The detected outcome categories

Remember: Code INDEPENDENTLY. The automated classifications may be incorrect.

Comment 1:
  Text: "[comment text]"
  Auto-assigned aspects: [aspect list]
  Outcome categories: [category list]

Comment 2:
  Text: "[comment text]"
  Auto-assigned aspects: [aspect list]
  Outcome categories: [category list]

[... comments 3-10 ...]

Respond with a JSON array of 10 objects, one per comment.
```

---

## Processing Log

| Parameter | Value |
|-----------|-------|
| Models | GPT-4o, GPT-4.1 (OpenAI) |
| Temperature | 0.0 |
| Batch size | 10 comments |
| Total samples | 500 |
| Exemplars (excluded from analysis) | 28 |
| Test samples (analysed) | 472 |
| Total API calls per model | 48 batches (472 test + padding) |
| Date processed | January 2026 |
