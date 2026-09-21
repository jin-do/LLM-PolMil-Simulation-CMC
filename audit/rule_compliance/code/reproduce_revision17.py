"""2026-09-22 preparation-stage wrapper for revision 17 fixed-label replay.
Reuses preserved functions; no AI calls, semantic recoding, network or source edits.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal,ROUND_HALF_EVEN
import csv,json,sys,hashlib,runpy,argparse
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
sys.path.insert(0,str(ROOT/'code'))
import reproduce as legacy
import recheck_criteria as criteria

def percent(n,d,digits=2):
 return '' if d==0 else str((Decimal(n)*100/Decimal(d)).quantize(Decimal(1).scaleb(-digits),rounding=ROUND_HALF_EVEN))
def verify_package(repo):
 rows=legacy.load_csv(repo/'PACKAGE_MANIFEST.csv')
 if legacy.sha(repo/'PACKAGE_MANIFEST.csv')!=(repo/'PACKAGE_MANIFEST.sha256').read_text().split()[0]:raise ValueError('manifest checksum mismatch')
 seen=set()
 for r in rows:
  p=repo/r['relative_path']
  if p.resolve().is_relative_to(repo.resolve()) is False:raise ValueError('manifest path escape')
  if r['relative_path'] in seen:raise ValueError('duplicate manifest entry')
  seen.add(r['relative_path'])
  if not p.is_file() or p.stat().st_size!=int(r['bytes']) or legacy.sha(p)!=r['sha256']:raise ValueError('manifest mismatch: '+r['relative_path'])
 return len(rows)

def aggregate_turns(rows):
 result=[]
 for domain,keys in criteria.GROUPS.items():
  for turn in sorted({k[1] for k in keys}):
   rr=[r for r in rows if r['metric_key'] in keys and r['metric_key'][1]==turn]
   if any(str(r['turn']).replace('T','')!=turn for r in rr):raise ValueError('metric/turn discrepancy')
   c=Counter(r['status'] for r in rr);C,V,U,NA=[c[x] for x in [legacy.C,legacy.V,legacy.U,legacy.NA]]
   if len(rr)!=(240 if turn=='1' else 120):raise ValueError('turn grid denominator')
   result.append(dict(domain=domain,turn=int(turn),unit='run-country' if turn=='1' else 'run-turn',C=C,V=V,U=U,NA=NA,assessability_denominator=C+V+U,compliance_denominator=C+V,assessable_percent=percent(C+V,C+V+U),conditional_compliance_percent=percent(C,C+V)))
 return result

def independent_crosscheck(raw,current,patches,turns):
 # No call to the production apply, aggregate, or turn aggregation functions.
 original={r['check_id']:r for r in raw if r['metric_key'].endswith(('_ROLE','_BRANCH','_EVENT','_PARENT_COVERAGE')) and r['metric_key'] in criteria.KEYS}
 expected={k:r['status'] for k,r in original.items()}
 for patch in patches:
  if expected[patch['check_id']]!=patch['legacy_status']:raise ValueError('independent old label mismatch')
  expected[patch['check_id']]=patch['proposed_status']
 if expected!={r['check_id']:r['status'] for r in current}:raise ValueError('independent item label disagreement')
 for t in turns:
  sums={x:0 for x in [legacy.C,legacy.V,legacy.U,legacy.NA]}
  for r in original.values():
   if r['metric_key'] not in criteria.GROUPS[t['domain']] or int(r['metric_key'][1])!=t['turn']:continue
   sums[expected[r['check_id']]]+=1
  if list(sums.values())!=[t[x] for x in ['C','V','U','NA']]:raise ValueError('independent turn counts differ')
 return {'common_rows':len(expected),'selected_rows_excluded':len(raw)-len(expected),'item_labels_match':True,'all_turn_counts_match':True,'method':'separate dictionary patch and nested integer-count loops; no production aggregate/apply call'}

def run_external(path,args):
 previous=sys.argv[:]
 try:
  sys.argv=[str(path),*map(str,args)];runpy.run_path(str(path),run_name='__main__')
 finally:sys.argv=previous

def run(out,check_manifest=True):
 out=out.resolve()
 for p in [REPO/'coding',REPO/'docs',ROOT]:
  if out==p or p in out.parents:raise ValueError('Output must be outside input modules (use repo_overlay/reproduced)')
 checked=verify_package(REPO) if check_manifest else 0
 out.mkdir(parents=True,exist_ok=True)
 legacy.tables(ROOT,out/'legacy_fixed');legacy.conflicts(ROOT,out/'legacy_fixed')
 info=criteria.run(ROOT,out/'criteria')
 raw=legacy.load_csv(ROOT/'data/core/07_semantic_validation_ledger.csv')
 current=legacy.load_csv(out/'criteria/conservative_common_1320.csv')
 patches=legacy.load_json(ROOT/'data/adjudication/patches.json');decisions={r['review_id']:r for r in legacy.load_csv(ROOT/'data/adjudication/decisions.csv')}
 turns=aggregate_turns(current)
 legacy.write_csv(out/'turn_summary.csv',turns)
 domains=criteria.aggregate(current,'conservative_boundaries')
 for d in domains:
  for key in ['C','V','U','NA']:
   if sum(t[key] for t in turns if t['domain']==d['domain'])!=d[key]:raise ValueError('turn/domain mismatch')
  for key in ['assessable_percent','conditional_compliance_percent']:
   d[key]=str(Decimal(d[key]).quantize(Decimal('.01'))) if d[key] else ''
 legacy.write_csv(out/'table4.csv',domains)
 changes=[]
 for p in patches:
  d=decisions[p['review_id']]
  changes.append(dict(check_id=p['check_id'],review_id=p['review_id'],run_id=p['run_id'],metric_key=p['metric_key'],before=p['legacy_status'],after=p['proposed_status'],tier=p['tier'],reason=d['reason'],source_path=d['source_path'],page=d['source_page'],source_sha256=d['pdf_sha256'],criteria_version='criteria-context-v1',actor='AI contextual review',human_record_verified=False,state='applied once in revision17 conservative set'))
 legacy.write_csv(out/'adjudication_change_history.csv',changes)
 independent=independent_crosscheck(raw,current,patches,turns)
 legacy.write_json(out/'independent_crosscheck.json',independent)
 mr=legacy.load_csv(ROOT/'data/supplemental_partial/fresh_marker_results_120.csv')
 if len(mr)!=120 or {r['run_id'] for r in mr}!=criteria.EXPECTED:raise ValueError('marker roster mismatch')
 markers=[]
 for key in ['readable_text','artifact_reference','explicit_result_log_label','all_four_state_dimensions','trigger_or_threshold','variable_status_label','explicit_reconfirm_variable_status','metadata_labels_present','independent_checker_phrase']:
  if any(r[key] not in ['True','False'] for r in mr):raise ValueError('invalid marker bool')
  found=sum(r[key]=='True' for r in mr)
  markers.append(dict(marker=key,n=len(mr),found=found,not_found=len(mr)-found,not_found_percent=percent(len(mr)-found,len(mr),1),scope='fixed per-PDF marker observations reaggregated; no fresh PDF extraction in this command'))
 legacy.write_csv(out/'marker_summary.csv',markers)
 # Optional modules are required when integrated; explicit paths only, no external folder discovery.
 extension=ROOT/'protocol/module_commands.json'
 if extension.exists():
  for m in legacy.load_json(extension):
   args=[str(out/x['output']) if isinstance(x,dict) and 'output' in x else str(REPO/x['repo']) if isinstance(x,dict) and 'repo' in x else x for x in m['args']]
   run_external(REPO/m['script'],args)
 legacy.write_json(out/'revision17_summary.json',dict(analysis_version='revision17-conservative-candidate-2026-09-22',common_judgments=1320,diagnostic_not_pooled=True,original_generation_reexecuted=False,independent_human_item_validation=False,criteria=info,scope='Fixed-label aggregation and documented arithmetic, not a full semantic revalidation'))
 print('Package manifest entries verified:',checked)
 print('Revision 17 fixed-input reproduction complete')
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=REPO/'reproduced');a=p.parse_args();run(a.out)
