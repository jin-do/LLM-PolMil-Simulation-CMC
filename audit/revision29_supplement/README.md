# Later calculation supplement for manuscript revision 29

This module reproduces the original-label/Top-1 comparison in Table B2 and the conditional state calculations in Tables D2 and A2. It also supplies the source register behind Table D1. It adds access to calculations on the existing archive; it does not run models, recode outcomes, or alter the common compliance ledger.

## Run locally

From the repository root, with Python 3.9 or later and no additional packages:

```sh
python audit/revision29_supplement/code/reproduce_supplement.py --out reproduced_revision29
python -m unittest discover -s audit/revision29_supplement/tests -v
```

The CLI can also take `--repo-root PATH` and `--module-root PATH`. Tests use the current repository directory; when run elsewhere, set `POLMIL_REPO_ROOT` to the repository path. No command downloads data or calls a model. All output is written under the explicitly selected output directory.

## Inputs and outputs

The module reads the existing `coding/top1_reanalysis/data/top1_source_recoding.csv` directly. The original and retrospective label columns remain separate. It derives the comparison from those two columns and checks their agreement with the existing change flags. Table B2 contains 120 executions: 104 classified, including 61 differences and 43 matches, plus 16 withheld. The 58.7% difference proportion uses only the 104 classified executions. Differences can reflect primary-path selection, terminal criteria, or errors in either record; missing original case-specific decision histories prevent treating all differences as verified corrections.

`data/conditional_cases.json` transcribes recorded priors, named effects and reported results for three Scenario 1 transitions and the separate Scenario 3 example in CLA-01. The coefficients are read from `vdm/Variable-Decision Matrix.json`, not duplicated here. Each complete named effect row is applied once; the resulting sum is clipped to 0–1. Every transition starts from its own **recorded** prior. Recalculated values are never passed into a later transition.

`data/path_source_register.csv` provides the six documentary links in Table D1. Its explanation is a source-linked assessment, not a computed proof of path validity. The source display names attached inputs but does not authenticate their exact historical versions. The prior leadership-unity cap of .85 is unsupported by the preserved VDM and is not silently repaired. Report 1's Turn 2 statement about enhanced unity in both capitals is also retained as a discrepancy with the shared recorded value.

The generated files are:

| File | Content |
|---|---|
| `table_b2_counts.csv` | Original-to-retrospective label matrix with row and column totals. |
| `outcome_label_comparison.csv` | 120 execution IDs with original/retrospective category codes and same/different/withheld status. |
| `table_d1_source_register.csv` | The published source register, copied for convenient inspection. |
| `table_d2_conditional_updates.csv` | Scenario 1 Turns 2–4: recorded prior, effects, checked and reported vectors, differences. |
| `table_a2_conditional_update.csv` | Scenario 3 Turn 4 using the same arithmetic procedure. |
| `conditional_variable_checks.csv` | All 16 component checks, full named increments, unclipped totals and clipping flags. |
| `reproduction.json` | Verified input digests, comparison counts, conditional results and scope. |

## Source integrity and limits

`data/provenance.json` records repository-relative paths, immutable GitHub links and SHA-256 digests. The source PDF and Top-1 CSV are checked byte for byte. The VDM digest normalizes line endings to LF because Git can check that historical text file out with CRLF on Windows. No other normalization is performed. A different input digest stops reproduction.

The CLA-01 PDF was directly rechecked for the transcribed states, effects and page locations during AI-assisted packaging on 5 October 2026. This was neither a new author coding pass nor independent human validation. The PDF is preserved at source commit `6867755772bfb74dd56c211df8c9a399607b5419`; the Top-1 input is preserved in revision-17 commit `4acc5add26f9b61d63ca3f51e7dfcc51c4a4e3fa`.

The arithmetic is conditional on source-recorded priors and effect assignments. It does not establish the appropriateness of those assignments, negotiate competing decision rules, or certify omitted events and preceding states. Local matching at Turn 4 retains earlier discrepancies. These purpose-selected checks are not independent trials and are not pooled into an accuracy rate. They do not validate either outcome-label set.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for field definitions. The missing historical extraction files are not recreated here: runtime reads transcribed inputs and checks source-file hashes, without extracting PDFs.
