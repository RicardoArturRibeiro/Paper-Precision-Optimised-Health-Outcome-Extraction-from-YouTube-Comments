# Precision-Optimized Health Outcome Extraction from YouTube Comments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A computational framework for extracting self-reported positive health outcomes from user-generated YouTube comments using ontology-driven rule-based classification.**

## Overview

This repository accompanies the paper:

> Ribeiro, R. & Zutshi, A. (2026). A Precision-Optimized Framework for Extracting Self-Reported Health Outcomes from User-Generated Content: A Large-Scale Analysis of YouTube Comments. *[Journal Name]*.

The framework analyses YouTube comments on metabolic health content (Therapeutic Carbohydrate Restriction) and identifies self-reported positive health outcomes with **97.6% precision** (95% CI: 95.7%–98.6%). It classifies outcomes across 35 health aspects organised under three research objectives: Subjective Well-Being (RO1), Tool-Mediated Validation (RO2), and Disease Specificity (RO3).

### Key Results

| Metric | Value | 95% CI |
|--------|-------|--------|
| Precision | 97.6% | 95.7% – 98.6% |
| Recall | 16.5% | 11.6% – 23.6% |
| F1-Score | 28.3% | — |
| Corpus Size | 209,661 comments | — |
| Classified Positives | 6,671 | — |
| Estimated True Positives | 6,510 | 6,384 – 6,577 |

## Repository Structure

```
├── README.md                          # This file
├── CITATION.cff                       # Citation metadata
├── LICENSE                            # MIT License
│
├── ontology/                          # Health outcome ontology (35 aspects)
│   ├── final_ontology.csv             # Complete ontology with keywords & exclusions
│   └── ONTOLOGY_CODEBOOK.md           # Ontology documentation & aspect definitions
│
├── classification/                    # Classification pipeline
│   ├── outcome_indicators.csv         # 110 positive outcome regex patterns
│   ├── exclusion_patterns.csv         # 45 exclusion filter regex patterns
│   └── scripts/                       # Python classification scripts
│       ├── phase1_eda.py              # Phase 1: Exploratory Data Analysis
│       ├── phase1_eda_v2.py           # Phase 1: EDA (extended version)
│       ├── phase2_corpus_exploration.py    # Phase 2: Corpus exploration
│       ├── phase2_lda_topic_modelling.py  # Phase 2: LDA topic modelling
│       ├── phase2_ngram_extraction.py     # Phase 2: N-gram extraction
│       ├── phase2_ontology_testing.py     # Phase 2: Ontology testing
│       ├── phase2_ontology_refinement.py  # Phase 2: Ontology refinement
│       ├── phase2_final_documentation.py  # Phase 2: Final documentation
│       ├── phase3_outcome_indicators.py   # Phase 3: Outcome indicator development
│       ├── phase3_full_classification.py  # Phase 3: Full corpus classification
│       ├── phase3_validation_sample.py    # Phase 3: Validation sample generation
│       ├── phase3_statistical_analysis.py # Phase 3: Statistical analysis & figures
│       └── phase3_ml_comparison.py        # Phase 3: ML baseline comparison
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
│   ├── positive_outcomes.csv          # Full classified corpus (6,671 outcomes)
│   └── sample_classifications.csv     # 5,000-comment sample with all fields
│
├── figures/                           # Paper figures (high-resolution)
│   ├── fig1_framework_architecture.png
│   ├── fig2_ro_overview.png
│   ├── fig3_top10_aspects.png
│   ├── fig4_channel_comparison.png
│   ├── fig5_outcome_categories.png
│   └── fig6_summary_dashboard.png
│
├── data_collection/                   # Data collection scripts
│   └── README.md                      # Instructions for corpus reconstruction
│
└── supplementary/                     # Additional materials
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
- The classified outputs (6,671 positive outcomes) are provided in `results/positive_outcomes.csv`
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

## Validation

| Assessment | Method | Result |
|-----------|--------|--------|
| Precision | Manual coding (n=500) | 97.6% (95% CI: 95.7%–98.6%) |
| Recall | Negative sampling (n=105) | 16.5% (95% CI: 11.6%–23.6%) |
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
  journal={[Journal Name]},
  year={2026},
  doi={[DOI]}
}
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

The YouTube comment data is subject to the [YouTube API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service) and cannot be redistributed in bulk.

## Contact

- **Ricardo Ribeiro** — UNIDEMI, Department of Mechanical and Industrial Engineering, NOVA School of Science and Technology, NOVA University Lisbon, Caparica 2829-516, Portugal
