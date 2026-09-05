"""Search the full extracted text of the 120 archived execution PDFs.

These are document-marker checks, not an audit of output-only compliance,
state arithmetic, factual metadata, or independent validation. User prompts,
model outputs, and other text captured in a PDF are not separated.

Default execution reads PDFs with pypdf. An optional, hash-checked cache avoids
repeating PDF extraction; the output records whether a cache was used.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import re
from pathlib import Path

import pypdf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LOG_ROOT = ROOT / 'runs' / 'raw_logs'
OUTPUT = ROOT / 'analysis'

# A marker is present when every named pattern in its definition is found
# somewhere in the full document. Occurrence in a prompt also counts.
MARKERS = {
    'artifact_reference': {
        'artifact': r'\bJSON\b|Variable[-– ]Decision Matrix|\bVDM\b',
    },
    'explicit_result_log_label': {
        'result_log': r'result[ _-]?log',
    },
    'all_four_state_dimensions': {
        'tension': r'tension',
        'diplomatic_support_alias': r'diplomatic[ _-]?(?:support|room|engagement)',
        'public_opinion': r'public[ _-]?opinion',
        'leadership_unity_alias': r'leadership[ _-]?(?:unity|cohesion)',
    },
    'trigger_or_threshold': {
        'trigger_or_threshold': r'trigger|threshold',
    },
    'variable_status_label': {
        'generic_variable_status': r'variable[ _-]?status',
    },
    'explicit_reconfirm_variable_status': {
        'explicit_reconfirmation': r'reconfirm(?:ed)?[ _-]?variable[ _-]?status',
    },
    'metadata_labels_present': {
        'model_identifier_label': r'(?:model|system)[ _-]?(?:name|version|identifier|id)',
        'temperature_label': r'temperature',
        'top_p_label': r'top[_ -]?p',
        'seed_label': r'seed',
        'timestamp_label': r'(?:run|execution)[ _-]?(?:time|timestamp|date)',
    },
    'independent_checker_phrase': {
        'checker_phrase': r'independent (?:rule|transition|state) checker|deterministic (?:recalculation|recomputation|validator)',
    },
}

SCOPE = (
    'Full-document text-marker search after whitespace normalization. '
    'Prompts and generated outputs are not separated. A hit does not establish '
    'a populated output field, rule compliance, valid metadata, correct state '
    'arithmetic, or independent validation; a missing phrase does not establish '
    'the nonexistence of an external record.'
)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def normalize_pages(pages: list[str]) -> tuple[str, list[int]]:
    normalized = [re.sub(r'\s+', ' ', page).strip() for page in pages]
    starts = []
    offset = 0
    for page in normalized:
        starts.append(offset)
        offset += len(page) + 1
    return ' '.join(normalized), starts

def read_cache_manifest(path: Path | None) -> dict | None:
    if path is None:
        return None
    manifest = json.loads(path.read_text(encoding='utf-8'))
    manifest['by_path'] = {entry['raw_log_path']: entry for entry in manifest['entries']}
    if len(manifest['by_path']) != len(manifest['entries']):
        raise ValueError('Duplicate raw-log path in cache manifest')
    return manifest

def load_pages(path: Path, cache_dir: Path | None, manifest: dict | None) -> list[str]:
    if cache_dir is None:
        return [page.extract_text() or '' for page in PdfReader(path).pages]
    relative = path.relative_to(ROOT).as_posix()
    entry = manifest['by_path'].get(relative) if manifest else None
    if entry is None or sha256(path) != entry['pdf_sha256']:
        raise ValueError(f'Cached extraction has no matching PDF hash: {relative}')
    cache_path = (cache_dir / entry['text_file']).resolve()
    if cache_dir.resolve() not in cache_path.parents:
        raise ValueError('Cache path must remain within the supplied cache directory')
    if sha256(cache_path) != entry['text_sha256']:
        raise ValueError(f'Cached text hash mismatch: {relative}')
    text = cache_path.read_text(encoding='utf-8')
    pages = re.split(r'--- PAGE \d+ ---\n', text)[1:]
    if len(pages) != entry['pages']:
        raise ValueError(f'Cached page count mismatch: {relative}')
    return pages

def pattern_evidence(text: str, starts: list[int], pattern: str) -> dict:
    matches = list(re.finditer(pattern, text, flags=re.I))
    hit_pages: set[int] = set()
    for match in matches:
        first = bisect.bisect_right(starts, match.start())
        last = bisect.bisect_right(starts, max(match.start(), match.end() - 1))
        hit_pages.update(range(first, last + 1))
    if matches:
        match = matches[0]
        snippet = text[max(0, match.start() - 100):min(len(text), match.end() + 160)]
        # Preserve search behavior, but omit nonprinting controls from the
        # display-only excerpt so ordinary CSV readers can open the evidence.
        snippet = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', snippet)
        page = bisect.bisect_right(starts, match.start())
    else:
        snippet, page = '', ''
    return {
        'match_count': len(matches),
        'hit_pages': ';'.join(str(page) for page in sorted(hit_pages)),
        'first_hit_page': page,
        'representative_snippet': snippet,
    }

def audit(path: Path, pages: list[str]) -> tuple[dict, list[dict]]:
    text, starts = normalize_pages(pages)
    relative = path.relative_to(ROOT).as_posix()
    result = {'raw_log_path': relative, 'readable_text': len(text.strip()) >= 500}
    evidence = [{
        'raw_log_path': relative,
        'marker': 'readable_text', 'pattern_key': 'minimum_characters',
        'pattern': 'at least 500 normalized extracted characters',
        'marker_present': result['readable_text'],
        'match_count': '', 'hit_pages': '', 'first_hit_page': '',
        'representative_snippet': f'{len(text.strip())} normalized extracted characters across {len(pages)} PDF pages',
    }]
    for marker, patterns in MARKERS.items():
        pieces = [(key, pattern, pattern_evidence(text, starts, pattern)) for key, pattern in patterns.items()]
        result[marker] = all(piece['match_count'] > 0 for _, _, piece in pieces)
        for key, pattern, piece in pieces:
            evidence.append({
                'raw_log_path': relative, 'marker': marker,
                'pattern_key': key, 'pattern': pattern,
                'marker_present': result[marker], **piece,
            })
    return result, evidence

def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cached-text-dir', type=Path)
    parser.add_argument('--cache-manifest', type=Path)
    args = parser.parse_args()
    if bool(args.cached_text_dir) != bool(args.cache_manifest):
        parser.error('--cached-text-dir and --cache-manifest must be supplied together')
    manifest = read_cache_manifest(args.cache_manifest)
    paths = sorted(LOG_ROOT.rglob('*.pdf'))
    if len(paths) != 120:
        raise RuntimeError(f'Expected 120 PDFs, found {len(paths)}')
    rows, evidence = [], []
    for path in paths:
        row, entries = audit(path, load_pages(path, args.cached_text_dir, manifest))
        rows.append(row)
        evidence.extend(entries)
    fields = list(rows[0])[1:]
    summary = {
        'scope': SCOPE,
        'unit': 'archived execution PDF',
        'extractor': 'pypdf.PdfReader.page.extract_text',
        'runtime_pypdf_version': pypdf.__version__,
        'cached_text_used': args.cached_text_dir is not None,
        'cache_source_extraction_date': manifest.get('source_extraction_date') if manifest else None,
        'cache_manifest_sha256': sha256(args.cache_manifest) if manifest else None,
        'cache_pdf_and_text_hashes_checked': len(paths) if manifest else 0,
        'input_pdf_sha256': {path.relative_to(ROOT).as_posix(): sha256(path) for path in paths},
        'normalization': 'collapse whitespace to a single space; concatenate pages in order',
        'evidence_policy': 'All hit page numbers and counts; first-match representative snippet for each component pattern. Nonprinting control characters are removed from display snippets only, after searching. Snippets are not source-validated factual assertions.',
        'readable_text_definition': 'at least 500 normalized extracted characters; not a human readability assessment',
        'metadata_labels_definition': 'all five label-pattern groups occur somewhere in one PDF; no value completeness or validity check',
        'fields': {
            field: {
                'denominator': len(rows),
                'marker_present': sum(bool(row[field]) for row in rows),
                'marker_not_found': sum(not bool(row[field]) for row in rows),
                'marker_not_found_rate': sum(not bool(row[field]) for row in rows) / len(rows),
            }
            for field in fields
        },
    }
    OUTPUT.mkdir(exist_ok=True)
    write_csv(OUTPUT / 'traceability_log_audit.csv', rows)
    write_csv(OUTPUT / 'traceability_marker_evidence.csv', evidence)
    (OUTPUT / 'traceability_audit_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'cached_text_used': summary['cached_text_used'], 'fields': summary['fields']}, indent=2))

if __name__ == '__main__':
    main()
