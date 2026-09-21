# Revision 17 reproducibility materials

This module reproduces fixed coding and documented calculations for manuscript revision 17. It does not rerun the original LLM generation or re-adjudicate all records. Prepared 21–22 September 2026, Asia/Seoul; the recorded analysis version `revision17-conservative-candidate-2026-09-22` is retained as a preparation-stage identifier.

From the repository root (or the root of a standalone module bundle), using Python 3.10 or later:

```sh
python -X utf8 audit/rule_compliance/code/reproduce_revision17.py --out reproduced
python -X utf8 -m unittest discover -s audit/rule_compliance/tests -v
```

The reproduction command uses the Python standard library, requires no API key, network, logged-in Drive, or original workspace, verifies the package manifest, and writes only to the requested output directory. The prepared package was tested on Windows with the runtime recorded in `qa/execution_summary.json`; other platforms are not empirically certified here. Use UTF-8 mode for inherited code that opens JSON without an explicit encoding.

## Inputs and results

| Result | Fixed input and rule | Generated file under the output directory |
|---|---|---|
| Table 3 common frame | `data/core/07_semantic_validation_ledger.csv`; 11 prespecified metric keys × 120 runs | `criteria/criteria_reproduction.json` |
| Table 4 | Original ledger → 6 clear amendments → 8 boundary labels set to U; `protocol/CRITERIA_CONTEXT_V1.md` | `table4.csv` |
| Appendix A6 / Table A4 | Three coding versions with explicit ID-linked patches | `criteria/criteria_comparison.csv` |
| Appendix A7 / Table A5 | 40 AI diagnostic records, 38 common plus 2 representative cases | `diagnostic/` |
| Appendix A8 / Table A6 | Same conservative 1,320-row ledger, grouped by metric key and turn | `turn_summary.csv` |
| Tables A1–A3 | Fixed marker observations; documented arithmetic; partial review ledgers and coverage | `marker_summary.csv`, `legacy_fixed/` |
| Table B1 | Separate source-linked Top-1 coding, including withheld cases | `top1/` |
| Table C1 | Public n, sums and squared sums from actual responses | `survey/` |
| Claim checks | Numeric targets and explicit result selectors | `claims/` |

`results/` contains the prepared run; rerun into a separate `reproduced/` directory. `qa/` records this preparation's actual execution, independent cross-check and error-injection tests. Historical descriptions are in `legacy/`, and do not describe the present package's completeness or human-review status.

The current ledger is generated as `criteria/conservative_common_1320.csv`. Never add the original, clear, conservative or diagnostic rows together. Original 67 selected observations are excluded from the common denominator. HR-011, HR-037 and HR-038 are already represented by the amendments; diagnostic review creates no extra patches. Repeated state declarations are preserved as observations.

T1 uses two country observations per execution; later domains use one observation per execution and turn. Do not connect them into one accuracy curve. NA is reported separately and excluded from both denominators. Undefined rates are blank; percentages are sorted in protocol domain/turn order and rounded with Decimal half-even (two decimals, marker rates one decimal).

## Evidence and limits

Read `DATA_DICTIONARY.md`, `ANALYSIS_VERSIONS.md` and `REVIEW_PROVENANCE.md`. The evidence files preserve bounded excerpts, source locations and hashes; they do not authenticate historical model attachment inputs. `protocol/pinned_raw_source_links.csv` links original PDFs, protocol, actor profiles and VDM at historical commit `6867755772bfb74dd56c211df8c9a399607b5419`. This historical commit contains the original repository records, not the new revision 17 package.

Table reaggregation is local. A fresh comparison against the complete PDFs is a separate step requiring the historical sources (included in a full repository checkout or retrieved from the pinned links) and, where applicable, a PDF parser. Table A1 here reaggregates retained per-PDF marker observations, rather than extracting all PDFs again. Top-1 here replays preserved classifications, rather than performing new semantic recoding. Survey arithmetic is reproducible from sufficient statistics; individual responses and the actually administered Q3 wording cannot be re-audited from the public package.

Partial effect reviews cover 79 runs with actual block judgments, although the annotation inventory includes 120 runs. Partial ledgers, candidate extractions and selected facets must not be described as a new full 120-run semantic validation. No pooled global accuracy, statistical system ranking, independent double-coding, human ground truth or inter-rater coefficient is certified.

Original local sources and judgments have not been overwritten. Public copies replace internal source locators with repository paths where possible; original and transformed-copy hashes are recorded separately in `protocol/public_copy_derivations.csv`. Historical source hash fields remain historical facts, not the hash of the transformed CSV.

Repository publication does not grant a new blanket license or certify rights to excerpts and derived materials. Rights and official citation metadata remain documented limitations. No Release, DOI, submission or change in sharing permissions is represented by this integration.
