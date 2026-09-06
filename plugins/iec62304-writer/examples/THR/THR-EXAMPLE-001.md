---
id: THR-EXAMPLE-001
title: Example — session theft through XSS in the single-page application
status: Draft
version: 1.0.0
created: 2026-05-07
updated: 2026-05-07
reviewed: null
owner: null
target_release: null
stride: [S, I]
attacker: external_unauth
asset: session cookie
likelihood: Medium
impact: High
risk_level: High
acceptable: false
residual_risk_level: Low
residual_acceptable: true
confidentiality_severity: High
integrity_severity: Medium
availability_severity: n/a
residual_confidentiality_severity: Low
residual_integrity_severity: Low
residual_availability_severity: n/a
architecture_view: security-global-view
source:
  - src/auth/oauth.ts
  - src/frontend/index.html
links:
  parent: []
  triggers: []
---

<!-- Exported (cyber risk analysis, SDD threat records). Normative sections state the threat as currently assessed. No dates, no markers, no CVE speculation. -->
## Threat description

Script injection in the front end — an unescaped user comment, a raw
HTML insertion, or a compromised front-end component — lets an attacker
run script in the application's context and steal the session cookie.
Without the HttpOnly flag the cookie is readable from script; with it,
the attacker can still drive the session from the victim's browser.

## Attack path and preconditions

Entry interface: the HTTPS user interface (browser-to-application
boundary of the global view). The attacker is an unauthenticated
Internet user. Preconditions: a user field is rendered without escaping,
or a front-end component of the OTS registry carries an injection
defect. Path: the attacker stores the payload → a victim with an open
session renders the page → the script reads or drives the session.

## Level justification

Likelihood `Medium` — script injection remains a common defect and the
surface is public. Impact `High` — session theft is an account takeover.
Matrix → `risk_level: High`, not acceptable without controls.

## Controls

- SRS-EXAMPLE-001 — the session cookie is set HttpOnly, Secure and
  SameSite=Lax on a successful callback.
- SDS-EXAMPLE-001 — the front end serves a content security policy of
  `script-src 'self'` with no inline script, and escapes every rendered
  user field.

TC-EXAMPLE-001 verifies the first control; it is verification, not a
control, and the exporter prints its bound status next to the SRS.

## Residual

Residual level `Low` — accepted because a stolen cookie cannot be read
from script and an injected script cannot load under the policy; the
remaining path (driving the session from the victim's browser) requires
a policy bypass and ends with the session lifetime.

## CIA impact analysis

### Confidentiality
The session cookie and everything the session can read are exposed.

### Integrity
Actions can be taken in the victim's name for the life of the session.

### Availability
Not affected.

<!-- Internal, never exported. -->
## Notes

Example item shipped with the scaffold. It shows the safety / cyber
separation: the same `auth/oauth` module mitigates a safety RSK (callback
CSRF) and a cyber THR (XSS) through shared SRS / SDS items, and the four
exported sections a threat record needs: description, attack path with
preconditions, controls as requirement ids, residual level with its
acceptance condition. CVE / CWE references go here, never in the body.

<!-- Internal, never exported. `[GAP-CYBER]` markers allowed here and in History only. -->
## Open questions

- None.

<!-- Internal, never exported. Dated re-assessments and change notes, newest first. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
