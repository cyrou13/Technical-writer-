---
name: test-evidence
description: Discover existing tests and formalise them as TC items (IEC 62304 §5.5/§5.7) whose test_id resolves to a real test, whose expected results are numbered and traceable to acceptance criteria, and which never count a planned test as coverage. Invoke to produce docs/items/TC/.
---

# Test evidence — discovering and formalising tests

## Discovery

- **TS/JS** — Vitest / Jest: `**/*.{test,spec}.{ts,tsx,js,jsx}`,
  `__tests__/`, `vitest.config.*` / `jest.config.*`. Playwright /
  Cypress: `e2e/`, `tests/`, `cypress/`.
- **Python** — pytest: `test_*.py`, `*_test.py`, `tests/`; config in
  `pytest.ini`, `pyproject.toml [tool.pytest.ini_options]`, `setup.cfg`.
  unittest: `unittest.TestCase` subclasses.

## Granularity

- One `describe` / test class ≈ one module under test — a grouping, not
  an item.
- One `it` / `test_xxx` = one TC item; when a TC legitimately groups
  several test functions (one file verifying one requirement), `expected`
  holds **one clause per test function**, in the file order.
- A test that **runs a benchmark or release gate** (the 94-case sweep,
  the lock-vs-installed check) is its own TC of `type: System` — a unit
  test of the gate script does not record the gate run.
- The TC's **own domain** (the DOMAIN token of its id) is the STDR
  grouping key, so a TC verifying an SRS of another domain still sits
  under its own.

## `test_id` must exist

`test_id` is a re-runnable node id: `tests/x.py::test_a`,
`tests/x.py::Class::test_a`, `src/x.test.ts::<describe>::<it>`; several
joined by `;`. Before writing it, confirm the node exists (`grep -n "def
test_a" tests/x.py`, or `pytest --collect-only -q tests/x.py` when the
user allows running the collector). A TC whose test is not written yet
has `test_id: "[TODO]"`, `automated: false`, `status: Draft`, and is
**not counted as verification coverage** by the build or by the
reviewer (SL-4).

## Linking `verifies`

1. `// @verifies SRS-…` or `# @verifies SRS-…` in the test — authority.
2. Otherwise the SRS whose `source:` contains the file under test
   (usually the main import of the test file).
3. Otherwise `[TODO] SRS mapping` in `## Notes`, never invented.

## Body of a TC item

```markdown
<!-- Exported (STDR). Fixture and environment — never an internal ruling, a person, an issue number. -->
## Preconditions
- <fixture: "a 40-frame synthetic study with a known AIF at slice 12">

<!-- Exported (STDR). Numbered PROCEDURE: fixture, action, observation. -->
## Steps
1. <fixture — "load the synthetic study and the reference AIF">
2. <action — "run the AIF selection with the default configuration">
3. <observation — "read the selected voxel coordinates and the arrival time">

<!-- Exported (STDR). Numbered; ONE clause per test function of `test_id`, in the same order; each maps to an acceptance criterion of the verified SRS. -->
## Expected results
1. <`test_rejects_short_study`: status code is `QC_TOO_FEW_FRAMES` when the study holds fewer than `min_frames` (8) frames (criterion 1)>

<!-- Internal. -->
## Notes
## Open questions
## History
```

**Steps are a procedure**, not "Run pytest tests/x.py": a reader must be
able to re-execute them by hand from the fixture, the action and the
observation. The frontmatter `steps:` / `expected:` lists mirror the
body. **Expected results hold one clause per test function** of
`test_id`; the STDR prints, next to each clause, the **per-test-function
actual result** of the bound run (`passed` / `failed` / `skipped` /
`xfailed`), so a "N passed" total is never the actual result of a case.
Expected results quote the parameter names and values of the SRS they
verify; the reviewer must be able to put criterion `n` and expected
result `n` side by side. An expected result is never a status: "recorded
as a strict expected failure", "provisional bar", "DRAFT margin" are
anomalies (below), not results.

## Execution status

The real status is not guessable without running the tests.

- Default `status: Unknown` on a TC item; `executed_at: null`.
- `tools/bind_test_results.py --junitxml <report> --apply` binds a
  pytest run to the TC items (`status`, `executed_at`) and produces the
  STR input. Nobody writes an execution result into a TC body by hand,
  and never into `## History`.
- Binder statuses: `passed`, `failed`, `skipped`, **`passed_with_skips`**
  (at least one matched test function skipped), **`passed_with_xfail`**
  (at least one matched function is an expected failure), `not_run`.
  The item receives `Passed | Failed | Skipped | PassedWithSkips |
  PassedWithXfail | Unknown`. A skip or an xfail inside a case is
  **never masked as passed**; the STR counts them and the case appears
  in the **unresolved anomalies** appendix. `executed_at` is the suite
  start and the STDR says so.
- The binder records the **run metadata** the STR prints: software
  version and its source (`software_version`,
  `software_version_source`), `release_evidence_mode` (the
  `RELEASE_EVIDENCE_MODE` environment of the run), `hostname`,
  `platform`, `git_branch`, `git_dirty`, `python_version`,
  `pytest_version`, `numpy_version`, `run_started`. A run outside
  release-evidence mode or on a dirty tree is bound as such, not hidden.
- `/doc-62304` does not run the suite. Recommend that the user provide a
  junit report or run the binder.

## Anti-patterns

- Inventing a test that does not exist in the code.
- `status: Passing` without a bound execution report.
- A TC without `links.verifies` and without a `[TODO]` in `## Notes`.
- Counting a `[TODO]` / planned TC in a coverage figure.
- Tick-boxes or free prose in `## Expected results`.
- A date, a run id or a result in a normative section.
- "Run pytest <file>" as the only step; `steps: []` with a bound status.
- A status word, a draft margin or an expected-failure note as an
  expected result.
- A benchmark gate recorded only through a unit test of its script.
- Preconditions citing an internal ruling or a URSK that no reviewable
  document defines.
