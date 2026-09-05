---
id: TC-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
type: Unit                # Unit | Integration | System | E2E
automated: true
test_id: [TODO] file::test   # tests/x.py, tests/x.py::test_a, tests/x.py::Class::test_a; several joined by `;`. MUST exist in the repo.
executed_at: null           # set by tools/bind_test_results.py --apply; never by hand
source:
  - [TODO] path/to/test_file.py
links:
  verifies: []
  mitigates: []
preconditions: []
steps: []
expected: []
---

<!-- Exported (STD). -->
## Preconditions

- [TODO]

<!-- Exported (STD). Numbered. -->
## Steps

1. [TODO]
2. [TODO]

<!-- Exported (STD). Numbered, one observable per line, each traceable to an acceptance criterion of the verified SRS. -->
## Expected results

1. [TODO]

<!-- Internal, never exported. -->
## Notes

[TODO if the mapping to SRS is not obvious]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated change notes, newest first. Execution results are NOT written here — they are bound by tools/bind_test_results.py. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO test file].
