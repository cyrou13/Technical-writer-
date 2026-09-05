---
id: PRSK-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0

# Production phase where the risk materialises
production_phase: Packaging      # Packaging | Delivery | Deployment | Update

# Asset exposed to the hazard
asset_at_risk: [TODO]            # container image, signing key, config file, artefact, etc.

# ISO 14971 §C.2 — chain of causation
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

# Initial risk estimate (before mitigation)
severity: Negligible             # Negligible | Minor | Serious | Critical | Catastrophic
probability: Remote              # Improbable | Remote | Occasional | Probable | Frequent
risk_level: Low                  # Low | Medium | High (qualitative, computed from the matrix)
acceptable: true                 # true if no mitigation is needed

# Risk control hierarchy — ISO 14971 §7.2
# inherent_design        : eliminate the hazard at process design time (preferred)
# protective_measure     : add a barrier / check that prevents harm
# information_for_safety : warn the operator / deployment team
control_hierarchy: protective_measure

# Residual risk (after mitigation) — re-evaluated once controls are in place
residual_probability: Improbable
residual_severity: Negligible
residual_risk_level: Low
residual_acceptable: true

source:
  - [TODO path/to/Dockerfile]
  - [TODO .github/workflows/release.yml]
links:
  parent: []
---

<!-- Exported (risk analysis, Production tab). Normative sections state the risk as currently assessed. No dates, no markers. -->
## Hazard

[TODO the hazard, anchored in a production artefact (Dockerfile, CI/CD workflow, deploy script, package manifest)]

## Initiating causes

[TODO independent causes: compromised registry, tampered base image, misconfigured CI secret, unpinned dependency, broken signing step]

## Foreseeable sequence of events

[TODO numbered chain from initiating cause to the hazardous situation]

## Hazardous situation

[TODO circumstance in which a corrupted or malicious artefact reaches the deployment target or the end user]

## Harm

[TODO envisaged damage: data integrity, patient safety, availability, propagation]

## Initial risk justification

[TODO why this severity and this probability; AAMI TIR57, IEC 81001-5-1 §6.1, incident data]

## Risk controls

[TODO informal list; formal controls are the SRS/SDS/TC items whose `links.mitigates` names this ID. Typical: image signing, pinned digests, SBOM attestation, reproducible builds.]

## Residual risk justification

[TODO why the residual risk is acceptable after the controls]

<!-- Internal, never exported. -->
## Notes

[TODO CI/CD configuration, SBOM tooling, key management, runbook references]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated re-assessments and change notes, newest first. -->
## History

- YYYY-MM-DD v1.0.0 — created.
