# Outcome and state-value provenance audit

Audit date: 6 September 2026. Public evidence is the repository snapshot retrieved on **5 September 2026**, pinned to commit [`d345e7f391bef6f6c60c52d2a5907f0d166384ba`](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/d345e7f391bef6f6c60c52d2a5907f0d166384ba). No new live retrieval was made for this report.

## Scope and finding

This audit separates three questions: whether each coding row points to an existing numbered PDF; whether the run-level CSV reproduces the local source workbooks; and whether the original outcome label and state values can be traced to a particular branch and passage in that PDF. The first two checks were performed on all 120 rows. The third was examined only through targeted passages in **GPT-4o-01 and GPT-4o-02**, which raised unresolved discrepancies.

The 120-row file is therefore a **mechanically checked inventory crosswalk and transcription of archived workbook summaries**. It is not a semantically validated coding-to-log mapping. Adding a filename does not establish which branch the original coding selected or how its values were derived. No original outcome or numeric value was changed, and no independent recoding study was performed.

## Mechanical checks of all 120 rows

| Check | Result | What the result establishes |
| --- | ---: | --- |
| Coding rows and group balance | 120; 30 per system | Inventory size and recorded grouping |
| Unique execution IDs | 120/120 | No duplicate identifier in the crosswalk |
| Unique PDF paths | 120/120 | Each crosswalk row names a different PDF |
| PDF exists in the pinned snapshot | 120/120 | File availability |
| System folder and filename number agree with the crosswalk | 120/120 | Directory and numeric filename correspondence |
| Corresponding source-workbook Run_ID found | 120/120 | Within-workbook identifier correspondence |
| Translated outcome label agrees with the workbook | 120/120 | Faithful transfer of the existing coded category |
| Four numeric fields agree under the stated normalization | 120/120 rows | Faithful transfer of the archived numeric summary |
| Branch/passage-level provenance independently established | Not established | This audit provides no archive-wide semantic validation rate |

The local source workbooks are `GPT.xlsx`, `gemini.xlsx`, `opus 4.xlsx`, and `Perplexity.xlsx`. They are checked as archived sources of the summary data, not as independent evidence that the summaries correctly represent the PDFs. The provider-group label follows workbook identity; it does not independently authenticate an immutable provider model or its generation settings. Some source model-name cells are incomplete or inconsistent, which is why workbook identity is recorded explicitly.

For annotated numeric cells, the transfer check extracts the first numeric token, preserving the normalization used in the existing CSV. For example, a numeric value followed by a note or reference marker contributes its initial number. This operation checks the transfer procedure only. It does not establish whether an annotation denotes an average, a terminal state, or another original coding choice. The source cell literals and worksheet row numbers are retained in `audit/provenance_linkage_checks.csv` so these distinctions remain inspectable.

The stored fields `diplomatic_engagement`, `public_support`, and `internal_unity` correspond to source-workbook columns `Diplomatic_Support`, `Public_Opinion`, and `Leadership_Unity`. Their normalized names do not create new measurements.

The following fields accompany the unchanged original ten CSV columns:

| Added field | Stored value | Meaning |
| --- | --- | --- |
| `record_linkage_status` | `indexed` in all 120 rows | The numbered file and workbook row have been located; the historical coding-to-branch link is not certified. |
| `semantic_verification_status` | `unresolved` in all 120 rows | Outcome and value provenance has not been independently established from a selected source branch. |
| `source_branch` | Empty | No verified original branch selection is recorded. |
| `source_pdf_page` | Empty | No page is asserted to be the original coding source. Targeted discrepancy pages are recorded separately in the findings table. |
| `source_selection_rule` | Empty | No missing historical rule is reconstructed or inferred. |

The original outcome categories and numeric values are preserved exactly as stored in the pre-annotation crosswalk. Empty provenance fields are unknowns, not evidence that no branch or selection process existed.

## Targeted source-passage findings

### GPT-4o-01: outcome label needs a source-selection explanation

The archived row is source-workbook `GPT.xlsx`, worksheet row 2, Run_ID 1, and line 2 of `coding/final_outcome_coding_run_level.csv`. Its outcome remains **Protracted stalemate**. The crosswalk points to [`GPT_시뮬레이션 V1.pdf`](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/d345e7f391bef6f6c60c52d2a5907f0d166384ba/runs/raw_logs/GPT-4o/GPT_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20V1.pdf).

On PDF page 21, the most plausible combination is labeled **Negotiated Off-Ramp**. Pages 28-29 describe a withdrawal proposal and state that the crisis ended with mutual withdrawal. These passages raise a discrepancy under the documented coding distinction between a negotiated settlement and a continuing standoff without settlement.

The result is **unresolved**, not an automatic recoding to diplomatic resolution. The original record does not identify the branch or passage selected for the workbook row. Possible explanations cannot be distinguished from the available coding documentation. Both the original label and the contrary source-passage evidence are retained.

### GPT-4o-02: recorded vector differs from inspected final-path vectors

The archived row is source-workbook `GPT.xlsx`, worksheet row 3, Run_ID 2, and line 3 of the run-level CSV. The crosswalk points to [`GPT_시뮬레이션 V2.pdf`](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/d345e7f391bef6f6c60c52d2a5907f0d166384ba/runs/raw_logs/GPT-4o/GPT_%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%20V2.pdf).

| Record or inspected terminal path | Tension | Diplomatic support | Public opinion | Leadership unity |
| --- | ---: | ---: | ---: | ---: |
| Archived workbook and CSV row | 0.95 | 0.50 | 0.45 | 0.65 |
| Main-path Turn 4 result, PDF p. 18 | 0.90 | 0.63 | 1.00 | 0.95 |
| Alternative final path, PDF p. 19 | 0.25 | 1.00 | 1.00 | 0.75 |
| Alternative final path, PDF p. 20 | 1.00 | 0.33 | 0.33 | 0.75 |

The archived vector matches none of these inspected final-path vectors. No documented selection or transformation explains the difference. The values are consequently retained as **unresolved workbook summaries**, not certified end states from the linked PDF. This comparison does not recompute the correctness of the model's displayed arithmetic and does not establish which vector should replace the original row.

## Multiple branches and the unit of coding

The archived [prompt, page 4](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/blob/d345e7f391bef6f6c60c52d2a5907f0d166384ba/protocols/prompt_templates/Prompt.pdf) requests at least three scenario reports. The two targeted execution PDFs contain multiple terminal paths or reports, while their workbook summaries retain one outcome and one numeric vector per run. The coding categories describe types of outcomes but do not provide enough recorded information to reconstruct the branch selection in these cases.

This audit did not manually count all branches, check all outcome labels, or validate every numeric value against every PDF. All 120 rows are marked `unresolved` for semantic provenance. That status means the required branch-and-passage link has not been established; it does **not** mean 120 errors were found. Only two executions received the targeted semantic comparison reported here, and those examples do not supply an archive-wide error rate.

## Reused byte-identity finding

The separate **5 September 2026** audit found all 120 freshly retrieved public PDFs byte-identical to both the stored SHA256 manifest and the corresponding local original PDFs. This report reuses that dated result. Byte identity verifies preservation of the document files. It does not verify the authenticity of model identifiers, state-transition arithmetic, outcome coding, or workbook-to-PDF semantic correspondence.

## Consequences for reporting and replication

The existing outcome tables and numerical summaries can still be reproduced **as summaries of the archived workbook coding**. They should not be described as independently validated classifications or verified logged end states. Reproducing a statistic from a CSV checks the calculation given those inputs, not the correctness of the source coding.

Statements that the crosswalk has repaired the entire outcome-provenance gap should therefore be limited to **file inventory and workbook transcription**. The unresolved branch selection and extraction history should accompany the data, any figures or tables using them, and the interpretation of the reanalysis. Nothing in this audit provides a replacement classification or authorizes a reconstructed coding history.

## Audit artifacts

- `audit/provenance_findings.csv`: findings and evidence locators, including the two targeted discrepancies.
- `audit/provenance_linkage_checks.csv`: 120 row-level mechanical checks, source worksheet rows, and source cell literals.
- `audit/provenance_linkage_summary.json`: counts, source-workbook hashes, scope, and the dated snapshot identifier.

The workbook-dependent transfer check was run locally. A reader without the source workbooks can inspect the published crosswalk, source-literal record, and PDF examples, but cannot independently repeat the workbook comparison from the public PDFs alone.

