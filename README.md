LLM-based Pol-Mil Simulation Framework: Cuban Missile Crisis Case

This repository contains the dataset and simulation framework for the study: **"Deriving Strategic Scenarios through Political-Military Simulation Based on Large Language Models (LLMs) V2."** This research introduces a structured methodology to mitigate AI stochasticity and explore diverse strategic alternatives in crisis management.

##  Folder Structure

### 01_Simulation_Setup
- `soviet_gpt.json` / `us_gpt.json`: JSON-based actor profiles defining strategic stances, operational decision rules, and risk tolerances.
- `Variable-Decision Matrix.json`: A quantitative rule-set for calculating the impact of strategic actions on internal/external variables (Tension, Diplomatic Support, etc.).
- `Simulation_Protocol_English.pdf`: Comprehensive system prompts and step-by-step instructions for turn-based simulation.

### 02_Results_and_Logs
- `Raw_Logs/`: 120 independent execution logs generated across four state-of-the-art LLMs (GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet, and Perplexity Pro).
- `Consolidated_Simulation_Data.xlsx`: A master dataset containing tension scores, diplomatic metrics, and categorized scenario types for all 120 runs.
- `reproduce_chi_square.py`: Python script to reproduce the statistical validation (Chi-squared test) demonstrating model-specific scenario distributions (**$p < .001$**).
- `Statistical_Validation_Summary.docx`: A detailed report of the statistical findings, including contingency tables and effect sizes.

### 03_Expert_Validation
- `Survey_Form.pdf`: The validation questionnaire used for the expert evaluation. (Note: Primarily in Korean as it was conducted with regional security experts in South Korea.)
- `Expert_Responses_Anonymized.csv`: Anonymized raw dataset from 18 experts. Contains qualitative feedback and quantitative scores.
- `reproduce_expert_analysis.py`: Python script to process survey data and calculate descriptive statistics (Mean, SD).
- `Expert_Survey_Analysis_Report.docx`: Comprehensive summary of expert evaluations, confirming a high overall validity score (**3.96/5.0**).

##  Data Language Note
To ensure the authenticity and depth of specialized feedback, the **Expert Validation data (Folder 03)** is maintained in its original **Korean**. This data represents the insights of 18 regional security and military strategy experts from South Korea. For global accessibility, key findings and thematic qualitative summaries have been translated and incorporated into the main manuscript.

##  How to Reproduce
1. **Scenario Generation**: Load the JSON profiles from `01_Simulation_Setup` and follow the `Simulation_Protocol` using the supported LLMs.
2. **Data Validation**: Run `reproduce_chi_square.py` within the `02_Results_and_Logs` folder to verify the statistical significance of scenario branching.
3. **Expert Analysis**: Execute `reproduce_expert_analysis.py` in the `03_Expert_Validation` folder to replicate the qualitative and quantitative evaluation metrics.
