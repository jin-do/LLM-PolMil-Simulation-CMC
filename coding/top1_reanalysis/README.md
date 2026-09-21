# Retrospective Top-1 coding replay

This module reproduces revision 17 Table B1 from the actual, preserved 120-execution coding ledger. The source-linked recoding is a separate outcome analysis; it is not a rule-compliance score, a historical ground-truth test, or an independent human validation set.

```sh
python coding/top1_reanalysis/code/reproduce_top1.py
```

Run from the repository root with Python 3.10+; only the standard library is required. The script reads local fixed inputs and writes only `results/` files. It needs no network, AI API, private files or credentials. `--root` selects the module directory and `--output` optionally changes the result directory.

The ledger is `data/top1_source_recoding.csv`, preserved byte-for-byte. Every execution retains its original category, revised label or withholding status, branch selection, actual source page numbers, short selection/terminal excerpts, rationale, limitations and source PDF hash. `confirmed` is the inherited label status; it does **not** mean independently confirmed by a human. The historical recoding was AI-assisted; no blinded human double coding or inter-rater reliability is asserted.

[RECODING_PROTOCOL.md](RECODING_PROTOCOL.md) supplies the selection, linkage, category and withholding criteria. The primary path must be explicitly identifiable and traceable to the ending. An offer alone is not a completed diplomatic resolution, a threat alone is not war, and a transient clash alone does not determine the terminal outcome. Untraceable selections, insufficient endings and incompatible final descriptions are withheld. Withheld is a reporting status, not a sixth crisis outcome.

`data/source_references.csv` links all 120 source PDFs to historical commit `6867755772bfb74dd56c211df8c9a399607b5419` and their preserved SHA-256 values. PDFs are not duplicated. The fixed table aggregation works locally; a new semantic reading of every PDF requires the historical sources from a full repository checkout or pinned-source downloads and is not performed by this script. The retrospective recoding ledger was added later and must not be described as present at that historical commit.

Outputs:

- `results/table_b1_counts.csv`: system-level and total frequencies, including zero categories.
- `results/table_b1_percentages.csv`: frequencies, denominators and percentages rounded half up to one decimal.
- `results/withheld_cases.csv`: the 16 withheld executions and preserved reasons.
- `results/top1_reproduction.json`: scope, totals and label-change count.

Every system denominator is all 30 executions; the total is 120. Withheld records stay in those denominators. Expected totals are 61 stalemate, 0 collapse, 38 diplomatic resolution, 5 full-scale war, 0 limited conflict and 16 withheld. There are 104 classified executions and 61 changed classifications relative to the retained original labels. The 61 changes are a label comparison, not a new accuracy estimate.

The aggregation code is a new packaging-stage replay written on 2026-09-21/22 KST. It replaces the old aggregation's private working-directory dependencies while preserving the fixed source ledger and substantive coding criteria. Missing states are not imputed, signed changes are not converted into absolute states, actor vectors are not averaged and no new model ranking or significance test is computed. Original source rights remain applicable; no blanket new license is assigned here.

In the integrated package, the root wrapper writes to `reproduced/diagnostic`, `reproduced/top1`, or `reproduced/survey`, respectively. Standalone module commands accept `--out`. The prepared integrated outputs are under `audit/rule_compliance/results/`.
