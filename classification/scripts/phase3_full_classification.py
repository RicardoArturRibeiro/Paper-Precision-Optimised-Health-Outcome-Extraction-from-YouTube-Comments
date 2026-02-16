# ==============================================================================
# PhD Thesis RQ1 Phase 3: Script 8 - Full Corpus Classification
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose:
# This script applies the validated outcome indicator framework to classify
# ALL 209,661 comments in the corpus. It identifies comments reporting
# definite positive health outcomes across all 35 aspects.
#
# Classification Categories:
# - positive_outcome: Definite positive health outcome reported
# - health_mention_no_outcome: Health topic mentioned but no clear outcome
# - excluded: Matches exclusion patterns (questions, intent, third-party, etc.)
# - no_health_content: No health-related content detected
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 3, Script 8 of 11
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup
# ==============================================================================

!pip install pandas numpy matplotlib seaborn tqdm -q

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from collections import defaultdict, Counter
from datetime import datetime
import warnings
from tqdm import tqdm

from google.colab import drive

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 300)

print("=" * 70)
print("PhD RQ1 Phase 3: Aspect Attribution")
print("Script 8 - Full Corpus Classification")
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
print(f"\n📊 Total comments in corpus: {len(df):,}")

# Display corpus info
print(f"\n📋 Columns available: {list(df.columns)}")
if 'channel_name' in df.columns:
    print(f"\n📺 Channels in corpus:")
    for channel, count in df['channel_name'].value_counts().items():
        print(f"   • {channel}: {count:,} comments")


# ==============================================================================
# CELL 4: Define Complete Ontology (from Phase 2)
# ==============================================================================

print("\n" + "=" * 70)
print("2. LOADING ONTOLOGY AND PATTERNS")
print("=" * 70)

# =============================================================================
# REFINED ONTOLOGY FROM PHASE 2 SCRIPT 5
# =============================================================================

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

print(f"✅ Ontology loaded: 3 ROs, 35 aspects")


# ==============================================================================
# CELL 5: Define Outcome Indicators (from Script 7)
# ==============================================================================

# =============================================================================
# DEFINITE POSITIVE OUTCOME PATTERNS
# =============================================================================

OUTCOME_INDICATORS = {
    'quantified_change': {
        'description': 'Specific numerical improvements reported',
        'patterns': [
            r'lost\s+\d+\s*(pound|lb|kg|kilo)',
            r'lost\s+(over|about|around|nearly)?\s*\d+\s*(pound|lb|kg|kilo)',
            r'down\s+\d+\s*(pound|lb|kg|kilo)',
            r'dropped\s+\d+\s*(pound|lb|kg|kilo)',
            r'shed\s+\d+\s*(pound|lb|kg|kilo)',
            r'\d+\s*(pound|lb|kg|kilo)\s*(lost|down|lighter)',
            r'a1c\s*(went|dropped|down|fell|came down|is now|now)\s*(from\s+\d+\.?\d*\s*(to|down to))?\s*\d+\.?\d*',
            r'a1c\s*(of|at|is|was)\s*\d+\.?\d*\s*(now|down from)',
            r'my\s+a1c\s+(is|was|went to|dropped to|came down to)\s+\d+\.?\d*',
            r'hba1c\s*(went|dropped|down|fell|is now)\s*\d+\.?\d*',
            r'blood\s+pressure\s*(went|dropped|down|is now|now)\s*(to|from)?\s*\d+',
            r'bp\s*(went|dropped|down|is now)\s*\d+',
            r'\d+\s*/\s*\d+\s*(now|down from|blood pressure)',
            r'blood\s+sugar\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'glucose\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'fasting\s+(blood\s+)?(sugar|glucose)\s*(of|at|is|was|down to)\s*\d+',
            r'(cholesterol|triglycerides?|ldl|hdl)\s*(went|dropped|down|is now)\s*(to|from)?\s*\d+',
            r'(cholesterol|triglycerides?)\s*(of|at)\s*\d+\s*(now|down)',
            r'went\s+from\s+\d+\s*(to|down to)\s+\d+',
            r'dropped\s+(from\s+)?\d+\s*(to|down to)\s+\d+',
        ]
    },
    'reversal_remission': {
        'description': 'Disease reversal or remission reported',
        'patterns': [
            r'reversed\s+(my|the)?\s*(type\s*2\s*)?(diabetes|diabetic|prediabetes)',
            r'reversed\s+(my|the)?\s*(fatty\s+liver|nafld|nash)',
            r'reversed\s+(my|the)?\s*(insulin\s+resistance)',
            r'reversed\s+(my|the)?\s*(pcos|polycystic)',
            r'reversed\s+(my|the)?\s*(metabolic\s+syndrome)',
            r'(diabetes|fatty\s+liver|insulin\s+resistance)\s*(is|was)?\s*reversed',
            r'no\s+longer\s+(diabetic|prediabetic|pre-diabetic)',
            r'no\s+longer\s+(have|had)\s+(diabetes|fatty\s+liver|high\s+blood\s+pressure|hypertension)',
            r'no\s+longer\s+(insulin\s+resistant|pre\s*diabetic)',
            r"(i'm|i\s+am|am)\s+no\s+longer\s+(diabetic|prediabetic)",
            r'not\s+(diabetic|prediabetic)\s+anymore',
            r'(diabetes|condition)\s+(is\s+)?gone',
            r'(in|into)\s+remission',
            r'(diabetes|crohn|colitis|ibs|autoimmune)\s*(is|in)\s*remission',
            r'cured\s+(my|the)?\s*(diabetes|fatty\s+liver|gout|ibs)',
            r'healed\s+(my|the)?\s*(gut|liver|body)',
        ]
    },
    'symptom_cessation': {
        'description': 'Symptoms stopped or disappeared',
        'patterns': [
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
            r'(pain|symptoms?|issues?)\s+(stopped|went\s+away|subsided)',
            r'(headaches?|migraines?)\s+(stopped|went\s+away)',
            r'(cravings?)\s+(stopped|went\s+away)',
            r'(pain|symptom)\s*-?\s*free',
            r'free\s+(of|from)\s+(pain|symptoms?|inflammation)',
            r'got\s+rid\s+of\s+(my\s+)?(pain|symptoms?|skin\s+tags?|acne)',
        ]
    },
    'medication_discontinuation': {
        'description': 'Stopped medications due to health improvement',
        'patterns': [
            r'off\s+(my\s+)?(metformin|insulin|statins?|lisinopril|medication|meds)',
            r'off\s+(my\s+)?(blood\s+pressure|bp|diabetes|cholesterol)\s*(meds|medication|pills)',
            r'off\s+(all\s+)?(my\s+)?medications?',
            r"(i'm|i\s+am|am)\s+off\s+(metformin|insulin|statins?|medications?)",
            r'stopped\s+taking\s+(metformin|insulin|statins?|medication|meds)',
            r'stopped\s+(my\s+)?(metformin|insulin|statins?)',
            r'no\s+longer\s+(take|taking|need|on)\s+(metformin|insulin|statins?|medication)',
            r"don't\s+(need|take)\s+(metformin|insulin|statins?|medication)\s*(anymore|any\s+more)",
            r'doctor\s+(took|taken)\s+me\s+off\s+(metformin|insulin|statins?|medication)',
            r'doctor\s+(reduced|lowered|cut)\s+(my\s+)?(metformin|insulin|medication)',
            r'(reduced|lowered|cut)\s+(my\s+)?(insulin|medication)\s+(dose|dosage|by)',
            r'weaned\s+off\s+(metformin|insulin|statins?|medication)',
            r'off\s+(cpap|blood\s+pressure\s+meds|bp\s+meds)',
            r"don't\s+need\s+(cpap|my\s+cpap)\s*(anymore|any\s+more)",
            r'no\s+longer\s+(use|need|on)\s+(cpap)',
        ]
    },
    'explicit_improvement': {
        'description': 'Explicit statements of personal health improvement',
        'patterns': [
            r'my\s+(a1c|blood\s+sugar|glucose|blood\s+pressure|bp)\s*(has\s+)?(improved|normalized|is\s+normal)',
            r'my\s+(cholesterol|triglycerides|ldl|hdl)\s*(has\s+)?(improved|normalized|is\s+normal)',
            r'my\s+(energy|sleep|mood|digestion)\s*(has\s+)?(improved|is\s+better)',
            r'my\s+(skin|joints|gut|liver)\s*(has\s+)?(improved|healed|is\s+better)',
            r'my\s+(inflammation|pain)\s*(has\s+)?(improved|reduced|is\s+better)',
            r'doctor\s*(was|is)?\s*(amazed|surprised|shocked|impressed)',
            r'doctor\s*(couldn\'t|could\s+not)\s+believe',
            r'doctor\s+said\s+(my|i)\s*(numbers?|results?|labs?)\s*(are|were|look)\s*(great|amazing|normal)',
            r'(best|lowest|healthiest)\s+(a1c|blood\s+sugar|blood\s+pressure|cholesterol|weight)\s*(in\s+years|ever|of\s+my\s+life)',
            r'(best|most)\s+(energy|sleep)\s*(in\s+years|ever|i\'ve\s+had)',
            r'feel\s+(better|healthier|amazing|great)\s+(than\s+ever|than\s+i\s+have\s+in\s+years|in\s+my\s+life)',
            r'never\s+felt\s+(better|healthier|this\s+good)',
            r'feel\s+like\s+a\s+new\s+(person|man|woman)',
            r'feel\s+\d+\s+years\s+younger',
            r'(this|it|keto|carnivore|fasting)\s+(changed|saved)\s+my\s+life',
            r'(life|game)\s*-?\s*changer',
            r'(completely|totally|fully)\s+(resolved|healed|gone|cured)',
            r'(100|hundred)\s*%?\s*(better|healed|resolved)',
        ]
    },
    'temporal_improvement': {
        'description': 'Improvement stated with temporal context',
        'patterns': [
            r'since\s+(starting|going|doing)\s+(keto|carnivore|low\s+carb|fasting).{0,50}(lost|improved|better|gone|no\s+more)',
            r'since\s+(i\s+)?started\s+(keto|carnivore|low\s+carb|fasting).{0,50}(lost|improved|better|gone|no\s+more)',
            r'since\s+(going|being)\s+(on\s+)?(keto|carnivore|low\s+carb).{0,50}(lost|improved|better|gone)',
            r'after\s+\d+\s*(week|month|day)s?\s*.{0,30}(lost|dropped|improved|reversed|gone|no\s+more)',
            r'(after|within)\s+\d+\s*(week|month|day)s?\s*(of\s+)?(keto|carnivore|fasting).{0,30}(lost|dropped|better)',
            r'\d+\s*(week|month|day)s?\s*(in|into|later).{0,30}(lost|dropped|improved|gone|no\s+more)',
            r'\d+\s*(week|month)s?\s+on\s+(keto|carnivore|this).{0,30}(lost|down|improved|better)',
            r'(now|today)\s+(my\s+)?(a1c|blood\s+sugar|bp|weight)\s+(is|at)\s+\d+',
            r'now\s+(i\s+)?(have|feel|am).{0,20}(more\s+energy|no\s+pain|no\s+more)',
        ]
    }
}

# =============================================================================
# EXCLUSION PATTERNS
# =============================================================================

EXCLUSION_PATTERNS = {
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
    'questions': {
        'description': 'Questions about health outcomes',
        'patterns': [
            r'\?\s*$',
            r'^(can|does|will|would|could|should|is|are|has|have|do|did)\s+(this|keto|carnivore|fasting|it)',
            r'^(how|what|why|when|where|which)\s+(do|does|can|will|should)',
            r'^(anyone|anybody|someone|has\s+anyone)\s+(lost|reversed|improved|tried)',
            r'^(is\s+it|are\s+there)\s+(possible|true|safe)',
            r'^(i\s+wonder|wondering)\s+(if|whether|about)',
        ]
    },
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

print(f"✅ Outcome indicators loaded: {len(OUTCOME_INDICATORS)} categories")
print(f"✅ Exclusion patterns loaded: {len(EXCLUSION_PATTERNS)} categories")


# ==============================================================================
# CELL 6: Classification Functions
# ==============================================================================

print("\n" + "=" * 70)
print("3. PREPARING CLASSIFICATION FUNCTIONS")
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
    """Return list of (aspect_id, aspect_name, ro_id) tuples that match the text."""
    if pd.isna(text) or not isinstance(text, str):
        return []

    text_lower = text.lower()
    matches = []

    for ro_id, ro in ONTOLOGY.items():
        for aspect_id, aspect in ro['aspects'].items():
            excluded = False
            for excl in aspect.get('exclusions', []):
                if check_keyword_match(text_lower, excl):
                    excluded = True
                    break

            if excluded:
                continue

            for keyword in aspect['keywords']:
                if check_keyword_match(text_lower, keyword):
                    matches.append((aspect_id, aspect['name'], ro_id))
                    break

    return matches

def check_outcome_indicators(text):
    """Check if text contains definite positive outcome indicators."""
    if pd.isna(text) or not isinstance(text, str):
        return {'has_outcome': False, 'categories': []}

    text_lower = text.lower()
    matched_categories = []

    for cat_name, cat_data in OUTCOME_INDICATORS.items():
        for pattern in cat_data['patterns']:
            try:
                if re.search(pattern, text_lower):
                    matched_categories.append(cat_name)
                    break
            except re.error:
                continue

    return {
        'has_outcome': len(matched_categories) > 0,
        'categories': matched_categories
    }

def check_exclusions(text):
    """Check if text matches any exclusion patterns."""
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

def classify_comment_full(text):
    """
    Full classification of a comment.
    Returns comprehensive classification result.
    """
    result = {
        'has_health_content': False,
        'aspect_matches': [],
        'ro_matches': [],
        'has_positive_outcome': False,
        'outcome_categories': [],
        'is_excluded': False,
        'exclusion_reasons': [],
        'classification': 'no_health_content'
    }

    if pd.isna(text) or not isinstance(text, str):
        return result

    # Step 1: Check for aspect matches
    aspect_matches = get_aspect_matches(text)
    if aspect_matches:
        result['has_health_content'] = True
        result['aspect_matches'] = [(a[0], a[1]) for a in aspect_matches]
        result['ro_matches'] = list(set([a[2] for a in aspect_matches]))

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

print("✅ Classification functions ready")


# ==============================================================================
# CELL 7: Run Full Corpus Classification
# ==============================================================================

print("\n" + "=" * 70)
print("4. CLASSIFYING FULL CORPUS")
print("=" * 70)

print(f"\n🔄 Processing {len(df):,} comments...")
print("   This may take several minutes...\n")

# Initialize result columns
df['classification'] = 'no_health_content'
df['has_positive_outcome'] = False
df['aspect_ids'] = ''
df['aspect_names'] = ''
df['ro_ids'] = ''
df['outcome_categories'] = ''
df['exclusion_reasons'] = ''

# Process in batches for progress tracking
batch_size = 10000
num_batches = (len(df) // batch_size) + 1

start_time = datetime.now()

for batch_num in tqdm(range(num_batches), desc="Processing batches"):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(df))

    for idx in range(start_idx, end_idx):
        text = df.iloc[idx]['comment_text']
        result = classify_comment_full(text)

        df.iloc[idx, df.columns.get_loc('classification')] = result['classification']
        df.iloc[idx, df.columns.get_loc('has_positive_outcome')] = result['has_positive_outcome']
        df.iloc[idx, df.columns.get_loc('aspect_ids')] = '; '.join([a[0] for a in result['aspect_matches']])
        df.iloc[idx, df.columns.get_loc('aspect_names')] = '; '.join([a[1] for a in result['aspect_matches']])
        df.iloc[idx, df.columns.get_loc('ro_ids')] = '; '.join(result['ro_matches'])
        df.iloc[idx, df.columns.get_loc('outcome_categories')] = '; '.join(result['outcome_categories'])
        df.iloc[idx, df.columns.get_loc('exclusion_reasons')] = '; '.join(result['exclusion_reasons'])

end_time = datetime.now()
processing_time = (end_time - start_time).total_seconds()

print(f"\n✅ Classification complete!")
print(f"   Processing time: {processing_time:.1f} seconds ({processing_time/60:.1f} minutes)")
print(f"   Rate: {len(df)/processing_time:.0f} comments/second")


# ==============================================================================
# CELL 8: Classification Summary Statistics
# ==============================================================================

print("\n" + "=" * 70)
print("5. CLASSIFICATION RESULTS SUMMARY")
print("=" * 70)

# Overall classification distribution
print("\n--- Overall Classification Distribution ---\n")
class_counts = df['classification'].value_counts()
for classification, count in class_counts.items():
    pct = count / len(df) * 100
    print(f"  {classification}: {count:,} ({pct:.2f}%)")

# Positive outcome statistics
positive_df = df[df['has_positive_outcome'] == True].copy()
print(f"\n📊 POSITIVE OUTCOMES: {len(positive_df):,} comments ({len(positive_df)/len(df)*100:.2f}%)")

# Outcome categories distribution
print("\n--- Outcome Categories Distribution ---\n")
category_counts = Counter()
for cats in positive_df['outcome_categories']:
    if cats:
        for cat in cats.split('; '):
            if cat:
                category_counts[cat] += 1

for cat, count in category_counts.most_common():
    pct = count / len(positive_df) * 100
    print(f"  {cat}: {count:,} ({pct:.1f}%)")


# ==============================================================================
# CELL 9: Research Objective Statistics
# ==============================================================================

print("\n" + "=" * 70)
print("6. RESEARCH OBJECTIVE STATISTICS")
print("=" * 70)

# Count positive outcomes by RO
ro_positive_counts = {'RO1': 0, 'RO2': 0, 'RO3': 0}
for ros in positive_df['ro_ids']:
    if ros:
        for ro in ros.split('; '):
            if ro in ro_positive_counts:
                ro_positive_counts[ro] += 1

print("\n--- Positive Outcomes by Research Objective ---\n")
for ro_id in ['RO1', 'RO2', 'RO3']:
    count = ro_positive_counts[ro_id]
    ro_name = ONTOLOGY[ro_id]['name']
    print(f"  {ro_id} ({ro_name}): {count:,} positive outcomes")


# ==============================================================================
# CELL 10: Aspect-Level Statistics
# ==============================================================================

print("\n" + "=" * 70)
print("7. ASPECT-LEVEL POSITIVE OUTCOME STATISTICS")
print("=" * 70)

# Count positive outcomes by aspect
aspect_positive_counts = defaultdict(int)
for aspects in positive_df['aspect_ids']:
    if aspects:
        for aspect in aspects.split('; '):
            if aspect:
                aspect_positive_counts[aspect] += 1

print("\n--- Positive Outcomes by Aspect ---\n")
print(f"{'Aspect':<10} {'Name':<35} {'Count':>10} {'% of Positive':>15}")
print("-" * 75)

for ro_id in ['RO1', 'RO2', 'RO3']:
    print(f"\n{ro_id}: {ONTOLOGY[ro_id]['name']}")
    aspects_sorted = sorted(
        [(aid, aspect_positive_counts.get(aid, 0)) for aid in ONTOLOGY[ro_id]['aspects'].keys()],
        key=lambda x: x[1],
        reverse=True
    )
    for aspect_id, count in aspects_sorted:
        aspect_name = ONTOLOGY[ro_id]['aspects'][aspect_id]['name']
        pct = count / len(positive_df) * 100 if len(positive_df) > 0 else 0
        print(f"  {aspect_id:<8} {aspect_name:<35} {count:>10,} {pct:>14.2f}%")


# ==============================================================================
# CELL 11: Channel-Level Statistics
# ==============================================================================

print("\n" + "=" * 70)
print("8. CHANNEL-LEVEL STATISTICS")
print("=" * 70)

if 'channel_name' in df.columns:
    print("\n--- Positive Outcomes by Channel ---\n")
    print(f"{'Channel':<30} {'Total':>12} {'Positive':>12} {'Rate':>10}")
    print("-" * 70)

    channel_stats = []
    for channel in df['channel_name'].unique():
        total = len(df[df['channel_name'] == channel])
        positive = len(positive_df[positive_df['channel_name'] == channel])
        rate = positive / total * 100 if total > 0 else 0
        channel_stats.append((channel, total, positive, rate))

    # Sort by positive count
    channel_stats.sort(key=lambda x: x[2], reverse=True)

    for channel, total, positive, rate in channel_stats:
        print(f"  {channel:<28} {total:>12,} {positive:>12,} {rate:>9.2f}%")


# ==============================================================================
# CELL 12: Export Complete Classified Dataset
# ==============================================================================

print("\n" + "=" * 70)
print("9. EXPORTING RESULTS")
print("=" * 70)

# Export 1: Full classified dataset
output_cols = ['comment_id', 'video_id', 'channel_name', 'comment_text',
               'classification', 'has_positive_outcome', 'aspect_ids',
               'aspect_names', 'ro_ids', 'outcome_categories', 'exclusion_reasons',
               'like_count', 'reply_count', 'published_at']

# Keep only columns that exist
export_cols = [col for col in output_cols if col in df.columns]
export_df = df[export_cols].copy()

export_df.to_csv(f'{OUTPUT_DIR}Phase3_Script8_full_classified_corpus.csv', index=False)
print(f"✅ Exported: Phase3_Script8_full_classified_corpus.csv ({len(export_df):,} rows)")

# Export 2: Positive outcomes only
positive_export = export_df[export_df['has_positive_outcome'] == True].copy()
positive_export.to_csv(f'{OUTPUT_DIR}Phase3_Script8_positive_outcomes.csv', index=False)
print(f"✅ Exported: Phase3_Script8_positive_outcomes.csv ({len(positive_export):,} rows)")

# Export 3: Summary statistics
summary_stats = {
    'total_comments': len(df),
    'positive_outcomes': len(positive_df),
    'positive_rate': len(positive_df) / len(df) * 100,
    'health_mentions': len(df[df['classification'] == 'health_mention_no_outcome']),
    'excluded': len(df[df['classification'] == 'excluded']),
    'no_health_content': len(df[df['classification'] == 'no_health_content'])
}

# Add RO counts
for ro_id in ['RO1', 'RO2', 'RO3']:
    summary_stats[f'{ro_id}_positive'] = ro_positive_counts[ro_id]

# Add aspect counts
for ro_id in ['RO1', 'RO2', 'RO3']:
    for aspect_id in ONTOLOGY[ro_id]['aspects'].keys():
        summary_stats[f'{aspect_id}_positive'] = aspect_positive_counts.get(aspect_id, 0)

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv(f'{OUTPUT_DIR}Phase3_Script8_summary_statistics.csv', index=False)
print(f"✅ Exported: Phase3_Script8_summary_statistics.csv")

# Export 4: Channel-level statistics
if 'channel_name' in df.columns:
    channel_df = pd.DataFrame(channel_stats, columns=['channel', 'total_comments', 'positive_outcomes', 'positive_rate'])
    channel_df.to_csv(f'{OUTPUT_DIR}Phase3_Script8_channel_statistics.csv', index=False)
    print(f"✅ Exported: Phase3_Script8_channel_statistics.csv")


# ==============================================================================
# CELL 13: Generate Visualizations
# ==============================================================================

print("\n" + "=" * 70)
print("10. GENERATING VISUALIZATIONS")
print("=" * 70)

# Figure 1: Classification Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Pie chart of classifications
ax1 = axes[0]
class_labels = ['Positive Outcome', 'Health Mention\n(no outcome)', 'Excluded', 'No Health Content']
class_values = [
    len(positive_df),
    len(df[df['classification'] == 'health_mention_no_outcome']),
    len(df[df['classification'] == 'excluded']),
    len(df[df['classification'] == 'no_health_content'])
]
colors = ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6']
ax1.pie(class_values, labels=class_labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Classification Distribution\n(Full Corpus)', fontsize=12, fontweight='bold')

# Bar chart of outcome categories
ax2 = axes[1]
if category_counts:
    cats = [cat.replace('_', ' ').title() for cat in category_counts.keys()]
    vals = list(category_counts.values())
    bars = ax2.barh(cats, vals, color='#2ecc71')
    ax2.set_xlabel('Number of Comments')
    ax2.set_title('Positive Outcomes by Category', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, vals):
        ax2.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
                f'{val:,}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}Phase3_Script8_classification_overview.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"✅ Saved: Phase3_Script8_classification_overview.png")

# Figure 2: Aspect-Level Positive Outcomes
fig, axes = plt.subplots(1, 3, figsize=(16, 8))

for idx, ro_id in enumerate(['RO1', 'RO2', 'RO3']):
    ax = axes[idx]

    aspects = list(ONTOLOGY[ro_id]['aspects'].keys())
    names = [ONTOLOGY[ro_id]['aspects'][a]['name'] for a in aspects]
    counts = [aspect_positive_counts.get(a, 0) for a in aspects]

    # Sort by count
    sorted_data = sorted(zip(names, counts), key=lambda x: x[1])
    names_sorted, counts_sorted = zip(*sorted_data) if sorted_data else ([], [])

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(names_sorted)))
    bars = ax.barh(names_sorted, counts_sorted, color=colors)

    ax.set_xlabel('Positive Outcomes', fontsize=10)
    ax.set_title(f"{ro_id}: {ONTOLOGY[ro_id]['name']}", fontsize=11, fontweight='bold')

    for bar, count in zip(bars, counts_sorted):
        if count > 0:
            ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                   f'{count:,}', va='center', fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}Phase3_Script8_positive_outcomes_by_aspect.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"✅ Saved: Phase3_Script8_positive_outcomes_by_aspect.png")


# ==============================================================================
# CELL 14: Final Summary Report
# ==============================================================================

print("\n" + "=" * 70)
print("11. FINAL SUMMARY REPORT")
print("=" * 70)
print(">>> COPY EVERYTHING BELOW THIS LINE AND PASTE TO CLAUDE <<<")
print("=" * 70)

print(f"""
PHASE 3 SCRIPT 8 - FULL CORPUS CLASSIFICATION RESULTS
=====================================================
Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Processing Time: {processing_time:.1f} seconds

1. CORPUS OVERVIEW
------------------
Total Comments Classified: {len(df):,}
Unique Channels: {df['channel_name'].nunique() if 'channel_name' in df.columns else 'N/A'}

2. CLASSIFICATION DISTRIBUTION
------------------------------""")

for classification, count in class_counts.items():
    pct = count / len(df) * 100
    print(f"  {classification}: {count:,} ({pct:.2f}%)")

print(f"""

3. POSITIVE OUTCOME STATISTICS
------------------------------
Total Positive Outcomes: {len(positive_df):,} ({len(positive_df)/len(df)*100:.2f}% of corpus)

By Research Objective:
  RO1 (Subjective Well-Being): {ro_positive_counts['RO1']:,}
  RO2 (Tool-Mediated Validation): {ro_positive_counts['RO2']:,}
  RO3 (Disease Specificity): {ro_positive_counts['RO3']:,}

By Outcome Category:""")

for cat, count in category_counts.most_common():
    print(f"  {cat}: {count:,}")

print(f"""

4. TOP 10 ASPECTS WITH POSITIVE OUTCOMES
----------------------------------------""")

top_aspects = sorted(aspect_positive_counts.items(), key=lambda x: x[1], reverse=True)[:10]
for aspect_id, count in top_aspects:
    # Find aspect name
    for ro_id in ONTOLOGY:
        if aspect_id in ONTOLOGY[ro_id]['aspects']:
            name = ONTOLOGY[ro_id]['aspects'][aspect_id]['name']
            break
    print(f"  {aspect_id} {name}: {count:,}")

print(f"""

5. CHANNEL STATISTICS (Top 5 by Positive Outcomes)
--------------------------------------------------""")

if 'channel_name' in df.columns:
    for channel, total, positive, rate in channel_stats[:5]:
        print(f"  {channel}: {positive:,} positive ({rate:.2f}%)")

print(f"""

6. FILES EXPORTED
-----------------
- Phase3_Script8_full_classified_corpus.csv ({len(export_df):,} rows)
- Phase3_Script8_positive_outcomes.csv ({len(positive_export):,} rows)
- Phase3_Script8_summary_statistics.csv
- Phase3_Script8_channel_statistics.csv
- Phase3_Script8_classification_overview.png
- Phase3_Script8_positive_outcomes_by_aspect.png

7. NEXT STEPS
-------------
1. Script 9: Validation sample extraction (500 random for manual coding)
2. Script 10: Detailed statistical analysis and confidence intervals
3. Script 11: ML validation (optional extension)

>>> END OF REPORT - COPY ABOVE THIS LINE <<<
""")

print("\n" + "=" * 70)
print("✅ Script 8 Complete - Full Corpus Classification Finished!")
print("=" * 70)
