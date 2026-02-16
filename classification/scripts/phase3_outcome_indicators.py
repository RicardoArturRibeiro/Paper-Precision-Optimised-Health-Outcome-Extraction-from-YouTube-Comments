# ==============================================================================
# PhD Thesis RQ1 Phase 3: Script 7 - Outcome Indicator Development
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script develops the outcome indicator framework for classifying comments
# that report DEFINITE positive health outcomes. It combines the validated
# ontology from Phase 2 with outcome patterns to distinguish personal health
# testimonials from general discussion.
#
# Methodology:
# - Rule-based classification (transparent, reproducible)
# - Definite outcomes only (conservative, defensible)
# - Unit of analysis: unique comments
#
# Outputs:
# 1. Outcome indicator lexicon with patterns
# 2. Sample classifications for validation
# 3. Framework statistics
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 3, Script 7 of 11
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
from collections import defaultdict, Counter
from datetime import datetime
import warnings
import random

from google.colab import drive

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)

print("=" * 70)
print("PhD RQ1 Phase 3: Aspect Attribution")
print("Script 7 - Outcome Indicator Development")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("✅ All libraries loaded successfully.")


# ==============================================================================
# CELL 2: Configuration
# ==============================================================================

drive.mount('/content/drive')

CORPUS_PATH = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/PhD_RQ1_youtube_comments_corpus_final.csv'
OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase3_Outputs/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n📂 Corpus Path: {CORPUS_PATH}")
print(f"📁 Output Directory: {OUTPUT_DIR}")


# ==============================================================================
# CELL 3: Load Corpus
# ==============================================================================

print("\n" + "=" * 70)
print("1. LOADING CORPUS")
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
print(f"\nTotal comments in corpus: {len(df):,}")


# ==============================================================================
# CELL 4: Define Outcome Indicator Framework
# ==============================================================================

print("\n" + "=" * 70)
print("2. DEFINING OUTCOME INDICATOR FRAMEWORK")
print("=" * 70)

# =============================================================================
# DEFINITE POSITIVE OUTCOME PATTERNS
# These patterns indicate a user is reporting a personal, achieved health outcome
# =============================================================================

OUTCOME_INDICATORS = {
    # =========================================================================
    # Category 1: QUANTIFIED CHANGE
    # User reports specific numbers showing improvement
    # =========================================================================
    'quantified_change': {
        'description': 'Specific numerical improvements reported',
        'patterns': [
            # Weight loss with numbers
            r'lost\s+\d+\s*(pound|lb|kg|kilo)',
            r'lost\s+(over|about|around|nearly)?\s*\d+\s*(pound|lb|kg|kilo)',
            r'down\s+\d+\s*(pound|lb|kg|kilo)',
            r'dropped\s+\d+\s*(pound|lb|kg|kilo)',
            r'shed\s+\d+\s*(pound|lb|kg|kilo)',
            r'\d+\s*(pound|lb|kg|kilo)\s*(lost|down|lighter)',

            # A1C improvements
            r'a1c\s*(went|dropped|down|fell|came down|is now|now)\s*(from\s+\d+\.?\d*\s*(to|down to))?\s*\d+\.?\d*',
            r'a1c\s*(of|at|is|was)\s*\d+\.?\d*\s*(now|down from)',
            r'my\s+a1c\s+(is|was|went to|dropped to|came down to)\s+\d+\.?\d*',
            r'hba1c\s*(went|dropped|down|fell|is now)\s*\d+\.?\d*',

            # Blood pressure with numbers
            r'blood\s+pressure\s*(went|dropped|down|is now|now)\s*(to|from)?\s*\d+',
            r'bp\s*(went|dropped|down|is now)\s*\d+',
            r'\d+\s*/\s*\d+\s*(now|down from|blood pressure)',

            # Blood sugar numbers
            r'blood\s+sugar\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'glucose\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'fasting\s+(blood\s+)?(sugar|glucose)\s*(of|at|is|was|down to)\s*\d+',

            # Cholesterol/triglycerides with numbers
            r'(cholesterol|triglycerides?|ldl|hdl)\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'(cholesterol|triglycerides?)\s*(of|at)\s*\d+\s*(now|down)',

            # General quantified improvement
            r'went\s+from\s+\d+\s*(to|down to)\s+\d+',
            r'dropped\s+(from\s+)?\d+\s*(to|down to)\s+\d+',
        ]
    },

    # =========================================================================
    # Category 2: REVERSAL/REMISSION
    # User reports disease reversal or remission
    # =========================================================================
    'reversal_remission': {
        'description': 'Disease reversal or remission reported',
        'patterns': [
            # Reversed
            r'reversed\s+(my|the)?\s*(type\s*2\s*)?(diabetes|diabetic|prediabetes)',
            r'reversed\s+(my|the)?\s*(fatty\s+liver|nafld|nash)',
            r'reversed\s+(my|the)?\s*(insulin\s+resistance)',
            r'reversed\s+(my|the)?\s*(pcos|polycystic)',
            r'reversed\s+(my|the)?\s*(metabolic\s+syndrome)',
            r'(diabetes|fatty\s+liver|insulin\s+resistance)\s*(is|was)?\s*reversed',

            # No longer / not anymore
            r'no\s+longer\s+(diabetic|prediabetic|pre-diabetic)',
            r'no\s+longer\s+(have|had)\s+(diabetes|fatty\s+liver|high\s+blood\s+pressure|hypertension)',
            r'no\s+longer\s+(insulin\s+resistant|pre\s*diabetic)',
            r"(i'm|i\s+am|am)\s+no\s+longer\s+(diabetic|prediabetic)",
            r'not\s+(diabetic|prediabetic)\s+anymore',
            r'(diabetes|condition)\s+(is\s+)?gone',

            # Remission
            r'(in|into)\s+remission',
            r'(diabetes|crohn|colitis|ibs|autoimmune)\s*(is|in)\s*remission',

            # Cured/healed (careful - strong claim)
            r'cured\s+(my|the)?\s*(diabetes|fatty\s+liver|gout|ibs)',
            r'healed\s+(my|the)?\s*(gut|liver|body)',
        ]
    },

    # =========================================================================
    # Category 3: SYMPTOM CESSATION
    # User reports symptoms have stopped/disappeared
    # =========================================================================
    'symptom_cessation': {
        'description': 'Symptoms stopped or disappeared',
        'patterns': [
            # Gone/disappeared
            r'(pain|ache|aches)\s*(is|are|was|were)?\s*(gone|disappeared|vanished)',
            r'(headache|migraine)s?\s*(is|are|was|were)?\s*(gone|disappeared)',
            r'(brain\s+fog|brainfog)\s*(is|was)?\s*(gone|lifted|cleared|disappeared)',
            r'(inflammation|swelling)\s*(is|was)?\s*(gone|down|reduced|disappeared)',
            r'(bloating|gas)\s*(is|was)?\s*(gone|disappeared)',
            r'(skin\s+tag)s?\s*(is|are|was|were)?\s*(gone|disappeared|fell\s+off)',
            r'(acne|eczema|psoriasis|rash)\s*(is|was)?\s*(gone|cleared|disappeared)',
            r'(fatigue|tiredness)\s*(is|was)?\s*(gone|disappeared)',
            r'(anxiety|depression)\s*(is|was)?\s*(gone|lifted|improved|better)',
            r'(insomnia)\s*(is|was)?\s*(gone|cured)',
            r'(cravings?)\s*(is|are|was|were)?\s*(gone|disappeared|stopped)',
            r'(heartburn|reflux|gerd)\s*(is|was)?\s*(gone|disappeared|stopped)',
            r'(joint\s+pain|back\s+pain|knee\s+pain)\s*(is|was)?\s*(gone|disappeared)',

            # No more
            r'no\s+more\s+(pain|ache|aches|headache|migraine)',
            r'no\s+more\s+(brain\s+fog|brainfog|fog)',
            r'no\s+more\s+(inflammation|swelling)',
            r'no\s+more\s+(bloating|gas|stomach\s+issues)',
            r'no\s+more\s+(skin\s+tag|acne|rash)',
            r'no\s+more\s+(fatigue|tiredness|exhaustion)',
            r'no\s+more\s+(anxiety|depression|mood\s+swings)',
            r'no\s+more\s+(cravings?|hunger|snacking)',
            r'no\s+more\s+(heartburn|reflux|acid\s+reflux)',
            r'no\s+more\s+(joint\s+pain|back\s+pain|knee\s+pain)',
            r'no\s+more\s+(insomnia|sleep\s+problems)',
            r'no\s+more\s+(medications?|pills|drugs)',
            r'no\s+more\s+(insulin|metformin|statins?)',

            # Stopped/went away
            r'(pain|symptoms?|issues?)\s+(stopped|went\s+away|subsided)',
            r'(headaches?|migraines?)\s+(stopped|went\s+away)',
            r'(cravings?)\s+(stopped|went\s+away)',

            # Free of / rid of
            r'(pain|symptom)\s*-?\s*free',
            r'free\s+(of|from)\s+(pain|symptoms?|inflammation)',
            r'got\s+rid\s+of\s+(my\s+)?(pain|symptoms?|skin\s+tags?|acne)',
        ]
    },

    # =========================================================================
    # Category 4: MEDICATION DISCONTINUATION
    # User reports stopping medications due to improvement
    # =========================================================================
    'medication_discontinuation': {
        'description': 'Stopped medications due to health improvement',
        'patterns': [
            # Off medication
            r'off\s+(my\s+)?(metformin|insulin|statins?|lisinopril|medication|meds)',
            r'off\s+(my\s+)?(blood\s+pressure|bp|diabetes|cholesterol)\s*(meds|medication|pills)',
            r'off\s+(all\s+)?(my\s+)?medications?',
            r"(i'm|i\s+am|am)\s+off\s+(metformin|insulin|statins?|medications?)",

            # Stopped taking / no longer taking
            r'stopped\s+taking\s+(metformin|insulin|statins?|medication|meds)',
            r'stopped\s+(my\s+)?(metformin|insulin|statins?)',
            r'no\s+longer\s+(take|taking|need|on)\s+(metformin|insulin|statins?|medication)',
            r"don't\s+(need|take)\s+(metformin|insulin|statins?|medication)\s*(anymore|any\s+more)",

            # Doctor took off / reduced
            r'doctor\s+(took|taken)\s+me\s+off\s+(metformin|insulin|statins?|medication)',
            r'doctor\s+(reduced|lowered|cut)\s+(my\s+)?(metformin|insulin|medication)',
            r'(reduced|lowered|cut)\s+(my\s+)?(insulin|medication)\s+(dose|dosage|by)',

            # Weaned off
            r'weaned\s+off\s+(metformin|insulin|statins?|medication)',

            # Specific medications
            r'off\s+(cpap|blood\s+pressure\s+meds|bp\s+meds)',
            r"don't\s+need\s+(cpap|my\s+cpap)\s*(anymore|any\s+more)",
            r'no\s+longer\s+(use|need|on)\s+(cpap)',
        ]
    },

    # =========================================================================
    # Category 5: EXPLICIT IMPROVEMENT STATEMENTS
    # User explicitly states improvement with personal markers
    # =========================================================================
    'explicit_improvement': {
        'description': 'Explicit statements of personal health improvement',
        'patterns': [
            # My X improved/better/normalized
            r'my\s+(a1c|blood\s+sugar|glucose|blood\s+pressure|bp)\s*(has\s+)?(improved|normalized|is\s+normal)',
            r'my\s+(cholesterol|triglycerides|ldl|hdl)\s*(has\s+)?(improved|normalized|is\s+normal)',
            r'my\s+(energy|sleep|mood|digestion)\s*(has\s+)?(improved|is\s+better)',
            r'my\s+(skin|joints|gut|liver)\s*(has\s+)?(improved|healed|is\s+better)',
            r'my\s+(inflammation|pain)\s*(has\s+)?(improved|reduced|is\s+better)',

            # Doctor amazed/surprised
            r'doctor\s*(was|is)?\s*(amazed|surprised|shocked|impressed)',
            r'doctor\s*(couldn\'t|could\s+not)\s+believe',
            r'doctor\s+said\s+(my|i)\s*(numbers?|results?|labs?)\s*(are|were|look)\s*(great|amazing|normal)',

            # Best in years / best ever
            r'(best|lowest|healthiest)\s+(a1c|blood\s+sugar|blood\s+pressure|cholesterol|weight)\s*(in\s+years|ever|of\s+my\s+life)',
            r'(best|most)\s+(energy|sleep)\s*(in\s+years|ever|i\'ve\s+had)',

            # Feel better than ever
            r'feel\s+(better|healthier|amazing|great)\s+(than\s+ever|than\s+i\s+have\s+in\s+years|in\s+my\s+life)',
            r'never\s+felt\s+(better|healthier|this\s+good)',
            r'feel\s+like\s+a\s+new\s+(person|man|woman)',
            r'feel\s+\d+\s+years\s+younger',

            # Life changing
            r'(this|it|keto|carnivore|fasting)\s+(changed|saved)\s+my\s+life',
            r'(life|game)\s*-?\s*changer',

            # Completely/totally resolved
            r'(completely|totally|fully)\s+(resolved|healed|gone|cured)',
            r'(100|hundred)\s*%?\s*(better|healed|resolved)',
        ]
    },

    # =========================================================================
    # Category 6: TEMPORAL + STATE (Since/After + Positive State)
    # User reports positive state after starting intervention
    # =========================================================================
    'temporal_improvement': {
        'description': 'Improvement stated with temporal context',
        'patterns': [
            # Since starting + positive outcome
            r'since\s+(starting|going|doing)\s+(keto|carnivore|low\s+carb|fasting).{0,50}(lost|improved|better|gone|no\s+more)',
            r'since\s+(i\s+)?started\s+(keto|carnivore|low\s+carb|fasting).{0,50}(lost|improved|better|gone|no\s+more)',
            r'since\s+(going|being)\s+(on\s+)?(keto|carnivore|low\s+carb).{0,50}(lost|improved|better|gone)',

            # After X weeks/months + positive outcome
            r'after\s+\d+\s*(week|month|day)s?\s*.{0,30}(lost|dropped|improved|reversed|gone|no\s+more)',
            r'(after|within)\s+\d+\s*(week|month|day)s?\s*(of\s+)?(keto|carnivore|fasting).{0,30}(lost|dropped|better)',

            # X weeks/months in/later + positive outcome
            r'\d+\s*(week|month|day)s?\s*(in|into|later).{0,30}(lost|dropped|improved|gone|no\s+more)',
            r'\d+\s*(week|month)s?\s+on\s+(keto|carnivore|this).{0,30}(lost|down|improved|better)',

            # Now + positive state (with context)
            r'(now|today)\s+(my\s+)?(a1c|blood\s+sugar|bp|weight)\s+(is|at)\s+\d+',
            r'now\s+(i\s+)?(have|feel|am).{0,20}(more\s+energy|no\s+pain|no\s+more)',
        ]
    }
}

# Count patterns
total_patterns = sum(len(cat['patterns']) for cat in OUTCOME_INDICATORS.values())
print(f"\n✅ Defined {len(OUTCOME_INDICATORS)} outcome categories with {total_patterns} patterns:")
for cat_name, cat_data in OUTCOME_INDICATORS.items():
    print(f"   • {cat_name}: {len(cat_data['patterns'])} patterns - {cat_data['description']}")


# ==============================================================================
# CELL 5: Define Exclusion Patterns
# ==============================================================================

print("\n" + "=" * 70)
print("3. DEFINING EXCLUSION PATTERNS")
print("=" * 70)

# =============================================================================
# EXCLUSION PATTERNS
# These patterns indicate the comment is NOT a personal, achieved outcome
# =============================================================================

EXCLUSION_PATTERNS = {
    # =========================================================================
    # Category 1: FUTURE/INTENT (Not yet achieved)
    # =========================================================================
    'future_intent': {
        'description': 'Future plans or intentions, not achieved outcomes',
        'patterns': [
            r'^i\s+(want|need|hope|plan|wish|aim)\s+to\s+(lose|reverse|improve|lower)',
            r"^i'm\s+(trying|hoping|planning|wanting|looking)\s+to\s+(lose|reverse|improve)",
            r'^(trying|hoping|planning|wanting)\s+to\s+(lose|reverse|improve|lower)',
            r'^my\s+goal\s+is\s+to\s+(lose|reverse|improve)',
            r'^i\s+(will|shall|should|must|need\s+to)\s+(lose|reverse|start)',
            r'^(hopefully|maybe)\s+(i\s+)?(will|can)\s+(lose|reverse|improve)',
            r'^i\s+would\s+like\s+to\s+(lose|reverse|improve)',
            r"^let's\s+see\s+if",
            r'^i\s+started\s+(today|yesterday|this\s+week)(?!.{0,50}(lost|improved|reversed|gone))',
        ]
    },

    # =========================================================================
    # Category 2: QUESTIONS (Asking, not reporting)
    # =========================================================================
    'questions': {
        'description': 'Questions about health outcomes',
        'patterns': [
            r'\?\s*$',  # Ends with question mark
            r'^(can|does|will|would|could|should|is|are|has|have|do|did)\s+(this|keto|carnivore|fasting|it)',
            r'^(how|what|why|when|where|which)\s+(do|does|can|will|should)',
            r'^(anyone|anybody|someone|has\s+anyone)\s+(lost|reversed|improved|tried)',
            r'^(is\s+it|are\s+there)\s+(possible|true|safe)',
            r'^(i\s+wonder|wondering)\s+(if|whether|about)',
        ]
    },

    # =========================================================================
    # Category 3: NEGATION (Negative outcomes)
    # =========================================================================
    'negation': {
        'description': 'Negative or failed outcomes',
        'patterns': [
            r"(can't|cannot|couldn't|could\s+not)\s+(lose|reverse|improve|lower)",
            r"(didn't|did\s+not|haven't|have\s+not|hasn't)\s+(lose|lost|help|work|improve)",
            r"(don't|do\s+not|doesn't)\s+(work|help|believe)",
            r'(not|no)\s+(losing|reversing|improving|working)',
            r'(still|yet)\s+(have|has|had)\s+(diabetes|pain|symptoms)',
            r'(still|yet)\s+(diabetic|prediabetic|overweight)',
            r'(weight|pain|symptoms)\s+(came\s+back|returned|worse)',
            r'(gained|regained)\s+(weight|it\s+back)',
            r'(failed|failing)\s+to\s+(lose|reverse)',
            r"(didn't|did\s+not)\s+(see|notice|experience)\s+(any|much)\s+(change|improvement)",
            r'no\s+(change|improvement|difference|effect|results)',
            r'(worse|worsened|worsening)',
        ]
    },

    # =========================================================================
    # Category 4: THIRD PARTY (Not personal experience)
    # =========================================================================
    'third_party': {
        'description': 'Reports about others, not personal',
        'patterns': [
            r'^my\s+(husband|wife|mom|dad|mother|father|friend|brother|sister|son|daughter|partner)\s+(lost|reversed|improved)',
            r'^(he|she|they)\s+(lost|reversed|improved|has|have)',
            r"^my\s+(husband|wife|mom|dad|friend)'s\s+(a1c|diabetes|weight)",
            r'^(a\s+)?friend\s+(of\s+mine\s+)?(lost|reversed)',
            r'^someone\s+i\s+know\s+(lost|reversed)',
        ]
    },

    # =========================================================================
    # Category 5: GENERAL STATEMENTS (Not personal reports)
    # =========================================================================
    'general_statements': {
        'description': 'General statements about diets, not personal outcomes',
        'patterns': [
            r'^(keto|carnivore|fasting|low\s+carb)\s+(helps?|can|will|is\s+good\s+for)',
            r'^(this|it)\s+(helps?|works?|can)\s+(with|for)',
            r'^(studies|research|science)\s+(show|say|prove)',
            r'^(people|many|most)\s+(lose|reverse|improve)',
            r'^(you|one)\s+(can|will|should|could)\s+(lose|reverse)',
            r'^the\s+(best|key|secret)\s+(way\s+)?to\s+(lose|reverse)',
            r'^(losing|reversing)\s+(weight|diabetes)\s+(is|requires)',
        ]
    },

    # =========================================================================
    # Category 6: ENGAGEMENT ONLY (No outcome content)
    # =========================================================================
    'engagement_only': {
        'description': 'Generic engagement without outcome content',
        'patterns': [
            r'^(great|good|nice|awesome|excellent|amazing|wonderful)\s+(video|content|info|channel)',
            r'^(thanks?|thank\s+you)\s*(for|doc|dr|doctor)?',
            r'^(subscribed|liked|shared)',
            r'^(first|second|third)\s*(comment|here|one)',
            r'^(hello|hi|hey)\s*(everyone|all|there)?',
            r'^(love|loving)\s+(this|your)\s+(channel|video|content)',
        ]
    }
}

# Count exclusion patterns
total_exclusions = sum(len(cat['patterns']) for cat in EXCLUSION_PATTERNS.values())
print(f"\n✅ Defined {len(EXCLUSION_PATTERNS)} exclusion categories with {total_exclusions} patterns:")
for cat_name, cat_data in EXCLUSION_PATTERNS.items():
    print(f"   • {cat_name}: {len(cat_data['patterns'])} patterns - {cat_data['description']}")


# ==============================================================================
# CELL 6: Import Phase 2 Ontology (Refined)
# ==============================================================================

print("\n" + "=" * 70)
print("4. IMPORTING PHASE 2 ONTOLOGY")
print("=" * 70)

# Refined ontology from Phase 2 Script 5
ONTOLOGY = {
    'RO1': {
        'name': 'Subjective Well-Being',
        'aspects': {
            'RO1.1': {
                'name': 'Cognitive Function',
                'keywords': ['brain fog', 'brainfog', 'mental clarity', 'clarity', r'\bfocus\b', 'focused', 'concentration', 'memory', 'cognitive', r'\bsharp\b', r'\balert\b', 'clear headed', 'clearheaded', 'mental focus', 'brain function', r'\bfoggy\b', 'my brain', 'mental performance', 'thinking clearly'],
                'exclusions': ['alzheimer', 'dementia', 'neurodegenerat']
            },
            'RO1.2': {
                'name': 'Energy & Vitality',
                'keywords': [r'\benergy\b', 'energetic', 'energized', r'\btired\b', 'fatigue', 'fatigued', 'exhausted', 'exhaustion', 'lethargy', 'lethargic', 'vitality', r'\bvigor\b', 'stamina', 'endurance', 'more energy', 'no energy', 'energy level', 'full of energy', 'chronic fatigue'],
                'exclusions': []
            },
            'RO1.3': {
                'name': 'Psychological Well-Being',
                'keywords': ['anxiety', 'anxious', 'depression', 'depressed', r'\bmood\b', 'moods', r'\bstress\b', 'stressed', 'mental health', 'happier', r'\bhappy\b', r'\bcalm\b', 'peaceful', 'relaxed', 'irritable', 'irritability', 'emotional', 'well-being', 'wellbeing', r'\bpositive\b', 'outlook', 'hopeful'],
                'exclusions': ['adhd', r'\badd\b', 'attention deficit']
            },
            'RO1.4': {
                'name': 'Sleep Quality',
                'keywords': [r'\bsleep\b', 'sleeping', r'\bslept\b', 'insomnia', 'restful', 'sleep better', 'better sleep', 'sleep quality', 'waking up', 'wake up', 'deep sleep', 'sleep apnea', r'\bapnea\b', r'\bcpap\b', 'snoring', r'\bsnore\b', 'refreshed', 'sleep through'],
                'exclusions': []
            },
            'RO1.5': {
                'name': 'Appetite & Satiety',
                'keywords': ['appetite', r'\bhungry\b', r'\bhunger\b', 'craving', 'cravings', 'satiety', 'satiated', 'not hungry', 'never hungry', 'sugar craving', 'carb craving', 'food craving', r'\bbinge\b', 'binging', 'overeating', 'snacking', 'satisfied', 'feel full', 'feeling full'],
                'exclusions': []
            },
            'RO1.6': {
                'name': 'Pain & Inflammation',
                'keywords': [r'\bpain\b', r'\bache\b', r'\baches\b', 'aching', 'inflammation', 'inflammatory', 'joint pain', 'back pain', 'knee pain', 'chronic pain', 'body aches', r'\bstiff\b', 'stiffness', 'swelling', 'swollen', 'headache', 'headaches', 'migraine', 'migraines', 'soreness', r'\bsore\b', 'no more pain', 'pain free', 'pain-free'],
                'exclusions': ['arthritis', 'fibromyalgia', r'\bgout\b', 'rheumatoid']
            },
            'RO1.7': {
                'name': 'Digestive Health',
                'keywords': ['digest', 'digestion', 'digestive', r'\bgut\b', 'gut health', r'\bbloat\b', 'bloating', 'bloated', r'\bgas\b', 'stomach', r'\bbowel\b', 'constipation', 'constipated', 'diarrhea', 'reflux', 'acid reflux', 'heartburn', r'\bgerd\b', 'leaky gut', 'gut issues', 'indigestion', 'nausea', 'bowel movement'],
                'exclusions': [r'\bibs\b', 'irritable bowel', 'crohn', 'colitis', r'\bibd\b']
            },
            'RO1.8': {
                'name': 'Skin Health',
                'keywords': [r'\bskin\b', 'skin tag', 'skin tags', r'\bacne\b', 'eczema', 'psoriasis', r'\brash\b', 'rashes', 'complexion', 'clear skin', 'skin cleared', 'glowing', 'rosacea', 'hives', r'\bitchy\b', 'dry skin', 'oily skin', 'skin issue', 'skin problem', 'dermatitis', 'skin health'],
                'exclusions': ['lupus rash']
            },
            'RO1.9': {
                'name': 'Hormonal & Menstrual Health',
                'keywords': [r'\bhormone\b', 'hormones', 'hormonal', r'\bperiod\b', 'periods', 'menstrual', 'menstruation', 'hot flash', 'hot flashes', 'menopause', 'menopausal', 'perimenopause', r'\bpms\b', r'\bcycle\b', 'monthly cycle', 'night sweats', 'regular period', 'irregular period'],
                'exclusions': [r'\bpcos\b', 'polycystic']
            }
        }
    },
    'RO2': {
        'name': 'Tool-Mediated Validation',
        'aspects': {
            'RO2.1': {
                'name': 'Anthropometric Changes',
                'keywords': [r'\bweight\b', 'lost weight', 'lose weight', 'weight loss', 'losing weight', 'pounds', r'\blbs\b', r'\bkg\b', 'kilos', r'\bwaist\b', 'inches', r'\bbmi\b', 'body fat', 'fat loss', 'dropped', r'\bscale\b', 'dress size', 'pant size', r'\bbelt\b', 'clothing size', 'visceral fat', 'lean mass', 'body composition', 'lost 10', 'lost 20', 'lost 30', 'lost 50', 'lost 100'],
                'exclusions': []
            },
            'RO2.2': {
                'name': 'Glycemic Control',
                'keywords': ['glucose', 'blood sugar', 'blood glucose', r'\ba1c\b', 'hba1c', 'my a1c', 'fasting glucose', 'fasting insulin', r'\binsulin\b', 'insulin level', 'insulin resistance', 'insulin resistant', r'\bcgm\b', 'glucometer', 'blood test', 'sugar level', 'glucose level', 'sugar spike', 'stable blood sugar', 'normal blood sugar', 'blood sugar down'],
                'exclusions': ['diabetes', 'diabetic', 'type 2', 't2d', 'prediabetes']
            },
            'RO2.3': {
                'name': 'Blood Pressure',
                'keywords': ['blood pressure', r'\bbp\b', 'high blood pressure', 'systolic', 'diastolic', 'pressure reading', 'pressure meds', 'pressure medication', 'my blood pressure', 'pressure down', 'normalized bp', 'off bp meds', 'blood pressure is', 'blood pressure was'],
                'exclusions': ['hypertension']
            },
            'RO2.4': {
                'name': 'Lipid Profile',
                'keywords': ['cholesterol', 'triglycerides', 'triglyceride', 'trigs', r'\bhdl\b', r'\bldl\b', 'my ldl', 'my hdl', r'\blipid\b', 'lipids', 'lipid panel', 'total cholesterol', r'\bvldl\b', r'\bstatin\b', 'statins', 'off statins', 'cholesterol level', 'high cholesterol', 'lowered cholesterol', r'\bapob\b', 'apo b'],
                'exclusions': ['heart disease', 'heart attack', 'cardiovascular']
            },
            'RO2.5': {
                'name': 'Inflammatory Markers',
                'keywords': [r'\bcrp\b', 'c-reactive', 'c reactive', 'homocysteine', 'hs-crp', 'hscrp', 'sed rate', r'\besr\b', 'inflammation marker', 'inflammatory marker', 'systemic inflammation'],
                'exclusions': []
            },
            'RO2.6': {
                'name': 'Liver Function',
                'keywords': ['liver enzyme', r'\bast\b', r'\balt\b', r'\bggt\b', 'bilirubin', 'liver function', 'liver test', r'\blft\b', 'liver number', 'liver panel', 'my liver', 'liver health', 'liver enzymes', 'elevated liver', 'liver marker'],
                'exclusions': ['fatty liver', 'nafld', 'nash', 'cirrhosis', 'liver disease']
            },
            'RO2.7': {
                'name': 'Kidney Function',
                'keywords': [r'\bgfr\b', r'\begfr\b', 'creatinine', 'kidney function', 'renal function', r'\bbun\b', 'blood urea', 'kidney number', 'kidney test', 'my kidneys', 'kidney health'],
                'exclusions': ['kidney disease', 'ckd', 'renal failure', 'dialysis', 'kidney stone']
            },
            'RO2.8': {
                'name': 'Hormonal Markers',
                'keywords': [r'\btsh\b', r'\bt3\b', r'\bt4\b', 'free t3', 'free t4', 'testosterone', 'estrogen', 'progesterone', r'\bdhea\b', 'cortisol', 'hormone level', 'hormone panel', 'thyroid panel', 'hormones balanced', 'hormone test'],
                'exclusions': ['hashimoto', 'hypothyroid', 'hyperthyroid', 'graves', 'thyroid disease']
            }
        }
    },
    'RO3': {
        'name': 'Disease Specificity',
        'aspects': {
            'RO3.1': {'name': 'Type 2 Diabetes', 'keywords': ['diabetes', 'diabetic', 'type 2 diabetes', 't2d', 't2dm', 'prediabetes', 'prediabetic', 'pre-diabetic', 'pre diabetic', 'reversed diabetes', 'metformin', 'my diabetes', 'am diabetic', 'type two diabetes', 'diabetics'], 'exclusions': []},
            'RO3.2': {'name': 'Fatty Liver Disease', 'keywords': ['fatty liver', 'nafld', 'nash', 'non-alcoholic fatty liver', 'hepatic steatosis', 'liver fibrosis', 'cirrhosis', 'my fatty liver', 'liver disease', 'fatty liver disease'], 'exclusions': []},
            'RO3.3': {'name': 'Cardiovascular Disease', 'keywords': ['heart disease', 'heart attack', 'cardiovascular', r'\bcvd\b', 'coronary artery', 'coronary heart', r'\bcad\b', 'heart failure', 'congestive heart', r'\bchf\b', r'\bstent\b', 'bypass surgery', 'myocardial', 'atherosclerosis', 'plaque buildup', 'angina', 'cardiac', 'heart condition', 'heart problem'], 'exclusions': []},
            'RO3.4': {'name': 'Hypertension', 'keywords': ['hypertension', 'hypertensive', 'diagnosed with high blood pressure', 'have high blood pressure'], 'exclusions': []},
            'RO3.5': {'name': 'PCOS', 'keywords': [r'\bpcos\b', 'polycystic ovary', 'polycystic ovarian', 'polycystic ovary syndrome', 'ovarian cyst', 'cysts on ovaries', 'polycystic syndrome'], 'exclusions': []},
            'RO3.6': {'name': 'Neurodegenerative Disease', 'keywords': ['alzheimer', "alzheimer's", 'alzheimers', 'dementia', 'cognitive decline', 'parkinson', "parkinson's", 'parkinsons', 'neurodegenerat', "parkinson's disease", 'alzheimer disease'], 'exclusions': []},
            'RO3.7': {'name': 'Chronic Kidney Disease', 'keywords': ['kidney disease', r'\bckd\b', 'chronic kidney', 'renal failure', 'end stage renal', 'esrd', 'dialysis', 'nephropathy', 'stage 3 kidney', 'stage 4 kidney', 'stage 5 kidney', 'kidney failure'], 'exclusions': []},
            'RO3.8': {'name': 'Gout', 'keywords': [r'\bgout\b', 'gouty', 'uric acid', 'gouty arthritis', 'high uric acid', 'uric acid level', 'gout attack', 'gout flare'], 'exclusions': []},
            'RO3.9': {'name': 'Cancer', 'keywords': ['cancer', 'tumor', 'tumour', 'malignant', 'carcinoma', 'sarcoma', 'lymphoma', 'leukemia', 'metastasis', r'\bchemo\b', 'chemotherapy', 'oncology', 'breast cancer', 'colon cancer', 'prostate cancer', 'lung cancer', 'cancer cells', 'cancer diagnosis', 'cancer treatment'], 'exclusions': []},
            'RO3.10': {'name': 'Osteoporosis', 'keywords': ['osteoporosis', 'osteopenia', 'bone density', 'bone mass', 'dexa scan', 'bone scan', 'bone loss', 'bone health', 'brittle bones'], 'exclusions': []},
            'RO3.11': {'name': 'Stroke', 'keywords': ['had a stroke', 'stroke survivor', 'after stroke', 'stroke recovery', r'\btia\b', 'transient ischemic', 'cerebrovascular', r'\bcva\b', 'ischemic stroke', 'hemorrhagic stroke', 'mini stroke', 'stroke risk'], 'exclusions': []},
            'RO3.12': {'name': 'ADHD', 'keywords': [r'\badhd\b', 'attention deficit', 'attention-deficit', 'hyperactivity disorder', 'adderall', 'ritalin', 'vyvanse', 'attention deficit disorder'], 'exclusions': []},
            'RO3.13': {'name': 'Thyroid Disease', 'keywords': ['thyroid disease', 'hashimoto', "hashimoto's", 'hashimotos', 'hypothyroid', 'hypothyroidism', 'hyperthyroid', 'hyperthyroidism', 'graves disease', 'goiter', 'levothyroxine', 'synthroid', 'thyroid condition', 'thyroid problem', 'underactive thyroid', 'overactive thyroid'], 'exclusions': []},
            'RO3.14': {'name': 'Inflammatory Bowel Disease', 'keywords': [r'\bibs\b', 'irritable bowel', 'irritable bowel syndrome', 'colitis', 'ulcerative colitis', 'crohn', "crohn's", 'crohns', r'\bibd\b', 'inflammatory bowel disease', r'\bsibo\b', 'leaky gut syndrome', "crohn's disease"], 'exclusions': []},
            'RO3.15': {'name': 'Autoimmune Disease', 'keywords': ['autoimmune', 'auto immune', 'auto-immune', r'\blupus\b', 'multiple sclerosis', 'rheumatoid arthritis', 'rheumatoid', 'celiac', 'celiac disease', 'sjogren', 'psoriatic arthritis', 'autoimmune disease', 'autoimmune condition'], 'exclusions': []},
            'RO3.16': {'name': 'Fibromyalgia & Neuropathy', 'keywords': ['fibromyalgia', 'fibro', 'neuropathy', 'nerve pain', 'diabetic neuropathy', 'peripheral neuropathy', 'nerve damage', 'numbness', 'tingling', 'neuropathic pain'], 'exclusions': []},
            'RO3.17': {'name': 'Arthritis', 'keywords': ['arthritis', 'osteoarthritis', 'arthritic', 'joint disease', 'degenerative joint', 'my arthritis'], 'exclusions': []},
            'RO3.18': {'name': 'Gallbladder Disease', 'keywords': ['gallbladder', 'gall bladder', 'gallstones', 'gallstone', 'cholecystectomy', 'gallbladder removal', 'gallbladder attack', 'gallbladder disease'], 'exclusions': []}
        }
    }
}

total_aspects = sum(len(ro['aspects']) for ro in ONTOLOGY.values())
print(f"\n✅ Imported ontology: {len(ONTOLOGY)} ROs, {total_aspects} aspects")


# ==============================================================================
# CELL 7: Create Classification Functions
# ==============================================================================

print("\n" + "=" * 70)
print("5. CREATING CLASSIFICATION FUNCTIONS")
print("=" * 70)

def check_keyword_match(text, keyword):
    """Check if a keyword matches in the text (supports regex patterns)."""
    if pd.isna(text) or not isinstance(text, str):
        return False
    text_lower = text.lower()
    if keyword.startswith(r'\b') or r'\b' in keyword:
        try:
            return bool(re.search(keyword, text_lower))
        except re.error:
            return keyword.replace(r'\b', '') in text_lower
    else:
        return keyword in text_lower

def get_aspect_matches(text):
    """
    Return list of (aspect_id, aspect_name) tuples that match the text.
    """
    if pd.isna(text) or not isinstance(text, str):
        return []

    text_lower = text.lower()
    matches = []

    for ro_id, ro in ONTOLOGY.items():
        for aspect_id, aspect in ro['aspects'].items():
            # Check exclusions first
            excluded = False
            for excl in aspect.get('exclusions', []):
                if check_keyword_match(text_lower, excl):
                    excluded = True
                    break

            if excluded:
                continue

            # Check keywords
            for keyword in aspect['keywords']:
                if check_keyword_match(text_lower, keyword):
                    matches.append((aspect_id, aspect['name']))
                    break  # Only need one keyword match per aspect

    return matches

def check_outcome_indicators(text):
    """
    Check if text contains definite positive outcome indicators.
    Returns dict with matched categories and specific patterns.
    """
    if pd.isna(text) or not isinstance(text, str):
        return {'has_outcome': False, 'categories': [], 'matched_patterns': []}

    text_lower = text.lower()
    matched_categories = []
    matched_patterns = []

    for cat_name, cat_data in OUTCOME_INDICATORS.items():
        for pattern in cat_data['patterns']:
            try:
                if re.search(pattern, text_lower):
                    if cat_name not in matched_categories:
                        matched_categories.append(cat_name)
                    matched_patterns.append((cat_name, pattern))
                    break  # One match per category is enough
            except re.error:
                continue

    return {
        'has_outcome': len(matched_categories) > 0,
        'categories': matched_categories,
        'matched_patterns': matched_patterns
    }

def check_exclusions(text):
    """
    Check if text matches any exclusion patterns.
    Returns dict with matched exclusion categories.
    """
    if pd.isna(text) or not isinstance(text, str):
        return {'is_excluded': False, 'reasons': []}

    text_lower = text.lower()
    matched_reasons = []

    for cat_name, cat_data in EXCLUSION_PATTERNS.items():
        for pattern in cat_data['patterns']:
            try:
                if re.search(pattern, text_lower):
                    matched_reasons.append(cat_name)
                    break
            except re.error:
                continue

    return {
        'is_excluded': len(matched_reasons) > 0,
        'reasons': matched_reasons
    }

def classify_comment(text):
    """
    Full classification of a comment.
    Returns comprehensive classification result.
    """
    result = {
        'has_health_content': False,
        'aspect_matches': [],
        'has_positive_outcome': False,
        'outcome_categories': [],
        'is_excluded': False,
        'exclusion_reasons': [],
        'classification': 'no_health_content'
    }

    if pd.isna(text) or not isinstance(text, str):
        return result

    # Step 1: Check for aspect matches (health content)
    aspect_matches = get_aspect_matches(text)
    if aspect_matches:
        result['has_health_content'] = True
        result['aspect_matches'] = aspect_matches

    # Step 2: Check for outcome indicators
    outcome_check = check_outcome_indicators(text)
    if outcome_check['has_outcome']:
        result['outcome_categories'] = outcome_check['categories']

    # Step 3: Check exclusions
    exclusion_check = check_exclusions(text)
    if exclusion_check['is_excluded']:
        result['is_excluded'] = True
        result['exclusion_reasons'] = exclusion_check['reasons']

    # Step 4: Determine final classification
    if not result['has_health_content']:
        result['classification'] = 'no_health_content'
    elif result['is_excluded']:
        result['classification'] = 'excluded'
    elif outcome_check['has_outcome']:
        result['has_positive_outcome'] = True
        result['classification'] = 'positive_outcome'
    else:
        result['classification'] = 'health_mention_no_outcome'

    return result

print("✅ Classification functions created")


# ==============================================================================
# CELL 8: Test on Sample
# ==============================================================================

print("\n" + "=" * 70)
print("6. TESTING ON SAMPLE")
print("=" * 70)

# Test on random sample
sample_size = 5000
print(f"🔄 Testing classification on {sample_size:,} random comments...")

sample_df = df.sample(n=sample_size, random_state=42).copy()

# Classify each comment
classifications = []
for idx, row in sample_df.iterrows():
    result = classify_comment(row['comment_text'])
    result['comment_id'] = idx
    result['channel'] = row.get('channel_name', 'Unknown')
    result['text_preview'] = str(row['comment_text'])[:200] if pd.notna(row['comment_text']) else ''
    classifications.append(result)

# Convert to DataFrame
class_df = pd.DataFrame(classifications)

# Summary statistics
print(f"\n--- Classification Summary (n={sample_size:,}) ---\n")

classification_counts = class_df['classification'].value_counts()
for classification, count in classification_counts.items():
    pct = count / len(class_df) * 100
    print(f"  {classification}: {count:,} ({pct:.1f}%)")

# Outcome category breakdown
positive_df = class_df[class_df['classification'] == 'positive_outcome']
print(f"\n--- Positive Outcome Categories (n={len(positive_df):,}) ---\n")

category_counts = Counter()
for cats in positive_df['outcome_categories']:
    for cat in cats:
        category_counts[cat] += 1

for cat, count in category_counts.most_common():
    print(f"  {cat}: {count:,}")


# ==============================================================================
# CELL 9: Display Sample Positive Outcomes
# ==============================================================================

print("\n" + "=" * 70)
print("7. SAMPLE POSITIVE OUTCOMES FOR VALIDATION")
print("=" * 70)

# Show examples from each outcome category
print("\n📌 SAMPLE POSITIVE OUTCOME COMMENTS BY CATEGORY:\n")

for category in OUTCOME_INDICATORS.keys():
    cat_examples = positive_df[positive_df['outcome_categories'].apply(lambda x: category in x)]

    if len(cat_examples) > 0:
        print(f"\n{'='*60}")
        print(f"📋 {category.upper().replace('_', ' ')} ({len(cat_examples)} examples in sample)")
        print(f"{'='*60}")

        # Show 3 examples
        for i, (_, row) in enumerate(cat_examples.head(3).iterrows()):
            aspects = ', '.join([a[0] for a in row['aspect_matches'][:3]]) if row['aspect_matches'] else 'N/A'
            print(f"\n[{i+1}] Aspects: {aspects}")
            print(f"    {row['text_preview']}...")


# ==============================================================================
# CELL 10: Aspect-Level Positive Outcome Analysis
# ==============================================================================

print("\n" + "=" * 70)
print("8. ASPECT-LEVEL POSITIVE OUTCOME ANALYSIS")
print("=" * 70)

# Count positive outcomes by aspect
aspect_outcome_counts = defaultdict(int)
aspect_total_counts = defaultdict(int)

for _, row in class_df.iterrows():
    for aspect_id, aspect_name in row['aspect_matches']:
        aspect_total_counts[aspect_id] += 1
        if row['classification'] == 'positive_outcome':
            aspect_outcome_counts[aspect_id] += 1

print("\n--- Positive Outcomes by Aspect (from sample) ---\n")
print(f"{'Aspect':<10} {'Name':<35} {'Positive':>10} {'Total':>10} {'Rate':>10}")
print("-" * 80)

for ro_id in ['RO1', 'RO2', 'RO3']:
    print(f"\n{ro_id}: {ONTOLOGY[ro_id]['name']}")
    for aspect_id, aspect in ONTOLOGY[ro_id]['aspects'].items():
        total = aspect_total_counts.get(aspect_id, 0)
        positive = aspect_outcome_counts.get(aspect_id, 0)
        rate = (positive / total * 100) if total > 0 else 0
        print(f"  {aspect_id:<8} {aspect['name']:<35} {positive:>10,} {total:>10,} {rate:>9.1f}%")


# ==============================================================================
# CELL 11: Export Framework and Sample Results
# ==============================================================================

print("\n" + "=" * 70)
print("9. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Outcome indicators (for documentation)
indicators_export = []
for cat_name, cat_data in OUTCOME_INDICATORS.items():
    for pattern in cat_data['patterns']:
        indicators_export.append({
            'category': cat_name,
            'description': cat_data['description'],
            'pattern': pattern
        })
indicators_df = pd.DataFrame(indicators_export)
indicators_df.to_csv(f'{OUTPUT_DIR}Phase3_Script7_outcome_indicators.csv', index=False)
print(f"✅ Exported: Phase3_Script7_outcome_indicators.csv ({len(indicators_df)} patterns)")

# Export 2: Exclusion patterns
exclusions_export = []
for cat_name, cat_data in EXCLUSION_PATTERNS.items():
    for pattern in cat_data['patterns']:
        exclusions_export.append({
            'category': cat_name,
            'description': cat_data['description'],
            'pattern': pattern
        })
exclusions_df = pd.DataFrame(exclusions_export)
exclusions_df.to_csv(f'{OUTPUT_DIR}Phase3_Script7_exclusion_patterns.csv', index=False)
print(f"✅ Exported: Phase3_Script7_exclusion_patterns.csv ({len(exclusions_df)} patterns)")

# Export 3: Sample classifications (for manual validation)
sample_export = []
for _, row in class_df.iterrows():
    sample_export.append({
        'comment_id': row['comment_id'],
        'channel': row['channel'],
        'classification': row['classification'],
        'has_positive_outcome': row['has_positive_outcome'],
        'aspect_matches': '; '.join([f"{a[0]}" for a in row['aspect_matches']]),
        'outcome_categories': '; '.join(row['outcome_categories']),
        'exclusion_reasons': '; '.join(row['exclusion_reasons']),
        'text_preview': row['text_preview']
    })
sample_export_df = pd.DataFrame(sample_export)
sample_export_df.to_csv(f'{OUTPUT_DIR}Phase3_Script7_sample_classifications.csv', index=False)
print(f"✅ Exported: Phase3_Script7_sample_classifications.csv ({len(sample_export_df)} comments)")

# Export 4: Positive outcomes only (for easy review)
positive_export = sample_export_df[sample_export_df['has_positive_outcome'] == True].copy()
positive_export.to_csv(f'{OUTPUT_DIR}Phase3_Script7_positive_outcomes_sample.csv', index=False)
print(f"✅ Exported: Phase3_Script7_positive_outcomes_sample.csv ({len(positive_export)} positive outcomes)")


# ==============================================================================
# CELL 12: Summary Report
# ==============================================================================

print("\n" + "=" * 70)
print("10. SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 3 SCRIPT 7 - OUTCOME INDICATOR DEVELOPMENT RESULTS
=========================================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. FRAMEWORK SUMMARY
--------------------
Outcome Indicator Categories: {len(OUTCOME_INDICATORS)}
Total Outcome Patterns: {total_patterns}
Exclusion Categories: {len(EXCLUSION_PATTERNS)}
Total Exclusion Patterns: {total_exclusions}

2. OUTCOME INDICATOR CATEGORIES
-------------------------------""")

for cat_name, cat_data in OUTCOME_INDICATORS.items():
    print(f"  • {cat_name}: {len(cat_data['patterns'])} patterns - {cat_data['description']}")

print(f"""

3. SAMPLE CLASSIFICATION RESULTS (n={sample_size:,})
-------------------------------------------""")

for classification, count in classification_counts.items():
    pct = count / len(class_df) * 100
    print(f"  {classification}: {count:,} ({pct:.1f}%)")

print(f"""

4. POSITIVE OUTCOME CATEGORY BREAKDOWN
--------------------------------------""")

for cat, count in category_counts.most_common():
    print(f"  {cat}: {count:,}")

print(f"""

5. ESTIMATED CORPUS-WIDE PROJECTIONS
------------------------------------
Based on sample rate of {len(positive_df)/len(class_df)*100:.1f}% positive outcomes:
Estimated positive outcome comments: ~{int(len(df) * len(positive_df)/len(class_df)):,}
(out of {len(df):,} total comments)

6. FILES EXPORTED
-----------------
- Phase3_Script7_outcome_indicators.csv ({len(indicators_df)} patterns)
- Phase3_Script7_exclusion_patterns.csv ({len(exclusions_df)} patterns)
- Phase3_Script7_sample_classifications.csv ({len(sample_export_df)} comments)
- Phase3_Script7_positive_outcomes_sample.csv ({len(positive_export)} positive outcomes)

7. NEXT STEPS
-------------
1. Review Phase3_Script7_positive_outcomes_sample.csv for accuracy
2. Identify any false positives or missed patterns
3. Refine patterns if needed
4. Proceed to Script 8 for full corpus classification

8. VALIDATION RECOMMENDATION
----------------------------
Review at least 100 positive outcome examples manually to estimate:
- Precision (what % of flagged positives are truly positive?)
- Any patterns that need adjustment

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 7 Complete")
print("=" * 70)
