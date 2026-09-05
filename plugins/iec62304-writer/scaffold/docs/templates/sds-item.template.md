---
id: SDS-XXX-NNN
title: [TODO] short title, 80 characters or fewer
status: Draft
version: 1.0.0
created: YYYY-MM-DD
updated: YYYY-MM-DD
reviewed: null            # last date the item was READ against the source it cites; set by the reviewer, never by a tool
owner: null               # who owes the open work on this item (a workstream, a role, a person)
target_release: null      # the release the open work is owed for, e.g. V1.0.0
module: [TODO] logical/path
parameters: []            # every frozen constant quoted in this item, declared ONCE across the store (same schema as SRS)
source:
  - [TODO] path/to/folder
links:
  parent: []
  implements: []
  mitigates: []
interfaces:
  inputs: []
  outputs: []
  depends_on: []          # internal modules by SDS ID; OTS components by their `component` key in docs/ots.yaml
---

<!-- Exported (SDS). Normative: what the module does, and only that. 1–3 sentences. -->
## Responsibility

[TODO 1–3 sentences]

<!-- Exported (SDS). Normative: the contracts the module offers and consumes. -->
## Interfaces

### Inputs
- [TODO]

### Outputs
- [TODO]

### Dependencies
- [TODO internal modules by SDS ID; OTS components by `docs/ots.yaml` key]

<!-- Exported (SDS). Normative: constraints the module maintains at all times. -->
## Invariants

- [TODO constraints maintained by the module]

<!-- Exported (SDS). Normative: the design as it is — data flow, algorithms, states, error handling. Present tense, no history. -->
## Design

[TODO the design as built]

<!-- Rationale. Not exported inline; rendered ONCE in the SDD rationale appendix. Alternatives discarded, why this design. No dates. -->
## Design notes

[TODO notable decisions, alternatives discarded]

<!-- Internal, never exported. -->
## Notes

[TODO working notes]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated closure notes, decisions, change notes, newest first. Replaces `## Changelog`. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO source].
