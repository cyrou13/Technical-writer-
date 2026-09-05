---
id: TC-EXAMPLE-001
title: Example — login redirects to the identity provider with state and PKCE
status: Draft
version: 1.0.0
created: 2026-05-07
updated: 2026-05-07
reviewed: null
owner: null
target_release: null
type: Integration
automated: true
test_id: src/auth/oauth.test.ts::login_flow_redirects_to_idp
executed_at: null
source:
  - src/auth/oauth.test.ts
links:
  verifies:
    - SRS-EXAMPLE-001
  mitigates:
    - RSK-EXAMPLE-001
    - THR-EXAMPLE-001
preconditions:
  - mock identity provider listening on localhost:9000
steps:
  - GET /auth/login without a session cookie
expected:
  - HTTP 302 to the provider's authorisation endpoint
  - client identifier, redirect target, state and code challenge present
---

<!-- Exported (STD). -->
## Preconditions

- A mock identity provider is listening on `http://localhost:9000`.
- The client identifier and secret are loaded in the environment.

<!-- Exported (STD). Numbered. -->
## Steps

1. Send `GET /auth/login` without a cookie.
2. Capture the HTTP response.

<!-- Exported (STD). Numbered, one observable per line, each traceable to an acceptance criterion of the verified SRS. -->
## Expected results

1. The status code is 302 and the `Location` header points to the
   provider's authorisation endpoint (SRS-EXAMPLE-001 criterion 1).
2. The query string carries the client identifier, the redirect target,
   a `state` of at least `oauth_state_min_entropy` (256 bit) and a
   `code_challenge` with method `S256` (criteria 1 and 2).

<!-- Internal, never exported. -->
## Notes

Example item shipped with the scaffold. `test_id` names a test that must
exist in the repository — a planned test is `test_id: "[TODO]"` and is
not counted as coverage.

<!-- Internal, never exported. -->
## Open questions

- None.

<!-- Internal, never exported. Execution results are bound by tools/bind_test_results.py, never written here. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
