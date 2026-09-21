"""External QA launcher; disallow networking and non-runtime reads outside extracted ZIP."""
import sys,os,runpy,json
from pathlib import Path
sys.dont_write_bytecode=True
repo=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
allowed=[repo,Path(sys.base_prefix).resolve(),Path(sys.prefix).resolve()]
events={'outside_reads':[],'outside_writes':[],'network_attempts':[],'read_calls':0,'write_calls':0}
def inside(path,root):return path==root or root in path.parents
def audit(event,args):
 if event.startswith('socket.'):
  events['network_attempts'].append(event);raise PermissionError('Network disallowed during offline QA')
 if event=='open':
  f,mode,flags=args
  if not isinstance(f,(str,bytes,os.PathLike)):return
  p=Path(os.fsdecode(f)).resolve()
  write=bool((flags or 0)&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if write:
   events['write_calls']+=1
   if not inside(p,out):
    events['outside_writes'].append(p.name);raise PermissionError('Write outside requested output forbidden')
  else:
   events['read_calls']+=1
   if not any(inside(p,a) for a in allowed):
    events['outside_reads'].append(p.name);raise PermissionError('External non-runtime input forbidden')
sys.addaudithook(audit)
sys.argv=[str(repo/'audit/rule_compliance/code/reproduce_revision17.py'),'--out',str(out)]
try:runpy.run_path(sys.argv[0],run_name='__main__')
finally:print('OFFLINE_GUARD '+json.dumps(events,sort_keys=True))
