---
id: RSK-EXAMPLE-001
title: Example — session hijack through a predictable OAuth2 state
status: Draft
version: 1.0.0
created: 2026-05-07
updated: 2026-05-07
reviewed: null
owner: null
target_release: null
risk_category: Design
software_function: user authentication
software_item: src/auth/oauth.ts
hazard: predictable OAuth2 state enabling CSRF on the callback
initiating_causes: |
  - state derived from a timestamp or a counter
  - state not bound to the pre-session
foreseeable_sequence: |
  (1) the attacker predicts the state value expected by the callback
  (2) the attacker sends the victim a forged callback link
  (3) the victim, already authenticated at the provider, follows it
hazardous_situation: the victim's browser completes a callback the attacker prepared
harm: session hijack, unauthorised access to the user's account and data
severity: Serious
probability: Remote
risk_level: Medium
acceptable: false
control_hierarchy: inherent_design
residual_probability: Improbable
residual_severity: Serious
residual_risk_level: Low
residual_acceptable: true
arising_risks: []
labeling_disclosure: null
source:
  - src/auth/oauth.ts
links:
  parent: []
---

<!-- Exported (risk analysis). Normative sections state the risk as currently assessed. No dates, no "re-assessed on", no markers. -->
## Hazard

An OAuth2 `state` generated without a cryptographic source lets an
attacker predict the value the callback expects and fix the victim's
session.

## Initiating causes

- `state` derived from a timestamp or a counter.
- `state` not bound to the pre-session that started the flow.

## Foreseeable sequence of events

1. The attacker predicts the `state` the callback will accept.
2. The attacker sends the victim a forged callback link.
3. The victim, already authenticated at the identity provider, follows it.

## Hazardous situation

The victim's browser completes a callback the attacker prepared.

## Harm

Session hijack: the attacker gains access to the user's account and to
the data it can reach.

## Initial risk justification

Severity `Serious` — privacy breach and unauthorised access. Probability
`Remote` — requires social engineering and an authenticated provider
session. Initial risk `Medium`, not acceptable without a control.

## Risk controls

- Cryptographic generation of `state` with the declared minimum entropy.
- Strict comparison on the callback between the received `state` and the
  one stored server-side for the pre-session.
- PKCE with the `S256` method in addition.

The formal controls are the items whose `links.mitigates` names this ID:
SRS-EXAMPLE-001, SDS-EXAMPLE-001 and TC-EXAMPLE-001.

<!-- Exported. The residual argument stays here, undated. A revision of the argument is noted in History. -->
## Residual risk justification

With a cryptographic `state` bound to the pre-session and verified on the
callback, a forged callback cannot be validated; the residual probability
is `Improbable` and the residual risk `Low`.

<!-- Internal, never exported. -->
## Notes

Example item shipped with the scaffold. It shows how an SRS, an SDS and a
TC mitigate one RSK and how the coverage matrix reflects it.

<!-- Internal, never exported. `[GAP-62304]` markers are allowed here and in History only. -->
## Open questions

- None.

<!-- Internal, never exported. Every re-assessment, decision and change note, dated, newest first. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
