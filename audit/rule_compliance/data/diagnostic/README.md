# 40-item explanatory AI re-review

Analysis: the preserved 2026-09-20 AI ledger used by revision 17 Appendix A7. This module reaggregates fixed labels; it does not perform another semantic review.

`ai_review_40.csv` preserves the complete source CSV byte-for-byte, including `reviewer_type=AI` and blank human judgment fields. Its 38 selected common checks overlap the 1,320-item common frame; the two `TRACE-*` rows are separately selected discrepancy examples. None of these 40 rows may be added to the common denominator. The set is purposive, with no population error-rate or human–AI agreement interpretation.

From the repository root:

```sh
python audit/rule_compliance/code/reproduce_diagnostic.py
```

When the current conservative core exists at `results/conservative_common_1320.csv`, the command also checks all 38 common IDs and labels against it, and checks the three already-applied amendments against `data/adjudication/patches.json`. Explicit paths are supported with `--core-ledger` and `--patch-ledger`. The script never writes to these inputs. Without a core ledger, standalone diagnostic counts are reproduced and `core_linkage_checked=0` explicitly records the unperformed link check.

Expected diagnostic composition: common selected 15 C / 11 V / 12 U; representative discrepancies 0 C / 2 V / 0 U; all 40 items 15 C / 13 V / 12 U. Human fields being blank in this AI ledger does not establish that no subsequent qualitative author review occurred.

`u_reason_assignments.csv` records one principal explanatory reason for each of the 12 U items, matching revision 17 Table A5. The principal reasons do not exclude other uncertainties. Counts are 4 missing-response, 3 active-parent-set, 2 post-termination applicability, 1 certainty-language and 2 compound-event-linkage items. HR-005/008 share the missing CLA-03 Turn 4 response; HR-014/019 share the missing GPT-25 Turn 2 response. Four judgment items therefore arise from two shared missing records, not four independent failures.

`existing_change_links.csv` records HR-011, HR-037 and HR-038 as references to already-applied corrections, never as three new amendments. Original rules, retrospective operating criteria and future design recommendations must remain distinct. No new pruning, retention or priority rule is applied retrospectively.

The original explanations are available in [Markdown](AI_REVIEW_EXPLANATION.md) and [HTML](AI_REVIEW_EXPLANATION.html). Public copies clarify the AI title and omit a private submission identifier and internal manuscript-editing advice. Item judgments and source references are retained. `review_scope.json` preserves the original scope and five direct PDF hash-check records; these are historical records, not new checks performed by this repository integration. Original PDFs are linked at a fixed historical commit instead of duplicated. A new PDF-level reassessment requires the historical PDFs from a full repository checkout or pinned-source downloads and is outside the replay.

Conditional arithmetic inputs preserve the representative CLA-01 example. `conditional_effect_sources.csv` links the two named effects to the original requirement IDs, source locators and input hashes. Decimal arithmetic and 0–1 clamping reproduce public opinion 0.85 versus recorded 0.80; this checks the named-effect calculation only and does not certify action-to-effect selection. The narrative/log example TRACE-GEM28 remains a fixed source-linked diagnosis, not a newly automated semantic test.

Outputs are in `../../results` relative to this directory: diagnostic counts, domain counts, principal U-reason counts, shared missing-response dependencies, conditional arithmetic and optional current-core linkage. Scientific outputs contain no current timestamps and are deterministic.

Python 3.10+ and its standard library suffice. No network, AI API key or original private working directory is required for fixed-label aggregation. Review criteria explain C/V/U but do not convert an AI judgment into human validation. Source PDF identity alone does not prove which file was attached in the historical simulation call.

In the integrated package, the root wrapper writes to `reproduced/diagnostic`, `reproduced/top1`, or `reproduced/survey`, respectively. Standalone module commands accept `--out`. The prepared integrated outputs are under `audit/rule_compliance/results/`.
