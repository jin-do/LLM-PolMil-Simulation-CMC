LLM-based Pol-Mil Simulation Framework: Cuban Missile Crisis Case

This repository contains the dataset, simulation setup, execution logs, quantitative summaries, statistical validation outputs, and expert validation materials for the study: **"Deriving Strategic Scenarios through Political-Military Simulation Based on Large Language Models (LLMs) V2."**

## Folder Structure

### 01_Simulation_setup

- `soviet_gpt.json` / `us_gpt.json`: JSON-based actor profiles defining strategic stances, decision rules, and risk tolerances.
- `Variable-Decision Matrix.json`: Variable-decision rules used to evaluate the impact of strategic actions.
- `Prompt.pdf`: Prompt material used for the simulation setup.
- `Simulation_Protocol_English.docx`: English simulation protocol and procedural instructions.

### 02_Results_and_Logs

- `Raw_Logs/`: Raw execution logs and source files from the model runs. The statistical validation uses the cleaned 30-run summary file for each of the four analyzed model groups in `Quantitative_Summaries/` (N = 120).
  - `ChatGPT/`: ChatGPT run logs.
  - `Claude/`: Claude run logs and source spreadsheets.
  - `Gemini/`: Gemini run logs and source spreadsheet.
  - `Perplexity/`: Perplexity run logs and source spreadsheet.
- `Quantitative_Summaries/`: Cleaned model-level summary spreadsheets used for statistical validation.
  - `GPT.xlsx`
  - `gemini.xlsx`
  - `opus 4.xlsx`
  - `Perplexity.xlsx`
- `statistical_validation/`: Chi-square validation script and generated statistical outputs.
  - `reproduce_chi_square.py`: Reproduces the scenario-type chi-square analysis from `Quantitative_Summaries/`.
  - `scenario_chi_square_summary.xlsx`: Reproduced contingency tables, row percentages, expected counts, data-quality checks, and chi-square results.
  - `Statistical_Validation_Summary_analyzed_files.docx`: Narrative statistical validation report.

### 03_Expert_validation

- `Survey_Form.pdf`: Expert validation questionnaire.
- `Expert_Responses.xlsx`: Expert response dataset used for validation analysis.
- `analysis/`: Expert validation analysis script and report.
  - `reproduce_expert_analysis.py`: Processes expert responses and calculates descriptive statistics.
  - `Expert_Survey_Analysis_Report.docx`: Expert validation report.

## Data Language Note

The expert validation data is maintained in its original Korean because the survey was conducted with regional security and military strategy experts in South Korea. Key findings and thematic summaries may be translated or summarized in the manuscript as needed.

## How to Reproduce

Python 3.10+ is recommended. The expert validation script requires `pandas`, `openpyxl`, and `python-docx`.

```powershell
python -m pip install -r requirements.txt
```

1. **Scenario setup**: Review the actor profiles, variable-decision matrix, prompt, and protocol in `01_Simulation_setup/`.
2. **Statistical validation**: Run `reproduce_chi_square.py` from `02_Results_and_Logs/statistical_validation/`.

   ```powershell
   cd .\02_Results_and_Logs\statistical_validation
   python .\reproduce_chi_square.py
   ```

   The script reads the four spreadsheets in `..\Quantitative_Summaries\` and writes `scenario_chi_square_summary.xlsx` in the current `statistical_validation/` folder.

3. **Expert validation**: Run `reproduce_expert_analysis.py` from `03_Expert_validation/analysis/`.

   ```powershell
   cd .\03_Expert_validation\analysis
   python .\reproduce_expert_analysis.py
   ```
