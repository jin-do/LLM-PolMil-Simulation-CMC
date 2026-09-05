"""Reproduce conditional summaries of the archived, unverified coding table.

Run ``python analysis/reanalyze_outcomes.py`` from the repository root.
Requires NumPy and ``coding/final_outcome_coding_run_level.csv``. This script
checks the table's structure and linked file existence. It does not validate
the outcome codes or state values against the narratives in the PDFs.

Permutation results assume exchangeability of the coded rows under the null;
bootstrap intervals describe resampling of this coding table. Neither step
establishes independent executions, correct coding, or a model-level effect.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "coding" / "final_outcome_coding_run_level.csv"
OUTPUT = ROOT / "analysis" / "reanalysis_results.json"
VARIABLE_SUMMARY = ROOT / "analysis" / "variable_summary.csv"
PERMUTATION_REPETITIONS = 100_000
BOOTSTRAP_REPETITIONS = 20_000

SYSTEMS = ["GPT-4o", "Gemini 2.5 Flash", "Claude Opus 4", "Perplexity Pro"]
CATEGORIES_5 = [
    "Protracted stalemate",
    "Internal collapse",
    "Diplomatic resolution",
    "Full-scale war",
    "Limited conflict",
]
CATEGORIES_3 = ["Stalemate", "Diplomatic resolution", "Adverse non-diplomatic outcome"]
COLLAPSED_CATEGORIES = {
    "Protracted stalemate": "Stalemate",
    "Internal collapse": "Adverse non-diplomatic outcome",
    "Diplomatic resolution": "Diplomatic resolution",
    "Full-scale war": "Adverse non-diplomatic outcome",
    "Limited conflict": "Adverse non-diplomatic outcome",
}
VARIABLES = [
    ("tension", "tension"),
    ("diplomatic_engagement", "diplomatic support"),
    ("public_support", "public opinion"),
    ("internal_unity", "leadership unity"),
]


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 120:
        raise RuntimeError(f"Expected 120 archived coding rows, found {len(rows)}")
    ids = {row["execution_id"] for row in rows}
    paths = {row["raw_log_path"] for row in rows}
    if len(ids) != 120 or len(paths) != 120:
        raise RuntimeError("Execution identifiers and indexed raw-log paths must be unique")
    for row in rows:
        identifier = row["execution_id"]
        if row["system"] not in SYSTEMS or row["final_outcome_5"] not in CATEGORIES_5:
            raise RuntimeError(f"Unknown system or outcome in {identifier}")
        if row["final_outcome_3"] != COLLAPSED_CATEGORIES[row["final_outcome_5"]]:
            raise RuntimeError(f"Inconsistent three-category aggregation in {identifier}")
        log_path = (ROOT / row["raw_log_path"]).resolve()
        if not log_path.is_relative_to(ROOT) or not log_path.is_file():
            raise RuntimeError(f"Missing or outside-repository indexed raw log: {row['raw_log_path']}")
        for field, _ in VARIABLES:
            value = float(row[field])
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise RuntimeError(f"Invalid archived state value {field} in {identifier}")
        if row["semantic_verification_status"] != "unresolved":
            raise RuntimeError("This archived analysis expects all source-coding statuses to be unresolved")
    for system in SYSTEMS:
        count = sum(row["system"] == system for row in rows)
        if count != 30:
            raise RuntimeError(f"Expected 30 rows for {system}, found {count}")
    return rows


def table(rows: list[dict[str, str]], systems: list[str], field: str, categories: list[str]) -> np.ndarray:
    return np.array(
        [[sum(row["system"] == system and row[field] == category for row in rows) for category in categories]
         for system in systems],
        dtype=int,
    )


def chi_square(values: np.ndarray) -> tuple[float, np.ndarray]:
    if values.sum() <= 0:
        raise ValueError("Contingency table must contain observations")
    expected = np.outer(values.sum(axis=1), values.sum(axis=0)) / values.sum()
    # An absent category in a bootstrap draw has observed = expected = 0.
    # Its Pearson contribution is zero, not an undefined 0/0.
    contributions = np.divide(
        (values - expected) ** 2,
        expected,
        out=np.zeros_like(expected, dtype=float),
        where=expected > 0,
    )
    return float(np.sum(contributions)), expected


def cramers_v(values: np.ndarray) -> float:
    active = values[values.sum(axis=1) > 0][:, values.sum(axis=0) > 0]
    dimension = min(active.shape[0] - 1, active.shape[1] - 1)
    if dimension < 1:
        return 0.0
    statistic, _ = chi_square(active)
    return math.sqrt(statistic / (active.sum() * dimension))


def permutation_test(values: np.ndarray, repetitions: int, seed: int) -> dict[str, object]:
    observed, expected = chi_square(values)
    labels = np.repeat(np.arange(values.shape[0]), values.sum(axis=1))
    outcomes = np.concatenate([np.repeat(np.arange(values.shape[1]), row) for row in values])
    rng = np.random.default_rng(seed)
    row_offsets = labels * values.shape[1]
    exceedances = 0
    for _ in range(repetitions):
        # One permutation call per repetition preserves the September 1 RNG
        # stream. Bincount changes counting only, not the sampled tables.
        shuffled = rng.permutation(outcomes)
        permuted = np.bincount(row_offsets + shuffled, minlength=values.size).reshape(values.shape)
        # Permutation preserves both margins, so expected counts are constant.
        statistic = float(np.sum((permuted - expected) ** 2 / expected))
        exceedances += int(statistic >= observed - 1e-12)
    return {
        "permutation_repetitions": repetitions,
        "permutation_seed": seed,
        "permutation_exceedances": exceedances,
        "permutation_p_plus_one": (exceedances + 1) / (repetitions + 1),
    }


def bootstrap_v_ci(values: np.ndarray, repetitions: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    totals = values.sum(axis=1)
    probabilities = values / totals[:, None]
    samples = []
    absent_category_draws = 0
    degenerate_draws = 0
    for _ in range(repetitions):
        sampled = np.vstack([rng.multinomial(int(n), p) for n, p in zip(totals, probabilities)])
        active_columns = int(np.count_nonzero(sampled.sum(axis=0)))
        absent_category_draws += int(active_columns < values.shape[1])
        degenerate_draws += int(active_columns < 2)
        samples.append(cramers_v(sampled))
    return {
        "cramers_v_bootstrap_repetitions": repetitions,
        "cramers_v_bootstrap_seed": seed,
        "cramers_v_bootstrap_95_resampling_interval": [
            float(value) for value in np.percentile(samples, [2.5, 97.5])
        ],
        "bootstrap_draws_with_absent_categories": absent_category_draws,
        "bootstrap_degenerate_draws_assigned_zero_v": degenerate_draws,
    }


def write_variable_summary(rows: list[dict[str, str]]) -> None:
    summary_rows: list[dict[str, object]] = []
    for system in SYSTEMS:
        system_rows = [row for row in rows if row["system"] == system]
        for field, label in VARIABLES:
            values = np.array([float(row[field]) for row in system_rows], dtype=float)
            summary_rows.append(
                {
                    "condition": system,
                    "variable": label,
                    "mean": f"{values.mean():.3f}",
                    "sd": f"{values.std(ddof=1):.3f}",
                }
            )
    with VARIABLE_SUMMARY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["condition", "variable", "mean", "sd"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)


def analyze(values: np.ndarray, seed: int, bootstrap_seed: int | None = None) -> dict[str, object]:
    statistic, expected = chi_square(values)
    if (expected <= 0).any():
        raise RuntimeError("Observed table has an absent category; review the category specification")
    result: dict[str, object] = {
        "counts": values.tolist(),
        "chi_square": statistic,
        "df": (values.shape[0] - 1) * (values.shape[1] - 1),
        **permutation_test(values, PERMUTATION_REPETITIONS, seed),
        "cramers_v": cramers_v(values),
        "minimum_expected_count": float(expected.min()),
        "expected_cells_below_5": int((expected < 5).sum()),
        "expected_cell_count": int(expected.size),
    }
    if bootstrap_seed is not None:
        result.update(bootstrap_v_ci(values, BOOTSTRAP_REPETITIONS, bootstrap_seed))
    return result


def main() -> None:
    rows = load_rows()
    input_hash = hashlib.sha256(INPUT.read_bytes()).hexdigest()
    five = table(rows, SYSTEMS, "final_outcome_5", CATEGORIES_5)
    three = table(rows, SYSTEMS, "final_outcome_3", CATEGORIES_3)
    results = {
        "metadata": {
            "analysis_scope": "Conditional reproduction of archived coding; not source-log semantic validation",
            "input_csv": INPUT.relative_to(ROOT).as_posix(),
            "input_csv_sha256": input_hash,
            "input_rows": len(rows),
            "source_coding_unverified": True,
            "source_coding_unverified_rows": sum(row["semantic_verification_status"] == "unresolved" for row in rows),
            "independent_semantic_validation_performed": False,
            "record_linkage_scope": "Indexed unique paths checked for file existence; branch, page, and code-selection provenance unresolved",
            "numerical_values_recode_performed": False,
            "interpretation": "Conditional archive summaries only; no model-effect inference or established independence of executions",
            "permutation_assumption": "Exchangeability of coded outcomes across the fixed system labels under the null; not established by this computation",
            "bootstrap_interpretation": "Within-system multinomial resampling of archived coded rows, conditional on their empirical frequencies; not population uncertainty",
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "random_generator": "numpy.random.default_rng",
            "bit_generator": type(np.random.default_rng(1962).bit_generator).__name__,
            "permutation_algorithm": "One rng.permutation(outcomes) per repetition; fixed margins; Pearson chi-square >= observed - 1e-12",
            "permutation_p_formula": "(exceedances + 1) / (repetitions + 1)",
            "bootstrap_algorithm": "One rng.multinomial(row_total, row_probabilities) per system per repetition; percentile interval [2.5, 97.5]",
            "bootstrap_percentile_method": "NumPy default linear interpolation",
            "bootstrap_absent_category_handling": "Remove all-zero rows/columns for Cramer's V; a one-category draw receives V=0; counts reported per analysis",
            "variable_summary_sd_ddof": 1,
        },
        "system_order": SYSTEMS,
        "five_category_order": CATEGORIES_5,
        "three_category_order": CATEGORIES_3,
        "primary_four_system_five_category": analyze(five, 1962),
        "sensitivity_three_standalone_five_category": analyze(five[:3], 1963),
        "sensitivity_four_system_three_category": analyze(three, 1964, bootstrap_seed=1965),
        "sensitivity_three_standalone_three_category": analyze(three[:3], 1965, bootstrap_seed=1966),
    }
    if hashlib.sha256(INPUT.read_bytes()).hexdigest() != input_hash:
        raise RuntimeError("Input coding CSV changed during analysis; rerun against a stable file")
    write_variable_summary(rows)
    OUTPUT.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
