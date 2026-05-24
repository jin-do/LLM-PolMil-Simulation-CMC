# LLM-PolMil-Simulation-CMC

## 1. Overview

This repository contains replication materials for a structured LLM-assisted Pol-Mil simulation framework tested in a Cuban Missile Crisis benchmark. The project evaluates whether JSON actor profiles, AHP-documented power weights, and a Variable-Decision Matrix (VDM) can make LLM-assisted scenario generation more traceable, controllable, and auditable.

This is a proof-of-concept framework evaluation. It is not a predictive model of the Cuban Missile Crisis.

## 2. Repository Structure

- `protocols/`: simulation protocol and prompt templates.
- `actor_json/`: U.S. and Soviet actor JSON profiles used in the final framework.
- `vdm/`: Variable-Decision Matrix and VDM action-space notes.
- `runs/raw_logs/`: raw execution logs for final runs, organized by condition.
- `coding/`: final outcome coding table, coding rules, and expert survey public materials.
- `analysis/`: statistical scripts, outcome tables, variable summary, and figure inputs.
- `figures/`: manuscript Figure 1 and Figure 2.
- `docs/`: data dictionary, file inventory, AHP method note, and replication notes.

## 3. Experimental Conditions

Primary frontier LLM comparison:

- GPT-4o
- Gemini 2.5 Flash
- Claude Opus 4

Auxiliary system-level condition:

- Perplexity Pro-based retrieval-augmented system

The Perplexity condition combines generation with retrieval, source ranking, and platform-level information access. It should not be interpreted as a direct foundation-model-only comparison.

## 4. Simulation Framework

The framework combines:

- JSON actor profiles for actor roles, goals, constraints, preferences, and behavior algorithms.
- AHP-documented power weights as auditable design assumptions.
- Variable-Decision Matrix (VDM) rules for action categories, variable-effect deltas, and trigger thresholds.
- A rule-effect-trigger cycle for turn-by-turn scenario progression.

The VDM is treated as an ex ante rule bundle. Each turn supplied the LLM with the current state, actor JSON, available VDM action categories, variable-effect rules, and trigger thresholds.

## 5. Data and Logs

The final experiment used 120 independent runs: 30 per condition. Final outcomes were coded into five categories and also aggregated into three categories for chi-square testing.

Five-category final outcomes:

- Protracted stalemate
- Diplomatic resolution
- Full-scale war
- Internal collapse
- Limited conflict

Three-category aggregation:

- Stalemate
- Diplomatic resolution
- Adverse non-diplomatic outcomes

## 6. Reproducing Analysis

From the repository root:

```bash
python analysis/statistical_analysis_script.py
```

Expected values:

- Four-condition aggregated table: chi-square = 37.00, Cramer's V = 0.393
- Three frontier LLMs only: chi-square = 15.08, Cramer's V = 0.289

The generated tables are in `analysis/outcome_tables.csv` and `analysis/variable_summary.csv`. Manuscript figures are in `figures/`.

## 7. Limitations

- Proof-of-concept framework evaluation, not a predictive crisis model.
- AHP weights are auditable design assumptions, not externally validated behavioral estimates.
- VDM deltas require sensitivity analysis.
- Traceability and grounding audits were author-led and require independent coding in future work.
- The Cuban Missile Crisis is a high-salience historical case likely represented in model pretraining data.
- Perplexity is structurally different from closed frontier LLM conditions.
- Expert survey materials are limited to public, non-identifying materials and aggregate notes.

## 8. Citation

Manuscript under review: *A Structured LLM-Assisted Pol-Mil Simulation Framework: Traceability, Scenario Diversity, and Design Control in a Cuban Missile Crisis Testbed*.

## 9. Contact

Contact information should follow the submitted manuscript. Public repository maintainers should avoid posting private reviewer correspondence or sensitive survey data.
