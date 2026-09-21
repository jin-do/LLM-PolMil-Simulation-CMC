# Diagnostic fields and interpretation

`ai_review_40.csv` has 40 purpose-selected rows. The key is `case_id`; `original_check_id` links 38 HR rows to the common ledger. Two TRACE rows are separate representative examples. `run_id` identifies a PDF and is not unique across diagnostic items; repeated runs are intentional.

`domain`, `turn`, `question`, `original_rule`, `observed_output`, `judgment_reason` and `scope_limit` define what was checked and what remains unassessed. `checked_pages`, `source_url`, `source_sha256`, `source_mode` and `evidence_note` locate evidence and preserve review scope. `old_card_ai_status` and `comparison_note` record comparison to earlier AI cards. `reviewer_type` is AI; `human_reviewer`, `human_review_date`, `human_status` and `human_reason` are blank and stay blank.

C = demonstrated compliance with the particular requirement; V = demonstrated contradiction or omission of an applicable requirement; U = insufficient record or unclear applicability. No new NA judgment is assigned in this set. These are preserved AI judgments, not truth labels.

`membership.csv` explicitly records common-selected versus representative scope. `in_common_denominator=false` means do not append diagnostic rows as new common observations: the 38 underlying common IDs already exist there. `independent_sample=false` prohibits treating repeated observations as an independent validation sample.

`u_reason_assignments.csv` has exactly one principal explanatory reason for every U item. `dependency_group` is populated only for missing-response reasons and joins judgments sharing the same absent response. The five reason categories describe these 12 selected U items, not all common U observations.

`existing_change_links.csv` is a linkage table, not an executable amendment list. The three changes already exist in `data/adjudication/patches.json`. Their proposed labels must agree with current conservative labels. The diagnostic replay neither applies them again nor appends rows to the common ledger.

The fixed ledger's turn strings (for example `4` and `T4`) are preserved; auxiliary U-reason rows normalize them to numeric strings solely for grouping. Original/public byte hashes are recorded separately where documentation was sanitized.
