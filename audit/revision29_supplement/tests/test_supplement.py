"""Regression and failure checks for the supplemental calculations (stdlib)."""
import copy
from decimal import Decimal
import importlib.util
import os
from pathlib import Path
import shutil
import unittest
from uuid import uuid4

MODULE_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reproduce_supplement", MODULE_ROOT / "code/reproduce_supplement.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SupplementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configured = os.environ.get("POLMIL_REPO_ROOT")
        cls.repo = Path(configured) if configured else module.infer_repo_root(Path.cwd())
        cls.provenance = module.read_json(MODULE_ROOT / "data/provenance.json")
        cls.rows = module.read_csv(cls.repo / cls.provenance["repository_inputs"]["top1"]["path"])
        cls.vdm = module.read_json(cls.repo / cls.provenance["repository_inputs"]["vdm"]["path"])
        cls.cases = module.read_json(MODULE_ROOT / "data/conditional_cases.json")["cases"]

    def test_table_b2_and_disagreement(self):
        matrix, summary, cases = module.outcome_comparison(self.rows)
        expected = [
            [25, 11, 1, 0, 0, 3, 40], [14, 15, 0, 0, 0, 6, 35],
            [16, 10, 3, 0, 0, 6, 35], [6, 1, 1, 0, 0, 1, 9],
            [0, 1, 0, 0, 0, 0, 1], [61, 38, 5, 0, 0, 16, 120],
        ]
        self.assertEqual([[row[col] for col in (*module.COLUMNS, "Total")] for row in matrix], expected)
        self.assertEqual((summary["classified"], summary["different"], summary["same"], summary["withheld"]),
                         (104, 61, 43, 16))
        self.assertEqual(summary["different_percent_of_classified"], "58.7")
        self.assertEqual(len(cases), 120)

    def test_duplicate_and_invalid_original_are_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[1] = copy.deepcopy(rows[0])
        with self.assertRaisesRegex(ValueError, "120 distinct"):
            module.outcome_comparison(rows)
        rows = copy.deepcopy(self.rows)
        rows[0]["original_outcome"] = "unknown"
        with self.assertRaisesRegex(ValueError, "original outcome"):
            module.outcome_comparison(rows)

    def test_inconsistent_status_and_stored_change_flag_are_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["recoding_changed"] = "False" if rows[0]["recoding_changed"] == "True" else "True"
        with self.assertRaisesRegex(ValueError, "Stored change flag"):
            module.outcome_comparison(rows)
        rows = copy.deepcopy(self.rows)
        rows[0]["status"] = "withheld"
        with self.assertRaisesRegex(ValueError, "empty outcome"):
            module.outcome_comparison(rows)

    def test_no_classified_denominator_is_undefined(self):
        rows = copy.deepcopy(self.rows)
        for row in rows:
            row.update(status="withheld", outcome_5="", reasoning="Synthetic test only", recoding_changed="False")
        _, summary, _ = module.outcome_comparison(rows)
        self.assertIsNone(summary["different_percent_of_classified"])

    def test_conditional_tables_d2_and_a2(self):
        summary, detail = module.calculate_cases(self.cases, self.vdm)
        expected = {
            "CLA-01-S1-T2": ("(0.75, 0.68, 0.58, 0.85)", "Diplomatic_Support; Public_Opinion; Leadership_Unity"),
            "CLA-01-S1-T3": ("(0.65, 0.85, 0.70, 0.95)", "Diplomatic_Support"),
            "CLA-01-S1-T4": ("(0.55, 1.00, 0.80, 1.00)", "None"),
            "CLA-01-S3-T4": ("(0.75, 0.80, 0.85, 1.00)", "Public_Opinion"),
        }
        self.assertEqual({row["case_id"]: (row["checked"], row["differing_components"]) for row in summary}, expected)
        self.assertEqual(len(detail), 16)
        unity = next(row for row in detail if row["case_id"] == "CLA-01-S3-T4" and row["variable"] == "Leadership_Unity")
        self.assertEqual((unity["unclipped"], unity["checked"], unity["clipped"]), ("1.15", "1.00", True))

    def test_calculations_do_not_propagate_corrected_states(self):
        # Reordering or altering an earlier prior must not change later independent checks.
        original, _ = module.calculate_cases(self.cases, self.vdm)
        altered = copy.deepcopy(self.cases)
        altered[0]["recorded_prior"][1] = "0.20"
        changed, _ = module.calculate_cases(altered, self.vdm)
        self.assertNotEqual(original[0]["checked"], changed[0]["checked"])
        self.assertEqual(original[1:], changed[1:])
        reordered, _ = module.calculate_cases(list(reversed(self.cases)), self.vdm)
        self.assertEqual(original, list(reversed(reordered)))

    def test_effect_rows_are_complete_and_clipping_follows_sum(self):
        # A synthetic boundary case distinguishes end-of-sum clipping from per-effect clipping.
        effects = {"rise": {key: Decimal("0.20") for key in module.VARIABLES},
                   "fall": {key: Decimal("-0.10") for key in module.VARIABLES}}
        raw, checked = module.conditional_update(["0.95"] * 4, ["rise", "fall"], effects)
        self.assertEqual(raw, (Decimal("1.05"),) * 4)
        self.assertEqual(checked, (Decimal("1"),) * 4)
        _, checked = module.conditional_update(["0.01"] * 4, ["fall"], effects)
        self.assertEqual(checked, (Decimal("0"),) * 4)
        with self.assertRaisesRegex(ValueError, "exactly once"):
            module.conditional_update(["0.5"] * 4, ["rise", "rise"], effects)
        del effects["rise"]["Public_Opinion"]
        with self.assertRaisesRegex(ValueError, "incomplete"):
            module.conditional_update(["0.5"] * 4, ["rise"], effects)

    def test_input_digests_and_path_safety(self):
        verified = module.verify_inputs(self.repo, self.provenance)
        self.assertEqual(set(verified), {"top1", "vdm", "claude_01_pdf"})
        bad = copy.deepcopy(self.provenance)
        bad["repository_inputs"]["vdm"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "digest differs"):
            module.verify_inputs(self.repo, bad)
        for path in ("../outside", "/absolute", "C:/outside", "folder\\outside"):
            with self.assertRaises(ValueError):
                module.local_path(self.repo, path)

    def test_full_reproduction_writes_traceable_outputs(self):
        directory = (MODULE_ROOT / ("test-output-" + uuid4().hex)).resolve()
        self.assertTrue(directory.is_relative_to(MODULE_ROOT.resolve()))
        directory.mkdir()
        try:
            result = module.reproduce(MODULE_ROOT, self.repo, directory)
            self.assertEqual(result["outcome_comparison"]["different"], 61)
            self.assertEqual(len(module.read_csv(Path(directory) / "table_d1_source_register.csv")), 6)
            self.assertEqual(len(module.read_csv(Path(directory) / "table_d2_conditional_updates.csv")), 3)
            self.assertEqual(len(module.read_csv(Path(directory) / "table_a2_conditional_update.csv")), 1)
            self.assertEqual(len(module.read_csv(Path(directory) / "outcome_label_comparison.csv")), 120)
        finally:
            shutil.rmtree(directory)


if __name__ == "__main__":
    unittest.main()
