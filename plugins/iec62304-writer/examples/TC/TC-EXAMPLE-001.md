---
id: TC-EXAMPLE-001
title: Example — login redirects to the identity provider with state and PKCE
status: Unknown
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
  - start the mock identity provider and load the client credentials
  - send GET /auth/login without a session cookie
  - capture the status code and the Location header
expected:
  - "login_flow_redirects_to_idp: HTTP 302 whose Location is the provider's authorisation endpoint with client id, redirect target, state of at least 256 bit and an S256 code challenge"
---

<!-- Exported (STDR). -->
## Preconditions

- A mock identity provider is listening on `http://localhost:9000`.
- The client identifier and secret are loaded in the environment.

<!-- Exported (STDR). Numbered procedure: fixture, action, observation. -->
## Steps

1. Start the mock identity provider and load the client identifier and
   secret in the environment.
2. Send `GET /auth/login` without a cookie.
3. Read the status code and the `Location` header of the response.

<!-- Exported (STDR). Numbered, one clause per test function of `test_id`, each traceable to an acceptance criterion of the verified SRS. -->
## Expected results

1. `login_flow_redirects_to_idp`: the status code is 302, the `Location`
   header points to the provider's authorisation endpoint, and the query
   string carries the client identifier, the redirect target, a `state`
   of at least `oauth_state_min_entropy` (256 bit) and a
   `code_challenge` with method `S256` (SRS-EXAMPLE-001 criteria 1
   and 2).

<!-- Internal, never exported. -->
## Notes

Example item shipped with the scaffold. `test_id` names a test that must
exist in the repository — a planned test is `test_id: "[TODO]"` and is
not counted as coverage. Steps are a procedure a reader can re-execute;
expected results hold one clause per test function, and the STDR prints
the bound per-function result next to each.

<!-- Internal, never exported. -->
## Open questions

- None.

<!-- Internal, never exported. Execution results are bound by tools/bind_test_results.py, never written here. -->
## History

- 2026-05-07 v1.0.0 — created as a scaffold example.
