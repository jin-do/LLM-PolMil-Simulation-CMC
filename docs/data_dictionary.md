# Data Dictionary

| Field | Meaning |
| --- | --- |
| condition | Experimental system condition. GPT-4o, Gemini 2.5 Flash, and Claude Opus 4 are primary frontier LLM conditions; Perplexity Pro-based RAG is an auxiliary retrieval-augmented system-level condition. |
| run_id | Independent run identifier where available in source files. |
| final_outcome | Top-1 final scenario category coded from the run output. |
| aggregated_category | Three-category grouping used for chi-square tests: stalemate, diplomatic resolution, or adverse non-diplomatic outcomes. |
| tension | End-of-run crisis tension variable on a 0-1 scale. |
| diplomatic_support | End-of-run diplomatic support variable on a 0-1 scale. |
| public_opinion | End-of-run public opinion variable on a 0-1 scale. |
| leadership_unity | End-of-run leadership unity variable on a 0-1 scale. |
| VDM action category | Predefined action category in Variable-Decision Matrix.json. |
| trigger_thresholds | VDM thresholds that alter available policy options or trigger branch events. |
