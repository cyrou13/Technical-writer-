---
name: items-store
description: Local item-per-file store for technical-file items (requirements, design, tests, risks, threats, use scenarios) — the offline equivalent of Matrix Requirements — and the section/frontmatter contract that separates normative, exported text from internal working notes. Invoke before creating, reading or updating any documentation item.
---

# Items store — layout, frontmatter and the export contract

One item = one Markdown file with a YAML frontmatter. Stable IDs, N:N
traceability links, statuses, git as the audit log, aggregation into
deliverables by the exporters. This skill is the **source of truth for
what goes where** in an item; the exporters in the CINA-CTP repository
(see `scaffold/tools/README.md`) implement the same contract and refuse
a release export that violates it (skill `submission-readiness`).

## Layout

```
docs/
├── items/
│   ├── MAP/         # upstream / stakeholder requirements, verbatim
│   ├── SRS/         # software requirements        (IEC 62304 §5.2)
│   ├── SDS/         # design and architecture      (IEC 62304 §5.3-§5.4)
│   ├── TC/          # test cases                   (IEC 62304 §5.5/§5.7)
│   ├── RSK/         # safety risks                 (ISO 14971 / 62304 §7)
│   ├── PRSK/        # production / supply-chain risks (ISO 14971, IEC 81001-5-1)
│   ├── THR/         # cyber threats                (IEC 81001-5-1 / STRIDE)
│   ├── USC/         # use scenarios                (IEC 62366-1)
│   └── URSK/        # use-related risks            (IEC 62366-1)
├── ots.yaml                 # OTS / SOUP registry — the only place a third-party component is identified
├── dt-clinical-context.md   # narrative sections inlined into the deliverables (anchors = `## slug`)
├── generated/               # produced by the build — never edited by hand
└── templates/               # item skeletons (`/doc-init`)
```

File name = `<ID>.md`. `dt-config.yaml` at the repository root carries
the document control data (`document.identifier`, `document.version_label`,
`document.date`, `revision_history`, signatures, `id_format`).

## ID format

`<CAT>-<DOMAIN>-<NNN>` by default, or the `id_format` of `dt-config.yaml`
(e.g. `{CAT}-{SUITE}-{APP}-{DOMAIN}-{NNN:03d}`). `CAT` is one of the
directories above, `DOMAIN` is short upper-case, `NNN` is zero-padded.

**IDs are immutable.** To retire an item set `status: Deprecated`. Never
delete, never renumber, never reuse an ID even if its file is gone.

## The two halves of an item

Every item body is split into **normative** sections, which the
exporters render into the deliverable, and **internal** sections, which
never leave the repository. The rule that follows from it:

> Normative sections state the present behaviour, design or assessment
> only. Every date, decision, re-argument, closure note and change note
> goes to `## History`.

| Category | Normative (exported) | Rationale | Internal (never exported) |
|---|---|---|---|
| SRS | `## Description`, `## Acceptance criteria` | — | `## Notes`, `## Open questions`, `## History` |
| SDS | `## Responsibility`, `## Interfaces`, `## Invariants`, `## Design` | `## Design notes` (rendered once, in the SDD rationale appendix, never inline) | `## Notes`, `## Open questions`, `## History` |
| TC | `## Preconditions`, `## Steps`, `## Expected results` | — | `## Notes`, `## Open questions`, `## History` |
| RSK / PRSK | `## Hazard`, `## Initiating causes`, `## Foreseeable sequence of events`, `## Hazardous situation`, `## Harm`, `## Initial risk justification`, `## Risk controls`, `## Residual risk justification` | — | `## Notes`, `## Open questions`, `## History` |
| THR | `## Threat`, `## Threatened asset`, `## Exploitation vector`, `## Level justification`, `## Expected controls`, `## CIA impact analysis` | — | `## Notes`, `## Open questions`, `## History` |
| URSK | `## Use error`, `## Conditions favoring the error`, `## Hazard and harm`, `## Level justification`, `## Expected controls` | — | `## Notes`, `## Open questions`, `## History` |
| USC | `## Persona`, `## Preconditions`, `## Normal usage sequence`, `## Foreseeable use errors` | — | `## Notes`, `## Open questions`, `## History` |
| MAP | `## Description`, `## Source` | — | `## Notes`, `## History` |

Rules per section:

- **`## Acceptance criteria`** is a **numbered list** (`1.`, `2.`), one
  measurable criterion per line, the number and unit stated. Never
  `- [ ]` / `- [x]` — a tick-box reads as a verification status in the
  exported SRS.
- **`## History`** replaces `## Changelog`. Format, newest first:
  `- YYYY-MM-DD vX.Y.Z — <what changed and why>`. Closure notes
  ("re-assessed after …: unchanged"), decisions, and the reasoning behind
  a revised residual argument live here, dated.
- **`## Open questions`** holds what the code does not answer. It feeds
  the open-points register, which is exported only with `--internal`.
- **`## Design notes`** (SDS only) is rationale: alternatives discarded,
  why this design. It is exported once, in an appendix of the SDD, not
  under each item, and it carries no dates (dated reasoning goes to
  History).
- **Markers** `[TODO …]`, `[DRAFT …]`, `[GAP-62304]`, `[GAP-CYBER]`,
  `[GAP-USE]` are allowed only in `## Notes`, `## Open questions` and
  `## History`. A marker in a normative section blocks the release export.
- **Inline commentary** the writer wants to keep next to a normative
  sentence goes in an HTML comment `<!-- … -->`; exporters strip it.
- Each template section starts with a one-line HTML comment saying
  whether the section is exported. Keep those comments in the items.

## Frontmatter — common schema

```yaml
---
id: SRS-AUTH-001                 # required, == file name
title: OAuth2 authentication     # required, 80 characters or fewer
status: Draft                    # Draft | Approved | Deprecated
version: 1.0.0                   # semver — bump on every substantive change
created: 2026-05-07              # ISO 8601, never changed after creation
updated: 2026-05-07              # ISO 8601, set on every modification
reviewed: null                   # last date the item was READ against its source; set by a reviewer, never by a tool
owner: null                      # who owes the open work (workstream, role, person)
target_release: null             # release the open work is owed for, e.g. V1.0.0
source:                          # code / test files that justify the item
  - src/auth/oauth.ts
links:                           # outgoing traces
  parent: []                     # item → item of the same category
  implements: []                 # SDS → SRS; SRS → MAP
  verifies: []                   # TC → SRS
  mitigates: []                  # SRS/SDS/TC → RSK / PRSK / THR / URSK
  triggers: []                   # THR / URSK → RSK
---
```

## SRS — specific keys

```yaml
kind: functional                 # functional | performance | interface | platform | usability | safety | security | process
description: |
  The system shall authenticate a user against the configured identity provider.
verification: Test               # Test | Inspection | Analysis | Demo
priority: Must                   # Must | Should | Could
parameters: []                   # see "Parameters" below
```

`kind` decides which section of the exported SRS the requirement is
rendered in. The exporter builds one section per kind that has at least
one item, so a product without a `performance` requirement has no
performance section — and a reviewer sees that immediately.

| kind | What it states | Example |
|---|---|---|
| `functional` | Behaviour on inputs, outputs produced | "The system shall compute a Tmax map for every accepted study." |
| `performance` | Time, throughput, accuracy or resource bounds, with the number | "The system shall complete processing of a 40-frame study within `max_processing_time` (600 s)." |
| `interface` | Contracts with external systems, formats, protocols | "The system shall export derived series as DICOM Secondary Capture with Modality OT." |
| `platform` | Operating environment: OS, runtime, hardware, OTS constraints | "The system shall run on a host providing at least `min_ram` (16 GiB) of memory." |
| `usability` | Presentation and interaction rules, IEC 62366-1 controls | "The system shall display the lesion side label on every summary plate." |
| `safety` | Risk control measures derived from RSK / PRSK items (`links.mitigates`) | "The system shall reject a study whose frame count is below `min_frames` (8)." |
| `security` | Controls derived from THR items | "The system shall verify the image signature before an update is applied." |
| `process` | Installation, update, decommissioning, record-keeping the software must support | "The system shall write an audit record for every processed study." |

## SDS — specific keys

```yaml
module: auth/oauth
parameters: []                   # same schema as SRS
interfaces:
  inputs:
    - HTTP GET /auth/login
  outputs:
    - Signed JWT
  depends_on:
    - SDS-AUTH-002               # internal module by ID
    - openid-client              # OTS component by its `component` key in docs/ots.yaml
```

A third-party component is named in `depends_on` **by its key in
`docs/ots.yaml`** and nowhere else. Version, supplier and role are read
from the registry, never repeated in prose.

## Parameters — one name, one value

Every frozen constant that an item quotes (a threshold, a series number,
a timeout, a default) is declared once in the `parameters:` list of the
item that owns it:

```yaml
parameters:
  - name: derived_series_number   # snake_case, unique across the whole store
    value: 1301
    unit: null                    # SI unit, or null for a count / enumeration
    settable: false               # true if a site or user can change it at runtime
    interval: null                # allowed range when settable, e.g. "[0.5, 6.0]"; null when fixed
    source: src/export/series.py  # where the constant lives in the code
```

Rules:

1. One `name` = one `value` across the whole store. Two items declaring
   the same name with different values fail the store lint (this is the
   defect that let a series number be 960 in one item and 1301 in
   another).
2. Normative text quotes the number **and** names the parameter:
   "… within `max_processing_time` (600 s)". A bare literal that matches
   no declared parameter is reported by the lint.
3. Another item that needs the same constant declares the same
   `name`/`value` (the lint enforces equality) or refers to it by name in
   prose; it never restates a different literal.
4. `settable: true` requires `interval`.

## Other categories — specific keys

See the templates in `docs/templates/` for RSK, PRSK, THR, URSK, USC and
MAP. Summary:

- **RSK**: `risk_category`, `software_function`, `software_item`,
  `hazard`, `initiating_causes`, `foreseeable_sequence`,
  `hazardous_situation`, `harm`, `severity`, `probability`, `risk_level`,
  `acceptable`, `control_hierarchy`, `residual_*`, `arising_risks`,
  `labeling_disclosure`. Controls are **not** stored on the RSK — they are
  computed from the items whose `links.mitigates` names it.
- **PRSK**: as RSK, with `production_phase` and `asset_at_risk`.
- **THR**: `stride`, `attacker`, `asset`, `likelihood`, `impact`,
  `risk_level`, `acceptable`, `residual_acceptable`, CIA severities,
  `architecture_view` (one of the four cybersecurity views), `links.triggers`.
- **URSK**: `use_scenario`, `use_error`, `hazard`, `hazardous_situation`,
  `harm`, `severity`, `likelihood`, `risk_level`, `acceptable`,
  `residual_acceptable`, `links.triggers`.
- **USC**: `persona`, `environment`, `task`, `frequency`, `criticality`.
- **TC**: `type` (Unit | Integration | System | E2E), `automated`,
  `test_id` (must resolve to a test that exists in the repository),
  `executed_at` (set only by `tools/bind_test_results.py`),
  `preconditions`, `steps`, `expected`, optional `usability_type`.
- **MAP**: `external_id`, `source_document`, `source_section`.

## Links and traceability

All links are **outgoing** and stored in the `links:` block of the
source item. The build computes the incoming side (coverage).

| Link | Direction | Meaning |
|---|---|---|
| `parent` | item → same category | hierarchy / decomposition |
| `implements` | SDS → SRS, SRS → MAP | "this module realises requirement X" / "this requirement realises upstream X" |
| `verifies` | TC → SRS | "this test verifies requirement X" |
| `mitigates` | SRS/SDS/TC → RSK / PRSK / THR / URSK | "this control addresses that risk" |
| `triggers` | THR / URSK → RSK | "this threat or use error triggers that safety hazard" |

## Statuses and versioning

- `Draft` — created or being changed, not reviewed.
- `Approved` — reviewed and signed. Any change bumps `version` (minor at
  least) and returns the item to `Draft`.
- `Deprecated` — kept for history, ignored by the coverage matrix.

`dt-config.yaml: versioning.mode` is `design` before the first release
(every item pinned to `baseline_version`, no History entries beyond
creation) and `maintenance` afterwards (full History discipline).

## What is NOT in an item

- Competitor product names. Comparisons live in `docs/competitors/` or
  the benchmark reports, never in an item.
- Code paths or test paths in **SRS** normative text. `source:` and
  `test_id:` carry them in the frontmatter; the exported SRS says what
  the device does, not where.
- Commit hashes, dates, "as of", "re-assessed on", "since v…" in any
  normative section.
- OTS versions and suppliers in prose (registry only).

## Idempotence rules (for agents)

1. **Read** the item before writing it.
2. If the substance does not change, do not touch the file (preserves
   `updated` and `version`).
3. On a change: set `updated`, bump `version` (patch for rewording, minor
   for a substantive addition, major for a change of meaning), return an
   `Approved` item to `Draft`, and add one line to `## History`.
4. Never rewrite `id` or `created`; never renumber.
5. Never write a date, a decision or a change note into a normative
   section — History only.

## Build

`python tools/build_docs.py` (via `/doc-build`) aggregates the store into
`docs/generated/` (SRS, SDS, STD, traceability, risk analyses, usability
analysis, `_to_implement.md`, `coverage.json`). The customer-facing
deliverables are produced by the reference exporters described in
`scaffold/tools/README.md`, which apply the release gate of
`submission-readiness`.
