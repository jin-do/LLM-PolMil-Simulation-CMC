# AHP Power-Weight Method

This note documents how power weights were specified for the LLM-assisted Pol-Mil simulation testbed.

## Purpose

Power weights represent the relative influence of internal actors in a national decision process. They are not estimated behavioral parameters. In this project, AHP is used as a transparent documentation procedure for scenario-design assumptions.

## Procedure

1. Define the internal actors included in the scenario, such as President, Joint Chiefs of Staff, State Department, and Public Opinion.
2. Compare each pair of actors on Saaty's 1-9 relative-importance scale.
3. Enter the pairwise-comparison values into an AHP calculator workflow, such as the BPMSG AHP Online System.
4. Review the resulting priority vector and Consistency Ratio (CR).
5. Revise pairwise judgments when CR is above the target threshold. The working rule used here is CR < 0.1.
6. Insert the accepted priority-vector values into the JSON actor profiles as `power_weight` fields.

## Example

For a simplified U.S. actor set in the Cuban Missile Crisis testbed, the AHP documentation gives the following illustrative power weights:

| Actor | Power weight |
| --- | ---: |
| President | 0.48 |
| Joint Chiefs of Staff | 0.32 |
| Public Opinion | 0.20 |

These values make actor-influence assumptions explicit and auditable. They should be treated as scenario-design inputs rather than externally validated historical estimates.

## References

- Saaty TL. The analytic hierarchy process: planning, priority setting, resource allocation. New York, NY: McGraw-Hill; 1980.
- BPMSG AHP Online System: https://bpmsg.com/ahp-online-system/
- Super Decisions Software: https://superdecisions.com/
