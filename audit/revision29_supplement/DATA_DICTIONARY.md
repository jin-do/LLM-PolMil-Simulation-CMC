# Data dictionary and calculation rules

## Referenced repository inputs

`data/provenance.json` identifies three inputs by repository-relative path, source commit, immutable URL and digest:

- `top1`: the existing 120-row retrospective coding file. The original/new label comparison uses `execution_id`, `system`, `original_outcome`, `status`, `outcome_5` and `recoding_changed`; the source file retains its existing selection evidence, terminal passages and withholding reasons.
- `vdm`: the preserved VDM. Only `event_driven_adjustments` supplies coefficients to the conditional calculation. The documented normalization rule is to clip the complete sum to 0–1.
- `claude_01_pdf`: the preserved 34-page CLA-01 execution PDF. It is hash-checked, not automatically interpreted or extracted at runtime.

`sha256_bytes` means the file's exact bytes. `sha256_lf_normalized` means CRLF and lone CR line endings become LF before hashing; this only applies to the VDM. All hashes are input identity checks, not evidence that historical model calls used authenticated attachment versions.

## `conditional_cases.json`

| Field | Meaning |
|---|---|
| `variable_order` | Tension, Diplomatic_Support, Public_Opinion, Leadership_Unity, in that order for every vector. |
| `source_id` / `source_pdf_key` | CLA-01 and its input entry in `provenance.json`. |
| `case_id` | Unique execution/scenario/turn reference. |
| `table` | D2 for the three Scenario 1 checks; A2 for the separate Scenario 3 check. |
| `turn` / `scenario` | Recorded turn number and source scenario label. |
| `recorded_prior` | Four source-recorded starting values stored as decimal strings. No imputation or propagation of recalculated values. |
| `effect_names` | Full VDM rows invoked by name in the source. Each is conditionally applied once. No coefficient is copied into this input file. |
| `reported_result` | Four source-reported end values, without correction. |
| `prior_pages` / `effects_pages` / `reported_pages` | One-based PDF page positions for each kind of evidence. |
| `source_action_pair` | Action pair associated with the source's selected log. |
| `source_excerpt` | Short transcription of relevant named effects. Punctuation and whitespace are normalized for readability. The complete PDF is authoritative. |
| `limit` | Interpretation and calculation limits for that particular check. |

For component j, `unclipped[j] = recorded_prior[j] + sum(VDM[effect][j])`; `checked[j] = max(0, min(1, unclipped[j]))`. Decimal arithmetic avoids binary floating-point discrepancies. A component matches only if its checked value equals the reported value exactly. Formatting to two decimal places is for presentation, not a matching tolerance. A zero or one after clipping can conceal an omitted increment.

## `path_source_register.csv`

One row each covers the input display, Turns 1–4 and final account. `pdf_pages` lists one-based page positions; `observed_connection` describes the matching labels/actions; `recorded_state` is a transcription where a stage has a single relevant state; `limit` records the inference boundary. All rows refer to CLA-01's PDF in provenance. Blank states for the input display and final account mean no vector is asserted for that row.

The register records evidence for Table D1 and is copied to the output. It is not regenerated from the PDF or promoted to a machine-verified interpretation. Table D2 checks local arithmetic for three of its transitions.

## Table B2 and generated comparison fields

Category codes are S = protracted stalemate, D = diplomatic resolution, W = full-scale war, I = internal collapse, L = limited conflict, H = withheld. H is a review status, not a sixth crisis outcome. Rows use original categories and columns use retrospective categories/status. Every execution appears once. `same` and `different` compare classified labels only; withheld cases count in the matrix and total of 120 but not in the 104-classified difference denominator. The percentage is rounded half up to one decimal; a zero classified denominator remains undefined (`null`).

`outcome_label_comparison.csv` is derived at runtime, not a new coding input. `recoding_changed` is checked for consistency but does not supply the computed difference count. The original Top-1 selection, terminal-outcome rules and evidence remain in `coding/top1_reanalysis/RECODING_PROTOCOL.md` and its existing CSV.

## Provenance and scope

`prepared_date` dates this public supplement. `source_transcription` records the AI-assisted verification undertaken for packaging. It does not change the earlier analysis or the author's separately documented contextual judgments. `new_simulations` and `new_outcome_adjudication` are false. This module does not include respondent-level survey records or missing historical extraction windows.
