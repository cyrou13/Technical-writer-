---
id: SRS-EXAMPLE-001
title: Example — OAuth2 authentication requirement
status: Draft
version: 1.0.0
created: 2026-05-07
updated: 2026-05-07
reviewed: null
owner: null
target_release: null
kind: security
verification: Test
priority: Must
parameters:
  - name: oauth_state_min_entropy
    value: 256
    unit: bit
    settable: false
    interval: null
    source: auth.oauth.STATE_MIN_ENTROPY   # a dotted symbol, never a path
references:
  - RFC7636
source:
  - src/auth/oauth.ts
  - src/auth/oauth.test.ts
links:
  parent: []
  implements: []
  verifies: []
  mitigates:
    - RSK-EXAMPLE-001
description: |
  The system shall let an unauthenticated user start an OAuth2 Authorization Code flow with the configured identity provider and shall establish a signed session on a successful callback.
---

<!-- Exported (SRS). Normative: present-tense behaviour only. No dates, decisions, hashes, code or test paths, competitor names. -->
## Description

The system **shall** let an unauthenticated user start an OAuth2
Authorization Code flow with the configured identity provider, and
**shall** establish a signed session when the callback succeeds.

<!-- Exported (SRS). Numbered list, one measurable criterion per line, the number stated. Never tick-boxes. -->
## Acceptance criteria

1. A request to the login endpoint without a session is answered with a
   redirection (HTTP 302) to the identity provider's authorisation
   endpoint carrying the client identifier, the redirect target, a
   `state` value and a PKCE code challenge.
2. The `state` value has at least `oauth_state_min_entropy` (256 bit) of
   entropy, is stored server-side and is verified on the callback.
   The PKCE code challenge uses the `S256` method [RFC7636].
3. A successful callback sets a session cookie flagged HttpOnly and
   Secure.
4. A failed identity-provider exchange redirects the user to the login
   page with an error code and sets no session cookie.

<!-- Internal, never exported. -->
## Notes

This item is an **example** shipped with the scaffold; delete or replace
it once real items exist. It shows the contract: `kind` set, the one
constant declared in `parameters:` with a dotted `source` and quoted by
name, the literature reference named through `references:` (the id
resolves in `dt-config.yaml: references`), criteria numbered as
behaviour with a number, and no path in the exported text (the paths
are in `source:`).

<!-- Internal, never exported. -->
## Open questions

- None.

<!-- Internal, never exported. Dated change notes, newest first. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
