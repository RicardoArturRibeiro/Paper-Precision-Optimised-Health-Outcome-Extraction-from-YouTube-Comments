# ==============================================================================
# PhD Thesis RQ1 Phase 3: Script 9 - Validation Sample Extraction
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script extracts a stratified random sample of 500 positive outcome
# comments for manual validation. It creates a coding sheet for the researcher
# to verify classification accuracy and calculate precision metrics.
#
# Validation Approach:
# - 500 random sample (provides ±4.4% margin at 95% CI)
# - Stratified by Research Objective to ensure coverage
# - Manual coding by researcher to assess precision
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 3, Script 9 of 11
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup
# ==============================================================================

!pip install pandas numpy matplotlib seaborn -q

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from collections import Counter
import warnings

from google.colab import drive

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)

print("=" * 70)
print("PhD RQ1 Phase 3: Aspect Attribution")
print("Script 9 - Validation Sample Extraction")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Configuration
# ==============================================================================

drive.mount('/content/drive')

INPUT_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase3_Outputs/Phase3_Script8_positive_outcomes.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase3_Outputs/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Validation parameters
SAMPLE_SIZE = 500  # Total sample size
RANDOM_SEED = 42   # For reproducibility

print(f"\n📂 Input Path: {INPUT_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print(f"📊 Sample Size: {SAMPLE_SIZE}")


# ==============================================================================
# CELL 3: Load Positive Outcomes Data
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING POSITIVE OUTCOMES DATA")
print("=" * 70)

positive_df = pd.read_csv(INPUT_PATH)
print(f"\n✅ Loaded {len(positive_df):,} positive outcome comments")

# Display columns
print(f"\n📋 Columns: {list(positive_df.columns)}")

# Show distribution by RO
print("\n--- Distribution by Primary RO ---")
ro_counts = Counter()
for ros in positive_df['ro_ids']:
    if pd.notna(ros):
        for ro in ros.split('; '):
            ro_counts[ro] += 1

for ro, count in sorted(ro_counts.items()):
    print(f"  {ro}: {count:,} ({count/len(positive_df)*100:.1f}%)")


# ==============================================================================
# CELL 4: Create Stratified Sample
# ==============================================================================

print("\n" + "=" * 70)
print("2. CREATING STRATIFIED RANDOM SAMPLE")
print("=" * 70)

# Strategy: Stratify by primary RO to ensure coverage of all Research Objectives
# Allocate proportionally but ensure minimum representation

def get_primary_ro(ro_ids):
    """Get the primary (first) RO from a comment."""
    if pd.isna(ro_ids) or ro_ids == '':
        return 'Unknown'
    return ro_ids.split('; ')[0]

positive_df['primary_ro'] = positive_df['ro_ids'].apply(get_primary_ro)

# Calculate proportional allocation
ro_distribution = positive_df['primary_ro'].value_counts()
print("\n--- Primary RO Distribution ---")
for ro, count in ro_distribution.items():
    print(f"  {ro}: {count:,} ({count/len(positive_df)*100:.1f}%)")

# Calculate sample allocation (proportional with minimum of 50 per RO)
total_positive = len(positive_df)
sample_allocation = {}

for ro in ['RO1', 'RO2', 'RO3']:
    ro_count = ro_distribution.get(ro, 0)
    # Proportional allocation
    proportional = int((ro_count / total_positive) * SAMPLE_SIZE)
    # Ensure minimum of 50 for meaningful analysis
    sample_allocation[ro] = max(50, proportional)

# Adjust to hit exactly SAMPLE_SIZE
total_allocated = sum(sample_allocation.values())
if total_allocated != SAMPLE_SIZE:
    # Adjust RO2 (largest group) to balance
    sample_allocation['RO2'] += (SAMPLE_SIZE - total_allocated)

print(f"\n--- Sample Allocation ---")
for ro, count in sample_allocation.items():
    print(f"  {ro}: {count} samples")
print(f"  Total: {sum(sample_allocation.values())}")

# Draw stratified sample
np.random.seed(RANDOM_SEED)
sample_dfs = []

for ro, n_samples in sample_allocation.items():
    ro_df = positive_df[positive_df['primary_ro'] == ro]
    if len(ro_df) >= n_samples:
        sampled = ro_df.sample(n=n_samples, random_state=RANDOM_SEED)
    else:
        sampled = ro_df  # Take all if not enough
    sample_dfs.append(sampled)

validation_sample = pd.concat(sample_dfs, ignore_index=True)

# Shuffle the sample
validation_sample = validation_sample.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

print(f"\n✅ Created validation sample: {len(validation_sample)} comments")


# ==============================================================================
# CELL 5: Create Coding Sheet
# ==============================================================================

print("\n" + "=" * 70)
print("3. CREATING VALIDATION CODING SHEET")
print("=" * 70)

# Prepare coding sheet with all necessary information
coding_sheet = pd.DataFrame({
    'sample_id': range(1, len(validation_sample) + 1),
    'comment_text': validation_sample['comment_text'].values,
    'channel': validation_sample['channel_name'].values if 'channel_name' in validation_sample.columns else 'Unknown',
    'auto_classification': validation_sample['classification'].values,
    'auto_aspect_ids': validation_sample['aspect_ids'].values,
    'auto_ro_ids': validation_sample['ro_ids'].values,
    'auto_outcome_categories': validation_sample['outcome_categories'].values,

    # Manual coding columns (to be filled by researcher)
    'manual_is_positive_outcome': '',  # Yes / No / Unclear
    'manual_is_personal': '',          # Yes / No (is it personal testimony?)
    'manual_is_definite': '',          # Yes / No (is outcome definite, not intent?)
    'manual_aspect_correct': '',       # Yes / No / Partial
    'manual_notes': ''                 # Any notes
})

print(f"✅ Coding sheet created with {len(coding_sheet)} rows")
print(f"\n📋 Coding columns:")
print("  • sample_id: Unique identifier for each sample")
print("  • comment_text: The full comment text")
print("  • channel: Source channel")
print("  • auto_*: Automated classification results")
print("  • manual_is_positive_outcome: [YOUR INPUT] Yes/No/Unclear")
print("  • manual_is_personal: [YOUR INPUT] Yes/No")
print("  • manual_is_definite: [YOUR INPUT] Yes/No")
print("  • manual_aspect_correct: [YOUR INPUT] Yes/No/Partial")
print("  • manual_notes: [YOUR INPUT] Any observations")


# ==============================================================================
# CELL 6: Create Quick Validation Subset (50 samples)
# ==============================================================================

print("\n" + "=" * 70)
print("4. CREATING QUICK VALIDATION SUBSET")
print("=" * 70)

# For initial quick validation, create a smaller 50-sample subset
quick_sample = validation_sample.head(50).copy()

quick_coding = pd.DataFrame({
    'sample_id': range(1, 51),
    'comment_text': quick_sample['comment_text'].values,
    'channel': quick_sample['channel_name'].values if 'channel_name' in quick_sample.columns else 'Unknown',
    'auto_aspect_ids': quick_sample['aspect_ids'].values,
    'auto_outcome_categories': quick_sample['outcome_categories'].values,
    'manual_is_positive_outcome': '',
    'manual_notes': ''
})

print(f"✅ Quick validation subset: 50 samples")
print("   Use this for initial precision estimate before full coding")


# ==============================================================================
# CELL 7: Sample Statistics
# ==============================================================================

print("\n" + "=" * 70)
print("5. VALIDATION SAMPLE STATISTICS")
print("=" * 70)

print("\n--- Sample by Primary RO ---")
sample_ro_dist = validation_sample['primary_ro'].value_counts()
for ro, count in sample_ro_dist.items():
    print(f"  {ro}: {count} ({count/len(validation_sample)*100:.1f}%)")

print("\n--- Sample by Channel ---")
if 'channel_name' in validation_sample.columns:
    sample_channel_dist = validation_sample['channel_name'].value_counts()
    for channel, count in sample_channel_dist.items():
        print(f"  {channel}: {count} ({count/len(validation_sample)*100:.1f}%)")

print("\n--- Sample by Outcome Category ---")
outcome_cats = Counter()
for cats in validation_sample['outcome_categories']:
    if pd.notna(cats) and cats:
        for cat in cats.split('; '):
            outcome_cats[cat] += 1

for cat, count in outcome_cats.most_common():
    print(f"  {cat}: {count} ({count/len(validation_sample)*100:.1f}%)")


# ==============================================================================
# CELL 8: Display Sample Examples
# ==============================================================================

print("\n" + "=" * 70)
print("6. SAMPLE EXAMPLES FOR PREVIEW")
print("=" * 70)

print("\n--- 10 Random Examples from Validation Sample ---\n")

preview_samples = validation_sample.sample(n=10, random_state=123)

for idx, (_, row) in enumerate(preview_samples.iterrows(), 1):
    print(f"[{idx}] Channel: {row.get('channel_name', 'Unknown')}")
    print(f"    Aspects: {row['aspect_ids']}")
    print(f"    Outcome: {row['outcome_categories']}")
    text = str(row['comment_text'])[:300]
    print(f"    Text: {text}...")
    print()


# ==============================================================================
# CELL 9: Export Validation Files
# ==============================================================================

print("\n" + "=" * 70)
print("7. EXPORTING VALIDATION FILES")
print("=" * 70)

# Export 1: Full coding sheet (500 samples)
coding_sheet.to_csv(f'{OUTPUT_DIR}Phase3_Script9_validation_coding_sheet.csv', index=False)
print(f"✅ Exported: Phase3_Script9_validation_coding_sheet.csv ({len(coding_sheet)} rows)")

# Export 2: Quick validation subset (50 samples)
quick_coding.to_csv(f'{OUTPUT_DIR}Phase3_Script9_quick_validation_50.csv', index=False)
print(f"✅ Exported: Phase3_Script9_quick_validation_50.csv (50 rows)")

# Export 3: Excel version for easier manual coding
try:
    coding_sheet.to_excel(f'{OUTPUT_DIR}Phase3_Script9_validation_coding_sheet.xlsx', index=False)
    print(f"✅ Exported: Phase3_Script9_validation_coding_sheet.xlsx")
except:
    print("⚠️ Excel export failed - use CSV version")


# ==============================================================================
# CELL 10: Validation Instructions
# ==============================================================================

print("\n" + "=" * 70)
print("8. VALIDATION INSTRUCTIONS")
print("=" * 70)

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    MANUAL VALIDATION INSTRUCTIONS                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  STEP 1: Open Phase3_Script9_validation_coding_sheet.xlsx            ║
║                                                                      ║
║  STEP 2: For each row, evaluate and fill in:                         ║
║                                                                      ║
║    manual_is_positive_outcome:                                       ║
║      • "Yes" = Comment reports a definite positive health outcome    ║
║      • "No" = Not a positive outcome (negative, question, general)   ║
║      • "Unclear" = Cannot determine                                  ║
║                                                                      ║
║    manual_is_personal:                                               ║
║      • "Yes" = First-person testimony ("I lost...", "My A1C...")     ║
║      • "No" = Third-party or general statement                       ║
║                                                                      ║
║    manual_is_definite:                                               ║
║      • "Yes" = Achieved outcome ("lost 30 lbs", "reversed")          ║
║      • "No" = Intent/hope ("trying to lose", "hope to reverse")      ║
║                                                                      ║
║    manual_aspect_correct:                                            ║
║      • "Yes" = Automated aspect assignment is correct                ║
║      • "No" = Automated aspect assignment is wrong                   ║
║      • "Partial" = Some aspects correct, some missing/wrong          ║
║                                                                      ║
║  STEP 3: Save the file and upload to Claude for precision analysis   ║
║                                                                      ║
║  TIP: Start with the 50-sample quick validation file first!          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

CODING DECISION GUIDE:
----------------------

✅ CODE AS "Yes" (True Positive):
  • "I lost 30 pounds on keto" → Personal, definite, quantified
  • "My A1C dropped from 10 to 5.5" → Personal, definite, quantified
  • "Reversed my type 2 diabetes" → Personal, definite, reversal
  • "Pain is completely gone" → Personal, definite, symptom cessation
  • "Off metformin for 6 months now" → Personal, definite, medication stop

❌ CODE AS "No" (False Positive):
  • "I want to lose weight" → Intent, not achieved
  • "Can keto reverse diabetes?" → Question, not report
  • "My husband lost 50 pounds" → Third-party, not personal
  • "Keto helps with weight loss" → General statement
  • "Still trying to lose weight" → Ongoing, not achieved

⚠️ CODE AS "Unclear":
  • "Feeling better on this diet" → Vague, no specific outcome
  • "Things are improving" → Non-specific
  • Truncated comments where outcome unclear
""")


# ==============================================================================
# CELL 11: Precision Calculator (for after manual coding)
# ==============================================================================

print("\n" + "=" * 70)
print("9. PRECISION CALCULATOR CODE")
print("=" * 70)

print("""
After completing manual validation, run this code to calculate precision:

```python
# Load your completed coding sheet
coded_df = pd.read_csv('Phase3_Script9_validation_coding_sheet.csv')
# Or: coded_df = pd.read_excel('Phase3_Script9_validation_coding_sheet.xlsx')

# Calculate precision metrics
total_coded = len(coded_df[coded_df['manual_is_positive_outcome'] != ''])

true_positives = len(coded_df[coded_df['manual_is_positive_outcome'] == 'Yes'])
false_positives = len(coded_df[coded_df['manual_is_positive_outcome'] == 'No'])
unclear = len(coded_df[coded_df['manual_is_positive_outcome'] == 'Unclear'])

# Precision (excluding unclear)
precision = true_positives / (true_positives + false_positives) * 100

print(f"Validation Results (n={total_coded})")
print(f"  True Positives: {true_positives}")
print(f"  False Positives: {false_positives}")
print(f"  Unclear: {unclear}")
print(f"  Precision: {precision:.1f}%")

# 95% Confidence Interval for precision
import scipy.stats as stats
p = true_positives / (true_positives + false_positives)
n = true_positives + false_positives
se = np.sqrt(p * (1-p) / n)
ci_lower = (p - 1.96 * se) * 100
ci_upper = (p + 1.96 * se) * 100
print(f"  95% CI: [{ci_lower:.1f}%, {ci_upper:.1f}%]")
```
""")


# ==============================================================================
# CELL 12: Summary Report
# ==============================================================================

print("\n" + "=" * 70)
print("10. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 3 SCRIPT 9 - VALIDATION SAMPLE EXTRACTION RESULTS
========================================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. SAMPLE OVERVIEW
------------------
Total Positive Outcomes in Corpus: {len(positive_df):,}
Validation Sample Size: {len(validation_sample)}
Sampling Method: Stratified random by Research Objective

2. SAMPLE ALLOCATION
--------------------""")

for ro, count in sample_allocation.items():
    print(f"  {ro}: {count} samples")

print(f"""

3. SAMPLE DISTRIBUTION BY RO
----------------------------""")
for ro, count in sample_ro_dist.items():
    print(f"  {ro}: {count} ({count/len(validation_sample)*100:.1f}%)")

print(f"""

4. SAMPLE DISTRIBUTION BY OUTCOME CATEGORY
------------------------------------------""")
for cat, count in outcome_cats.most_common():
    print(f"  {cat}: {count}")

print(f"""

5. FILES EXPORTED
-----------------
- Phase3_Script9_validation_coding_sheet.csv (500 samples)
- Phase3_Script9_validation_coding_sheet.xlsx (500 samples)
- Phase3_Script9_quick_validation_50.csv (50 samples for quick check)

6. NEXT STEPS
-------------
1. Open the Excel/CSV coding sheet
2. Code each sample manually using the decision guide
3. Upload completed sheet to Claude for precision analysis
4. Proceed to Script 10 for final statistical analysis

7. EXPECTED PRECISION
---------------------
Based on Script 7 sample review: ~90-95% precision expected
(Your manual coding will confirm this)

8. STATISTICAL POWER
--------------------
Sample size: 500
Margin of error: ±4.4% at 95% confidence
Sufficient for: Publication-quality precision estimate

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 9 Complete - Validation Sample Ready for Manual Coding")
print("=" * 70)
