# Self-Reported Health Outcomes in Metabolic Health YouTube Comments: Rule-Based NLP Framework Development and Validation Study

> **Status:** Revised manuscript resubmitted to *Journal of Medical Internet Research* (JMIR), Manuscript #94855

## Overview

This repository contains the code, ontology, validation protocols, and reproducibility artefacts for a precision-optimised computational framework that extracts self-reported positive health outcomes from YouTube comments on metabolic health channels.

From a corpus of **43,111 unique comments** across 11 Therapeutic Carbohydrate Restriction (TCR) channels (37,458 unique authors; November 2013 – January 2026), the framework classified **1,790 positive health outcome reports** spanning 35 health aspects and 18 named disease conditions.

## Key Metrics

| Metric | Value | 95% CI |
|--------|-------|--------|
| Precision (n=500) | **97.6%** | 95.7% – 98.6% |
| Recall (n=510) | **56.2%** | 43.4% – 67.9% |
| Estimated true positives | 1,747 | 1,713 – 1,764 |
| External validation precision (n=243) | **93.4%** | 89.6% – 95.9% |
| External validation recall | 50.1% | 31.4% – 59.1% |

## Core Components

### Three-Stage Classification Pipeline
1. **Health Content Detection** — keyword matching against a 35-aspect hierarchical ontology (520 keywords)
2. **Outcome Indicator Detection** — 110 regex patterns across six categories (quantified change, symptom cessation, reversal/remission, medication discontinuation, explicit improvement, temporal improvement)
3. **Exclusion Filtering** — 45 patterns minimising false positives (questions, negation, third-party, hypothetical, general statements, engagement-only)

### Ontology Structure
Outcomes are organised under three Research Objectives:
- **RO1 – Subjective Well-Being** (9 aspects): cognitive function, energy, psychological well-being, sleep, appetite, pain, digestive health, skin health, hormonal health
- **RO2 – Tool-Mediated Validation** (8 aspects): anthropometric changes, glycaemic control, blood pressure, lipid profile, inflammatory markers, liver function, kidney function, hormonal markers
- **RO3 – Disease Specificity** (18 aspects): type 2 diabetes, fatty liver, cardiovascular disease, hypertension, PCOS, neurodegenerative disease, CKD, gout, cancer, osteoporosis, stroke, ADHD, thyroid disease, IBD, autoimmune disease, fibromyalgia, arthritis, gallbladder disease

### Validation Programme
Five complementary validation studies:
1. **Precision validation** — stratified random sample (n=500), manual coding on 5 dimensions
2. **Recall estimation** — stratified negative sampling (n=510) across 3 comment-length strata and 11 channels
3. **External validation** — 12,653 comments from 5 held-out channels with zero overlap with development corpus
4. **Inter-rater reliability** — LLM-assisted annotation (GPT-4o, GPT-4.1) with bias audit; Cohen κ and percent agreement as primary metrics
5. **Transformer baseline comparison** — BERT-base-uncased and RoBERTa-base fine-tuned on same data (n=836); both achieved higher recall but lower precision, confirming the rule-based precision advantage

### Supplementary Analysis
- **Aspect-Based Sentiment Analysis (ABSA)** — dual-model (GPT-4o, GPT-4.1) consensus coding on 1,003 stratified comments; positive-to-negative ratio of 4.6:1

## Repository Structure

```
├── absa/                    # ABSA prompt, scripts, and results
├── classification/          # Classification pipeline and scripts
├── data_collection/         # YouTube Data API v3 collection scripts
├── figures/                 # Paper figures (high resolution, 300 DPI)
├── ontology/                # 35-aspect health outcome ontology
├── results/                 # Classification outputs and statistics
├── supplementary/           # Phase-specific outputs
├── validation/              # Validation protocols, coding sheets, results
├── CITATION.cff             # Citation metadata
├── LICENSE                  # MIT License
├── README.md                # This file
└── REVISION_CHANGELOG.md    # Revision history
```

## Data Availability

The raw YouTube comment corpus cannot be redistributed under the YouTube Data API v3 Terms of Service. Data collection scripts are provided to enable corpus reconstruction. Classified outputs (1,790 positive outcomes with aspect assignments) are publicly available in `results/`.

## Citation

```
Ribeiro R, Zutshi A. Self-Reported Health Outcomes in Metabolic Health YouTube
Comments: Rule-Based NLP Framework Development and Validation Study. J Med
Internet Res. 2026 (under review). Manuscript #94855.
```

## License

MIT License applies to code and documentation. YouTube data is governed by Google's API Terms of Service.
