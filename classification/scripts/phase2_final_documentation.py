# ==============================================================================
# PhD Thesis RQ1 Phase 2: Script 6 - Final Ontology Documentation
# ==============================================================================
#
# Author: Ricardo Artur Silva Ribeiro
# PhD Program in Industrial Engineering and Management at NOVA FCT
#
# Purpose: 
# This script generates the final ontology documentation as a professional
# Word document (.docx) containing the complete validated ontology structure,
# methodology notes, and coverage statistics.
#
# AI Assistance Disclaimer:
# This script was developed with the assistance of Claude (Anthropic).
# All methodological decisions were made by the researcher.
#
# Date: 02 January 2026
# Phase 2, Script 6 of 6
#
# ==============================================================================


# ==============================================================================
# CELL 1: Environment Setup
# ==============================================================================

# Install required packages
!npm install -g docx 2>/dev/null
!pip install pandas numpy -q

import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

from google.colab import drive

print("=" * 70)
print("PhD RQ1 Phase 2: Ontology Development")
print("Script 6 - Final Ontology Documentation")
print("=" * 70)
print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ==============================================================================
# CELL 2: Configuration
# ==============================================================================

drive.mount('/content/drive')

OUTPUT_DIR = '/content/drive/MyDrive/PhD Thesis/PhD_ResearchQuestion_1/Phase2_Outputs/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load coverage data from Script 5
coverage_path = f'{OUTPUT_DIR}Phase2_Script5_refined_coverage.csv'
coverage_df = pd.read_csv(coverage_path)

print(f"\n📂 Output Directory: {OUTPUT_DIR}")
print(f"✅ Coverage data loaded: {len(coverage_df)} aspects")


# ==============================================================================
# CELL 3: Define Final Ontology Data
# ==============================================================================

print("\n" + "=" * 70)
print("1. PREPARING ONTOLOGY DATA")
print("=" * 70)

# Final validated ontology structure with all metadata
ONTOLOGY_DATA = {
    'RO1': {
        'name': 'Subjective Well-Being',
        'description': 'User-reported improvements in directly perceived, subjective states of metabolic health. These outcomes are self-assessed without external measurement tools.',
        'aspects': [
            {
                'id': 'RO1.1',
                'name': 'Cognitive Function',
                'definition': 'Changes in mental clarity, focus, concentration, and memory',
                'keywords': 'brain fog, mental clarity, focus, concentration, memory, cognitive, alert, clear headed, brain function, foggy, thinking clearly',
                'examples': 'brain fog lifted, better focus, clearer thinking, improved memory'
            },
            {
                'id': 'RO1.2',
                'name': 'Energy & Vitality',
                'definition': 'Changes in perceived energy levels, fatigue, and overall vitality',
                'keywords': 'energy, energetic, tired, fatigue, exhausted, lethargy, vitality, stamina, endurance, chronic fatigue',
                'examples': 'more energy, less tired, no longer fatigued, increased stamina'
            },
            {
                'id': 'RO1.3',
                'name': 'Psychological Well-Being',
                'definition': 'Changes in mood, anxiety, depression, and emotional state',
                'keywords': 'anxiety, depression, mood, stress, mental health, happy, calm, peaceful, irritable, wellbeing',
                'examples': 'less anxiety, improved mood, no longer depressed, feeling happier'
            },
            {
                'id': 'RO1.4',
                'name': 'Sleep Quality',
                'definition': 'Changes in sleep patterns, quality, and related conditions',
                'keywords': 'sleep, insomnia, restful, sleep quality, deep sleep, sleep apnea, snoring, refreshed',
                'examples': 'sleep better, no more insomnia, sleep through the night, off CPAP'
            },
            {
                'id': 'RO1.5',
                'name': 'Appetite & Satiety',
                'definition': 'Changes in hunger, cravings, and feeling of fullness',
                'keywords': 'appetite, hungry, hunger, craving, satiety, satiated, not hungry, sugar craving, binge, snacking',
                'examples': 'no more cravings, feel full, not hungry, sugar cravings gone'
            },
            {
                'id': 'RO1.6',
                'name': 'Pain & Inflammation',
                'definition': 'Changes in general pain, aches, inflammation, and headaches',
                'keywords': 'pain, ache, inflammation, joint pain, back pain, headache, migraine, stiff, swelling, chronic pain',
                'examples': 'pain free, no more headaches, inflammation reduced, joints feel better'
            },
            {
                'id': 'RO1.7',
                'name': 'Digestive Health',
                'definition': 'Changes in digestive function, bloating, and gastrointestinal comfort',
                'keywords': 'digestion, gut, bloating, gas, stomach, bowel, constipation, diarrhea, reflux, heartburn, gerd, nausea',
                'examples': 'no more bloating, better digestion, heartburn gone, regular bowels'
            },
            {
                'id': 'RO1.8',
                'name': 'Skin Health',
                'definition': 'Changes in skin appearance, conditions, and skin tags',
                'keywords': 'skin, skin tags, acne, eczema, psoriasis, rash, complexion, clear skin, rosacea, dermatitis',
                'examples': 'skin tags disappeared, acne cleared, skin glowing, eczema improved'
            },
            {
                'id': 'RO1.9',
                'name': 'Hormonal & Menstrual Health',
                'definition': 'Changes in hormonal balance, menstrual cycle, and menopausal symptoms',
                'keywords': 'hormone, period, menstrual, hot flash, menopause, pms, cycle, night sweats',
                'examples': 'regular periods, no hot flashes, hormones balanced, PMS improved'
            }
        ]
    },
    'RO2': {
        'name': 'Tool-Mediated Validation',
        'description': 'User-reported improvements in objectively measured health outcomes requiring measurement tools, tests, or medical equipment.',
        'aspects': [
            {
                'id': 'RO2.1',
                'name': 'Anthropometric Changes',
                'definition': 'Changes in weight, body composition, and physical measurements',
                'keywords': 'weight, lost weight, weight loss, pounds, lbs, kg, waist, bmi, body fat, fat loss, scale, dress size',
                'examples': 'lost 30 pounds, down 2 dress sizes, waist reduced, BMI normal'
            },
            {
                'id': 'RO2.2',
                'name': 'Glycemic Control',
                'definition': 'Changes in blood sugar, insulin levels, and related markers',
                'keywords': 'glucose, blood sugar, a1c, hba1c, fasting glucose, fasting insulin, insulin resistance, cgm, glucometer',
                'examples': 'A1C down to 5.4, blood sugar normal, insulin resistance improved'
            },
            {
                'id': 'RO2.3',
                'name': 'Blood Pressure',
                'definition': 'Changes in blood pressure readings',
                'keywords': 'blood pressure, bp, systolic, diastolic, pressure meds, pressure medication',
                'examples': 'blood pressure normalized, off BP meds, pressure down to 120/80'
            },
            {
                'id': 'RO2.4',
                'name': 'Lipid Profile',
                'definition': 'Changes in cholesterol, triglycerides, and related lipid markers',
                'keywords': 'cholesterol, triglycerides, hdl, ldl, lipid panel, total cholesterol, statin, apob',
                'examples': 'triglycerides dropped, HDL improved, off statins, cholesterol normalized'
            },
            {
                'id': 'RO2.5',
                'name': 'Inflammatory Markers',
                'definition': 'Changes in laboratory markers of inflammation',
                'keywords': 'crp, c-reactive, homocysteine, hs-crp, sed rate, esr, inflammation marker',
                'examples': 'CRP down, inflammation markers improved, homocysteine normalized'
            },
            {
                'id': 'RO2.6',
                'name': 'Liver Function',
                'definition': 'Changes in liver enzyme tests and liver health markers',
                'keywords': 'liver enzyme, ast, alt, ggt, bilirubin, liver function, liver test, liver panel',
                'examples': 'liver enzymes normal, ALT improved, liver function restored'
            },
            {
                'id': 'RO2.7',
                'name': 'Kidney Function',
                'definition': 'Changes in kidney function tests and markers',
                'keywords': 'gfr, egfr, creatinine, kidney function, renal function, bun, blood urea',
                'examples': 'GFR improved, creatinine down, kidney function better'
            },
            {
                'id': 'RO2.8',
                'name': 'Hormonal Markers',
                'definition': 'Changes in hormone blood test results',
                'keywords': 'tsh, t3, t4, testosterone, estrogen, cortisol, hormone level, hormone panel, thyroid panel',
                'examples': 'TSH normalized, testosterone improved, cortisol balanced'
            }
        ]
    },
    'RO3': {
        'name': 'Disease Specificity',
        'description': 'User-reported improvements or remission of specific, diagnosed metabolic-related diseases or chronic conditions.',
        'aspects': [
            {
                'id': 'RO3.1',
                'name': 'Type 2 Diabetes',
                'definition': 'Reports of diabetes reversal, remission, or management improvement',
                'keywords': 'diabetes, diabetic, type 2 diabetes, t2d, prediabetes, reversed diabetes, metformin',
                'examples': 'reversed my diabetes, off metformin, no longer diabetic, prediabetes gone'
            },
            {
                'id': 'RO3.2',
                'name': 'Fatty Liver Disease',
                'definition': 'Reports of fatty liver improvement or reversal',
                'keywords': 'fatty liver, nafld, nash, hepatic steatosis, liver fibrosis, cirrhosis, liver disease',
                'examples': 'fatty liver reversed, NAFLD gone, liver scan clear'
            },
            {
                'id': 'RO3.3',
                'name': 'Cardiovascular Disease',
                'definition': 'Reports related to heart disease, heart attacks, and cardiovascular conditions',
                'keywords': 'heart disease, heart attack, cardiovascular, coronary artery, heart failure, stent, bypass, atherosclerosis, angina',
                'examples': 'heart disease improved, plaque reduced, after heart attack recovery'
            },
            {
                'id': 'RO3.4',
                'name': 'Hypertension',
                'definition': 'Diagnosed high blood pressure as a condition',
                'keywords': 'hypertension, hypertensive',
                'examples': 'hypertension resolved, no longer hypertensive'
            },
            {
                'id': 'RO3.5',
                'name': 'PCOS',
                'definition': 'Polycystic Ovary Syndrome reports',
                'keywords': 'pcos, polycystic ovary, polycystic ovarian, ovarian cyst',
                'examples': 'PCOS symptoms improved, cysts reduced, cycles normalized'
            },
            {
                'id': 'RO3.6',
                'name': 'Neurodegenerative Disease',
                'definition': 'Reports related to Alzheimer\'s, dementia, and Parkinson\'s',
                'keywords': 'alzheimer, dementia, cognitive decline, parkinson, neurodegenerat',
                'examples': 'dementia symptoms improved, cognitive decline slowed'
            },
            {
                'id': 'RO3.7',
                'name': 'Chronic Kidney Disease',
                'definition': 'Diagnosed kidney disease reports',
                'keywords': 'kidney disease, ckd, chronic kidney, renal failure, dialysis, nephropathy',
                'examples': 'CKD stage improved, avoided dialysis, kidney disease reversed'
            },
            {
                'id': 'RO3.8',
                'name': 'Gout',
                'definition': 'Reports of gout and uric acid conditions',
                'keywords': 'gout, gouty, uric acid, gouty arthritis, gout attack',
                'examples': 'gout attacks stopped, uric acid normalized, no more gout flares'
            },
            {
                'id': 'RO3.9',
                'name': 'Cancer',
                'definition': 'Reports related to cancer prevention, treatment, or outcomes',
                'keywords': 'cancer, tumor, malignant, carcinoma, chemotherapy, oncology, metastasis',
                'examples': 'cancer in remission, tumor shrunk, cancer prevention'
            },
            {
                'id': 'RO3.10',
                'name': 'Osteoporosis',
                'definition': 'Reports of bone density and osteoporosis',
                'keywords': 'osteoporosis, osteopenia, bone density, bone mass, dexa scan, bone loss',
                'examples': 'bone density improved, osteopenia reversed, DEXA scan better'
            },
            {
                'id': 'RO3.11',
                'name': 'Stroke',
                'definition': 'Reports related to stroke history or recovery',
                'keywords': 'had a stroke, stroke survivor, stroke recovery, tia, mini stroke',
                'examples': 'stroke recovery, after my stroke, TIA prevention'
            },
            {
                'id': 'RO3.12',
                'name': 'ADHD',
                'definition': 'Reports of attention deficit hyperactivity disorder',
                'keywords': 'adhd, attention deficit, hyperactivity disorder, adderall, ritalin',
                'examples': 'ADHD symptoms reduced, off Adderall, better focus with ADHD'
            },
            {
                'id': 'RO3.13',
                'name': 'Thyroid Disease',
                'definition': 'Reports of thyroid conditions',
                'keywords': 'thyroid disease, hashimoto, hypothyroid, hyperthyroid, graves disease, levothyroxine',
                'examples': 'thyroid normalized, Hashimoto\'s improved, off thyroid medication'
            },
            {
                'id': 'RO3.14',
                'name': 'Inflammatory Bowel Disease',
                'definition': 'Reports of IBS, Crohn\'s, colitis, and related conditions',
                'keywords': 'ibs, irritable bowel, colitis, ulcerative colitis, crohn, ibd, sibo',
                'examples': 'IBS gone, Crohn\'s in remission, colitis improved'
            },
            {
                'id': 'RO3.15',
                'name': 'Autoimmune Disease',
                'definition': 'Reports of autoimmune conditions',
                'keywords': 'autoimmune, lupus, multiple sclerosis, rheumatoid arthritis, celiac, psoriatic arthritis',
                'examples': 'autoimmune symptoms reduced, lupus in remission, RA improved'
            },
            {
                'id': 'RO3.16',
                'name': 'Fibromyalgia & Neuropathy',
                'definition': 'Reports of fibromyalgia and nerve-related conditions',
                'keywords': 'fibromyalgia, neuropathy, nerve pain, peripheral neuropathy, numbness, tingling',
                'examples': 'fibromyalgia pain reduced, neuropathy improved, numbness gone'
            },
            {
                'id': 'RO3.17',
                'name': 'Arthritis',
                'definition': 'Reports of arthritis conditions',
                'keywords': 'arthritis, osteoarthritis, arthritic, joint disease',
                'examples': 'arthritis pain gone, joints improved, osteoarthritis better'
            },
            {
                'id': 'RO3.18',
                'name': 'Gallbladder Disease',
                'definition': 'Reports of gallbladder conditions',
                'keywords': 'gallbladder, gallstones, cholecystectomy, gallbladder attack',
                'examples': 'gallstones dissolved, gallbladder function improved'
            }
        ]
    }
}

print(f"✅ Ontology data prepared: 3 ROs, {sum(len(ro['aspects']) for ro in ONTOLOGY_DATA.values())} aspects")


# ==============================================================================
# CELL 4: Create Word Document
# ==============================================================================

print("\n" + "=" * 70)
print("2. GENERATING WORD DOCUMENT")
print("=" * 70)

# Merge coverage data with ontology
coverage_dict = {}
for _, row in coverage_df.iterrows():
    coverage_dict[row['aspect_id']] = {
        'count': int(row['match_count']),
        'percentage': float(row['match_percentage'])
    }

# Create JavaScript file for docx generation
js_code = '''
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel, 
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Coverage data from Python
const coverageData = ''' + json.dumps(coverage_dict) + ''';

// Ontology data
const ontologyData = ''' + json.dumps(ONTOLOGY_DATA) + ''';

// Border style for tables
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };
const headerShading = { fill: "1F4E79", type: ShadingType.CLEAR };
const altRowShading = { fill: "F2F2F2", type: ShadingType.CLEAR };

// Helper function to create a table row
function createTableRow(cells, isHeader = false, isAlt = false) {
    return new TableRow({
        tableHeader: isHeader,
        children: cells.map((cell, idx) => new TableCell({
            borders: cellBorders,
            width: { size: cell.width, type: WidthType.DXA },
            shading: isHeader ? headerShading : (isAlt ? altRowShading : undefined),
            children: [new Paragraph({
                alignment: cell.align || AlignmentType.LEFT,
                children: [new TextRun({ 
                    text: cell.text, 
                    bold: isHeader || cell.bold,
                    color: isHeader ? "FFFFFF" : "000000",
                    size: isHeader ? 22 : 20
                })]
            })]
        }))
    });
}

// Helper for multi-line cell content
function createMultiLineCell(lines, width, isAlt = false) {
    return new TableCell({
        borders: cellBorders,
        width: { size: width, type: WidthType.DXA },
        shading: isAlt ? altRowShading : undefined,
        children: lines.map(line => new Paragraph({
            children: [new TextRun({ text: line, size: 20 })]
        }))
    });
}

// Build document content
const children = [];

// Title
children.push(new Paragraph({
    heading: HeadingLevel.TITLE,
    children: [new TextRun({ text: "PhD Research Question 1", bold: true })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ 
        text: "Health Outcome Classification Ontology",
        size: 36,
        bold: true
    })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ 
        text: "Phase 2: Ontology Development - Final Documentation",
        size: 24,
        italics: true
    })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 600 },
    children: [new TextRun({ 
        text: "Ricardo Artur Silva Ribeiro",
        size: 24
    })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ 
        text: "PhD Program in Industrial Engineering and Management, NOVA FCT",
        size: 20
    })]
}));

children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 800 },
    children: [new TextRun({ 
        text: "Generated: ''' + datetime.now().strftime('%d %B %Y') + '''",
        size: 20,
        color: "666666"
    })]
}));

// Executive Summary
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("1. Executive Summary")]
}));

children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ 
        text: "This document presents the validated classification ontology for Research Question 1 (RQ1) of the PhD thesis investigating user-reported health outcomes in Healthcasting YouTube content. The ontology was developed through a systematic, iterative process combining expert domain knowledge with data-driven corpus analysis.",
        size: 22
    })]
}));

children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ 
        text: "The ontology comprises three Research Objectives (ROs) with 35 distinct aspects, designed to classify user comments reporting health improvements across subjective well-being, objective measurements, and disease-specific outcomes.",
        size: 22
    })]
}));

// Summary Statistics Table
children.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun("1.1 Coverage Summary")]
}));

const ro1Total = Object.entries(coverageData).filter(([k,v]) => k.startsWith('RO1')).reduce((a,b) => a + b[1].count, 0);
const ro2Total = Object.entries(coverageData).filter(([k,v]) => k.startsWith('RO2')).reduce((a,b) => a + b[1].count, 0);
const ro3Total = Object.entries(coverageData).filter(([k,v]) => k.startsWith('RO3')).reduce((a,b) => a + b[1].count, 0);

children.push(new Table({
    columnWidths: [4000, 2500, 2500],
    rows: [
        createTableRow([
            { text: "Research Objective", width: 4000, align: AlignmentType.LEFT },
            { text: "Aspects", width: 2500, align: AlignmentType.CENTER },
            { text: "Total Matches", width: 2500, align: AlignmentType.CENTER }
        ], true),
        createTableRow([
            { text: "RO1: Subjective Well-Being", width: 4000 },
            { text: "9", width: 2500, align: AlignmentType.CENTER },
            { text: ro1Total.toLocaleString(), width: 2500, align: AlignmentType.CENTER }
        ], false, true),
        createTableRow([
            { text: "RO2: Tool-Mediated Validation", width: 4000 },
            { text: "8", width: 2500, align: AlignmentType.CENTER },
            { text: ro2Total.toLocaleString(), width: 2500, align: AlignmentType.CENTER }
        ]),
        createTableRow([
            { text: "RO3: Disease Specificity", width: 4000 },
            { text: "18", width: 2500, align: AlignmentType.CENTER },
            { text: ro3Total.toLocaleString(), width: 2500, align: AlignmentType.CENTER }
        ], false, true),
        createTableRow([
            { text: "TOTAL", width: 4000, bold: true },
            { text: "35", width: 2500, align: AlignmentType.CENTER, bold: true },
            { text: (ro1Total + ro2Total + ro3Total).toLocaleString(), width: 2500, align: AlignmentType.CENTER, bold: true }
        ])
    ]
}));

// Methodology
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("2. Methodology")]
}));

children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ 
        text: "The ontology was developed through a six-phase iterative process:",
        size: 22
    })]
}));

const methodSteps = [
    "Phase 1: Corpus exploration and vocabulary analysis (Script 1)",
    "Phase 2: Unsupervised topic discovery using LDA (Script 2)",
    "Phase 3: N-gram extraction for multi-word health terms (Script 3)",
    "Phase 4: Initial ontology construction and coverage testing (Script 4)",
    "Phase 5: Refinement and false positive elimination (Script 5)",
    "Phase 6: Final documentation and validation (Script 6)"
];

methodSteps.forEach((step, idx) => {
    children.push(new Paragraph({
        spacing: { after: 100 },
        indent: { left: 720 },
        children: [new TextRun({ text: (idx + 1) + ". " + step, size: 22 })]
    }));
});

children.push(new Paragraph({
    spacing: { before: 200, after: 200 },
    children: [new TextRun({ 
        text: "Key refinements included implementing regex word boundaries for short keywords (e.g., \\\\bast\\\\b for liver enzyme AST) and removing ambiguous terms that caused false positives (e.g., 'ms' matching timestamps, 'add' matching the verb).",
        size: 22
    })]
}));

// RO1 Section
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("3. RO1: Subjective Well-Being")]
}));

children.push(new Paragraph({
    spacing: { after: 300 },
    children: [new TextRun({ 
        text: ontologyData.RO1.description,
        size: 22,
        italics: true
    })]
}));

// RO1 Aspects Table
ontologyData.RO1.aspects.forEach((aspect, idx) => {
    const coverage = coverageData[aspect.id] || { count: 0, percentage: 0 };
    
    children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun(aspect.id + ": " + aspect.name)]
    }));
    
    children.push(new Table({
        columnWidths: [2500, 6500],
        rows: [
            createTableRow([
                { text: "Definition", width: 2500, bold: true },
                { text: aspect.definition, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Keywords", width: 2500, bold: true },
                { text: aspect.keywords, width: 6500 }
            ]),
            createTableRow([
                { text: "Examples", width: 2500, bold: true },
                { text: aspect.examples, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Coverage", width: 2500, bold: true },
                { text: coverage.count.toLocaleString() + " matches (" + coverage.percentage.toFixed(2) + "%)", width: 6500 }
            ])
        ]
    }));
    
    children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
});

// RO2 Section
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("4. RO2: Tool-Mediated Validation")]
}));

children.push(new Paragraph({
    spacing: { after: 300 },
    children: [new TextRun({ 
        text: ontologyData.RO2.description,
        size: 22,
        italics: true
    })]
}));

// RO2 Aspects Table
ontologyData.RO2.aspects.forEach((aspect, idx) => {
    const coverage = coverageData[aspect.id] || { count: 0, percentage: 0 };
    
    children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun(aspect.id + ": " + aspect.name)]
    }));
    
    children.push(new Table({
        columnWidths: [2500, 6500],
        rows: [
            createTableRow([
                { text: "Definition", width: 2500, bold: true },
                { text: aspect.definition, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Keywords", width: 2500, bold: true },
                { text: aspect.keywords, width: 6500 }
            ]),
            createTableRow([
                { text: "Examples", width: 2500, bold: true },
                { text: aspect.examples, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Coverage", width: 2500, bold: true },
                { text: coverage.count.toLocaleString() + " matches (" + coverage.percentage.toFixed(2) + "%)", width: 6500 }
            ])
        ]
    }));
    
    children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
});

// RO3 Section
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("5. RO3: Disease Specificity")]
}));

children.push(new Paragraph({
    spacing: { after: 300 },
    children: [new TextRun({ 
        text: ontologyData.RO3.description,
        size: 22,
        italics: true
    })]
}));

// RO3 Aspects Table
ontologyData.RO3.aspects.forEach((aspect, idx) => {
    const coverage = coverageData[aspect.id] || { count: 0, percentage: 0 };
    
    children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun(aspect.id + ": " + aspect.name)]
    }));
    
    children.push(new Table({
        columnWidths: [2500, 6500],
        rows: [
            createTableRow([
                { text: "Definition", width: 2500, bold: true },
                { text: aspect.definition, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Keywords", width: 2500, bold: true },
                { text: aspect.keywords, width: 6500 }
            ]),
            createTableRow([
                { text: "Examples", width: 2500, bold: true },
                { text: aspect.examples, width: 6500 }
            ], false, true),
            createTableRow([
                { text: "Coverage", width: 2500, bold: true },
                { text: coverage.count.toLocaleString() + " matches (" + coverage.percentage.toFixed(2) + "%)", width: 6500 }
            ])
        ]
    }));
    
    children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
});

// AI Disclaimer
children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun("6. AI Assistance Disclaimer")]
}));

children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ 
        text: "This ontology was developed with the assistance of Claude (Anthropic), an AI assistant. Claude assisted with:",
        size: 22
    })]
}));

const aiTasks = [
    "Writing Python scripts for corpus analysis and keyword extraction",
    "Suggesting initial keyword lists based on corpus patterns",
    "Implementing regex patterns for word boundary matching",
    "Generating documentation and formatting outputs"
];

aiTasks.forEach(task => {
    children.push(new Paragraph({
        spacing: { after: 100 },
        indent: { left: 720 },
        children: [new TextRun({ text: "• " + task, size: 22 })]
    }));
});

children.push(new Paragraph({
    spacing: { before: 200, after: 200 },
    children: [new TextRun({ 
        text: "All methodological decisions, including the selection of Research Objectives, aspect definitions, and validation criteria, were made by the researcher. The AI served as a technical assistant for implementation tasks.",
        size: 22
    })]
}));

// Create Document
const doc = new Document({
    styles: {
        default: {
            document: {
                run: { font: "Arial", size: 22 }
            }
        },
        paragraphStyles: [
            {
                id: "Title",
                name: "Title",
                basedOn: "Normal",
                run: { size: 52, bold: true, color: "1F4E79", font: "Arial" },
                paragraph: { spacing: { before: 0, after: 120 }, alignment: AlignmentType.CENTER }
            },
            {
                id: "Heading1",
                name: "Heading 1",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 32, bold: true, color: "1F4E79", font: "Arial" },
                paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 }
            },
            {
                id: "Heading2",
                name: "Heading 2",
                basedOn: "Normal",
                next: "Normal",
                quickFormat: true,
                run: { size: 26, bold: true, color: "2E75B6", font: "Arial" },
                paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
            }
        ]
    },
    sections: [{
        properties: {
            page: {
                margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
            }
        },
        headers: {
            default: new Header({
                children: [new Paragraph({
                    alignment: AlignmentType.RIGHT,
                    children: [new TextRun({ 
                        text: "PhD RQ1 - Health Outcome Classification Ontology",
                        size: 18,
                        color: "666666"
                    })]
                })]
            })
        },
        footers: {
            default: new Footer({
                children: [new Paragraph({
                    alignment: AlignmentType.CENTER,
                    children: [
                        new TextRun({ text: "Page ", size: 18 }),
                        new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
                        new TextRun({ text: " of ", size: 18 }),
                        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 })
                    ]
                })]
            })
        },
        children: children
    }]
});

// Save document
Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("''' + OUTPUT_DIR + '''PhD_RQ1_Phase2_Ontology_Documentation.docx", buffer);
    console.log("Document created successfully!");
});
'''

# Write and execute JavaScript
with open('/tmp/create_ontology_doc.js', 'w') as f:
    f.write(js_code)

print("🔄 Generating Word document...")
!node /tmp/create_ontology_doc.js

print(f"✅ Document saved to: {OUTPUT_DIR}PhD_RQ1_Phase2_Ontology_Documentation.docx")


# ==============================================================================
# CELL 5: Summary Report
# ==============================================================================

print("\n" + "=" * 70)
print("3. FINAL SUMMARY")
print("=" * 70)

# Calculate totals
ro1_total = coverage_df[coverage_df['ro_id'] == 'RO1']['match_count'].sum()
ro2_total = coverage_df[coverage_df['ro_id'] == 'RO2']['match_count'].sum()
ro3_total = coverage_df[coverage_df['ro_id'] == 'RO3']['match_count'].sum()

print(f"""
PHASE 2 COMPLETE - ONTOLOGY DEVELOPMENT FINISHED
================================================

ONTOLOGY STRUCTURE
------------------
Research Objectives: 3
Total Aspects: 35
  • RO1 (Subjective Well-Being): 9 aspects
  • RO2 (Tool-Mediated Validation): 8 aspects  
  • RO3 (Disease Specificity): 18 aspects

COVERAGE STATISTICS
-------------------
RO1 Total Matches: {ro1_total:,}
RO2 Total Matches: {ro2_total:,}
RO3 Total Matches: {ro3_total:,}
Combined: {ro1_total + ro2_total + ro3_total:,}

DELIVERABLES
------------
1. PhD_RQ1_Phase2_Ontology_Documentation.docx (Final ontology document)
2. Phase2_Script5_final_ontology.csv (Machine-readable ontology)
3. Phase2_Script5_refined_coverage.csv (Coverage statistics)

NEXT STEPS (Phase 3)
--------------------
• Use ontology for aspect-based sentiment analysis
• Apply classification to full corpus
• Generate quantitative results for each Research Objective

AI ASSISTANCE DISCLAIMER
------------------------
This ontology was developed with the assistance of Claude (Anthropic).
All methodological decisions were made by the researcher.
""")

print("=" * 70)
print("✅ Phase 2 Script 6 Complete - Ontology Development Finished!")
print("=" * 70)
