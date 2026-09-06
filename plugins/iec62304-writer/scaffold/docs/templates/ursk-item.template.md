---
id: URSK-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
use_scenario: USC-XXX-NNN              # parent USC
use_error: [TODO erroneous user action or inaction]
hazard: [TODO potential source of harm]
hazardous_situation: [TODO circumstance of exposure to the hazard]
harm: [TODO envisaged damage]
severity: Negligible       # Negligible | Minor | Serious | Critical | Catastrophic
likelihood: Remote         # Improbable | Remote | Occasional | Probable | Frequent
risk_level: Low            # Low | Medium | High (ISO 14971 matrix)
acceptable: true           # before mitigation
residual_acceptable: true  # after mitigation
source:
  - [TODO path/to/UI/component]
links:
  parent: []
  triggers: []             # safety RSK IDs triggered if the error occurs
---

<!-- Exported (usability analysis). Normative sections state the risk as currently assessed. No dates, no markers. -->
## Use error

[TODO precise description of the user action or inaction]

## Conditions favoring the error

[TODO confusable labels, ambiguous default, fatigue, multi-patient context]

## Hazard and harm

[TODO hazard → harm, short causal link]

## Level justification

[TODO why this severity, this likelihood, this risk_level]

## Expected controls

(ISO 14971 hierarchy: elimination > technical measure > information.)

- [TODO control 1]

The formal controls are the SRS/SDS/TC items whose `links.mitigates` names this ID.

<!-- Internal, never exported. -->
## Notes

[TODO usability study references, user training]

<!-- Internal, never exported. `[GAP-USE]` markers allowed here and in History only. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated re-assessments and change notes, newest first. -->
## History

- YYYY-MM-DD v1.0.0 — created.
