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
parameters: []            # every frozen constant this item OWNS, declared once across the store and described in the text below:
# parameters:
#   - name: series_number          # snake_case, unique across the whole store — one owner per name
#     value: 1301                  # a list value is written as a YAML list, never as a truncated string:
#                                  #   value: [4, 6, 8, 10]
#     unit: null                   # SI unit or null for a count / enumeration
#     settable: false              # true if a site or user can change it at runtime
#     interval: null               # allowed range when settable, e.g. "[0.5, 6.0]"; null when fixed
#     source: package.export.series  # prose ("configuration schema") or a dotted symbol — NEVER a file path;
#                                  # the registry is rendered in SRS §4.1 and SDD §3.8 and the lint refuses paths
# A second item that quotes the same constant references it by name in its text; it never redeclares it.
references: []            # ids of `references:` entries of dt-config.yaml — every clinical threshold and every algorithm names its source
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

<!-- Exported (SRS), as a heading of its own. Normative: present-tense behaviour only. No dates, decisions, hashes, code or test paths, competitor names. Use the glossary term for every concept, verbatim (the labeling vocabulary wins). Every frozen parameter this item owns is described here. -->
## Description

The system **shall** [TODO behaviour] when [TODO condition], and **shall**
[TODO guarantee] in all cases.

<!-- Exported (SRS). Numbered list, one measurable behaviour per line with its number and unit (the parameter name when the number is a declared parameter). A tolerance is a number taken from the test that asserts it. Never a status, a test id, a decision id, a "placeholder until …", a "stays an expected failure". A measurement ("peak 20.6 GB") is evidence and goes to Notes; the bound ("at most `max_rss` (24 GB)") is the criterion. Never tick-boxes. -->
## Acceptance criteria

1. [TODO criterion 1: "<observable> is <relation> `<parameter>` (<value unit>)"]
2. [TODO criterion 2]

<!-- Internal, never exported. Rationale, where a threshold comes from, the measurements that motivated the bounds, what was considered and rejected. -->
## Notes

[TODO non-normative context if useful]

<!-- Internal, never exported. Questions the code does not answer. Listed in the open-points register (--internal exports only). -->
## Open questions

- [TODO if anything cannot be inferred from the code]

<!-- Internal, never exported. Every dated closure note, decision, re-argument and change note goes here, newest first. Replaces `## Changelog`. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO source].
