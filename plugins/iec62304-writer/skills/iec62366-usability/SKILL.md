---
name: iec62366-usability
description: IEC 62366-1 reference (usability engineering for medical devices). Invoke to produce Use Scenarios (USC), Use-Related Risks (URSK) and usability test cases (TC type E2E with usability_type), with the same normative-vs-History discipline as the other items.
---

## OUTPUT LANGUAGE — STRICT

Any artifact produced while applying this skill (USC/URSK items,
frontmatter values, body sections, `[GAP-USE]` markers) MUST be
written in **English**, regardless of the user's conversational
language or any global `CLAUDE.md` instruction.

# IEC 62366-1 — usability engineering

## Framework

- **IEC 62366-1:2015 + A1:2020** — application of usability engineering
  to medical devices; **IEC 62366-2** — guidance.
- Complements IEC 62304 (software) and ISO 14971 (risk): covers **use
  errors** by the end user.

## Vocabulary

Use specification, use scenario, use error, hazard-related use scenario,
formative evaluation, summative evaluation — IEC 62366-1 §3.

## Item categories

- **USC** — who does what, where, how. Frontmatter: `persona`,
  `environment`, `task`, `frequency`, `criticality`.
- **URSK** — use errors that may lead to a hazard. Distinct from RSK
  (code origin) and THR (attacker origin): the origin is the user.
  `links.triggers: [RSK-…]` when the error triggers a known safety
  hazard.
- **TC type E2E** with `usability_type` ∈ {`formative`, `summative`}.

## Method (agent `usability-analyst`)

1. **UI surfaces** from the codemap: components (`*.tsx`, `*.jsx`,
   `*.vue`, `*.svelte`, Angular templates), pages / routes, forms,
   dialogs, error states, keyboard shortcuts, drag-and-drop.

   ### UI pattern catalogue → frontend SRS → E2E TC

   SRS produced here have `kind: usability` and a `VIEWER` (or
   component-name) domain, distinct from the backend SRS.

   | Source scanned | SRS produced | E2E TC domain |
   |---|---|---|
   | routes, route guards, programmatic navigation | `SRS-VIEWER-NAV-*` | permissions + navigation |
   | required / pattern fields, Yup / Zod, `useForm` | `SRS-VIEWER-FORM-*` | form validation |
   | confirmation dialogs, `confirm()`, double action | `SRS-VIEWER-CONFIRM-*` | confirmations |
   | auth flows (login, logout, forced password change) | `SRS-VIEWER-AUTH-*` | auth |
   | loading skeletons, empty states, error banners | `SRS-VIEWER-STATE-*` | error states |
   | permission guards, conditional render | `SRS-VIEWER-PERM-*` | permission boundary |
   | WebSocket subscriptions (live updates, reconnect) | `SRS-VIEWER-WS-*` | websocket |
   | `aria-*`, keyboard navigation, focus management | `SRS-VIEWER-A11Y-*` | axe-core / a11y |
   | test anchors: `data-testid`, `role="alert"`, `aria-busy` | `SRS-VIEWER-A11Y-*` (missing anchors) | testability |

   ### Missing-anchor scan

   For every interactive component: check `data-testid`; for
   multi-state components (loading / empty / error / ready) check
   distinct role + testid per state. A missing anchor yields a
   `SRS-VIEWER-A11Y-*` requiring it, `priority: Should` (Must if it
   blocks an existing E2E TC). This channel flags what is **missing**.

   Existing Playwright / Cypress specs (`tests/e2e/**`, `e2e/**`,
   `cypress/**`) are referenced through `test_id:`, not regenerated.

2. **Personas** from CLAUDE.md / README / product context. Not explicit →
   ask; never invent.
3. **USC** per identifiable user task (one business task = one USC).
4. **Plausible use errors** per USC: wrong default, hasty validation,
   confusable actions, entry error (typo, unit, magnitude),
   misinterpreted visualisation (colour, scale, side), irreversible
   action without confirmation, context error (multi-patient,
   multi-window).
5. **URSK** for every use error that can cause harm; otherwise a line in
   the USC's `## Foreseeable use errors`.
6. **Controls** in the ISO 14971 hierarchy: elimination > technical
   measure > information. Mitigation SRS `kind: usability`,
   `priority: Must`, `links.mitigates: [URSK-…]`.
7. **Linkage** — `URSK.links.triggers`, mitigation SRS, usability TC.

## Scales

As ISO 14971: severity Negligible … Catastrophic; likelihood Improbable …
Frequent; `risk_level` Low / Medium / High.

## What goes where

The normative sections of USC and URSK state the scenario and the risk
as currently assessed. Re-assessments after a UI change, decisions and
revised arguments are dated lines in `## History`. `[GAP-USE]` goes in
`## Open questions` and `## History` only, with
`residual_acceptable: false` in the frontmatter.

## Summative validation

IEC 62366-1 expects a documented **summative evaluation** before release:
TC `type: E2E`, `usability_type: summative`; the STD strategy section
states method, sample size and pass / fail criteria; the summative report
itself is human observation, written by the user as
`docs/usability_summative_report.md` and referenced from the STD.

## Guard rails

- No invented personas, no USC without a real UI component in `source:`,
  no URSK without an inferable use error.
- No duplication with RSK / THR — the distinction is the origin; use
  `triggers` rather than a copy.
- No active scanning or runtime instrumentation.
- No UI in the project → an explicit empty report ("no UI surface
  detected — IEC 62366-1 not applicable").

## Class A note

A clinical UI can still induce errors with impact (misreading, wrong
side, wrong priority). 62366-1 applies whenever there is a user
interface. A URSK reaching `severity: Critical/Catastrophic` questions
the class A classification.
