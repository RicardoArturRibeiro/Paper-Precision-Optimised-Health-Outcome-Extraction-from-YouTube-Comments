# ==============================================================================
# PhD Thesis RQ1: Complete Exploratory Data Analysis (EDA) Script
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose: 
# Comprehensive Exploratory Data Analysis of the YouTube comment corpus
# for Research Question 1, examining the 'Healthcasting' phenomenon.
#
# Script Sections:
# 1. Environment Setup & Configuration
# 2. Data Loading with Robust Error Handling
# 3. Data Quality Assessment
# 4. Corpus Structure Analysis
# 5. Channel Profile Analysis
# 6. Content Analysis (Text & Tags)
# 7. Temporal Analysis
# 8. Engagement Metrics Analysis
# 9. Export Summary Statistics
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date of Final Version: 02 January 2026
# Version: 2.0 (Fixed timezone compatibility for Excel export)
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup & Library Installation
# ==============================================================================
# Action: Run this cell first to install and import all required libraries.

# Install required packages
!pip install pandas matplotlib seaborn wordcloud nltk openpyxl -q

# Core imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import re
import os

# Text analysis imports
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Google Colab specific
from google.colab import drive

# Download NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Configure display settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.float_format', '{:.2f}'.format)

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')

print("=" * 60)
print("PhD RQ1: Exploratory Data Analysis Script")
print("=" * 60)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Google Drive Mount & File Configuration
# ==============================================================================
# Action: Mount Google Drive and configure the file paths.
# IMPORTANT: Update DATASET_PATH to match your file location.

# Mount Google Drive
drive.mount('/content/drive')

# =============================================================================
# CONFIGURATION - UPDATE THESE PATHS AS NEEDED
# =============================================================================
DATASET_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/EDA_Outputs/'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("FILE CONFIGURATION")
print("=" * 60)
print(f"📂 Dataset Path: {DATASET_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("✅ Google Drive mounted successfully.")


# ==============================================================================
# CELL 3: Data Loading with Robust Error Handling
# ==============================================================================
# Action: Load the CSV with multiple fallback strategies to handle
# problematic characters in YouTube comments.

print("=" * 60)
print("DATA LOADING")
print("=" * 60)

def load_corpus_robust(filepath):
    """
    Attempts to load the YouTube corpus CSV with multiple fallback strategies.
    YouTube comments often contain special characters that break standard CSV parsing.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame or None
        Loaded dataframe or None if all strategies fail
    """
    
    strategies = [
        # Strategy 1: C engine with standard settings (fastest, most common)
        {
            'name': 'C engine with standard settings',
            'params': {
                'engine': 'c',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'low_memory': False
            }
        },
        # Strategy 2: C engine with relaxed quoting
        {
            'name': 'C engine with QUOTE_NONE',
            'params': {
                'engine': 'c',
                'quoting': 3,  # csv.QUOTE_NONE
                'on_bad_lines': 'skip',
                'encoding': 'utf-8',
                'low_memory': False
            }
        },
        # Strategy 3: Python engine (more flexible with malformed data)
        {
            'name': 'Python engine with error handling',
            'params': {
                'engine': 'python',
                'on_bad_lines': 'skip',
                'encoding': 'utf-8'
            }
        },
        # Strategy 4: Python engine with different encoding
        {
            'name': 'Python engine with latin-1 encoding',
            'params': {
                'engine': 'python',
                'on_bad_lines': 'skip',
                'encoding': 'latin-1'
            }
        }
    ]
    
    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}/{len(strategies)}: {strategy['name']}...")
            df = pd.read_csv(filepath, **strategy['params'])
            print(f"  ✅ SUCCESS! Loaded {len(df):,} rows using: {strategy['name']}")
            return df
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:80]}...")
            continue
    
    print("❌ All loading strategies failed. Please check the file manually.")
    return None

# Load the dataset
print(f"🔄 Attempting to load: {DATASET_PATH}")
df = load_corpus_robust(DATASET_PATH)

if df is not None:
    print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
else:
    raise FileNotFoundError("Could not load the dataset. Please verify the file path and format.")


# ==============================================================================
# CELL 4: Data Quality Assessment
# ==============================================================================
# Action: Perform initial data quality checks and document any issues.

print("\n" + "=" * 60)
print("1. DATA QUALITY ASSESSMENT")
print("=" * 60)

# 4.1 Schema Inspection
print("\n--- 1.1 Dataset Schema ---")
print(df.dtypes)

# 4.2 Missing Values Analysis
print("\n--- 1.2 Missing Values Analysis ---")
missing_df = pd.DataFrame({
    'Column': df.columns,
    'Missing Count': df.isnull().sum().values,
    'Missing %': (df.isnull().sum().values / len(df) * 100).round(2),
    'Dtype': df.dtypes.values
})
missing_df = missing_df.sort_values('Missing %', ascending=False)
print(missing_df.to_string(index=False))

# 4.3 Duplicate Analysis
print("\n--- 1.3 Duplicate Analysis ---")
total_rows = len(df)
duplicate_comments = df.duplicated(subset=['comment_text'], keep='first').sum()
duplicate_full = df.duplicated(keep='first').sum()
print(f"Total rows: {total_rows:,}")
print(f"Duplicate rows (all columns): {duplicate_full:,} ({duplicate_full/total_rows*100:.2f}%)")
print(f"Duplicate comment texts: {duplicate_comments:,} ({duplicate_comments/total_rows*100:.2f}%)")

# 4.4 Data Type Conversions
print("\n--- 1.4 Data Type Conversions ---")
# Convert datetime columns
datetime_cols = ['comment_published_at', 'video_published_at', 'retrieval_timestamp']
for col in datetime_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
        print(f"  ✓ Converted {col} to datetime")

# Ensure numeric columns are correct type
numeric_cols = ['comment_like_count', 'total_reply_count', 'video_category_id']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        print(f"  ✓ Converted {col} to integer")

print("\n✅ Data quality assessment complete.")


# ==============================================================================
# CELL 5: Corpus Structure Analysis
# ==============================================================================
# Action: Analyze the overall structure and composition of the corpus.

print("\n" + "=" * 60)
print("2. CORPUS STRUCTURE ANALYSIS")
print("=" * 60)

# 5.1 Overall Statistics
print("\n--- 2.1 Overall Corpus Statistics ---")
corpus_stats = {
    'Total Comments': len(df),
    'Unique Channels': df['channel_name'].nunique() if 'channel_name' in df.columns else 'N/A',
    'Unique Videos': df['video_id'].nunique() if 'video_id' in df.columns else 'N/A',
    'Unique Authors': df['comment_author'].nunique() if 'comment_author' in df.columns else 'N/A',
    'Date Range Start': df['comment_published_at'].min().strftime('%Y-%m-%d') if 'comment_published_at' in df.columns else 'N/A',
    'Date Range End': df['comment_published_at'].max().strftime('%Y-%m-%d') if 'comment_published_at' in df.columns else 'N/A'
}
for key, value in corpus_stats.items():
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        print(f"  {key}: {value:,}")
    else:
        print(f"  {key}: {value}")

# 5.2 Comments per Channel Distribution
print("\n--- 2.2 Comments per Channel ---")
if 'channel_name' in df.columns:
    channel_counts = df['channel_name'].value_counts()
    print(channel_counts.to_string())
    
    # Visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(channel_counts.index[::-1], channel_counts.values[::-1], color=sns.color_palette('viridis', len(channel_counts)))
    ax.set_xlabel('Number of Comments', fontsize=12)
    ax.set_ylabel('Channel Name', fontsize=12)
    ax.set_title('Distribution of Comments per Channel', fontsize=16, fontweight='bold')
    
    # Add value labels
    for bar, val in zip(bars, channel_counts.values[::-1]):
        ax.text(val + 200, bar.get_y() + bar.get_height()/2, f'{val:,}', 
                va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comments_per_channel.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comments_per_channel.png")

# 5.3 Comments per Video Category
print("\n--- 2.3 Comments per Video Category ---")
if 'video_category_name' in df.columns:
    category_counts = df['video_category_name'].value_counts()
    print(category_counts.to_string())
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(category_counts.index[::-1], category_counts.values[::-1], 
                   color=sns.color_palette('plasma', len(category_counts)))
    ax.set_xlabel('Number of Comments', fontsize=12)
    ax.set_ylabel('Video Category', fontsize=12)
    ax.set_title('Distribution of Comments per Video Category', fontsize=16, fontweight='bold')
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comments_per_category.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comments_per_category.png")


# ==============================================================================
# CELL 6: Channel Profile Analysis
# ==============================================================================
# Action: Analyze channel characteristics including age and activity patterns.

print("\n" + "=" * 60)
print("3. CHANNEL PROFILE ANALYSIS")
print("=" * 60)

if 'video_published_at' in df.columns and 'channel_name' in df.columns:
    # 6.1 Channel Statistics
    print("\n--- 3.1 Channel Age Analysis ---")
    
    # Get earliest video per channel (proxy for channel activity start in corpus)
    channel_profile = df.groupby('channel_name').agg(
        earliest_video=('video_published_at', 'min'),
        latest_video=('video_published_at', 'max'),
        total_comments=('comment_text', 'count'),
        unique_videos=('video_id', 'nunique'),
        avg_likes_per_comment=('comment_like_count', 'mean')
    ).reset_index()
    
    # Calculate channel activity span in years
    current_date = pd.Timestamp.now(tz='UTC')
    channel_profile['activity_span_years'] = (
        (channel_profile['latest_video'] - channel_profile['earliest_video']).dt.days / 365.25
    ).round(1)
    
    # Create string version for display (timezone-naive for Excel compatibility)
    channel_profile['earliest_video_str'] = channel_profile['earliest_video'].dt.strftime('%Y-%m-%d')
    channel_profile['latest_video_str'] = channel_profile['latest_video'].dt.strftime('%Y-%m-%d')
    
    # Display
    display_cols = ['channel_name', 'earliest_video_str', 'activity_span_years', 
                   'unique_videos', 'total_comments', 'avg_likes_per_comment']
    channel_display = channel_profile[display_cols].copy()
    channel_display['avg_likes_per_comment'] = channel_display['avg_likes_per_comment'].round(1)
    channel_display = channel_display.sort_values('activity_span_years', ascending=False)
    print(channel_display.to_string(index=False))
    
    # Visualization: Channel Activity Span
    fig, ax = plt.subplots(figsize=(12, 8))
    sorted_profile = channel_profile.sort_values('activity_span_years', ascending=True)
    bars = ax.barh(sorted_profile['channel_name'], sorted_profile['activity_span_years'], 
                   color=sns.color_palette('mako', len(sorted_profile)))
    ax.set_xlabel('Activity Span (Years)', fontsize=12)
    ax.set_ylabel('Channel Name', fontsize=12)
    ax.set_title('Channel Content Age (Based on Earliest Video in Corpus)', fontsize=16, fontweight='bold')
    
    # Add value labels
    for bar, val in zip(bars, sorted_profile['activity_span_years']):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2, f'{val:.1f}', 
                va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_channel_activity_span.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_channel_activity_span.png")


# ==============================================================================
# CELL 7: Content Analysis - Video Tags
# ==============================================================================
# Action: Analyze video tags to understand thematic focus.

print("\n" + "=" * 60)
print("4. CONTENT ANALYSIS - VIDEO TAGS")
print("=" * 60)

if 'video_tags' in df.columns:
    # 7.1 Process Tags
    print("\n--- 4.1 Video Tags Word Cloud ---")
    
    # Combine all tags (handling potential list-as-string format)
    all_tags_raw = df['video_tags'].dropna().astype(str)
    
    # Clean and combine tags
    all_tags = ' '.join(all_tags_raw.tolist())
    # Remove common delimiters that might be in the string representation
    all_tags = re.sub(r"[\[\]',\"]", ' ', all_tags)
    
    if all_tags.strip():
        # Generate word cloud
        wordcloud = WordCloud(
            width=1600, 
            height=800, 
            background_color='white', 
            colormap='cividis',
            max_words=150,
            min_font_size=10,
            collocations=False
        ).generate(all_tags)
        
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud of Creator-Assigned Video Tags', fontsize=20, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}fig_video_tags_wordcloud.png', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"  📊 Figure saved: fig_video_tags_wordcloud.png")
    else:
        print("  ⚠️ No video tags available for word cloud generation.")


# ==============================================================================
# CELL 8: Content Analysis - Comment Text
# ==============================================================================
# Action: Analyze comment content including length distribution and vocabulary.

print("\n" + "=" * 60)
print("5. CONTENT ANALYSIS - COMMENTS")
print("=" * 60)

if 'comment_text' in df.columns:
    # 8.1 Comment Length Analysis
    print("\n--- 5.1 Comment Length Analysis ---")
    
    # Calculate word count for each comment
    df['comment_word_count'] = df['comment_text'].fillna('').str.split().str.len()
    df['comment_char_count'] = df['comment_text'].fillna('').str.len()
    
    # Statistics
    length_stats = df['comment_word_count'].describe()
    print("Word Count Statistics:")
    print(f"  Mean: {length_stats['mean']:.1f} words")
    print(f"  Median: {length_stats['50%']:.1f} words")
    print(f"  Std Dev: {length_stats['std']:.1f} words")
    print(f"  Min: {length_stats['min']:.0f} words")
    print(f"  Max: {length_stats['max']:.0f} words")
    
    # Visualization: Comment Length Distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df['comment_word_count'], bins=100, kde=True, color='teal', ax=ax)
    ax.set_xlabel('Number of Words', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Comment Length (Word Count)', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 200)  # Focus on typical comment lengths
    ax.axvline(x=length_stats['50%'], color='red', linestyle='--', label=f'Median: {length_stats["50%"]:.0f}')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comment_length_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comment_length_distribution.png")
    
    # 8.2 Top Words in Comments
    print("\n--- 5.2 Top 30 Most Frequent Words in Comments ---")
    
    # Prepare text for analysis
    all_comments = ' '.join(df['comment_text'].dropna().astype(str))
    all_comments_clean = re.sub(r'[^A-Za-z\s]', '', all_comments.lower())
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    # Add custom stopwords common in YouTube comments
    custom_stopwords = {'like', 'would', 'could', 'also', 'get', 'got', 'one', 'two', 
                       'really', 'much', 'even', 'just', 'know', 'think', 'make', 
                       'going', 'want', 'say', 'said', 'see', 'look', 'come', 'take',
                       'video', 'videos', 'channel', 'thank', 'thanks', 'great', 'good',
                       'love', 'amazing', 'awesome', 'best', 'watch', 'watching'}
    stop_words.update(custom_stopwords)
    
    words = [word for word in all_comments_clean.split() 
             if word not in stop_words and len(word) > 2]
    
    # Get top words
    word_counts = Counter(words)
    top_words = pd.DataFrame(word_counts.most_common(30), columns=['Word', 'Frequency'])
    print(top_words.to_string(index=False))
    
    # Visualization: Top Words
    fig, ax = plt.subplots(figsize=(12, 10))
    bars = ax.barh(top_words['Word'][::-1], top_words['Frequency'][::-1], 
                   color=sns.color_palette('cubehelix', 30))
    ax.set_xlabel('Frequency', fontsize=12)
    ax.set_ylabel('Word', fontsize=12)
    ax.set_title('Top 30 Most Frequent Words in User Comments', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_top_words_comments.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_top_words_comments.png")
    
    # 8.3 Comment Word Cloud
    print("\n--- 5.3 Comment Text Word Cloud ---")
    wordcloud_comments = WordCloud(
        width=1600, 
        height=800, 
        background_color='white', 
        colormap='viridis',
        max_words=200,
        stopwords=stop_words,
        collocations=True
    ).generate(all_comments_clean)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.imshow(wordcloud_comments, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud of User Comments', fontsize=20, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comments_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comments_wordcloud.png")


# ==============================================================================
# CELL 9: Temporal Analysis
# ==============================================================================
# Action: Analyze comment activity patterns over time.

print("\n" + "=" * 60)
print("6. TEMPORAL ANALYSIS")
print("=" * 60)

if 'comment_published_at' in df.columns:
    # 9.1 Comments per Year
    print("\n--- 6.1 Comment Volume by Year ---")
    df['comment_year'] = df['comment_published_at'].dt.year
    yearly_counts = df['comment_year'].value_counts().sort_index()
    print(yearly_counts.to_string())
    
    # Visualization: Yearly Trend
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2, 
            markersize=8, color='dodgerblue')
    ax.fill_between(yearly_counts.index, yearly_counts.values, alpha=0.3)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Comments', fontsize=12)
    ax.set_title('Volume of Comments Published per Year', fontsize=16, fontweight='bold')
    ax.set_xticks(yearly_counts.index)
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for x, y in zip(yearly_counts.index, yearly_counts.values):
        ax.annotate(f'{y:,}', (x, y), textcoords="offset points", 
                   xytext=(0, 10), ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comments_per_year.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comments_per_year.png")
    
    # 9.2 Comments per Month (Recent Years)
    print("\n--- 6.2 Monthly Comment Trend (Last 3 Years) ---")
    df['comment_month'] = df['comment_published_at'].dt.to_period('M')
    recent_years = df[df['comment_year'] >= (df['comment_year'].max() - 2)]
    monthly_counts = recent_years['comment_month'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    monthly_counts.plot(kind='line', marker='.', ax=ax, color='coral')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of Comments', fontsize=12)
    ax.set_title('Monthly Comment Volume (Last 3 Years)', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_comments_monthly_trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_comments_monthly_trend.png")


# ==============================================================================
# CELL 10: Engagement Metrics Analysis
# ==============================================================================
# Action: Analyze comment likes and replies to understand engagement patterns.

print("\n" + "=" * 60)
print("7. ENGAGEMENT METRICS ANALYSIS")
print("=" * 60)

# 10.1 Engagement Statistics
print("\n--- 7.1 Engagement Summary Statistics ---")
engagement_cols = ['comment_like_count', 'total_reply_count']
available_engagement = [col for col in engagement_cols if col in df.columns]

if available_engagement:
    engagement_stats = df[available_engagement].describe()
    print(engagement_stats.round(2).to_string())
    
    # Calculate additional metrics
    print("\n--- 7.2 Engagement Distribution Insights ---")
    for col in available_engagement:
        zero_count = (df[col] == 0).sum()
        zero_pct = zero_count / len(df) * 100
        non_zero_mean = df[df[col] > 0][col].mean()
        print(f"\n{col}:")
        print(f"  Comments with zero: {zero_count:,} ({zero_pct:.1f}%)")
        print(f"  Mean (excluding zeros): {non_zero_mean:.2f}")
        print(f"  Top 1% threshold: {df[col].quantile(0.99):.0f}")
    
    # 10.2 Engagement Distribution Visualization
    print("\n--- 7.3 Engagement Distribution Plots ---")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Likes distribution (log scale for visibility)
    if 'comment_like_count' in df.columns:
        likes_nonzero = df[df['comment_like_count'] > 0]['comment_like_count']
        sns.histplot(likes_nonzero, bins=50, ax=axes[0], color='salmon', log_scale=(True, True))
        axes[0].set_title('Distribution of Comment Likes (Non-Zero, Log Scale)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Number of Likes')
        axes[0].set_ylabel('Frequency')
    
    # Replies distribution
    if 'total_reply_count' in df.columns:
        replies_nonzero = df[df['total_reply_count'] > 0]['total_reply_count']
        sns.histplot(replies_nonzero, bins=30, ax=axes[1], color='purple', log_scale=(True, True))
        axes[1].set_title('Distribution of Comment Replies (Non-Zero, Log Scale)', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Number of Replies')
        axes[1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}fig_engagement_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    print(f"  📊 Figure saved: fig_engagement_distribution.png")
    
    # 10.3 Engagement by Channel
    print("\n--- 7.4 Average Engagement by Channel ---")
    if 'channel_name' in df.columns:
        channel_engagement = df.groupby('channel_name')[available_engagement].mean().round(2)
        channel_engagement = channel_engagement.sort_values('comment_like_count', ascending=False)
        print(channel_engagement.to_string())
        
        # Visualization
        fig, ax = plt.subplots(figsize=(12, 8))
        channel_engagement['comment_like_count'].sort_values().plot(
            kind='barh', ax=ax, color=sns.color_palette('rocket', len(channel_engagement))
        )
        ax.set_xlabel('Average Likes per Comment', fontsize=12)
        ax.set_ylabel('Channel Name', fontsize=12)
        ax.set_title('Average Comment Engagement by Channel', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}fig_engagement_by_channel.png', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"  📊 Figure saved: fig_engagement_by_channel.png")


# ==============================================================================
# CELL 11: Export Summary Statistics
# ==============================================================================
# Action: Export all key statistics to an Excel file for the report.

print("\n" + "=" * 60)
print("8. EXPORT SUMMARY STATISTICS")
print("=" * 60)

# Helper function to remove timezone from datetime columns for Excel compatibility
def make_excel_compatible(dataframe):
    """
    Convert timezone-aware datetime columns to timezone-naive for Excel export.
    Excel does not support timezone-aware datetimes.
    """
    df_copy = dataframe.copy()
    for col in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
            # Check if timezone-aware
            if df_copy[col].dt.tz is not None:
                df_copy[col] = df_copy[col].dt.tz_localize(None)
    return df_copy

# Create summary dataframes for export
summary_file = f'{OUTPUT_DIR}PhD_RQ1_EDA_Summary_Statistics.xlsx'

with pd.ExcelWriter(summary_file, engine='openpyxl') as writer:
    
    # Sheet 1: Corpus Overview
    corpus_overview = pd.DataFrame({
        'Metric': list(corpus_stats.keys()),
        'Value': list(corpus_stats.values())
    })
    corpus_overview.to_excel(writer, sheet_name='Corpus_Overview', index=False)
    print("  ✓ Exported: Corpus_Overview")
    
    # Sheet 2: Channel Statistics (with timezone fix)
    if 'channel_profile' in dir():
        # Select columns for export and make Excel-compatible
        channel_export_cols = ['channel_name', 'earliest_video_str', 'latest_video_str',
                              'activity_span_years', 'unique_videos', 'total_comments', 
                              'avg_likes_per_comment']
        # Only include columns that exist
        channel_export_cols = [c for c in channel_export_cols if c in channel_profile.columns]
        channel_export = channel_profile[channel_export_cols].copy()
        channel_export.to_excel(writer, sheet_name='Channel_Profile', index=False)
        print("  ✓ Exported: Channel_Profile")
    
    # Sheet 3: Missing Values
    missing_df.to_excel(writer, sheet_name='Missing_Values', index=False)
    print("  ✓ Exported: Missing_Values")
    
    # Sheet 4: Comment Length Stats
    if 'comment_word_count' in df.columns:
        length_summary = df['comment_word_count'].describe().reset_index()
        length_summary.columns = ['Statistic', 'Value']
        length_summary.to_excel(writer, sheet_name='Comment_Length', index=False)
        print("  ✓ Exported: Comment_Length")
    
    # Sheet 5: Top Words
    if 'top_words' in dir():
        top_words.to_excel(writer, sheet_name='Top_Words', index=False)
        print("  ✓ Exported: Top_Words")
    
    # Sheet 6: Yearly Counts
    if 'yearly_counts' in dir():
        yearly_df = yearly_counts.reset_index()
        yearly_df.columns = ['Year', 'Comment_Count']
        yearly_df.to_excel(writer, sheet_name='Yearly_Volume', index=False)
        print("  ✓ Exported: Yearly_Volume")
    
    # Sheet 7: Engagement Stats
    if available_engagement:
        engagement_stats.to_excel(writer, sheet_name='Engagement_Stats')
        print("  ✓ Exported: Engagement_Stats")
    
    # Sheet 8: Channel Engagement
    if 'channel_engagement' in dir():
        channel_engagement.to_excel(writer, sheet_name='Channel_Engagement')
        print("  ✓ Exported: Channel_Engagement")

print(f"\n✅ Summary statistics exported to: {summary_file}")


# ==============================================================================
# CELL 12: Final Summary & Completion
# ==============================================================================

print("\n" + "=" * 60)
print("EDA COMPLETE - SUMMARY")
print("=" * 60)

print(f"""
📊 CORPUS PROFILE
   • Total Comments: {len(df):,}
   • Unique Channels: {df['channel_name'].nunique() if 'channel_name' in df.columns else 'N/A'}
   • Unique Videos: {df['video_id'].nunique() if 'video_id' in df.columns else 'N/A'}
   • Date Range: {corpus_stats.get('Date Range Start', 'N/A')} to {corpus_stats.get('Date Range End', 'N/A')}

📁 OUTPUT FILES SAVED TO: {OUTPUT_DIR}
   • fig_comments_per_channel.png
   • fig_comments_per_category.png
   • fig_channel_activity_span.png
   • fig_video_tags_wordcloud.png
   • fig_comment_length_distribution.png
   • fig_top_words_comments.png
   • fig_comments_wordcloud.png
   • fig_comments_per_year.png
   • fig_comments_monthly_trend.png
   • fig_engagement_distribution.png
   • fig_engagement_by_channel.png
   • PhD_RQ1_EDA_Summary_Statistics.xlsx

⏱️ Execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

print("=" * 60)
print("✅ EDA Script Execution Complete")
print("=" * 60)
