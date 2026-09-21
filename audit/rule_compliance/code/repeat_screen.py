"""Repeat bounded text retrieval only. A hit or non-hit is NEVER a C/V/U decision."""
import argparse,csv,json,re
from pathlib import Path
PATTERN=r'guarantee|ensur|certain|surest|destroy|eliminat|neutrali|surviv|miss.*missile|all missiles|complete success'
def screen(root):
 out=[]
 for p in sorted((root/'evidence/criteria_recheck/initial_windows').glob('*.json')):
  source=json.loads(p.read_text());spans=[]
  for pg in source['pages']:
   text='\n'.join(s for s in pg['text'].replace('\r','').splitlines() if not any(x in s for x in ['--tw-','--font-','hsl(','hsla(']));merged=[]
   for m in re.finditer(PATTERN,text,re.I):
    a,z=max(0,m.start()-160),min(len(text),m.end()+240)
    if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(z,merged[-1][1]))
    else:merged.append((a,z))
   spans.extend({'page':pg['page'],'quote':text[a:z].replace('\n',' ')} for a,z in merged)
  out.append({'run_id':source['run_id'],'source_pages':'1-'+str(source['pages'][-1]['page']),'snippets':spans,'semantic_verdict':None})
 if len(out)!=120:raise ValueError('Expected exactly 120 retained windows')
 return out
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a.add_argument('--out',type=Path,required=True);n=a.parse_args();d=screen(n.root);n.out.parent.mkdir(parents=True,exist_ok=True);n.out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Screened 120 bounded windows; no semantic decisions made.')
