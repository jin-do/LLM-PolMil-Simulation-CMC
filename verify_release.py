"""Verify the current public file inventory without network access or dependencies."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = ROOT / 'CURRENT_MANIFEST.csv'
    expected = (ROOT / 'CURRENT_MANIFEST.sha256').read_text(encoding='utf-8').split()[0]
    if sha(manifest) != expected:
        raise ValueError('Current manifest checksum mismatch')
    rows = list(csv.DictReader(manifest.open(encoding='utf-8', newline='')))
    seen = set()
    for row in rows:
        name = row['relative_path']
        path = (ROOT / name).resolve()
        if name in seen or not path.is_relative_to(ROOT):
            raise ValueError('Duplicate or invalid manifest path: ' + name)
        seen.add(name)
        if not path.is_file() or path.stat().st_size != int(row['bytes']) or sha(path) != row['sha256']:
            raise ValueError('Missing or altered file: ' + name)
    pins = list(csv.DictReader((ROOT / 'audit/rule_compliance/protocol/pinned_raw_source_links.csv').open(encoding='utf-8-sig', newline='')))
    for row in pins:
        if sha(ROOT / row['repo_path']) != row['sha256']:
            raise ValueError('Historical source changed: ' + row['repo_path'])
    pdfs = list((ROOT / 'runs/raw_logs').glob('*/*.pdf'))
    groups = {p.name: len(list(p.glob('*.pdf'))) for p in (ROOT / 'runs/raw_logs').iterdir() if p.is_dir()}
    if len(pdfs) != 120 or sorted(groups.values()) != [30, 30, 30, 30]:
        raise ValueError('Expected four groups of 30 execution PDFs')
    return {'status': 'PASS', 'manifest_files': len(rows), 'pinned_sources_verified': len(pins), 'execution_pdfs': len(pdfs), 'groups': groups, 'scope': 'File integrity and source identity; not semantic validation or historical model regeneration.'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
