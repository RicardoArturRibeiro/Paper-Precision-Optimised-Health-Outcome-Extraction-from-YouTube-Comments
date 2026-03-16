# Precision-Optimized Health Outcome Extraction from YouTube Comments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A computational framework for extracting self-reported positive health outcomes from user-generated YouTube comments using ontology-driven rule-based classification.**

> **Correction Notice (March 2026):** The corpus was corrected from 209,661 records to 43,111 unique comments after discovering that the YouTube Data API v3 returned duplicate records during pagination. All result files, figures, and statistics have been updated. Validation metrics (precision 97.6%) remain unchanged. See [`REVISION_CHANGELOG.md`](REVISION_CHANGELOG.md) for full details.

## Overview

This repository accompanies the paper:

> Ribeiro, R. & Zutshi, A. (2026). A Precision-Optimized Framework for Extracting Self-Reported Health Outcomes from User-Generated Content: A Large-Scale Analysis of YouTube Comments. *Journal of Medical Internet Research (JMIR)*.

The framework analyses YouTube comments on metabolic health content (Therapeutic Carbohydrate Restriction) and identifies self-reported positive health outcomes with **97.6% precision** (95% CI: 95.7%–98.6%). It classifies outcomes across 35 health aspects organised under three research objectives: Subjective Well-Being (RO1), Tool-Mediated Validation (RO2), and Disease Specificity (RO3).

### Key Results

| Metric | Value | 95% CI |
|--------|-------|--------|
| Precision | 97.6% | 95.7% – 98.6% |
| Recall | 20.7% | 14.8% – 29.0% |
| F1-Score | 33.8% | — |
| Corpus Size | 43,111 unique comments | — |
| Classified Positives | 1,790 | — |
| Estimated True Positives | 1,747 | 1,713 – 1,764 |

## Repository Structure

```
├── README.md                          # This file
├── CITATION.cff                       # Citation metadata
├── LICENSE                            # MIT License
│
│   ── Phase 1: Exploratory Data Analysis ──────────────────────
│
├── data_collection/                   # Data collection scripts
│   └── README.md                      # Instructions for corpus reconstruction
│
│   ── Phase 2: Ontology Development ───────────────────────────
│
├── ontology/                          # Health outcome ontology (35 aspects)
│   ├── final_ontology.csv             # Complete ontology with keywords & exclusions
│   └── ONTOLOGY_CODEBOOK.md           # Ontology documentation & aspect definitions
│
│   ── Phase 3: Classification & Validation ────────────────────
│
├── classification/                    # Classification pipeline
│   ├── outcome_indicators.csv         # 110 positive outcome regex patterns
│   ├── exclusion_patterns.csv         # 45 exclusion filter regex patterns
│   └── scripts/                       # Python scripts (Phases 1–3)
│       ├── phase1_eda.py              # EDA
│       ├── phase1_eda_v2.py           # EDA (extended)
│       ├── phase2_corpus_exploration.py    # Corpus exploration
│       ├── phase2_lda_topic_modelling.py  # LDA topic modelling
│       ├── phase2_ngram_extraction.py     # N-gram extraction
│       ├── phase2_ontology_testing.py     # Ontology testing
│       ├── phase2_ontology_refinement.py  # Ontology refinement
│       ├── phase2_final_documentation.py  # Final documentation
│       ├── phase3_outcome_indicators.py   # Outcome indicator development
│       ├── phase3_full_classification.py  # Full corpus classification
│       ├── phase3_validation_sample.py    # Validation sample generation
│       ├── phase3_statistical_analysis.py # Statistical analysis & figures
│       └── phase3_ml_comparison.py        # ML baseline comparison
│
├── validation/                        # Validation protocol & results
│   ├── VALIDATION_PROTOCOL.md         # Detailed validation procedures
│   ├── LLM_ANNOTATION_PROMPT.md       # Complete LLM coding prompt (Appendix C)
│   ├── validation_coded.xlsx          # 500-sample precision validation (de-identified)
│   ├── validation_coding_sheet.xlsx   # Blank coding sheet template
│   └── recall_estimation_sample.xlsx  # 105-sample recall estimation (de-identified)
│
├── results/                           # Classification outputs & statistics
│   ├── summary_statistics.csv         # Overall framework metrics
│   ├── aspect_statistics.csv          # Per-aspect classification statistics
│   ├── channel_analysis.csv           # Per-channel analysis with CIs
│   ├── category_statistics.csv        # Outcome category distribution
│   ├── positive_outcomes.csv          # Full classified corpus (1,790 outcomes)
│   └── sample_classifications.csv     # 5,000-comment sample with all fields
│
│   ── Phase 4: Aspect-Based Sentiment Analysis (ABSA) ────────
│
├── absa/                              # Dual-model ABSA validation
│   ├── README.md                      # ABSA documentation
│   ├── absa_colab.py                  # Google Colab ABSA pipeline script
│   ├── absa_sample.csv               # Stratified sample input
│   ├── absa_gpt_4o.jsonl             # GPT-4o ABSA output
│   └── absa_gpt_4_1.jsonl            # GPT-4.1 ABSA output
│
│   ── Supporting Materials ────────────────────────────────────
│
├── figures/                           # Paper figures (high-resolution)
│   ├── fig1_framework_architecture.png
│   ├── fig2_ro_overview.png
│   ├── fig3_top10_aspects.png
│   ├── fig4_channel_comparison.png
│   ├── fig5_outcome_categories.png
│   └── fig6_summary_dashboard.png
│
└── supplementary/                     # Additional outputs by phase
    ├── phase1_eda/                    # Phase 1 EDA outputs
    │   ├── lda_topics.csv
    │   ├── topic_distribution.csv
    │   ├── bigrams.csv
    │   └── representative_comments.csv
    ├── phase2_development/            # Phase 2 ontology development outputs
    │   ├── health_bigrams.csv
    │   ├── health_trigrams.csv
    │   ├── ro_ngrams.csv
    │   ├── outcome_examples.csv
    │   ├── ontology_structure.csv
    │   ├── coverage_stats.csv
    │   ├── refined_coverage.csv
    │   └── sample_matches.csv
    └── phase3_classification/         # Phase 3 additional outputs
        ├── channel_statistics.csv
        └── positive_outcomes_sample.csv
```

## Quick Start

### Requirements

- Python 3.9+
- Required packages: `pandas`, `numpy`, `scikit-learn`, `nltk`, `gensim`, `matplotlib`, `seaborn`, `scipy`

```bash
pip install pandas numpy scikit-learn nltk gensim matplotlib seaborn scipy openpyxl
```

### Running the Classification Pipeline

The pipeline assumes a comment corpus CSV with columns: `video_id`, `channel_name`, `comment_text`.

```bash
# Phase 1: Exploratory Data Analysis
python classification/scripts/phase1_eda.py --input data/comments.csv

# Phase 2: Ontology Development & Testing
python classification/scripts/phase2_ontology_testing.py --input data/comments.csv
python classification/scripts/phase2_ontology_refinement.py --input data/comments.csv

# Phase 3: Full Classification
python classification/scripts/phase3_full_classification.py \
    --input data/comments.csv \
    --ontology ontology/final_ontology.csv \
    --indicators classification/outcome_indicators.csv \
    --exclusions classification/exclusion_patterns.csv

# Phase 3: Statistical Analysis & Figures
python classification/scripts/phase3_statistical_analysis.py
```

### Data Availability

The raw YouTube comment corpus **cannot be redistributed** in accordance with the YouTube API Terms of Service (Section III.E.4). However:

- Data collection scripts are provided in `data_collection/` for corpus reconstruction using the YouTube Data API v3
- The classified outputs (1,790 positive outcomes) are provided in `results/positive_outcomes.csv`
- Validation codings are provided in de-identified form in `validation/`

## Ontology

The health outcome ontology comprises 35 aspects under three research objectives:

| RO | Description | Aspects | Example Aspects |
|----|-------------|---------|-----------------|
| RO1 | Subjective Well-Being | 9 | Cognitive Function, Energy & Vitality, Pain & Inflammation |
| RO2 | Tool-Mediated Validation | 8 | Anthropometric Changes, Glycemic Control, Blood Pressure |
| RO3 | Disease Specificity | 18 | Type 2 Diabetes, Fatty Liver Disease, PCOS, Arthritis |

Total: 520 keywords, 35 aspects. See `ontology/ONTOLOGY_CODEBOOK.md` for full documentation.

## Classification Pipeline

The three-stage pipeline maximises precision through conservative, layered filtering:

1. **Stage 1 — Health Content Detection:** Keyword matching against the 35-aspect ontology vocabulary
2. **Stage 2 — Outcome Indicator Detection:** 110 regex patterns across 6 categories (quantified change, symptom cessation, reversal/remission, medication discontinuation, explicit improvement, temporal improvement)
3. **Stage 3 — Exclusion Filtering:** 45 regex patterns across 6 categories (questions, negation, third-party references, future intent, general statements, engagement only)

## Aspect-Based Sentiment Analysis (ABSA)

A dual-model ABSA approach using GPT-4o and GPT-4.1 was applied to a stratified sample of classified comments to extract fine-grained aspect-sentiment pairs. This provides independent validation of the ontology-driven classification and enables granular analysis of sentiment polarity per health aspect. See `absa/README.md` for details.

## Validation

| Assessment | Method | Result |
|-----------|--------|--------|
| Precision | Manual coding (n=500) | 97.6% (95% CI: 95.7%–98.6%) |
| Recall | Negative sampling (n=105) | 20.7% (95% CI: 14.8%–29.0%) |
| IRR: Human vs. GPT-4o | PABAK | 0.673 (Substantial) |
| IRR: Human vs. GPT-4.1 | PABAK | 0.741 (Substantial) |
| IRR: GPT-4o vs. GPT-4.1 | Cohen's κ | 0.771 (Substantial) |

See `validation/VALIDATION_PROTOCOL.md` for detailed procedures and `validation/LLM_ANNOTATION_PROMPT.md` for the complete LLM coding prompt.

## Citation

If you use this framework, ontology, or dataset in your research, please cite:

```bibtex
@article{ribeiro2026precision,
  title={A Precision-Optimized Framework for Extracting Self-Reported Health Outcomes from User-Generated Content: A Large-Scale Analysis of YouTube Comments},
  author={Ribeiro, Ricardo and Zutshi, Aneesh},
  journal={Journal of Medical Internet Research},
  year={2026},
  doi={[pending]}
}
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

The YouTube comment data is subject to the [YouTube API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service) and cannot be redistributed in bulk.

## Contact

- **Ricardo Ribeiro** — UNIDEMI, Department of Mechanical and Industrial Engineering, NOVA School of Science and Technology, Universidade NOVA de Lisboa, Caparica 2829-516, Portugal — rasi.ribeiro@campus.fct.unl.pt
- **Aneesh Zutshi** — UNIDEMI, Department of Mechanical and Industrial Engineering, NOVA School of Science and Technology, Universidade NOVA de Lisboa, Caparica 2829-516, Portugal; LASI, 4800-058 Guimarães, Portugal — aneesh@fct.unl.pt
