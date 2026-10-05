"""Reproduce Tables B2, D1, D2 and A2 from preserved local inputs.

Python standard library only; no network, model calls, or new outcome coding.
The numeric checks are conditional on the source-recorded states and named effects.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path, PurePosixPath


VARIABLES = ("Tension", "Diplomatic_Support", "Public_Opinion", "Leadership_Unity")
CATEGORIES = {
    "Protracted stalemate": "S",
    "Diplomatic resolution": "D",
    "Full-scale war": "W",
    "Internal collapse": "I",
    "Limited conflict": "L",
}
COLUMNS = ("S", "D", "W", "I", "L", "H")
SYSTEM_PREFIXES = {
    "GPT-4o": "GPT-4o",
    "Gemini_2.5_Flash": "Gemini 2.5 Flash",
    "Claude_Opus_4": "Claude Opus 4",
    "Perplexity_RAG": "Perplexity Pro",
}


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path):
    # Decimal retains the decimal values supplied in the preserved VDM.
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_float=Decimal)


def write_csv(path, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def local_path(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or ".." in rel.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Unsafe repository-relative path: {relative}")
    target = (Path(root) / Path(*rel.parts)).resolve()
    if not target.is_relative_to(Path(root).resolve()):
        raise ValueError(f"Path escapes repository: {relative}")
    return target


def verify_inputs(repo_root, provenance):
    verified = {}
    for name, spec in provenance["repository_inputs"].items():
        path = local_path(repo_root, spec["path"])
        payload = path.read_bytes()
        if spec["digest_kind"] == "sha256_lf_normalized":
            payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        elif spec["digest_kind"] != "sha256_bytes":
            raise ValueError(f"Unknown digest kind for {name}")
        actual = hashlib.sha256(payload).hexdigest()
        if actual != spec["sha256"]:
            raise ValueError(f"Input digest differs: {spec['path']}")
        verified[name] = {"path": spec["path"], "sha256": actual,
                          "digest_kind": spec["digest_kind"]}
    return verified


def validate_top1(rows):
    expected = {f"{prefix}-{n:02d}": system
                for prefix, system in SYSTEM_PREFIXES.items() for n in range(1, 31)}
    ids = [row["execution_id"] for row in rows]
    if len(rows) != 120 or len(set(ids)) != len(ids) or set(ids) != set(expected):
        raise ValueError("Top-1 roster must contain the 120 distinct preserved execution IDs")
    for row in rows:
        if row["system"] != expected[row["execution_id"]]:
            raise ValueError("Top-1 execution/system mismatch")
        if row["original_outcome"] not in CATEGORIES:
            raise ValueError("Unknown original outcome")
        if row["status"] == "confirmed":
            if row["outcome_5"] not in CATEGORIES:
                raise ValueError("Unknown classified outcome")
        elif row["status"] == "withheld":
            if row["outcome_5"] or not row["reasoning"].strip():
                raise ValueError("Withheld rows require empty outcome and an existing reason")
        else:
            raise ValueError("Unknown Top-1 status")
        changed = row["status"] == "confirmed" and row["outcome_5"] != row["original_outcome"]
        if row["recoding_changed"].lower() not in {"true", "false"}:
            raise ValueError("Invalid stored change flag")
        if (row["recoding_changed"].lower() == "true") != changed:
            raise ValueError("Stored change flag contradicts original and retrospective labels")


def outcome_comparison(rows):
    """Compare actual original/new labels, rather than summing stored change flags."""
    validate_top1(rows)
    counts = Counter()
    changed = unchanged = withheld = 0
    cases = []
    for row in rows:
        original = CATEGORIES[row["original_outcome"]]
        reviewed = CATEGORIES[row["outcome_5"]] if row["status"] == "confirmed" else "H"
        counts[original, reviewed] += 1
        if reviewed == "H":
            comparison = "withheld"
            withheld += 1
        elif original == reviewed:
            comparison = "same"
            unchanged += 1
        else:
            comparison = "different"
            changed += 1
        cases.append({"execution_id": row["execution_id"], "original": original,
                      "retrospective": reviewed, "comparison": comparison})
    matrix = []
    for label, code in CATEGORIES.items():
        matrix.append({"original_label": label, **{col: counts[code, col] for col in COLUMNS},
                       "Total": sum(counts[code, col] for col in COLUMNS)})
    matrix.append({"original_label": "Total",
                   **{col: sum(counts[code, col] for code in CATEGORIES.values())
                      for col in COLUMNS}, "Total": len(rows)})
    classified = changed + unchanged
    percent = ((Decimal(changed) * 100 / classified).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
               if classified else None)
    summary = {"executions": len(rows), "classified": classified, "withheld": withheld,
               "different": changed, "same": unchanged,
               "different_percent_of_classified": str(percent) if percent is not None else None,
               "interpretation": "Coding-record disagreement; not a verified error rate or correction."}
    return matrix, summary, cases


def decimal_vector(values):
    if len(values) != len(VARIABLES):
        raise ValueError("State vector must have four components in the documented order")
    vector = tuple(Decimal(str(value)) for value in values)
    if any(not value.is_finite() or not Decimal(0) <= value <= Decimal(1) for value in vector):
        raise ValueError("Source state must contain finite values in [0, 1]")
    return vector


def conditional_update(prior, effect_names, effects):
    prior = decimal_vector(prior)
    if not effect_names or len(set(effect_names)) != len(effect_names):
        raise ValueError("Each named effect row must be applied exactly once")
    rows = []
    for name in effect_names:
        if name not in effects or set(effects[name]) != set(VARIABLES):
            raise ValueError(f"Unknown or incomplete VDM effect row: {name}")
        effect = tuple(Decimal(str(effects[name][key])) for key in VARIABLES)
        if any(not value.is_finite() for value in effect):
            raise ValueError(f"Nonfinite effect value: {name}")
        rows.append(effect)
    raw = tuple(value + sum((row[i] for row in rows), Decimal(0)) for i, value in enumerate(prior))
    checked = tuple(max(Decimal(0), min(Decimal(1), value)) for value in raw)
    return raw, checked


def number(value):
    return f"{value:.2f}"


def vector_text(values):
    return "(" + ", ".join(number(value) for value in values) + ")"


def calculate_cases(records, vdm):
    effects = vdm["event_driven_adjustments"]
    case_ids = [case["case_id"] for case in records]
    if not records or len(case_ids) != len(set(case_ids)):
        raise ValueError("Conditional cases need distinct IDs")
    detail, summary = [], []
    for case in records:
        prior, reported = decimal_vector(case["recorded_prior"]), decimal_vector(case["reported_result"])
        if any(not isinstance(page, int) or page < 1
               for key in ("prior_pages", "effects_pages", "reported_pages") for page in case[key]):
            raise ValueError("PDF pages must be positive one-based integers")
        # Intentionally use this case's recorded prior, never the preceding checked vector.
        raw, checked = conditional_update(prior, case["effect_names"], effects)
        differing = [key for key, actual, expected in zip(VARIABLES, reported, checked) if actual != expected]
        summary.append({"case_id": case["case_id"], "table": case["table"], "turn": case["turn"],
                        "scenario": case["scenario"], "recorded_prior": vector_text(prior),
                        "effect_names": " + ".join(case["effect_names"]), "checked": vector_text(checked),
                        "reported": vector_text(reported), "differing_components": "; ".join(differing) or "None"})
        for i, key in enumerate(VARIABLES):
            detail.append({"case_id": case["case_id"], "variable": key, "recorded_prior": number(prior[i]),
                           "named_effects": json.dumps({name: number(Decimal(str(effects[name][key])))
                                                       for name in case["effect_names"]}, sort_keys=True),
                           "unclipped": number(raw[i]), "checked": number(checked[i]),
                           "reported": number(reported[i]), "matches": checked[i] == reported[i],
                           "clipped": raw[i] != checked[i]})
    return summary, detail


def infer_repo_root(start):
    for candidate in (Path(start).resolve(), *Path(start).resolve().parents):
        if (candidate / "coding/top1_reanalysis/data/top1_source_recoding.csv").is_file():
            return candidate
    raise ValueError("Cannot locate repository; pass --repo-root")


def reproduce(module_root, repo_root, output):
    module_root, repo_root, output = Path(module_root), Path(repo_root), Path(output)
    provenance = read_json(module_root / "data/provenance.json")
    verified = verify_inputs(repo_root, provenance)
    rows = read_csv(local_path(repo_root, provenance["repository_inputs"]["top1"]["path"]))
    matrix, comparison, comparisons = outcome_comparison(rows)
    vdm = read_json(local_path(repo_root, provenance["repository_inputs"]["vdm"]["path"]))
    cases = read_json(module_root / "data/conditional_cases.json")
    if tuple(cases["variable_order"]) != VARIABLES:
        raise ValueError("Conditional-input variable order mismatch")
    summary, detail = calculate_cases(cases["cases"], vdm)
    links = read_csv(module_root / "data/path_source_register.csv")
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "table_b2_counts.csv", matrix)
    write_csv(output / "outcome_label_comparison.csv", comparisons)
    write_csv(output / "table_d1_source_register.csv", links)
    write_csv(output / "table_d2_conditional_updates.csv", [row for row in summary if row["table"] == "D2"])
    write_csv(output / "table_a2_conditional_update.csv", [row for row in summary if row["table"] == "A2"])
    write_csv(output / "conditional_variable_checks.csv", detail)
    result = {"module": "revision29-later-calculation-supplement", "verified_repository_inputs": verified,
              "outcome_comparison": comparison, "conditional_cases": summary,
              "scope": "Fixed coding comparison and conditional local calculations, not new simulations, semantic recoding, or independent validation."}
    (output / "reproduction.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root or infer_repo_root(args.module_root)
    result = reproduce(args.module_root, repo, args.out)
    print(json.dumps({"status": "REPRODUCED", **result["outcome_comparison"],
                      "conditional_cases": len(result["conditional_cases"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
