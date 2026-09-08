---
name: items-store
description: Local item-per-file store for technical-file items (requirements, design, tests, risks, threats, use scenarios) — the offline equivalent of Matrix Requirements — and the section/frontmatter contract that separates normative, exported text from internal working notes. Invoke before creating, reading or updating any documentation item.
---

## OUTPUT LANGUAGE — STRICT

Any item created or updated under `docs/items/` (frontmatter values,
body sections, `[TODO]` markers) MUST be written in **English**,
regardless of the user's conversational language or any global
`CLAUDE.md` instruction.

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
| SRS | `## Description`, `## Acceptance criteria` — each requirement is rendered as a heading of its own | — | `## Notes`, `## Open questions`, `## History` |
| SDS | `## Responsibility`, `## Interfaces`, `## Invariants`, `## Design` (the normative detailed design) | `## Design notes` (alternatives and reasons only; rendered once, in the SDD rationale appendix, never inline) | `## Notes`, `## Open questions`, `## History` |
| TC | `## Preconditions`, `## Steps` (a procedure), `## Expected results` (one clause per test function) | — | `## Notes`, `## Open questions`, `## History` |
| RSK / PRSK | `## Hazard`, `## Initiating causes`, `## Foreseeable sequence of events`, `## Hazardous situation`, `## Harm`, `## Initial risk justification`, `## Risk controls`, `## Residual risk justification` — the last two are rendered per record in the RAR | — | `## Notes`, `## Open questions`, `## History` |
| THR | `## Threat description`, `## Attack path and preconditions`, `## Level justification`, `## Controls` (SRS/SDS ids — a TC id is verification, never a control), `## Residual` (level + acceptance condition), `## CIA impact analysis` | — | `## Notes`, `## Open questions`, `## History` |
| URSK | `## Use error`, `## Conditions favoring the error`, `## Hazard and harm`, `## Level justification`, `## Expected controls` | — | `## Notes`, `## Open questions`, `## History` |
| USC | `## Persona`, `## Preconditions`, `## Normal usage sequence`, `## Foreseeable use errors` | — | `## Notes`, `## Open questions`, `## History` |
| MAP | `## Description`, `## Source` | — | `## Notes`, `## History` |

Rules per section:

- **`## Acceptance criteria`** is a **numbered list** (`1.`, `2.`), one
  measurable **behaviour** per line, the number and unit stated. Never
  `- [ ]` / `- [x]` — a tick-box reads as a verification status in the
  exported SRS. A criterion is never a status ("confirmed by RAQA"), a
  test id ("TC-AIF-013 stays an expected failure"), a decision id, a
  "placeholder until …", or a statement about the source code. A
  tolerance is a number taken from the test that asserts it ("within
  `aif_offset_tol` (2 voxels)"), never "about", "small margin", "~85 %".
  A **measurement** ("peak RSS 20.6 GB on the 40-frame study") is
  evidence and goes to `## Notes`; the **bound** ("peak RSS at most
  `max_rss` (24 GB)") is the criterion.
- **Terminology.** One glossary term per concept (the `## glossary`
  anchor of `docs/dt-clinical-context.md`), used verbatim in every
  requirement, in the labeling and in the report strings; when the
  labeling and an item disagree, the labeling vocabulary wins. "Tmax > 6 s
  region" is not also "hypoperfusion region", "high-Tmax region" and
  "critically hypoperfused region".
- **Link stripping.** When a commit hash, an issue number or a competitor
  reference is removed from a normative sentence, the whole
  parenthetical or clause goes with it — never leave "(open issue" or
  "measured in issue;" behind.
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
references: []                   # ids of `dt-config.yaml: references` entries this item cites (SRS, SDS)
links:                           # outgoing traces
  parent: []                     # item → item of the same category
  implements: []                 # SDS → SRS; SRS → MAP
  verifies: []                   # TC → SRS
  mitigates: []                  # SRS/SDS/TC → RSK / PRSK / THR / URSK
  triggers: []                   # THR / URSK → RSK
---
```

`references:` names the literature and standards the item relies on, by
the `id` of an entry of `dt-config.yaml: references`
(`references: [{id, citation}]`). **Every clinical threshold and every
algorithm names its source** — a DEFUSE-3 cut, an oSVD deconvolution, a
published oxygen-transport model each carry an id, quoted in the text as
`[DEFUSE3]`. The exporters render one References section per
deliverable from the ids in use; an id no entry defines, or an entry no
item uses, is a lint finding (SL-9).

Exports carry **no per-item `version`** — the deliverable has one
version label (`document.version_label`); the kind sections of the SRS
list `id` + `title` only, never a summary derived from the first
sentence (the summary diverges from the body).

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

Optional keys written by the `mitigation-auditor` (skill
`mitigation-audit`) on a control SRS, additive and absent until an audit
runs — the audit treats a missing value as `unknown`:

```yaml
implementation_status: unknown    # absent | partial | implemented | unknown
implementation_evidence: []       # list of {path: src/foo.py:42, note: "…"}
implementation_gap: null          # what is missing when partial, else null
```

They are internal metadata: never rendered in an export.

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
  - name: derived_series_number   # snake_case, unique across the whole store — ONE owner
    value: 1301                   # a list value is a YAML list: value: [4, 6, 8, 10]
    unit: null                    # SI unit, or null for a count / enumeration
    settable: false               # true if a site or user can change it at runtime
    interval: null                # allowed range when settable, e.g. "[0.5, 6.0]"; null when fixed
    source: package.export.series.SERIES_NUMBER  # prose or a dotted symbol — never a file path
```

Rules:

1. One `name` = one `value` across the whole store. Two items declaring
   the same name with different values fail the store lint (this is the
   defect that let a series number be 960 in one item and 1301 in
   another).
2. Normative text quotes the number **and** names the parameter:
   "… within `max_processing_time` (600 s)". A bare literal that matches
   no declared parameter is reported by the lint.
3. **One owner per name.** The item that owns the constant declares it
   and **describes it in its own text** — a frozen parameter that no
   requirement describes is a registry row without a specification
   ("arterial_lead_s frozen but described in no requirement"). Another
   item that needs the constant refers to it by name in prose; it never
   redeclares it, with the same value or another.
4. `settable: true` requires `interval`.
5. `source` is **prose** ("configuration schema", "DICOM standard PS3.3")
   or a **dotted symbol** (`ctperfusion.common.config.MIN_FRAMES`) —
   never a path. The registry is rendered in **SRS §4.1** and **SDD
   §3.8** (one table: SRS and SDS parameters joined), where a path is
   a code reference in a customer document; the lint refuses paths and
   duplicate names (SL-8).
6. A list value is written as a YAML list (`[4, 6, 8, 10]`), never as a
   string that the table truncates to its first element.
7. Two names for one constant (`min_slice_visits` and
   `dynamic_min_visits_per_location`) are a duplicate: keep the one the
   glossary uses, reference it from the other item.

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
  `risk_level`, `acceptable`, `residual_risk_level`,
  `residual_acceptable`, the CIA triad (`confidentiality_severity`,
  `integrity_severity`, `availability_severity` and their `residual_*`
  counterparts, each `n/a | Low | Medium | High`; `impact` equals their
  maximum — skill `cyber-risk-analysis`), `architecture_view` (one of
  the four cybersecurity views), `links.triggers`.
- **URSK**: `use_scenario`, `use_error`, `hazard`, `hazardous_situation`,
  `harm`, `severity`, `likelihood`, `risk_level`, `acceptable`,
  `residual_acceptable`, `links.triggers`.
- **USC**: `persona`, `environment`, `task`, `frequency`, `criticality`.
- **TC**: `type` (Unit | Integration | System | E2E), `automated`,
  `test_id` (must resolve to a test that exists in the repository),
  `executed_at` (set only by `tools/bind_test_results.py`),
  `preconditions`, `steps` (a procedure: fixture, action, observation),
  `expected` (one clause per test function of `test_id`), optional
  `usability_type`. `status` is `Unknown` until the binder sets it from
  the run status (`passed | passed_with_skips | passed_with_xfail |
  failed | skipped | not_run | manual_passed | manual_failed`, item
  labels `Passed`, `PassedWithSkips`, `PassedWithXfail`, `Failed`,
  `Skipped`, `Unknown`) — a case with a pytest-level skip or an xfail
  inside is never `Passed`.
- **MAP**: `external_id`, `source_document`, `source_section`.

## The statement of an SRS requirement — altitude and shape

`## Description` says **what** the software does, never **how**: indicative
present, one paragraph (two at most) of 30 to 80 words, no `shall`, no list, no
constant other than a declared clinical value. The method goes to the
`## Design notes` of the SDS item that `implements:` the requirement; the
rationale to `## Notes`. The `description:` frontmatter carries the paragraph
verbatim. `## Acceptance criteria`: a numbered list of at most 8 one-line
criteria, each an observable outcome. The `altitude` lint of the SRS export
refuses the rest. Detailed rule, worked example and the substitution/change
tests: agent `requirements-writer`, section "Altitude".

The **context of a functional area** (clinical, technical, the literature cited
as `[Rn]`) is written once, by hand, in `docs/srs-domain-introductions.md` —
one `## <DOMAIN>` section per code of `domain_order` — and the SRS export
places it under the area heading (§2.2.k), before its requirements. That file
is not an item: no requirement, no method, no code path in it.

## Links and traceability

All links are **outgoing** and stored in the `links:` block of the
source item. The build computes the incoming side (coverage).

| Link | Direction | Meaning |
|---|---|---|
| `parent` | item → same category | hierarchy / decomposition |
| `implements` | SDS → SRS, SRS → MAP | "this module realises requirement X" / "this requirement realises upstream X" — the SRS → MAP form is what the §3 traceability table of the exported SRS renders; `links.parent: [MAP-…]` is the legacy form the scaffolded working-draft exporter still reads and is accepted, never required |
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
- A person, a host or a machine name ("confirm with Cyril", "on
  choupinette"), an issue number, an internal ruling id ("ruling H35")
  in a normative section.
- In a risk item, the state **before** the controls ("nothing is
  hash-pinned yet", "currently contains PLACEHOLDER") presented as the
  hazard: the hazard is the source of harm in the released software.
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

## Two lists that are not the same

- The **open-points register** (`## Open questions`, `[TODO`/`[GAP-`
  markers) is internal; it is exported only with `--internal`.
- The **unresolved anomalies appendix** (Enhanced documentation level)
  is exported in every deliverable (SDD Appendix C, STR). It is built by
  the exporters from the known-defects register (the `KNOWN_DEFECTS`
  literal of `tests/test_known_defects.py`), every TC bound
  `passed_with_xfail`, `skipped` or `passed_with_skips`, every risk item
  with `residual_acceptable: false`, and the open-actions section of the
  decision record named in `dt-config.yaml: anomalies.open_actions_record`
  / `open_actions_section` — one row each: id, description, owner, target
  release, risk link. Nothing is written into it by hand; it is the only
  exported text allowed to carry dates.

## Mode versioning : design vs maintenance

`dt-config.yaml` peut porter un bloc `versioning` qui pilote le comportement
des agents :

```yaml
versioning:
  mode: design            # design | maintenance (défaut : maintenance)
  baseline_version: "1.0.0"
```

- **`maintenance`** (défaut, comportement historique) : les règles
  d'idempotence ci-dessus s'appliquent — bump de `version`, `## Changelog`,
  `Approved` → `Draft`. C'est le mode après la première release, où chaque
  évolution doit laisser une trace versionnée.

- **`design`** : tant qu'aucune première version n'est sortie, l'objectif est
  une **baseline unique et clean**, pas un historique de patchs. Les agents :
  1. écrivent **toujours** `version: <baseline_version>` (jamais de bump) ;
  2. n'ajoutent **jamais** de section `## Changelog` (il n'y a rien à
     « changer » avant la V1) ;
  3. ne repassent pas d'`Approved` à `Draft` sur reformulation (tout reste
     `Draft` en phase design) ;
  4. mettent quand même `updated` à jour à la date courante.

  La réinitialisation d'une baseline existante vers cet état est faite par
  `tools/normalize_baseline.py` (idempotent) — voir /doc-build.

## Build

`python tools/build_docs.py` (via `/doc-build`) aggregates the store into
`docs/generated/` (SRS, SDS, STD, traceability, risk analyses, usability
analysis, `_to_implement.md`, `coverage.json`). The customer-facing
deliverables are produced by the reference exporters described in
`scaffold/tools/README.md`, which apply the release gate of
`submission-readiness`.

## Register of the exported text

Exported sections and exported frontmatter fields are controlled-document
text: declarative, present tense, stating the released software and the
controls in force. Evaluative clauses, descriptions of the pre-control
state, dramatised consequences and person or host names are refused by
the release lint (kind `register`, classes `editorial`, `pre-control`,
`rhetoric`, `name`) and belong in `## History` / `## Notes`. An open
condition is stated once, in the residual section, as condition + owner
+ target release. The rule changes wording, never a fact, a rating or an
acceptance decision — see `agents/risk-analyst.md`, "Register".

## Scope of the technical documentation: the released device only

The technical file describes the device that is released. A sentence earns its
place if it states a property of that device, narrows the claim ("the thresholds
are not user-selectable"), or answers a feature the predicate has. A sentence
whose subject is something the release does not contain — a configuration nobody
may deploy, a build target nobody receives, a tree that is never packaged, a
product identity that was dropped — narrates an absence: it enlarges the file,
invites a question no reader needs to ask, and protects nobody. The release lint
refuses it (kind `scope`).

Two things survive the rule. A **control** of the released device is named by
what it does, never by the release status of what it acts on: write "the
configuration boundary refuses every series name outside the declared set", not
"the research maps are gated off". A **component that ships inside the image**
may be named for what it is — 62304 asks for the architecture of the item as
built — but never for its release status or its identity as another product.

## Research features are not in the technical documentation

A research feature — an arm of the code base that no released configuration
reaches, a build target that is not a device, an experimental output — is out of
the file entirely:

- it gets **no requirement, no design item, no test case and no risk record** of
  its own in the exported documentation. If such records exist from an earlier
  scope, retire them (`status: Retired` + `retired_reason`); a retired record
  keeps its history in the store and is exported nowhere;
- **no active item names one**, in its text or in its links: a traceability
  column that cites a retired record re-imports into the file exactly what
  retiring it removed;
- the **risk file** does not carry its hazards. A function that is not in the
  device has no hazards of the device;
- if the code of that feature ships inside the released image, the design
  description says what the component is and what gate keeps it inert — that is
  a statement about the released image, not about the research feature;
- keep the research assets **outside the release tree** (their own directory,
  their own profile, refused by the release build), so the documentation and the
  build agree.

Do not spend a rewrite pass on retired research records: they are not exported,
so their register and their altitude do not matter. Leave them as the historical
record they are.
