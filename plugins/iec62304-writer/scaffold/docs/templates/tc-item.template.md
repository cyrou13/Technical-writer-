---
id: TC-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Unknown           # Unknown until tools/bind_test_results.py binds a run: Passed | Failed | Skipped | PassedWithSkips | PassedWithXfail — never written by hand
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
type: Unit                # Unit | Integration | System | E2E — printed per case in the STDR, which groups cases by the DOMAIN token of the TC id, not by the verified SRS
automated: true
test_id: [TODO] file::test   # tests/x.py::test_a, tests/x.py::Class::test_a; several joined by `;`. MUST exist in the repo. A test that runs a benchmark or release gate is its own TC.
executed_at: null           # set by tools/bind_test_results.py --apply (the suite start, stated as such); never by hand
source:
  - [TODO] path/to/test_file.py
links:
  verifies: []
  mitigates: []
preconditions: []
steps: []                   # a PROCEDURE, not "run pytest <file>": the fixture, the action, the observation — one entry per step
expected: []                # one clause per test function of `test_id`, in the same order; the STDR prints the per-function actual result next to each
---

<!-- Exported (STDR). The fixture and the environment the procedure needs. Never an internal ruling, a person, an issue number. -->
## Preconditions

- [TODO fixture: "a 40-frame synthetic study with a known AIF at slice 12"]

<!-- Exported (STDR). Numbered PROCEDURE: what is set up, what is done, what is observed — a reader must be able to re-execute it by hand. "Run pytest tests/x.py" is not a procedure. -->
## Steps

1. [TODO fixture — "load the synthetic study and the reference AIF"]
2. [TODO action — "run the AIF selection with the default configuration"]
3. [TODO observation — "read the selected voxel coordinates and the arrival time"]

<!-- Exported (STDR). Numbered, ONE clause per test function of `test_id`, in the same order; each traceable to an acceptance criterion of the verified SRS, quoting the parameter name and value. Never a status, a "recorded as an expected failure", a draft margin — an xfail is an unresolved anomaly, listed in the anomalies appendix, not an expected result. -->
## Expected results

1. [TODO "<test function>: the selected voxel lies within `aif_max_offset` (2 voxels) of the reference (criterion 2)"]

<!-- Internal, never exported. -->
## Notes

[TODO if the mapping to SRS is not obvious]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated change notes, newest first. Execution results are NOT written here — they are bound by tools/bind_test_results.py. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO test file].
