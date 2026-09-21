# LLM-PolMil-Simulation-CMC

> **Version guide:** the retained sections below describe the historical workbook-coded analysis and document-marker search. For the subsequent manuscript revision 17 materials, use [Revision 17 reproducibility materials](#revision-17-reproducibility-materials). The historical coding remains preserved; the later rule-compliance and Top-1 modules have their own inputs, criteria and limitations. They were not present in source commit 6867755772bfb74dd56c211df8c9a399607b5419.

This repository contains archived materials and a retrospective methodological reanalysis of a structured LLM-assisted political-military simulation using a Cuban Missile Crisis testbed. The workflow combines JSON actor profiles, researcher-set influence weights, a Variable-Decision Matrix (VDM), prompts, and archived conversations.

The package supports inspection of these artifacts and reproduction of the **existing workbook-coded summaries**. The coding has not been independently validated against the narratives. All 120 rows retain semantic_verification_status=unresolved; their PDF paths are indexed, not semantically certified. The analysis does not establish predictive accuracy, rule compliance, or a causal effect of model architecture.

## Archive and revision scope

The original public archive inspected on 5 September 2026 is pinned to commit [d345e7f391bef6f6c60c52d2a5907f0d166384ba](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/d345e7f391bef6f6c60c52d2a5907f0d166384ba). It contained 120 execution PDFs and a 20-row aggregate outcome table. The September reanalysis adds a 120-row index, provenance findings, executable analyses, and a document-marker search. Original PDF logs, JSON inputs, VDM, and protocol/prompt documents are preserved as historical evidence.

The four archived system groups are GPT-4o, Gemini 2.5 Flash, Claude Opus 4, and Perplexity Pro, with 30 PDFs per group. These are archive labels, not independently authenticated provider snapshots. Perplexity Pro is a retrieval-augmented system condition; its exclusion is examined in sensitivity analyses. Separate files do not establish independent or exchangeable observations.

## Reproducing the coded-data analysis

From the repository root:

~~~bash
python -m pip install -r requirements.txt
python analysis/reanalyze_outcomes.py
python analysis/generate_figures.py
~~~

The primary table retains all five original outcome categories. The three further calculations are exploratory sensitivity analyses, not preregistered tests.

| Analysis | Pearson discrepancy statistic | Cramer's V | Conditional random-label reference p |
| --- | ---: | ---: | ---: |
| Four systems, five categories: primary | 57.266667 | 0.398841 | 0.0000099999 |
| Excluding Perplexity, five categories | 20.078947 | 0.333991 | 0.0049499505 |
| Four systems, three categories | 37.000000 | 0.392641 | 0.0000199998 |
| Excluding Perplexity, three categories | 15.078947 | 0.289434 | 0.0040999590 |

Each reference p value uses 100,000 label reallocations and the plus-one correction. The two three-category analyses also use 20,000 within-group bootstrap draws. Seeds, input hash, environment, and full results are recorded in [analysis/reanalysis_results.json](analysis/reanalysis_results.json).

The [companion notebook](analysis/reproduce_audit.ipynb) exposes the calculation and input-identity checks. Its saved marker checks inspect the existing audit outputs; a fresh PDF extraction uses the separate audit command below.

These calculations reproduce association in the archived coding. They do not verify the coding itself. Exchangeability and valid within-group resampling are unestablished, so the p values and bootstrap intervals are conditional reference quantities, not population inference or estimates of crisis probabilities.

## Reproducing the document-marker search

~~~bash
python analysis/audit_traceability.py
~~~

The script searches the full extracted PDF text after whitespace normalization; user prompts, generated responses, and other captured text are not separated. All 120 PDFs meet the text-length criterion and contain artifact references, four state-dimension labels, and trigger/threshold language. A result-log label occurs in 119; a generic variable-status label in 113; and the stricter reconfirm-variable-status phrase in 111. All five metadata-label patterns jointly occur in 0 PDFs, and the specified independent-checker phrase occurs in 0.

These are **text-marker counts**, not compliance rates. A phrase hit does not prove valid populated metadata or independent checking; a missing phrase does not prove that an external record never existed. Pattern definitions, hit pages, counts, and representative snippets are supplied in the audit outputs. See [replication notes](docs/replication_notes.md).

## Evidence limitations

- The 120-row index reproduces local workbook records and matching file numbers. Branch, page, and selection-rule provenance remains unresolved. Targeted GPT-4o-01 and GPT-4o-02 comparisons identify discrepancies without assigning replacement codes or values. See the [provenance audit](docs/provenance_audit.md).
- Inputs intended for an October 14 start contain later information. The original documents also contain unresolved source markers and inconsistent scale descriptions. See [input artifact caveats](docs/input_artifact_caveats.md).
- The archive does not establish a randomized comparison of information modes, a frozen final configuration, complete generation metadata, or independent transition verification.
- Expert ratings concern one selected Gemini-generated scenario set and support preliminary face validity only. The public package contains an instrument and aggregate note, not individual responses.

The [data dictionary](docs/data_dictionary.md), [design notes](docs/final_experiment_design_notes.md), and [file inventory](docs/file_inventory.md) identify what each artifact can support.

## Manuscript

The accompanying manuscript is *Auditing Traceability and Outcome Variation in a Structured LLM-Assisted Pol-Mil Simulation: A Methodological Reanalysis of a Cuban Missile Crisis Testbed*. The archive and survey are reused data; the methodological audit and reanalysis should not be presented as a new execution experiment. The original snapshot identifier above refers to the historical archive, not to a later release of the revised package.

## Revision 17 reproducibility materials

The modules below reproduce fixed-input results associated with manuscript revision 17, *A Structured Method for LLM-Assisted Political-Military Scenario Generation in a Cuban Missile Crisis Testbed*. They extend the repository while preserving the historical analyses above, including their unresolved coding status and earlier manuscript title. They do not replace the archived execution PDFs or retrospectively rewrite the original judgments.

| Module | Contents |
| --- | --- |
| [Rule-compliance audit](audit/rule_compliance/README.md) | Original judgments, ID-linked amendments, conservative analysis, turn totals, diagnostic AI review and partial-check coverage |
| [Top-1 reanalysis](coding/top1_reanalysis/README.md) | Preserved source-linked coding, selection and withholding rules, evidence locators and Table B1 tabulation |
| [Survey summary](docs/survey_summary/README.md) | Non-individual aggregates, item wording, valid counts, means and sample SDs, with the unresolved Q3 wording difference |
| [Claim reconciliation](docs/claim_reconciliation/README.md) | Manuscript target locations linked to input hashes, criteria, code and generated result rows |

### Reproduce revision 17 results

From the repository root, using Python 3.10 or later:

~~~bash
python -X utf8 audit/rule_compliance/code/reproduce_revision17.py --out reproduced
~~~

This command uses the standard library and verifies the supplied manifest. It requires no AI API key, network connection, logged-in Drive, or private working directory. It writes results under `reproduced/`. The prepared outputs are stored in [audit/rule_compliance/results](audit/rule_compliance/results); each module README identifies its inputs, criteria and output files. The older commands above remain the reproduction route for the historical analysis.

To run the revision 17 automated checks:

~~~bash
python -X utf8 -m unittest discover -s audit/rule_compliance/tests -v
python -X utf8 -m unittest discover -s coding/top1_reanalysis/tests -v
~~~

The [recorded local preparation](audit/rule_compliance/qa/execution_summary.json), performed on 22 September 2026 (KST) with Python 3.12.14 on Windows, passed 61 automated tests: 53 core/diagnostic tests and 8 Top-1 tests. Two isolated offline runs produced identical hashes for 33 scientific CSV/JSON outputs, matching the packaged results, with no recorded network attempts or reads from outside the allowed isolated environment. These are local preparation results, not a claim of remote CI execution or certification of every operating system.

The [claim summary](audit/rule_compliance/results/claims/claim_summary.json) records **308 of 315 targets matched**, **7 NOT_REPRODUCED**, and no numeric mismatch. The reproduced targets cover Table 3, Table 4, Tables A1–A6, Table B1 and Table C1 within the stated scope. The seven source-dependent boundaries include the original readability-threshold check, historical PDF retrieval operations, selected source-meaning examples and survey administration. The [claim reconciliation guide](docs/claim_reconciliation/README.md) lists their exact limits. Targets can repeat the same quantity across prose and table cells; 315 is not a scientific sample size or a count of independently validated findings.

### Analysis versions and denominators

The current rule-compliance analysis starts with 1,320 common checks: 240 initial-setting observations and 360 observations in each of three later domains. Six explicit corrections are applied once, followed by eight ambiguous initial-setting judgments assigned U in the conservative version. The 67 selected supplemental observations and the 40-item diagnostic review are separate scopes and are not added to that denominator. Of the diagnostic items, 38 refer to existing common checks and two are separately selected discrepancies. Their frequencies are not archive-wide error rates.

Turn totals use the same conservative ledger as Table 4. T1 has country-level observations; T2–T4 use run-by-turn observations. They should not be combined into one accuracy curve. Partial effect review contains actual block judgments for 79 runs despite an annotation inventory covering 120. Top-1 tabulation separately retains all 120 executions, including 16 withheld classifications. Survey arithmetic uses item-level sufficient statistics, with 105 item responses from 18 participants; individual response rows are withheld.

See [analysis versions](audit/rule_compliance/ANALYSIS_VERSIONS.md), [data dictionary](audit/rule_compliance/DATA_DICTIONARY.md), and [review provenance](audit/rule_compliance/REVIEW_PROVENANCE.md). The recorded analysis identifier `revision17-conservative-candidate-2026-09-22` is retained for provenance; its name describes the preparation stage, not an assertion that the repository modules remain unpublished.

### Evidence and review limits

The 40-item re-review is **AI review**, not completed human adjudication or independent double coding. The author's qualitative, non-blind review of the methodological criteria is recorded separately. Publication does not establish independent human item labels, evaluator reliability, authenticated historical model snapshots or the exact inputs attached to each original model call.

Fixed-input replay checks calculations given preserved judgments and coding. It does not regenerate the original LLM outputs or conduct a new semantic review of every PDF. Table A1 reaggregates retained marker observations; Top-1 replays the supplied recoding. The Q3 wording actually administered and the derivation of survey aggregates from private respondent rows cannot be independently established from this public module.

There are 1,405 historical extraction references across 929 check IDs pointing to 160 extraction files not distributed with these modules. Source PDF paths, pages and excerpts remain available, but do not certify equivalent reconstruction of the full historical review windows or coverage decisions. These missing extraction files are not required for fixed-label aggregation. See [historical evidence availability](audit/rule_compliance/protocol/HISTORICAL_EVIDENCE_AVAILABILITY.md).

Original PDFs and simulation inputs remain in the repository and are linked by [pinned paths and hashes](audit/rule_compliance/protocol/pinned_raw_source_links.csv). A full repository checkout includes those historical files; a standalone copy of the added modules requires retrieving the linked originals for fresh PDF inspection. No unpublished manuscript, reviewer correspondence, private source mapping or respondent-level survey file is added by these modules.

### Citation and rights

Historical source materials are pinned to [6867755772bfb74dd56c211df8c9a399607b5419](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/6867755772bfb74dd56c211df8c9a399607b5419). The revision 17 modules were **not present** in that commit. Cite the actual repository commit containing the version of these modules that you use, and retain the historical source reference separately. No new Release, DOI, paper acceptance or finalized author/affiliation metadata is asserted here.

The existing repository license is retained. This addition supplies no new blanket license or independent certification of redistribution rights for excerpts, generated materials or survey-derived aggregates. Computational reproduction and public availability do not establish those rights.
