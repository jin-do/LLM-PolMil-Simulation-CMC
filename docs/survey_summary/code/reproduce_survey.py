"""Recompute Table C1 from actual-response aggregate sufficient statistics.

Prepared on 2026-09-22 (Asia/Seoul). Python 3.10+ standard library only.
This code cannot re-audit private respondent records or administered Q3 wording.
"""
from pathlib import Path
import csv
import json
import math
import argparse


def reproduce(root=None, out=None):
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    with (root / "data/survey_sufficient_statistics.csv").open(encoding="utf-8", newline="") as handle:
        inputs = list(csv.DictReader(handle))
    if [r["item"] for r in inputs] != [f"Q{i}" for i in range(1, 7)]:
        raise ValueError("Expected exactly one ordered record for each of Q1–Q6")
    result = []
    for r in inputs:
        n, total, squares = (int(r[k]) for k in ["n", "sum_scores", "sum_squared_scores"])
        low, high = int(r["scale_min"]), int(r["scale_max"])
        if not (n > 1 and low == 1 and high == 5 and n * low <= total <= n * high):
            raise ValueError(f"Invalid sample size, scale, or sum for {r['item']}")
        if not (n * low**2 <= squares <= n * high**2 and squares * n >= total**2):
            raise ValueError(f"Invalid squared sum for {r['item']}")
        mean = total / n
        sd = math.sqrt((squares - total * total / n) / (n - 1))
        result.append({"item": r["item"], "valid_n": n, "mean": mean, "sample_sd": sd,
                       "mean_display": f"{mean:.2f}", "sample_sd_display": f"{sd:.2f}"})
    overall = sum(r["mean"] for r in result) / len(result)
    context = json.loads((root / "data/survey_context.json").read_text(encoding="utf-8"))
    summary = {
        "participants": context["participants"],
        "valid_item_responses": sum(r["valid_n"] for r in result),
        "unweighted_mean_of_item_means": overall,
        "unweighted_mean_display": f"{overall:.2f}",
        "open_ended_response_count": context["open_ended_response_count"],
        "raw_respondent_reproduction": "NOT_PUBLICLY_REPRODUCIBLE",
        "aggregate_calculation": "REPRODUCED_FROM_ACTUAL_RESPONSE_SUFFICIENT_STATISTICS",
        "Q3_wording": "ADMINISTERED_VERSION_UNRESOLVED",
    }
    output = Path(out) if out else root / "results"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "table_c1_reproduced.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=result[0].keys())
        writer.writeheader()
        writer.writerows(result)
    (output / "survey_summary_reproduced.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return result, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Write generated results here instead of module/results")
    args = parser.parse_args()
    _, summary = reproduce(out=args.out)
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
