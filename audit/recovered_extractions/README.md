# Recovered historical extraction windows

The revision-17 release documented 1,405 references, across 929 check IDs, to 160 historical extraction artifacts that were not included in that release. This module now supplies those artifacts from the retained earlier audit package. No text was newly extracted or reconstructed for this recovery.

All 160 files match the SHA-256 and byte size recorded in the retained historical `package_contents.csv`: 159 text windows under `cla_gem2_evidence/` and one keyed evidence file, `semantic_v2/sem_b_evidence.json`, totaling 6,849,488 bytes. Extraction defects, replacement characters, and the original line endings remain unchanged.

## Find an extraction

- [Recovery catalog](recovery_catalog.csv): maps each historical reference to its restored file and old/current hashes.
- [All 1,405 reference instances with recovery locations](recovered_reference_instances.csv): retains check IDs, PDF links, pages, excerpts' availability indicators, and the new recovery status.
- [Original availability record](historical_reference_instances.csv): preserves the preparation-stage statement that these files were not included in the old release.
- [Selected historical manifest entries](historical_manifest_selected_160.csv): the 160 relevant hash/size records.
- [Full historical package manifest](historical_package_contents.csv): the preserved integrity source, containing 1,149 package entries. Its inclusion does not mean that all 1,149 listed files are publicly distributed.
- [Recovery provenance](recovery_provenance.json): identity basis, dates, scope, and screening results.

To verify the recovery from the repository root:

```text
python audit/recovered_extractions/verify.py
```

The verifier uses only Python's standard library. It checks the historical manifest's hash, every restored file against the recorded SHA-256 and byte size, and the complete reference mapping. It neither edits the common ledger nor runs an AI model.

## Limits of the recovery

The integrity source is a preserved local archival manifest, not an independently timestamp-certified record. A retained inventory from the September 20 review also records September 13 creation metadata for the package and these extraction artifacts. That private Drive inventory is not part of this public package.

Recovery makes the retained windows available for inspection. It does not certify that they include every passage originally considered, that a historical coverage decision was correct, or that AI-assisted labels have been independently validated. It does not recover missing model call settings or all evaluation-session records. The fixed-label aggregation did not require these extraction files and remains unchanged.

The old `NOT_INCLUDED_IN_PUBLIC_CANDIDATE` and `full_window_or_coverage_equivalence_certified=False` fields are preserved as historical fields. The appended `recovery_status` records the later availability change; restoring files is not a new semantic adjudication or a claim of full coverage equivalence.
