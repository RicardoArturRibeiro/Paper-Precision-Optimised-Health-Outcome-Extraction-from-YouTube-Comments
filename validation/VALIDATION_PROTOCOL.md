# Validation Protocol

## Overview

This document describes the three-component validation protocol used to assess the classification framework's performance: (1) precision validation through manual coding, (2) recall estimation through negative sampling, and (3) inter-rater reliability assessment through LLM-assisted annotation.

## 1. Precision Validation

### 1.1 Sampling Design

- **Population:** 6,671 comments classified as positive health outcomes
- **Sample size:** n = 500
- **Confidence level:** 95%
- **Margin of error:** 4%
- **Stratification:** Proportional by research objective (RO1, RO2, RO3)
- **Sampling method:** Stratified random sampling

### 1.2 Coding Dimensions

Each comment was coded on four structured dimensions plus free-text notes:

| Dimension | Values | Definition |
|-----------|--------|------------|
| `is_positive_outcome` | Yes / No / Unclear | Does this comment report a positive health outcome? |
| `is_personal` | Yes / No | Is this a first-person personal testimony? |
| `is_definite` | Yes / No | Is the outcome definite and established (not preliminary or aspirational)? |
| `aspect_correct` | Yes / Partial / No | Did the automated system correctly assign the health aspect(s)? |
| `notes` | Free text | Qualitative observations, error descriptions, edge cases |

### 1.3 Coding Guidelines

**is_positive_outcome:**
- **Yes:** The comment clearly describes a positive health change attributed to a dietary intervention
- **No:** The comment does not describe a positive health outcome (false positive) — includes negative outcomes, general discussion, questions, third-party reports with negative context
- **Unclear:** The comment contains mixed signals — some positive elements but with caveats, ambiguity, or confounding factors

**is_personal:**
- **Yes:** The commenter is describing their own first-person experience ("I lost 30 pounds", "My blood sugar dropped")
- **No:** The comment describes someone else's experience ("My husband reversed his diabetes", "She lost weight") or makes general claims

**is_definite:**
- **Yes:** The outcome is clearly established — specific numbers, clear before/after, sustained change
- **No:** The outcome is preliminary ("just started and already feeling better"), aspirational, or insufficiently specific

**aspect_correct:**
- **Yes:** All automatically assigned aspects accurately reflect the health outcomes described
- **Partial:** Some aspects are correct but the system missed additional relevant aspects or included an incorrect one
- **No:** The assigned aspects do not match the outcomes described in the comment

### 1.4 Precision Calculation

```
Precision = True Positives / (True Positives + False Positives)
```

Comments coded as "Yes" or "Unclear" on `is_positive_outcome` were counted as true positives. Comments coded as "No" were counted as false positives. Confidence intervals were computed using the Wilson score method (Wilson, 1927).

### 1.5 Output Files

- `validation_coded.xlsx` — The 500 coded samples with all dimension codings (de-identified: no author identifiers)
- `validation_coding_sheet.xlsx` — Blank coding template

---

## 2. Recall Estimation

### 2.1 Sampling Design

- **Population:** 202,990 comments NOT classified as positive outcomes
- **Sample size:** n = 105
- **Stratification:** By channel (proportional to non-classified comments per channel)
- **Sampling method:** Stratified random sampling

### 2.2 Coding Procedure

Each non-classified comment was reviewed by the human coder to determine whether it contained a genuine positive health outcome that the classification system missed (false negative).

### 2.3 Recall Calculation

```
False Negative Rate = False Negatives / n
Estimated Total FN = False Negative Rate × Total Non-Classified
Estimated True Positives = Precision × Classified Positives
Recall = Estimated TP / (Estimated TP + Estimated Total FN)
```

### 2.4 Output Files

- `recall_estimation_sample.xlsx` — The 105 coded non-classified samples

---

## 3. Inter-Rater Reliability (LLM-Assisted Annotation)

### 3.1 Design

Two independent LLM coders (GPT-4o and GPT-4.1, OpenAI) served as second annotators. Both received identical structured prompts containing:

1. Task definition with coding guidelines for all four structured dimensions
2. Complete 35-aspect ontology reference
3. 28 few-shot exemplars with human ground-truth codings
4. Comment text with automated classification details (but NOT human manual codings)

### 3.2 Few-Shot Exemplar Selection

28 exemplars were selected through purposive stratified sampling across six categories:

| Category | n | Purpose |
|----------|---|---------|
| Clear true positive | 10 | Anchor correct positive identification |
| Clear negative (FP) | 5 | Prevent blanket positive bias |
| Unclear/ambiguous | 5 | Model boundary-case reasoning |
| Positive, not personal | 3 | Distinguish personal vs. third-party |
| Positive, not definite | 2 | Distinguish definite vs. preliminary |
| Aspect assignment issue | 3 | Model aspect correctness evaluation |

### 3.3 Processing Parameters

| Parameter | Value |
|-----------|-------|
| Temperature | 0.0 (deterministic) |
| Batch size | 10 comments |
| Test samples | 472 (500 minus 28 exemplars) |
| Output format | JSON array with four dimensions + optional notes |

### 3.4 Anti-Anchoring Measures

1. Exemplars deliberately span all six coding categories, including negatives and errors
2. Prompt instructs models to "code INDEPENDENTLY based on the comment text"
3. Prompt states the automated system's classification may be incorrect
4. Deterministic output ensures reproducibility

### 3.5 Agreement Metrics

| Metric | Purpose |
|--------|---------|
| Raw agreement (%) | Simple proportion of matching codings |
| Cohen's κ | Chance-corrected agreement |
| PABAK | Prevalence-Adjusted Bias-Adjusted Kappa — corrects for kappa paradox in imbalanced datasets |

Interpretation follows Landis & Koch (1977): Slight (0.00–0.20), Fair (0.21–0.40), Moderate (0.41–0.60), Substantial (0.61–0.80), Almost Perfect (0.81–1.00).

### 3.6 Comparison Pairs

1. Human vs. GPT-4o
2. Human vs. GPT-4.1
3. GPT-4o vs. GPT-4.1 (cross-model convergence)

### 3.7 Complete LLM Prompt

See `LLM_ANNOTATION_PROMPT.md` for the full prompt as provided to both models.

---

## References

- Byrt, T., Bishop, J., & Carlin, J. B. (1993). Bias, prevalence and kappa. *Journal of Clinical Epidemiology*, 46(5), 423–429.
- Cicchetti, D. V., & Feinstein, A. R. (1990). High agreement but low kappa: II. Resolving the paradoxes. *Journal of Clinical Epidemiology*, 43(6), 551–558.
- Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *PNAS*, 120(30), e2305016120.
- Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174.
- Törnberg, P. (2023). ChatGPT-4 outperforms experts and crowd workers in annotating political Twitter messages. *arXiv [cs.CL]*.
- Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA*, 22(158), 209–212.
