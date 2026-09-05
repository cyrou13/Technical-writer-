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
risk_level: Low                        # Low | Medium | High (3x3 matrix, skill cyber-risk-analysis)
acceptable: true                       # before mitigation
residual_acceptable: true              # after mitigation

# CIA triad (IEC 81001-5-1 + IEC TR 60601-4-5) — severity per dimension
confidentiality_severity: n/a          # n/a | Low | Medium | High
integrity_severity: n/a                # n/a | Low | Medium | High
availability_severity: n/a             # n/a | Low | Medium | High

# Residual CIA (after remediation)
residual_confidentiality_severity: n/a
residual_integrity_severity: n/a
residual_availability_severity: n/a

# Cybersecurity architecture view this threat is drawn on (docs/dt-clinical-context.md anchors)
architecture_view: security-global-view   # security-global-view | security-multi-patient-view | security-updateability-view | security-use-case-views
source:
  - [TODO path/to/file]
links:
  parent: []
  triggers: []                         # safety RSK IDs triggered if exploited
---

<!-- Exported (cyber risk analysis). Normative sections state the threat as currently assessed. No dates, no markers, no CVE speculation. -->
## Threat

[TODO the threat, anchored in the code or in a dependency of docs/ots.yaml]

## Threatened asset

[TODO asset compromised and the nature of the compromise]

## Exploitation vector

[TODO how the attacker exploits, from which position and trust boundary]

## Level justification

[TODO why this likelihood, this impact]

## Expected controls

- [TODO informal list; formal controls are the SRS/SDS/TC items whose `links.mitigates` names this ID]

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
