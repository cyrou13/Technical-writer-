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
parameters: []            # every frozen constant this item OWNS (same schema and rules as SRS: one owner per name, `source` is prose or a dotted symbol, never a path, list values as lists). A constant an SRS already owns is referenced by name in the text, never redeclared. Rendered in SDD §3.8 with the SRS parameters.
references: []            # ids of `references:` entries of dt-config.yaml — every algorithm names its source
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

<!-- Exported (SDS). Normative: what the module does, and only that. 1–3 sentences, no rationale. -->
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

<!-- Exported (SDS). Normative DETAILED DESIGN: the algorithm (formula, steps, model), the data (structures, fields, units), the interfaces it realises, and every threshold — as a number owned here, or by name when the registry owns it. Present tense, no history. "Features named, no formula" is a defect: a reviewer must be able to re-implement the module from this section. An architecture chart belongs here, not in Design notes. -->
## Design

[TODO the design as built: algorithm, data, interfaces, thresholds or a pointer to the registry]

<!-- Rationale ONLY: alternatives discarded and the reasons for this design. Not exported inline; rendered ONCE in the SDD rationale appendix. Nothing normative here — a statement that specifies the design (a rule, an allowlist, a bound, a chart) goes in Design. No dates. -->
## Design notes

[TODO alternatives discarded, why this design]

<!-- Internal, never exported. -->
## Notes

[TODO working notes]

<!-- Internal, never exported. -->
## Open questions

- [TODO]

<!-- Internal, never exported. Dated closure notes, decisions, change notes, newest first. Replaces `## Changelog`. -->
## History

- YYYY-MM-DD v1.0.0 — created from [TODO source].
