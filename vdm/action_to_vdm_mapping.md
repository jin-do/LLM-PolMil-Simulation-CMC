# VDM Action-Space and Variable-Effect Logic

The Variable-Decision Matrix was used as an ex ante rule bundle. The model selected an action category from the VDM-defined option space and generated a natural-language rationale. Researchers then audited whether the selected action, variable update, and trigger activation matched the published rule bundle.

| VDM action category | Typical strategic meaning | Variable-effect rule | Trigger relevance |
| --- | --- | --- | --- |
| Strike | Kinetic or imminent kinetic military option | Apply Strike deltas | May raise Tension above escalation threshold |
| Defense_Prep | Coercive military deployment without immediate kinetic use | Apply Defense_Prep deltas | May increase Tension while preserving some diplomatic space |
| Diplomatic_Success | Negotiation or compromise pathway succeeds | Apply Diplomatic_Success deltas | May prevent escalation trigger |
| Diplomatic_Failure | Diplomatic attempt fails or is rejected | Apply Diplomatic_Failure deltas | May reduce Diplomatic Support below threshold |
| Civil_Unrest | Domestic instability becomes a decision constraint | Apply Civil_Unrest deltas | May reduce Public Opinion and Leadership Unity |
| Strong_Leadership | Leadership consolidation or successful public framing | Apply Strong_Leadership deltas | May preserve Leadership Unity above threshold |
| Economic_Sanctions | Coercive non-kinetic pressure | Apply Economic_Sanctions deltas | May increase Tension and weaken diplomatic support |
| Alliance_Strengthening | External coordination strengthens bargaining position | Apply Alliance_Strengthening deltas | May increase Diplomatic Support and Leadership Unity |

When a selected action contained multiple strategic components, the primary VDM category selected by the model governed the variable update. Secondary components were reflected only when explicitly linked to a separate VDM rule in the published rule bundle.
