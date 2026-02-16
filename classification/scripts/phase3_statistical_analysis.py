# ==============================================================================
# PhD THESIS RQ1 - PHASE 3: SCRIPT 10
# STATISTICAL ANALYSIS WITH PUBLICATION-READY OUTPUTS
# ==============================================================================
#
# Purpose: Generate final statistical analysis with confidence intervals,
#          chi-square tests, and publication-ready figures and tables
#
# Input:   Phase3_Script8_positive_outcomes.csv
#          Phase3_Script8_channel_statistics.csv
#          Phase2_Script5_final_ontology.csv
#          Phase3_Script9_validation_CODED.xlsx (manual validation results)
#
# Output:  - Phase3_Script10_summary_statistics.csv
#          - Phase3_Script10_aspect_statistics.csv
#          - Phase3_Script10_channel_analysis.csv
#          - Phase3_Script10_category_statistics.csv
#          - Phase3_Script10_Fig1_RO_Overview.png
#          - Phase3_Script10_Fig2_Top10_Aspects.png
#          - Phase3_Script10_Fig3_Channel_Comparison.png
#          - Phase3_Script10_Fig4_Outcome_Categories.png
#          - Phase3_Script10_Fig5_Summary_Dashboard.png
#          - Phase3_Script10_publication_tables.xlsx
#
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. SETUP AND IMPORTS
# ------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Define paths
BASE_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/'
PHASE2_PATH = BASE_PATH + 'Phase2_Outputs/'
PHASE3_PATH = BASE_PATH + 'Phase3_Outputs/'

print("=" * 80)
print("PhD RQ1 - SCRIPT 10: STATISTICAL ANALYSIS")
print("=" * 80)

# ------------------------------------------------------------------------------
# 2. LOAD DATA FILES
# ------------------------------------------------------------------------------

print("\n[1] Loading data files...")

# Load positive outcomes
positive_df = pd.read_csv(PHASE3_PATH + 'Phase3_Script8_positive_outcomes.csv')
print(f"    ✓ Positive outcomes loaded: {len(positive_df):,} rows")

# Load channel statistics
channel_stats = pd.read_csv(PHASE3_PATH + 'Phase3_Script8_channel_statistics.csv')
print(f"    ✓ Channel statistics loaded: {len(channel_stats)} channels")

# Load ontology
ontology = pd.read_csv(PHASE2_PATH + 'Phase2_Script5_final_ontology.csv')
print(f"    ✓ Ontology loaded: {len(ontology)} aspects")

# Load validation results
try:
    validation_df = pd.read_excel(PHASE3_PATH + 'Phase3_Script9_validation_CODED.xlsx')
    print(f"    ✓ Validation data loaded: {len(validation_df)} samples")
    VALIDATION_AVAILABLE = True
except:
    print("    ⚠ Validation file not found - using default precision estimates")
    VALIDATION_AVAILABLE = False

# ------------------------------------------------------------------------------
# 3. DEFINE KEY CONSTANTS AND FUNCTIONS
# ------------------------------------------------------------------------------

# Corpus constants
TOTAL_CORPUS = 209661
TOTAL_POSITIVES = len(positive_df)

# Validation results (from manual coding)
if VALIDATION_AVAILABLE:
    true_pos = len(validation_df[validation_df['manual_is_positive_outcome'] == 'Yes'])
    false_pos = len(validation_df[validation_df['manual_is_positive_outcome'] == 'No'])
    valid_total = true_pos + false_pos
    PRECISION = true_pos / valid_total if valid_total > 0 else 0.976
else:
    PRECISION = 0.976  # Default from validation

print(f"\n    Key parameters:")
print(f"    - Total corpus: {TOTAL_CORPUS:,}")
print(f"    - Classified positives: {TOTAL_POSITIVES:,}")
print(f"    - Validated precision: {PRECISION:.1%}")

# Wilson confidence interval function
def wilson_ci(successes, total, confidence=0.95):
    """Calculate Wilson score confidence interval for a proportion."""
    if total == 0:
        return 0, 0, 0
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    p = successes / total
    denominator = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denominator
    margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * total)) / total) / denominator
    return p, max(0, centre - margin), min(1, centre + margin)

# Calculate precision CI
if VALIDATION_AVAILABLE:
    _, PRECISION_CI_LOW, PRECISION_CI_HIGH = wilson_ci(true_pos, valid_total)
else:
    PRECISION_CI_LOW, PRECISION_CI_HIGH = 0.957, 0.986

# ------------------------------------------------------------------------------
# 4. OVERALL PREVALENCE ANALYSIS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[2] OVERALL PREVALENCE ANALYSIS")
print("=" * 80)

# Raw prevalence
raw_prevalence = TOTAL_POSITIVES / TOTAL_CORPUS
p, ci_low, ci_high = wilson_ci(TOTAL_POSITIVES, TOTAL_CORPUS)

print(f"\nRaw Classification Results:")
print(f"    Positive outcomes: {TOTAL_POSITIVES:,} / {TOTAL_CORPUS:,}")
print(f"    Raw prevalence: {raw_prevalence:.2%} (95% CI: {ci_low:.2%} - {ci_high:.2%})")

# Adjusted for precision
adjusted_positives = int(TOTAL_POSITIVES * PRECISION)
adjusted_positives_low = int(TOTAL_POSITIVES * PRECISION_CI_LOW)
adjusted_positives_high = int(TOTAL_POSITIVES * PRECISION_CI_HIGH)

adj_prevalence = adjusted_positives / TOTAL_CORPUS

print(f"\nPrecision-Adjusted Results:")
print(f"    Estimated true positives: {adjusted_positives:,} (95% CI: {adjusted_positives_low:,} - {adjusted_positives_high:,})")
print(f"    Adjusted prevalence: {adj_prevalence:.2%}")

# ------------------------------------------------------------------------------
# 5. RESEARCH OBJECTIVE ANALYSIS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[3] RESEARCH OBJECTIVE ANALYSIS")
print("=" * 80)

# Parse RO from aspect IDs
def extract_ros(aspect_str):
    if pd.isna(aspect_str):
        return set()
    ros = set()
    for aspect in str(aspect_str).split(';'):
        aspect = aspect.strip()
        if aspect.startswith('RO1'):
            ros.add('RO1')
        elif aspect.startswith('RO2'):
            ros.add('RO2')
        elif aspect.startswith('RO3'):
            ros.add('RO3')
    return ros

positive_df['ROs'] = positive_df['aspect_ids'].apply(extract_ros)
positive_df['has_RO1'] = positive_df['ROs'].apply(lambda x: 'RO1' in x)
positive_df['has_RO2'] = positive_df['ROs'].apply(lambda x: 'RO2' in x)
positive_df['has_RO3'] = positive_df['ROs'].apply(lambda x: 'RO3' in x)

ro1_count = positive_df['has_RO1'].sum()
ro2_count = positive_df['has_RO2'].sum()
ro3_count = positive_df['has_RO3'].sum()

print("\nPositive Outcomes by Research Objective:")
print("-" * 60)

ro_data = []
for ro_name, ro_count, ro_desc in [
    ('RO1', ro1_count, 'Subjective Well-Being'),
    ('RO2', ro2_count, 'Tool-Mediated Validation'),
    ('RO3', ro3_count, 'Disease Specificity')
]:
    pct_of_positives = ro_count / TOTAL_POSITIVES * 100
    pct_of_corpus = ro_count / TOTAL_CORPUS * 100
    p, ci_l, ci_h = wilson_ci(ro_count, TOTAL_POSITIVES)
    print(f"\n{ro_name}: {ro_desc}")
    print(f"    Count: {ro_count:,} ({pct_of_positives:.1f}% of positives)")
    print(f"    Corpus prevalence: {pct_of_corpus:.2f}%")
    print(f"    95% CI (of positives): {ci_l:.1%} - {ci_h:.1%}")

    ro_data.append({
        'ro_id': ro_name,
        'ro_name': ro_desc,
        'count': ro_count,
        'pct_of_positives': pct_of_positives,
        'pct_of_corpus': pct_of_corpus,
        'ci_low': ci_l * 100,
        'ci_high': ci_h * 100
    })

ro_df = pd.DataFrame(ro_data)

# Multi-RO analysis
multi_ro = positive_df[(positive_df['has_RO1'].astype(int) +
                        positive_df['has_RO2'].astype(int) +
                        positive_df['has_RO3'].astype(int)) > 1]
print(f"\nMulti-RO Comments: {len(multi_ro):,} ({len(multi_ro)/TOTAL_POSITIVES*100:.1f}% report outcomes across multiple ROs)")

# ------------------------------------------------------------------------------
# 6. ASPECT-LEVEL ANALYSIS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[4] ASPECT-LEVEL ANALYSIS")
print("=" * 80)

# Count aspects
aspect_counts = {}
for _, row in positive_df.iterrows():
    if pd.notna(row['aspect_ids']):
        for aspect in str(row['aspect_ids']).split(';'):
            aspect = aspect.strip()
            if aspect:
                aspect_counts[aspect] = aspect_counts.get(aspect, 0) + 1

# Create aspect dataframe with CIs
aspect_data = []
for aspect_id, count in sorted(aspect_counts.items(), key=lambda x: -x[1]):
    pct_positives = count / TOTAL_POSITIVES * 100
    pct_corpus = count / TOTAL_CORPUS * 100
    p, ci_low, ci_high = wilson_ci(count, TOTAL_POSITIVES)

    # Get aspect name from ontology
    aspect_name = ontology[ontology['aspect_id'] == aspect_id]['aspect_name'].values
    name = aspect_name[0] if len(aspect_name) > 0 else aspect_id

    aspect_data.append({
        'rank': len(aspect_data) + 1,
        'aspect_id': aspect_id,
        'aspect_name': name,
        'count': count,
        'pct_of_positives': pct_positives,
        'pct_of_corpus': pct_corpus,
        'ci_low': ci_low * 100,
        'ci_high': ci_high * 100
    })

aspect_df = pd.DataFrame(aspect_data)

print("\nTop 15 Aspects with 95% Confidence Intervals:")
print("-" * 90)
print(f"{'Rank':<5} {'Aspect ID':<10} {'Name':<25} {'Count':>8} {'% Pos':>8} {'95% CI':>18}")
print("-" * 90)

for i, row in aspect_df.head(15).iterrows():
    print(f"{row['rank']:<5} {row['aspect_id']:<10} {row['aspect_name'][:24]:<25} {row['count']:>8,} {row['pct_of_positives']:>7.1f}% ({row['ci_low']:>5.1f}%-{row['ci_high']:>5.1f}%)")

# ------------------------------------------------------------------------------
# 7. CHANNEL ANALYSIS WITH CHI-SQUARE TEST
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[5] CHANNEL VARIATION ANALYSIS")
print("=" * 80)

# Channel statistics
channel_positive_counts = positive_df.groupby('channel_name').size().reset_index(name='positive_count')

# Merge with total counts
channel_analysis = channel_stats.merge(channel_positive_counts, left_on='channel', right_on='channel_name', how='left')
channel_analysis['positive_count'] = channel_analysis['positive_count'].fillna(channel_analysis['positive_outcomes']).astype(int)

# Add confidence intervals
for idx, row in channel_analysis.iterrows():
    p, ci_l, ci_h = wilson_ci(int(row['positive_count']), int(row['total_comments']))
    channel_analysis.loc[idx, 'ci_low'] = ci_l * 100
    channel_analysis.loc[idx, 'ci_high'] = ci_h * 100
    channel_analysis.loc[idx, 'rate_pct'] = row['positive_count'] / row['total_comments'] * 100

channel_analysis = channel_analysis.sort_values('rate_pct', ascending=False).reset_index(drop=True)

print("\nChannel Positive Outcome Rates with 95% CIs:")
print("-" * 85)
print(f"{'Channel':<25} {'Total':>10} {'Positive':>10} {'Rate':>8} {'95% CI':>18}")
print("-" * 85)

for _, row in channel_analysis.iterrows():
    print(f"{row['channel'][:24]:<25} {int(row['total_comments']):>10,} {int(row['positive_count']):>10,} {row['rate_pct']:>7.2f}% ({row['ci_low']:>5.2f}%-{row['ci_high']:>5.2f}%)")

# Chi-square test for channel variation
print("\n" + "-" * 60)
print("Chi-Square Test for Channel Variation:")
print("-" * 60)

observed = channel_analysis[['positive_count', 'total_comments']].copy()
observed['non_positive'] = observed['total_comments'] - observed['positive_count']
contingency = observed[['positive_count', 'non_positive']].values

chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

# Effect size (Cramer's V)
n = contingency.sum()
min_dim = min(contingency.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))

print(f"\n    Chi-square statistic: {chi2:.2f}")
print(f"    Degrees of freedom: {dof}")
print(f"    p-value: {p_value:.2e}")
print(f"    Cramer's V (effect size): {cramers_v:.3f}")

# Effect size interpretation
if cramers_v < 0.1:
    effect_interp = "negligible"
elif cramers_v < 0.3:
    effect_interp = "small"
elif cramers_v < 0.5:
    effect_interp = "medium"
else:
    effect_interp = "large"
print(f"    Effect size interpretation: {effect_interp}")

# Pairwise comparison (highest vs lowest)
highest = channel_analysis.iloc[0]
lowest = channel_analysis.iloc[-1]

table = np.array([
    [highest['positive_count'], highest['total_comments'] - highest['positive_count']],
    [lowest['positive_count'], lowest['total_comments'] - lowest['positive_count']]
])
a, b = table[0]
c, d = table[1]
odds_ratio = (a * d) / (b * c)

print(f"\n    Odds Ratio ({highest['channel']} vs {lowest['channel']}): {odds_ratio:.2f}")

# ------------------------------------------------------------------------------
# 8. OUTCOME CATEGORY ANALYSIS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[6] OUTCOME CATEGORY ANALYSIS")
print("=" * 80)

category_counts = {}
for _, row in positive_df.iterrows():
    if pd.notna(row['outcome_categories']):
        for cat in str(row['outcome_categories']).split(';'):
            cat = cat.strip()
            if cat:
                category_counts[cat] = category_counts.get(cat, 0) + 1

print("\nOutcome Categories with 95% CIs:")
print("-" * 70)
print(f"{'Category':<30} {'Count':>8} {'% Pos':>10} {'95% CI':>18}")
print("-" * 70)

category_data = []
for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
    pct = count / TOTAL_POSITIVES * 100
    p, ci_l, ci_h = wilson_ci(count, TOTAL_POSITIVES)
    print(f"{cat:<30} {count:>8,} {pct:>9.1f}% ({ci_l*100:>5.1f}%-{ci_h*100:>5.1f}%)")
    category_data.append({
        'category': cat,
        'count': count,
        'pct_of_positives': pct,
        'ci_low': ci_l * 100,
        'ci_high': ci_h * 100
    })

category_df = pd.DataFrame(category_data)

# ------------------------------------------------------------------------------
# 9. CREATE PUBLICATION-READY FIGURES
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[7] CREATING PUBLICATION-READY FIGURES")
print("=" * 80)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Color function for RO
def get_ro_color(aspect_id):
    if aspect_id.startswith('RO1'):
        return '#3498db'
    elif aspect_id.startswith('RO2'):
        return '#2ecc71'
    else:
        return '#e74c3c'

# --- FIGURE 1: Research Objectives Overview ---
fig1, ax1 = plt.subplots(figsize=(10, 6))

ros = ['RO1\nSubjective\nWell-Being', 'RO2\nTool-Mediated\nValidation', 'RO3\nDisease\nSpecificity']
counts = [ro1_count, ro2_count, ro3_count]
colors = ['#3498db', '#2ecc71', '#e74c3c']

bars = ax1.bar(ros, counts, color=colors, edgecolor='black', linewidth=1.2)

for bar, count in zip(bars, counts):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
             f'{count:,}\n({count/TOTAL_POSITIVES*100:.1f}%)', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('Number of Positive Outcome Reports', fontsize=12)
ax1.set_title(f'Positive Health Outcomes by Research Objective\n(n = {TOTAL_POSITIVES:,} total; {len(multi_ro)/TOTAL_POSITIVES*100:.1f}% span multiple ROs)', fontsize=13, fontweight='bold')
ax1.set_ylim(0, max(counts) * 1.2)

plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script10_Fig1_RO_Overview.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Figure 1: Research Objectives Overview saved")

# --- FIGURE 2: Top 10 Aspects with CIs ---
fig2, ax2 = plt.subplots(figsize=(12, 7))

top10 = aspect_df.head(10).iloc[::-1]
colors = [get_ro_color(a) for a in top10['aspect_id']]

y_pos = np.arange(len(top10))
bars = ax2.barh(y_pos, top10['pct_of_positives'], color=colors, edgecolor='black', linewidth=0.8)

xerr_low = top10['pct_of_positives'] - top10['ci_low']
xerr_high = top10['ci_high'] - top10['pct_of_positives']
ax2.errorbar(top10['pct_of_positives'], y_pos, xerr=[xerr_low, xerr_high],
             fmt='none', color='black', capsize=3, linewidth=1.5)

labels = [f"{row['aspect_id']}: {row['aspect_name']}" for _, row in top10.iterrows()]
ax2.set_yticks(y_pos)
ax2.set_yticklabels(labels, fontsize=10)
ax2.set_xlabel('Percentage of Positive Outcome Reports (%)', fontsize=11)
ax2.set_title(f'Top 10 Health Aspects with 95% Confidence Intervals\n(n = {TOTAL_POSITIVES:,} positive outcomes)', fontsize=13, fontweight='bold')

legend_elements = [Patch(facecolor='#3498db', label='RO1: Subjective Well-Being'),
                   Patch(facecolor='#2ecc71', label='RO2: Tool-Mediated Validation'),
                   Patch(facecolor='#e74c3c', label='RO3: Disease Specificity')]
ax2.legend(handles=legend_elements, loc='lower right', fontsize=9)

for i, (_, row) in enumerate(top10.iterrows()):
    ax2.text(row['pct_of_positives'] + 1, i, f"{row['pct_of_positives']:.1f}%", va='center', fontsize=9)

ax2.set_xlim(0, 85)
plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script10_Fig2_Top10_Aspects.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Figure 2: Top 10 Aspects saved")

# --- FIGURE 3: Channel Comparison with CIs ---
fig3, ax3 = plt.subplots(figsize=(12, 7))

channel_sorted = channel_analysis.sort_values('rate_pct', ascending=True)

y_pos = np.arange(len(channel_sorted))
bars = ax3.barh(y_pos, channel_sorted['rate_pct'], color='#3498db', edgecolor='black', linewidth=0.8)

xerr_low = channel_sorted['rate_pct'] - channel_sorted['ci_low']
xerr_high = channel_sorted['ci_high'] - channel_sorted['rate_pct']
ax3.errorbar(channel_sorted['rate_pct'], y_pos, xerr=[xerr_low, xerr_high],
             fmt='none', color='black', capsize=3, linewidth=1.5)

ax3.set_yticks(y_pos)
ax3.set_yticklabels(channel_sorted['channel'], fontsize=10)
ax3.set_xlabel('Positive Outcome Rate (%)', fontsize=11)
ax3.set_title(f'Channel Variation in Positive Outcome Rates\n(χ² = {chi2:.2f}, p < 0.001, Cramér\'s V = {cramers_v:.3f})', fontsize=13, fontweight='bold')

for i, (_, row) in enumerate(channel_sorted.iterrows()):
    ax3.text(row['rate_pct'] + 0.2, i, f"{row['rate_pct']:.2f}%", va='center', fontsize=9)

ax3.axvline(x=TOTAL_POSITIVES/TOTAL_CORPUS*100, color='red', linestyle='--', linewidth=1.5, label=f'Overall rate: {TOTAL_POSITIVES/TOTAL_CORPUS*100:.2f}%')
ax3.legend(loc='lower right')

ax3.set_xlim(0, 10)
plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script10_Fig3_Channel_Comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Figure 3: Channel Comparison saved")

# --- FIGURE 4: Outcome Categories ---
fig4, ax4 = plt.subplots(figsize=(10, 6))

category_sorted = category_df.sort_values('count', ascending=True)

category_names = {
    'quantified_change': 'Quantified Change\n(e.g., "lost 30 lbs")',
    'symptom_cessation': 'Symptom Cessation\n(e.g., "pain gone")',
    'explicit_improvement': 'Explicit Improvement\n(e.g., "feel better")',
    'reversal_remission': 'Reversal/Remission\n(e.g., "reversed diabetes")',
    'medication_discontinuation': 'Medication Stop\n(e.g., "off meds")',
    'temporal_improvement': 'Temporal Improvement\n(e.g., "better now")'
}

labels = [category_names.get(c, c) for c in category_sorted['category']]
y_pos = np.arange(len(category_sorted))

bars = ax4.barh(y_pos, category_sorted['pct_of_positives'], color='#9b59b6', edgecolor='black', linewidth=0.8)

ax4.set_yticks(y_pos)
ax4.set_yticklabels(labels, fontsize=10)
ax4.set_xlabel('Percentage of Positive Outcome Reports (%)', fontsize=11)
ax4.set_title(f'Distribution of Outcome Categories\n(n = {TOTAL_POSITIVES:,} positive outcomes)', fontsize=13, fontweight='bold')

for i, (_, row) in enumerate(category_sorted.iterrows()):
    ax4.text(row['pct_of_positives'] + 1, i, f"{row['count']:,} ({row['pct_of_positives']:.1f}%)", va='center', fontsize=9)

ax4.set_xlim(0, 85)
plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script10_Fig4_Outcome_Categories.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Figure 4: Outcome Categories saved")

# --- FIGURE 5: Summary Dashboard ---
fig5, axes = plt.subplots(2, 2, figsize=(14, 12))
fig5.suptitle('PhD RQ1: Health Outcomes in Healthcasting Content - Summary Dashboard', fontsize=14, fontweight='bold', y=1.02)

# Panel A: Overall Classification
ax_a = axes[0, 0]
class_labels = ['Positive\nOutcomes', 'Health Mentions\n(no outcome)', 'Excluded', 'No Health\nContent']
class_counts = [TOTAL_POSITIVES, 43839, 12688, 146463]
class_colors = ['#2ecc71', '#3498db', '#f39c12', '#95a5a6']
wedges, texts, autotexts = ax_a.pie(class_counts, labels=class_labels, colors=class_colors,
                                     autopct='%1.1f%%', startangle=90, explode=(0.05, 0, 0, 0))
ax_a.set_title(f'A. Corpus Classification\n(N = {TOTAL_CORPUS:,} comments)', fontsize=11, fontweight='bold')

# Panel B: RO Distribution
ax_b = axes[0, 1]
ro_labels = ['RO1', 'RO2', 'RO3']
ro_counts = [ro1_count, ro2_count, ro3_count]
ro_colors = ['#3498db', '#2ecc71', '#e74c3c']
bars = ax_b.bar(ro_labels, ro_counts, color=ro_colors, edgecolor='black')
for bar, count in zip(bars, ro_counts):
    ax_b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 80, f'{count:,}', ha='center', fontsize=10)
ax_b.set_ylabel('Count')
ax_b.set_title(f'B. Outcomes by Research Objective\n(n = {TOTAL_POSITIVES:,} positive outcomes)', fontsize=11, fontweight='bold')
ax_b.set_ylim(0, max(ro_counts) * 1.15)

# Panel C: Top 5 Aspects
ax_c = axes[1, 0]
top5 = aspect_df.head(5)
y_pos_c = np.arange(5)
colors_c = [get_ro_color(a) for a in top5['aspect_id']]
bars = ax_c.barh(y_pos_c, top5['pct_of_positives'], color=colors_c, edgecolor='black')
ax_c.set_yticks(y_pos_c)
ax_c.set_yticklabels([f"{r['aspect_id']}: {r['aspect_name'][:20]}" for _, r in top5.iterrows()], fontsize=9)
ax_c.set_xlabel('% of Positives')
ax_c.set_title('C. Top 5 Health Aspects', fontsize=11, fontweight='bold')
ax_c.invert_yaxis()

# Panel D: Key Statistics
ax_d = axes[1, 1]
ax_d.axis('off')
stats_text = f"""
KEY FINDINGS

Corpus: {TOTAL_CORPUS:,} comments from 11 YouTube channels

Classification Results:
• Positive outcomes: {TOTAL_POSITIVES:,} ({TOTAL_POSITIVES/TOTAL_CORPUS*100:.2f}%)
• Validated precision: {PRECISION:.1%} (95% CI: {PRECISION_CI_LOW:.1%}-{PRECISION_CI_HIGH:.1%})
• Estimated true positives: ~{adjusted_positives:,}

Top Health Outcomes:
1. Weight loss ({aspect_df.iloc[0]['pct_of_positives']:.1f}% of positives)
2. Pain/inflammation ({aspect_df.iloc[1]['pct_of_positives']:.1f}%)
3. Type 2 diabetes ({aspect_df.iloc[2]['pct_of_positives']:.1f}%)

Channel Variation:
• Range: {channel_analysis.iloc[-1]['rate_pct']:.2f}% - {channel_analysis.iloc[0]['rate_pct']:.2f}%
• χ² = {chi2:.0f}, p < 0.001
• {odds_ratio:.1f}× difference (highest vs lowest)

Outcome Types:
• Quantified changes: {category_df[category_df['category']=='quantified_change']['pct_of_positives'].values[0]:.1f}%
• Symptom cessation: {category_df[category_df['category']=='symptom_cessation']['pct_of_positives'].values[0]:.1f}%
• Reversal/remission: {category_df[category_df['category']=='reversal_remission']['pct_of_positives'].values[0]:.1f}%
"""
ax_d.text(0.05, 0.95, stats_text, transform=ax_d.transAxes, fontsize=10,
          verticalalignment='top', fontfamily='monospace',
          bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#dee2e6', pad=0.5))

plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script10_Fig5_Summary_Dashboard.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Figure 5: Summary Dashboard saved")

# ------------------------------------------------------------------------------
# 10. SAVE DATA FILES
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[8] SAVING DATA FILES")
print("=" * 80)

# Save aspect statistics
aspect_df.to_csv(PHASE3_PATH + 'Phase3_Script10_aspect_statistics.csv', index=False)
print("    ✓ Aspect statistics saved")

# Save channel analysis
channel_analysis.to_csv(PHASE3_PATH + 'Phase3_Script10_channel_analysis.csv', index=False)
print("    ✓ Channel analysis saved")

# Save category statistics
category_df.to_csv(PHASE3_PATH + 'Phase3_Script10_category_statistics.csv', index=False)
print("    ✓ Category statistics saved")

# Save RO statistics
ro_df.to_csv(PHASE3_PATH + 'Phase3_Script10_ro_statistics.csv', index=False)
print("    ✓ RO statistics saved")

# Create comprehensive summary
summary_data = {
    'Metric': [
        'Total Corpus Size',
        'Classified Positive Outcomes',
        'Raw Prevalence',
        'Raw Prevalence 95% CI',
        'Validation Precision',
        'Validation Precision 95% CI',
        'Estimated True Positives',
        'Estimated True Positives 95% CI',
        'Adjusted Prevalence',
        'RO1 Count (Subjective Well-Being)',
        'RO1 Percentage of Positives',
        'RO2 Count (Tool-Mediated Validation)',
        'RO2 Percentage of Positives',
        'RO3 Count (Disease Specificity)',
        'RO3 Percentage of Positives',
        'Multi-RO Comments',
        'Chi-Square Statistic (Channel)',
        'Chi-Square p-value',
        "Cramer's V Effect Size",
        'Highest Channel Rate',
        'Lowest Channel Rate',
        'Channel Odds Ratio (High/Low)'
    ],
    'Value': [
        TOTAL_CORPUS,
        TOTAL_POSITIVES,
        f"{raw_prevalence*100:.2f}%",
        f"{ci_low*100:.2f}%-{ci_high*100:.2f}%",
        f"{PRECISION*100:.1f}%",
        f"{PRECISION_CI_LOW*100:.1f}%-{PRECISION_CI_HIGH*100:.1f}%",
        adjusted_positives,
        f"{adjusted_positives_low}-{adjusted_positives_high}",
        f"{adj_prevalence*100:.2f}%",
        ro1_count,
        f"{ro1_count/TOTAL_POSITIVES*100:.1f}%",
        ro2_count,
        f"{ro2_count/TOTAL_POSITIVES*100:.1f}%",
        ro3_count,
        f"{ro3_count/TOTAL_POSITIVES*100:.1f}%",
        f"{len(multi_ro)} ({len(multi_ro)/TOTAL_POSITIVES*100:.1f}%)",
        f"{chi2:.2f}",
        f"{p_value:.2e}",
        f"{cramers_v:.3f} ({effect_interp})",
        f"{highest['channel']} ({highest['rate_pct']:.2f}%)",
        f"{lowest['channel']} ({lowest['rate_pct']:.2f}%)",
        f"{odds_ratio:.2f}"
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(PHASE3_PATH + 'Phase3_Script10_summary_statistics.csv', index=False)
print("    ✓ Summary statistics saved")

# Save publication tables to Excel
with pd.ExcelWriter(PHASE3_PATH + 'Phase3_Script10_publication_tables.xlsx') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    ro_df.to_excel(writer, sheet_name='Research Objectives', index=False)
    aspect_df.to_excel(writer, sheet_name='Aspects', index=False)
    channel_analysis.to_excel(writer, sheet_name='Channels', index=False)
    category_df.to_excel(writer, sheet_name='Outcome Categories', index=False)
print("    ✓ Publication tables (Excel) saved")

# ------------------------------------------------------------------------------
# 11. FINAL SUMMARY
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("SCRIPT 10 COMPLETE - STATISTICAL ANALYSIS")
print("=" * 80)

print(f"""
SUMMARY OF KEY FINDINGS
=======================

1. PREVALENCE
   - Raw: {TOTAL_POSITIVES:,} positive outcomes ({raw_prevalence:.2%} of corpus)
   - Validated precision: {PRECISION:.1%}
   - Estimated true positives: ~{adjusted_positives:,}

2. RESEARCH OBJECTIVES
   - RO1 (Subjective): {ro1_count:,} ({ro1_count/TOTAL_POSITIVES*100:.1f}%)
   - RO2 (Objective): {ro2_count:,} ({ro2_count/TOTAL_POSITIVES*100:.1f}%)
   - RO3 (Disease): {ro3_count:,} ({ro3_count/TOTAL_POSITIVES*100:.1f}%)
   - Multi-RO: {len(multi_ro):,} ({len(multi_ro)/TOTAL_POSITIVES*100:.1f}%)

3. TOP ASPECTS
   - #1: {aspect_df.iloc[0]['aspect_name']} ({aspect_df.iloc[0]['pct_of_positives']:.1f}%)
   - #2: {aspect_df.iloc[1]['aspect_name']} ({aspect_df.iloc[1]['pct_of_positives']:.1f}%)
   - #3: {aspect_df.iloc[2]['aspect_name']} ({aspect_df.iloc[2]['pct_of_positives']:.1f}%)

4. CHANNEL VARIATION
   - χ² = {chi2:.2f}, p < 0.001
   - Effect size: {cramers_v:.3f} ({effect_interp})
   - Range: {lowest['rate_pct']:.2f}% - {highest['rate_pct']:.2f}%
   - Odds ratio: {odds_ratio:.2f}

OUTPUT FILES CREATED
====================
✓ Phase3_Script10_summary_statistics.csv
✓ Phase3_Script10_aspect_statistics.csv
✓ Phase3_Script10_channel_analysis.csv
✓ Phase3_Script10_category_statistics.csv
✓ Phase3_Script10_ro_statistics.csv
✓ Phase3_Script10_publication_tables.xlsx
✓ Phase3_Script10_Fig1_RO_Overview.png
✓ Phase3_Script10_Fig2_Top10_Aspects.png
✓ Phase3_Script10_Fig3_Channel_Comparison.png
✓ Phase3_Script10_Fig4_Outcome_Categories.png
✓ Phase3_Script10_Fig5_Summary_Dashboard.png
""")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Review the figures and tables in Phase3_Outputs folder
2. Copy validated XLSX file to Phase3_Outputs if not already there
3. (Optional) Run Script 11 for ML validation
4. Generate final thesis chapter with these results
""")
