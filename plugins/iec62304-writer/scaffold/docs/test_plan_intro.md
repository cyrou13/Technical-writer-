<!--
  Narrative sections of the Software Test Description (STD) and of the STP /
  STDR deliverables. The working build (`tools/build_docs.py`) inlines the
  sections below into `docs/generated/30_STD.md`; the reference exporters
  inline them into the STP / STDR.

  Recognised sections:
    ## test-strategy   → STD section 3
    ## test-pass-fail  → STD section 4 (overrides the default)
    ## test-exclusions → STD section 7

  Any other H2 is ignored. Hand-maintained — no agent edits this file.
  Everything here is EXPORTED: present tense, no dates, no markers. A
  `[TODO …]` left below shows in the working draft by design and blocks a
  `--release` export (TL-1).
-->

## test-strategy

[TODO Describe the test strategy:

- levels targeted (unit / integration / system / E2E),
- method (TDD / BDD / test-after, coverage expectation),
- tooling (Vitest / Jest, pytest, Playwright / Cypress …),
- frequency and triggers (pre-commit, CI on pull request, nightly),
- scope of automation vs manual tests,
- fixtures and test data management,
- for a UI: the summative usability evaluation (IEC 62366-1) — method,
  sample size, pass / fail criteria.]

## test-exclusions

[TODO List what is NOT tested automatically and why:

- third-party components treated as black boxes (with justification and
  the `docs/ots.yaml` entry that carries their verification),
- environments not covered (mobile, legacy browsers …),
- load / performance scenarios out of scope for this release,
- accessibility tests deferred.]
