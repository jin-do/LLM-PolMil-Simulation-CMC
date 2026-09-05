# LLM-PolMil-Simulation-CMC

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
