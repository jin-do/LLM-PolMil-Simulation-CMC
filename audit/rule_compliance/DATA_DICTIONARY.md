# Data dictionary and denominator rules

The inherited field dictionary is in `protocol/DATA_DICTIONARY.md`. The original core CSV contains one row per `check_id`; the common frame is selected by the eleven `metric_key` values in `protocol/analysis_spec.json`, not by file length or free-text domain labels.

| Field or output | Meaning |
|---|---|
| check_id | Stable observation identifier; duplicates or missing grid cells are errors. |
| run_id | CLA/GEM/GPT/PER-01 through -30; 120 runs. |
| metric_key / turn | T1_US_ROLE, T1_SU_ROLE; T2–T4_BRANCH, EVENT and PARENT_COVERAGE. Turn must agree. |
| status | C=준수, V=위반, U=판정 불가, NA=적용 대상 아님. |
| source_file, page, evidence | Public repository source alias, original page locator and retained text. Old extraction-file references are archival provenance, not runtime dependencies. |
| review_completed | Recorded assessment completed; does not mean a human completed it. |
| candidate_only | Extraction candidate; excluded from official partial-review rates. |
| assessability_denominator | C+V+U; assessment unit depends on the domain. |
| compliance_denominator | C+V; conditionally assessable observations. |
| assessable_percent | 100×(C+V)/(C+V+U). |
| conditional_compliance_percent | 100×C/(C+V). Undefined when C+V=0; blank rather than zero. |
| legacy_status_before_amendment | Original fixed label before a documented patch. |
| criteria_review_id | Link to focused AI decision entry. |
| original/public SHA-256 | Separate identities for source bytes and locator-transformed public copies. |

The common frame has 240 T1 run-country observations and 360 run-turn observations in each of three later domains. Forty selected diagnostic cases are not an error-rate sample. State-declaration repetition and differing partial-review units are retained, not de-duplicated or pooled.
