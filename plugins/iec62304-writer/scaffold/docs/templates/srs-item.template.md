---
id: SRS-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
kind: functional          # functional | performance | interface | platform | usability | safety | security | process
verification: Test        # Test | Inspection | Analysis | Demo
priority: Must            # Must | Should | Could
parameters: []            # every frozen constant quoted in this item, declared ONCE across the store:
# parameters:
#   - name: series_number          # snake_case, unique across the whole store (one name = one value)
#     value: 1301
#     unit: null                   # SI unit or null for a count / enumeration
#     settable: false              # true if a site or user can change it at runtime
#     interval: null               # allowed range when settable, e.g. "[0.5, 6.0]"; null when fixed
#     source: src/export/series.py # where the constant is defined in the code
source:
  - [TODO] path/to/file.py
links:
  parent: []
  implements: []
  verifies: []
  mitigates: []
description: |
  The system shall [TODO testable behaviour] when [TODO condition].
---

<!-- Exported (SRS). Normative: present-tense behaviour only. No dates, decisions, hashes, code or test paths, competitor names. -->
## Description

The system **shall** [TODO behaviour] when [TODO condition], and **shall**
[TODO guarantee] in all cases.

<!-- Exported (SRS). Numbered list, one measurable criterion per line, the number stated (use the parameter name when the number is a declared parameter). Never tick-boxes. -->
## Acceptance criteria

1. [TODO criterion 1, measurable, with its number and unit]
2. [TODO criterion 2]

<!-- Internal, never exported. Rationale, where a threshold comes from, what was considered and rejected. -->
## Notes

[TODO non-normative context if useful]

<!-- Internal, never exported. Questions the code does not answer. Listed in the open-points register (--internal exports only). -->
## Open questions

- [TODO if anything cannot be inferred from the code]

<!-- Internal, never exported. Every dated closure note, decision, re-argument and change note goes here, newest first. Replaces `## Changelog`. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO source].
