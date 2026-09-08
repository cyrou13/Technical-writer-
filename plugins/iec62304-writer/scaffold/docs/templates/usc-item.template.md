---
id: USC-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
persona: [TODO user role, e.g. radiologist, operator, admin]
environment: [TODO usage environment: reading room, clinical console, browser]
task: [TODO business task accomplished, e.g. validate a case]
frequency: Occasional       # Rare | Occasional | Frequent | Continuous
criticality: Medium         # Low | Medium | High (impact if the task fails)
source:
  - [TODO path/to/UI/component]
links:
  parent: []
---

<!-- Exported (usability analysis). -->
## Persona

[TODO role, experience level, typical context]

## Preconditions

- [TODO system states required before the task]

## Normal usage sequence

1. [TODO step 1]
2. [TODO step 2]
3. [TODO final step = observable business effect]

## Foreseeable use errors

(Informal — those with impact become URSK items whose `use_scenario` names this ID.)

- [TODO error 1]

<!-- Internal, never exported. -->
## Notes

[TODO user documentation references]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated change notes, newest first. -->
## History

- YYYY-MM-DD v1.0.0 — created.
