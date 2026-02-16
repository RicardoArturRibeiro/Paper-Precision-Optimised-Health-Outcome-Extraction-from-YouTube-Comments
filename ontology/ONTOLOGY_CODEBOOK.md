# Ontology Codebook

## Health Outcome Ontology — Version 1.0

This document describes the 35-aspect health outcome ontology used for classifying self-reported positive health outcomes in YouTube comments on metabolic health content.

## Structure

The ontology is organised under three **Research Objectives (ROs)**:

| RO | Name | Aspects | Description |
|----|------|---------|-------------|
| RO1 | Subjective Well-Being | 9 | Self-reported improvements in quality of life, symptoms, and subjective health status |
| RO2 | Tool-Mediated Validation | 8 | Outcomes verified through measurement tools, clinical tests, or quantification |
| RO3 | Disease Specificity | 18 | Improvements in named medical conditions |

**Total:** 35 aspects, 520 keywords

## File Format

The ontology is provided in `final_ontology.csv` with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `ro_id` | String | Research objective ID (RO1, RO2, RO3) |
| `ro_name` | String | Research objective name |
| `aspect_id` | String | Aspect identifier (e.g., RO1.3, RO2.1) |
| `aspect_name` | String | Human-readable aspect name |
| `keywords` | String | Semicolon-separated keyword list for matching |
| `exclusions` | String | Semicolon-separated exclusion terms (redirects to more specific aspects) |
| `num_keywords` | Integer | Total keyword count for this aspect |

## Aspect Definitions

### RO1 — Subjective Well-Being (9 aspects)

| ID | Name | Description | Keywords (n) |
|----|------|-------------|-------------|
| RO1.1 | Cognitive Function | Mental clarity, focus, concentration, memory improvements | 19 |
| RO1.2 | Energy & Vitality | Energy levels, fatigue reduction, stamina improvements | 19 |
| RO1.3 | Psychological Well-Being | Mood, anxiety, depression, stress, emotional well-being | 22 |
| RO1.4 | Sleep Quality | Sleep improvements, insomnia resolution, sleep apnea changes | 18 |
| RO1.5 | Appetite & Satiety | Hunger control, cravings, satiety, appetite changes | 15 |
| RO1.6 | Pain & Inflammation | Pain reduction, inflammation, headaches, joint/back pain | 24 |
| RO1.7 | Digestive Health | GI improvements, bloating, acid reflux, IBS symptoms | 18 |
| RO1.8 | Skin Health | Skin improvements, acne, eczema, psoriasis, complexion | 16 |
| RO1.9 | Hormonal & Menstrual Health | Menstrual regularity, fertility, hormonal balance | 15 |

### RO2 — Tool-Mediated Validation (8 aspects)

| ID | Name | Description | Keywords (n) |
|----|------|-------------|-------------|
| RO2.1 | Anthropometric Changes | Weight loss, BMI, waist circumference, body composition | 28 |
| RO2.2 | Glycemic Control | Blood sugar, A1C, fasting glucose, insulin resistance | 21 |
| RO2.3 | Blood Pressure | Blood pressure readings, hypertension management | 12 |
| RO2.4 | Lipid Profile | Cholesterol, triglycerides, HDL, LDL improvements | 14 |
| RO2.5 | Inflammatory Markers | CRP, ESR, inflammation marker changes | 8 |
| RO2.6 | Liver Function | Liver enzyme changes, ALT, AST improvements | 8 |
| RO2.7 | Kidney Function | Kidney markers, creatinine, GFR changes | 6 |
| RO2.8 | Hormonal Markers | Testosterone, thyroid markers, hormone panels | 8 |

### RO3 — Disease Specificity (18 aspects)

| ID | Name | Description | Keywords (n) |
|----|------|-------------|-------------|
| RO3.1 | Type 2 Diabetes | Diabetes reversal, A1C normalisation, metformin discontinuation | 15 |
| RO3.2 | Fatty Liver Disease | NAFLD/NASH improvement, liver fat reduction | 8 |
| RO3.3 | Cardiovascular Disease | Heart disease improvement, cardiac markers | 8 |
| RO3.4 | Hypertension | Blood pressure normalisation, medication reduction | 7 |
| RO3.5 | PCOS | Polycystic ovary syndrome improvements | 6 |
| RO3.6 | Neurodegenerative Disease | Alzheimer's, Parkinson's, dementia improvements | 8 |
| RO3.7 | Chronic Kidney Disease | CKD stage improvement, kidney function markers | 6 |
| RO3.8 | Gout | Gout flare reduction, uric acid improvements | 5 |
| RO3.9 | Cancer | Cancer-related outcomes, tumour markers | 6 |
| RO3.10 | Osteoporosis | Bone density, osteoporosis improvements | 5 |
| RO3.11 | Stroke | Stroke recovery, cerebrovascular improvements | 4 |
| RO3.12 | ADHD | Attention deficit improvements, focus, concentration | 5 |
| RO3.13 | Thyroid Disease | Thyroid function, Hashimoto's, hypothyroidism | 7 |
| RO3.14 | Inflammatory Bowel Disease | Crohn's, ulcerative colitis, IBD improvements | 7 |
| RO3.15 | Autoimmune Disease | Lupus, MS, autoimmune condition improvements | 8 |
| RO3.16 | Fibromyalgia & Neuropathy | Fibromyalgia, neuropathy, chronic pain conditions | 7 |
| RO3.17 | Arthritis | Rheumatoid arthritis, osteoarthritis improvements | 6 |
| RO3.18 | Gallbladder Disease | Gallbladder function, gallstone-related outcomes | 5 |

## Exclusion Logic

Exclusion terms redirect keyword matches to more specific disease aspects. For example:

- A comment mentioning "pain" + "arthritis" → classified under **RO3.17 (Arthritis)**, not RO1.6 (Pain & Inflammation)
- A comment mentioning "blood sugar" + "diabetes" → classified under **RO3.1 (Type 2 Diabetes)**, not RO2.2 (Glycemic Control)
- A comment mentioning "anxiety" + "adhd" → classified under **RO3.12 (ADHD)**, not RO1.3 (Psychological Well-Being)

This ensures that disease-specific outcomes are not double-counted under general symptom categories.

## Matching Rules

1. All keyword matching is **case-insensitive**
2. Keywords are matched as substrings within the comment text
3. A comment can match **multiple aspects** simultaneously (aspects are not mutually exclusive)
4. Exclusion terms are checked after keyword matching — if an exclusion term is present, the match is redirected
5. The ontology is applied at **Stage 1** of the three-stage classification pipeline; Stages 2 (outcome indicators) and 3 (exclusion filters) provide additional filtering

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01 | Initial release accompanying paper submission |
