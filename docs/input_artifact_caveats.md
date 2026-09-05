# Caveats for preserved input artifacts

The actor JSON files, Variable-Decision Matrix (VDM), prompt, protocol, and execution PDFs retain their original content from the source archive inspected at commit [`d345e7f391bef6f6c60c52d2a5907f0d166384ba`](https://github.com/jin-do/LLM-PolMil-Simulation-CMC/tree/d345e7f391bef6f6c60c52d2a5907f0d166384ba) on 5 September 2026. They are preserved so the historical workflow and its limitations remain inspectable. The clarifications below do not imply that corrected inputs were used in the archived executions.

## Temporal information

The declared scenario start is 14 October 1962, but the actor profiles also contain 21–22 October framing and later-known decisions or settlement elements, including quarantine-related positions and the Turkey-missile compromise. These inputs should not be treated as a clean contemporaneous information set for a counterfactual beginning on 14 October.

A hypothetical future trigger differs from a later historical fact supplied as already-known context. In particular, the Turkey-missile removal passage presents a conditional compromise option, not a statement that the later settlement has already occurred. It may be hindsight-informed design, but is not conclusive leakage on that wording alone. Explicit October 21–22 descriptions establish the cutoff failure. This audit does not verify every historical statement or classify every hypothetical future trigger as a factual error.

## Fixed events and generated continuations

The archived prompt supplies four event stages: missile-site discovery, a naval blockade confrontation with DEFCON 3, a U-2 shootdown, and a submarine-related DEFCON 2 episode. These researcher-injected events must be distinguished from generated actions, triggers, and narratives. A transcript's reference to an injected trigger does not establish autonomous event generation or independent adjudication.

The protocol describes several information modes, and the prompt requests multiple scenario reports. Neither document alone establishes the mode assignment actually used for every execution or explains how one summary code was selected from multiple branches. See the [design notes](final_experiment_design_notes.md) and [provenance audit](provenance_audit.md).

## Source markers in the actor JSON

The two actor JSON files contain 78 unresolved `oaicite`-style source markers: 41 in the U.S. profile and 37 in the Soviet profile. Neither file supplies HTTP source URLs that resolve those markers. These exported-looking tokens are not complete, independently traceable citations.

This is a provenance gap, not proof that every associated historical claim is false. The revision does not invent retrospective replacement citations or treat marker presence as successful source verification. A complete historical fact-check of the input profiles remains separate work.

## Scale and initialization

Section 5 of the archived protocol provides illustrative default values of zero and a numeric range of 0–100. The archived coding summaries use 0–1 values, while fractional thresholds appear elsewhere in the inputs and transcripts. A final-run ledger establishing the initial values actually used and any scale conversion has not been recovered.

The reanalysis therefore preserves the stored 0–1 values as unresolved workbook summaries. It does not silently apply the protocol's illustrative defaults, infer a conversion procedure, or reconstruct terminal states from incomplete records.

## Influence weights and state updates

The actor weights are researcher-set scenario inputs. The historical AHP note describes a general method and an illustrative weight vector, but full pairwise-comparison matrices and Consistency Ratio outputs for the actual profile weights have not been located. Their derivation cannot be independently reproduced from this package. See the [AHP method note](AHP_power_weight_method.md).

Likewise, named VDM rules do not demonstrate that each generated state update applied the intended rule, initial state, or arithmetic. A model's own assertion of compliance is not an independent verification of that assertion.

## Preserving uncertainty

Missing generation settings, resolvable source citations, initialization records, mode assignments, and branch-selection history remain unresolved. Reproducing a statistic from the existing coding table does not repair these historical evidence gaps.
