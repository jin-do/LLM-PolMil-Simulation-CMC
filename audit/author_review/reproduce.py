"""Reproduce the separately reported 40-item contextual-review summaries.

Python standard library only. No network, LLM calls, or new classifications.
"""
from pathlib import Path
import argparse, collections, csv, hashlib, json

BASE=Path(__file__).resolve().parent

def write_json(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_csv(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=BASE/'results')
    args=parser.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((BASE/'source_records/manifest.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        payload=(BASE/row['path']).read_bytes()
        if len(payload)!=row['bytes'] or hashlib.sha256(payload).hexdigest()!=row['sha256']:
            raise ValueError('Changed historical source record: '+row['path'])
    record_path=BASE/'source_records/author_review_20260927.json'
    record=json.loads(record_path.read_text(encoding='utf-8-sig'))
    rows=record['reviews']
    assert len(rows)==40 and len({r['case_id'] for r in rows})==40
    clarification=json.loads((BASE/'evidence_recheck/changed_12_cases_20260929.json').read_text(encoding='utf-8'))
    assert clarification['source_record_sha256']==hashlib.sha256(record_path.read_bytes()).hexdigest()
    later={r['case_id']:r for r in clarification['cases']}
    mapping={'C':'A','V':'R','U':'I'}
    normalized=[]
    for r in rows:
        assert r['human_review_completed']=='true'
        assert r['applied_to_paper_core_ledger']=='false'
        status=r['author_reviewed_ai_status']
        assert status==r['proposed_ai_status'] and status in mapping
        updated=later.get(r['case_id'])
        normalized.append({
          'case_id':r['case_id'],'original_check_id':r['original_check_id'],'run_id':r['run_id'],
          'domain':r['domain'],'turn':r['turn'],'membership':r['membership'],
          'earlier_ai_status_20260920':r['previous_ai_status_20260920'],
          'historical_contextual_status':status,'contextual_judgment':mapping[status],
          'contextual_criterion':r['criteria_version'],
          'author_confirmation_date':r['human_review_confirmation_date'],
          'actual_review_date':r['human_review_date'],
          'judgment_origin':r['judgment_origin'],
          'source_pages':r['evidence_pages'],'source_url':r['source_url'],'source_sha256':r['source_sha256'],
          'historical_reason_ko':r['reason_ko'],'historical_limit_ko':r['uncertainty'],
          'later_explanation_date':'2026-09-29' if updated else '',
          'later_explanation_origin':'AI-only source recheck; labels unchanged' if updated else '',
          'later_explanation_en':updated['recommended_A8_rationale_en'] if updated else '',
          'independent_human_label_set':False,'replaces_common_ledger_label':False})
    transition=collections.Counter((r['earlier_ai_status_20260920'],r['contextual_judgment']) for r in normalized)
    counts=dict(collections.Counter(r['contextual_judgment'] for r in normalized))
    by_membership={key:dict(collections.Counter(r['contextual_judgment'] for r in normalized if r['membership']==key)) for key in sorted({r['membership'] for r in normalized})}
    changed=[r['case_id'] for r in normalized if mapping[r['earlier_ai_status_20260920']]!=r['contextual_judgment']]
    assert counts=={'A':27,'R':10,'I':3}
    assert set(changed)==set(record['summary']['changed_vs_20260920'])==set(later)
    assert len(changed)==12
    summary={
      'source_record_sha256':hashlib.sha256(record_path.read_bytes()).hexdigest(),
      'contextual_counts':counts,'counts_by_membership':by_membership,
      'transition_counts':[{ 'earlier_ai_status':old,'A':transition[old,'A'],'R':transition[old,'R'],'I':transition[old,'I'],'total':sum(transition[old,new] for new in 'ARI')} for old in 'CVU'],
      'changed_interpretation_ids':changed,'author_confirmation_date':'2026-09-27','actual_review_date':None,
      'clarification_date':'2026-09-29','clarification_origin':'AI-only source recheck; no new human labels',
      'independent_human_label_set_collected':False,'blinded':False,'common_1320_labels_changed':False,
      'meaning':'A/R/I describe contextual acceptability, revision need, or indeterminacy under a different criterion; they do not replace C/V/U in the common assessment. Counts are not accuracy or agreement estimates.'}
    write_csv(out/'contextual_review_40.csv',normalized)
    write_json(out/'contextual_review_40.json',{'provenance':summary,'records':normalized})
    write_json(out/'contextual_summary.json',summary)
    write_csv(out/'contextual_transitions.csv',summary['transition_counts'])
    print(json.dumps({'items':len(rows),'counts':counts,'changed_interpretations':len(changed),'output':str(out)},ensure_ascii=False))

if __name__=='__main__':main()
