# Availability of historical extraction references

This note accompanies `historical_evidence_availability.csv` and applies to the frozen 1,387-row rule-compliance ledger. The ledger retains historical extraction locators to preserve its recorded provenance.

There are 1,405 nonempty `evidence_file` or `coverage_evidence_files` reference instances across 929 distinct check IDs whose extraction files are not distributed with these public modules. These references name the historical `cla_gem2_evidence/` text windows or `semantic_v2/sem_b_evidence.json`. The CSV identifies each reference without adding or changing a judgment.

For every listed instance, the public ledger retains a source PDF path, page field, and nonempty `evidence` excerpt. Its PDF is linked to a path present in the live-queried historical Git tree at commit `6867755772bfb74dd56c211df8c9a399607b5419`, with SHA-256 tied to verified bytes. The availability CSV provides the pinned URL and hash for each alternative source locator. Original PDFs were not duplicated in the standalone module bundle. They remain available in a full repository checkout or through the pinned public source links.

These retained locators and excerpts let a reader find the cited source passages. They are **not certified substitutes for the complete historical extraction windows or coverage records**. Excerpts may be bounded or truncated; a passage alone cannot establish that every applicable branch or absent turn was reviewed. This screen checked structural availability, not the semantic correctness or completeness of all judgments.

The missing extraction artifacts are not dependencies of the fixed-label aggregation command. Counts can be regenerated from the local frozen ledger and documented amendments. Rebuilding the exact historical extraction workflow, independently repeating every coverage decision, or newly adjudicating the full PDFs is a separate task and remains incomplete where the retained provenance is insufficient.

No missing file was silently treated as a successful source check. The CSV retains the preparation-stage status `extraction_availability=NOT_INCLUDED_IN_PUBLIC_CANDIDATE` and `full_window_or_coverage_equivalence_certified=False`; the historical extraction files remain undistributed. AI-generated evidence and judgments retain their AI provenance; this availability check does not turn them into human adjudication.

