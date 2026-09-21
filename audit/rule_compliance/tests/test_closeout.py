import unittest,sys,json,csv,tempfile,copy
from pathlib import Path
from collections import Counter
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code'))
from reproduce import *

class CloseoutTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.req=load_csv(ROOT/'protocol/control_requirements.csv')
  cls.events,cls.trules,cls.paths=source_rules(cls.req)
  cls.core=load_csv(ROOT/'data/core/07_semantic_validation_ledger.csv')
 def test_core_grid_complete_unique(self):
  rr=[r for r in self.core if r['metric_key'] in KEYS]
  self.assertEqual(len(rr),1320);self.assertEqual(len({(r['run_id'],r['metric_key']) for r in rr}),1320)
  self.assertEqual(len({r['run_id'] for r in rr}),120)
 def test_common_selected_not_mixed(self):
  self.assertEqual(sum(r['metric_key'] not in KEYS for r in self.core),67)
  self.assertTrue(all(included(r) for r in self.core))
 def test_all_source_ledger_check_ids_unique(self):
  for p in [ROOT/'data/core/07_semantic_validation_ledger.csv',*sorted((ROOT/'data/supplemental_partial').glob('*ledger.csv'))]:
   with self.subTest(file=p.name):unique(load_csv(p))
 def test_zero_denominator_is_undefined(self):
  self.assertEqual(rates(0,0,0),('',''));self.assertEqual(rates(0,0,5),('0.0000',''))
 def test_candidate_and_unreviewed_excluded(self):
  self.assertFalse(included({'candidate_only':'true','review_completed':'true'}))
  self.assertFalse(included({'review_completed':'false'}))
  self.assertTrue(included({'review_completed':'True','candidate_only':'False'}))
 def test_candidate_subset_not_promoted(self):
  rr=load_csv(ROOT/'data/diagnostic_only/v3_arithmetic_candidates_subset.csv')
  self.assertEqual(len(rr),1717);self.assertTrue(all(true(r['candidate_only']) and not included(r) for r in rr))
 def test_clipping_bounds(self):
  for x,y in [('-0.1','0'),('0','0'),('0.85','0.85'),('1','1'),('1.15','1')]:self.assertEqual(clip(D(x)),D(y))
 def test_original_threshold_boundary(self):
  status,gates=threshold_class(['.8','.5','.4'],'yes',False,self.trules)
  self.assertEqual(status,V);self.assertTrue(all(g=='Disabled' for g in gates.values()))
 def test_no_retrospective_conflict_priority(self):
  status,gates=threshold_class(['.85','.65','.70'],'yes',False,self.trules)
  self.assertEqual(status,U);self.assertEqual(gates['Tension'],'Disabled')
 def test_no_negotiation_not_claimed_gate_enforcement(self):
  status,_=threshold_class(['.9','.4','.3'],'no',False,self.trules);self.assertEqual(status,C)
 def test_state_timing_unknown_remains_U(self):
  self.assertEqual(threshold_class(['.6','.6','.6'],'yes',True,self.trules)[0],U)
  self.assertEqual(threshold_class(None,'yes',False,self.trules)[0],U)
 def test_CLA_full_row_calculation(self):
  self.assertEqual(clip(D('.70')+self.events['Strong_Leadership']['Public_Opinion']+self.events['Diplomatic_Success']['Public_Opinion']),D('.85'))
  self.assertNotEqual(D('.85'),D('.80'))
 def test_matching_not_based_on_values_or_parser_ids(self):
  a=dict(run_id='X',source_file='x.pdf',page='1',turn='2',branch='A',actor='US',variable='Tension',evidence='x = y',check_id='old',status=C,reported_value='1',recomputed_value='1')
  b=dict(a,check_id='new');self.assertEqual(reconcile([a],[b])[0]['match_cardinality'],'1:1')
  b['page']='2';self.assertEqual({r['match_cardinality'] for r in reconcile([a],[b])},{'old_only','candidate_only'})
 def test_multiple_matches_are_not_forced(self):
  a=dict(run_id='X',source_file='x',page='1',turn='1',branch='A',actor='',variable='Tension',evidence='same source',check_id='a',status=C,reported_value='1',recomputed_value='1')
  b=dict(a,check_id='b');c=dict(a,check_id='c');self.assertEqual(reconcile([a],[b,c])[0]['match_cardinality'],'1:N')
 def test_duplicate_ids_detected(self):
  with self.assertRaises(ValueError):unique([{'check_id':'x'},{'check_id':'x'}])
 def test_source_index_unique_and_hashes_well_formed(self):
  rr=load_csv(ROOT/'source_assets.csv');unique(rr,'run_id');self.assertEqual(len(rr),120)
  self.assertTrue(all(re.fullmatch('[0-9a-f]{64}',r['sha256']) for r in rr))
 def test_unknown_status_not_accepted(self):
  self.assertNotIn('human_verified',VALID)
 def test_no_human_completion_claim(self):
  spec=load_json(ROOT/'protocol/analysis_spec.json');self.assertIn('pending',spec['human_review'])
  vi=load_json(ROOT/'evidence/visual_inspection_record.json');self.assertFalse(vi['human_reviewed'])
 def test_original_rule_index_not_future_proposed_precedence(self):
  self.assertEqual(self.trules['$.decision_options.Tension[">=0.8"].Diplomatic_Negotiation'],'Disabled')
  self.assertEqual(self.trules['$.decision_options.Diplomatic_Support[">0.5"].Diplomatic_Negotiation'],'Strongly Encouraged')
if __name__=='__main__':unittest.main(verbosity=2)
