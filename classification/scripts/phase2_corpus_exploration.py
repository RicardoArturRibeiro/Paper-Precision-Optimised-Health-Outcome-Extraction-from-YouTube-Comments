# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 1 - Corpus Exploration & Text Preparation
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script performs the foundational corpus exploration for Phase 2
# (Ontology Development). It loads the corpus, validates its structure,
# cleans the text data, and extracts initial vocabulary statistics to
# inform the ontology development process.
#
# Outputs:
# 1. Console output with corpus statistics (copy/paste to Claude)
# 2. CSV file with health-related word frequencies
# 3. CSV file with sample comments for manual review
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 1 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk wordcloud -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from datetime import datetime
import warnings

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Google Colab specific
from google.colab import drive

# Configure settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 1 - Corpus Exploration & Text Preparation")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & Configuration
# ==============================================================================

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus with Robust Error Handling
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    """Load the corpus with multiple fallback strategies."""
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
        {'name': 'Python engine latin-1', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'latin-1'}}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:60]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)

if df is None:
    raise FileNotFoundError("Could not load corpus. Check file path.")


# ==============================================================================
# CELL 4: Schema Validation
# ==============================================================================

print("\n" + "=" * 70)
print("2. SCHEMA VALIDATION")
print("=" * 70)

print(f"\n--- 2.1 Dataset Shape ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print(f"\n--- 2.2 Column Names ---")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\n--- 2.3 Data Types ---")
print(df.dtypes)

# Check for comment_text column (essential for ontology development)
if 'comment_text' not in df.columns:
    print("\n❌ ERROR: 'comment_text' column not found!")
    print("Available columns:", list(df.columns))
else:
    print(f"\n✅ 'comment_text' column found")
    print(f"   Non-null comments: {df['comment_text'].notna().sum():,}")
    print(f"   Null comments: {df['comment_text'].isna().sum():,}")


# ==============================================================================
# CELL 5: Text Cleaning & Preprocessing
# ==============================================================================

print("\n" + "=" * 70)
print("3. TEXT CLEANING & PREPROCESSING")
print("=" * 70)

def clean_text(text):
    """
    Clean and normalise comment text for analysis.
    Preserves health-related context while removing noise.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove timestamps (e.g., 2:30, 12:45:30)
    text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', text)

    # Keep important health-related patterns before removing numbers
    # Preserve patterns like "a1c", "t2d", "b12", etc.
    text = re.sub(r'\b(\d+)\s*(lbs?|pounds?|kg|kilos?)\b', r'\1_weight_unit', text)
    text = re.sub(r'\b(\d+)/(\d+)\b', r'blood_pressure_reading', text)  # BP readings

    # Remove standalone numbers (but keep alphanumeric like "a1c")
    text = re.sub(r'\b\d+\b', '', text)

    # Remove special characters but keep apostrophes and hyphens in words
    text = re.sub(r"[^\w\s'-]", ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Apply cleaning
print("🔄 Cleaning comment text...")
df['clean_text'] = df['comment_text'].apply(clean_text)

# Calculate statistics
df['word_count'] = df['clean_text'].str.split().str.len().fillna(0).astype(int)
df['char_count'] = df['clean_text'].str.len().fillna(0).astype(int)

print(f"✅ Text cleaning complete")

print(f"\n--- 3.1 Cleaned Text Statistics ---")
print(f"Total comments: {len(df):,}")
print(f"Empty after cleaning: {(df['clean_text'] == '').sum():,}")
print(f"Mean word count: {df['word_count'].mean():.1f}")
print(f"Median word count: {df['word_count'].median():.1f}")
print(f"Max word count: {df['word_count'].max():,}")

# Show sample cleaned comments
print(f"\n--- 3.2 Sample Cleaned Comments ---")
sample_df = df[df['word_count'] > 10].sample(n=5, random_state=42)
for idx, row in sample_df.iterrows():
    print(f"\nOriginal ({len(str(row['comment_text']))} chars):")
    print(f"  {str(row['comment_text'])[:150]}...")
    print(f"Cleaned ({row['word_count']} words):")
    print(f"  {row['clean_text'][:150]}...")


# ==============================================================================
# CELL 6: Vocabulary Analysis for Ontology Development
# ==============================================================================

print("\n" + "=" * 70)
print("4. VOCABULARY ANALYSIS")
print("=" * 70)

# Combine all cleaned text
all_text = ' '.join(df['clean_text'].dropna())

# Tokenize
print("🔄 Tokenizing corpus...")
all_words = all_text.split()
print(f"Total tokens: {len(all_words):,}")

# Define stopwords (expanded for YouTube comments)
stop_words = set(stopwords.words('english'))
youtube_stopwords = {
    # Common YouTube comment words
    'video', 'videos', 'channel', 'subscribe', 'subscribed', 'like', 'liked',
    'watch', 'watching', 'watched', 'thanks', 'thank', 'great', 'good', 'best',
    'love', 'loved', 'amazing', 'awesome', 'wonderful', 'excellent', 'fantastic',
    'really', 'much', 'very', 'just', 'also', 'would', 'could', 'should',
    'get', 'got', 'getting', 'make', 'made', 'making', 'take', 'took', 'taking',
    'one', 'two', 'first', 'know', 'think', 'see', 'look', 'come', 'go', 'going',
    'want', 'need', 'say', 'said', 'tell', 'told', 'try', 'tried', 'trying',
    'even', 'still', 'always', 'never', 'ever', 'every', 'many', 'much',
    'well', 'back', 'now', 'way', 'thing', 'things', 'something', 'anything',
    'lot', 'lots', 'bit', 'little', 'big', 'long', 'new', 'old', 'right',
    'dont', "don't", 'doesnt', "doesn't", 'didnt', "didn't", 'cant', "can't",
    'wont', "won't", 'ive', "i've", 'im', "i'm", 'youre', "you're", 'thats', "that's",
    'its', "it's", 'hes', "he's", 'shes', "she's", 'theyre', "they're",
    'people', 'person', 'everyone', 'someone', 'anyone', 'nobody',
    'time', 'times', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
    'ago', 'today', 'yesterday', 'tomorrow', 'since', 'last', 'next',
    'please', 'help', 'question', 'answer', 'comment', 'comments', 'post',
    'dr', 'doc', 'doctor', 'doctors'  # Keep medical terms but remove generic 'dr' references
}
stop_words.update(youtube_stopwords)

# Filter words
filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
print(f"Filtered tokens (no stopwords, len>2): {len(filtered_words):,}")

# Word frequency
word_freq = Counter(filtered_words)

print(f"\n--- 4.1 Top 100 Most Frequent Words ---")
print("(These inform initial ontology keyword selection)\n")
top_100 = word_freq.most_common(100)
for i, (word, count) in enumerate(top_100, 1):
    print(f"{i:3}. {word:20} {count:,}")


# ==============================================================================
# CELL 7: Health-Related Vocabulary Extraction
# ==============================================================================

print("\n" + "=" * 70)
print("5. HEALTH-RELATED VOCABULARY EXTRACTION")
print("=" * 70)

# Define seed health-related terms to find related vocabulary
health_seed_terms = {
    # RO1: Subjective Well-Being seeds
    'energy', 'tired', 'fatigue', 'sleep', 'mood', 'anxiety', 'depression',
    'brain', 'fog', 'focus', 'mental', 'pain', 'joint', 'inflammation',
    'gut', 'bloating', 'digestion', 'skin', 'acne', 'craving', 'hunger',
    'appetite', 'headache', 'migraine',

    # RO2: Tool-Mediated Validation seeds
    'weight', 'lost', 'pounds', 'lbs', 'glucose', 'sugar', 'a1c', 'insulin',
    'pressure', 'cholesterol', 'triglycerides', 'hdl', 'ldl', 'liver',
    'kidney', 'blood', 'test', 'numbers', 'levels',

    # RO3: Disease Specificity seeds
    'diabetes', 'diabetic', 't2d', 'prediabetes', 'pcos', 'thyroid',
    'hashimoto', 'autoimmune', 'arthritis', 'fibromyalgia', 'cancer',
    'heart', 'disease', 'hypertension', 'fatty', 'nafld', 'gout',
    'alzheimer', 'dementia', 'ibs', 'crohn', 'colitis'
}

# Find health-related words in corpus
print("🔄 Extracting health-related vocabulary...")

health_words_found = {}
for word, count in word_freq.items():
    # Direct match with seed terms
    if word in health_seed_terms:
        health_words_found[word] = count
    # Partial match (word contains seed term)
    elif any(seed in word for seed in health_seed_terms if len(seed) > 3):
        health_words_found[word] = count

# Sort by frequency
health_words_sorted = sorted(health_words_found.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- 5.1 Health-Related Words Found ({len(health_words_sorted)} terms) ---\n")
for i, (word, count) in enumerate(health_words_sorted[:80], 1):
    print(f"{i:3}. {word:25} {count:,}")


# ==============================================================================
# CELL 8: Research Objective Category Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("6. RESEARCH OBJECTIVE CATEGORY ANALYSIS")
print("=" * 70)

# Define preliminary keyword groups for each RO
ro_keywords = {
    'RO1_Subjective_WellBeing': [
        'energy', 'tired', 'fatigue', 'exhausted', 'sleep', 'insomnia', 'slept',
        'mood', 'anxiety', 'anxious', 'depression', 'depressed', 'happy', 'happier',
        'brain', 'fog', 'focus', 'mental', 'clarity', 'memory', 'cognitive',
        'pain', 'joint', 'ache', 'inflammation', 'swelling', 'stiff',
        'gut', 'bloating', 'bloated', 'digestion', 'stomach', 'bowel',
        'skin', 'acne', 'eczema', 'psoriasis', 'rash', 'complexion',
        'craving', 'cravings', 'hunger', 'hungry', 'appetite', 'satiety',
        'headache', 'migraine', 'calm', 'stress', 'stressed'
    ],
    'RO2_ToolMediated_Validation': [
        'weight', 'lost', 'pounds', 'lbs', 'kg', 'kilos', 'scale', 'waist',
        'glucose', 'sugar', 'a1c', 'hba1c', 'insulin', 'fasting', 'cgm',
        'pressure', 'bp', 'systolic', 'diastolic', 'hypertension',
        'cholesterol', 'triglycerides', 'hdl', 'ldl', 'lipid', 'statin',
        'liver', 'ast', 'alt', 'enzyme', 'bilirubin',
        'kidney', 'creatinine', 'gfr', 'egfr',
        'blood', 'test', 'numbers', 'levels', 'results', 'lab',
        'tsh', 't3', 't4', 'testosterone', 'hormone'
    ],
    'RO3_Disease_Specificity': [
        'diabetes', 'diabetic', 't2d', 'type2', 'prediabetes', 'prediabetic',
        'pcos', 'polycystic', 'ovary', 'ovarian',
        'thyroid', 'hashimoto', 'hashimotos', 'hypothyroid', 'hyperthyroid', 'graves',
        'autoimmune', 'lupus', 'arthritis', 'rheumatoid', 'celiac',
        'fibromyalgia', 'neuropathy', 'nerve',
        'cancer', 'tumor', 'chemo', 'chemotherapy',
        'heart', 'cardiovascular', 'coronary', 'attack', 'failure',
        'fatty', 'nafld', 'nash', 'cirrhosis',
        'gout', 'uric',
        'alzheimer', 'alzheimers', 'dementia',
        'ibs', 'crohn', 'crohns', 'colitis', 'ibd',
        'stroke', 'adhd', 'add', 'osteoporosis'
    ]
}

# Count matches for each RO category
print("\n--- 6.1 Preliminary Keyword Coverage by Research Objective ---\n")

ro_results = {}
for ro_name, keywords in ro_keywords.items():
    matches = 0
    matched_words = []
    for word in keywords:
        if word in word_freq:
            matches += word_freq[word]
            matched_words.append((word, word_freq[word]))

    # Sort matched words by frequency
    matched_words.sort(key=lambda x: x[1], reverse=True)
    ro_results[ro_name] = {
        'total_matches': matches,
        'unique_keywords_found': len(matched_words),
        'top_keywords': matched_words[:15]
    }

    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {matches:,}")
    print(f"  Unique keywords found: {len(matched_words)}/{len(keywords)}")
    print(f"  Top 15 keywords:")
    for word, count in matched_words[:15]:
        print(f"    - {word}: {count:,}")


# ==============================================================================
# CELL 9: Export Results for Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("7. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Top 500 words with frequencies
top_500_df = pd.DataFrame(word_freq.most_common(500), columns=['word', 'frequency'])
top_500_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_top500_words.csv', index=False)
print(f"✅ Exported: Phase2_Script1_top500_words.csv")

# Export 2: Health-related vocabulary
health_vocab_df = pd.DataFrame(health_words_sorted, columns=['word', 'frequency'])
health_vocab_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_health_vocabulary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_health_vocabulary.csv")

# Export 3: Sample comments for manual review (stratified by length)
print("\n🔄 Extracting sample comments for manual review...")

# Get samples from different length categories
samples = []

# Short comments (5-15 words) - often simple testimonials
short = df[(df['word_count'] >= 5) & (df['word_count'] <= 15)].sample(n=min(100, len(df)), random_state=42)
short['length_category'] = 'short'
samples.append(short)

# Medium comments (16-50 words) - more detailed experiences
medium = df[(df['word_count'] >= 16) & (df['word_count'] <= 50)].sample(n=min(100, len(df)), random_state=42)
medium['length_category'] = 'medium'
samples.append(medium)

# Long comments (51+ words) - detailed testimonials
long = df[df['word_count'] >= 51].sample(n=min(100, len(df)), random_state=42)
long['length_category'] = 'long'
samples.append(long)

sample_comments = pd.concat(samples, ignore_index=True)
sample_comments_export = sample_comments[['channel_name', 'length_category', 'word_count', 'comment_text', 'clean_text']].copy()
sample_comments_export.to_csv(f'{OUTPUT_DIR}Phase2_Script1_sample_comments.csv', index=False)
print(f"✅ Exported: Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)")

# Export 4: RO Category Summary
ro_summary = []
for ro_name, data in ro_results.items():
    ro_summary.append({
        'research_objective': ro_name,
        'total_matches': data['total_matches'],
        'unique_keywords_found': data['unique_keywords_found'],
        'top_keywords': ', '.join([f"{w}({c})" for w, c in data['top_keywords'][:10]])
    })
ro_summary_df = pd.DataFrame(ro_summary)
ro_summary_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_RO_summary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_RO_summary.csv")


# ==============================================================================
# CELL 10: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("8. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 1 - CORPUS EXPLORATION RESULTS
=============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. CORPUS STATISTICS
--------------------
Total comments: {len(df):,}
Non-empty after cleaning: {(df['clean_text'] != '').sum():,}
Total tokens (all words): {len(all_words):,}
Filtered tokens (no stopwords): {len(filtered_words):,}
Unique vocabulary size: {len(word_freq):,}

2. COMMENT LENGTH DISTRIBUTION
------------------------------
Mean word count: {df['word_count'].mean():.1f}
Median word count: {df['word_count'].median():.1f}
Std deviation: {df['word_count'].std():.1f}
Min: {df['word_count'].min()}
Max: {df['word_count'].max()}
25th percentile: {df['word_count'].quantile(0.25):.0f}
75th percentile: {df['word_count'].quantile(0.75):.0f}

3. TOP 50 WORDS (excluding stopwords)
-------------------------------------""")

for i, (word, count) in enumerate(word_freq.most_common(50), 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
4. RESEARCH OBJECTIVE PRELIMINARY COVERAGE
------------------------------------------""")

for ro_name, data in ro_results.items():
    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {data['total_matches']:,}")
    print(f"  Top 10 keywords: {', '.join([f'{w}({c:,})' for w, c in data['top_keywords'][:10]])}")

print(f"""
5. HEALTH-RELATED VOCABULARY (Top 40)
-------------------------------------""")
for i, (word, count) in enumerate(health_words_sorted[:40], 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
6. FILES EXPORTED
-----------------
- Phase2_Script1_top500_words.csv
- Phase2_Script1_health_vocabulary.csv
- Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)
- Phase2_Script1_RO_summary.csv

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 1 Complete")
print("=" * 70)

# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 1 - Corpus Exploration & Text Preparation
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script performs the foundational corpus exploration for Phase 2
# (Ontology Development). It loads the corpus, validates its structure,
# cleans the text data, and extracts initial vocabulary statistics to
# inform the ontology development process.
#
# Outputs:
# 1. Console output with corpus statistics (copy/paste to Claude)
# 2. CSV file with health-related word frequencies
# 3. CSV file with sample comments for manual review
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 1 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk wordcloud -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from datetime import datetime
import warnings

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Google Colab specific
from google.colab import drive

# Configure settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 1 - Corpus Exploration & Text Preparation")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & Configuration
# ==============================================================================

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus with Robust Error Handling
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    """Load the corpus with multiple fallback strategies."""
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
        {'name': 'Python engine latin-1', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'latin-1'}}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:60]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)

if df is None:
    raise FileNotFoundError("Could not load corpus. Check file path.")


# ==============================================================================
# CELL 4: Schema Validation
# ==============================================================================

print("\n" + "=" * 70)
print("2. SCHEMA VALIDATION")
print("=" * 70)

print(f"\n--- 2.1 Dataset Shape ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print(f"\n--- 2.2 Column Names ---")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\n--- 2.3 Data Types ---")
print(df.dtypes)

# Check for comment_text column (essential for ontology development)
if 'comment_text' not in df.columns:
    print("\n❌ ERROR: 'comment_text' column not found!")
    print("Available columns:", list(df.columns))
else:
    print(f"\n✅ 'comment_text' column found")
    print(f"   Non-null comments: {df['comment_text'].notna().sum():,}")
    print(f"   Null comments: {df['comment_text'].isna().sum():,}")


# ==============================================================================
# CELL 5: Text Cleaning & Preprocessing
# ==============================================================================

print("\n" + "=" * 70)
print("3. TEXT CLEANING & PREPROCESSING")
print("=" * 70)

def clean_text(text):
    """
    Clean and normalise comment text for analysis.
    Preserves health-related context while removing noise.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove timestamps (e.g., 2:30, 12:45:30)
    text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', text)

    # Keep important health-related patterns before removing numbers
    # Preserve patterns like "a1c", "t2d", "b12", etc.
    text = re.sub(r'\b(\d+)\s*(lbs?|pounds?|kg|kilos?)\b', r'\1_weight_unit', text)
    text = re.sub(r'\b(\d+)/(\d+)\b', r'blood_pressure_reading', text)  # BP readings

    # Remove standalone numbers (but keep alphanumeric like "a1c")
    text = re.sub(r'\b\d+\b', '', text)

    # Remove special characters but keep apostrophes and hyphens in words
    text = re.sub(r"[^\w\s'-]", ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Apply cleaning
print("🔄 Cleaning comment text...")
df['clean_text'] = df['comment_text'].apply(clean_text)

# Calculate statistics
df['word_count'] = df['clean_text'].str.split().str.len().fillna(0).astype(int)
df['char_count'] = df['clean_text'].str.len().fillna(0).astype(int)

print(f"✅ Text cleaning complete")

print(f"\n--- 3.1 Cleaned Text Statistics ---")
print(f"Total comments: {len(df):,}")
print(f"Empty after cleaning: {(df['clean_text'] == '').sum():,}")
print(f"Mean word count: {df['word_count'].mean():.1f}")
print(f"Median word count: {df['word_count'].median():.1f}")
print(f"Max word count: {df['word_count'].max():,}")

# Show sample cleaned comments
print(f"\n--- 3.2 Sample Cleaned Comments ---")
sample_df = df[df['word_count'] > 10].sample(n=5, random_state=42)
for idx, row in sample_df.iterrows():
    print(f"\nOriginal ({len(str(row['comment_text']))} chars):")
    print(f"  {str(row['comment_text'])[:150]}...")
    print(f"Cleaned ({row['word_count']} words):")
    print(f"  {row['clean_text'][:150]}...")


# ==============================================================================
# CELL 6: Vocabulary Analysis for Ontology Development
# ==============================================================================

print("\n" + "=" * 70)
print("4. VOCABULARY ANALYSIS")
print("=" * 70)

# Combine all cleaned text
all_text = ' '.join(df['clean_text'].dropna())

# Tokenize
print("🔄 Tokenizing corpus...")
all_words = all_text.split()
print(f"Total tokens: {len(all_words):,}")

# Define stopwords (expanded for YouTube comments)
stop_words = set(stopwords.words('english'))
youtube_stopwords = {
    # Common YouTube comment words
    'video', 'videos', 'channel', 'subscribe', 'subscribed', 'like', 'liked',
    'watch', 'watching', 'watched', 'thanks', 'thank', 'great', 'good', 'best',
    'love', 'loved', 'amazing', 'awesome', 'wonderful', 'excellent', 'fantastic',
    'really', 'much', 'very', 'just', 'also', 'would', 'could', 'should',
    'get', 'got', 'getting', 'make', 'made', 'making', 'take', 'took', 'taking',
    'one', 'two', 'first', 'know', 'think', 'see', 'look', 'come', 'go', 'going',
    'want', 'need', 'say', 'said', 'tell', 'told', 'try', 'tried', 'trying',
    'even', 'still', 'always', 'never', 'ever', 'every', 'many', 'much',
    'well', 'back', 'now', 'way', 'thing', 'things', 'something', 'anything',
    'lot', 'lots', 'bit', 'little', 'big', 'long', 'new', 'old', 'right',
    'dont', "don't", 'doesnt', "doesn't", 'didnt', "didn't", 'cant', "can't",
    'wont', "won't", 'ive', "i've", 'im', "i'm", 'youre', "you're", 'thats', "that's",
    'its', "it's", 'hes', "he's", 'shes', "she's", 'theyre', "they're",
    'people', 'person', 'everyone', 'someone', 'anyone', 'nobody',
    'time', 'times', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
    'ago', 'today', 'yesterday', 'tomorrow', 'since', 'last', 'next',
    'please', 'help', 'question', 'answer', 'comment', 'comments', 'post',
    'dr', 'doc', 'doctor', 'doctors'  # Keep medical terms but remove generic 'dr' references
}
stop_words.update(youtube_stopwords)

# Filter words
filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
print(f"Filtered tokens (no stopwords, len>2): {len(filtered_words):,}")

# Word frequency
word_freq = Counter(filtered_words)

print(f"\n--- 4.1 Top 100 Most Frequent Words ---")
print("(These inform initial ontology keyword selection)\n")
top_100 = word_freq.most_common(100)
for i, (word, count) in enumerate(top_100, 1):
    print(f"{i:3}. {word:20} {count:,}")


# ==============================================================================
# CELL 7: Health-Related Vocabulary Extraction
# ==============================================================================

print("\n" + "=" * 70)
print("5. HEALTH-RELATED VOCABULARY EXTRACTION")
print("=" * 70)

# Define seed health-related terms to find related vocabulary
health_seed_terms = {
    # RO1: Subjective Well-Being seeds
    'energy', 'tired', 'fatigue', 'sleep', 'mood', 'anxiety', 'depression',
    'brain', 'fog', 'focus', 'mental', 'pain', 'joint', 'inflammation',
    'gut', 'bloating', 'digestion', 'skin', 'acne', 'craving', 'hunger',
    'appetite', 'headache', 'migraine',

    # RO2: Tool-Mediated Validation seeds
    'weight', 'lost', 'pounds', 'lbs', 'glucose', 'sugar', 'a1c', 'insulin',
    'pressure', 'cholesterol', 'triglycerides', 'hdl', 'ldl', 'liver',
    'kidney', 'blood', 'test', 'numbers', 'levels',

    # RO3: Disease Specificity seeds
    'diabetes', 'diabetic', 't2d', 'prediabetes', 'pcos', 'thyroid',
    'hashimoto', 'autoimmune', 'arthritis', 'fibromyalgia', 'cancer',
    'heart', 'disease', 'hypertension', 'fatty', 'nafld', 'gout',
    'alzheimer', 'dementia', 'ibs', 'crohn', 'colitis'
}

# Find health-related words in corpus
print("🔄 Extracting health-related vocabulary...")

health_words_found = {}
for word, count in word_freq.items():
    # Direct match with seed terms
    if word in health_seed_terms:
        health_words_found[word] = count
    # Partial match (word contains seed term)
    elif any(seed in word for seed in health_seed_terms if len(seed) > 3):
        health_words_found[word] = count

# Sort by frequency
health_words_sorted = sorted(health_words_found.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- 5.1 Health-Related Words Found ({len(health_words_sorted)} terms) ---\n")
for i, (word, count) in enumerate(health_words_sorted[:80], 1):
    print(f"{i:3}. {word:25} {count:,}")


# ==============================================================================
# CELL 8: Research Objective Category Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("6. RESEARCH OBJECTIVE CATEGORY ANALYSIS")
print("=" * 70)

# Define preliminary keyword groups for each RO
ro_keywords = {
    'RO1_Subjective_WellBeing': [
        'energy', 'tired', 'fatigue', 'exhausted', 'sleep', 'insomnia', 'slept',
        'mood', 'anxiety', 'anxious', 'depression', 'depressed', 'happy', 'happier',
        'brain', 'fog', 'focus', 'mental', 'clarity', 'memory', 'cognitive',
        'pain', 'joint', 'ache', 'inflammation', 'swelling', 'stiff',
        'gut', 'bloating', 'bloated', 'digestion', 'stomach', 'bowel',
        'skin', 'acne', 'eczema', 'psoriasis', 'rash', 'complexion',
        'craving', 'cravings', 'hunger', 'hungry', 'appetite', 'satiety',
        'headache', 'migraine', 'calm', 'stress', 'stressed'
    ],
    'RO2_ToolMediated_Validation': [
        'weight', 'lost', 'pounds', 'lbs', 'kg', 'kilos', 'scale', 'waist',
        'glucose', 'sugar', 'a1c', 'hba1c', 'insulin', 'fasting', 'cgm',
        'pressure', 'bp', 'systolic', 'diastolic', 'hypertension',
        'cholesterol', 'triglycerides', 'hdl', 'ldl', 'lipid', 'statin',
        'liver', 'ast', 'alt', 'enzyme', 'bilirubin',
        'kidney', 'creatinine', 'gfr', 'egfr',
        'blood', 'test', 'numbers', 'levels', 'results', 'lab',
        'tsh', 't3', 't4', 'testosterone', 'hormone'
    ],
    'RO3_Disease_Specificity': [
        'diabetes', 'diabetic', 't2d', 'type2', 'prediabetes', 'prediabetic',
        'pcos', 'polycystic', 'ovary', 'ovarian',
        'thyroid', 'hashimoto', 'hashimotos', 'hypothyroid', 'hyperthyroid', 'graves',
        'autoimmune', 'lupus', 'arthritis', 'rheumatoid', 'celiac',
        'fibromyalgia', 'neuropathy', 'nerve',
        'cancer', 'tumor', 'chemo', 'chemotherapy',
        'heart', 'cardiovascular', 'coronary', 'attack', 'failure',
        'fatty', 'nafld', 'nash', 'cirrhosis',
        'gout', 'uric',
        'alzheimer', 'alzheimers', 'dementia',
        'ibs', 'crohn', 'crohns', 'colitis', 'ibd',
        'stroke', 'adhd', 'add', 'osteoporosis'
    ]
}

# Count matches for each RO category
print("\n--- 6.1 Preliminary Keyword Coverage by Research Objective ---\n")

ro_results = {}
for ro_name, keywords in ro_keywords.items():
    matches = 0
    matched_words = []
    for word in keywords:
        if word in word_freq:
            matches += word_freq[word]
            matched_words.append((word, word_freq[word]))

    # Sort matched words by frequency
    matched_words.sort(key=lambda x: x[1], reverse=True)
    ro_results[ro_name] = {
        'total_matches': matches,
        'unique_keywords_found': len(matched_words),
        'top_keywords': matched_words[:15]
    }

    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {matches:,}")
    print(f"  Unique keywords found: {len(matched_words)}/{len(keywords)}")
    print(f"  Top 15 keywords:")
    for word, count in matched_words[:15]:
        print(f"    - {word}: {count:,}")


# ==============================================================================
# CELL 9: Export Results for Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("7. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Top 500 words with frequencies
top_500_df = pd.DataFrame(word_freq.most_common(500), columns=['word', 'frequency'])
top_500_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_top500_words.csv', index=False)
print(f"✅ Exported: Phase2_Script1_top500_words.csv")

# Export 2: Health-related vocabulary
health_vocab_df = pd.DataFrame(health_words_sorted, columns=['word', 'frequency'])
health_vocab_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_health_vocabulary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_health_vocabulary.csv")

# Export 3: Sample comments for manual review (stratified by length)
print("\n🔄 Extracting sample comments for manual review...")

# Get samples from different length categories
samples = []

# Short comments (5-15 words) - often simple testimonials
short = df[(df['word_count'] >= 5) & (df['word_count'] <= 15)].sample(n=min(100, len(df)), random_state=42)
short['length_category'] = 'short'
samples.append(short)

# Medium comments (16-50 words) - more detailed experiences
medium = df[(df['word_count'] >= 16) & (df['word_count'] <= 50)].sample(n=min(100, len(df)), random_state=42)
medium['length_category'] = 'medium'
samples.append(medium)

# Long comments (51+ words) - detailed testimonials
long = df[df['word_count'] >= 51].sample(n=min(100, len(df)), random_state=42)
long['length_category'] = 'long'
samples.append(long)

sample_comments = pd.concat(samples, ignore_index=True)
sample_comments_export = sample_comments[['channel_name', 'length_category', 'word_count', 'comment_text', 'clean_text']].copy()
sample_comments_export.to_csv(f'{OUTPUT_DIR}Phase2_Script1_sample_comments.csv', index=False)
print(f"✅ Exported: Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)")

# Export 4: RO Category Summary
ro_summary = []
for ro_name, data in ro_results.items():
    ro_summary.append({
        'research_objective': ro_name,
        'total_matches': data['total_matches'],
        'unique_keywords_found': data['unique_keywords_found'],
        'top_keywords': ', '.join([f"{w}({c})" for w, c in data['top_keywords'][:10]])
    })
ro_summary_df = pd.DataFrame(ro_summary)
ro_summary_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_RO_summary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_RO_summary.csv")


# ==============================================================================
# CELL 10: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("8. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 1 - CORPUS EXPLORATION RESULTS
=============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. CORPUS STATISTICS
--------------------
Total comments: {len(df):,}
Non-empty after cleaning: {(df['clean_text'] != '').sum():,}
Total tokens (all words): {len(all_words):,}
Filtered tokens (no stopwords): {len(filtered_words):,}
Unique vocabulary size: {len(word_freq):,}

2. COMMENT LENGTH DISTRIBUTION
------------------------------
Mean word count: {df['word_count'].mean():.1f}
Median word count: {df['word_count'].median():.1f}
Std deviation: {df['word_count'].std():.1f}
Min: {df['word_count'].min()}
Max: {df['word_count'].max()}
25th percentile: {df['word_count'].quantile(0.25):.0f}
75th percentile: {df['word_count'].quantile(0.75):.0f}

3. TOP 50 WORDS (excluding stopwords)
-------------------------------------""")

for i, (word, count) in enumerate(word_freq.most_common(50), 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
4. RESEARCH OBJECTIVE PRELIMINARY COVERAGE
------------------------------------------""")

for ro_name, data in ro_results.items():
    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {data['total_matches']:,}")
    print(f"  Top 10 keywords: {', '.join([f'{w}({c:,})' for w, c in data['top_keywords'][:10]])}")

print(f"""
5. HEALTH-RELATED VOCABULARY (Top 40)
-------------------------------------""")
for i, (word, count) in enumerate(health_words_sorted[:40], 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
6. FILES EXPORTED
-----------------
- Phase2_Script1_top500_words.csv
- Phase2_Script1_health_vocabulary.csv
- Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)
- Phase2_Script1_RO_summary.csv

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 1 Complete")
print("=" * 70)

# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 1 - Corpus Exploration & Text Preparation
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script performs the foundational corpus exploration for Phase 2
# (Ontology Development). It loads the corpus, validates its structure,
# cleans the text data, and extracts initial vocabulary statistics to
# inform the ontology development process.
#
# Outputs:
# 1. Console output with corpus statistics (copy/paste to Claude)
# 2. CSV file with health-related word frequencies
# 3. CSV file with sample comments for manual review
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 1 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk wordcloud -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from datetime import datetime
import warnings

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Google Colab specific
from google.colab import drive

# Configure settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 1 - Corpus Exploration & Text Preparation")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & Configuration
# ==============================================================================

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus with Robust Error Handling
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    """Load the corpus with multiple fallback strategies."""
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
        {'name': 'Python engine latin-1', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'latin-1'}}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:60]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)

if df is None:
    raise FileNotFoundError("Could not load corpus. Check file path.")


# ==============================================================================
# CELL 4: Schema Validation
# ==============================================================================

print("\n" + "=" * 70)
print("2. SCHEMA VALIDATION")
print("=" * 70)

print(f"\n--- 2.1 Dataset Shape ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print(f"\n--- 2.2 Column Names ---")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\n--- 2.3 Data Types ---")
print(df.dtypes)

# Check for comment_text column (essential for ontology development)
if 'comment_text' not in df.columns:
    print("\n❌ ERROR: 'comment_text' column not found!")
    print("Available columns:", list(df.columns))
else:
    print(f"\n✅ 'comment_text' column found")
    print(f"   Non-null comments: {df['comment_text'].notna().sum():,}")
    print(f"   Null comments: {df['comment_text'].isna().sum():,}")


# ==============================================================================
# CELL 5: Text Cleaning & Preprocessing
# ==============================================================================

print("\n" + "=" * 70)
print("3. TEXT CLEANING & PREPROCESSING")
print("=" * 70)

def clean_text(text):
    """
    Clean and normalise comment text for analysis.
    Preserves health-related context while removing noise.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove timestamps (e.g., 2:30, 12:45:30)
    text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', text)

    # Keep important health-related patterns before removing numbers
    # Preserve patterns like "a1c", "t2d", "b12", etc.
    text = re.sub(r'\b(\d+)\s*(lbs?|pounds?|kg|kilos?)\b', r'\1_weight_unit', text)
    text = re.sub(r'\b(\d+)/(\d+)\b', r'blood_pressure_reading', text)  # BP readings

    # Remove standalone numbers (but keep alphanumeric like "a1c")
    text = re.sub(r'\b\d+\b', '', text)

    # Remove special characters but keep apostrophes and hyphens in words
    text = re.sub(r"[^\w\s'-]", ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Apply cleaning
print("🔄 Cleaning comment text...")
df['clean_text'] = df['comment_text'].apply(clean_text)

# Calculate statistics
df['word_count'] = df['clean_text'].str.split().str.len().fillna(0).astype(int)
df['char_count'] = df['clean_text'].str.len().fillna(0).astype(int)

print(f"✅ Text cleaning complete")

print(f"\n--- 3.1 Cleaned Text Statistics ---")
print(f"Total comments: {len(df):,}")
print(f"Empty after cleaning: {(df['clean_text'] == '').sum():,}")
print(f"Mean word count: {df['word_count'].mean():.1f}")
print(f"Median word count: {df['word_count'].median():.1f}")
print(f"Max word count: {df['word_count'].max():,}")

# Show sample cleaned comments
print(f"\n--- 3.2 Sample Cleaned Comments ---")
sample_df = df[df['word_count'] > 10].sample(n=5, random_state=42)
for idx, row in sample_df.iterrows():
    print(f"\nOriginal ({len(str(row['comment_text']))} chars):")
    print(f"  {str(row['comment_text'])[:150]}...")
    print(f"Cleaned ({row['word_count']} words):")
    print(f"  {row['clean_text'][:150]}...")


# ==============================================================================
# CELL 6: Vocabulary Analysis for Ontology Development
# ==============================================================================

print("\n" + "=" * 70)
print("4. VOCABULARY ANALYSIS")
print("=" * 70)

# Combine all cleaned text
all_text = ' '.join(df['clean_text'].dropna())

# Tokenize
print("🔄 Tokenizing corpus...")
all_words = all_text.split()
print(f"Total tokens: {len(all_words):,}")

# Define stopwords (expanded for YouTube comments)
stop_words = set(stopwords.words('english'))
youtube_stopwords = {
    # Common YouTube comment words
    'video', 'videos', 'channel', 'subscribe', 'subscribed', 'like', 'liked',
    'watch', 'watching', 'watched', 'thanks', 'thank', 'great', 'good', 'best',
    'love', 'loved', 'amazing', 'awesome', 'wonderful', 'excellent', 'fantastic',
    'really', 'much', 'very', 'just', 'also', 'would', 'could', 'should',
    'get', 'got', 'getting', 'make', 'made', 'making', 'take', 'took', 'taking',
    'one', 'two', 'first', 'know', 'think', 'see', 'look', 'come', 'go', 'going',
    'want', 'need', 'say', 'said', 'tell', 'told', 'try', 'tried', 'trying',
    'even', 'still', 'always', 'never', 'ever', 'every', 'many', 'much',
    'well', 'back', 'now', 'way', 'thing', 'things', 'something', 'anything',
    'lot', 'lots', 'bit', 'little', 'big', 'long', 'new', 'old', 'right',
    'dont', "don't", 'doesnt', "doesn't", 'didnt', "didn't", 'cant', "can't",
    'wont', "won't", 'ive', "i've", 'im', "i'm", 'youre', "you're", 'thats', "that's",
    'its', "it's", 'hes', "he's", 'shes', "she's", 'theyre', "they're",
    'people', 'person', 'everyone', 'someone', 'anyone', 'nobody',
    'time', 'times', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
    'ago', 'today', 'yesterday', 'tomorrow', 'since', 'last', 'next',
    'please', 'help', 'question', 'answer', 'comment', 'comments', 'post',
    'dr', 'doc', 'doctor', 'doctors'  # Keep medical terms but remove generic 'dr' references
}
stop_words.update(youtube_stopwords)

# Filter words
filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
print(f"Filtered tokens (no stopwords, len>2): {len(filtered_words):,}")

# Word frequency
word_freq = Counter(filtered_words)

print(f"\n--- 4.1 Top 100 Most Frequent Words ---")
print("(These inform initial ontology keyword selection)\n")
top_100 = word_freq.most_common(100)
for i, (word, count) in enumerate(top_100, 1):
    print(f"{i:3}. {word:20} {count:,}")


# ==============================================================================
# CELL 7: Health-Related Vocabulary Extraction
# ==============================================================================

print("\n" + "=" * 70)
print("5. HEALTH-RELATED VOCABULARY EXTRACTION")
print("=" * 70)

# Define seed health-related terms to find related vocabulary
health_seed_terms = {
    # RO1: Subjective Well-Being seeds
    'energy', 'tired', 'fatigue', 'sleep', 'mood', 'anxiety', 'depression',
    'brain', 'fog', 'focus', 'mental', 'pain', 'joint', 'inflammation',
    'gut', 'bloating', 'digestion', 'skin', 'acne', 'craving', 'hunger',
    'appetite', 'headache', 'migraine',

    # RO2: Tool-Mediated Validation seeds
    'weight', 'lost', 'pounds', 'lbs', 'glucose', 'sugar', 'a1c', 'insulin',
    'pressure', 'cholesterol', 'triglycerides', 'hdl', 'ldl', 'liver',
    'kidney', 'blood', 'test', 'numbers', 'levels',

    # RO3: Disease Specificity seeds
    'diabetes', 'diabetic', 't2d', 'prediabetes', 'pcos', 'thyroid',
    'hashimoto', 'autoimmune', 'arthritis', 'fibromyalgia', 'cancer',
    'heart', 'disease', 'hypertension', 'fatty', 'nafld', 'gout',
    'alzheimer', 'dementia', 'ibs', 'crohn', 'colitis'
}

# Find health-related words in corpus
print("🔄 Extracting health-related vocabulary...")

health_words_found = {}
for word, count in word_freq.items():
    # Direct match with seed terms
    if word in health_seed_terms:
        health_words_found[word] = count
    # Partial match (word contains seed term)
    elif any(seed in word for seed in health_seed_terms if len(seed) > 3):
        health_words_found[word] = count

# Sort by frequency
health_words_sorted = sorted(health_words_found.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- 5.1 Health-Related Words Found ({len(health_words_sorted)} terms) ---\n")
for i, (word, count) in enumerate(health_words_sorted[:80], 1):
    print(f"{i:3}. {word:25} {count:,}")


# ==============================================================================
# CELL 8: Research Objective Category Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("6. RESEARCH OBJECTIVE CATEGORY ANALYSIS")
print("=" * 70)

# Define preliminary keyword groups for each RO
ro_keywords = {
    'RO1_Subjective_WellBeing': [
        'energy', 'tired', 'fatigue', 'exhausted', 'sleep', 'insomnia', 'slept',
        'mood', 'anxiety', 'anxious', 'depression', 'depressed', 'happy', 'happier',
        'brain', 'fog', 'focus', 'mental', 'clarity', 'memory', 'cognitive',
        'pain', 'joint', 'ache', 'inflammation', 'swelling', 'stiff',
        'gut', 'bloating', 'bloated', 'digestion', 'stomach', 'bowel',
        'skin', 'acne', 'eczema', 'psoriasis', 'rash', 'complexion',
        'craving', 'cravings', 'hunger', 'hungry', 'appetite', 'satiety',
        'headache', 'migraine', 'calm', 'stress', 'stressed'
    ],
    'RO2_ToolMediated_Validation': [
        'weight', 'lost', 'pounds', 'lbs', 'kg', 'kilos', 'scale', 'waist',
        'glucose', 'sugar', 'a1c', 'hba1c', 'insulin', 'fasting', 'cgm',
        'pressure', 'bp', 'systolic', 'diastolic', 'hypertension',
        'cholesterol', 'triglycerides', 'hdl', 'ldl', 'lipid', 'statin',
        'liver', 'ast', 'alt', 'enzyme', 'bilirubin',
        'kidney', 'creatinine', 'gfr', 'egfr',
        'blood', 'test', 'numbers', 'levels', 'results', 'lab',
        'tsh', 't3', 't4', 'testosterone', 'hormone'
    ],
    'RO3_Disease_Specificity': [
        'diabetes', 'diabetic', 't2d', 'type2', 'prediabetes', 'prediabetic',
        'pcos', 'polycystic', 'ovary', 'ovarian',
        'thyroid', 'hashimoto', 'hashimotos', 'hypothyroid', 'hyperthyroid', 'graves',
        'autoimmune', 'lupus', 'arthritis', 'rheumatoid', 'celiac',
        'fibromyalgia', 'neuropathy', 'nerve',
        'cancer', 'tumor', 'chemo', 'chemotherapy',
        'heart', 'cardiovascular', 'coronary', 'attack', 'failure',
        'fatty', 'nafld', 'nash', 'cirrhosis',
        'gout', 'uric',
        'alzheimer', 'alzheimers', 'dementia',
        'ibs', 'crohn', 'crohns', 'colitis', 'ibd',
        'stroke', 'adhd', 'add', 'osteoporosis'
    ]
}

# Count matches for each RO category
print("\n--- 6.1 Preliminary Keyword Coverage by Research Objective ---\n")

ro_results = {}
for ro_name, keywords in ro_keywords.items():
    matches = 0
    matched_words = []
    for word in keywords:
        if word in word_freq:
            matches += word_freq[word]
            matched_words.append((word, word_freq[word]))

    # Sort matched words by frequency
    matched_words.sort(key=lambda x: x[1], reverse=True)
    ro_results[ro_name] = {
        'total_matches': matches,
        'unique_keywords_found': len(matched_words),
        'top_keywords': matched_words[:15]
    }

    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {matches:,}")
    print(f"  Unique keywords found: {len(matched_words)}/{len(keywords)}")
    print(f"  Top 15 keywords:")
    for word, count in matched_words[:15]:
        print(f"    - {word}: {count:,}")


# ==============================================================================
# CELL 9: Export Results for Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("7. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Top 500 words with frequencies
top_500_df = pd.DataFrame(word_freq.most_common(500), columns=['word', 'frequency'])
top_500_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_top500_words.csv', index=False)
print(f"✅ Exported: Phase2_Script1_top500_words.csv")

# Export 2: Health-related vocabulary
health_vocab_df = pd.DataFrame(health_words_sorted, columns=['word', 'frequency'])
health_vocab_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_health_vocabulary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_health_vocabulary.csv")

# Export 3: Sample comments for manual review (stratified by length)
print("\n🔄 Extracting sample comments for manual review...")

# Get samples from different length categories
samples = []

# Short comments (5-15 words) - often simple testimonials
short = df[(df['word_count'] >= 5) & (df['word_count'] <= 15)].sample(n=min(100, len(df)), random_state=42)
short['length_category'] = 'short'
samples.append(short)

# Medium comments (16-50 words) - more detailed experiences
medium = df[(df['word_count'] >= 16) & (df['word_count'] <= 50)].sample(n=min(100, len(df)), random_state=42)
medium['length_category'] = 'medium'
samples.append(medium)

# Long comments (51+ words) - detailed testimonials
long = df[df['word_count'] >= 51].sample(n=min(100, len(df)), random_state=42)
long['length_category'] = 'long'
samples.append(long)

sample_comments = pd.concat(samples, ignore_index=True)
sample_comments_export = sample_comments[['channel_name', 'length_category', 'word_count', 'comment_text', 'clean_text']].copy()
sample_comments_export.to_csv(f'{OUTPUT_DIR}Phase2_Script1_sample_comments.csv', index=False)
print(f"✅ Exported: Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)")

# Export 4: RO Category Summary
ro_summary = []
for ro_name, data in ro_results.items():
    ro_summary.append({
        'research_objective': ro_name,
        'total_matches': data['total_matches'],
        'unique_keywords_found': data['unique_keywords_found'],
        'top_keywords': ', '.join([f"{w}({c})" for w, c in data['top_keywords'][:10]])
    })
ro_summary_df = pd.DataFrame(ro_summary)
ro_summary_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_RO_summary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_RO_summary.csv")


# ==============================================================================
# CELL 10: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("8. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 1 - CORPUS EXPLORATION RESULTS
=============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. CORPUS STATISTICS
--------------------
Total comments: {len(df):,}
Non-empty after cleaning: {(df['clean_text'] != '').sum():,}
Total tokens (all words): {len(all_words):,}
Filtered tokens (no stopwords): {len(filtered_words):,}
Unique vocabulary size: {len(word_freq):,}

2. COMMENT LENGTH DISTRIBUTION
------------------------------
Mean word count: {df['word_count'].mean():.1f}
Median word count: {df['word_count'].median():.1f}
Std deviation: {df['word_count'].std():.1f}
Min: {df['word_count'].min()}
Max: {df['word_count'].max()}
25th percentile: {df['word_count'].quantile(0.25):.0f}
75th percentile: {df['word_count'].quantile(0.75):.0f}

3. TOP 50 WORDS (excluding stopwords)
-------------------------------------""")

for i, (word, count) in enumerate(word_freq.most_common(50), 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
4. RESEARCH OBJECTIVE PRELIMINARY COVERAGE
------------------------------------------""")

for ro_name, data in ro_results.items():
    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {data['total_matches']:,}")
    print(f"  Top 10 keywords: {', '.join([f'{w}({c:,})' for w, c in data['top_keywords'][:10]])}")

print(f"""
5. HEALTH-RELATED VOCABULARY (Top 40)
-------------------------------------""")
for i, (word, count) in enumerate(health_words_sorted[:40], 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
6. FILES EXPORTED
-----------------
- Phase2_Script1_top500_words.csv
- Phase2_Script1_health_vocabulary.csv
- Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)
- Phase2_Script1_RO_summary.csv

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 1 Complete")
print("=" * 70)

# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 1 - Corpus Exploration & Text Preparation
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script performs the foundational corpus exploration for Phase 2
# (Ontology Development). It loads the corpus, validates its structure,
# cleans the text data, and extracts initial vocabulary statistics to
# inform the ontology development process.
#
# Outputs:
# 1. Console output with corpus statistics (copy/paste to Claude)
# 2. CSV file with health-related word frequencies
# 3. CSV file with sample comments for manual review
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 1 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk wordcloud -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import Counter
from datetime import datetime
import warnings

# NLP imports
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Google Colab specific
from google.colab import drive

# Configure settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 1 - Corpus Exploration & Text Preparation")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & Configuration
# ==============================================================================

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus with Robust Error Handling
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
print("=" * 70)

def load_corpus_robust(filepath):
    """Load the corpus with multiple fallback strategies."""
    strategies = [
        {'name': 'C engine standard', 'params': {'engine': 'c', 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'C engine QUOTE_NONE', 'params': {'engine': 'c', 'quoting': 3, 'on_bad_lines': 'skip', 'encoding': 'utf-8', 'low_memory': False}},
        {'name': 'Python engine', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'utf-8'}},
        {'name': 'Python engine latin-1', 'params': {'engine': 'python', 'on_bad_lines': 'skip', 'encoding': 'latin-1'}}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:60]}...")
    return None

df = load_corpus_robust(CORPUS_PATH)

if df is None:
    raise FileNotFoundError("Could not load corpus. Check file path.")


# ==============================================================================
# CELL 4: Schema Validation
# ==============================================================================

print("\n" + "=" * 70)
print("2. SCHEMA VALIDATION")
print("=" * 70)

print(f"\n--- 2.1 Dataset Shape ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print(f"\n--- 2.2 Column Names ---")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\n--- 2.3 Data Types ---")
print(df.dtypes)

# Check for comment_text column (essential for ontology development)
if 'comment_text' not in df.columns:
    print("\n❌ ERROR: 'comment_text' column not found!")
    print("Available columns:", list(df.columns))
else:
    print(f"\n✅ 'comment_text' column found")
    print(f"   Non-null comments: {df['comment_text'].notna().sum():,}")
    print(f"   Null comments: {df['comment_text'].isna().sum():,}")


# ==============================================================================
# CELL 5: Text Cleaning & Preprocessing
# ==============================================================================

print("\n" + "=" * 70)
print("3. TEXT CLEANING & PREPROCESSING")
print("=" * 70)

def clean_text(text):
    """
    Clean and normalise comment text for analysis.
    Preserves health-related context while removing noise.
    """
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove timestamps (e.g., 2:30, 12:45:30)
    text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', text)

    # Keep important health-related patterns before removing numbers
    # Preserve patterns like "a1c", "t2d", "b12", etc.
    text = re.sub(r'\b(\d+)\s*(lbs?|pounds?|kg|kilos?)\b', r'\1_weight_unit', text)
    text = re.sub(r'\b(\d+)/(\d+)\b', r'blood_pressure_reading', text)  # BP readings

    # Remove standalone numbers (but keep alphanumeric like "a1c")
    text = re.sub(r'\b\d+\b', '', text)

    # Remove special characters but keep apostrophes and hyphens in words
    text = re.sub(r"[^\w\s'-]", ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Apply cleaning
print("🔄 Cleaning comment text...")
df['clean_text'] = df['comment_text'].apply(clean_text)

# Calculate statistics
df['word_count'] = df['clean_text'].str.split().str.len().fillna(0).astype(int)
df['char_count'] = df['clean_text'].str.len().fillna(0).astype(int)

print(f"✅ Text cleaning complete")

print(f"\n--- 3.1 Cleaned Text Statistics ---")
print(f"Total comments: {len(df):,}")
print(f"Empty after cleaning: {(df['clean_text'] == '').sum():,}")
print(f"Mean word count: {df['word_count'].mean():.1f}")
print(f"Median word count: {df['word_count'].median():.1f}")
print(f"Max word count: {df['word_count'].max():,}")

# Show sample cleaned comments
print(f"\n--- 3.2 Sample Cleaned Comments ---")
sample_df = df[df['word_count'] > 10].sample(n=5, random_state=42)
for idx, row in sample_df.iterrows():
    print(f"\nOriginal ({len(str(row['comment_text']))} chars):")
    print(f"  {str(row['comment_text'])[:150]}...")
    print(f"Cleaned ({row['word_count']} words):")
    print(f"  {row['clean_text'][:150]}...")


# ==============================================================================
# CELL 6: Vocabulary Analysis for Ontology Development
# ==============================================================================

print("\n" + "=" * 70)
print("4. VOCABULARY ANALYSIS")
print("=" * 70)

# Combine all cleaned text
all_text = ' '.join(df['clean_text'].dropna())

# Tokenize
print("🔄 Tokenizing corpus...")
all_words = all_text.split()
print(f"Total tokens: {len(all_words):,}")

# Define stopwords (expanded for YouTube comments)
stop_words = set(stopwords.words('english'))
youtube_stopwords = {
    # Common YouTube comment words
    'video', 'videos', 'channel', 'subscribe', 'subscribed', 'like', 'liked',
    'watch', 'watching', 'watched', 'thanks', 'thank', 'great', 'good', 'best',
    'love', 'loved', 'amazing', 'awesome', 'wonderful', 'excellent', 'fantastic',
    'really', 'much', 'very', 'just', 'also', 'would', 'could', 'should',
    'get', 'got', 'getting', 'make', 'made', 'making', 'take', 'took', 'taking',
    'one', 'two', 'first', 'know', 'think', 'see', 'look', 'come', 'go', 'going',
    'want', 'need', 'say', 'said', 'tell', 'told', 'try', 'tried', 'trying',
    'even', 'still', 'always', 'never', 'ever', 'every', 'many', 'much',
    'well', 'back', 'now', 'way', 'thing', 'things', 'something', 'anything',
    'lot', 'lots', 'bit', 'little', 'big', 'long', 'new', 'old', 'right',
    'dont', "don't", 'doesnt', "doesn't", 'didnt', "didn't", 'cant', "can't",
    'wont', "won't", 'ive', "i've", 'im', "i'm", 'youre', "you're", 'thats', "that's",
    'its', "it's", 'hes', "he's", 'shes', "she's", 'theyre', "they're",
    'people', 'person', 'everyone', 'someone', 'anyone', 'nobody',
    'time', 'times', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years',
    'ago', 'today', 'yesterday', 'tomorrow', 'since', 'last', 'next',
    'please', 'help', 'question', 'answer', 'comment', 'comments', 'post',
    'dr', 'doc', 'doctor', 'doctors'  # Keep medical terms but remove generic 'dr' references
}
stop_words.update(youtube_stopwords)

# Filter words
filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
print(f"Filtered tokens (no stopwords, len>2): {len(filtered_words):,}")

# Word frequency
word_freq = Counter(filtered_words)

print(f"\n--- 4.1 Top 100 Most Frequent Words ---")
print("(These inform initial ontology keyword selection)\n")
top_100 = word_freq.most_common(100)
for i, (word, count) in enumerate(top_100, 1):
    print(f"{i:3}. {word:20} {count:,}")


# ==============================================================================
# CELL 7: Health-Related Vocabulary Extraction
# ==============================================================================

print("\n" + "=" * 70)
print("5. HEALTH-RELATED VOCABULARY EXTRACTION")
print("=" * 70)

# Define seed health-related terms to find related vocabulary
health_seed_terms = {
    # RO1: Subjective Well-Being seeds
    'energy', 'tired', 'fatigue', 'sleep', 'mood', 'anxiety', 'depression',
    'brain', 'fog', 'focus', 'mental', 'pain', 'joint', 'inflammation',
    'gut', 'bloating', 'digestion', 'skin', 'acne', 'craving', 'hunger',
    'appetite', 'headache', 'migraine',

    # RO2: Tool-Mediated Validation seeds
    'weight', 'lost', 'pounds', 'lbs', 'glucose', 'sugar', 'a1c', 'insulin',
    'pressure', 'cholesterol', 'triglycerides', 'hdl', 'ldl', 'liver',
    'kidney', 'blood', 'test', 'numbers', 'levels',

    # RO3: Disease Specificity seeds
    'diabetes', 'diabetic', 't2d', 'prediabetes', 'pcos', 'thyroid',
    'hashimoto', 'autoimmune', 'arthritis', 'fibromyalgia', 'cancer',
    'heart', 'disease', 'hypertension', 'fatty', 'nafld', 'gout',
    'alzheimer', 'dementia', 'ibs', 'crohn', 'colitis'
}

# Find health-related words in corpus
print("🔄 Extracting health-related vocabulary...")

health_words_found = {}
for word, count in word_freq.items():
    # Direct match with seed terms
    if word in health_seed_terms:
        health_words_found[word] = count
    # Partial match (word contains seed term)
    elif any(seed in word for seed in health_seed_terms if len(seed) > 3):
        health_words_found[word] = count

# Sort by frequency
health_words_sorted = sorted(health_words_found.items(), key=lambda x: x[1], reverse=True)

print(f"\n--- 5.1 Health-Related Words Found ({len(health_words_sorted)} terms) ---\n")
for i, (word, count) in enumerate(health_words_sorted[:80], 1):
    print(f"{i:3}. {word:25} {count:,}")


# ==============================================================================
# CELL 8: Research Objective Category Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("6. RESEARCH OBJECTIVE CATEGORY ANALYSIS")
print("=" * 70)

# Define preliminary keyword groups for each RO
ro_keywords = {
    'RO1_Subjective_WellBeing': [
        'energy', 'tired', 'fatigue', 'exhausted', 'sleep', 'insomnia', 'slept',
        'mood', 'anxiety', 'anxious', 'depression', 'depressed', 'happy', 'happier',
        'brain', 'fog', 'focus', 'mental', 'clarity', 'memory', 'cognitive',
        'pain', 'joint', 'ache', 'inflammation', 'swelling', 'stiff',
        'gut', 'bloating', 'bloated', 'digestion', 'stomach', 'bowel',
        'skin', 'acne', 'eczema', 'psoriasis', 'rash', 'complexion',
        'craving', 'cravings', 'hunger', 'hungry', 'appetite', 'satiety',
        'headache', 'migraine', 'calm', 'stress', 'stressed'
    ],
    'RO2_ToolMediated_Validation': [
        'weight', 'lost', 'pounds', 'lbs', 'kg', 'kilos', 'scale', 'waist',
        'glucose', 'sugar', 'a1c', 'hba1c', 'insulin', 'fasting', 'cgm',
        'pressure', 'bp', 'systolic', 'diastolic', 'hypertension',
        'cholesterol', 'triglycerides', 'hdl', 'ldl', 'lipid', 'statin',
        'liver', 'ast', 'alt', 'enzyme', 'bilirubin',
        'kidney', 'creatinine', 'gfr', 'egfr',
        'blood', 'test', 'numbers', 'levels', 'results', 'lab',
        'tsh', 't3', 't4', 'testosterone', 'hormone'
    ],
    'RO3_Disease_Specificity': [
        'diabetes', 'diabetic', 't2d', 'type2', 'prediabetes', 'prediabetic',
        'pcos', 'polycystic', 'ovary', 'ovarian',
        'thyroid', 'hashimoto', 'hashimotos', 'hypothyroid', 'hyperthyroid', 'graves',
        'autoimmune', 'lupus', 'arthritis', 'rheumatoid', 'celiac',
        'fibromyalgia', 'neuropathy', 'nerve',
        'cancer', 'tumor', 'chemo', 'chemotherapy',
        'heart', 'cardiovascular', 'coronary', 'attack', 'failure',
        'fatty', 'nafld', 'nash', 'cirrhosis',
        'gout', 'uric',
        'alzheimer', 'alzheimers', 'dementia',
        'ibs', 'crohn', 'crohns', 'colitis', 'ibd',
        'stroke', 'adhd', 'add', 'osteoporosis'
    ]
}

# Count matches for each RO category
print("\n--- 6.1 Preliminary Keyword Coverage by Research Objective ---\n")

ro_results = {}
for ro_name, keywords in ro_keywords.items():
    matches = 0
    matched_words = []
    for word in keywords:
        if word in word_freq:
            matches += word_freq[word]
            matched_words.append((word, word_freq[word]))

    # Sort matched words by frequency
    matched_words.sort(key=lambda x: x[1], reverse=True)
    ro_results[ro_name] = {
        'total_matches': matches,
        'unique_keywords_found': len(matched_words),
        'top_keywords': matched_words[:15]
    }

    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {matches:,}")
    print(f"  Unique keywords found: {len(matched_words)}/{len(keywords)}")
    print(f"  Top 15 keywords:")
    for word, count in matched_words[:15]:
        print(f"    - {word}: {count:,}")


# ==============================================================================
# CELL 9: Export Results for Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("7. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Top 500 words with frequencies
top_500_df = pd.DataFrame(word_freq.most_common(500), columns=['word', 'frequency'])
top_500_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_top500_words.csv', index=False)
print(f"✅ Exported: Phase2_Script1_top500_words.csv")

# Export 2: Health-related vocabulary
health_vocab_df = pd.DataFrame(health_words_sorted, columns=['word', 'frequency'])
health_vocab_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_health_vocabulary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_health_vocabulary.csv")

# Export 3: Sample comments for manual review (stratified by length)
print("\n🔄 Extracting sample comments for manual review...")

# Get samples from different length categories
samples = []

# Short comments (5-15 words) - often simple testimonials
short = df[(df['word_count'] >= 5) & (df['word_count'] <= 15)].sample(n=min(100, len(df)), random_state=42)
short['length_category'] = 'short'
samples.append(short)

# Medium comments (16-50 words) - more detailed experiences
medium = df[(df['word_count'] >= 16) & (df['word_count'] <= 50)].sample(n=min(100, len(df)), random_state=42)
medium['length_category'] = 'medium'
samples.append(medium)

# Long comments (51+ words) - detailed testimonials
long = df[df['word_count'] >= 51].sample(n=min(100, len(df)), random_state=42)
long['length_category'] = 'long'
samples.append(long)

sample_comments = pd.concat(samples, ignore_index=True)
sample_comments_export = sample_comments[['channel_name', 'length_category', 'word_count', 'comment_text', 'clean_text']].copy()
sample_comments_export.to_csv(f'{OUTPUT_DIR}Phase2_Script1_sample_comments.csv', index=False)
print(f"✅ Exported: Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)")

# Export 4: RO Category Summary
ro_summary = []
for ro_name, data in ro_results.items():
    ro_summary.append({
        'research_objective': ro_name,
        'total_matches': data['total_matches'],
        'unique_keywords_found': data['unique_keywords_found'],
        'top_keywords': ', '.join([f"{w}({c})" for w, c in data['top_keywords'][:10]])
    })
ro_summary_df = pd.DataFrame(ro_summary)
ro_summary_df.to_csv(f'{OUTPUT_DIR}Phase2_Script1_RO_summary.csv', index=False)
print(f"✅ Exported: Phase2_Script1_RO_summary.csv")


# ==============================================================================
# CELL 10: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("8. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 1 - CORPUS EXPLORATION RESULTS
=============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. CORPUS STATISTICS
--------------------
Total comments: {len(df):,}
Non-empty after cleaning: {(df['clean_text'] != '').sum():,}
Total tokens (all words): {len(all_words):,}
Filtered tokens (no stopwords): {len(filtered_words):,}
Unique vocabulary size: {len(word_freq):,}

2. COMMENT LENGTH DISTRIBUTION
------------------------------
Mean word count: {df['word_count'].mean():.1f}
Median word count: {df['word_count'].median():.1f}
Std deviation: {df['word_count'].std():.1f}
Min: {df['word_count'].min()}
Max: {df['word_count'].max()}
25th percentile: {df['word_count'].quantile(0.25):.0f}
75th percentile: {df['word_count'].quantile(0.75):.0f}

3. TOP 50 WORDS (excluding stopwords)
-------------------------------------""")

for i, (word, count) in enumerate(word_freq.most_common(50), 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
4. RESEARCH OBJECTIVE PRELIMINARY COVERAGE
------------------------------------------""")

for ro_name, data in ro_results.items():
    print(f"\n{ro_name}:")
    print(f"  Total keyword matches: {data['total_matches']:,}")
    print(f"  Top 10 keywords: {', '.join([f'{w}({c:,})' for w, c in data['top_keywords'][:10]])}")

print(f"""
5. HEALTH-RELATED VOCABULARY (Top 40)
-------------------------------------""")
for i, (word, count) in enumerate(health_words_sorted[:40], 1):
    print(f"{i:2}. {word:20} {count:,}")

print(f"""
6. FILES EXPORTED
-----------------
- Phase2_Script1_top500_words.csv
- Phase2_Script1_health_vocabulary.csv
- Phase2_Script1_sample_comments.csv ({len(sample_comments_export)} comments)
- Phase2_Script1_RO_summary.csv

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 1 Complete")
print("=" * 70)
