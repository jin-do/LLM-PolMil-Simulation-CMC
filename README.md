# LLM-PolMil-Simulation-CMC

Research materials for *Structured LLM-Assisted Political-Military Scenario Generation: A Retrospective Assessment in a Cuban Missile Crisis Testbed*.

This repository preserves 120 historical execution PDFs and the inputs used in a structured LLM-assisted political-military scenario workflow. It supplies recorded judgments, source locators and code used to assess that archive. The four archive groups are GPT-4o, Gemini 2.5 Flash, Claude Opus 4 and Perplexity Pro, with 30 PDFs each. Complete provider and session settings are unavailable.

The 5 October 2026 update brings the public materials into line with the results in manuscript revision 29. It adds the later contextual review and conditional calculations, and restores previously omitted extraction files. It contains no new model executions or treatment–control experiment. Revision 30 of the submission documents updates the data-availability description; the research results remain those of revision 29.

## Start here

| Material | Location and purpose |
| --- | --- |
| Original execution records | [runs/raw_logs](runs/raw_logs): 120 PDFs, indexed with [pinned paths and hashes](audit/rule_compliance/protocol/pinned_raw_source_links.csv) |
| Historical inputs | [Actor profiles](actor_json), [VDM](vdm), [protocol and prompts](protocols); read the [input caveats](docs/input_artifact_caveats.md) |
| Common assessment | [audit/rule_compliance](audit/rule_compliance/README.md): 1,320 common judgments, amendments, alternative summaries, turn totals and partial checks |
| Top-1 recoding | [coding/top1_reanalysis](coding/top1_reanalysis/README.md): all 120 records, selection evidence and 16 withheld classifications |
| Survey | [docs/survey_summary](docs/survey_summary/README.md): sufficient statistics and wording caveats; no individual response rows |
| Contextual author review | [audit/author_review](audit/author_review/README.md): 40 judgments and later explanatory source checks |
| Later calculations | [audit/revision29_supplement](audit/revision29_supplement/README.md): Table B2 and Appendix D calculations |
| Recovered historical extractions | [audit/recovered_extractions](audit/recovered_extractions/README.md): 160 retained files and recovery provenance |
| Historical workbook analyses | [README_revision17.md](README_revision17.md): earlier analyses and reproduction commands, retained with their original scope |

## Reproduce the current tables

Use Python 3.10 or later, from the repository root. These commands use only the standard library and need no network connection, model account or API key.

```sh
python -X utf8 verify_release.py
python -X utf8 audit/rule_compliance/code/reproduce_revision17.py --out reproduced/core
python -X utf8 audit/revision29_supplement/code/reproduce_supplement.py --out reproduced/later
python -X utf8 audit/author_review/reproduce.py --out reproduced/author_review
python -X utf8 audit/recovered_extractions/verify.py
```

The first command checks the current file inventory and 126 pinned source assets, including all 120 execution PDFs. The remaining commands reproduce fixed-input calculations. Prepared outputs and provenance are supplied in the modules. The original revision-17 module and its manifests are preserved; its preparation-stage review status describes the September records, not the later contextual review.

```sh
python -X utf8 -m unittest discover -s audit/rule_compliance/tests -v
python -X utf8 -m unittest discover -s coding/top1_reanalysis/tests -v
python -X utf8 -m unittest discover -s audit/revision29_supplement/tests -v
```

Fresh PDF extraction is a separate operation. Optional dependencies and historical statistical analyses are described in [replication notes](docs/replication_notes.md). `.gitattributes` preserves file bytes across platforms so that checkout line endings do not invalidate source hashes.

## How the assessments relate

The conservative common assessment has 1,320 observations: 240 initial-setting observations and 360 in each later domain. C/V/U counts are 222/10/8 for initial compatibility, 180/173/7 for additional combinations, 316/17/27 for events, and 180/20/160 for continuation. The 67 selected observations and 40 diagnostic items have separate scopes and are not added to this denominator.

The earlier AI diagnostic assigned 15 C, 13 V and 12 U labels to 40 selected items. A later non-blind contextual review, confirmed by the corresponding author, recorded 27 acceptable, 10 revision-needed and 3 indeterminate judgments. It used a different criterion, with AI-assisted explanations; it is not independent double coding and does not replace the common ledger. The September 29 source recheck clarifies the 12 changed interpretations without collecting new human judgments.

Top-1 recoding classifies 104 executions as 61 stalemate, 38 diplomatic resolution and 5 full-scale war; 16 remain withheld. Table B2 shows that 61 of the 104 classified records differ from the original coding. This is not a verified count of original errors because the original branch-selection history is incomplete.

The arithmetic reconciliation is already public: [matching code](audit/rule_compliance/code/reproduce.py), [pair-level results](audit/rule_compliance/results/legacy_fixed/differences.csv) and [summary](audit/rule_compliance/results/legacy_fixed/reconciliation_summary.json). It finds 1,385 identical one-to-one pairs; 3 multiple-match groups, 324 candidate-only groups and 882 old-only groups remain separate. This is not an archive-wide arithmetic accuracy rate.

## Version and evidence boundaries

Historical PDFs and inputs are pinned to [6867755772bfb74dd56c211df8c9a399607b5419](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/6867755772bfb74dd56c211df8c9a399607b5419). Revision-17 modules are pinned to [4acc5add26f9b61d63ca3f51e7dfcc51c4a4e3fa](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/4acc5add26f9b61d63ca3f51e7dfcc51c4a4e3fa). Cite the commit containing the later supplement separately. [The release audit](docs/release_audit_20261005.md) records this update and its verification scope.

The 160 extraction files were absent from the revision-17 public commit. This update supplies retained copies matching a preserved local checksum inventory; they are not newly reconstructed text. The recovery guide distinguishes those checks from independent authentication of the original extraction process or review decisions.

Historical inputs retain 78 unresolved source placeholders, post-start information and scale inconsistencies. Public materials do not establish complete call-by-call settings, independent evaluator reliability, predictive validity or an advantage over less structured generation. The Q3 survey wording difference remains unresolved. Individual survey responses and reviewer correspondence are not included. The existing repository license is retained.
