"""JDMS bounded audit closeout. No model calls, no source edits, no semantic reclassification.
Default tables mode reproduces frozen-label summaries and explicitly specified calculations.
source_checks checks only PDFs explicitly provided via --source-root; missing PDFs stay blocked.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, sys, unicodedata
from collections import Counter, defaultdict
from decimal import Decimal as D
from pathlib import Path

C,V,U,NA = '준수','위반','판정 불가','적용 대상 아님'
VALID={C,V,U,NA}
CORE_GROUPS={
 'initial_role':['T1_US_ROLE','T1_SU_ROLE'],
 'local_branch':['T2_BRANCH','T3_BRANCH','T4_BRANCH'],
 'event_condition':['T2_EVENT','T3_EVENT','T4_EVENT'],
 'parent_coverage':['T2_PARENT_COVERAGE','T3_PARENT_COVERAGE','T4_PARENT_COVERAGE']}
KEYS=[k for ks in CORE_GROUPS.values() for k in ks]

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def load_csv(p:Path)->list[dict[str,str]]:
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def load_json(p:Path):return json.loads(p.read_text(encoding='utf-8-sig'))
def write_json(p:Path,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def write_csv(p:Path,rows:list[dict],fields=None):
 p.parent.mkdir(parents=True,exist_ok=True)
 if fields is None:fields=list(rows[0]) if rows else []
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='raise');w.writeheader();w.writerows(rows)
def norm(s:str)->str:
 return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).replace('’',"'").replace('‘',"'").replace('￾','')).strip()
def true(s)->bool:return str(s).strip().lower()=='true'
def included(r:dict)->bool:
 return not true(r.get('candidate_only','false')) and ('review_completed' not in r or true(r['review_completed']))
def clip(v:D)->D:return max(D(0),min(D(1),v))
def rates(c:int,v:int,u:int)->tuple[str,str]:
 # Empty is undefined, not zero percent. Values returned to four decimals for reproducibility.
 return (str((D(c+v)*100/D(c+v+u)).quantize(D('.0001'))) if c+v+u else '',
         str((D(c)*100/D(c+v)).quantize(D('.0001'))) if c+v else '')
def unique(rows,key='check_id'):
 values=[r[key] for r in rows]
 if any(not x for x in values) or len(values)!=len(set(values)):raise ValueError(f'Blank/duplicate {key}')
def source_rules(req):
 events={};trules={};by_path={}
 for r in req:
  path=r['json_path_or_page'];by_path[(r['source_file'].replace('\\','/'),path)]=r['original_requirement']
  m=re.fullmatch(r'\$\.event_driven_adjustments\.([^.]+)\.([^.]+)',path)
  if m:events.setdefault(m[1],{})[m[2]]=D(r['original_requirement'])
  if '.Diplomatic_Negotiation' in path:trules[path]=r['original_requirement']
 return events,trules,by_path

def threshold_class(state,negotiation,timing_unresolved,trules):
 gates={k:None for k in ['Tension','Diplomatic_Support','Public_Opinion']}
 if state is not None:
  t,ds,po=map(D,state)
  opts={'Tension':'>=0.8' if t>=D('.8') else '<0.8',
        'Diplomatic_Support':'<=0.5' if ds<=D('.5') else '>0.5',
        'Public_Opinion':'<=0.4' if po<=D('.4') else '>0.4'}
  gates={k:trules[f'$.decision_options.{k}["{cond}"].Diplomatic_Negotiation'] for k,cond in opts.items()}
 if negotiation in ['ambiguous','not_observable']:status=U
 elif negotiation=='no':status=C # Only absence of prohibited negotiation, not proof of enforcement.
 elif state is None or timing_unresolved:status=U
 elif all(x=='Disabled' for x in gates.values()):status=V
 elif any(x=='Disabled' for x in gates.values()):status=U # No retrospectively invented precedence.
 else:status=C
 return status,gates

def eligible_recipe(r,recipe):
 return all(r.get(k,'') in vals for k,vals in recipe.get('in',{}).items()) and all(r.get(k,'')==v for k,v in recipe.get('eq',{}).items())

def tables(root:Path,out:Path):
 spec=load_json(root/'protocol/analysis_spec.json');cache={};read_hashes={}
 def rows(rel):
  if rel not in cache:
   p=root/rel;cache[rel]=load_csv(p);read_hashes[rel]=sha(p)
   if cache[rel] and 'check_id' in cache[rel][0]:unique(cache[rel])
  return cache[rel]
 def js(rel):
  p=root/rel;read_hashes[rel]=sha(p);return load_json(p)
 domain=[]
 for recipe in spec['domain_recipes']:
  rs=[r for r in rows(recipe['file']) if eligible_recipe(r,recipe)]
  kept=[r for r in rs if included(r)]
  statuses=Counter(r['status'] for r in kept)
  if set(statuses)-VALID:raise ValueError('Unexpected status')
  verification,compliance=rates(statuses[C],statuses[V],statuses[U])
  domain.append(dict(domain_id=recipe['id'],label=recipe['label'],unit=recipe['unit'],source_ledger=recipe['file'],
    inventory_rows=len(rs),reviewed_rows=len(kept),unreviewed_or_candidate_rows=len(rs)-len(kept),
    runs_in_inventory=len({r['run_id'] for r in rs}),runs_reviewed=len({r['run_id'] for r in kept}),
    C=statuses[C],V=statuses[V],U=statuses[U],NA=statuses[NA],
    assessable_percent=verification,conditional_compliance_percent=compliance,
    selection_basis=recipe['selection_basis'],recommended_use=recipe['recommended_use']))
 write_csv(out/'domain_results.csv',domain)
 core=rows('data/core/07_semantic_validation_ledger.csv');unique(core)
 common=[r for r in core if r['metric_key'] in KEYS]
 idx={(r['run_id'],r['metric_key']):r for r in common}
 if len(idx)!=len(common):raise ValueError('Duplicate common run/metric')
 runids=sorted({r['run_id'] for r in common})
 source_runids={r['run_id'] for r in rows('source_assets.csv')}
 if set(runids)!=source_runids:raise ValueError('Common grid differs from preserved source run roster')
 if len(runids)!=120 or len(common)!=1320 or any((run,k) not in idx for run in runids for k in KEYS):
  raise ValueError('Incomplete/expanded prespecified common grid')
 if any(not included(r) for r in common):raise ValueError('Unreviewed rows in historical core grid')
 outcomes=[]
 for run in runids:
  vals=[idx[(run,k)]['status'] for k in KEYS]
  outcomes.append(dict(run_id=run,local_eight_all_C=all(x==C for x in vals[:8]),eleven_all_C=all(x==C for x in vals),
    interpretation='Defined subcontrols only; no complete-path certification; no outcome recoding used.'))
 write_csv(out/'run_subcontrol_status.csv',outcomes)
 req=rows('protocol/control_requirements.csv');events,trules,by_path=source_rules(req)
 checks={};detail=[]
 # Fixed parent mapping and transcribed values. Recalculation is independent of stored difference.
 ir=rows('data/supplemental_partial/inheritance_ledger.csv');unique(ir)
 compared=0
 for r in ir:
  if not included(r) or r['status'] not in [C,V]:continue
  previous,reported=D(r['previous_value']),D(r['reported_value']);delta=reported-previous
  status=C if delta==0 else V
  okay=(D(r['recomputed_value'])==previous and D(r['difference'])==delta and r['status']==status)
  detail.append(dict(check_family='inheritance',check_id=r['check_id'],calculated=str(previous),stored=r['recomputed_value'],match=okay,scope='fixed parent identification and value transcription'))
  compared+=1
 checks['inheritance_comparisons']=compared
 wr=rows('data/supplemental_partial/actor_weight_value_checks.csv');dist=Counter()
 for r in wr:
  val=by_path.get((r['source_json'].replace('\\','/'),r['json_path']))
  if val is None:path,num=V,NA;label='missing_attributed_path'
  else:path=C;num=C if D(val)==D(r['reported_value']) else V;label='numeric_match' if num==C else 'numeric_mismatch'
  dist[label]+=1
  detail.append(dict(check_family='weight_quote',check_id=r['check_id'],calculated=label,stored=r['path_status']+'/'+r['numeric_equality_status'],match=path==r['path_status'] and num==r['numeric_equality_status'],scope='quoted original rule index, not AHP execution'))
 checks['weight_quote_distribution']=dict(dist)
 # Re-evaluate explicit arithmetic specs from frozen source judgments.
 annotation=js('annotations/effect_semantics.json');expected={}
 for run,review in annotation['runs'].items():
  for s in review.get('deterministic_calculations',[]):
   if s['operation']=='sum_events':v=sum((events[e][s['variable']] for e in s['events']),D(0))+D(s.get('extra_delta','0'))
   elif s['operation']=='clamp':v=clip(D(s['value']))
   elif s['operation']=='reported_gap_formula':v=D(s['old'])+(D(1)-D(s['old']))*D(s['factor'])
   else:raise ValueError('Unknown operation')
   expected[run+'-'+s['id']]=(v,C if v==D(s['reported']) else V)
 # Three explicitly documented source-level supplemental specs, not free-form parsing.
 for s in js('annotations/extra_calculation_specs.json'):
  v=sum((events[e][s['variable']]*D(mult) for e,mult in s['terms']),D(s['constant']))
  status=U if s['semantic_status']=='unassessable' else C if v==D(s['reported']) else V
  expected[s['check_id']]=(v,status)
 for r in rows('data/supplemental_partial/effect_independent_calculations.csv'):
  v,status=expected[r['check_id']]
  detail.append(dict(check_family='effect_arithmetic',check_id=r['check_id'],calculated=str(v),stored=r['recalculated'],match=D(r['recalculated'])==v and status==r['status'],scope='explicit fixed event set; includes internal-only formulas, no pooled rate'))
 # Predicates from original quotations, semantics/timing fixed and separately pending human review.
 td={r['check_id']:r for r in rows('data/supplemental_partial/threshold_action_ledger.csv')}
 ta=js('annotations/threshold_action_anchors.json');precount=0;quotes=0
 for a in ta:
  b,act=a['fixed_annotation'],a['action_annotation'];r=td[a['check_id']]
  status,gates=threshold_class(b['state'],act['negotiation'],b.get('choice_state_timing_unresolved',False),trules)
  okay=status==r['status'] and gates==json.loads(r['python_gate_result'])
  if b.get('explicit_base_state'):
   pre=[clip(D(x)+D(dx)) for x,dx in zip(b['explicit_base_state'],b['explicit_predecision_delta'])]
   okay=okay and pre==list(map(D,b['state']));precount+=1
  pool=' '.join(norm(p['text']) for p in a['source_pages'])
  quote_ok=all(norm(q) in pool for q in [b['state_anchor'],act['action_anchor']]);quotes+=2
  detail.append(dict(check_family='threshold',check_id=r['check_id'],calculated=status,stored=r['status'],match=okay and quote_ok,scope='fixed action/state/timing; quote presence within frozen evidence'))
 checks['threshold_comparisons']=len(ta);checks['explicit_predecision_calculations']=precount;checks['threshold_quote_checks']=quotes
 na=js('annotations/narrative_anchors.json')
 for a in na:
  for kind in ['narrative','log']:
   hit=norm(a[kind]['anchor']) in norm(a[kind]['source_page_text'])
   detail.append(dict(check_family='narrative_anchor',check_id=a['check_id']+':'+kind,calculated='present' if hit else 'missing',stored='source excerpt',match=hit,scope='frozen source-page text; not new semantic validation'))
 checks['narrative_quote_checks']=len(na)*2
 # CLA-01: four state values conditional on applying both FULL named VDM rows.
 local=js('annotations/local_case_inputs.json');local_rows=[]
 for case in local['calculations']:
  v=clip(D(case['prior'])+sum((events[e][case['variable']] for e in case['events']),D(0)))
  local_rows.append(dict(case_id=case['case_id'],run_id=case['run_id'],variable=case['variable'],prior=case['prior'],
   events=' + '.join(case['events']),computed=str(v),reported=case['reported'],numeric_correspondence=C if v==D(case['reported']) else V,
   scope=case['scope']))
 write_csv(out/'local_case_calculations.csv',local_rows)
 write_csv(out/'deterministic_check_details.csv',detail)
 checks['mismatch_count']=sum(not x['match'] for x in detail)
 checks['technical_checks']='passed' if checks['mismatch_count']==0 else 'failed'
 checks['human_review']='pending'
 checks['publication_preparation']='draft_pending_human_review'
 checks['original_pipeline_replayed']=False
 checks['core_rows']=len(common);checks['core_selected_rows']=len(core)-len(common)
 checks['local_eight_all_C_runs']=sum(r['local_eight_all_C'] for r in outcomes)
 checks['eleven_all_C_runs']=sum(r['eleven_all_C'] for r in outcomes)
 checks['scope']='Frozen-label aggregation and explicit numeric/quote checks only. No AI or human semantics regenerated. No global arithmetic accuracy claim.'
 checks['input_sha256']=read_hashes
 write_json(out/'technical_results.json',checks)
 if checks['mismatch_count']:raise ValueError('Deterministic mismatch; inspect details; do not overwrite expected data.')

# Location/evidence matching deliberately excludes numeric equality and parser row sequence.
def match_key(r):
 return tuple(norm(r.get(k,'')) for k in ['run_id','source_file','page','turn','branch','actor','variable','evidence'])
def reconcile(old,new):
 groups=defaultdict(lambda:[[],[]])
 for r in old:groups[match_key(r)][0].append(r)
 for r in new:groups[match_key(r)][1].append(r)
 result=[]
 for key,(aa,bb) in sorted(groups.items()):
  if len(aa)==1 and len(bb)==1:card='1:1'
  elif len(aa)==1 and len(bb)>1:card='1:N'
  elif len(aa)>1 and len(bb)==1:card='N:1'
  elif aa and bb:card='N:M'
  elif aa:card='old_only'
  else:card='candidate_only'
  same=None
  if card=='1:1':same=all(aa[0].get(k,'')==bb[0].get(k,'') for k in ['status','reported_value','recomputed_value'])
  result.append(dict(run_id=key[0],source_file=key[1],page=key[2],turn=key[3],branch=key[4],actor=key[5],variable=key[6],
    normalized_source_evidence=key[7],old_ids=' | '.join(r['check_id'] for r in aa),candidate_ids=' | '.join(r['check_id'] for r in bb),
    old_status=' | '.join(r['status'] for r in aa),candidate_status=' | '.join(r['status'] for r in bb),
    old_values=' | '.join(r['reported_value']+' => '+r['recomputed_value'] for r in aa),candidate_values=' | '.join(r['reported_value']+' => '+r['recomputed_value'] for r in bb),
    match_cardinality=card,exact_numeric_and_status_agreement='' if same is None else same,
    candidate_admitted_to_final_rates=False,resolution='same_observation_same_result_not_promoted' if same else 'unresolved_different_or_unmatched_no_forced_link',
    affected_claim='GLOBAL_ARITHMETIC_RATE_WITHHELD',candidate_human_review='pending'))
 return result

def conflicts(root:Path,out:Path):
 old=load_csv(root/'data/diagnostic_only/v1_arithmetic_subset.csv');new=load_csv(root/'data/diagnostic_only/v3_arithmetic_candidates_subset.csv')
 result=reconcile(old,new);write_csv(out/'differences.csv',result)
 stat=Counter(r['match_cardinality'] for r in result)
 write_json(out/'reconciliation_summary.json',{'old_rows':len(old),'candidate_rows':len(new),'exact_source_key_groups':dict(stat),
  'one_to_one_identical':sum(r['match_cardinality']=='1:1' and r['exact_numeric_and_status_agreement'] is True for r in result),
  'one_to_one_changed':sum(r['match_cardinality']=='1:1' and r['exact_numeric_and_status_agreement'] is False for r in result),
  'matching_note':'Same normalized source text and location, never parser index or numeric coincidence. Unmatched may reflect changed extraction/coverage; no error verdict inferred.',
  'global_arithmetic_compliance_rate':'WITHHELD','semantic_judgments_changed':0})

def verify_manifest(root:Path):
 rows=load_csv(root/'manifest.csv');issues=[]
 outer=root/'MANIFEST.sha256'
 if not outer.is_file():issues.append({'file':'MANIFEST.sha256','issue':'missing'})
 else:
  expected=outer.read_text(encoding='utf-8-sig').split()[0]
  if sha(root/'manifest.csv')!=expected:issues.append({'file':'manifest.csv','issue':'outer_sha256_mismatch'})
 listed={r['relative_path'] for r in rows}
 for r in rows:
  p=root/r['relative_path']
  if not p.is_file():issues.append({'file':r['relative_path'],'issue':'missing'})
  elif p.stat().st_size!=int(r['bytes']) or sha(p)!=r['sha256']:issues.append({'file':r['relative_path'],'issue':'changed'})
 return {'checked':len(rows),'issues':issues,'scope':'Manifest does not hash itself; separate MANIFEST.sha256 covers it.'}

def source_checks(root:Path,out:Path,source_root:Path|None):
 assets=load_csv(root/'source_assets.csv');results=[];quote_results=[]
 try:import fitz
 except ImportError:fitz=None
 anchors=load_json(root/'evidence/representative_source_checks.json')
 for a in assets:
  p=(source_root/(a['run_id']+'.pdf')) if source_root else None
  if p is None or not p.is_file():status='blocked_source_not_supplied';actual=''
  else:actual=sha(p);status='hash_matched' if actual==a['sha256'] else 'failed_hash'
  results.append({'run_id':a['run_id'],'expected_sha256':a['sha256'],'actual_sha256':actual,'status':status})
  if status!='hash_matched':continue
  for check in anchors:
   if check['run_id']!=a['run_id']:continue
   if fitz is None:
    quote_results.append({'check_id':check['id'],'status':'blocked_PyMuPDF_not_installed'});continue
   with fitz.open(p) as doc:
    page=check['page'];present=0<page<=len(doc) and norm(check['quote']) in norm(doc[page-1].get_text())
    quote_results.append({'check_id':check['id'],'status':'matched' if present else 'failed_quote','page':page})
 write_csv(out/'source_hash_checks.csv',results)
 write_json(out/'source_check_results.json',{'status':'partial_scope','raw_hash_matched':sum(r['status']=='hash_matched' for r in results),
  'source_not_supplied':sum(r['status']=='blocked_source_not_supplied' for r in results),'source_failures':sum(r['status']=='failed_hash' for r in results),
  'representative_quotes':quote_results,'visual_review':'not performed by this command; separate AI page-inspection record only',
  'historical_input_binding':'not certified','human_review':'pending'})
 if any(r['status']=='failed_hash' for r in results) or any(r['status']=='failed_quote' for r in quote_results):raise ValueError('Source mismatch')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--mode',choices=['tables','source_checks','manifest'],default='tables');ap.add_argument('--source-root',type=Path)
 a=ap.parse_args();root=a.root.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
 # Output may not touch source directories or frozen data.
 if any(out==root/p or root/p in out.parents for p in ['data','protocol','annotations','evidence','code','tests']):raise ValueError('Unsafe output directory')
 if a.mode=='tables':tables(root,out);conflicts(root,out)
 elif a.mode=='source_checks':source_checks(root,out,a.source_root)
 else:
  result=verify_manifest(root);write_json(out/'manifest_check.json',result)
  if result['issues']:raise ValueError('Manifest mismatch')
 print(json.dumps({'mode':a.mode,'status':'executed','output':str(out)},ensure_ascii=False))
if __name__=='__main__':main()
