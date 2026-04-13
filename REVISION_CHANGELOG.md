# Revision Changelog: JMIR ms#94855

## Revision 2 (April 2026) — Response to Peer Review

This revision addresses all comments from the editor and two external peer reviewers (Reviewer S and Reviewer BG). The changes are substantial and span methodology, validation, results, and discussion.

### Major Additions

#### 1. Expanded Recall Estimation (Reviewer S, Point 3)
- **Previous:** n=105 negative sample, recall estimate 20.7%
- **Revised:** n=510 stratified sample (short <50 words: n=300; medium 50–150: n=150; long >150: n=60) with proportional allocation across 11 channels
- **New result:** Recall 56.2% (95% CI 43.4%–67.9%), 27 false negatives identified
- Channel-level recall variation now reported (χ²(10)=28.76, P=.001)
- Comment-length variation now reported (χ²(2)=19.36, P<.001)

#### 2. External Validation on Held-Out Channels (Reviewer S, Point 4)
- 12,653 comments from 5 independent channels (Georgia Ede MD, Robert Kiltz MD, Sten Ekberg DC, Chris Palmer MD, Ted Naiman MD)
- Zero overlap with development corpus; channels selected by independent co-author
- Precision: 93.4% (227/243; 95% CI 89.6%–95.9%)
- Recall: 50.1% (95% CI 31.4%–59.1%)
- Reported in new Multimedia Appendix E

#### 3. Transformer Baseline Comparison (Reviewer S, Point 7)
- BERT-base-uncased and RoBERTa-base fine-tuned on combined validation dataset (n=836; 347 positive, 489 negative)
- Stratified five-fold cross-validation
- BERT: precision 87.0%, recall 93.4%; RoBERTa: precision 88.2%, recall 95.7%
- Confirms rule-based precision advantage for high-confidence corpus generation
- Reported in new Multimedia Appendix F

#### 4. LLM Bias Audit (Reviewer S, Point 2)
- Full confusion matrices between each LLM and human coder
- Systematic directional bias characterised (both LLMs stricter than human coder)
- McNemar tests: P<.001 (GPT-4o) and P=.048 (GPT-4.1)
- Reported in new Multimedia Appendix H

### Metric Changes (Revision 1 → Revision 2)

| Metric | Revision 1 | Revision 2 | Note |
|--------|-----------|-----------|------|
| Recall sample size | n=105 | n=510 | Expanded per reviewer request |
| Recall estimate | 20.7% | 56.2% | Stratified weighted estimation |
| Recall 95% CI | 11.6%–23.6% | 43.4%–67.9% | Tighter with larger sample |
| Inter-rater primary metric | PABAK | Cohen κ + % agreement | PABAK removed from primary table |
| External validation | Not conducted | 93.4% precision (n=12,653) | New validation study |
| Transformer baseline | Not conducted | BERT 87.0%P / RoBERTa 88.2%P | New comparison |
| References | 1–46 | 1–49 | Three reviewer-cited papers added |

### Unchanged from Revision 1
- Classification precision: 97.6% (488/500)
- Corpus size: 43,111 unique comments
- Positive outcomes classified: 1,790
- 35-aspect ontology framework
- Rule-based classification methodology
- ABSA results (4.6:1 positive-to-negative ratio)

### Discussion and Framing Changes (Reviewer S, Points 5–6)
- Removed "rival or exceed clinical trials" and all clinical-level claims
- Removed advocacy language ("democratising access...")
- Channel-level interpretations explicitly labelled as "interpretive hypotheses"
- All disease-specific counts now presented as "self-reported" with caveats

### Additional Changes
- **Title:** Revised to JMIR format ("Issue in Condition: Method/Study Design")
- **Abstract:** Expanded to full 450 words with all required elements
- **Ethical Considerations:** Dedicated subsection addressing all 5 JMIR-required points
- **Funding:** Separate section distinct from Acknowledgements
- **AI Disclosure:** Dedicated "Use of AI/LLM" section
- **Table/Figure captions:** All expanded to be self-contained
- **Figure 1:** New framework architecture diagram (300 DPI PNG)
- **Confidence intervals:** Wilson score 95% CIs for all point estimates
- **Statistics format:** P-values uppercase, CI format per JMIR guidelines
- **Limitations:** New subsections on viral content bias, reply thread exclusion, construct validity
- **Healthcasting term:** Justified with explicit rationale for compound term adoption
- **References updated:** Added [47] Cao et al. 2025 (PROBAST bias framework), [48] Xu et al. 2026 (LLM annotation shifts), [49] Ding et al. 2025 (ML/DL trade-offs)
- **Video metadata:** Durations reported (range 19s–115.8min, mean 23.3min); short-form videos (n=13) noted
- **Content creator credentials:** Table 1 expanded with degree-granting institutions
- **CREMLS checklist:** Completed in Multimedia Appendix G

---

## Revision 1 (March 2026) — Corpus Deduplication Correction

### Core Issue
The study discovered that YouTube Data API v3's pagination with relevance-based ordering produced duplicate records. After deduplication, the corpus shrank from 209,661 to **43,111 unique comments** (a 4.86× inflation factor).

### Key Metric Changes

| Metric | Original | Corrected | Impact |
|--------|----------|-----------|--------|
| Corpus size | 209,661 | 43,111 | −79.4% |
| Positive outcomes | 6,671 | 1,790 | −73.2% |
| Prevalence | 3.18% | 4.15% | +0.97pp |
| Recall estimate | 16.5% | 20.7% | +4.2pp |
| Chi-square | 3,509 | 927.51 | Recalculated |

### Unchanged Elements
- Classification precision (97.6%)
- 35-aspect ontology framework
- Rule-based methodology
- All qualitative interpretation
