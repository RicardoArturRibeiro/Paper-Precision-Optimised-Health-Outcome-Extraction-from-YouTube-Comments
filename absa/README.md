# Aspect-Based Sentiment Analysis (ABSA)

This folder contains materials for the ABSA validation component described in Phase 4 of the paper (Section 4.4).

## Overview

Two LLM models (GPT-4o and GPT-4.1) independently performed aspect-based sentiment analysis on a stratified sample of classified comments. This dual-model approach provides:

- Independent validation of aspect assignments
- Inter-rater reliability assessment between LLM annotators
- Granular sentiment polarity for each identified health aspect

## Files

| File | Description |
|------|-------------|
| `absa_colab.py` | Google Colab script for running the ABSA pipeline via OpenAI API |
| `absa_sample.csv` | Stratified sample of classified comments used as ABSA input |
| `absa_gpt_4o.jsonl` | GPT-4o ABSA output (aspect-sentiment pairs per comment) |
| `absa_gpt_4_1.jsonl` | GPT-4.1 ABSA output (aspect-sentiment pairs per comment) |

## Running the ABSA Pipeline

The script requires an OpenAI API key and is designed to run in Google Colab:

1. Upload `absa_sample.csv` to your Colab environment
2. Set your OpenAI API key as an environment variable
3. Run `absa_colab.py`

The script processes comments through the OpenAI API using structured prompts that identify health aspects and their associated sentiment polarity.

## Inter-Rater Reliability

| Comparison | Metric | Value | Interpretation |
|-----------|--------|-------|----------------|
| Human vs. GPT-4o | PABAK | 0.673 | Substantial |
| Human vs. GPT-4.1 | PABAK | 0.741 | Substantial |
| GPT-4o vs. GPT-4.1 | Cohen's κ | 0.771 | Substantial |
