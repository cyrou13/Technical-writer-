---
id: SDS-EXAMPLE-001
title: Example — auth/oauth module
status: Draft
version: 1.0.0
created: 2026-05-07
updated: 2026-05-07
reviewed: null
owner: null
target_release: null
module: src/auth/oauth
parameters:
  - name: oauth_state_min_entropy
    value: 256
    unit: bit
    settable: false
    interval: null
    source: auth.oauth.STATE_MIN_ENTROPY   # a dotted symbol, never a path
source:
  - src/auth/oauth.ts
links:
  parent: []
  implements:
    - SRS-EXAMPLE-001
  mitigates:
    - RSK-EXAMPLE-001
    - THR-EXAMPLE-001
interfaces:
  inputs:
    - HTTP GET /auth/login
    - HTTP GET /auth/callback
  outputs:
    - HTTP 302 to the identity provider
    - session cookie, HttpOnly + Secure
  depends_on:
    - openid-client          # docs/ots.yaml key
    - jose                   # docs/ots.yaml key
---

<!-- Exported (SDS). Normative: what the module does, and only that. -->
## Responsibility

Runs the OAuth2 Authorization Code + PKCE handshake and creates the
signed session at the end of the callback.

<!-- Exported (SDS). Normative: the contracts the module offers and consumes. -->
## Interfaces

### Inputs
- `GET /auth/login` — without a session cookie.
- `GET /auth/callback?code=…&state=…` — the identity provider's return.

### Outputs
- HTTP 302 to the provider's authorisation endpoint with the OAuth2 and
  PKCE parameters.
- Session cookie `sid`, HttpOnly + Secure + SameSite=Lax.

### Dependencies
- `openid-client` — provider discovery and token exchange.
- `jose` — JWT verification.

<!-- Exported (SDS). Normative: constraints the module maintains at all times. -->
## Invariants

- `state` is generated with at least `oauth_state_min_entropy` (256 bit)
  of entropy and bound to the pre-session identifier.
- No identity-provider token is stored on the client side.

<!-- Exported (SDS). Normative: the design as it is. Present tense, no history. -->
## Design

The login handler creates a pre-session identifier, generates the
`state` and the PKCE verifier, stores both server-side under that
identifier, and answers with the redirection. The callback handler looks
the pre-session up by the cookie, compares the received `state` with the
stored one, exchanges the code with the PKCE verifier, verifies the
identity token signature, and only then issues the session cookie. Any
failure in that chain clears the pre-session and redirects to the login
page with an error code.

<!-- Rationale. Not exported inline; rendered ONCE in the SDD rationale appendix. No dates. -->
## Design notes

PKCE is enforced even though the client is confidential — defence in
depth against a leaked client secret. Storing the `state` server-side
rather than in a signed cookie was preferred so that a replayed callback
cannot be validated twice.

<!-- Internal, never exported. -->
## Notes

Example item shipped with the scaffold. The two third-party components
are named by their `docs/ots.yaml` key only — version and supplier live
in the registry.

<!-- Internal, never exported. -->
## Open questions

- None.

<!-- Internal, never exported. Dated change notes, newest first. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
