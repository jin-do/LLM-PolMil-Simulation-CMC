"""Meaningful boundary checks on copies of fixed diagnostic inputs."""
from pathlib import Path
import copy, importlib.util, unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('diagnostic_replay',ROOT/'code/reproduce_diagnostic.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.rows=m.read_csv(ROOT/'data/diagnostic/ai_review_40.csv')
        self.members=m.read_csv(ROOT/'data/diagnostic/membership.csv')
        self.reasons=m.read_csv(ROOT/'data/diagnostic/u_reason_assignments.csv')
    def check(self):return m.validate(self.rows,self.members,self.reasons)
    def test_independent_counts_and_shared_dependencies(self):
        # Separate scalar loop, without calling the aggregation function.
        totals={k:[0,0,0] for k in ['common_selected','representative_discrepancy']}
        for r in self.rows:
            scope='common_selected' if r['case_id'].startswith('HR-') else 'representative_discrepancy'
            totals[scope][{'C':0,'V':1,'U':2}[r['ai_status']]]+=1
        self.assertEqual(totals,{'common_selected':[15,11,12],'representative_discrepancy':[0,2,0]})
        groups={}
        for r in self.reasons:
            if r['dependency_group']:groups.setdefault(r['dependency_group'],set()).add(r['case_id'])
        self.assertEqual(groups,{'CLA-03-T4-missing-response':{'HR-005','HR-008'},'GPT-25-T2-missing-response':{'HR-014','HR-019'}})
        self.check()
    def test_duplicate_or_missing_case_rejected(self):
        self.rows[-1]=copy.deepcopy(self.rows[0])
        with self.assertRaises(ValueError):self.check()
    def test_common_denominator_contamination_rejected(self):
        self.members[0]['in_common_denominator']='true'
        with self.assertRaises(ValueError):self.check()
    def test_false_human_completion_rejected(self):
        self.rows[0]['human_status']='C'
        with self.assertRaises(ValueError):self.check()
    def test_invalid_run_rejected(self):
        self.rows[0]['run_id']='CLA-31'
        with self.assertRaises(ValueError):self.check()
    def test_duplicate_u_reason_rejected(self):
        self.reasons[-1]=copy.deepcopy(self.reasons[0])
        with self.assertRaises(ValueError):self.check()
    def test_missing_dependency_group_rejected(self):
        self.reasons[0]['dependency_group']=''
        with self.assertRaises(ValueError):self.check()
    def test_invalid_label_rejected(self):
        self.rows[0]['ai_status']='PASS'
        with self.assertRaises(ValueError):self.check()

if __name__=='__main__':unittest.main()
