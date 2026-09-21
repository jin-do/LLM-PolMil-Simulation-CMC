# Fixed Top-1 input fields

Unit: one archived execution PDF, 120 unique `execution_id` values and 30 per system.

| Field | Meaning |
|---|---|
| execution_id / system | Preserved execution identifier and system label; not a modern model snapshot certification. |
| raw_log_path / source_pdf_sha256 | Repository-relative historical PDF path and expected SHA-256. |
| original_outcome | Retained pre-recoding outcome, not overwritten. |
| status | `confirmed` or `withheld`; fixed review status, not human certification. |
| outcome_5 | One of five terminal outcome categories when classified; empty when withheld. |
| recoding_changed | True only when classified and the revised category differs from original_outcome. |
| source_branch | Preserved selected branch identification, with the limits in RECODING_PROTOCOL.md. |
| selection_evidence / terminal_evidence | JSON lists of short excerpts and one-based PDF page numbers. |
| reasoning / limitations | Review rationale, including withholding reasons and unresolved source limitations. |
| common_state / actor_states / state_pages | Optional directly reported state records retained from source coding; not used in Table B1. No imputation or averaging. |

The source CSV uses UTF-8 with BOM. Results use UTF-8, LF and stable system/category order. Table B1 percentages use all 30/120 records including withheld and round half up to one decimal. The CLI rejects a missing roster before division, so zero denominators cannot be silently treated as zero percent.
