# Follow-up contextual author review

This module supports Appendix A9 (Tables A7–A8) of manuscript revision 29. It keeps the September 27 author-confirmed contextual judgments separate from the common 1,320-item rule-compliance assessment and the earlier September 20 AI diagnostic.

## Reproduce the tables

From the repository root, run:

```text
python audit/author_review/reproduce.py --out audit/author_review/results
```

Python's standard library is sufficient. The command verifies the preserved input hashes, derives a normalized 40-row register, and calculates the transition table. It makes no network or model calls and assigns no new judgments.

The [summary](results/contextual_summary.json) records 27 acceptable (A), 10 requiring revision (R), and 3 indeterminate (I) items. The 38 items already in the common frame contain 27 A, 8 R, and 3 I; the two purpose-selected trace examples both require revision. The [CSV register](results/contextual_review_40.csv) and [JSON register](results/contextual_review_40.json) retain every item identifier and source link.

## What the records mean

The author confirmed direct review of the source material and proposed judgments for all 40 items on September 27, 2026. The actual date of review was not separately specified. AI prepared the evidence and initial proposals, and the author reviewed those proposals without blinding. No separate independent human label set or inter-rater reliability estimate was collected.

The byte-preserved [historical JSON](source_records/author_review_20260927.json) and [CSV](source_records/author_review_20260927.csv), together with the preserved judgments in the [historical report](source_records/author_review_report_20260927.md), use C/V/U for the contextual judgments. To avoid confusing them with the common assessment, the normalized outputs render those same historical values as A/R/I. This is a notation change only. The common ledger is not altered, and the 40 selected items are not added to its denominator.

Fifteen earlier C judgments map to contextual A; 13 earlier V judgments map to 3 A and 10 R; 12 earlier U judgments map to 9 A and 3 I. The 12 differences combine a change in criterion with interpretive review of selected cases. They are not measurements of AI error, human–AI agreement, or model performance.

## Later clarification of the 12 changed interpretations

Read the [September 29 source recheck](evidence_recheck/changed_12_cases_20260929.md) alongside the historical report. Its [machine-readable record](evidence_recheck/changed_12_cases_20260929.json) preserves the earlier source-record hash, source pages, findings, and narrower explanations used in later manuscript revisions.

This was an AI-only source recheck. It collected no new human judgments and changed neither the historical contextual labels nor the common-rule labels. For example, HR-004 was accepted for contrasting possible developments even though one parent still lacked an additional explicit U.S.–Soviet action pair. Broader narrative acceptance does not establish fulfillment of that procedural requirement. Other clarifications distinguish later narrative evidence from a missing contemporaneous turn record, scenario-family continuity from complete branch tracking, and an explained termination from permission to terminate under the original protocol.

The earlier Korean report is retained as a historical record, not as current instructions or a substitute for these later qualifications. Its one link to an unpublished manuscript insertion draft is replaced by plain text noting that draft's exclusion. The source manifest records both the original and public-copy hashes; judgments, reasons, and evidence are unchanged. The normalized register carries the September 29 English clarification for all 12 affected items.

## Provenance and scope

[The source manifest](source_records/manifest.json) fixes the bytes of the preserved records. The source JSON SHA-256 is `5049d038623b23ca243c2e9d96e7bd469f35ebea5d21c8dbf41f6fb516c51aa5`; identical copies were retained in the September 27 and September 29 work folders. Source links point to the historical repository commit `6867755772bfb74dd56c211df8c9a399607b5419`.

No archived simulation output is repaired by this module. It does not independently validate historical assumptions, every numerical state transition, or the full common assessment. Personal local filesystem paths from the separate historical PDF-hash log are not published; the source URLs and PDF SHA-256 values remain in the preserved author-review records.

The public September 29 JSON and report omit manuscript insertion drafts and the internal working-file list. All 12 case records, quotations, findings and interpretive limitations are retained. Original and public-copy hashes, byte sizes and the transformation are recorded in the source manifest.
