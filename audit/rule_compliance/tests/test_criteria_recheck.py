import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('cr',ROOT/'code/recheck_criteria.py');cr=importlib.util.module_from_spec(spec);spec.loader.exec_module(cr)
class CriteriaRecheck(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=cr.read_csv(ROOT/'data/core/07_semantic_validation_ledger.csv');cls.assets=cr.read_csv(ROOT/'source_assets.csv');cls.common=cr.validate(cls.raw,cls.assets);cls.patches=json.loads((ROOT/'data/adjudication/patches.json').read_text());cls.decisions=cr.read_csv(ROOT/'data/adjudication/decisions.csv')
 def test_original_frame(self):self.assertEqual(len(self.common),1320)
 def test_zero_denominator(self):self.assertEqual(cr.percent(0,0),'')
 def test_duplicate_core_rejected(self):
  with self.assertRaises(ValueError):cr.validate(self.raw+[self.raw[0]],self.assets)
 def test_duplicate_selected_rejected(self):
  r=next(x for x in self.raw if x['metric_key'] not in cr.KEYS)
  with self.assertRaises(ValueError):cr.validate(self.raw+[r],self.assets)
 def test_fake_roster_rejected(self):
  a=copy.deepcopy(self.assets);a[0]['run_id']='GPT-99'
  with self.assertRaises(ValueError):cr.validate(self.raw,a)
 def test_invalid_label_rejected(self):
  r=copy.deepcopy(self.raw);next(x for x in r if x['metric_key'] in cr.KEYS)['status']='PASS'
  with self.assertRaises(ValueError):cr.validate(r,self.assets)
 def test_wrong_old_label_rejected(self):
  p=copy.deepcopy(self.patches);p[0]['legacy_status']='판정 불가'
  with self.assertRaises(ValueError):cr.apply(self.common,p,self.decisions)
 def test_duplicate_patch_rejected(self):
  with self.assertRaises(ValueError):cr.apply(self.common,self.patches+[self.patches[0]],self.decisions)
 def test_unknown_target_rejected(self):
  p=copy.deepcopy(self.patches);p[0]['check_id']='invented'
  with self.assertRaises(ValueError):cr.apply(self.common,p,self.decisions)
 def test_clear_counts(self):
  r=cr.aggregate(cr.apply(self.common,self.patches,self.decisions), 'x');self.assertEqual((r[0]['C'],r[0]['V'],r[0]['U']),(230,10,0));self.assertEqual((r[3]['C'],r[3]['V'],r[3]['U']),(180,20,160))
 def test_conservative_counts(self):
  r=cr.aggregate(cr.apply(self.common,self.patches,self.decisions,True),'x');self.assertEqual((r[0]['C'],r[0]['V'],r[0]['U']),(222,10,8))
 def test_no_source_mutation(self):
  old=copy.deepcopy(self.common);cr.apply(self.common,self.patches,self.decisions,True);self.assertEqual(old,self.common)
 def test_excerpts_match(self):self.assertEqual(cr.validate_evidence(ROOT,self.decisions),19)

class ManifestGuards(unittest.TestCase):
 def test_manifest_tamper_rejected(self):
  import tempfile,hashlib
  sp=importlib.util.spec_from_file_location('legacy',ROOT/'code/reproduce.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'data.txt').write_text('x');manifest=p/'manifest.csv';manifest.write_text('relative_path,bytes,sha256\ndata.txt,1,'+hashlib.sha256(b'x').hexdigest()+'\n');(p/'MANIFEST.sha256').write_text(hashlib.sha256(manifest.read_bytes()).hexdigest()+' manifest.csv\n');self.assertFalse(m.verify_manifest(p)['issues']);manifest.write_text(manifest.read_text()+'\n');self.assertTrue(m.verify_manifest(p)['issues'])
 def test_screening_is_not_adjudication(self):
  sp=importlib.util.spec_from_file_location('scr',ROOT/'code/repeat_screen.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);r=m.screen(ROOT);self.assertEqual(len(r),120);self.assertTrue(all(x['semantic_verdict'] is None for x in r))
