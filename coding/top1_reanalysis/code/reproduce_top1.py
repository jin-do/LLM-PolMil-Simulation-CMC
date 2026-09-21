"""Replay preserved Top-1 coding. New packaging-stage aggregation, 2026-09-21/22 KST.

Python standard library only. Local input reads and results writes; no external APIs.
Does not reclassify PDFs, reconstruct simulation states, or verify original judgments.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import argparse, csv, json, re

SYSTEMS=['GPT-4o','Gemini 2.5 Flash','Claude Opus 4','Perplexity Pro']
PREFIXES=['GPT-4o','Gemini_2.5_Flash','Claude_Opus_4','Perplexity_RAG']
CATEGORIES=['Protracted stalemate','Internal collapse','Diplomatic resolution','Full-scale war','Limited conflict','Withheld']

def read_csv(p):
    with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def write_csv(p,rows):
    with Path(p).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def validate(rows):
    expected={f'{pre}-{i:02d}':system for pre,system in zip(PREFIXES,SYSTEMS) for i in range(1,31)}
    if len(rows)!=120 or {r['execution_id'] for r in rows}!=set(expected):raise ValueError('Missing, duplicate, or invalid Top-1 execution ID')
    for r in rows:
        if r['system']!=expected[r['execution_id']]:raise ValueError('Execution/system mismatch')
        if r['status'] not in {'confirmed','withheld'}:raise ValueError('Unknown coding status')
        if r['status']=='withheld' and (r['outcome_5'] or not r['reasoning']):raise ValueError('Withheld requires empty outcome and preserved reason')
        if r['status']=='confirmed' and r['outcome_5'] not in CATEGORIES[:-1]:raise ValueError('Invalid classified outcome')
        if r['recoding_changed'].lower() not in {'true','false'}:raise ValueError('Invalid change flag')
        if (r['recoding_changed'].lower()=='true')!=(r['status']=='confirmed' and r['outcome_5']!=r['original_outcome']):raise ValueError('Change flag inconsistent with original/new labels')
        if not re.fullmatch('[0-9a-f]{64}',r['source_pdf_sha256']):raise ValueError('Missing source PDF hash')
        if not r['raw_log_path'].startswith('runs/raw_logs/') or '..' in Path(r['raw_log_path']).parts:raise ValueError('Unsafe source reference')
        for k in ['selection_evidence','terminal_evidence']:
            evidence=json.loads(r[k])
            if not evidence or any(not isinstance(e['page'],int) or e['page']<1 or not e['excerpt'] for e in evidence):raise ValueError('Invalid source evidence locator')

def reproduce(root,output_dir=None):
    root=Path(root);rows=read_csv(root/'data/top1_source_recoding.csv');validate(rows)
    refs=read_csv(root/'data/source_references.csv');byid={r['execution_id']:r for r in refs}
    if len(refs)!=120 or set(byid)!={r['execution_id'] for r in rows}:raise ValueError('Source reference IDs mismatch')
    for r in rows:
        if byid[r['execution_id']]['source_pdf_sha256']!=r['source_pdf_sha256'] or byid[r['execution_id']]['raw_log_path']!=r['raw_log_path']:raise ValueError('Source reference mismatch')
    out=Path(output_dir) if output_dir else root/'results';out.mkdir(parents=True,exist_ok=True)
    counts=[];long=[]
    for system in SYSTEMS+['Total']:
        rr=[r for r in rows if system=='Total' or r['system']==system]
        n=len(rr); cc=Counter(r['outcome_5'] if r['status']=='confirmed' else 'Withheld' for r in rr)
        counts.append({'System':system,'Denominator':n,**{cat:cc[cat] for cat in CATEGORIES}})
        for category in CATEGORIES:
            percent=(Decimal(cc[category])*100/Decimal(n)).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP) if n else ''
            long.append(dict(system=system,category=category,count=cc[category],denominator=n,percent_1dp=str(percent)))
    write_csv(out/'table_b1_counts.csv',counts);write_csv(out/'table_b1_percentages.csv',long)
    write_csv(out/'withheld_cases.csv',[{k:r[k] for k in ['execution_id','system','status','reasoning','selection_evidence','terminal_evidence','limitations']} for r in rows if r['status']=='withheld'])
    result=dict(analysis_version='revision17-top1-fixed-recoding',executions=len(rows),classified=sum(r['status']=='confirmed' for r in rows),withheld=sum(r['status']=='withheld' for r in rows),changed_classifications=sum(r['recoding_changed'].lower()=='true' for r in rows),counts=counts,denominator_policy='30 per system, 120 overall; withheld retained',rounding='Decimal ROUND_HALF_UP to 1 decimal',scope='Fixed coding replay only; no new PDF semantic recoding or human validation')
    (out/'top1_reproduction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='REPRODUCED',executions=len(rows),counts=counts[-1]),ensure_ascii=False))
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out','--output',dest='output',type=Path);a=ap.parse_args();reproduce(a.root,a.output)

if __name__=='__main__':main()
