---
description: Updates the 62304 documentation after the code evolved — detects orphans, stale items and coverage gaps, re-processes only the delta, writes History (never Changelog), then reports the lint counts. Optional label `Vx.y` for a global major bump (e.g. /doc-update V2.0).
---

The user wants to **update** the existing documentation after the code
changed, not regenerate from scratch. Idempotent: nothing changed →
nothing modified.

Optional `$ARGUMENTS`: `Vx.y` (e.g. `V2.0`) — global major bump. Every
item modified in steps 3 or 4 gets `version: x.y.0`, and every modified
`Approved` item returns to `Draft`.

## Steps

### 1. Map (refresh)

Run `code-archeologist` → `docs/generated/_codemap.md`.

### 2. Diff (framing)

Run `doc-updater`. It deprecates total orphans, cleans partial orphans
(both through `## History`), renames any legacy `## Changelog` header it
meets, and lists stale items and gaps in
`docs/generated/_update_diff.md`.

**Blocking.** Read the report. Empty → say "Documentation already up to
date" and jump to step 6.

### 3. Targeted re-processing

Run **only** the writers the diff concerns (in parallel when
independent):

- SRS gaps or stale SRS → `requirements-writer`
- SDS gaps or stale SDS → `architecture-writer` (also refreshes
  `docs/ots.yaml` when a manifest changed)
- TC gaps or stale TC → `test-evidence-collector`

Order: `requirements-writer` first, then the two others in parallel. The
writers are idempotent: they re-read, modify only what needs it, create
what is missing, and rewrite normative sections **so that they read as
the present** — every "was / is now" goes to `## History`.

### 4. Risk re-evaluation

If **any** SRS / SDS / TC changed in step 3, run in sequence
`risk-analyst`, `security-analyst`, `usability-analyst` (the last only
if UI components changed). Each re-reads the modified items, checks
that the existing controls (`links.mitigates`) still hold, updates the
residual fields when needed, and records the re-assessment as **one
dated line in `## History` of the risk item** — the normative sections
are rewritten only when the assessment itself changed, and then undated.
A risk that becomes non-acceptable gets its `[GAP-…]` marker in
`## Open questions` and `## History`, never in the body.

### 5. Major bump (with `Vx.y`)

For each item modified in steps 3 or 4:

- `version: x.y.0`;
- `Approved` → `Draft`;
- one line at the top of `## History` (create the section if absent;
  never a `## Changelog`):
  ```markdown
  - YYYY-MM-DD vx.y.0 — aligned on Vx.y: <short summary of the change>
  ```

Without the argument, the writers bump at their natural granularity
(`items-store` rules).

### 6. Build

`python tools/build_docs.py`. Check the aggregates are regenerated.

### 7. Review

Run `compliance-reviewer` → `docs/generated/99_compliance_review.md`.
Its first section is the release-gate offender list.

### 8. Summary to the user (16 lines or fewer)

- Deprecated items (total orphans): N — listed.
- Partial orphans cleaned: N. Changelog sections renamed: N.
- Stale items re-processed: N. Coverage gaps created: N.
- Risk items whose residual changed: N — alert if > 0.
- **Lint counts** from the review: offenders per rule (DC-*, TL-*,
  SL-*), and whether a `--release` export would pass today.
- Before / after coverage if the previous `coverage.json` is in git.
- Paths of the main outputs.
- If `Vx.y` applied: number of items aligned.

## Guard rails

- **Strict idempotence**: unchanged code → zero item modified.
- **No deletion of items.** Ever. Always `Deprecated`.
- **No date, decision or change note outside `## History`.**
- If `_codemap.md` is not produced → stop.
- Build failure → show the Python error, do not hide it.
- The `Vx.y` label touches only the items modified in this pass.
- Never commit or push unless asked.
