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
- One `it` / `test_xxx` = one TC item.

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
<!-- Exported (STD). -->
## Preconditions
- <fixtures, environment>

<!-- Exported (STD). Numbered. -->
## Steps
1. <action>
2. <action>

<!-- Exported (STD). Numbered; each line maps to one acceptance criterion of the verified SRS, ideally in the same order. -->
## Expected results
1. <observable, with the number: "status code is `QC_TOO_FEW_FRAMES` when the study holds fewer than `min_frames` (8) frames">

<!-- Internal. -->
## Notes
## Open questions
## History
```

Expected results quote the parameter names and values of the SRS they
verify; the reviewer must be able to put criterion `n` and expected
result `n` side by side.

## Execution status

The real status is not guessable without running the tests.

- Default `status: Unknown` on a TC item; `executed_at: null`.
- `tools/bind_test_results.py --junitxml <report> --apply` binds a
  pytest run to the TC items (`status`, `executed_at`) and produces the
  STR input. Nobody writes an execution result into a TC body by hand,
  and never into `## History`.
- `/doc-62304` does not run the suite. Recommend that the user provide a
  junit report or run the binder.

## Anti-patterns

- Inventing a test that does not exist in the code.
- `status: Passing` without a bound execution report.
- A TC without `links.verifies` and without a `[TODO]` in `## Notes`.
- Counting a `[TODO]` / planned TC in a coverage figure.
- Tick-boxes or free prose in `## Expected results`.
- A date, a run id or a result in a normative section.
