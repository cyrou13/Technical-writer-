---
name: iec62304-class-a
description: Reference for the IEC 62304 class A deliverables, their minimal content and the writing contract that makes them submission-grade (normative vs internal text, kinds, parameters, OTS registry, cybersecurity views, release gate). Invoke whenever an agent generates, updates or reviews 62304 documentation.
---

## OUTPUT LANGUAGE — STRICT

Any artifact produced while applying this skill (SRS/SDS/TC/RSK/THR/
USC/URSK items, aggregated reports, frontmatter values, body sections,
`[TODO]`/`[GAP-...]` markers) MUST be written in **English**,
regardless of the user's conversational language or any global
`CLAUDE.md` instruction.

# IEC 62304 — class A — reference

This skill is the **source of truth for the content of the
deliverables**. Storage and the section contract are in `items-store`;
the release gate is in `submission-readiness`.

## Class A — reminder

No injury or damage to health is possible. Lightened 62304 scope, full
document structure.

## Deliverables

| Clause | Deliverable | Items | Working build | Release export |
|---|---|---|---|---|
| §5.1 | Development plan | — | `00_dev_plan.md` | QMS |
| §5.2 | Software Requirements Specification | `SRS` (+ `MAP` upstream) | `10_SRS.md` | `build_srs_export.py` |
| §5.3–§5.4 | Software Design Description | `SDS`, `docs/ots.yaml`, `dt-clinical-context.md` | `20_SDS.md` | `build_sdd_export.py` |
| §5.5 / §5.7 | Software Test Plan / Description / Report | `TC` | `30_STD.md` | `build_stp_export.py`, `build_stdr_export.py`, `build_str_export.py` |
| §5.1.1 / §5.2.6 | Traceability | computed | `40_traceability.md` | inside SRS / STDR |
| §7, ISO 14971 | Risk analysis (safety, production) | `RSK`, `PRSK` | `50_risk_analysis.md` | `build_risk_export.py` |
| IEC 81001-5-1 | Cyber risk analysis | `THR` + four architecture views | `60_cyber_risk_analysis.md` | `build_risk_export.py` |
| IEC 62366-1 | Usability analysis | `USC`, `URSK` | `70_usability_analysis.md` | `build_risk_export.py` |
| — | Actionable backlog | computed | `_to_implement.md` | never |
| — | Open-points register | computed | — | `--internal` only |
| — | Design rationale | `## Design notes` | — | SDD appendix (`build_rationale.py`) |

## Writing rules

1. **No invention.** Every statement traces to a source file, a test or
   a tagged comment. Otherwise `[TODO]` — in an internal section.
2. **Testable sentences.** `shall` + measurable criterion. No "fast",
   "easy", "intuitive".
3. **Normative text is the present.** Sections the exporters render
   describe the device as released: no dates, no decisions, no
   re-assessments, no commit hashes, no "since version". All of that is
   `## History`.
4. **Criteria are numbered**, measurable, with the number and unit;
   never tick-boxes.
5. **One constant, one declaration** — `parameters:` (skill
   `items-store`). A number drifting between two items is a lint error.
6. **Requirement kinds** — every SRS has `kind:` so the SRS has a
   performance, interface, platform, usability, safety, security and
   process section when the product has such requirements — and visibly
   lacks one when it does not.
7. **No duplication** SRS ↔ SDS — *what* vs *how*.
8. **Immutable IDs.** Retired items are `Deprecated`.
9. **Atomicity.** One item = one requirement / module / test / risk.
10. **No competitor names, no code or test paths in SRS text.**
11. **Third-party software** is identified in `docs/ots.yaml` only.
12. **Cybersecurity architecture** is documented in the four views of
    `docs/dt-clinical-context.md` (skill `cyber-risk-analysis`).

## Minimal fields

- **SRS**: `id`, `title`, `kind`, `description`, `verification`,
  `priority`, `source`, `status`, `parameters` (may be empty).
- **SDS**: `id`, `module`, `responsibility`, `interfaces`, `implements`,
  `source`, `## Design`.
- **TC**: `id`, `title`, `verifies`, `test_id` (existing), `steps`,
  `expected`, `source`.

## Gap markers

When a deliverable cannot be completed:

```
[GAP-62304] §5.2.2 — <explanation> — <action required from the user>
```

Placed in `## Open questions` (and echoed in `## History`) of the item
concerned — never in a normative section. The `compliance-reviewer`
aggregates them; the release export refuses any that leaked (TL-1).

## Not covered in v1

- Configuration management (§8) — git.
- Problem resolution (§9) — the issue tracker.

## Risks (§7) — class A scope

Covered by `risk-analysis` / `risk-analyst`. In class A the analysis
**justifies the classification**: every risk ends `risk_level: Low` and
`acceptable: true`, or has at least one control bringing
`residual_acceptable: true`. Any non-acceptable residual, or any hazard
with `severity: Critical/Catastrophic`, **invalidates class A** — alert.

For class B/C or fuller SOUP management, derive `iec62304-class-b` or
extend this skill.
