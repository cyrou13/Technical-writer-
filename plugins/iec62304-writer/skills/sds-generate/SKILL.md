---
name: sds-generate
description: Generate Software Design Specification and architecture items (IEC 62304 §5.3-§5.4) from a TS/JS + Python codebase — module items with Design vs Design notes, the OTS registry, and the six required narrative sections of dt-clinical-context.md including the four cybersecurity architecture views. Invoke to produce items in docs/items/SDS/.
---

# SDS — extracting design and architecture

## Modules to identify

In **multi-repo** mode (codemap mode = `multi-repo`), treat each
component separately and prefix `source:` / `module:` with the component
name (`front/src/auth`, `back/api/routes`).

- **TypeScript / JavaScript** — workspaces / packages, first-level folders
  under `src/`, modules published through an `index.ts`, Nest/Next
  feature folders.
- **Python** — top-level packages (`__init__.py`), layers if present
  (`domain/`, `application/`, `infrastructure/`, `interfaces/`).

One SDS item = **one module with one responsibility**. If
`## Responsibility` needs "and … and …", split.

## Body of an SDS item — Design vs Design notes

```markdown
<!-- Exported. -->
## Responsibility
<1–3 sentences>

<!-- Exported. -->
## Interfaces
### Inputs
### Outputs
### Dependencies
- SDS-<ID> for internal modules; `docs/ots.yaml` key for third-party components

<!-- Exported. -->
## Invariants
- <constraints the module maintains>

<!-- Exported. The design AS BUILT: data flow, algorithm, states, error handling. Present tense. -->
## Design
<what the module does and how, today>

<!-- Rationale — rendered once in the SDD appendix, never inline. No dates. -->
## Design notes
<alternatives discarded, why this design, known limits of the approach>

<!-- Internal. -->
## Notes
## Open questions
## History
```

The line between the two: **`## Design` says what the design is;
`## Design notes` says why.** "The deconvolution uses oSVD with a fixed
oscillation index" is Design. "Standard SVD was rejected because the
oscillation index drifts with noise" is Design notes. "Changed from
sSVD to oSVD after the noise sweep" is History, dated.

## Parameters

An SDS quoting a constant (a regularisation floor, a buffer size, a
default) declares it in `parameters:` exactly as an SRS does (skill
`items-store`). If the SRS already declares the name, reuse the name and
the value; never restate a different literal.

## OTS / SOUP registry — `docs/ots.yaml`

Third-party components are **identified in the registry, not in prose**.
One entry per component:

```yaml
components:
  - component: numpy            # key used in interfaces.depends_on
    version: "1.26.4"
    supplier: NumPy developers
    role: array arithmetic for all map computations
    safety_relevant: true       # does a failure of this component reach a clinical output?
    functions_used:
      - numpy.linalg.svd
      - numpy.fft
    hazard_review: RSK-CTP-OTS-001   # RSK item reviewing the failure modes, or "none — not safety relevant"
    verification: TC-CTP-OTS-001     # TC (or suite) that exercises the functions_used
    eol_status: supported            # supported | maintenance | end-of-life | unknown
    sbom_ref: sbom/cyclonedx.json#numpy
```

The architecture-writer creates or updates the registry from the
dependency manifests; the security-analyst reads it for supply-chain
threats; the exporter renders the registry as the SDD's SOUP table. A
version or supplier written in an item body fails SL-3.

## Architecture views — `SDS-ARCH-*` items

- `SDS-ARCH-001` logical view (components ↔ responsibilities),
- `SDS-ARCH-002` deployment view (if Dockerfile / compose / k8s /
  serverless detected),
- `SDS-ARCH-003` data view (if a persistence layer exists).

Mermaid diagrams in `## Design` when they carry more than three nodes.

## Narrative sections — `docs/dt-clinical-context.md`

The exporters inline `## <anchor>` sections of this file into the
deliverables. The SDD **requires** the six below with real content (SL-6);
`/doc-init` scaffolds them as empty headed sections and the
architecture-writer fills them.

| Anchor | Content |
|---|---|
| `general-system-architecture` | the component diagram and one paragraph per component |
| `run-states` | the state machine of the software: idle, receiving, processing, exporting, error, maintenance; entry and exit conditions; what is observable in each state |
| `architecture-rationale` | why the architecture is what it is — the module-level `## Design notes` roll up here; no dates |
| `security-global-view` | FDA 2023 premarket cybersecurity guidance, global system view: every network interface, port, protocol, trust boundary, authentication point, data store and its protection at rest and in transit, on one diagram |
| `security-multi-patient-view` | how data of one patient is isolated from another across the same instance: session scope, storage separation, identifiers, cleanup |
| `security-updateability-view` | how software and OTS updates are delivered, authenticated (signature), applied, rolled back; who can trigger an update; what the device does during one |
| `security-use-case-views` | one view per security-relevant use case (ingest a study, export results, administer, update), each showing the actors, the data crossing a boundary and the control that protects it |

Each THR item names the view it is drawn on in `architecture_view:`.

## Dependencies

`interfaces.depends_on` lists internal modules by SDS ID and OTS
components by their registry key. Nothing else — no version, no URL.

## Linking to SRS

For every SDS item fill `links.implements:` with the SRS IDs whose
`source:` files fall inside the module. A module implementing no SRS gets
a `[GAP-62304]` line in `## Open questions` (never in a normative
section): either the SRS is missing or the module is dead.

## Anti-patterns

- Describing code line by line — describe interfaces and invariants.
- Duplicating the SRS — SDS says *how*, SRS says *what*.
- "Utility module" with no responsibility — extract one or flag it.
- Naming a competitor or a code path as the subject of a sentence in
  `## Design`.
- A dated sentence anywhere but `## History`.
