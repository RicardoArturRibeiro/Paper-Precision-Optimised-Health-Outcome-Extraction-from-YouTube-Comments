# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 2 - LDA Topic Modelling
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script performs unsupervised topic discovery using Latent Dirichlet
# Allocation (LDA) to identify organic themes in the YouTube comment corpus.
# The discovered topics will inform and validate the ontology structure.
#
# Outputs:
# 1. Console output with topic-word distributions (copy/paste to Claude)
# 2. CSV file with topic compositions
# 3. CSV file with representative comments per topic
# 4. Visualisation of topic coherence scores
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 2 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================

# Install required packages
!pip install pandas numpy matplotlib seaborn nltk gensim pyLDAvis scikit-learn -q

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

# Topic modelling imports
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
from gensim.models.phrases import Phrases, Phraser
from sklearn.feature_extraction.text import CountVectorizer

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
pd.set_option('display.max_colwidth', 150)

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 2 - LDA Topic Modelling")
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

# LDA Configuration
NUM_TOPICS = 15  # Number of topics to discover
RANDOM_STATE = 42  # For reproducibility
SAMPLE_SIZE = 50000  # Sample size for faster LDA (None for full corpus)

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print(f"🎯 Number of Topics: {NUM_TOPICS}")
print(f"📊 Sample Size: {SAMPLE_SIZE if SAMPLE_SIZE else 'Full corpus'}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Load Corpus
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

print(f"\nTotal comments loaded: {len(df):,}")


# ==============================================================================
# CELL 4: Text Preprocessing for LDA
# ==============================================================================

print("\n" + "=" * 70)
print("2. TEXT PREPROCESSING FOR LDA")
print("=" * 70)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Extended stopwords for YouTube health comments
stop_words = set(stopwords.words('english'))
custom_stopwords = {
    # YouTube/social media terms
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
    'dr', 'doc', 'doctor', 'doctors', 'guy', 'guys', 'man', 'woman',
    # Common verbs to exclude
    'start', 'started', 'starting', 'stop', 'stopped', 'stopping',
    'feel', 'feeling', 'felt', 'keep', 'keeping', 'kept',
    'give', 'giving', 'gave', 'put', 'putting',
    # Numbers and time
    'ago', 'later', 'before', 'after', 'during'
}
stop_words.update(custom_stopwords)

def preprocess_for_lda(text):
    """
    Preprocess text for LDA topic modelling.
    Returns a list of tokens.
    """
    if pd.isna(text) or not isinstance(text, str):
        return []

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove special characters but keep hyphens in compound words
    text = re.sub(r"[^\w\s-]", ' ', text)

    # Remove standalone numbers
    text = re.sub(r'\b\d+\b', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize
    tokens = text.split()

    # Filter: remove stopwords, short words, and lemmatize
    processed_tokens = []
    for token in tokens:
        if token not in stop_words and len(token) > 2:
            # Lemmatize
            lemma = lemmatizer.lemmatize(token)
            if lemma not in stop_words and len(lemma) > 2:
                processed_tokens.append(lemma)

    return processed_tokens

# Sample data if specified
if SAMPLE_SIZE and len(df) > SAMPLE_SIZE:
    print(f"🔄 Sampling {SAMPLE_SIZE:,} comments from {len(df):,} total...")
    df_sample = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE).copy()
else:
    df_sample = df.copy()
    print(f"🔄 Using full corpus: {len(df_sample):,} comments")

# Apply preprocessing
print("🔄 Preprocessing text for LDA...")
df_sample['tokens'] = df_sample['comment_text'].apply(preprocess_for_lda)

# Filter out empty token lists
df_sample = df_sample[df_sample['tokens'].apply(len) >= 3]
print(f"✅ Comments with 3+ tokens: {len(df_sample):,}")

# Get the tokenized corpus
tokenized_corpus = df_sample['tokens'].tolist()
print(f"✅ Tokenized corpus ready: {len(tokenized_corpus):,} documents")


# ==============================================================================
# CELL 5: Build Bigram Model for Phrase Detection
# ==============================================================================

print("\n" + "=" * 70)
print("3. BUILDING BIGRAM MODEL")
print("=" * 70)

# Build bigram model to capture phrases like "blood_sugar", "weight_loss"
print("🔄 Training bigram phrase model...")
bigram = Phrases(tokenized_corpus, min_count=50, threshold=100)
bigram_mod = Phraser(bigram)

# Apply bigram model
tokenized_corpus_bigram = [bigram_mod[doc] for doc in tokenized_corpus]

# Show discovered bigrams
bigram_examples = []
for doc in tokenized_corpus_bigram[:1000]:
    for token in doc:
        if '_' in token:
            bigram_examples.append(token)

bigram_freq = Counter(bigram_examples)
print(f"\n--- Top 30 Discovered Bigrams ---")
for bigram_term, count in bigram_freq.most_common(30):
    print(f"  {bigram_term}: {count}")


# ==============================================================================
# CELL 6: Create Dictionary and Corpus for LDA
# ==============================================================================

print("\n" + "=" * 70)
print("4. CREATING DICTIONARY AND CORPUS")
print("=" * 70)

# Create dictionary
print("🔄 Building dictionary...")
dictionary = corpora.Dictionary(tokenized_corpus_bigram)

# Filter extremes: remove very rare and very common words
original_size = len(dictionary)
dictionary.filter_extremes(no_below=50, no_above=0.5)
print(f"Dictionary size: {original_size:,} → {len(dictionary):,} (after filtering)")

# Create corpus (bag of words)
print("🔄 Creating bag-of-words corpus...")
corpus = [dictionary.doc2bow(doc) for doc in tokenized_corpus_bigram]
print(f"✅ Corpus ready: {len(corpus):,} documents")


# ==============================================================================
# CELL 7: Train LDA Model
# ==============================================================================

print("\n" + "=" * 70)
print("5. TRAINING LDA MODEL")
print("=" * 70)

print(f"🔄 Training LDA model with {NUM_TOPICS} topics...")
print("   (This may take several minutes...)")

lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=NUM_TOPICS,
    random_state=RANDOM_STATE,
    update_every=1,
    chunksize=1000,
    passes=10,
    alpha='auto',
    per_word_topics=True
)

print("✅ LDA model training complete!")


# ==============================================================================
# CELL 8: Calculate Coherence Score
# ==============================================================================

print("\n" + "=" * 70)
print("6. EVALUATING MODEL COHERENCE")
print("=" * 70)

# Calculate coherence score
print("🔄 Calculating coherence score (c_v)...")
coherence_model = CoherenceModel(
    model=lda_model,
    texts=tokenized_corpus_bigram,
    dictionary=dictionary,
    coherence='c_v'
)
coherence_score = coherence_model.get_coherence()
print(f"✅ Coherence Score (c_v): {coherence_score:.4f}")
print("   (Score > 0.4 is generally considered acceptable)")


# ==============================================================================
# CELL 9: Display Topics
# ==============================================================================

print("\n" + "=" * 70)
print("7. DISCOVERED TOPICS")
print("=" * 70)

# Get topics with words and weights
topics_data = []

print("\n" + "-" * 70)
for topic_id in range(NUM_TOPICS):
    topic_words = lda_model.show_topic(topic_id, topn=15)
    words_str = ', '.join([f"{word}({weight:.3f})" for word, weight in topic_words])

    print(f"\n📌 TOPIC {topic_id}:")
    print(f"   {words_str}")

    # Store for export
    topics_data.append({
        'topic_id': topic_id,
        'top_words': ', '.join([word for word, _ in topic_words]),
        'words_with_weights': words_str
    })

print("\n" + "-" * 70)


# ==============================================================================
# CELL 10: Analyse Topic Distribution
# ==============================================================================

print("\n" + "=" * 70)
print("8. TOPIC DISTRIBUTION ANALYSIS")
print("=" * 70)

# Get dominant topic for each document
def get_dominant_topic(doc_bow, lda_model):
    """Get the dominant topic for a document."""
    topic_probs = lda_model.get_document_topics(doc_bow)
    if topic_probs:
        dominant = max(topic_probs, key=lambda x: x[1])
        return dominant[0], dominant[1]
    return -1, 0.0

print("🔄 Assigning dominant topics to documents...")
dominant_topics = []
for i, doc_bow in enumerate(corpus):
    topic_id, prob = get_dominant_topic(doc_bow, lda_model)
    dominant_topics.append({
        'doc_index': i,
        'dominant_topic': topic_id,
        'topic_probability': prob
    })

df_sample['dominant_topic'] = [d['dominant_topic'] for d in dominant_topics]
df_sample['topic_probability'] = [d['topic_probability'] for d in dominant_topics]

# Count documents per topic
topic_counts = df_sample['dominant_topic'].value_counts().sort_index()

print(f"\n--- Documents per Topic ---")
for topic_id, count in topic_counts.items():
    pct = count / len(df_sample) * 100
    print(f"  Topic {topic_id}: {count:,} documents ({pct:.1f}%)")


# ==============================================================================
# CELL 11: Extract Representative Comments per Topic
# ==============================================================================

print("\n" + "=" * 70)
print("9. REPRESENTATIVE COMMENTS PER TOPIC")
print("=" * 70)

representative_comments = []

for topic_id in range(NUM_TOPICS):
    # Get comments with this dominant topic, sorted by probability
    topic_docs = df_sample[df_sample['dominant_topic'] == topic_id].nlargest(5, 'topic_probability')

    print(f"\n📌 TOPIC {topic_id} - Top 3 Representative Comments:")
    print("-" * 50)

    for idx, (_, row) in enumerate(topic_docs.head(3).iterrows()):
        comment = str(row['comment_text'])[:300]
        print(f"  [{idx+1}] (prob={row['topic_probability']:.3f})")
        print(f"      {comment}...")
        print()

        representative_comments.append({
            'topic_id': topic_id,
            'rank': idx + 1,
            'probability': row['topic_probability'],
            'channel': row.get('channel_name', 'Unknown'),
            'comment': str(row['comment_text'])[:500]
        })


# ==============================================================================
# CELL 12: Topic Labelling Suggestions
# ==============================================================================

print("\n" + "=" * 70)
print("10. TOPIC LABELLING SUGGESTIONS")
print("=" * 70)

# Analyse each topic's top words to suggest labels
print("\nBased on the top words, here are suggested topic labels:")
print("(These are algorithmic suggestions - manual review recommended)\n")

# Define keyword groups for automatic labelling
label_keywords = {
    'Weight Loss & Body Composition': ['weight', 'lost', 'pound', 'fat', 'lose', 'scale', 'waist', 'size'],
    'Diet & Eating Patterns': ['eat', 'eating', 'food', 'meal', 'diet', 'fast', 'fasting', 'breakfast', 'lunch', 'dinner'],
    'Keto/Carnivore Diet': ['keto', 'carnivore', 'carb', 'carbs', 'ketogenic', 'ketosis', 'low-carb'],
    'Blood Sugar & Diabetes': ['sugar', 'glucose', 'insulin', 'diabetes', 'diabetic', 'a1c', 'blood_sugar'],
    'Energy & Fatigue': ['energy', 'tired', 'fatigue', 'exhausted', 'energetic'],
    'Pain & Inflammation': ['pain', 'inflammation', 'joint', 'ache', 'arthritis', 'swelling'],
    'Mental Health & Mood': ['anxiety', 'depression', 'mood', 'mental', 'stress', 'brain', 'fog'],
    'Heart & Cardiovascular': ['heart', 'cholesterol', 'ldl', 'hdl', 'cardiovascular', 'blood_pressure'],
    'Digestive Health': ['gut', 'stomach', 'digest', 'bloat', 'bowel', 'ibs'],
    'Skin Health': ['skin', 'acne', 'eczema', 'rash', 'complexion'],
    'Sleep Quality': ['sleep', 'insomnia', 'sleeping', 'rest', 'night'],
    'Medical/Clinical': ['doctor', 'medication', 'medicine', 'prescription', 'drug'],
    'Food Types': ['meat', 'beef', 'egg', 'butter', 'vegetable', 'fruit', 'fish'],
    'General Health': ['health', 'healthy', 'body', 'life', 'wellness']
}

for topic_id in range(NUM_TOPICS):
    topic_words = [word for word, _ in lda_model.show_topic(topic_id, topn=20)]

    # Score each label based on keyword overlap
    label_scores = {}
    for label, keywords in label_keywords.items():
        score = sum(1 for kw in keywords if any(kw in tw for tw in topic_words))
        if score > 0:
            label_scores[label] = score

    # Get best label(s)
    if label_scores:
        best_labels = sorted(label_scores.items(), key=lambda x: x[1], reverse=True)[:2]
        suggested = ' / '.join([l[0] for l in best_labels])
    else:
        suggested = "General Discussion"

    top_5_words = ', '.join(topic_words[:5])
    print(f"Topic {topic_id}: {suggested}")
    print(f"         Top words: {top_5_words}\n")


# ==============================================================================
# CELL 13: Export Results
# ==============================================================================

print("\n" + "=" * 70)
print("11. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Topics with words
topics_df = pd.DataFrame(topics_data)
topics_df.to_csv(f'{OUTPUT_DIR}Phase2_Script2_LDA_topics.csv', index=False)
print(f"✅ Exported: Phase2_Script2_LDA_topics.csv")

# Export 2: Representative comments
rep_comments_df = pd.DataFrame(representative_comments)
rep_comments_df.to_csv(f'{OUTPUT_DIR}Phase2_Script2_representative_comments.csv', index=False)
print(f"✅ Exported: Phase2_Script2_representative_comments.csv")

# Export 3: Topic distribution
topic_dist_df = pd.DataFrame({
    'topic_id': topic_counts.index,
    'document_count': topic_counts.values,
    'percentage': (topic_counts.values / len(df_sample) * 100).round(2)
})
topic_dist_df.to_csv(f'{OUTPUT_DIR}Phase2_Script2_topic_distribution.csv', index=False)
print(f"✅ Exported: Phase2_Script2_topic_distribution.csv")

# Export 4: Bigram frequencies
bigram_df = pd.DataFrame(bigram_freq.most_common(100), columns=['bigram', 'frequency'])
bigram_df.to_csv(f'{OUTPUT_DIR}Phase2_Script2_bigrams.csv', index=False)
print(f"✅ Exported: Phase2_Script2_bigrams.csv")


# ==============================================================================
# CELL 14: Visualisation - Topic Distribution
# ==============================================================================

print("\n" + "=" * 70)
print("12. GENERATING VISUALISATIONS")
print("=" * 70)

# Plot topic distribution
fig, ax = plt.subplots(figsize=(12, 6))
colors = plt.cm.viridis(np.linspace(0, 0.8, NUM_TOPICS))

bars = ax.bar(range(NUM_TOPICS), topic_counts.values, color=colors)
ax.set_xlabel('Topic ID', fontsize=12)
ax.set_ylabel('Number of Documents', fontsize=12)
ax.set_title('Distribution of Documents Across Topics', fontsize=14, fontweight='bold')
ax.set_xticks(range(NUM_TOPICS))

# Add value labels on bars
for bar, count in zip(bars, topic_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
            f'{count:,}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}Phase2_Script2_topic_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"✅ Saved: Phase2_Script2_topic_distribution.png")


# ==============================================================================
# CELL 15: Summary Report for Claude
# ==============================================================================

print("\n" + "=" * 70)
print("13. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 2 SCRIPT 2 - LDA TOPIC MODELLING RESULTS
==============================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. MODEL CONFIGURATION
----------------------
Number of Topics: {NUM_TOPICS}
Sample Size: {len(df_sample):,} documents
Dictionary Size: {len(dictionary):,} terms
Coherence Score (c_v): {coherence_score:.4f}

2. DISCOVERED TOPICS
--------------------""")

for topic_id in range(NUM_TOPICS):
    topic_words = lda_model.show_topic(topic_id, topn=12)
    words_str = ', '.join([f"{word}" for word, weight in topic_words])
    count = topic_counts.get(topic_id, 0)
    pct = count / len(df_sample) * 100
    print(f"\nTOPIC {topic_id} ({count:,} docs, {pct:.1f}%):")
    print(f"  {words_str}")

print(f"""

3. TOPIC DISTRIBUTION SUMMARY
-----------------------------""")
for topic_id, count in topic_counts.items():
    pct = count / len(df_sample) * 100
    print(f"Topic {topic_id}: {count:,} documents ({pct:.1f}%)")

print(f"""

4. TOP 30 DISCOVERED BIGRAMS
----------------------------""")
for bigram_term, count in bigram_freq.most_common(30):
    print(f"  {bigram_term}: {count}")

print(f"""

5. FILES EXPORTED
-----------------
- Phase2_Script2_LDA_topics.csv
- Phase2_Script2_representative_comments.csv
- Phase2_Script2_topic_distribution.csv
- Phase2_Script2_bigrams.csv
- Phase2_Script2_topic_distribution.png

6. INTERPRETATION NOTES FOR ONTOLOGY DEVELOPMENT
------------------------------------------------
Review the topics above and identify:
1. Topics that align with RO1 (Subjective Well-Being)
2. Topics that align with RO2 (Tool-Mediated Validation)
3. Topics that align with RO3 (Disease Specificity)
4. Any unexpected themes that should be added to the ontology
5. Community-specific vocabulary from bigrams

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 2 Complete")
print("=" * 70)

