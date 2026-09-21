"""Fixed-label replay boundaries; no semantic-coding correctness claims."""
from pathlib import Path
import copy, importlib.util, unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('top1_replay',ROOT/'code/reproduce_top1.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Top1Tests(unittest.TestCase):
    def setUp(self):self.rows=m.read_csv(ROOT/'data/top1_source_recoding.csv')
    def test_independent_scalar_aggregation(self):
        # Independent direct scalar loop: no aggregation function called.
        values=[0]*6;system_n={};changed=0
        names=['Protracted stalemate','Internal collapse','Diplomatic resolution','Full-scale war','Limited conflict','']
        for r in self.rows:
            values[names.index(r['outcome_5'])]+=1
            system_n[r['system']]=system_n.get(r['system'],0)+1
            changed+=r['recoding_changed'].lower()=='true'
        self.assertEqual(values,[61,0,38,5,0,16]);self.assertEqual(changed,61)
        self.assertEqual(set(system_n.values()),{30});self.assertEqual(len(system_n),4)
        m.validate(self.rows)
    def test_duplicate_execution_rejected(self):
        self.rows[-1]=copy.deepcopy(self.rows[0])
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_wrong_system_rejected(self):
        self.rows[0]['system']='Claude Opus 4'
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_withheld_not_reclassified(self):
        r=next(r for r in self.rows if r['status']=='withheld');r['outcome_5']='Protracted stalemate'
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_withheld_reason_required(self):
        r=next(r for r in self.rows if r['status']=='withheld');r['reasoning']=''
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_wrong_change_flag_rejected(self):
        self.rows[0]['recoding_changed']='false'
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_source_traversal_rejected(self):
        self.rows[0]['raw_log_path']='runs/raw_logs/../../private.pdf'
        with self.assertRaises(ValueError):m.validate(self.rows)
    def test_missing_execution_rejected(self):
        self.rows.pop()
        with self.assertRaises(ValueError):m.validate(self.rows)

if __name__=='__main__':unittest.main()
