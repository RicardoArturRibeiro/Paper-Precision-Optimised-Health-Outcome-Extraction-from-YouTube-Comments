# Revision Changelog — JMIR ms#94855

**Document:** Ribeiro_JMIR_2026_REVISED.docx
**Date:** 13 March 2026
**Author:** Ricardo Ribeiro (with AI-assisted analysis)
**Reason:** Corpus deduplication following discovery of YouTube Data API v3 pagination duplicates

---

## Summary of Change

The YouTube Data API v3 returned duplicate comment records during paginated retrieval with `order='relevance'`. After deduplication by comment text, the corpus was corrected from 209,661 records to **43,111 unique comments** (inflation factor: 4.86×).

---

## Corrected Metrics Overview

| Metric | Original | Corrected | Change |
|--------|----------|-----------|--------|
| Corpus size | 209,661 | 43,111 | −166,550 |
| Positive outcomes | 6,671 | 1,790 | −4,881 |
| Prevalence | 3.18% | 4.15% | +0.97pp |
| Unique authors | 37,742 | 37,458 | −284 |
| Est. true positives | 6,510 | 1,747 | −4,763 |
| Est. false negatives | 32,865 | 6,690 | −26,175 |
| Recall | 16.5% | 20.7% | +4.2pp |
| Recall 95% CI | 11.6%–23.6% | 14.8%–29.0% | improved |
| Chi-square | 3,509 | 927.51 | recalculated |
| Cramér's V | 0.129 | 0.147 | recalculated |
| Highest rate | 8.06% (KenDBerryMD) | 10.40% (KenDBerryMD) | +2.34pp |
| Lowest rate | 1.14% (Mark Hyman) | 1.32% (Shawn Baker MD) | channel changed |
| Odds ratio (max/min) | 7.61 | 8.68 | +1.07 |
| Adjusted prevalence | 3.11% | 4.05% | +0.94pp |
| Precision | 97.6% | 97.6% | **UNCHANGED** |
| Ontology (35 aspects) | — | — | **UNCHANGED** |
| Framework methodology | — | — | **UNCHANGED** |

---

## Section-by-Section Changes

### Abstract

1. **Methods:** "209,661 comments" → "43,111 unique comments"; "37,742 unique authors" → "37,458 unique authors"
2. **Results:** "6,671 positive health outcome reports (3.18% prevalence)" → "1,790 positive health outcome reports (4.15% prevalence)"; recall "16.5% (95% CI: 11.6%–23.6%)" → "20.7% (95% CI: 14.8%–29.0%)"; "χ²=3,509" → "χ²=927.51"; rates "1.14% to 8.06% (OR=7.61)" → "1.32% to 10.40% (OR=8.68)"
3. **Conclusions:** "6,510 estimated true positives" → "1,747 estimated true positives"

### Introduction — Contributions

4. "6,510 estimated true positive health outcome reports extracted from 209,661 comments across 37,742 unique commenters" → "1,747 ... from 43,111 unique comments across 37,458 unique commenters"

### Background — Table 1 Footnote

5. "comparable to this study's 3.18%" → "comparable to this study's 4.15%"

### Methods — Data Collection

6. **NEW TEXT ADDED:** "yielding a raw corpus of 209,661 records from 110 videos. After removing duplicate records caused by API pagination (the YouTube Data API v3 returns non-unique results when paginating beyond available comments with relevance-based ordering), 43,111 unique comments were retained"

### Methods — Table 2

7. **All 11 channel rows updated:** comment counts, positive outcome counts, and rates corrected to deduplicated values
8. **Channel ranking changes:** Jason Fung moves from #4 to #2; Shawn Baker MD becomes lowest rate (was Mark Hyman)

### Methods — Phase 2 Ontology

9. "N = 209,661" → "N = 43,111"; "3.18% of the full corpus (n = 6,671)" → "4.15% of the full corpus (n = 1,790)"

### Results — Classification

10. "6,671 comments (3.18% of the corpus)" → "1,790 comments (4.15% of the corpus)"

### Results — Recall Estimation

11. "non-positive pool of 202,990 comments" → "41,321 unique comments"
12. "32,865 false negatives (95% CI: 21,032–49,542)" → "6,690 false negatives (95% CI: 4,281–10,084)"
13. "6,510 estimated true positives, this yields an estimated recall of 16.5%" → "1,747 estimated true positives, this yields an estimated recall of 20.7%"
14. "6,510 estimated true positive health outcome reports (95% CI: 6,384–6,577)" → "1,747 (95% CI: 1,713–1,764)"
15. **Table 4:** Recall CI "11.6% – 23.6%" → "14.8% – 29.0%"

### Results — Prevalence

16. "3.18% (6,671 / 209,661)" → "4.15% (1,790 / 43,111)"; adjusted prevalence "3.11%" → "4.05%"

### Results — Channel Variation

17. "χ² = 3,509" → "χ² = 927.51"
18. "1.14% (Mark Hyman) to 8.06% (KenDBerryMD), yielding an odds ratio of 7.61" → "1.32% (Shawn Baker MD) to 10.40% (KenDBerryMD), yielding an odds ratio of 8.68"
19. "Cramér's V = 0.129" → "Cramér's V = 0.147"

### Figures

20. **Figure 1:** Image regenerated — "Corpus (N=209,661)" → "(N=43,111)"; "Validated Corpus (n=6,671)" → "(n=1,790)"
21. **Figure 2:** Caption "(n = 6,671)" → "(n = 1,790)"; image regenerated with corrected data
21. **Figure 3:** Caption and image regenerated with corrected data
22. **Figure 4:** Caption updated (rate 3.18%→4.15%, χ²=927.51, V=0.147); image regenerated
23. **Figure 5:** Image regenerated with corrected data

### Discussion

24. "209,661 comments from 37,742 unique individuals ... 6,671" → "43,111 unique comments from 37,458 unique individuals ... 1,790"
25. "3.18% positive outcome rate" → "4.15%"
26. "7.61-fold difference ... KenDBerryMD, 8.06% ... Mark Hyman, 1.14%" → "8.68-fold ... 10.40% ... Shawn Baker MD, 1.32%"
27. "χ² = 3,508.86" → "χ² = 927.51"
28. "Mark Hyman (1.14%)" → "Mark Hyman (1.71%)" in channel discussion paragraph
29. "6,510 estimated true positives" → "1,747"
30. "16.5% recall (95% CI: 11.6%–23.6%) ... 83.5% of actual positive outcome reports" → "20.7% recall (95% CI: 14.8%–29.0%) ... 79.3%"
31. Recall limitation paragraph: "16.5% ... 11.6%–23.6%" → "20.7% ... 14.8%–29.0%"
32. "6,671 verifiable positive health outcome reports ... 37,742 unique individuals" → "1,790 ... 37,458"
33. "3.18% prevalence" → "4.15% prevalence" in limitation section

### Conclusions

34. "209,661 comments" → "43,111 unique comments"
35. "6,671 classified positive outcomes (6,510 estimated true positives) ... 37,742 unique commenters" → "1,790 ... (1,747) ... 37,458"
36. "7.61-fold variation ... KenDBerryMD at 8.06% to Mark Hyman at 1.14%" → "8.68-fold ... 10.40% to Shawn Baker MD at 1.32%"
37. "6,671 outcomes" → "1,790 outcomes"

### ABSA Section

38. "full corpus of 209,661" → "full corpus of 43,111 unique comments"
39. **Table 9 — "Est. Full Corpus" column:** Corpus-level sentiment extrapolations rescaled from old N=209,661 to N=43,111 (×0.2056). Positive ~63,800→~13,100; Negative ~13,900→~2,900; Neutral ~18,200→~3,700; Mixed ~20,800→~4,300. Sample counts (n), percentages, and table note unchanged.

---

## What Remains UNCHANGED

- **Precision:** 97.6% (95% CI: 95.7%–98.6%) — validated on unique manually coded comments
- **Ontology:** All 35 aspects across 3 Research Objectives
- **Framework methodology:** Four-phase pipeline design
- **Classification logic:** Rule-based classifier unchanged
- **Table 1:** Comparative literature review (unchanged)
- **Table 3:** Complete ontology (unchanged)
- **Figure 1:** Framework architecture — image regenerated with corrected N=43,111 and n=1,790
- **All qualitative findings** and interpretive analysis
- **Ethical considerations** section
- **References** section

## Notable Correction: Recall Improvement

The recall estimate improved from 16.5% to 20.7% after correction. This is because the original paper extrapolated the false negative rate (16.2%) to the inflated non-positive pool of 202,990 records, overestimating false negatives. With the corrected pool of 41,321 unique comments, the extrapolated false negatives decrease proportionally more than the true positives, yielding a higher (and more accurate) recall estimate.

---

*This changelog was prepared as part of the Author Correction Request for JMIR ms#94855.*
