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

<!-- Exported (cyber risk analysis). Normative sections state the threat as currently assessed. No dates, no markers, no CVE speculation. -->
## Threat

Script injection in the front end — an unescaped user comment, a raw
HTML insertion, or a compromised front-end component — lets an attacker
run script in the application's context and steal the session cookie.

## Threatened asset

The session cookie. Without the HttpOnly flag it is readable from
script; with it, the attacker can still drive the session from the
victim's browser.

## Exploitation vector

An unauthenticated Internet attacker inserts a payload through a user
field displayed verbatim, or exploits a vulnerable front-end component
listed in the OTS registry. The crossing is the browser-to-application
boundary of the global view.

## Level justification

Likelihood `Medium` — script injection remains a common defect and the
surface is public. Impact `High` — session theft is an account takeover.
Matrix → `risk_level: High`, not acceptable without controls.

## Expected controls

- Session cookie HttpOnly + Secure + SameSite=Lax.
- Strict content security policy (`script-src 'self'`, no inline
  scripts).
- Systematic escaping in the front end (framework default plus lint).
- Dependency audit of the front-end components.

The formal controls are the items whose `links.mitigates` names this ID:
SDS-EXAMPLE-001 and TC-EXAMPLE-001.

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
CSRF) and a cyber THR (XSS) through shared SDS / TC items. CVE / CWE
references go here, never in the body.

<!-- Internal, never exported. `[GAP-CYBER]` markers allowed here and in History only. -->
## Open questions

- None.

<!-- Internal, never exported. Dated re-assessments and change notes, newest first. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
