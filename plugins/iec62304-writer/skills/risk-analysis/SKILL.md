---
name: risk-analysis
description: ISO 14971 + IEC 62304 §7 reference for software risk analysis (class A) — hazard identification, control derivation, RSK and PRSK items, and the rule that re-assessments are History, not body text. Invoke to identify hazards, derive controls and produce RSK / PRSK items and mitigation SRS.
---

# Risk analysis — reference

Applies **ISO 14971:2019** and **IEC 62304 §7** to class A software. In
class A the analysis mainly **justifies the classification**: every
identified hazard is either acceptable as is or reduced to acceptable by
controls.

## Vocabulary (ISO 14971)

- **Hazard** — potential source of harm.
- **Initiating cause** — an independent trigger of the sequence.
- **Foreseeable sequence of events** — the chain from cause to hazardous
  situation (§C.2).
- **Hazardous situation** — circumstance of exposure to the hazard.
- **Harm** — physical injury, damage to health, or damage to data /
  property.
- **Risk** — severity × probability.
- **Risk control** — measure reducing the risk; **residual risk** —
  what remains after it.

## Two item categories

- **RSK** — design risks arising from runtime behaviour of the software
  (`risk_category: Design`) or from use (`Usability`, when the URSK
  analysis is not applicable).
- **PRSK** — production / supply-chain risks arising from packaging,
  delivery, deployment and update (`production_phase`), anchored in a
  Dockerfile, CI workflow, deploy script or manifest. Produced with the
  security-analyst, since most initiating causes are cyber.

## Typical software hazard categories

1. Functional error — wrong computation, inconsistent state.
2. Failure — crash, deadlock, memory leak, OOM, timeout.
3. Security — injection, XSS, CSRF, secret leak, privilege escalation
   (cross-link to a THR rather than duplicate).
4. Data integrity — corruption, loss, desynchronisation, wrong patient.
5. Auth / authz — bypass, fixation.
6. Confidentiality — sensitive data exposure, PII in logs.
7. Availability — prolonged outage, silent degradation.
8. Usability — misleading interface (URSK when a UI exists).

## Scales (class A — simplified)

| Severity | Definition |
|---|---|
| Negligible | transient inconvenience, no consequence |
| Minor | recoverable data loss, annoyance |
| Serious | lasting damage (privacy, financial) |
| Critical | not class A — triggers reclassification B/C |
| Catastrophic | not class A |

Probability: `Improbable` / `Remote` / `Occasional` / `Probable` /
`Frequent`. Risk level: `Low` / `Medium` / `High`. Any `Medium` or `High`
that cannot be reduced questions class A.

## Control hierarchy (ISO 14971 §7.2) — `control_hierarchy`

1. `inherent_design` — eliminate the hazard (preferred).
2. `protective_measure` — a barrier or check in the software (input
   validation, timeouts, bounded retry).
3. `information_for_safety` — IFU / labeling text; requires
   `labeling_disclosure` to hold the verbatim string.

## Form of a mitigation

Always linked to the risk through `links.mitigates` on the control:

- **Mitigation SRS** — `kind: safety`, `priority: Must`,
  `links.mitigates: [RSK-…]`. Appears in `_to_implement.md` until an SDS
  implements it and a TC verifies it.
- **SDS constraint** — a design decision (isolation, no secret in state).
- **Dedicated TC** — evidence of effectiveness.

One control may mitigate several risks. Controls are never stored on the
RSK; the build computes them.

## Acceptability criterion

A risk item is **addressed** when either `risk_level: Low` and
`acceptable: true`, or at least one item mitigates it and
`residual_acceptable: true` with the residual fields filled. Anything
else appears in `_to_implement.md`.

## What goes where in a RSK / PRSK body

The eight normative sections (`## Hazard` … `## Residual risk
justification`) state the risk **as currently assessed**. They carry no
date, no "re-assessed after …", no marker, no reference to a commit.

- A **re-assessment** ("after the frame-rejection change, probability
  unchanged; controls still hold") is one dated line in `## History`.
- A **revised residual argument**: rewrite `## Residual risk
  justification` so it reads as the current argument, and record in
  `## History` what changed and why.
- `[GAP-62304]` (residual not acceptable, class A in question) goes in
  `## Open questions` and `## History`, and `residual_acceptable: false`
  in the frontmatter — never in a normative section.
- `arising_risks` lists RSK IDs created by a control (§7.5).

## Identification method (in the agent)

Walk the codemap and look systematically at: external entry points,
trust boundaries, secret storage, persistence, sensitive computations
(dose, amount, identifier, map values), logs and telemetry, and — for
PRSK — every build, packaging and deploy artefact. For each candidate
state `hazard` / `initiating_causes` / `foreseeable_sequence` /
`hazardous_situation` / `harm` in short factual sentences. **Do not
invent** hazards that cannot be anchored in a file.

## Class A note

If a risk keeps `severity: Critical` or `Catastrophic` after mitigation:
stop, set `residual_acceptable: false`, write the `[GAP-62304]` line in
`## Open questions`, and alert the user — the product is not class A.
