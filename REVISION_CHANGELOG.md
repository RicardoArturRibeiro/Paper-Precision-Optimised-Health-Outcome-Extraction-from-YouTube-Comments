# Revision Changelog: JMIR ms#94855

## Revision 3 (April 2026) — Minor Formatting Revision

Five formatting and structural changes requested by the editor (no scientific concerns). Submitted 19 April 2026.

### Changes Applied
- **Title updated** — Added "Cross-Sectional Study of" to the title per editor request. Full title: "Self-Reported Health Outcomes in Metabolic Health YouTube Comments: Cross-Sectional Study of Rule-Based NLP Framework Development and Validation."
- **IMRD format enforced** — "Discussion" heading added; all content now falls strictly within Introduction, Methods, Results, and Discussion sections.
- **Table 13 relocated** — Moved from Discussion to the end of the Results section (after the transformer baseline comparison paragraph).
- **Discussion restructured** — Rewritten to follow: (a) Principal Findings, (b) Comparison With Prior Work, (c) Limitations, (d) Conclusions. Numeric findings removed from Discussion except for one direct literature comparison (97.6% vs 80–90%).
- **Unreferenced statements addressed** — 9 Discussion/Conclusions statements cited with 8 new references [50]–[57]. "The first validated" softened to "to our knowledge, the first validated." Reference list now [1]–[57].
- **Word count trimmed** — Four targeted cuts in Discussion brought body text from 10,074 to 9,993 words (under the 10,000-word limit).
- **JMIR compliance audit** — British spellings converted to American English (90 instances), Latin abbreviations standardized (eg, ie), chi-square values rounded to 1 decimal, statistical notation spacing fixed (n=, N=), OR/CI formatting corrected, ± notation replaced with SD format in Appendix F.

---

## Revision 2 (April 2026) — Response to Peer Review

Addresses all comments from the editor and two external peer reviewers. Changes span methodology, validation, results, and discussion.

### Major Additions
- **Expanded recall estimation** — Sample increased from n=105 to n=510 (stratified by comment length across 11 channels). Recall estimate revised from 20.7% to 56.2% (95% CI 43.4%–67.9%).
- **External validation on held-out channels** — 12,653 comments from 5 independent channels with zero development overlap. Precision: 93.4% (95% CI 89.6%–95.9%); recall: 50.1% (95% CI 31.4%–59.1%). Reported in Multimedia Appendix E.
- **Transformer baseline comparison** — BERT-base-uncased and RoBERTa-base fine-tuned on combined validation dataset (n=836). Both achieved higher recall but lower precision, confirming the rule-based precision advantage. Reported in Multimedia Appendix F.
- **LLM bias audit** — Full confusion matrices and McNemar tests for GPT-4o and GPT-4.1 against human coder. Reported in Multimedia Appendix H.

### Metric Changes (Revision 1 → Revision 2)

| Metric | Revision 1 | Revision 2 |
|--------|-----------|-----------|
| Recall sample size | n=105 | n=510 |
| Recall estimate | 20.7% | 56.2% |
| Recall 95% CI | 11.6%–23.6% | 43.4%–67.9% |
| Inter-rater primary metric | PABAK | Cohen κ + % agreement |
| External validation | Not conducted | 93.4% precision (n=12,653) |
| Transformer baseline | Not conducted | BERT 87.0%P / RoBERTa 88.2%P |
| References | [1]–[46] | [1]–[49] |

### Unchanged from Revision 1
- Classification precision: 97.6% (488/500)
- Corpus size: 43,111 unique comments
- Positive outcomes classified: 1,790
- 35-aspect ontology framework
- Rule-based classification methodology
- ABSA results (4.6:1 positive-to-negative ratio)

### Discussion and Framing Changes
- Removed clinical-level claims and advocacy language
- Channel-level interpretations labeled as "interpretive hypotheses"
- All disease-specific counts presented as "self-reported" with caveats

### Additional Changes
- Title revised to JMIR format
- Abstract expanded to 450 words with all required elements
- Ethical Considerations, Funding, and AI Disclosure sections added
- Table/Figure captions expanded to be self-contained
- Figure 1: new framework architecture diagram (300 DPI)
- Wilson score 95% CIs added for all point estimates
- Limitations expanded (viral content bias, reply thread exclusion, construct validity)
- CREMLS checklist completed (Multimedia Appendix G)

---

## Revision 1 (March 2026) — Corpus Deduplication Correction

YouTube Data API v3 pagination with relevance-based ordering produced duplicate records. After deduplication, the corpus shrank from 209,661 to **43,111 unique comments** (a 4.86× inflation factor).

### Key Metric Changes

| Metric | Original | Corrected | Impact |
|--------|----------|-----------|--------|
| Corpus size | 209,661 | 43,111 | −79.4% |
| Positive outcomes | 6,671 | 1,790 | −73.2% |
| Prevalence | 3.18% | 4.15% | +0.97pp |
| Recall estimate | 16.5% | 20.7% | +4.2pp |
| Chi-square | 3,509 | 927.5 | Recalculated |

### Unchanged Elements
- Classification precision (97.6%)
- 35-aspect ontology framework
- Rule-based methodology
- All qualitative interpretation
