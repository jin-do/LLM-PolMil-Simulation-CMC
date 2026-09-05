# Data dictionary

## Run-level coding table

[coding/final_outcome_coding_run_level.csv](../coding/final_outcome_coding_run_level.csv) contains 120 records, 30 per archived system group. One record reproduces one source-workbook summary with one outcome and four numeric values. It is not a record of every generated branch or an independently verified terminal state.

| Field | Meaning and limitation |
| --- | --- |
| execution_id | Identifier assigned for the archive index. Unique within this table; not an original provider execution identifier. |
| system | Archived group label: GPT-4o, Gemini 2.5 Flash, Claude Opus 4, or Perplexity Pro. Assignment follows workbook identity, not an independently authenticated model snapshot. |
| run_id | Within-workbook Run_ID, 1-30. It corresponds numerically to the indexed PDF filename; it does not demonstrate independence or correct branch selection. |
| raw_log_path | Relative path to an existing archived PDF under runs/raw_logs/. A file locator, not a semantic validation claim. |
| final_outcome_5 | Existing workbook-coded category: Protracted stalemate, Internal collapse, Diplomatic resolution, Full-scale war, or Limited conflict. No category was recoded in this revision. |
| final_outcome_3 | Exploratory aggregation: Stalemate, Diplomatic resolution, or Adverse non-diplomatic outcome. The last combines Internal collapse, Full-scale war, and Limited conflict. |
| tension | Numeric summary transferred from source-workbook Tension; stored in the range 0-1. Its original branch and extraction basis remain unresolved. |
| diplomatic_engagement | Storage alias for source-workbook Diplomatic_Support; displayed as Diplomatic support. This alias does not change the construct or validate the value. |
| public_support | Storage alias for source-workbook Public_Opinion; displayed as Public opinion. |
| internal_unity | Storage alias for source-workbook Leadership_Unity; displayed as Leadership unity. |
| record_linkage_status | indexed for all 120 rows: the numbered workbook row and PDF file were located. Indexed does not mean validated. |
| semantic_verification_status | unresolved for all 120 rows: the historical link to a selected branch and source passage has not been independently established. This is not a claim that all 120 records are erroneous. |
| source_branch | Empty because a verified original branch selection is unavailable. |
| source_pdf_page | Empty because the original coding source page has not been established. Pages used to demonstrate discrepancies are recorded separately in the provenance findings. |
| source_selection_rule | Empty because no missing historical selection rule is inferred or reconstructed. |

The original ten data columns are preserved. Annotated source-workbook numeric cells were transferred using their first numeric token, following the existing normalization. Source literals and worksheet row numbers are recorded in [audit/provenance_linkage_checks.csv](../audit/provenance_linkage_checks.csv). Successful transfer does not explain whether an original value was an average, a selected branch state, or another kind of summary.

## Aggregate and derived files

- coding/final_outcome_coding.csv: original 20-row aggregate coded-outcome table. condition names the archived group, final_outcome its coded category, and count the recorded frequency. It cannot identify the original branch behind an outcome.
- analysis/outcome_tables.csv: tabular display of the archived outcome counts and their aggregation.
- analysis/variable_summary.csv: arithmetic means and sample SDs (ddof=1) computed from the workbook-derived numbers. These are descriptive summaries of unresolved coded records.
- analysis/reanalysis_results.json: outcome counts, Pearson discrepancy statistics, Cramer's V, conditional permutation reference quantities, and aggregated-table resampling intervals; metadata records assumptions and input identity.

## Document-marker outputs

analysis/traceability_log_audit.csv contains one row per PDF and nine marker indicators. All searches cover the full document, including prompts. readable_text means at least 500 normalized extracted characters; it is not a human assessment of readability. variable_status_label uses a generic label pattern, whereas explicit_reconfirm_variable_status requires the stricter reconfirmation phrase. metadata_labels_present requires all five label-pattern groups somewhere in the document, not verified metadata values. independent_checker_phrase records a phrase match, not an independent validation record.

analysis/traceability_marker_evidence.csv records component patterns, counts, all hit page numbers, and a first-match representative snippet. analysis/traceability_audit_summary.json records scope, input PDF hashes, extraction/cache information, and denominators. See [replication notes](replication_notes.md) and the [provenance audit](provenance_audit.md) for the distinctions between marker presence, file linkage, and semantic validation.
