"""Compare numeric manuscript targets against public fixed-input reproduction.

Prepared 2026-09-22, Python 3.10+ standard library only. Selects named records,
not records found by their numeric values. Does not change source data.
"""
from pathlib import Path
from collections import Counter
import argparse
import csv
import hashlib
import json
import math
import re


class NotReproduced(Exception):
    pass


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Reader:
    def __init__(self, repo, results):
        self.repo, self.results = repo.resolve(), results.resolve()
        self.cache = {}
        self.locations = []

    def file(self, scope, rel):
        root = self.repo if scope == "repo" else self.results
        path = (root / rel).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Source path escapes supplied root")
        if not path.is_file():
            raise NotReproduced(f"Missing {scope} file: {rel}")
        return path

    def read(self, scope, rel, kind):
        path = self.file(scope, rel)
        key = (scope, rel, kind)
        if key not in self.cache:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                self.cache[key] = list(csv.DictReader(handle)) if kind == "csv" else json.load(handle)
        return self.cache[key]

    def evaluate(self, x):
        if isinstance(x, list):
            return [self.evaluate(v) for v in x]
        if not isinstance(x, dict):
            return x  # Only explicit arithmetic factors/scale constants occur in specs.
        if "unresolved" in x:
            raise NotReproduced(x["unresolved"])
        if "label_code" in x:
            value = self.evaluate(x["label_code"])
            return {"준수": "C", "위반": "V", "판정 불가": "U", "적용 대상 아님": "NA"}[value]
        if "regex_float" in x:
            value = self.evaluate(x["regex_float"])
            matched = re.search(x["pattern"], value)
            if not matched:
                raise ValueError("Documented numeric rule pattern not found")
            return float(matched.group(1))
        if "csv" in x:
            scope = x.get("scope", "results")
            all_rows = self.read(scope, x["csv"], "csv")
            rows = [(i, r) for i, r in enumerate(all_rows, 2) if all(
                str(r.get(k, "")) in list(map(str, v)) if isinstance(v, list) else str(r.get(k, "")) == str(v)
                for k, v in x.get("where", {}).items())]
            self.locations.append({"scope": scope, "file": x["csv"], "selector": x.get("where", {}),
                                   "csv_rows": [i for i, _ in rows], "field": x.get("field"), "op": x.get("op", "field")})
            op = x.get("op", "field")
            if op == "count":
                value = len(rows)
            elif op == "distinct_count":
                value = len({r[x["field"]] for _, r in rows})
            elif op == "sum":
                value = sum(float(r[x["field"]]) for _, r in rows)
            elif op == "values":
                value = [r[x["field"]] for _, r in rows]
            else:
                if len(rows) != 1:
                    raise ValueError(f"Selector must find one record: {x['csv']} {x.get('where')} found {len(rows)}")
                value = rows[0][1][x["field"]]
            if x.get("cast") == "int":
                value = int(value)
            elif x.get("cast") == "float":
                value = float(value)
            if "round" in x:
                value = round(value, x["round"])
            return value
        if "json" in x:
            scope = x.get("scope", "results")
            value = self.read(scope, x["json"], "json")
            for step in x.get("path", []):
                value = value[step]
            self.locations.append({"scope": scope, "file": x["json"], "json_path": x.get("path", [])})
            return value
        if "calc" in x:
            vals = [self.evaluate(v) for v in x["args"]]
            op = x["calc"]
            if op == "sum": value = sum(vals)
            elif op == "sub": value = vals[0] - vals[1]
            elif op == "mul": value = math.prod(vals)
            elif op == "div":
                if vals[1] == 0: raise NotReproduced("Undefined zero denominator")
                value = vals[0] / vals[1]
            elif op == "len": value = len(vals[0])
            elif op == "min": value = min(vals)
            elif op == "max": value = max(vals)
            else: raise ValueError("Unknown calculation: " + op)
            return round(value, x["round"]) if "round" in x else value
        return {k: self.evaluate(v) for k, v in x.items()}


def equivalent(expected, actual):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and set(expected) == set(actual) and all(equivalent(expected[k], actual[k]) for k in expected)
    if isinstance(expected, list):
        return isinstance(actual, list) and len(expected) == len(actual) and all(equivalent(a, b) for a, b in zip(expected, actual))
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        return isinstance(actual, (int, float)) and math.isclose(expected, actual, rel_tol=0, abs_tol=1e-9)
    return expected == actual


def verify(repo, results, out, spec_path=None):
    repo, results, out = Path(repo), Path(results), Path(out)
    spec_path = Path(spec_path) if spec_path else Path(__file__).resolve().parents[1] / "claim_spec.json"
    specs = json.loads(spec_path.read_text(encoding="utf-8"))["claims"]
    reader = Reader(repo, results)
    output = []
    for spec in specs:
        reader.locations = []
        actual = None
        notes = ""
        hashes = []
        status = "NOT_REPRODUCED"
        try:
            for rel in spec["criteria"] + spec["code"]:
                reader.file("repo", rel)
            for source in spec["inputs"]:
                path = reader.file("repo", source["path"])
                actual_hash = digest(path)
                hashes.append({"path": source["path"], "sha256": actual_hash})
                if actual_hash != source["sha256"]:
                    raise ValueError("Input hash mismatch: " + source["path"])
            actual = reader.evaluate(spec["expression"])
            status = "MATCH_REPRODUCED" if equivalent(spec["expected"], actual) else "MISMATCH"
        except (NotReproduced, FileNotFoundError) as exc:
            notes = str(exc)
        except Exception as exc:
            status = "ERROR"
            notes = str(exc)
        output.append({"claim_id": spec["claim_id"], "anchor": spec["anchor"], "label": spec["label"],
                       "expected": spec["expected"], "actual": actual, "status": status,
                       "input_sha256": hashes, "criteria": spec["criteria"], "code": spec["code"],
                       "command": spec["command"], "analysis_version": spec["analysis_version"],
                       "filter_and_denominator": spec["filter_and_denominator"],
                       "result_locations": reader.locations, "scope": spec["scope"], "unresolved": notes})
    counts = dict(sorted(Counter(r["status"] for r in output).items()))
    summary = {"claims": len(output), "status_counts": counts,
               "interpretation": "Computational matching of specified numeric targets only; no fresh scientific recoding or independent human validation",
               "manuscript_prose_in_public_spec": False}
    out.mkdir(parents=True, exist_ok=True)
    (out / "claim_comparison.json").write_text(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (out / "claim_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (out / "claim_comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()} for row in output)
    print(json.dumps(summary, ensure_ascii=True, sort_keys=True))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = verify(args.repo, args.results, args.out)
    if summary["status_counts"].get("MISMATCH", 0) or summary["status_counts"].get("ERROR", 0):
        raise SystemExit(1)
