# File inventory and evidentiary roles

The original source archive is the public snapshot retrieved on 5 September 2026 at commit d345e7f391bef6f6c60c52d2a5907f0d166384ba. The inventory below distinguishes preserved source artifacts from derived coding, audit outputs, and documentation. Sizes are omitted because regenerated files can change without changing the original research records.

| Location | Contents | Evidentiary role |
| --- | --- | --- |
| runs/raw_logs/GPT-4o/ | 30 PDFs | Preserved archived conversations |
| runs/raw_logs/Gemini_2.5_Flash/ | 30 PDFs | Preserved archived conversations |
| runs/raw_logs/Claude_Opus_4/ | 30 PDFs | Preserved archived conversations |
| runs/raw_logs/Perplexity_RAG/ | 30 PDFs | Preserved archived conversations from a retrieval-augmented system group |
| actor_json/us_gpt.json, actor_json/soviet_gpt.json | Two actor-profile files | Preserved design inputs; historical and source-provenance caveats apply |
| vdm/Variable-Decision Matrix.json | State-effect and threshold definitions | Preserved design artifact, not an independent execution checker |
| vdm/action_to_vdm_mapping.md | Action-space notes | Supporting design documentation |
| protocols/Simulation_Protocol_English.docx, protocols/prompt_templates/Prompt.pdf | Original protocol and prompt | Preserved instructions; do not establish execution-by-execution configuration history |
| coding/final_outcome_coding.csv | 20-row aggregate table | Original aggregate coding |
| coding/final_outcome_coding_run_level.csv | 120 rows with indexed paths and unresolved provenance fields | Workbook-summary transcription and file index; not independent recoding |
| coding/coding_rules.md | Five category definitions and selection limitations | Meaning of existing labels; unresolved branch-selection history |
| coding/expert_survey_instrument.pdf, coding/expert_survey_aggregate.md | Questionnaire and aggregate note | Public survey material; individual responses are not included |
| analysis/reanalyze_outcomes.py | Executable coded-data analysis | Primary five-category analysis and three exploratory sensitivities |
| analysis/reproduce_audit.ipynb | Inspectable companion notebook | Recomputes the four permutation analyses and two bootstrap intervals; checks saved marker evidence and PDF hashes |
| analysis/reproduce_chi_square.py, analysis/statistical_analysis_script.py | Compatibility entry points | Both delegate to the current reanalysis; they no longer run the earlier hard-coded calculation |
| analysis/reanalysis_results.json, analysis/variable_summary.csv, analysis/outcome_tables.csv | Coded-data summaries and calculations | Derived outputs conditional on the archived coding |
| analysis/audit_traceability.py | Executable full-PDF marker search | Searches the complete text without prompt/output separation |
| analysis/traceability_log_audit.csv, analysis/traceability_audit_summary.json | Nine marker indicators and summary | Text-marker counts, definitions, hashes, and extraction information |
| analysis/traceability_marker_evidence.csv | Pattern-level page and snippet evidence | Supports the marker counts, not semantic validation |
| analysis/generate_figures.py, figures/ | Figure generation and resulting displays | Visualizations of archived coded records |
| audit/provenance_findings.csv | Mechanical checks and targeted discrepancies | Explicitly limited outcome/value provenance findings |
| audit/provenance_linkage_checks.csv, audit/provenance_linkage_summary.json | 120 row checks and scope metadata | Workbook transfer and file-number checks; all semantic statuses remain unresolved |
| docs/ | Dictionary, design, replication, provenance, input, and AHP notes | Interpretation and reproduction boundaries |

analysis/scenario_chi_square_summary.xlsx belongs to the earlier archive. Use the revised executable analysis and its JSON for current calculations; the older spreadsheet is not the authority for the new analysis. The two historical script names are retained as compatibility wrappers. The main entry points are reanalyze_outcomes.py and audit_traceability.py; optional notebook setup and its execution scope are described in [replication notes](replication_notes.md).

The index locates all 120 PDFs. The complete list of paths and source-workbook locators is in audit/provenance_linkage_checks.csv; the marker summary also records a hash for each inspected PDF. Byte preservation, row transcription, semantic source validation, and statistical calculation are different checks and should not be inferred from one another.
