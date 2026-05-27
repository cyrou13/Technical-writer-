---
name: mitigation-audit
description: Convention pour auditer la couverture code-vs-mitigation d'un risque résiduel non-acceptable. À invoquer quand on doit décider si un contrôle proposé en `[TODO]` est en réalité déjà implémenté dans le code, ou pour annoter les SRS de mitigation avec un statut d'implémentation (`absent | partial | implemented`) accompagné d'une evidence code:line.
---

## OUTPUT LANGUAGE — STRICT

Any artifact produced under this skill (`docs/generated/_mitigation_audit.md`,
`implementation_status` / `implementation_evidence` / `implementation_gap`
frontmatter values, `[TODO]` / `[GAP-IMPL]` markers, audit-report text)
MUST be written in **English**, regardless of the user's conversational
language or any global `CLAUDE.md` instruction. Conversational replies
MAY follow the user's language.

# Mitigation audit — code-vs-control coverage check

## Why this skill exists

When the risk analysts (`risk-analyst`, `security-analyst`,
`production-risk-analyst`, `usability-analyst`) propose controls for a
hazard, they often mint a brand-new `SRS-MIT-XXX` marked `[TODO]`
without first checking whether the codebase already implements the
control. Result: a long tail of `residual_acceptable: false` risks that
look like missing-code gaps but are actually missing-documentation
gaps — the code is there, the SRS-MIT just doesn't point to it.

The audit step closes that gap. For every risk with
`residual_acceptable: false`:

1. **Static cadrage** (deterministic, scripted) — list every control
   cited in the risk body or linked via `links.mitigates`, and assign
   each control a static state (item exists, has `source:` pointer,
   has `[TODO]` in body, has TC).
2. **Code inspection** (agent-driven, requires judgment) — read the
   files in `source:` and decide if the control is `absent`,
   `partial` (implemented but with a concrete gap), or `implemented`.
3. **Frontmatter annotation** — write the verdict on the SRS-MIT
   itself, so downstream readers (notified body, future agents)
   inherit the conclusion instead of re-doing the audit.

## When to invoke

- The user reports a high count of `residual_acceptable: false` after
  `/doc-62304` or `/doc-update`.
- Before any submission deliverable (`/doc-risk-export`,
  `/doc-risk-xlsx`) — to remove false-positive gaps.
- After a code change that may have implemented previously-proposed
  controls (rare, but possible).

The recommended entry point is the `/doc-audit-mitigations` command,
which orchestrates the script + agent + apply + rebuild.

## Verdict scale

| Verdict       | Meaning                                                                                   |
|---------------|-------------------------------------------------------------------------------------------|
| `absent`      | No code in the cited `source:` files implements the requirement at all.                   |
| `partial`     | Some code exists, but at least one acceptance criterion (or one stated sub-step) is not met. Always paired with a concrete `implementation_gap`. |
| `implemented` | Every acceptance criterion is met by the cited code. No `[TODO]` remains.                 |
| `unknown`     | Default when the SRS has not been audited yet.                                            |

`partial` MUST be paired with an `implementation_gap` string describing
the missing piece in operational terms ("`anonymise()` is called but
the exception is not caught in `handle_store()` — instance saved even
on failure"). Vague phrasing ("incomplete coverage") is forbidden.

## Frontmatter schema additions on SRS items

The audit adds three optional fields to the SRS frontmatter:

```yaml
implementation_status: partial         # absent | partial | implemented | unknown
implementation_evidence:               # list of {path, note}
  - path: src/cina/dicom/dicom_receiver.py:247
    note: "anonymise_instance() called before save_as()"
implementation_gap: |
  No exception handler around anonymise_instance(); a raise leaves
  dataset.save_as() to run with un-anonymised data.
```

These fields are read by:

- `tools/audit_mitigations.py` — surface in static cadrage.
- `mitigation-auditor` agent — produce / refresh.
- `risk-analyst` (future enhancement) — consume to decide whether a
  proposed control is already in place before minting a new SRS-MIT.

The fields are **additive**. Items without them are valid; the audit
treats them as `unknown` and triggers an agent review.

## Flipping `residual_acceptable`

A risk's `residual_acceptable` can be flipped from `false` to `true`
**only** when:

1. **Every** control linked via `links.mitigates` has
   `implementation_status: implemented`, AND
2. Each linked SRS has at least one TC in `links.verifies` of a TC
   item (or `verifies: []` is explicitly justified in the SRS body).

If only some controls flip to `implemented`, the risk stays
`not-acceptable` but the residual narrative is updated to reflect what
has been validated and what remains.

The agent does **not** mutate the risk item's
`residual_acceptable` field directly during the audit pass — it
recommends the flip and the orchestrator's `--apply` flag (or a
follow-up `risk-analyst` invocation) performs it. Rationale: the
flip cascades through the build (`coverage.json`, risk report) and is
a meaningful documentation event, not a side effect of an audit.

## Outputs

- `docs/generated/_mitigation_audit.md` — human-readable audit
  report. Lists every risk in scope with a per-control verdict table
  and an agent review queue.
- `docs/generated/_mitigation_audit.json` — same content,
  machine-readable. Consumed by the agent.
- `docs/items/SRS/SRS-*.md` — frontmatter updated in place with
  `implementation_status` / `implementation_evidence` /
  `implementation_gap` (only when the agent runs with `--apply`).

## Guardrails

- **Read code, do not run it.** The audit never executes tests, never
  invokes the application — it reads files only.
- **Never invent evidence.** If a verdict requires evidence that is not
  in the codebase (e.g. "the IFU says X"), record the verdict as
  `unknown` and flag the open question instead of fabricating a
  `path:line`.
- **Preserve existing frontmatter.** The audit only adds the three
  implementation fields and never edits any other field.
- **Bump on changes.** If the audit modifies an SRS, bump
  `version` patch and update `updated:`. If the item was `Approved`,
  drop it back to `Draft`.
