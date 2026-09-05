# AHP Power-Weight Method

This note preserves the historical description of an AHP-based approach to specifying actor power weights. It is an illustrative method description, not a reconstruction of the calculations underlying the archived actor profiles.

## Purpose

Power weights represent assumed relative influence among internal actors in a national decision process. The archived values are researcher-set scenario-design inputs, not estimated behavioral parameters or externally validated historical measurements.

## Illustrative Procedure

The historical method note describes the following workflow:

1. Define the internal actors included in the scenario, such as President, Joint Chiefs of Staff, State Department, and Public Opinion.
2. Compare each pair of actors on Saaty's 1-9 relative-importance scale.
3. Enter the pairwise-comparison values into an AHP calculator workflow, such as the BPMSG AHP Online System.
4. Review the resulting priority vector and Consistency Ratio (CR).
5. Revise pairwise judgments when CR is above the target threshold. The historical note specifies CR < 0.1 as the intended criterion.
6. Insert the accepted priority-vector values into the JSON actor profiles as `power_weight` fields.

## Example

The historical note gives the following illustrative weights for a simplified U.S. actor set. These are an example only and are not the actual weight vectors in the archived JSON actor profiles.

| Actor | Power weight |
| --- | ---: |
| President | 0.48 |
| Joint Chiefs of Staff | 0.32 |
| Public Opinion | 0.20 |

The example shows how actor-influence assumptions can be expressed numerically. It does not establish how the actual profile weights were derived.

## Evidence Available

No full pairwise-comparison matrices or corresponding CR outputs for the actual profile vectors have been located in the available archive. Their AHP derivation and compliance with CR < 0.1 therefore cannot be independently reproduced or verified from this package. A method description and a normalized weight vector do not supply the missing calculation records. The profile weights should be interpreted as researcher-set assumptions unless those records are recovered.

## References

- Saaty TL. The analytic hierarchy process: planning, priority setting, resource allocation. New York, NY: McGraw-Hill; 1980.
- BPMSG AHP Online System: https://bpmsg.com/ahp-online-system/
- Super Decisions Software: https://superdecisions.com/
