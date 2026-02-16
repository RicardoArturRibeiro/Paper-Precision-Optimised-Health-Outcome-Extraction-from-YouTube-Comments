# ==============================================================================
# PhD THESIS RQ1 - PHASE 3: SCRIPT 11
# MACHINE LEARNING BASELINE COMPARISON & RECALL ESTIMATION
# ==============================================================================
#
# Purpose: Compare rule-based classification with ML baselines and estimate recall
#
# Input:   - PhD_RQ1_youtube_comments_corpus_final.csv (full corpus)
#          - Phase3_Script8_positive_outcomes.csv (classified positives)
#          - Phase2_Script5_final_ontology.csv (ontology)
#
# Output:  - Phase3_Script11_model_comparison.csv
#          - Phase3_Script11_confusion_matrices.png
#          - Phase3_Script11_roc_curves.png
#          - Phase3_Script11_precision_recall_curves.png
#          - Phase3_Script11_recall_estimation_sample.xlsx
#          - Phase3_Script11_summary_statistics.csv
#
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. SETUP AND IMPORTS
# ------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ML imports
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (classification_report, confusion_matrix,
                             precision_score, recall_score, f1_score,
                             roc_curve, auc, precision_recall_curve,
                             average_precision_score, accuracy_score)
from sklearn.preprocessing import label_binarize
import re
import string

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Define paths
BASE_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/'
PHASE2_PATH = BASE_PATH + 'Phase2_Outputs/'
PHASE3_PATH = BASE_PATH + 'Phase3_Outputs/'

print("=" * 80)
print("PhD RQ1 - SCRIPT 11: ML BASELINE COMPARISON & RECALL ESTIMATION")
print("=" * 80)

# ------------------------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------------------------

print("\n[1] Loading data files...")

# Load full corpus
print("    Loading full corpus (this may take a moment)...")
corpus_df = pd.read_csv(BASE_PATH + 'PhD_RQ1_youtube_comments_corpus_final.csv')
print(f"    ✓ Full corpus loaded: {len(corpus_df):,} comments")

# Load positive outcomes
positive_df = pd.read_csv(PHASE3_PATH + 'Phase3_Script8_positive_outcomes.csv')
print(f"    ✓ Positive outcomes loaded: {len(positive_df):,} rows")

# Load ontology
ontology_df = pd.read_csv(PHASE2_PATH + 'Phase2_Script5_final_ontology.csv')
print(f"    ✓ Ontology loaded: {len(ontology_df)} aspects")

# Get comment text column name
text_col = None
for col in ['comment_text', 'text', 'comment', 'Comment', 'Text']:
    if col in corpus_df.columns:
        text_col = col
        break

if text_col is None:
    print("    Available columns:", corpus_df.columns.tolist())
    text_col = input("    Enter the comment text column name: ")

print(f"    Using text column: '{text_col}'")

# ------------------------------------------------------------------------------
# 3. CREATE LABELED DATASET
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[2] CREATING LABELED DATASET")
print("=" * 80)

# Get positive comment IDs/texts
positive_texts = set(positive_df['comment_text'].str.lower().str.strip())
print(f"    Positive outcomes: {len(positive_texts):,}")

# Label all corpus comments
corpus_df['text_lower'] = corpus_df[text_col].astype(str).str.lower().str.strip()
corpus_df['label'] = corpus_df['text_lower'].isin(positive_texts).astype(int)

n_positive = corpus_df['label'].sum()
n_negative = len(corpus_df) - n_positive
print(f"    Labeled positives in corpus: {n_positive:,}")
print(f"    Labeled negatives in corpus: {n_negative:,}")

# Create balanced dataset for training
# Sample negatives to create roughly 1:2 ratio (positives : negatives)
np.random.seed(42)

positive_samples = corpus_df[corpus_df['label'] == 1].copy()
n_neg_sample = min(n_positive * 2, n_negative)  # 2:1 ratio or all available
negative_samples = corpus_df[corpus_df['label'] == 0].sample(n=n_neg_sample, random_state=42).copy()

dataset = pd.concat([positive_samples, negative_samples], ignore_index=True)
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

print(f"\n    Training dataset created:")
print(f"    - Positive samples: {len(positive_samples):,}")
print(f"    - Negative samples: {len(negative_samples):,}")
print(f"    - Total: {len(dataset):,}")
print(f"    - Class ratio: 1:{n_neg_sample/n_positive:.1f}")

# ------------------------------------------------------------------------------
# 4. TEXT PREPROCESSING
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[3] TEXT PREPROCESSING")
print("=" * 80)

def preprocess_text(text):
    """Clean and preprocess text for ML."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove special characters but keep health-related punctuation
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

dataset['text_clean'] = dataset[text_col].apply(preprocess_text)
print(f"    ✓ Text preprocessing complete")

# Remove empty texts
dataset = dataset[dataset['text_clean'].str.len() > 10].reset_index(drop=True)
print(f"    ✓ After removing short texts: {len(dataset):,} samples")

# ------------------------------------------------------------------------------
# 5. FEATURE EXTRACTION
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[4] FEATURE EXTRACTION (TF-IDF)")
print("=" * 80)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.95,
    stop_words='english'
)

X = tfidf.fit_transform(dataset['text_clean'])
y = dataset['label'].values

print(f"    ✓ TF-IDF features: {X.shape[1]:,}")
print(f"    ✓ Vocabulary size: {len(tfidf.vocabulary_):,}")

# ------------------------------------------------------------------------------
# 6. TRAIN/TEST SPLIT
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[5] TRAIN/TEST SPLIT")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"    Training set: {X_train.shape[0]:,} samples")
print(f"    Test set: {X_test.shape[0]:,} samples")
print(f"    Positive in train: {y_train.sum():,} ({y_train.sum()/len(y_train)*100:.1f}%)")
print(f"    Positive in test: {y_test.sum():,} ({y_test.sum()/len(y_test)*100:.1f}%)")

# ------------------------------------------------------------------------------
# 7. TRAIN ML MODELS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[6] TRAINING ML MODELS")
print("=" * 80)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', n_jobs=-1),
    'Linear SVM': LinearSVC(random_state=42, class_weight='balanced', max_iter=2000),
    'Naive Bayes': MultinomialNB(alpha=0.1),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)
}

results = []
trained_models = {}

for name, model in models.items():
    print(f"\n    Training {name}...")

    # Train
    model.fit(X_train, y_train)
    trained_models[name] = model

    # Predict
    y_pred = model.predict(X_test)

    # For models that support probability
    if hasattr(model, 'predict_proba'):
        y_prob = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, 'decision_function'):
        y_prob = model.decision_function(X_test)
        # Normalize to 0-1 range for ROC
        y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())
    else:
        y_prob = y_pred

    # Metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)

    # Cross-validation F1
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')

    results.append({
        'Model': name,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'Accuracy': accuracy,
        'CV F1 Mean': cv_scores.mean(),
        'CV F1 Std': cv_scores.std(),
        'y_prob': y_prob
    })

    print(f"        Precision: {precision:.3f}")
    print(f"        Recall: {recall:.3f}")
    print(f"        F1-Score: {f1:.3f}")
    print(f"        CV F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# ------------------------------------------------------------------------------
# 8. ADD RULE-BASED RESULTS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[7] ADDING RULE-BASED RESULTS")
print("=" * 80)

# Rule-based validation results (from Script 10)
RULE_BASED_PRECISION = 0.976
RULE_BASED_PRECISION_CI = (0.957, 0.986)

# Estimate rule-based recall (we'll refine this with manual checking)
# For now, use a conservative estimate based on precision-optimized design
# This will be updated after recall estimation

results.append({
    'Model': 'Rule-Based (Ours)',
    'Precision': RULE_BASED_PRECISION,
    'Recall': np.nan,  # To be estimated
    'F1-Score': np.nan,  # To be calculated after recall estimation
    'Accuracy': np.nan,
    'CV F1 Mean': np.nan,
    'CV F1 Std': np.nan,
    'y_prob': None
})

print(f"    Rule-based precision: {RULE_BASED_PRECISION:.3f}")
print(f"    Rule-based recall: To be estimated from negative sampling")

# ------------------------------------------------------------------------------
# 9. CREATE COMPARISON TABLE
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[8] MODEL COMPARISON TABLE")
print("=" * 80)

results_df = pd.DataFrame(results)
results_df_display = results_df[['Model', 'Precision', 'Recall', 'F1-Score', 'Accuracy', 'CV F1 Mean', 'CV F1 Std']].copy()

# Sort by F1-Score (descending), keeping Rule-Based at top for comparison
ml_results = results_df_display[results_df_display['Model'] != 'Rule-Based (Ours)'].sort_values('F1-Score', ascending=False)
rb_results = results_df_display[results_df_display['Model'] == 'Rule-Based (Ours)']
results_df_sorted = pd.concat([rb_results, ml_results], ignore_index=True)

print("\n" + results_df_sorted.to_string(index=False))

# ------------------------------------------------------------------------------
# 10. GENERATE FIGURES
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[9] GENERATING FIGURES")
print("=" * 80)

plt.style.use('seaborn-v0_8-whitegrid')

# --- Figure 1: Model Comparison Bar Chart ---
fig1, ax1 = plt.subplots(figsize=(12, 6))

models_names = [r['Model'] for r in results if r['Model'] != 'Rule-Based (Ours)']
precisions = [r['Precision'] for r in results if r['Model'] != 'Rule-Based (Ours)']
recalls = [r['Recall'] for r in results if r['Model'] != 'Rule-Based (Ours)']
f1_scores = [r['F1-Score'] for r in results if r['Model'] != 'Rule-Based (Ours)']

x = np.arange(len(models_names))
width = 0.25

bars1 = ax1.bar(x - width, precisions, width, label='Precision', color='#3498db')
bars2 = ax1.bar(x, recalls, width, label='Recall', color='#2ecc71')
bars3 = ax1.bar(x + width, f1_scores, width, label='F1-Score', color='#e74c3c')

# Add rule-based precision line
ax1.axhline(y=RULE_BASED_PRECISION, color='#9b59b6', linestyle='--', linewidth=2,
            label=f'Rule-Based Precision ({RULE_BASED_PRECISION:.1%})')

ax1.set_xlabel('Model', fontsize=12)
ax1.set_ylabel('Score', fontsize=12)
ax1.set_title('ML Model Comparison vs. Rule-Based Classification', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(models_names, rotation=15, ha='right')
ax1.legend(loc='lower right')
ax1.set_ylim(0, 1.1)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script11_model_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Model comparison figure saved")

# --- Figure 2: Confusion Matrices ---
fig2, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, (name, model) in enumerate(trained_models.items()):
    if idx >= 5:
        break

    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['Negative', 'Positive'],
                yticklabels=['Negative', 'Positive'])
    axes[idx].set_title(f'{name}', fontsize=11, fontweight='bold')
    axes[idx].set_xlabel('Predicted')
    axes[idx].set_ylabel('Actual')

# Hide last subplot if odd number
if len(trained_models) < 6:
    axes[-1].axis('off')

plt.suptitle('Confusion Matrices for ML Models', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script11_confusion_matrices.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Confusion matrices figure saved")

# --- Figure 3: ROC Curves ---
fig3, ax3 = plt.subplots(figsize=(10, 8))

colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']

for idx, result in enumerate(results):
    if result['Model'] == 'Rule-Based (Ours)' or result['y_prob'] is None:
        continue

    y_prob = result['y_prob']
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    ax3.plot(fpr, tpr, color=colors[idx % len(colors)], linewidth=2,
             label=f"{result['Model']} (AUC = {roc_auc:.3f})")

ax3.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
ax3.set_xlabel('False Positive Rate', fontsize=12)
ax3.set_ylabel('True Positive Rate', fontsize=12)
ax3.set_title('ROC Curves for ML Models', fontsize=14, fontweight='bold')
ax3.legend(loc='lower right')
ax3.set_xlim([0, 1])
ax3.set_ylim([0, 1.05])

plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script11_roc_curves.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ ROC curves figure saved")

# --- Figure 4: Precision-Recall Curves ---
fig4, ax4 = plt.subplots(figsize=(10, 8))

for idx, result in enumerate(results):
    if result['Model'] == 'Rule-Based (Ours)' or result['y_prob'] is None:
        continue

    y_prob = result['y_prob']
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_prob)
    ap = average_precision_score(y_test, y_prob)

    ax4.plot(recall_curve, precision_curve, color=colors[idx % len(colors)], linewidth=2,
             label=f"{result['Model']} (AP = {ap:.3f})")

# Add rule-based point
ax4.scatter([np.nan], [RULE_BASED_PRECISION], color='#9b59b6', s=200, marker='*',
            zorder=5, label=f'Rule-Based (Precision = {RULE_BASED_PRECISION:.3f})')

ax4.set_xlabel('Recall', fontsize=12)
ax4.set_ylabel('Precision', fontsize=12)
ax4.set_title('Precision-Recall Curves for ML Models', fontsize=14, fontweight='bold')
ax4.legend(loc='lower left')
ax4.set_xlim([0, 1])
ax4.set_ylim([0, 1.05])

plt.tight_layout()
plt.savefig(PHASE3_PATH + 'Phase3_Script11_precision_recall_curves.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("    ✓ Precision-recall curves figure saved")

# ------------------------------------------------------------------------------
# 11. RECALL ESTIMATION - NEGATIVE SAMPLING
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[10] RECALL ESTIMATION - NEGATIVE SAMPLING")
print("=" * 80)

# Sample from comments that were NOT classified as positive
# These are potential false negatives
non_positive_df = corpus_df[corpus_df['label'] == 0].copy()

# Stratified sample by channel if channel column exists
channel_col = None
for col in ['channel_name', 'channel', 'Channel']:
    if col in non_positive_df.columns:
        channel_col = col
        break

if channel_col:
    print(f"    Stratifying by channel: '{channel_col}'")
    # Sample proportionally from each channel
    recall_sample = non_positive_df.groupby(channel_col, group_keys=False).apply(
        lambda x: x.sample(n=min(50, len(x)), random_state=42)
    )
    recall_sample = recall_sample.sample(n=min(500, len(recall_sample)), random_state=42)
else:
    recall_sample = non_positive_df.sample(n=500, random_state=42)

print(f"    ✓ Sampled {len(recall_sample)} non-positive comments for recall estimation")

# Prepare for manual review
recall_sample_export = recall_sample[[text_col]].copy()
recall_sample_export.columns = ['comment_text']
recall_sample_export['sample_id'] = range(1, len(recall_sample_export) + 1)
recall_sample_export['is_actually_positive'] = ''  # For manual coding
recall_sample_export['notes'] = ''

# Reorder columns
recall_sample_export = recall_sample_export[['sample_id', 'comment_text', 'is_actually_positive', 'notes']]

# Save to Excel
recall_sample_export.to_excel(PHASE3_PATH + 'Phase3_Script11_recall_estimation_sample.xlsx', index=False)
print(f"    ✓ Recall estimation sample saved to Excel")

print(f"""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║  MANUAL STEP REQUIRED FOR RECALL ESTIMATION                                  ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║  1. Open: Phase3_Script11_recall_estimation_sample.xlsx                      ║
    ║  2. For each comment, mark 'is_actually_positive' as:                        ║
    ║     - 'Yes' if it contains a positive health outcome (FALSE NEGATIVE)        ║
    ║     - 'No' if correctly classified as non-positive                           ║
    ║  3. Save the file and run the recall calculation cell below                  ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
""")

# ------------------------------------------------------------------------------
# 12. SAVE RESULTS
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("[11] SAVING RESULTS")
print("=" * 80)

# Save model comparison
results_df_sorted.to_csv(PHASE3_PATH + 'Phase3_Script11_model_comparison.csv', index=False)
print("    ✓ Model comparison saved")

# Create summary statistics
best_ml = ml_results.iloc[0]
summary_stats = {
    'Metric': [
        'Total Corpus Size',
        'Training Dataset Size',
        'Test Dataset Size',
        'Positive Samples',
        'Negative Samples',
        'TF-IDF Features',
        'Best ML Model',
        'Best ML Precision',
        'Best ML Recall',
        'Best ML F1-Score',
        'Rule-Based Precision',
        'Rule-Based Precision 95% CI',
        'Precision Advantage (Rule-Based vs Best ML)',
        'Recall Estimation Sample Size'
    ],
    'Value': [
        f"{len(corpus_df):,}",
        f"{len(dataset):,}",
        f"{X_test.shape[0]:,}",
        f"{len(positive_samples):,}",
        f"{len(negative_samples):,}",
        f"{X.shape[1]:,}",
        best_ml['Model'],
        f"{best_ml['Precision']:.3f}",
        f"{best_ml['Recall']:.3f}",
        f"{best_ml['F1-Score']:.3f}",
        f"{RULE_BASED_PRECISION:.3f}",
        f"{RULE_BASED_PRECISION_CI[0]:.3f} - {RULE_BASED_PRECISION_CI[1]:.3f}",
        f"{RULE_BASED_PRECISION - best_ml['Precision']:.3f} ({(RULE_BASED_PRECISION - best_ml['Precision'])/best_ml['Precision']*100:.1f}%)",
        f"{len(recall_sample_export)}"
    ]
}

summary_df = pd.DataFrame(summary_stats)
summary_df.to_csv(PHASE3_PATH + 'Phase3_Script11_summary_statistics.csv', index=False)
print("    ✓ Summary statistics saved")

# ------------------------------------------------------------------------------
# 13. FINAL SUMMARY
# ------------------------------------------------------------------------------

print("\n" + "=" * 80)
print("SCRIPT 11 COMPLETE - ML BASELINE COMPARISON")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           RESULTS SUMMARY                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  RULE-BASED METHOD (OURS)                                                    ║
║  • Precision: {RULE_BASED_PRECISION:.1%} (95% CI: {RULE_BASED_PRECISION_CI[0]:.1%} - {RULE_BASED_PRECISION_CI[1]:.1%})                          ║
║  • Recall: Pending manual estimation                                         ║
║                                                                              ║
║  BEST ML MODEL: {best_ml['Model']:<30}                            ║
║  • Precision: {best_ml['Precision']:.1%}                                                         ║
║  • Recall: {best_ml['Recall']:.1%}                                                            ║
║  • F1-Score: {best_ml['F1-Score']:.1%}                                                          ║
║                                                                              ║
║  KEY FINDING:                                                                ║
║  Rule-based precision ({RULE_BASED_PRECISION:.1%}) exceeds best ML precision ({best_ml['Precision']:.1%})               ║
║  by {(RULE_BASED_PRECISION - best_ml['Precision'])*100:.1f} percentage points ({(RULE_BASED_PRECISION - best_ml['Precision'])/best_ml['Precision']*100:.1f}% relative improvement)                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

OUTPUT FILES CREATED:
• Phase3_Script11_model_comparison.csv
• Phase3_Script11_model_comparison.png
• Phase3_Script11_confusion_matrices.png
• Phase3_Script11_roc_curves.png
• Phase3_Script11_precision_recall_curves.png
• Phase3_Script11_recall_estimation_sample.xlsx
• Phase3_Script11_summary_statistics.csv

NEXT STEP:
Complete manual coding of 'Phase3_Script11_recall_estimation_sample.xlsx'
to estimate rule-based recall and calculate F1-score.
""")

# ==============================================================================
# CELL 2: RUN AFTER MANUAL RECALL CODING
# ==============================================================================
# Uncomment and run this cell after completing manual coding of recall sample

"""
print("=" * 80)
print("RECALL ESTIMATION - AFTER MANUAL CODING")
print("=" * 80)

# Load coded recall sample
recall_coded = pd.read_excel(PHASE3_PATH + 'Phase3_Script11_recall_estimation_sample.xlsx')

# Count false negatives
false_negatives = len(recall_coded[recall_coded['is_actually_positive'].str.lower() == 'yes'])
total_checked = len(recall_coded[recall_coded['is_actually_positive'].str.lower().isin(['yes', 'no'])])

print(f"    Total coded: {total_checked}")
print(f"    False negatives found: {false_negatives}")

# Estimate false negative rate in non-positive corpus
fn_rate = false_negatives / total_checked
fn_rate_ci_low, fn_rate_ci_high = proportion_confint(false_negatives, total_checked, method='wilson')

print(f"    False negative rate: {fn_rate:.2%} (95% CI: {fn_rate_ci_low:.2%} - {fn_rate_ci_high:.2%})")

# Estimate total false negatives in corpus
non_positive_count = len(corpus_df) - len(positive_df)
estimated_fn = int(non_positive_count * fn_rate)
estimated_fn_low = int(non_positive_count * fn_rate_ci_low)
estimated_fn_high = int(non_positive_count * fn_rate_ci_high)

print(f"    Estimated false negatives in corpus: {estimated_fn:,} (95% CI: {estimated_fn_low:,} - {estimated_fn_high:,})")

# Calculate recall
true_positives = len(positive_df)
estimated_total_positives = true_positives + estimated_fn
recall = true_positives / estimated_total_positives

print(f"\\n    RECALL ESTIMATION:")
print(f"    True Positives (classified): {true_positives:,}")
print(f"    Estimated Total Positives: {estimated_total_positives:,}")
print(f"    Estimated Recall: {recall:.1%}")

# Calculate F1
precision = 0.976
f1 = 2 * (precision * recall) / (precision + recall)
print(f"    F1-Score: {f1:.1%}")

# Update results
print(f"\\n    FINAL RULE-BASED METRICS:")
print(f"    Precision: {precision:.1%}")
print(f"    Recall: {recall:.1%}")
print(f"    F1-Score: {f1:.1%}")
"""
