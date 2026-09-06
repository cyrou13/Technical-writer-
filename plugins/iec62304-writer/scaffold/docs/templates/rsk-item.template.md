---
id: RSK-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0

# ISO 14971 risk category — selects the tab of the risk table this item lives in
risk_category: Design          # Design | Production | Usability

# ISO 14971 §C.2 — context: where the risk originates
software_function: [TODO]      # high-level function affected, e.g. "perfusion map computation"
software_item: [TODO]          # module / file path contributing to the hazard

# ISO 14971 §C.2 — chain of causation. The hazard is the potential source of harm as it exists in the released
# software — never the pre-control state ("nothing is pinned yet"), never a person or a host name.
hazard: [TODO potential source of harm]
initiating_causes: |
  - [TODO cause 1]
  - [TODO cause 2 — independent triggers that can start the sequence]
foreseeable_sequence: |
  (1) [TODO initial event]
  (2) [TODO intermediate step]
  (3) [TODO event leading to the hazardous situation]
hazardous_situation: [TODO circumstance of exposure]
harm: [TODO envisaged damage]

# Initial risk estimate (before mitigation) — on the scales DEFINED in dt-config.yaml
# `classification.severity_definitions` / `probability_definitions` (harm-based, ISO 14971 Annex C)
severity: Negligible           # Negligible | Minor | Serious | Critical | Catastrophic
probability: Remote             # Improbable | Remote | Occasional | Probable | Frequent
risk_level: Low                 # Low | Medium | High (qualitative, computed from the matrix)
acceptable: true                # true if no mitigation is needed

# Risk control hierarchy — ISO 14971 §7.2
# inherent_design        : eliminate the hazard at design time (preferred)
# protective_measure     : add a barrier / check that prevents harm
# information_for_safety : warn the user in the IFU / labeling — on its own it is NOT creditable risk
#                          reduction: the residual index stays at the initial index unless an engineering
#                          control also applies
control_hierarchy: inherent_design

# Residual risk (after mitigation) — re-evaluated once controls are in place. A residual accepted with an
# UNCHANGED index (same severity, same probability) requires a stated rationale in `## Residual risk justification`.
residual_probability: Improbable
residual_severity: Negligible
residual_risk_level: Low
residual_acceptable: true

# Cascade — risks newly created by this mitigation (ISO 14971 §7.5)
arising_risks: []                # list of RSK IDs

# IFU disclosure — required only when control_hierarchy = information_for_safety
labeling_disclosure: null        # null or a verbatim string copied into the IFU

source:
  - [TODO path/to/file]
links:
  parent: []
---

<!-- Exported (risk analysis). Normative sections below state the risk as currently assessed. No dates, no "re-assessed on", no markers, no person or host name, no issue number. -->
## Hazard

[TODO the hazard as it exists in the released software (ISO 14971 §3.2) — describe the source of harm, not the state before the controls]

## Initiating causes

[TODO independent causes that can start the chain]

## Foreseeable sequence of events

[TODO numbered chain from initiating cause to the hazardous situation (ISO 14971 §C.2)]

## Hazardous situation

[TODO circumstance in which the user, patient or data is exposed]

## Harm

[TODO envisaged damage, as concrete as possible, on the harm definitions of the severity scale]

## Initial risk justification

[TODO why this severity and this probability, against the harm definitions of dt-config.yaml; cite evidence]

<!-- Exported (RAR, per record). One line per control: the SRS/SDS id, what the control does, and its tier. The formal controls are the items whose `links.mitigates` names this ID; the exporter prints each control's title and the status of the TC bound to it — a control's evidence is that bound TC status, nothing else. State the chosen `control_hierarchy` and why no higher tier is practicable. -->
## Risk controls

- SRS-XXX-NNN — [TODO what the control does] (tier: [TODO inherent_design | protective_measure | information_for_safety])

<!-- Exported (RAR, per record). The residual argument stays here, undated: why the index moved (or, if unchanged, why the risk is accepted anyway). If the argument was revised, the revision note goes to History. -->
## Residual risk justification

[TODO why the residual risk is acceptable after the controls]

<!-- Internal, never exported. -->
## Notes

[TODO context, links to `arising_risks`]

<!-- Internal, never exported. `[GAP-62304]` markers are allowed here and in History only. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Every re-assessment ("re-assessed after change X: probability unchanged"), decision and change note, dated, newest first. -->
## History

- YYYY-MM-DD v1.0.0 — created.
