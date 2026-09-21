"""Apply explicit source-linked AI adjudications; never generate semantic labels by regex.
Standard-library only. Historical inputs are read-only; outputs are new files.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re
from collections import Counter
from decimal import Decimal
from pathlib import Path
GROUPS={'initial_role':['T1_US_ROLE','T1_SU_ROLE'], 'local_branch':['T2_BRANCH','T3_BRANCH','T4_BRANCH'], 'event_condition':['T2_EVENT','T3_EVENT','T4_EVENT'], 'parent_coverage':['T2_PARENT_COVERAGE','T3_PARENT_COVERAGE','T4_PARENT_COVERAGE']}
KEYS={k for v in GROUPS.values() for k in v};VALID={'준수','위반','판정 불가','적용 대상 아님'}
EXPECTED={f'{s}-{i:02d}' for s in ('CLA','GEM','GPT','PER') for i in range(1,31)}

def read_csv(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(p,rows):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def validate(raw,assets):
 ids=[r['check_id'] for r in raw]
 if len(ids)!=len(set(ids)):raise ValueError('duplicate observation ID')
 roster=[r['run_id'] for r in assets]
 if len(roster)!=120 or set(roster)!=EXPECTED:raise ValueError('source roster mismatch')
 common=[r for r in raw if r['metric_key'] in KEYS]
 if len(common)!=1320 or len(raw)-len(common)!=67:raise ValueError('unexpected common/selected frame')
 grid=[(r['run_id'],r['metric_key']) for r in common]
 if len(grid)!=len(set(grid)) or set(grid)!={(r,k) for r in EXPECTED for k in KEYS}:raise ValueError('invalid common grid')
 if any(r['status'] not in VALID for r in common):raise ValueError('invalid label')
 if any(r.get('review_completed','').lower()!='true' for r in common):raise ValueError('unreviewed item cannot enter assessed frame')
 return common

def apply(common,patches,decisions,include_boundary=False):
 out=[dict(r) for r in common]; index={r['check_id']:r for r in out}; seen=set();dec={r['review_id']:r for r in decisions}
 if len(dec)!=len(decisions):raise ValueError('duplicate review ID')
 for p in patches:
  if p['check_id'] in seen:raise ValueError('duplicate patch')
  seen.add(p['check_id'])
  if p['check_id'] not in index or p['review_id'] not in dec:raise ValueError('unknown patch target/review')
  r=index[p['check_id']]; d=dec[p['review_id']]
  if r['status']!=p['legacy_status']:raise ValueError('legacy label mismatch')
  if any(r[k]!=p[k] for k in ['run_id','metric_key']):raise ValueError('patch identity mismatch')
  if any(d[k]!=p[k] for k in ['check_id','run_id','metric_key','legacy_status','proposed_status','tier']):raise ValueError('patch is not supported by decision entry')
  if p['tier'] not in ('clear','boundary') or p['proposed_status'] not in VALID:raise ValueError('invalid adjudication')
  if p['tier']=='boundary' and not include_boundary:continue
  r['legacy_status_before_amendment']=r['status'];r['legacy_reason_before_amendment']=r['reason']
  r['status']=p['proposed_status'];r['reason']=d['reason'];r['criteria_review_id']=p['review_id']
  r['criteria_basis']='criteria-context-v1, AI source comparison; not human ground truth'
  r['adjudication_source']='criteria-context-v1';r['human_review_required']='True'
  if r.get('parent_coverage_status'):r['parent_coverage_status']=p['proposed_status']
  if p['proposed_status']=='판정 불가':r['uncertainty']=d['reason']
 for r in out:
  for k in ['legacy_status_before_amendment','legacy_reason_before_amendment','criteria_review_id','criteria_basis']:r.setdefault(k,'')
 return out

def percent(n,d):return '' if d==0 else str((Decimal(n)*100/Decimal(d)).quantize(Decimal('0.000001')))
def aggregate(rows,scenario):
 result=[]
 for group,keys in GROUPS.items():
  rr=[r for r in rows if r['metric_key'] in keys];c=Counter(r['status'] for r in rr);C,V,U,NA=[c[k] for k in ['준수','위반','판정 불가','적용 대상 아님']]
  result.append(dict(scenario=scenario,domain=group,C=C,V=V,U=U,NA=NA,assessability_denominator=C+V+U,compliance_denominator=C+V,assessable_percent=percent(C+V,C+V+U),conditional_compliance_percent=percent(C,C+V)))
 return result

def validate_evidence(root,decisions):
 # Location matching is not validation of the interpretation.
 issues=[];items=json.loads((root/'evidence/criteria_recheck/initial_excerpts.json').read_text())
 for r in items:
  source=json.loads((root/'evidence/criteria_recheck/initial_windows'/f"{r['run_id']}.json").read_text())
  text=next((p['text'] for p in source['pages'] if str(p['page'])==r['source_page']),'')
  norm=lambda s:re.sub(r'\s+',' ',s).strip()
  if norm(r['excerpt']) not in norm(text):issues.append(r['review_id'])
 if issues:raise ValueError('source excerpt mismatch: '+','.join(issues))
 return len(items)

def run(root,out):
 root=Path(root).resolve();out=Path(out).resolve()
 if out==root or any(out==root/x or root/x in out.parents for x in ['data','code','evidence','protocol','annotations','tests','legacy']):raise ValueError('unsafe output directory')
 raw=read_csv(root/'data/core/07_semantic_validation_ledger.csv');common=validate(raw,read_csv(root/'source_assets.csv'))
 patches=json.loads((root/'data/adjudication/patches.json').read_text());decisions=read_csv(root/'data/adjudication/decisions.csv')
 n=validate_evidence(root,decisions);conservative=apply(common,patches,decisions,True);clear=apply(common,patches,decisions,False)
 out.mkdir(parents=True,exist_ok=True);write_csv(out/'criteria_comparison.csv',aggregate(common,'legacy_frozen')+aggregate(clear,'clear_corrections')+aggregate(conservative,'conservative_boundaries'))
 write_csv(out/'clear_common_1320.csv',clear);write_csv(out/'conservative_common_1320.csv',conservative)
 # Standalone recomputation deliberately uses integer counts; no legacy replay helper.
 info=dict(input_sha256=hashlib.sha256((root/'data/core/07_semantic_validation_ledger.csv').read_bytes()).hexdigest(),common_rows=len(common),excluded_selected_rows=len(raw)-len(common),clear_changes=sum(a['status']!=b['status'] for a,b in zip(common,clear)),conservative_changes=sum(a['status']!=b['status'] for a,b in zip(common,conservative)),excerpt_locations_matched=n,semantics='fixed AI decisions applied, not automatic independent validation',full_1320_semantic_recheck=False)
 (out/'criteria_reproduction.json').write_text(json.dumps(info,indent=2)+'\n');return info
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.root,a.out),ensure_ascii=False))
