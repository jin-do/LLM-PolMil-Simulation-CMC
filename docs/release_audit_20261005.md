# Public material reconciliation on 5 October 2026

The repository was checked against the results and evidence descriptions in manuscript revision 29. At the start of this check, public `main` was `4acc5add26f9b61d63ca3f51e7dfcc51c4a4e3fa`. Its existing numerical results reproduced, but later contextual-review records, Table B2 and Appendix D calculation support, and 160 cited historical extraction artifacts were absent.

## Changes in this update

- Added [the contextual author-review module](../audit/author_review/README.md): the September 27 records, an A/R/I presentation of the 40 judgments, executable transition counts, and the September 29 AI-only explanatory recheck. No common-assessment labels changed.
- Added [later calculations](../audit/revision29_supplement/README.md): the original-to-Top-1 cross-tabulation and conditional calculations for Appendix D and the earlier Table A2 example. The code reads the existing Top-1 data and original VDM.
- Added [160 recovered extraction artifacts](../audit/recovered_extractions/README.md), totaling 6,849,488 bytes. All match the retained historical checksum inventory. The recovery maps 1,405 references across 929 check IDs and performs no new extraction.
- Reorganized the [main guide](../README.md) around the current manuscript. The previous guide is preserved as [README_revision17.md](../README_revision17.md); earlier inventory, dictionary and replication notes now identify their historical scope.
- Extended `.gitattributes` to preserve bytes on checkout. Windows line-ending conversion had changed working-copy hashes of historical text inputs although the Git objects were correct.
- Added [a complete current file manifest](../CURRENT_MANIFEST.csv), its checksum, and [a verification command](../verify_release.py). The original revision-17 module and its manifests remain unchanged.

## Verification

These were actual local checks using Python 3.12.14 on Windows. They are not claims of hosted CI execution, independent scientific validation or fresh model experiments.

| Check | Result |
| --- | --- |
| Original module manifest | 282 entries verified |
| Original automated tests | 53 core/diagnostic and 8 Top-1 tests passed |
| Prepared revision-17 outputs | All 33 regenerated CSV/JSON files matched the preserved outputs byte-for-byte |
| Revision-17 claim targets | 308 of 315 matched; 7 explicitly documented reproduction boundaries; no numerical mismatch |
| Fresh marker search | All 120 PDFs, using pypdf 6.10.0 without a text cache; all nine counts and source hashes matched |
| Historical numerical analyses | Four conditional random-label calculations and two bootstrap calculations matched the saved results, using NumPy 2.3.5 |
| Original source identity | All 126 pinned source assets matched after restoring canonical checkout bytes |
| Top-1 locators | All 533 page locators fell within their source PDFs |
| Later calculation tests | All 9 passed, including recorded-prior nonpropagation, effect summation/clipping, input identity and invalid-input cases |
| Contextual author review | 40 items: 27 A, 10 R, 3 I; 12 changed interpretations; 35 distinct source PDFs matched their recorded hashes |
| Later explanatory quotations | All 44 quotations in the 12-case recheck were found on their cited pages in 11 PDFs, with NFKC/whitespace normalization |
| Recovered artifacts | 160 of 160 historical sizes and SHA-256 hashes matched; all 1,405 references mapped |

The seven unreproduced claim targets in the older reconciliation concern source-dependent activities rather than arithmetic disagreements. Their original status is retained in [the claim results](../audit/rule_compliance/results/claims/claim_comparison.csv). Recovering the extraction artifacts does not retrospectively change those adjudication or process claims.

## Publication boundaries

Historical simulations, input profiles, VDM coefficients, common-assessment labels, survey sufficient statistics and Top-1 coding remain unchanged. Historical extraction defects and line endings are preserved. The original missing-file availability record remains true of its dated release; a separate recovery catalog records the availability change.

Author-review JSON and CSV records retain their original bytes. The public historical report removes a link to an excluded manuscript insertion draft. The later explanatory copies omit manuscript insertion drafts and an internal working-file list. These transformations preserve all case findings and judgments and are recorded with original/public hashes in [the source manifest](../audit/author_review/source_records/manifest.json).

The additions contain no respondent-level survey records, reviewer correspondence, model credentials or manuscript files. Pattern screening and source inspection found no email addresses, personal Windows paths or credential-like strings in the new evidence files. This limited screening is not a formal privacy audit. The preserved local manifest supports byte identity of the recovered files; it does not independently certify their original timestamps or the completeness of every historical review decision.

The manuscript and response-letter update changes the data-availability description to match this release. No numerical result or claim of comparative effectiveness is added.
