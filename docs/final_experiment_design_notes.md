# Final Experiment Design Notes

## Final information-input configuration

The final 120-run experiment used the Self-Guided Restricted Learning configuration only. The same JSON actor profiles, AHP-documented power weights, VDM effect rules, trigger thresholds, and prompt structure were used across GPT-4o, Gemini 2.5 Flash, Claude Opus 4, and the Perplexity Pro-based retrieval-augmented condition.

Curated and Hybrid modes were examined during pilot development as design alternatives, but they were not included in the final outcome-distribution experiment. The final results therefore compare LLM-based systems under one selected information condition rather than estimating a crossed model-by-mode effect.

## Pilot and final runs

More than 200 pilot runs were used to refine prompts, identify malformed JSON outputs, detect temporal leakage, compare information-input modes, and remove threshold dead ends. Pilot outputs were excluded from the final analysis. After pilot development, the self-guided configuration and VDM rule bundle were frozen before the final 120 runs.

## Perplexity condition

Perplexity Pro is treated as an auxiliary retrieval-augmented system-level condition rather than as a foundation-model-only comparison. The archived outputs do not contain a complete retrieval trace for every search decision, so the Perplexity results should be interpreted as exploratory system-level evidence.
