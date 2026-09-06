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
  without `--internal`. The **unresolved anomalies** appendix is a
  different list and is exported in every mode (see SL-12).
- **TL-11 criteria are behaviour** — an `## Acceptance criteria` line or
  a TC `## Expected results` line that carries a status word
  ("confirmed", "recorded", "expected failure", "placeholder until"),
  a TC / SDS / decision id as its subject, a person's name, or an
  unquantified tolerance ("about", "roughly", "small margin", "~") is
  an offender. A measurement is Notes; a bound is a criterion.
- **TL-12 dangling clause** — an unbalanced parenthesis or a clause
  ending in "issue", "commit", "see" with nothing after it (the trace of
  a stripped hash / issue / competitor reference) is an offender: the
  whole parenthetical goes.
- **TL-13 terminology** — a concept named by more than one term across
  the exported SRS, the labeling anchors (`intended-use`,
  `warnings-and-precautions`) and the report strings is reported
  (warning); the glossary term wins, the labeling vocabulary first.
- **TL-14 exporter rendering** — no per-item `version` in an export (the
  document version label is the only version); each requirement is a
  heading with one attribute row; kind sections list id, title and
  attributes only — never a summary derived from the first sentence;
  each deliverable carries its own `documents.<x>` identifier and its
  own title; headings left empty by section stripping are removed. The
  anomalies appendix is a dated record and the only exported text
  exempt from TL-2.

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
- **SL-7 class severities** — in class A no RSK / URSK with
  `severity: Critical` or `Catastrophic`; in any class no risk item with
  `residual_acceptable: false` unless it is listed in the anomalies
  appendix with an owner; no risk item `acceptable: false` without a
  control (the historical `--strict` rules of `build_docs.py`).
- **SL-8 parameter registry** — `parameters[].source` is not a path
  (no `/`, no `.py`/`.ts`/`.yaml` suffix); one owner per name (a second
  declaration is an error even with the same value); a list value is a
  list; every frozen parameter is described in the text of the item
  that owns it (the name appears in its `## Description` or criteria).
- **SL-9 references** — every id in an item's `references:` resolves to
  `dt-config.yaml: references[].id`; every SRS whose text quotes a
  clinical threshold or names an algorithm carries at least one id
  (warning); every entry is used by at least one item (warning).
- **SL-10 document identifiers** — `documents: {srs, sdd, rar, stp,
  stdr, str}` are all set, no two equal, none `[TODO]`, `srs` equals
  `document.identifier`; every `project_references` entry that names
  one of them carries the same identifier; the export takes its own
  identifier from `documents.<x>` and its title from `document.title`
  with the document type substituted.
- **SL-11 risk scales** — `classification.severity_definitions` and
  `probability_definitions` define every level used by a risk item with
  a harm-based sentence, not a number; a residual accepted with an
  unchanged index (`residual_severity == severity` and
  `residual_probability == probability`) has a non-empty `## Residual
  risk justification`; `control_hierarchy: information_for_safety`
  with no other mitigating item does not lower the residual index; one
  risk matrix, applied identically to every THR.
- **SL-12 OTS rows** — one row per installed component at an exact
  version (no range pin, no duplicate name); `supersedes` filled when
  two package managers carry the name; `functions_used` non-empty for
  every `safety_relevant: true` row and each symbol importable from the
  device code; `hazard_review` / `verification` of a
  `safety_relevant: false` row state the reason after the dash; the
  base image is one entry; no second inventory in item prose or in a
  clinical-context anchor.
- **SL-13 THR sections and views** — every THR carries `## Threat
  description`, `## Attack path and preconditions`, `## Controls` with
  at least one SRS/SDS id and no TC id, `## Residual` with a level
  and a condition; the four `security-*` anchors are non-empty.
- **SL-14 test evidence** — every TC `steps` has at least two entries
  and none is "run pytest"; `expected` has one clause per test
  function of `test_id`; a TC bound `passed_with_skips` /
  `passed_with_xfail` / `skipped` appears in the anomalies appendix; a
  test that runs a benchmark or release gate is its own TC.

## Decision findings (DEC) — reported, never fixed by a tool or a writer

- **DEC-1 labeling vs specification** — a warning in
  `warnings-and-precautions` that names an output the SRS forbids, or an
  `intended-use` that omits the indication the thresholds encode (a
  stroke cut with no stroke indication), is a contradiction between
  approved labeling and the specification. The `compliance-reviewer`
  reports it at **DECISION** level for the product owner / RAQA at the
  top of its report; nobody edits the labeling anchors to make it go
  away.
- **DEC-2 undeclared configuration** — a configuration named in the
  labeling (a second deployment form, a Python API) that no requirement
  specifies is reported the same way.

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
`<rule> <item or anchor> L<line>: <excerpt>`. Each export also renders,
from `dt-config.yaml`, its own identifier (`documents.<x>`) and title,
the References section (`references`), the unresolved anomalies
appendix (`tests/test_known_defects.py: KNOWN_DEFECTS` + TC bound with a
skip or an xfail + `residual_acceptable: false` items + the open actions
of `anomalies.open_actions_record`), and — in the STDR and STR — the
run metadata of the bound run (`test_results_path`): software version
and its source, release-evidence mode, host, platform, branch, dirty
flag, Python / pytest / numpy versions, run start. The `compliance-reviewer`
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
8. `parameters[].source` is prose or a dotted symbol; each constant has
   one owner and is described in the owner's text.
9. `references:` names the source of every clinical threshold and every
   algorithm.
10. Criteria are behaviour with a number — no status, test id, decision
    id, placeholder; measurements in Notes.
11. One glossary term per concept, the labeling's term.
12. A risk item: hazard as released, controls one line each with tier,
    residual argument present even when the index is unchanged.
13. A THR: description, attack path and preconditions, controls as
    SRS ids, residual level with its condition.
14. A TC: steps a reader can re-execute, one expected clause per test
    function, no status in the body.
