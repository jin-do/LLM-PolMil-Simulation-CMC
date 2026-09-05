# Replication notes

## What can be reproduced

The revised scripts reproduce tabulations and statistics from the existing workbook-coded records and search for specified text markers in the execution PDFs. Reproduction of those calculations does not independently validate the coding, state arithmetic, provider identity, or factual correctness of the narratives. Exact regeneration of the original model outputs is not supported by the incomplete generation records.

The original archive is pinned to commit d345e7f391bef6f6c60c52d2a5907f0d166384ba, retrieved on 5 September 2026. That audit found all 120 public PDFs byte-identical to their local originals. This dated preservation check is distinct from the unresolved coding-to-branch link.

## Coded-data analysis

From the repository root:

~~~bash
python -m pip install -r requirements.txt
python analysis/reanalyze_outcomes.py
~~~

The input is coding/final_outcome_coding_run_level.csv. Its 120 records preserve the original outcomes and numeric values, with an indexed PDF path and explicit unresolved semantic status. Before calculation, the script checks row count, group balance, identifiers, file existence, numeric bounds, and category aggregation. Those are structural checks, not narrative validation.

requirements.txt pins NumPy 2.3.5 and pypdf 6.10.0. The older entry points analysis/reproduce_chi_square.py and analysis/statistical_analysis_script.py are compatibility wrappers that call the current reanalysis, not separate analyses. Figures can be regenerated with python analysis/generate_figures.py after the calculation.

| Analysis | Label permutations | Seed | Exceedances | Plus-one p | Cramer's V |
| --- | ---: | ---: | ---: | ---: | ---: |
| Primary four-system five-category | 100,000 | 1962 | 0 | 0.0000099999 | 0.398841 |
| Three-group five-category sensitivity | 100,000 | 1963 | 494 | 0.0049499505 | 0.333991 |
| Four-system three-category sensitivity | 100,000 | 1964 | 1 | 0.0000199998 | 0.392641 |
| Three-group three-category sensitivity | 100,000 | 1965 | 409 | 0.0040999590 | 0.289434 |

The plus-one formula is (exceedances + 1) / (repetitions + 1). For the two three-category tables, 20,000 bootstrap draws use seeds 1965 and 1966, producing percentile 95% resampling intervals [0.306644522, 0.522089633] and [0.188933154, 0.440694001], respectively. The recorded run used Python 3.12.14 and NumPy 2.3.5 with default_rng/PCG64; the output JSON includes the full parameters and input hash.

The primary 4-by-5 table is sparse: 8 of 20 expected counts are below five and the minimum is 0.25. No asymptotic chi-square p value is interpreted. The permutation calculation also requires exchangeability for a usual test interpretation, which the archive does not establish. Bootstrap ranges similarly depend on valid within-group resampling. Both are reported as conditional reference quantities for the retained coding.

analysis/variable_summary.csv reports means and sample SDs of the workbook-derived numbers. For Claude public opinion, the reproduced SD is 0.224; the original public summary's 0.289 was a summary-level discrepancy. Correcting that computed SD does not resolve the original numeric records' semantic provenance.

## Inspectable companion notebook

[analysis/reproduce_audit.ipynb](../analysis/reproduce_audit.ipynb) contains four code cells. It checks the indexed coding input, actually recomputes all four permutation analyses and both bootstrap intervals, and checks saved marker evidence and the identity of the PDF inputs. It does not itself repeat full PDF text extraction; use the audit command in the next section for that step. Recalculation replaces generated analysis outputs but leaves the coding input unchanged.

The notebook's four code cells were executed sequentially in a fresh Python process on 6 September 2026. Its metadata records that this was not a Jupyter-kernel run and that the nbformat validation library was unavailable; only required notebook structure fields were checked. This execution check is not a claim of formal notebook-schema validation.

Jupyter is optional and is not included in requirements.txt. To use a notebook interface, install it separately in the same environment, for example with python -m pip install jupyterlab, then open the notebook from the repository root or analysis directory. The scripts above remain the direct reproduction route without Jupyter.

## Full-document marker search

~~~bash
python analysis/audit_traceability.py
~~~

The script reads the PDFs with pypdf, normalizes whitespace, and searches the entire document. A prompt, response, or other captured text can supply a hit. The results do not distinguish field requests from completed output fields.

| Marker | Found / 120 PDFs | Not found |
| --- | ---: | ---: |
| At least 500 extracted characters | 120 | 0 |
| JSON/VDM artifact reference | 120 | 0 |
| Explicit result-log label | 119 | 1 |
| Four state-dimension label patterns | 120 | 0 |
| Trigger or threshold language | 120 | 0 |
| Generic variable-status label | 113 | 7 |
| Strict reconfirm-variable-status phrase | 111 | 9 |
| All five metadata-label pattern groups | 0 | 120 |
| Specified independent-checker phrase | 0 | 120 |

The generic and strict state-status counts refer to different patterns. In particular, the strict pattern is reconfirm(?:ed)?[ _-]?variable[ _-]?status. A hit still does not show that the model successfully confirmed a valid numeric state. The metadata/checker rows report label or phrase searches, not the actual completeness of generation metadata or the nonexistence of independent records elsewhere.

Outputs are analysis/traceability_log_audit.csv, analysis/traceability_marker_evidence.csv, and analysis/traceability_audit_summary.json. Evidence rows list each component pattern, match count, all hit pages, and one representative snippet. Nonprinting control characters are removed from displayed snippets after searching; the original PDF text is not edited.

The script optionally accepts --cached-text-dir and --cache-manifest together. A supplied cache must match both PDF and extracted-text hashes and retain numbered page boundaries. The distributed audit result records use of the 5 September extraction cache and verification of 120 hash pairs. A default fresh-PDF run should reproduce the marker counts and evidence; its cache-use metadata will differ.

## Unresolved evidence

The [provenance audit](provenance_audit.md) records which checks cover all 120 records and which are limited to two targeted PDF examples. Source-workbook transfer checks were performed locally; the source literals and worksheet locators are published, but the original local workbooks are not supplied as a new public source in this package. The raw PDFs alone cannot reproduce the historical branch-selection decisions.

The original protocol includes illustrative initial defaults and a 0-100 scale, while the summaries use 0-1 values. A verified run-specific initialization and conversion ledger was not identified. Full AHP matrices and actual consistency ratios were likewise not identified. These limitations are detailed in [input artifact caveats](input_artifact_caveats.md), rather than filled with reconstructed values.
