---
name: submission-readiness
description: The release gate for exported deliverables — the document-control check and the submission lint that refuse an SRS, SDD, STP, STD, STR or risk report carrying history, markers, dates, hashes, competitor names or code paths. Invoke before any `--release` export, in `compliance-reviewer`, and whenever a deliverable is about to leave the repository.
---

# Submission readiness — release lint and document-control gate

A technical file is read by a reviewer who has never seen the repository.
It must read as a description of the device as released, signed on one
date, with one revision history. The gate below is what separates a
submission-grade export from an engineering journal. The reference
exporters (`tools/build_*_export.py` in the CINA-CTP repository, shared
helpers in `tools/_lib.py`) implement it; this skill states the rules so
that writers produce items that pass it and reviewers know what to check.

## Three export modes

| Flag | Cover | Open points | Gate |
|---|---|---|---|
| (none) | `WORKING DRAFT — generated <today>` | omitted | lint reported, never blocking |
| `--internal` | `WORKING DRAFT — generated <today>` | appended as a register (from `## Open questions` and `[TODO`/`[GAP-` markers) | lint reported, never blocking |
| `--release` | document identifier, `document.version_label`, `document.date`, signatures from `dt-config.yaml` | never | **every rule below must pass or the export is refused** |

`--release` and `--internal` are mutually exclusive. `/doc-build --release`
runs the gate before calling any exporter and stops at the first offender
list.

## Document-control gate (DC)

Read from `dt-config.yaml`:

- **DC-1** For every exported item (status ≠ Deprecated in the
  deliverable's categories), `updated` ≤ `document.date` and, when set,
  `reviewed` ≤ `document.date`. An item changed after the signature date
  cannot be in the signed document. Fix: bump `document.version_label`
  and `document.date`, and add the row to `revision_history`.
- **DC-2** `revision_history` contains an entry whose `version` equals
  `document.version_label`, with a `date` equal to `document.date` and a
  non-empty `reason`.
- **DC-3** `revision_history` dates are strictly increasing and the last
  one is `document.date`.
- **DC-4** No exported item is `status: Draft` when
  `versioning.mode: maintenance`. (In `design` mode all items are Draft
  by construction and DC-4 is skipped.)

## Text lint (TL) — applied to the exported text after internal sections and HTML comments are stripped

- **TL-1 markers** — no `[TODO`, `[DRAFT`, `[GAP-` anywhere in exported
  text (normative sections, titles, frontmatter fields that are
  rendered, narrative anchors of `dt-clinical-context.md`).
- **TL-2 dates** — no ISO date (`\d{4}-\d{2}-\d{2}`), no "as of", "re-assessed
  on", "since v", "on <Month> <year>" in exported text. Dates belong to
  `## History` and to the document control block.
- **TL-3 commit hashes** — no token matching `\b[0-9a-f]{7,40}\b` that is
  not a declared parameter value.
- **TL-4 competitor names** — none of the terms listed in
  `dt-config.yaml: lint.forbidden_terms` (the product's competitor list,
  case-insensitive, word-bounded) appears in exported text.
- **TL-5 code and test paths (SRS)** — SRS normative text contains no
  path-like token (`src/…`, `tests/…`, `*.py`, `*.ts`, `*.yaml`,
  `::test_`). `source:` and `test_id:` are the only carriers. The rule
  is relaxed for SDS (`module:` and interfaces may cite paths) and STD.
- **TL-6 tick-boxes** — no `- [ ]` or `- [x]` in exported text.
  Acceptance criteria are numbered lists.
- **TL-7 internal sections** — `## Notes`, `## Open questions`,
  `## History` (and any legacy `## Changelog`) are never rendered. `##
  Design notes` is rendered once, in the SDD rationale appendix, not per
  item. An item body that still contains a `## Changelog` header fails.
- **TL-8 HTML comments** — stripped before rendering and before the
  other TL rules run.
- **TL-9 duplicate rendering** — each item is rendered exactly once in
  its deliverable (the SDD used to render each item three times).
- **TL-10 open points** — the open-points register is never appended
  without `--internal`.

## Store lint (SL) — applied to `docs/items/**` and the registries

- **SL-1 parameters** — one `name` = one `value` across the store; a
  `settable: true` parameter has an `interval`; a bare numeric literal
  in SRS normative text that equals no declared parameter value is
  reported (warning without `--release`, error with it).
- **SL-2 kinds** — every SRS has `kind` in the allowed set.
- **SL-3 OTS** — every `interfaces.depends_on` entry that is not an item
  ID is a `component` key of `docs/ots.yaml`; every registry entry has
  the ten fields filled (`component`, `version`, `supplier`, `role`,
  `safety_relevant`, `functions_used`, `hazard_review`, `verification`,
  `eol_status`, `sbom_ref`); no OTS version or supplier appears in item
  prose.
- **SL-4 test ids** — every TC `test_id` resolves to a test node that
  exists in the repository; a TC whose `steps` say "planned" or whose
  `test_id` is `[TODO]` is not counted as verification coverage.
- **SL-5 links** — no link to a missing or Deprecated item; `id` equals
  the file name.
- **SL-6 clinical-context anchors** — `docs/dt-clinical-context.md`
  contains the required `## <anchor>` sections with non-placeholder
  content for the deliverable being exported. For the SDD:
  `general-system-architecture`, `run-states`, `architecture-rationale`,
  `security-global-view`, `security-multi-patient-view`,
  `security-updateability-view`, `security-use-case-views`.
- **SL-7 class A severities** — no RSK / URSK with `severity: Critical`
  or `Catastrophic`; no risk item with `residual_acceptable: false`; no
  risk item `acceptable: false` without a control (the historical
  `--strict` rules of `build_docs.py`).

## How to run it

```bash
# Store lint first (SL-5, SL-7, markers anywhere in the store)
python tools/build_docs.py --strict

# The gate itself is the release export: DC + TL + SL run before any file is
# written, and a failure leaves no deliverable behind. `--md-only` skips the
# .docx rendering when only the verdict is wanted.
python tools/build_srs_export.py --release --md-only

# Release exports — each refuses on its own offenders
python tools/build_srs_export.py --release
python tools/build_sdd_export.py --release
python tools/build_stp_export.py --release
python tools/build_stdr_export.py --release
python tools/build_str_export.py --release
python tools/build_risk_export.py --release

# Internal review copy with the open-points register
python tools/build_srs_export.py --internal
python tools/build_open_points.py                  # standalone register
python tools/build_rationale.py                    # standalone SDD rationale appendix
```

The exporters print offenders grouped by rule, one line per offender:
`<rule> <item or anchor> L<line>: <excerpt>`. The `compliance-reviewer`
copies that list to the top of `99_compliance_review.md`, offenders
first, before any coverage metric.

When the exporters are not present in the repository (a project
scaffolded by `/doc-init` before syncing them), the reviewer applies the
rules by hand with `grep` over `docs/items/**` and reports the same
format; the release export is then **not** claimed to be clean.

## Writer-side checklist (before handing an item over)

1. Normative sections describe the present behaviour or assessment;
   nothing dated, no "we decided", no "re-assessed".
2. Acceptance criteria numbered, each with its number and unit, each
   traceable to a test.
3. Every constant quoted appears in `parameters:` with one value.
4. No competitor name, no code or test path in SRS text.
5. Third-party components referenced by their `docs/ots.yaml` key.
6. Markers only in `## Notes`, `## Open questions`, `## History`.
7. `updated` set; one `## History` line added.
