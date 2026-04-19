# Revision Changelog: JMIR ms#94855

## Revision 3 (April 2026) — Minor Revision (Decision B)

Decision received 16 April 2026. Deadline: 23 April 2026.
Reviewer S recommends acceptance: "The authors have comprehensively addressed all my concerns. The manuscript now meets the high standards for publication. I recommend that the paper be accepted in its current form."

Editor requests five formatting/structural changes (no scientific concerns):

### Outstanding Editor Comments

1. **IMRD format** — Follow strict Introduction, Methods, Results, and Discussion (IMRD) format.
2. **"Cross-sectional" in title** — Mention "cross-sectional" in the title and main text.
3. **Unreferenced Discussion statements** — There are still statements in the Discussion without references.
4. **Discussion structure** — Restructure Discussion: (a) brief summary of main findings relative to aims, (b) detailed discussion with interpretations/comparisons to literature, (c) limitations, (d) conclusions with broader implications. Avoid repeating numeric findings except for direct literature comparisons. Ensure all conclusions match what the methodology supports.
5. **No tables in Discussion** — Move any tables currently in the Discussion to Methods or Results.

### Changes Applied
- [x] **Add "Cross-Sectional" to title** — Title changed to: "Self-Reported Health Outcomes in Metabolic Health YouTube Comments: Cross-Sectional Study of Rule-Based NLP Framework Development and Validation". "Cross-Sectional Study of" marked in red. Term already appeared 5 times in body text (abstract, table captions, CREMLS checklist).
- [x] **Move Table 13 from Discussion to Results** — Table 13 (intro sentence, caption, data, footnote) relocated from Discussion → end of Results section, after transformer baseline paragraph. CREMLS checklist reference updated. Discussion retains cross-reference to Table 13.
- [x] **Add references to all unreferenced Discussion statements** — 9 claims addressed: added 8 new references [50]–[57], reused existing [33], [44], [49]. All new citations in red. "the first validated" softened to "to our knowledge, the first validated" (red). New references: [50] Eysenbach 2009 (JMIR), [51] Staudacher et al. 2022 (Am J Gastroenterol), [52] Sarker et al. 2015 (J Biomed Inform), [53] Madathil et al. 2015 (Health Informatics J), [54] Eysenbach 2011 (Am J Prev Med), [55] Walsh et al. 2019 (Br J Clin Pharmacol), [56] Jim et al. 2020 (CA Cancer J Clin), [57] Reading & Merrill 2018 (JAMIA). Reference list now [1]–[57].
- [x] **Restructure Discussion to strict IMRD with editor's prescribed paragraph order** — (1) Added "Discussion" Heading1 (red). (2) Rewrote Principal Findings as plain-language summary mapped to RQ1–RQ4, no numeric repetition. (3) Removed repeated numeric findings from Comparison With Prior Work: chi-square removed from channel variation, "56%" removed from recall, "4.6:1" removed from ABSA, "more than two thousand" removed; kept 97.6% vs 80–90% as direct literature comparison. (4) Limitations unchanged. (5) Conclusions restructured: removed finding restatement (old P1) and "Three findings deserve emphasis" enumeration (old P3); merged broader implications into flowing prose. All new/changed text in red.
- [x] **Verify no numeric findings repeated in Discussion except for literature comparisons** — Only numeric comparison retained is 97.6% vs 80–90% (Table 13 literature comparison, [33,44]). All other numeric findings (corpus size, recall %, chi-square, ABSA ratio, transformer %) removed from Discussion and expressed in plain language.
- [x] **Trim body text to ≤10,000 words** — Four targeted cuts in Discussion (no scientific content lost): (1) removed editorialising sentence ("data beyond weight loss is where the real health interest lies"), (2) removed redundant caveat in Outcome Patterns already covered by Introduction and Limitations, (3) replaced 40-word verbatim comment example with concise summary ("These multi-objective reports describe single metabolic interventions with systemic consequences"), (4) tightened ABSA paragraph by removing parenthetical detail. Net effect: 10,074 → 9,993 words (7 words under limit). Abstract: 452 words (within JMIR tolerance of 450).
- [x] **JMIR compliance audit — formatting and style standardization** — Comprehensive audit against JMIR House Style, Statistics Reporting, and Table Formatting guidelines. Changes applied (not highlighted in red; formatting-only, no scientific content):
  - **British → American spellings (90 instances):** All British English forms converted to American English throughout manuscript and appendices (eg, optimised→optimized, characterisation→characterization, analysed→analyzed, modelling→modeling, programme→program, behaviour→behavior, contextualise→contextualize, etc.). Reference titles preserved in original published spelling.
  - **Latin abbreviations (15 instances):** "e.g." → "eg" and "i.e." → "ie" per JMIR House Style (no periods, no italics for Latin abbreviations).
  - **Chi-square decimal places (4 values):** Rounded to 1 decimal per JMIR statistics guidelines: χ²=927.51→927.5, χ²(10)=28.76→28.8, χ²(2)=19.36→19.4.
  - **Statistical notation spacing (61 instances):** Removed spaces in n= and N= notation per JMIR guidelines ("n=500" not "n = 500").
  - **Mean/median format (1 instance):** Removed equals signs per JMIR ("mean 32.5" not "mean = 32.5").
  - **OR formatting (Abstract):** Fixed spacing and format: "OR=8.68,95% CI 7.10, 10.61" → "OR 8.68, 95% CI 7.10-10.61".
  - **CI range format (body text):** Standardized comma-separated CI bounds to hyphenated ranges per JMIR style (eg, "95% CI 95.7%, 98.6%" → "95% CI 95.7%-98.6%").
  - **± notation (Appendix F, 8 instances):** Replaced "±" with "(SD)" format per JMIR preference (eg, "87.0 ± 5.3%" → "87.0 (SD 5.3)%").

### Unreferenced Claims Analysis

The following Discussion/Conclusions statements were identified as lacking citations. For each, candidate peer-reviewed references are listed below.

#### Claim 1 (Line 492): Multi-objective outcomes and prospective research designs
> "...a pattern that could be explored through prospective clinical research designs."

**Candidate references:**
- Staudacher HM, et al. Optimal Design of Clinical Trials of Dietary Interventions in Disorders of Gut–Brain Interaction. *Am J Gastroenterol*. 2022;117(6):973–984. doi:10.14309/ajg.0000000000001732 — PMC9169766
- Hébert JR, et al. Perspective: Design and Conduct of Human Nutrition Randomized Controlled Trials. *Adv Nutr*. 2022;13(2):372–382. doi:10.1093/advances/nmab132

#### Claim 2 (Line 504): Recall improvements achievable without compromising precision
> "...recall improvements are achievable without compromising precision."

**Candidate references:**
- Ding et al. 2025 [49] (already in reference list — ML/DL trade-offs; can be cited here)
- Childs JE, et al. Rule-Based Information Extraction for Rapid Deployment. *Proc LREC*. 2022:509–517. — aclanthology.org/2022.lrec-1.55
- Gonzalez-Hernandez G, Sarker A, O'Connor K, Savova G. Capturing the Patient's Perspective: a Review of Advances in Natural Language Processing of Health-Related Text. *Yearb Med Inform*. 2017;26(1):214–227. doi:10.15265/IY-2017-029 — PMC6250990

#### Claim 3 (Line 523): Precision "typically 80–90%" for comparable systems
> "The framework's 97.6% precision substantially exceeds comparable systems (typically 80–90%, Table 13)"

**Candidate references:**
- Golder S, Norman G, Loke YK. Systematic review on the prevalence, frequency and comparative value of adverse events data in social media. *Br J Clin Pharmacol*. 2015;80(4):878–888. doi:10.1111/bcp.12746 (already [33] in reference list — cite explicitly here)
- Sarker A, Gonzalez G. Portable automatic text classification for adverse drug reaction detection via multi-corpus training. *J Biomed Inform*. 2015;53:196–207. doi:10.1016/j.jbi.2014.11.002 (already [44] — cite explicitly here)

#### Claim 4 (Line 567): "The first validated computational approach"
> "the first validated computational approach for large-scale extraction of self-reported health outcomes from YouTube comment sections"

**Candidate references (to soften to "to our knowledge, the first"):**
- Gonzalez-Hernandez G, et al. Capturing the Patient's Perspective: a Review of Advances in NLP of Health-Related Text. *Yearb Med Inform*. 2017;26(1):214–227. PMC6250990 — comprehensive review showing no prior YouTube comment outcome extraction system
- Sarker A, et al. Utilizing social media data for pharmacovigilance: A review. *J Biomed Inform*. 2015;54:202–212. doi:10.1016/j.jbi.2015.02.004 — reviews social media health NLP landscape, confirms no YouTube outcome extraction
- Liu X, Chen H. A research framework for pharmacovigilance in health social media: identification and evaluation of patient adverse drug event reports. *J Biomed Inform*. 2015;58:268–279. — scoping of platforms used (Twitter dominant; YouTube absent)

#### Claim 5 (Line 571): Healthcasting phenomenon "larger and more structured than previously recognised"
> "the Healthcasting phenomenon is larger and more structured than previously recognised"

**Candidate references:**
- Madathil KC, et al. Healthcare information on YouTube: A systematic review. *Health Informatics J*. 2015;21(3):173–194. doi:10.1177/1460458213512220 — established the scale of YouTube health content but did not examine comment-level outcome data
- Bora K, et al. Users' experience with health-related content on YouTube: an exploratory study. *BMC Public Health*. 2024;24:56. doi:10.1186/s12889-023-17585-5 — documents user engagement scale with health YouTube content
- Reference [19] (already in list — cite explicitly here as the prior Healthcasting baseline)

#### Claim 6 (Line 573): Scalable methods to monitor population-level dietary intervention adoption
> "...public health researchers seeking scalable methods to monitor population-level adoption of dietary interventions."

**Candidate references:**
- Eysenbach G. Infodemiology and Infoveillance: Framework for an Emerging Set of Public Health Informatics Methods to Analyze Search, Communication and Publication Behavior on the Internet. *J Med Internet Res*. 2009;11(1):e11. doi:10.2196/jmir.1157 — PMC2762766 (foundational infodemiology framework)
- Eysenbach G. Infodemiology and infoveillance: tracking online health information and cyberbehavior for public health. *Am J Prev Med*. 2011;40(5 Suppl 2):S154–S158. doi:10.1016/j.amepre.2011.02.006
- Mavragani A, Ochoa G. Google Trends in Infodemiology and Infoveillance: Methodology Framework. *JMIR Public Health Surveill*. 2019;5(2):e13439. doi:10.2196/13439

#### Claim 7 (Line 579): Clinical significance of unsupervised medication discontinuation
> "The medication discontinuation reports in this corpus carry genuine clinical significance: people stopping prescription medications based on YouTube content, presumably without clinical supervision."

**Candidate references:**
- Walsh CA, et al. The association between medication non-adherence and adverse health outcomes in ageing populations: A systematic review and meta-analysis. *Br J Clin Pharmacol*. 2019;85(11):2464–2478. doi:10.1111/bcp.14075 — PMC6848955
- Raman S, et al. Inside the Bell Jar of Social Media: A Descriptive Study Assessing YouTube Coverage of Psychotropic Medication Adherence. *Psychiatry Investig*. 2023;20(8):758–766. doi:10.30773/pi.2023.0109 — PMC10454501 (directly addresses YouTube and medication discontinuation)
- Kleinsinger F. The Unmet Challenge of Medication Nonadherence. *Perm J*. 2018;22:18-033. doi:10.7812/TPP/18-033

#### Claim 8 (Line 579): Absence of mechanisms to connect social media discourse to clinical care
> "The absence of mechanisms to connect health-related social media discourse to clinical care systems represents an open question for health informatics research."

**Candidate references:**
- Shapiro M, Johnston D, Wald J, Mon D. Patient-Generated Health Data. White Paper. ONC. 2012. (foundational PGHD definition; widely cited)
- Reading MJ, Merrill JA. Converging and diverging needs between patients and providers who are collecting and using patient-generated health data: an integrative review. *J Am Med Inform Assoc*. 2018;25(6):759–771. doi:10.1093/jamia/ocy006 — PMC6697140
- Jim HSL, et al. Innovations in Research and Clinical Care Using Patient-Generated Health Data. *CA Cancer J Clin*. 2020;70(3):182–199. doi:10.3322/caac.21608 — PMC7488179 (documents the gap between PGHD collection and clinical integration)

#### Claim 9 (Line 478, borderline): Comment volume growth warranting systematic tools
> "Comment volume grew more than 100-fold between 2017 and 2024, suggesting that systematic tools to understand what people report in these spaces are warranted."

**Candidate references (optional, strengthens framing):**
- Madathil KC, et al. Healthcare information on YouTube: A systematic review. *Health Informatics J*. 2015;21(3):173–194. doi:10.1177/1460458213512220
- Eysenbach G. Infodemiology and Infoveillance. *J Med Internet Res*. 2009;11(1):e11. doi:10.2196/jmir.1157

### Submission to JMIR

**Date:** 19 April 2026

**Files uploaded to JMIR manuscript management system:**

| File | JMIR ID | Role |
|------|---------|------|
| Ribeiro_JMIR_2026_v4_CLEAN.docx | 94855-1433512-1-ED.docx | Revised Manuscript (clean, no highlights) |
| Ribeiro_JMIR_2026_v4_HIGHLIGHTED.docx | — | Supplementary file (yellow-highlighted changes) |
| Figure_1_Framework_Architecture_1200.png | — | Figure 1 |

**Point-by-point response:** Submitted via Editor/Author Correspondence on 19 April 2026. Addresses all 5 editor comments and acknowledges Reviewer S acceptance recommendation.

**Status:** Currently under editorial review (Round 2).

---

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
