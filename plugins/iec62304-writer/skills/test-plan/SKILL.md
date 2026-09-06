---
name: test-plan
description: Convention for the Software Test Description (STD, IEEE 829 / IEC 62304 §5.5/§5.7) built from TC items and the hand-maintained narrative in docs/test_plan_intro.md, and for how STP / STDR / STR deliverables consume it. Invoke to generate or understand docs/generated/30_STD.md.
---

# STD — Software Test Description

`docs/generated/30_STD.md` is regenerated on every `python
tools/build_docs.py`; **never edit it by hand**. The customer-facing STP
(plan), STDR (description and results) and STR (report) are produced by
the reference exporters (`scaffold/tools/README.md`) from the same items
and the same narrative file, under the release gate of
`submission-readiness`. Each takes **its own identifier and title** from
`dt-config.yaml: documents.{stp, stdr, str}` (the title is
`document.title` with the document type substituted — an STP is never
titled after the SRS) and `project_references` entries that cite them
carry the same identifiers (SL-10).

## Inputs

- **TC items** (`docs/items/TC/*.md`), grouped by `type`.
- **Codemap** (`docs/generated/_codemap.md`) for the detected frameworks.
- **`docs/test_plan_intro.md`** — narrative sections inlined by the build.

## Structure produced

1. Introduction — purpose, references, levels covered.
2. Test environment — frameworks detected from the manifests.
3. Test strategy — from `## test-strategy`, else a `[TODO]` placeholder.
4. Pass / fail criteria — conservative default, overridable by
   `## test-pass-fail`.
5. Coverage — table per level (#TC, #Must SRS covered). **Only TC with a
   resolvable `test_id` count** (SL-4).
6. Test cases — table per level (ID, title, `verifies`, automated).
7. Exclusions — from `## test-exclusions`, else `[TODO]`.

Appendix A: each TC rendered once (title, status, verifies / mitigates,
source, exported body sections only — `## Notes`, `## Open questions`,
`## History` are stripped; no per-item version).

## What the three exports must contain

**STP** — the coverage table names every uncovered requirement (id +
title), states the coverage rule it applies ("Must requirements only"
said, never implied), and the ID format once. Tool qualification
(`## test-tools`, `## qualification`) gives a rationale per tool at an
exact version, not "off-the-shelf, versions locked".

**STDR** — cases **grouped by the TC's own domain** (the DOMAIN token
of its id), each with its `type`, `verifies`, `mitigates`, the
procedure, and per expected clause the **per-test-function actual
result** of the bound run; `executed_at` stated as the suite start; the
summary by type totals every case (Security, Static, Usability rows
included); every narrative anchor it cites (`test-data-doc`,
`hardware-and-software-requirements`, `test-tools`) resolves.

**STR** — the run metadata block (software version + source,
release-evidence mode, host, platform, branch, dirty flag, Python /
pytest / numpy versions, run start); results by status including
`PassedWithSkips` / `PassedWithXfail` / `Skipped`, never folded into
passed; an **anomalies and deviations** section; the **disposition of
every not-executed case** (why, owner, when); the **unresolved
anomalies** appendix; and a **conclusion** (pass / fail against the
stated criteria, with the count of anomalies carried). A run on a
workstation outside release-evidence mode is reported as such.

## `docs/test_plan_intro.md` format

H2 sections whose slug is the key:

```markdown
## test-strategy
## test-pass-fail
## test-exclusions
```

Other H2 headers are ignored. Hand-maintained; no agent edits it. A
`[TODO]` left in it appears in the working-draft STD by design, and
blocks a `--release` export (TL-1).

## Test levels

`type` ∈ `Unit`, `Integration`, `System`, `E2E` (default `Unit`).

- **Unit** — isolated components.
- **Integration** — interfaces between backend modules.
- **System** — end-to-end backend without UI.
- **E2E** — end-to-end through the real UI (Playwright, Cypress);
  tracked separately for IEC 62366-1; often carries
  `links.mitigates: [URSK-…]`.

Class A: §5.6 integration is lightened; an empty Integration table is
acceptable and rendered as such.

## Usability sub-type

```yaml
type: E2E
usability_type: formative   # formative | summative
```

At least one `summative` TC per USC with `criticality: High`
(checked by `compliance-reviewer`).

## Default pass / fail

- **PASS** — every Must TC executed and passing; no orphan TC; every
  `PassedWithSkips` / `PassedWithXfail` case dispositioned in the
  anomalies appendix.
- **FAIL** — at least one TC verifying a Must SRS failing.
- **Skipped**, **PassedWithSkips**, **PassedWithXfail** — traced, not a
  pass; each is an unresolved anomaly until the skip or xfail is
  removed.

The STD does not consume execution results. The **STR** does, from the
output of `tools/bind_test_results.py --junitxml … --apply`, which sets
`status` and `executed_at` on the TC items.

## Guard rails

- Never edit `30_STD.md` by hand.
- Never write a run result, a date or a run id into a TC body.
- Planned tests (`test_id: "[TODO]"`) are listed as planned, not
  counted.
- A system test that runs the benchmark or release gate has its own TC;
  "System tests (3)" in the STP must name three.
