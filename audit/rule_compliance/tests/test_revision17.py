"""Additional error-injection and independent-logic checks, prepared 2026-09-22."""
import unittest,csv,json,copy,tempfile,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import recheck_criteria as cr
import reproduce_revision17 as rev

class Revision17Guards(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=cr.read_csv(ROOT/'data/core/07_semantic_validation_ledger.csv');cls.assets=cr.read_csv(ROOT/'source_assets.csv')
  cls.patches=json.loads((ROOT/'data/adjudication/patches.json').read_text(encoding='utf8'));cls.decisions=cr.read_csv(ROOT/'data/adjudication/decisions.csv')
 def mutated_file(self,edit):
  rows=copy.deepcopy(self.raw);edit(rows)
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'mutated.csv';cr.write_csv(p,rows)
   with self.assertRaises(ValueError):cr.validate(cr.read_csv(p),self.assets)
 def test_missing_common_row_file(self):self.mutated_file(lambda r:r.pop(0))
 def test_invalid_run_in_common_file(self):self.mutated_file(lambda r:r[0].update(run_id='GPT-99'))
 def test_unique_duplicate_common_observation(self):
  def edit(r):
   x=dict(r[0]);x['check_id']='injected-unique-id';r.append(x)
  self.mutated_file(edit)
 def test_selected_67_cannot_enter_common_grid(self):
  def edit(r):
   for x in r:
    if x['metric_key'] not in cr.KEYS:x['metric_key']='T2_BRANCH'
  self.mutated_file(edit)
 def test_already_applied_patch_rejected(self):
  common=cr.validate(self.raw,self.assets);applied=cr.apply(common,self.patches,self.decisions,True)
  with self.assertRaisesRegex(ValueError,'legacy label mismatch'):cr.apply(applied,self.patches,self.decisions,True)
 def test_changed_old_label_from_temporary_patch_file(self):
  pp=copy.deepcopy(self.patches);pp[0]['legacy_status']='판정 불가'
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'patches.json';p.write_text(json.dumps(pp),encoding='utf8')
   with self.assertRaises(ValueError):cr.apply(cr.validate(self.raw,self.assets),json.loads(p.read_text()),self.decisions,True)
 def test_turn_field_mismatch_rejected(self):
  current=cr.apply(cr.validate(self.raw,self.assets),self.patches,self.decisions,True);current[0]['turn']='4'
  with self.assertRaisesRegex(ValueError,'metric/turn'):rev.aggregate_turns(current)
 def test_zero_denominator_blank_and_U_not_V(self):
  self.assertEqual(rev.percent(0,0),'');self.assertEqual(rev.percent(0,12),'0.00')
 def test_independent_crosscheck_detects_wrong_output_count(self):
  current=cr.apply(cr.validate(self.raw,self.assets),self.patches,self.decisions,True);turns=rev.aggregate_turns(current);turns[0]['C']+=1
  with self.assertRaises(ValueError):rev.independent_crosscheck(self.raw,current,self.patches,turns)
 def test_manifest_modified_input_file_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp);(p/'input.csv').write_bytes(b'correct')
   cr.write_csv(p/'PACKAGE_MANIFEST.csv',[{'relative_path':'input.csv','bytes':7,'sha256':hashlib.sha256(b'correct').hexdigest()}]);(p/'PACKAGE_MANIFEST.sha256').write_text(hashlib.sha256((p/'PACKAGE_MANIFEST.csv').read_bytes()).hexdigest()+' PACKAGE_MANIFEST.csv\n')
   rev.verify_package(p);(p/'input.csv').write_bytes(b'incorrect')
   with self.assertRaisesRegex(ValueError,'manifest mismatch'):rev.verify_package(p)
 def test_diagnostic_ids_not_added_to_current_common(self):
  current=cr.apply(cr.validate(self.raw,self.assets),self.patches,self.decisions,True)
  self.assertEqual(len(current),1320);self.assertTrue(all(not r['check_id'].startswith('HR-') for r in current))

if __name__=='__main__':unittest.main(verbosity=2)
