# tools/ — what is scaffolded here, and what is not

`/doc-init` copies **one** script into this folder:

| File | Role | Deliverable? |
|---|---|---|
| `build_docs.py` | working build: aggregates `docs/items/**` into `docs/generated/` (SRS, SDS, STD, traceability, risk / cyber / usability analyses, `_to_implement.md`, `coverage.json`); `--strict` fails on open markers, class A severities and unaccepted residuals | **No.** `docs/generated/` is an engineering view for the writers and the reviewer. |

`build_docs.py` is a stdlib-only snapshot kept deliberately simple. It is
**older than the reference copy** and knows nothing of the release gate:
it does not strip `## History`, does not check `parameters:`, `kind:`,
`docs/ots.yaml` or the clinical-context anchors, and its `--strict`
counts a `[TODO]` in `## Open questions` as an offender (a release
refuses open questions anyway). It reads `SRS SDS TC RSK THR USC URSK`
only — `PRSK` and `MAP` items are ignored by the working build and
appear in the release exports only.

## The reference exporters live in the CINA-CTP repository

The customer-facing deliverables are produced by exporters that are
**not part of this plugin**. They are maintained in the CINA-CTP
repository (`tools/`) and must be synced from there — never edited in a
target project, never copied into the plugin:

| Script | Produces |
|---|---|
| `_lib.py` | shared helpers: frontmatter parser, `strip_internal_sections`, HTML-comment stripping, document-control and lint checks, Mermaid → figure rendering for pandoc |
| `build_srs_export.py` | Software Requirements Specification (one section per `kind`, parameters appendix) |
| `build_sdd_export.py` | Software Design Description (modules rendered once, OTS table from `docs/ots.yaml`, the six narrative sections, rationale appendix) |
| `build_stp_export.py`, `build_stdr_export.py`, `build_str_export.py` | Software Test Plan / Description / Report |
| `build_risk_export.py` | risk analysis (Design / Production / Usability tabs, cyber threats, `.xlsx`) |
| `build_open_points.py` | the open-points register (`## Open questions` + markers) — `--internal` only |
| `build_rationale.py` | the SDD rationale appendix from the `## Design notes` sections |
| `bind_test_results.py` | binds a junit report to the TC items (`status`, `executed_at`) for the STR |

Sync: copy the scripts above from the CINA-CTP repository at the commit
you want to pin, and record that commit in your `dt-config.yaml`
(`exporters.synced_from`) or the project changelog. When the plugin's
skills and the exporters disagree, the exporters are the executable
truth and the skill is corrected.

## The contract the exporters implement

Stated in the skills `items-store` and `submission-readiness`; restated
here so a reader of `tools/` finds it:

1. **Sections.** Normative sections are rendered: SRS `## Description`,
   `## Acceptance criteria`; SDS `## Responsibility`, `## Interfaces`,
   `## Invariants`, `## Design`; TC `## Preconditions`, `## Steps`,
   `## Expected results`; the standard RSK / PRSK / THR / URSK / USC
   sections. `## Notes`, `## Open questions`, `## History` (and any
   legacy `## Changelog`) are never rendered. `## Design notes` is
   rendered once, in the SDD rationale appendix. HTML comments
   `<!-- … -->` are stripped before anything else.
2. **Frontmatter.** SRS `kind:` ∈ functional | performance | interface |
   platform | usability | safety | security | process — one exported
   section per kind in use. `parameters:` (`name`, `value`, `unit`,
   `settable`, `interval`, `source`) on SRS and SDS: one name = one
   value across the store. TC `test_id` must resolve to a test that
   exists; planned TC are never counted as coverage.
3. **Modes.** No flag → cover `WORKING DRAFT — generated <date>`, no
   open points. `--internal` → same cover plus the open-points register.
   `--release` → signed cover from `dt-config.yaml`, and the export is
   **refused** when any exported item's `updated` / `reviewed` postdates
   `document.date`, when `revision_history` lacks
   `document.version_label` at `document.date`, or when exported text
   carries `[TODO`, `[DRAFT`, `[GAP-`, an ISO date, a commit hash, a
   term of `lint.forbidden_terms` (competitor names), a tick-box, or —
   in the SRS — a code or test path.
4. **Registries.** Third-party components are identified in
   `docs/ots.yaml` only (`component`, `version`, `supplier`, `role`,
   `safety_relevant`, `functions_used`, `hazard_review`, `verification`,
   `eol_status`, `sbom_ref`). The SDD requires the six narrative anchors
   of `docs/dt-clinical-context.md`: `general-system-architecture`,
   `run-states`, `architecture-rationale`, `security-global-view`,
   `security-multi-patient-view`, `security-updateability-view`,
   `security-use-case-views`.
5. **Rendering.** Each item is rendered exactly once in its deliverable.
   The open-points register is never an appendix of a deliverable
   outside `--internal`.

`/doc-build --release` runs the gate and refuses to call an exporter
when the store is not clean; the `compliance-reviewer` reports the
offenders first. Without the exporters in `tools/`, `/doc-build
--release` states that no deliverable can be produced.
