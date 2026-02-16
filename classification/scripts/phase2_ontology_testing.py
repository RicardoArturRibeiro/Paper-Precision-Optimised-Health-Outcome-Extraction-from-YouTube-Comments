# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 4 - Initial Ontology Construction & Testing
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script constructs the initial ontology structure based on findings from
# Scripts 1-3, then tests keyword coverage against the corpus to validate
# the ontology and identify gaps.
#
# Outputs:
# 1. Console output with ontology coverage statistics
# 2. CSV files with aspect-level coverage analysis
# 3. Sample matched comments for manual validation
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 4 of 6
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
import re
import os
from collections import defaultdict
from datetime import datetime
import warnings

from google.colab import drive

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 200)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 4 - Initial Ontology Construction & Testing")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Configuration
# ==============================================================================

drive.mount('/content/drive')

CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")


# ==============================================================================
# CELL 3: Define Complete Ontology Structure
# ==============================================================================

print("\n" + "=" * 70)
print("1. DEFINING ONTOLOGY STRUCTURE")
print("=" * 70)

# =============================================================================
# THE ONTOLOGY - Based on findings from Scripts 1-3
# =============================================================================

ONTOLOGY = {
    # =========================================================================
    # RO1: SUBJECTIVE WELL-BEING
    # "To quantify user-reported improvements in subjective well-being"
    # =========================================================================
    'RO1': {
        'name': 'Subjective Well-Being',
        'description': 'User-reported improvements in directly perceived, subjective states of metabolic health',
        'aspects': {
            'RO1.1': {
                'name': 'Cognitive Function',
                'keywords': [
                    'brain fog', 'brainfog', 'mental clarity', 'clarity', 'focus', 'focused',
                    'concentration', 'memory', 'cognitive', 'sharp', 'alert', 'clear headed',
                    'clearheaded', 'mental focus', 'brain function', 'thinking', 'foggy',
                    'brain is', 'my brain', 'mental performance'
                ],
                'exclusions': ['alzheimer', 'dementia', 'neurodegenerat']  # → RO3
            },
            'RO1.2': {
                'name': 'Energy & Vitality',
                'keywords': [
                    'energy', 'energetic', 'energized', 'tired', 'fatigue', 'fatigued',
                    'exhausted', 'exhaustion', 'lethargy', 'lethargic', 'vitality', 'vigor',
                    'stamina', 'endurance', 'more energy', 'no energy', 'energy level',
                    'full of energy', 'chronic fatigue'
                ],
                'exclusions': []
            },
            'RO1.3': {
                'name': 'Psychological Well-Being',
                'keywords': [
                    'anxiety', 'anxious', 'depression', 'depressed', 'mood', 'moods',
                    'stress', 'stressed', 'mental health', 'happier', 'happy', 'calm',
                    'peaceful', 'relaxed', 'irritable', 'irritability', 'emotional',
                    'well-being', 'wellbeing', 'positive', 'outlook', 'hopeful'
                ],
                'exclusions': ['adhd', 'add', 'attention deficit']  # → RO3
            },
            'RO1.4': {
                'name': 'Sleep Quality',
                'keywords': [
                    'sleep', 'sleeping', 'slept', 'insomnia', 'restful', 'rest',
                    'sleep better', 'better sleep', 'sleep quality', 'waking up',
                    'wake up', 'night', 'deep sleep', 'sleep apnea', 'apnea',
                    'cpap', 'snoring', 'snore', 'refreshed'
                ],
                'exclusions': []
            },
            'RO1.5': {
                'name': 'Appetite & Satiety',
                'keywords': [
                    'appetite', 'hungry', 'hunger', 'craving', 'cravings', 'satiety',
                    'satiated', 'full', 'fuller', 'not hungry', 'never hungry',
                    'sugar craving', 'carb craving', 'food craving', 'binge', 'binging',
                    'overeating', 'snacking', 'satisfied'
                ],
                'exclusions': []
            },
            'RO1.6': {
                'name': 'Pain & Inflammation',
                'keywords': [
                    'pain', 'ache', 'aches', 'aching', 'inflammation', 'inflammatory',
                    'joint pain', 'back pain', 'knee pain', 'chronic pain', 'body aches',
                    'stiff', 'stiffness', 'swelling', 'swollen', 'headache', 'headaches',
                    'migraine', 'migraines', 'soreness', 'sore'
                ],
                'exclusions': ['arthritis', 'fibromyalgia', 'gout']  # → RO3
            },
            'RO1.7': {
                'name': 'Digestive Health',
                'keywords': [
                    'digest', 'digestion', 'digestive', 'gut', 'gut health', 'bloat',
                    'bloating', 'bloated', 'gas', 'stomach', 'bowel', 'constipation',
                    'constipated', 'diarrhea', 'reflux', 'acid reflux', 'heartburn',
                    'gerd', 'leaky gut', 'gut issues', 'indigestion', 'nausea'
                ],
                'exclusions': ['ibs', 'irritable bowel', 'crohn', 'colitis', 'ibd']  # → RO3
            },
            'RO1.8': {
                'name': 'Skin Health',
                'keywords': [
                    'skin', 'skin tag', 'skin tags', 'acne', 'eczema', 'psoriasis',
                    'rash', 'rashes', 'complexion', 'clear skin', 'skin cleared',
                    'glowing', 'rosacea', 'hives', 'itchy', 'dry skin', 'oily skin',
                    'skin issue', 'skin problem', 'dermatitis', 'skin health'
                ],
                'exclusions': ['lupus rash', 'autoimmune']  # → RO3
            },
            'RO1.9': {
                'name': 'Hormonal & Menstrual Health',
                'keywords': [
                    'hormone', 'hormones', 'hormonal', 'period', 'periods', 'menstrual',
                    'menstruation', 'hot flash', 'hot flashes', 'menopause', 'menopausal',
                    'perimenopause', 'pms', 'cycle', 'monthly cycle', 'night sweats',
                    'regular period', 'irregular period'
                ],
                'exclusions': ['pcos', 'polycystic']  # → RO3
            }
        }
    },

    # =========================================================================
    # RO2: TOOL-MEDIATED VALIDATION
    # "To determine the prevalence of objective health metrics"
    # =========================================================================
    'RO2': {
        'name': 'Tool-Mediated Validation',
        'description': 'User-reported improvements in tool-mediated, objectively measured outcomes',
        'aspects': {
            'RO2.1': {
                'name': 'Anthropometric Changes',
                'keywords': [
                    'weight', 'lost weight', 'lose weight', 'weight loss', 'losing weight',
                    'pounds', 'lbs', 'kg', 'kilos', 'waist', 'inches', 'bmi',
                    'body fat', 'fat loss', 'dropped', 'scale', 'dress size', 'pant size',
                    'belt', 'clothing size', 'visceral fat', 'lean mass', 'body composition',
                    '10 pounds', '20 pounds', '30 pounds', '50 pounds', '100 pounds'
                ],
                'exclusions': []
            },
            'RO2.2': {
                'name': 'Glycemic Control',
                'keywords': [
                    'glucose', 'blood sugar', 'blood glucose', 'a1c', 'hba1c', 'my a1c',
                    'fasting glucose', 'fasting insulin', 'insulin', 'insulin level',
                    'insulin resistance', 'insulin resistant', 'cgm', 'glucometer',
                    'blood test', 'sugar level', 'glucose level', 'sugar spike',
                    'stable blood sugar', 'normal blood sugar'
                ],
                'exclusions': ['diabetes', 'diabetic', 'type 2', 't2d', 'prediabetes']  # → RO3
            },
            'RO2.3': {
                'name': 'Blood Pressure',
                'keywords': [
                    'blood pressure', 'bp', 'high blood pressure', 'systolic', 'diastolic',
                    'pressure reading', 'pressure meds', 'pressure medication',
                    'my blood pressure', 'pressure down', 'normalized bp', 'off bp meds'
                ],
                'exclusions': ['hypertension']  # → RO3
            },
            'RO2.4': {
                'name': 'Lipid Profile',
                'keywords': [
                    'cholesterol', 'triglycerides', 'triglyceride', 'trigs', 'hdl', 'ldl',
                    'my ldl', 'my hdl', 'lipid', 'lipids', 'lipid panel', 'total cholesterol',
                    'vldl', 'statin', 'statins', 'off statins', 'cholesterol level',
                    'high cholesterol', 'lowered cholesterol', 'apob', 'apo b'
                ],
                'exclusions': ['heart disease', 'heart attack', 'cardiovascular']  # → RO3
            },
            'RO2.5': {
                'name': 'Inflammatory Markers',
                'keywords': [
                    'crp', 'c-reactive', 'c reactive', 'homocysteine', 'hs-crp',
                    'sed rate', 'esr', 'inflammation marker', 'inflammatory marker',
                    'systemic inflammation'
                ],
                'exclusions': []
            },
            'RO2.6': {
                'name': 'Liver Function',
                'keywords': [
                    'liver enzyme', 'ast', 'alt', 'ggt', 'bilirubin', 'liver function',
                    'liver test', 'lft', 'liver number', 'liver panel', 'my liver',
                    'liver health'
                ],
                'exclusions': ['fatty liver', 'nafld', 'nash', 'cirrhosis']  # → RO3
            },
            'RO2.7': {
                'name': 'Kidney Function',
                'keywords': [
                    'gfr', 'egfr', 'creatinine', 'kidney function', 'renal function',
                    'bun', 'blood urea', 'kidney number', 'kidney test', 'my kidneys'
                ],
                'exclusions': ['kidney disease', 'ckd', 'renal failure', 'dialysis']  # → RO3
            },
            'RO2.8': {
                'name': 'Hormonal Markers',
                'keywords': [
                    'tsh', 't3', 't4', 'free t3', 'free t4', 'testosterone',
                    'estrogen', 'progesterone', 'dhea', 'cortisol', 'hormone level',
                    'hormone panel', 'thyroid panel', 'hormones balanced'
                ],
                'exclusions': ['hashimoto', 'hypothyroid', 'hyperthyroid', 'graves', 'thyroid disease']  # → RO3
            }
        }
    },

    # =========================================================================
    # RO3: DISEASE SPECIFICITY
    # "To determine the extent of reported improvements in specific medical conditions"
    # =========================================================================
    'RO3': {
        'name': 'Disease Specificity',
        'description': 'User-reported improvements or remission of specific, diagnosed metabolic-related diseases',
        'aspects': {
            'RO3.1': {
                'name': 'Type 2 Diabetes',
                'keywords': [
                    'diabetes', 'diabetic', 'type 2', 'type 2 diabetes', 't2d', 't2dm',
                    'prediabetes', 'prediabetic', 'pre-diabetic', 'pre diabetic',
                    'reversed diabetes', 'metformin', 'my diabetes', 'am diabetic',
                    'type two diabetes'
                ],
                'exclusions': []
            },
            'RO3.2': {
                'name': 'Fatty Liver Disease',
                'keywords': [
                    'fatty liver', 'nafld', 'nash', 'non-alcoholic fatty liver',
                    'hepatic steatosis', 'liver fibrosis', 'cirrhosis', 'my fatty liver',
                    'liver disease'
                ],
                'exclusions': []
            },
            'RO3.3': {
                'name': 'Cardiovascular Disease',
                'keywords': [
                    'heart disease', 'heart attack', 'cardiovascular', 'cvd',
                    'coronary artery', 'coronary heart', 'cad', 'heart failure',
                    'congestive heart', 'chf', 'stent', 'bypass', 'myocardial',
                    'atherosclerosis', 'plaque', 'angina', 'cardiac'
                ],
                'exclusions': []
            },
            'RO3.4': {
                'name': 'Hypertension',
                'keywords': [
                    'hypertension', 'hypertensive', 'high blood pressure disease'
                ],
                'exclusions': []
            },
            'RO3.5': {
                'name': 'PCOS',
                'keywords': [
                    'pcos', 'polycystic ovary', 'polycystic ovarian', 'polycystic ovary syndrome',
                    'ovarian cyst', 'cysts on ovaries'
                ],
                'exclusions': []
            },
            'RO3.6': {
                'name': 'Neurodegenerative Disease',
                'keywords': [
                    'alzheimer', "alzheimer's", 'alzheimers', 'dementia', 'cognitive decline',
                    'parkinson', "parkinson's", 'parkinsons', 'neurodegenerat'
                ],
                'exclusions': []
            },
            'RO3.7': {
                'name': 'Chronic Kidney Disease',
                'keywords': [
                    'kidney disease', 'ckd', 'chronic kidney', 'renal failure',
                    'end stage renal', 'esrd', 'dialysis', 'nephropathy', 'stage 3 kidney',
                    'stage 4 kidney', 'stage 5 kidney'
                ],
                'exclusions': []
            },
            'RO3.8': {
                'name': 'Gout',
                'keywords': [
                    'gout', 'gouty', 'uric acid', 'uric', 'gouty arthritis',
                    'high uric acid'
                ],
                'exclusions': []
            },
            'RO3.9': {
                'name': 'Cancer',
                'keywords': [
                    'cancer', 'tumor', 'tumour', 'malignant', 'carcinoma', 'sarcoma',
                    'lymphoma', 'leukemia', 'metastasis', 'chemo', 'chemotherapy',
                    'oncology', 'breast cancer', 'colon cancer', 'prostate cancer',
                    'lung cancer', 'cancer cells'
                ],
                'exclusions': []
            },
            'RO3.10': {
                'name': 'Osteoporosis',
                'keywords': [
                    'osteoporosis', 'osteopenia', 'bone density', 'bone mass',
                    'dexa scan', 'bone scan', 'bone loss', 'fracture risk'
                ],
                'exclusions': []
            },
            'RO3.11': {
                'name': 'Stroke',
                'keywords': [
                    'stroke', 'had a stroke', 'mini stroke', 'tia', 'transient ischemic',
                    'cerebrovascular', 'cva', 'ischemic stroke', 'hemorrhagic stroke'
                ],
                'exclusions': []
            },
            'RO3.12': {
                'name': 'ADHD',
                'keywords': [
                    'adhd', 'add', 'attention deficit', 'attention-deficit',
                    'hyperactivity disorder', 'adderall', 'ritalin', 'vyvanse'
                ],
                'exclusions': []
            },
            'RO3.13': {
                'name': 'Thyroid Disease',
                'keywords': [
                    'thyroid', 'hashimoto', "hashimoto's", 'hashimotos', 'hypothyroid',
                    'hypothyroidism', 'hyperthyroid', 'hyperthyroidism', 'graves disease',
                    'goiter', 'levothyroxine', 'synthroid', 'thyroid disease'
                ],
                'exclusions': []
            },
            'RO3.14': {
                'name': 'Inflammatory Bowel Disease',
                'keywords': [
                    'ibs', 'irritable bowel', 'irritable bowel syndrome', 'colitis',
                    'ulcerative colitis', 'crohn', "crohn's", 'crohns', 'ibd',
                    'inflammatory bowel disease', 'sibo', 'leaky gut syndrome'
                ],
                'exclusions': []
            },
            'RO3.15': {
                'name': 'Autoimmune Disease',
                'keywords': [
                    'autoimmune', 'auto immune', 'auto-immune', 'lupus', 'multiple sclerosis',
                    'ms', 'rheumatoid arthritis', 'rheumatoid', 'celiac', 'celiac disease',
                    'ra', 'sjogren', 'psoriatic arthritis'
                ],
                'exclusions': []
            },
            'RO3.16': {
                'name': 'Fibromyalgia & Neuropathy',
                'keywords': [
                    'fibromyalgia', 'fibro', 'neuropathy', 'nerve pain', 'diabetic neuropathy',
                    'peripheral neuropathy', 'nerve damage', 'numbness', 'tingling'
                ],
                'exclusions': []
            },
            'RO3.17': {
                'name': 'Arthritis',
                'keywords': [
                    'arthritis', 'osteoarthritis', 'arthritic', 'joint disease',
                    'degenerative joint'
                ],
                'exclusions': []
            },
            'RO3.18': {
                'name': 'Gallbladder Disease',
                'keywords': [
                    'gallbladder', 'gall bladder', 'gallstones', 'gallstone',
                    'cholecystectomy', 'gallbladder removal', 'gallbladder attack'
                ],
                'exclusions': []
            }
        }
    }
}

# Count aspects
total_aspects = sum(len(ro['aspects']) for ro in ONTOLOGY.values())
print(f"\n✅ Ontology defined with {len(ONTOLOGY)} Research Objectives and {total_aspects} aspects:")
for ro_id, ro in ONTOLOGY.items():
    print(f"   {ro_id} ({ro['name']}): {len(ro['aspects'])} aspects")


# ==============================================================================
# CELL 4: Load Corpus
# ==============================================================================

print("\n" + "=" * 70)
print("2. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
    ]
    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:50]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)


# ==============================================================================
# CELL 5: Keyword Matching Function
# ==============================================================================

print("\n" + "=" * 70)
print("3. TESTING ONTOLOGY COVERAGE")
print("=" * 70)

def check_aspect_match(text, aspect_data):
    """
    Check if a comment matches an aspect based on keywords.
    Returns True if any keyword matches AND no exclusion matches.
    """
    if pd.isna(text) or not isinstance(text, str):
        return False

    text_lower = text.lower()

    # Check exclusions first
    for excl in aspect_data.get('exclusions', []):
        if excl in text_lower:
            return False

    # Check keywords
    for keyword in aspect_data['keywords']:
        if keyword in text_lower:
            return True

    return False

def get_matched_keywords(text, aspect_data):
    """Return list of keywords that matched."""
    if pd.isna(text) or not isinstance(text, str):
        return []

    text_lower = text.lower()
    matched = []

    for keyword in aspect_data['keywords']:
        if keyword in text_lower:
            matched.append(keyword)

    return matched

# Test coverage for each aspect
print("🔄 Testing keyword coverage across corpus...")

coverage_results = []

for ro_id, ro in ONTOLOGY.items():
    for aspect_id, aspect in ro['aspects'].items():
        # Count matches
        matches = df['comment_text'].apply(lambda x: check_aspect_match(x, aspect))
        match_count = matches.sum()
        match_pct = match_count / len(df) * 100

        # Get sample matched comments
        matched_df = df[matches].head(5)

        coverage_results.append({
            'ro_id': ro_id,
            'ro_name': ro['name'],
            'aspect_id': aspect_id,
            'aspect_name': aspect['name'],
            'match_count': match_count,
            'match_percentage': match_pct,
            'num_keywords': len(aspect['keywords'])
        })

        print(f"  {aspect_id} {aspect['name']}: {match_count:,} matches ({match_pct:.2f}%)")

coverage_df = pd.DataFrame(coverage_results)


# ==============================================================================
# CELL 6: Coverage Summary by Research Objective
# ==============================================================================

print("\n" + "=" * 70)
print("4. COVERAGE SUMMARY BY RESEARCH OBJECTIVE")
print("=" * 70)

for ro_id in ['RO1', 'RO2', 'RO3']:
    ro_data = coverage_df[coverage_df['ro_id'] == ro_id]
    total_matches = ro_data['match_count'].sum()
    # Note: Comments may match multiple aspects, so this is not unique count
    print(f"\n{ro_id} - {ONTOLOGY[ro_id]['name']}:")
    print(f"  Total aspect matches: {total_matches:,}")
    print(f"  Top aspects:")
    for _, row in ro_data.nlargest(5, 'match_count').iterrows():
        print(f"    • {row['aspect_id']} {row['aspect_name']}: {row['match_count']:,} ({row['match_percentage']:.2f}%)")


# ==============================================================================
# CELL 7: Calculate Unique Comment Coverage
# ==============================================================================

print("\n" + "=" * 70)
print("5. UNIQUE COMMENT COVERAGE")
print("=" * 70)

# Check which comments match ANY aspect in each RO
def check_ro_match(text, ro_id):
    """Check if comment matches any aspect in the RO."""
    if pd.isna(text) or not isinstance(text, str):
        return False

    for aspect_id, aspect in ONTOLOGY[ro_id]['aspects'].items():
        if check_aspect_match(text, aspect):
            return True
    return False

print("🔄 Calculating unique comment coverage...")

df['matches_RO1'] = df['comment_text'].apply(lambda x: check_ro_match(x, 'RO1'))
df['matches_RO2'] = df['comment_text'].apply(lambda x: check_ro_match(x, 'RO2'))
df['matches_RO3'] = df['comment_text'].apply(lambda x: check_ro_match(x, 'RO3'))
df['matches_any'] = df['matches_RO1'] | df['matches_RO2'] | df['matches_RO3']

ro1_unique = df['matches_RO1'].sum()
ro2_unique = df['matches_RO2'].sum()
ro3_unique = df['matches_RO3'].sum()
any_match = df['matches_any'].sum()

print(f"\nUnique comments matching each RO:")
print(f"  RO1 (Subjective Well-Being): {ro1_unique:,} ({ro1_unique/len(df)*100:.1f}%)")
print(f"  RO2 (Tool-Mediated Validation): {ro2_unique:,} ({ro2_unique/len(df)*100:.1f}%)")
print(f"  RO3 (Disease Specificity): {ro3_unique:,} ({ro3_unique/len(df)*100:.1f}%)")
print(f"\n  ANY Research Objective: {any_match:,} ({any_match/len(df)*100:.1f}%)")
print(f"  No match (general discussion): {len(df) - any_match:,} ({(len(df)-any_match)/len(df)*100:.1f}%)")


# ==============================================================================
# CELL 8: Extract Sample Matched Comments
# ==============================================================================

print("\n" + "=" * 70)
print("6. SAMPLE MATCHED COMMENTS")
print("=" * 70)

sample_matches = []

for ro_id, ro in ONTOLOGY.items():
    for aspect_id, aspect in ro['aspects'].items():
        matches = df[df['comment_text'].apply(lambda x: check_aspect_match(x, aspect))]

        if len(matches) > 0:
            # Get 3 diverse samples
            samples = matches.sample(n=min(3, len(matches)), random_state=42)

            for _, row in samples.iterrows():
                matched_kw = get_matched_keywords(row['comment_text'], aspect)
                sample_matches.append({
                    'ro_id': ro_id,
                    'aspect_id': aspect_id,
                    'aspect_name': aspect['name'],
                    'channel': row.get('channel_name', 'Unknown'),
                    'matched_keywords': ', '.join(matched_kw[:5]),
                    'comment': str(row['comment_text'])[:500]
                })

# Show samples for key aspects
print("\nSample matches for selected aspects:\n")

key_aspects = ['RO1.1', 'RO1.2', 'RO1.6', 'RO2.1', 'RO2.2', 'RO3.1', 'RO3.2', 'RO3.14']
for aspect_id in key_aspects:
    aspect_samples = [s for s in sample_matches if s['aspect_id'] == aspect_id]
    if aspect_samples:
        s = aspect_samples[0]
        print(f"📌 {s['aspect_id']} - {s['aspect_name']}")
        print(f"   Keywords: {s['matched_keywords']}")
        print(f"   Comment: {s['comment'][:200]}...")
        print()


# ==============================================================================
# CELL 9: Identify Low Coverage Aspects
# ==============================================================================

print("\n" + "=" * 70)
print("7. LOW COVERAGE ASPECTS (Need Keyword Expansion)")
print("=" * 70)

low_coverage = coverage_df[coverage_df['match_count'] < 500].sort_values('match_count')

print("\nAspects with fewer than 500 matches:")
for _, row in low_coverage.iterrows():
    print(f"  ⚠️ {row['aspect_id']} {row['aspect_name']}: {row['match_count']:,} matches")


# ==============================================================================
# CELL 10: Export Results
# ==============================================================================

print("\n" + "=" * 70)
print("8. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Coverage statistics
coverage_df.to_csv(f'{OUTPUT_DIR}Phase2_Script4_coverage_stats.csv', index=False)
print(f"✅ Exported: Phase2_Script4_coverage_stats.csv")

# Export 2: Sample matched comments
sample_df = pd.DataFrame(sample_matches)
sample_df.to_csv(f'{OUTPUT_DIR}Phase2_Script4_sample_matches.csv', index=False)
print(f"✅ Exported: Phase2_Script4_sample_matches.csv")

# Export 3: Ontology structure (for documentation)
ontology_export = []
for ro_id, ro in ONTOLOGY.items():
    for aspect_id, aspect in ro['aspects'].items():
        ontology_export.append({
            'ro_id': ro_id,
            'ro_name': ro['name'],
            'aspect_id': aspect_id,
            'aspect_name': aspect['name'],
            'keywords': '; '.join(aspect['keywords']),
            'exclusions': '; '.join(aspect.get('exclusions', [])),
            'num_keywords': len(aspect['keywords'])
        })
ontology_df = pd.DataFrame(ontology_export)
ontology_df.to_csv(f'{OUTPUT_DIR}Phase2_Script4_ontology_structure.csv', index=False)
print(f"✅ Exported: Phase2_Script4_ontology_structure.csv")


# ==============================================================================
# CELL 11: Visualisation
# ==============================================================================

print("\n" + "=" * 70)
print("9. GENERATING VISUALISATION")
print("=" * 70)

fig, axes = plt.subplots(1, 3, figsize=(16, 8))

for idx, ro_id in enumerate(['RO1', 'RO2', 'RO3']):
    ax = axes[idx]
    ro_data = coverage_df[coverage_df['ro_id'] == ro_id].sort_values('match_count', ascending=True)

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(ro_data)))
    bars = ax.barh(ro_data['aspect_name'], ro_data['match_count'], color=colors)

    ax.set_xlabel('Number of Matches', fontsize=10)
    ax.set_title(f"{ro_id}: {ONTOLOGY[ro_id]['name']}", fontsize=12, fontweight='bold')

    # Add value labels
    for bar, count in zip(bars, ro_data['match_count']):
        ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
                f'{count:,}', va='center', fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}Phase2_Script4_coverage_by_aspect.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"✅ Saved: Phase2_Script4_coverage_by_aspect.png")


# ==============================================================================
# CELL 12: Summary Report
# ==============================================================================

print("\n" + "=" * 70)
print("10. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 4 - ONTOLOGY COVERAGE RESULTS
============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. ONTOLOGY STRUCTURE
---------------------
Total Research Objectives: 3
Total Aspects: {total_aspects}
  - RO1 (Subjective Well-Being): {len(ONTOLOGY['RO1']['aspects'])} aspects
  - RO2 (Tool-Mediated Validation): {len(ONTOLOGY['RO2']['aspects'])} aspects
  - RO3 (Disease Specificity): {len(ONTOLOGY['RO3']['aspects'])} aspects

2. CORPUS COVERAGE
------------------
Total comments: {len(df):,}
Comments matching RO1: {ro1_unique:,} ({ro1_unique/len(df)*100:.1f}%)
Comments matching RO2: {ro2_unique:,} ({ro2_unique/len(df)*100:.1f}%)
Comments matching RO3: {ro3_unique:,} ({ro3_unique/len(df)*100:.1f}%)
Comments matching ANY RO: {any_match:,} ({any_match/len(df)*100:.1f}%)
General discussion (no match): {len(df) - any_match:,} ({(len(df)-any_match)/len(df)*100:.1f}%)

3. ASPECT-LEVEL COVERAGE (sorted by match count)
------------------------------------------------""")

for ro_id in ['RO1', 'RO2', 'RO3']:
    print(f"\n{ro_id} - {ONTOLOGY[ro_id]['name']}:")
    ro_data = coverage_df[coverage_df['ro_id'] == ro_id].sort_values('match_count', ascending=False)
    for _, row in ro_data.iterrows():
        print(f"  {row['aspect_id']:8} {row['aspect_name']:30} {row['match_count']:>8,} ({row['match_percentage']:.2f}%)")

print(f"""

4. LOW COVERAGE ASPECTS (< 500 matches)
---------------------------------------""")
for _, row in low_coverage.iterrows():
    print(f"  ⚠️ {row['aspect_id']} {row['aspect_name']}: {row['match_count']:,}")

print(f"""

5. FILES EXPORTED
-----------------
- Phase2_Script4_coverage_stats.csv
- Phase2_Script4_sample_matches.csv
- Phase2_Script4_ontology_structure.csv
- Phase2_Script4_coverage_by_aspect.png

6. RECOMMENDATIONS
------------------
1. Review sample matches to validate keyword accuracy
2. Consider expanding keywords for low-coverage aspects
3. Check for false positives in high-coverage aspects
4. Verify exclusion rules are working correctly

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 4 Complete")
print("=" * 70)
