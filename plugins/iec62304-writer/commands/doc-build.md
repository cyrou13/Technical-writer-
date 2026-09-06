---
description: Aggregates the items into the working documents (SRS/SDS/STD/traceability/risk) and computes coverage; with --release runs the document-control gate and the submission lint and refuses to export when the store is not clean. Idempotent.
---

Build the documentation from `docs/items/`. Three modes, decided by
`$ARGUMENTS`:

| Arguments | Effect |
|---|---|
| (none) or `--strict` | working build: `python tools/build_docs.py [--strict]` → `docs/generated/`. Deliverables, if the exporters are present, are produced with a `WORKING DRAFT — generated <today>` cover, each with its own `documents.<x>` identifier and title, its References section and its **unresolved anomalies** appendix. |
| `--internal` | as above, plus the **open-points register** appended to each deliverable (from `## Open questions` and the `[TODO`/`[GAP-` markers). The open-points register and the anomalies appendix are two different lists: the anomalies appendix is exported in every mode, the register only here. Never for a customer. |
| `--release` | the gate of skill `submission-readiness` runs first; only if it passes are the exporters called with `--release`, producing the signed-cover deliverables. |

`--release` and `--internal` together → stop and explain they are
exclusive.

## Steps

1. Check Python 3 is available (`python --version` or `python3 --version`).

2. **Working build** — `python tools/build_docs.py` (add `--strict` if
   requested). Non-zero exit → show the Python error verbatim, do not
   hide it, stop.

3. **Release gate** (only with `--release`), in this order, stopping at
   the first failing step and printing its offender list verbatim:

   a. `python tools/build_docs.py --strict` — markers anywhere in the
      store, class A severities, residuals, controls (SL-7, SL-5).
   b. **Document control** — read `dt-config.yaml`: `document.date`,
      `document.version_label`, `revision_history`. Refuse if any
      non-Deprecated item has `updated` or `reviewed` later than
      `document.date` (DC-1), if `revision_history` has no entry for
      `document.version_label` dated `document.date` (DC-2), or if the
      history dates are not increasing (DC-3). Print the offending items
      with their dates. Say what fixes it: bump `version_label` and
      `date`, add the `revision_history` row.
   c. **Store lint** — parameters (SL-1: one name, one value; settable
      needs interval; SL-8: `source` not a path, one owner, described
      by its owner, list values as lists), kinds (SL-2), OTS registry
      (SL-3, SL-12: one row per component at exact version,
      `supersedes`, honest `hazard_review`, base image, no second
      inventory), test ids (SL-4), the six `dt-clinical-context.md`
      anchors (SL-6), references (SL-9), document identifiers vs
      `project_references` (SL-10), harm-based risk scales and residual
      rationale (SL-11), THR sections and the four views (SL-13), test
      procedures and binder statuses (SL-14). Use the exporters' own
      check where present; otherwise apply the `compliance-reviewer`
      grep recipe and say the gate was applied manually.
   c'. **Decision findings** — DEC-1/2 (labeling vs specification) are
      printed but do **not** block: they are for the product owner /
      RAQA and no tool or writer resolves them. Say so in the summary.
   d. **Exports** — for each exporter present in `tools/`
      (`build_srs_export.py`, `build_sdd_export.py`,
      `build_stp_export.py`, `build_stdr_export.py`,
      `build_str_export.py`, `build_risk_export.py`): run it with
      `--release` (plus `--md-only` if the user asked for Markdown only).
      Each exporter applies the text lint (TL-1 … TL-14) and refuses on
      its own offenders; print them grouped by rule. An exporter that
      refuses leaves no file behind — do not fall back to a draft
      export in the same run. The STDR / STR need a bound run
      (`tools/bind_test_results.py`): report the run metadata they will
      print (software version + source, release-evidence mode, host,
      branch, dirty flag) and warn when the run is outside
      release-evidence mode or on a dirty tree — the export states it
      honestly, the user decides whether that is the release run.

   If the exporters are not present in `tools/`, say so and point to
   `scaffold/tools/README.md`: the release export cannot be produced
   without them, and `docs/generated/` is not a deliverable.

4. **Internal build** (only with `--internal`) — run the exporters with
   `--internal`, then `python tools/build_open_points.py` if present.

5. Summary, 10 lines or fewer:
   - items read per category,
   - coverage metrics from `coverage.json` (verification counted on
     existing tests only; planned TC stated separately),
   - mode (working draft / internal / release) and the files produced,
     each with its `documents.<x>` identifier,
   - the unresolved anomalies count (known defects + xfail/skip TCs +
     `residual_acceptable: false` items + decision-record open actions),
   - DEC findings (count, not blocking),
   - for `--release`: "gate passed" or the count of offenders per rule
     and the first three offenders.

## Guard rails

- Never edit an item to make the gate pass — report, the writers fix.
- Never edit the labeling anchors or `dt-config.yaml` to make a DEC
  finding or SL-10 pass.
- Never call an exporter with `--release` when step 3.a–c failed.
- Never commit or push.
