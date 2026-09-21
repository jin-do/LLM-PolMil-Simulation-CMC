"""Replay the 40 fixed AI labels and explanatory U-reason assignments.

New packaging-stage reaggregation, 2026-09-21/22 KST. Python standard library only.
Reads local inputs; writes only named result CSV/JSON files; no API/network calls.
Optional current-core crosscheck never applies a diagnostic label as a patch.
"""
from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal
import argparse, csv, json, re

LABELS={'C':'C','V':'V','U':'U','NA':'NA','준수':'C','위반':'V','판정 불가':'U','비적용':'NA'}
REASONS=['missing_turn_response','unclear_active_parent_set','termination_applicability','certainty_language','compound_event_linkage']
DOMAINS=['Initial actor-setting compatibility','Local alternative-pair generation','Specified event decision conditions','Previous parent-path coverage','Conditional arithmetic example','Narrative-log correspondence example']

def read_csv(p):
    with Path(p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def write_csv(p,rows,fields=None):
    with Path(p).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def validate(rows,membership,reasons):
    expected={f'HR-{i:03d}' for i in range(1,39)}|{'TRACE-CLA01','TRACE-GEM28'}
    ids=[r['case_id'] for r in rows]
    if len(ids)!=40 or set(ids)!=expected: raise ValueError('Missing or duplicate diagnostic case IDs')
    members={m['case_id']:m for m in membership}
    if len(membership)!=40 or set(members)!=expected: raise ValueError('Diagnostic membership does not match 40 cases')
    for r in rows:
        if r['ai_status'] not in {'C','V','U'}: raise ValueError('Invalid diagnostic label')
        if not re.fullmatch(r'(CLA|GPT|GEM|PER)-(0[1-9]|[12][0-9]|30)',r['run_id']): raise ValueError('Invalid run ID')
        if r['reviewer_type']!='AI' or any(r[k] for k in ['human_reviewer','human_review_date','human_status','human_reason']):
            raise ValueError('This fixed AI ledger must not be represented as completed human judgments')
        m=members[r['case_id']]
        expected_scope='common_selected' if r['case_id'].startswith('HR-') else 'representative_discrepancy'
        if m['scope']!=expected_scope or m['original_check_id']!=r['original_check_id']: raise ValueError('Scope/ID linkage mismatch')
        if m['in_common_denominator']!='false' or m['independent_sample']!='false': raise ValueError('Diagnostic rows cannot be appended to common denominator or treated as independent samples')
        if not re.fullmatch('[0-9a-f]{64}',r['source_sha256']): raise ValueError('Missing source hash')
    uids={r['case_id'] for r in rows if r['ai_status']=='U'}
    if len(reasons)!=len(uids) or {r['case_id'] for r in reasons}!=uids: raise ValueError('Each U item requires exactly one principal reason')
    for r in reasons:
        if r['reason_code'] not in REASONS: raise ValueError('Unknown U reason')
        if (r['reason_code']=='missing_turn_response')!=bool(r['dependency_group']): raise ValueError('Missing-response dependency linkage required')
    return members

def reproduce(root,output_dir=None,core_ledger=None,patch_ledger=None):
    root=Path(root); data=root/'data/diagnostic'; out=Path(output_dir) if output_dir else root/'results'
    rows=read_csv(data/'ai_review_40.csv'); reasons=read_csv(data/'u_reason_assignments.csv')
    members=validate(rows,read_csv(data/'membership.csv'),reasons); out.mkdir(parents=True,exist_ok=True)
    scopes=['common_selected','representative_discrepancy','all_diagnostic']
    totals=[]
    for scope in scopes:
        selected=[r for r in rows if scope=='all_diagnostic' or members[r['case_id']]['scope']==scope]
        c=Counter(r['ai_status'] for r in selected)
        totals.append(dict(scope=scope,items=len(selected),C=c['C'],V=c['V'],U=c['U'],NA=c['NA']))
    write_csv(out/'diagnostic_counts.csv',totals)
    domain_rows=[]
    for domain in dict.fromkeys(r['domain'] for r in rows):
        rr=[r for r in rows if r['domain']==domain]; c=Counter(r['ai_status'] for r in rr)
        domain_rows.append(dict(domain=domain,items=len(rr),C=c['C'],V=c['V'],U=c['U'],NA=c['NA']))
    write_csv(out/'diagnostic_by_domain.csv',domain_rows)
    rs=[]
    for code in REASONS:
        rr=[r for r in reasons if r['reason_code']==code]
        rs.append(dict(reason_code=code,reason_label=rr[0]['reason_label'],items=len(rr),case_ids=';'.join(sorted(r['case_id'] for r in rr))))
    write_csv(out/'diagnostic_u_reason_counts.csv',rs)
    dep=defaultdict(list)
    for r in reasons:
        if r['dependency_group']: dep[r['dependency_group']].append(r['case_id'])
    write_csv(out/'diagnostic_missing_response_dependencies.csv',[dict(dependency_group=k,items=len(v),case_ids=';'.join(sorted(v)),interpretation='Shared missing response; not independent failures') for k,v in sorted(dep.items())])
    arithmetic=[]
    for r in read_csv(data/'conditional_arithmetic_inputs.csv'):
        computed=min(Decimal(1),max(Decimal(0),sum(Decimal(r[k]) for k in ['prior','strong_leadership','diplomatic_success'])))
        arithmetic.append(dict(variable=r['variable'],calculated=format(computed,'.2f'),reported=format(Decimal(r['reported']),'.2f'),difference=format(computed-Decimal(r['reported']),'.2f'),match=str(computed==Decimal(r['reported'])).lower()))
    write_csv(out/'diagnostic_conditional_arithmetic.csv',arithmetic)
    linked=[]
    if core_ledger is not None or patch_ledger is not None:
        if core_ledger is None or patch_ledger is None: raise ValueError('Provide both current core and amendment ledger')
        core=read_csv(core_ledger); cids=[r['check_id'] for r in core]
        if len(cids)!=1320 or len(set(cids))!=1320: raise ValueError('Core must contain precisely 1320 unique common checks')
        coremap={r['check_id']:r for r in core}; changes=json.loads(Path(patch_ledger).read_text(encoding='utf-8-sig'))
        for r in rows:
            if members[r['case_id']]['scope']!='common_selected':continue
            key=r['original_check_id']; current=coremap.get(key)
            if current is None: raise ValueError('Missing diagnostic/core link: '+key)
            current_label=LABELS[current['status']]
            if current_label!=r['ai_status']: raise ValueError('Current-core diagnostic disagreement: '+key)
            linked.append(dict(case_id=r['case_id'],check_id=key,ai_label=r['ai_status'],current_core_label=current_label,match='true',applied_as_new_change='false'))
        for r in read_csv(data/'existing_change_links.csv'):
            p=[p for p in changes if p['check_id']==r['check_id']]
            if len(p)!=1 or p[0]['review_id']!=r['review_id'] or LABELS[p[0]['proposed_status']]!=r['ai_review_status']: raise ValueError('Existing amendment link mismatch')
        write_csv(out/'diagnostic_core_linkage.csv',linked)
    result=dict(analysis_version='revision17-diagnostic-fixed-20260920',reviewer_type='AI',human_judgments_completed=0,counts=totals,
                common_denominator_additions=0,representative_denominator_additions=0,core_linkage_checked=len(linked),new_core_changes_applied=0,
                unique_reviewed_runs=len({r['run_id'] for r in rows}),principal_u_reasons=rs,missing_response_groups=len(dep),
                scope='Fixed-label aggregation and conditional arithmetic; no new semantic or independent human validation')
    (out/'diagnostic_reproduction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out','--output',dest='output',type=Path);ap.add_argument('--core-ledger',type=Path);ap.add_argument('--patch-ledger',type=Path);a=ap.parse_args()
    core=a.core_ledger;patches=a.patch_ledger
    if core is None and patches is None:
        for candidate in [a.root/'results/criteria/conservative_common_1320.csv',a.root/'results/conservative_common_1320.csv']:
            if candidate.exists():
                core=candidate;patches=a.root/'data/adjudication/patches.json';break
    result=reproduce(a.root,a.output,core,patches)
    print(json.dumps(dict(status='REPRODUCED',counts=result['counts'],core_linkage_checked=result['core_linkage_checked']),ensure_ascii=False))

if __name__=='__main__': main()
