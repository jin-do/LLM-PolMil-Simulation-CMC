# Earlier expert survey aggregate reproduction

This module recalculates Table C1 of manuscript revision 17 from non-individual aggregate statistics derived from the retained response workbook. It contains no respondent rows, timestamps, respondent identifiers, or open-ended comments.

Run from the repository root using Python 3.10 or later, with no third-party packages or network access:

```text
python docs/survey_summary/code/reproduce_survey.py --out reproduced/survey
```

The script writes `table_c1_reproduced.csv` and `survey_summary_reproduced.json` in the selected output directory. Omitting `--out` uses `results/` within this module. The CSV gives `item`, `valid_n`, full-precision `mean` and `sample_sd`, and their two-decimal display values. Re-running it overwrites these generated result files only. Python integration may call `reproduce(root=None, out=None)`.

## Inputs and calculation

`data/survey_sufficient_statistics.csv` contains each item's valid response count, sum of actual scores, and sum of squared actual scores. These values were directly calculated from the retained private workbook during preparation on 22 September 2026 (Asia/Seoul), not inferred from rounded manuscript means and not reconstructed into synthetic individual responses. The internal delivery retains source hashes, column mappings, and the derivation record; it is excluded from this public module.

For each item, mean = sum/n and sample SD = sqrt((sum_of_squares − sum²/n)/(n−1)). Missing responses were excluded per item, with no imputation. The overall 3.96 is the unweighted mean of six full-precision item means. The 105 valid item responses are repeated item responses from 18 participants. They are not 105 participants. The eight open-ended responses are a retained aggregate count and are not coded or analyzed here.

`data/question_labels.csv` preserves the manuscript's descriptive labels and the retained workbook question wording. For Q3 it also identifies the alternate wording in the retained questionnaire (page 14): changes in tension reduction, diplomatic support, and internal cohesion. Which wording was administered remains unresolved. The full questionnaire is not duplicated here because its retained PDF contains an editor URL; this module uses question information only. `legacy/` preserves the earlier full-precision numeric summary and public scope note without changing their content. Those files are historical comparison records, not raw responses.

## Reproduction boundary

All six displayed means, sample SDs, and valid counts match Table C1, and their calculations can be repeated from the public aggregates. Public users cannot independently re-derive the aggregates from individual responses, inspect missing-response positions, determine Q3 administration wording, or verify recruitment and consent records. The selected set consisted of three Gemini scenarios assessed in one survey round; this appraisal does not validate the 120-execution rule labels or all generated scenarios.

The supplied sums and squared sums describe item-level totals and dispersion, without cross-item respondent linkage. Individual responses remain withheld. Publication and arithmetic reproduction do not independently certify applicable data-use permissions, recruitment or consent. No new license or blanket permission is asserted. Original source rights remain applicable.

In the integrated package, the root wrapper writes to `reproduced/diagnostic`, `reproduced/top1`, or `reproduced/survey`, respectively. Standalone module commands accept `--out`. The prepared integrated outputs are under `audit/rule_compliance/results/`.
