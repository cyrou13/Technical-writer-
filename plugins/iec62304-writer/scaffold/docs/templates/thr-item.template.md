---
id: THR-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
stride: [T]                            # S | T | R | I | D | E (may be combined)
attacker: external_unauth              # external_unauth | external_auth | internal | supply_chain | physical
asset: [TODO threatened asset]
likelihood: Low                        # Low | Medium | High
impact: Low                            # Low | Medium | High
risk_level: Low                        # Low | Medium | High (3x3 matrix, skill cyber-risk-analysis) — one matrix, applied the same way on every THR
acceptable: true                       # before mitigation
residual_risk_level: Low               # Low | Medium | High after the controls
residual_acceptable: true              # after mitigation; false requires the acceptance condition in `## Residual`

# CIA triad (IEC 81001-5-1 + IEC TR 60601-4-5) — severity per dimension
confidentiality_severity: n/a          # n/a | Low | Medium | High
integrity_severity: n/a                # n/a | Low | Medium | High
availability_severity: n/a             # n/a | Low | Medium | High

# Residual CIA (after remediation)
residual_confidentiality_severity: n/a
residual_integrity_severity: n/a
residual_availability_severity: n/a

# Cybersecurity architecture view this threat is drawn on (docs/dt-clinical-context.md anchors). All four views are required by the SDD export.
architecture_view: security-global-view   # security-global-view | security-multi-patient-view | security-updateability-view | security-use-case-views
source:
  - [TODO path/to/file]
links:
  parent: []
  triggers: []                         # safety RSK IDs triggered if exploited
---

<!-- Exported (cyber risk analysis, SDD threat records). Normative sections state the threat as currently assessed. No dates, no markers, no CVE speculation, no OTS version. -->
## Threat description

[TODO what the attacker achieves and against which asset, anchored in the code or in a component of docs/ots.yaml — "an attacker who controls the input series makes the decoder allocate unbounded memory and starves the host"]

<!-- Exported. The entry interface, the attacker position and trust boundary crossed, and every precondition the attack needs (access, a prior failure, a configuration). -->
## Attack path and preconditions

[TODO entry interface → boundary crossed → what must already hold → the step that compromises the asset]

<!-- Exported. Why this likelihood and this impact, with the matrix result. -->
## Level justification

[TODO why this likelihood, this impact]

<!-- Exported. The controls are REQUIREMENTS: SRS ids (and SDS ids for a design constraint), one line each, stating what the control does. A TC id is verification of a control and is never listed as a control; the exporter prints each control's bound TC status next to it. -->
## Controls

- SRS-XXX-NNN — [TODO what the control does]

<!-- Exported. The residual level after the controls and the condition under which it is accepted; when `residual_acceptable: false`, the condition that would make it acceptable and who owes it. -->
## Residual

Residual level `[TODO Low | Medium | High]` — accepted because [TODO condition], or not accepted until [TODO condition] (owner: [TODO]).

<!-- Exported. -->
## CIA impact analysis

### Confidentiality
[TODO how the threat affects confidentiality, or "Not affected"]

### Integrity
[TODO]

### Availability
[TODO]

<!-- Internal, never exported. -->
## Notes

[TODO CVE/CWE references, audit recommendation]

<!-- Internal, never exported. `[GAP-CYBER]` markers allowed here and in History only. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated re-assessments and change notes, newest first. -->
## History

- YYYY-MM-DD v1.0.0 — created.
