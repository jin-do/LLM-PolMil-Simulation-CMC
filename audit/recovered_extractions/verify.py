"""Verify restored archival bytes and all historical-reference mappings."""
from pathlib import Path
import csv, hashlib, json

BASE=Path(__file__).resolve().parent
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    provenance=json.loads((BASE/'recovery_provenance.json').read_text(encoding='utf-8'))
    original=BASE/'historical_package_contents.csv'
    assert sha(original)==provenance['historical_manifest_sha256']
    history={r['path']:r for r in rows(original)}
    catalog=rows(BASE/'recovery_catalog.csv')
    assert len(catalog)==len({r['historical_extraction_reference'] for r in catalog})==160
    by_ref={r['historical_extraction_reference']:r for r in catalog}
    total=0
    for r in catalog:
        p=(BASE/r['recovered_path']).resolve()
        assert p.is_relative_to((BASE/'files').resolve())
        old=history[r['historical_package_path']]
        assert sha(p)==r['recovered_sha256']==r['historical_sha256']==old['sha256']
        assert p.stat().st_size==int(r['bytes'])==int(old['bytes'])
        total+=p.stat().st_size
    selected=rows(BASE/'historical_manifest_selected_160.csv')
    assert len(selected)==160
    assert all(r==history[r['path']] for r in selected)
    original_refs=rows(BASE/'historical_reference_instances.csv')
    restored_refs=rows(BASE/'recovered_reference_instances.csv')
    assert len(original_refs)==len(restored_refs)==1405
    assert len({r['check_id'] for r in original_refs})==929
    for old,new in zip(original_refs,restored_refs):
        assert all(new[k]==v for k,v in old.items())
        r=by_ref[old['historical_extraction_reference']]
        assert new['recovered_path']==r['recovered_path']
        assert new['recovered_sha256']==r['recovered_sha256']
    assert total==provenance['restored_bytes']==6849488
    print(json.dumps({'restored_files':len(catalog),'byte_hash_matches':len(catalog),'reference_instances':len(original_refs),'distinct_check_ids':929,'restored_bytes':total,'new_extraction_performed':False},indent=2))
if __name__=='__main__':main()
