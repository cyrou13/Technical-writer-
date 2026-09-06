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

## Scales — defined in `dt-config.yaml`, harm-based

The scales are **not** in this skill and not in the exporter: they are
`classification.severity_definitions` and
`classification.probability_definitions` of `dt-config.yaml`, one
harm-based sentence per level in ISO 14971:2019 Annex C terms, rendered
in the RAR methodology section. A names → integers mapping is a defect:
it lets "regulatory breach" and "neurological injury" share `Serious`
without anybody having decided so.

```yaml
classification:
  severity_definitions:
    Negligible: inconvenience or temporary discomfort; no medical intervention
    Minor: temporary injury or impairment not requiring professional medical intervention
    Serious: injury or impairment requiring professional medical intervention
    Critical: permanent impairment or life-threatening injury
    Catastrophic: patient death
  probability_definitions:
    Improbable: not expected in the lifetime of the installed base
    Remote: …
```

Levels: severity `Negligible` … `Catastrophic`; probability
`Improbable` / `Remote` / `Occasional` / `Probable` / `Frequent`; risk
level `Low` / `Medium` / `High` from one matrix. In class A, `Critical`
and `Catastrophic` trigger reclassification. The **class argument**
(the MAP record named in `classification.record`) lists **each RSK and
PRSK once**, with its initial and its residual severity in two columns
— never one row per severity field, never a subset.

## Control hierarchy (ISO 14971 §7.2) — `control_hierarchy`

1. `inherent_design` — eliminate the hazard (preferred).
2. `protective_measure` — a barrier or check in the software (input
   validation, timeouts, bounded retry).
3. `information_for_safety` — IFU / labeling text; requires
   `labeling_disclosure` to hold the verbatim string. **On its own it is
   not creditable risk reduction**: a risk whose only control is a
   warning keeps its initial index, and its acceptance is argued on
   that index (or an engineering control is added).

## Form of a mitigation

Always linked to the risk through `links.mitigates` on the control:

- **Mitigation SRS** — `kind: safety`, `priority: Must`,
  `links.mitigates: [RSK-…]`. Appears in `_to_implement.md` until an SDS
  implements it and a TC verifies it.
- **SDS constraint** — a design decision (isolation, no secret in state).
- **Dedicated TC** — evidence of effectiveness.

One control may mitigate several risks. Controls are never stored on the
RSK frontmatter; the build computes them from `links.mitigates`, and the
item's `## Risk controls` section states them **one line each — id,
what the control does, tier** — because the RAR renders that section per
record. **A control's evidence is the status of the TC bound to it**
(`Passed` from `bind_test_results.py`), printed next to the control by
the exporter; a control with no TC, or a TC bound `Unknown`, is an
unverified control and the residual argument must say so.

A control must address the **mechanism** of the hazard it is linked to:
a clinical-evidence regeneration hazard is not mitigated by a phantom
accuracy test. Before adding `links.mitigates`, state in one sentence
how the control interrupts the foreseeable sequence; if the sentence
cannot be written, the link is a mis-trace.

## Acceptability criterion

A risk item is **addressed** when either `risk_level: Low` and
`acceptable: true`, or at least one item mitigates it and
`residual_acceptable: true` with the residual fields filled. Anything
else appears in `_to_implement.md`.

## What goes where in a RSK / PRSK body

The eight normative sections (`## Hazard` … `## Residual risk
justification`) state the risk **as currently assessed**. They carry no
date, no "re-assessed after …", no marker, no reference to a commit, no
person or host name ("confirm with Cyril", "on choupinette"), no issue
number. When a hash, an issue or a competitor reference is removed, the
**whole parenthetical or clause** goes — never "(open issue".

- **`## Hazard` describes the hazard**, the potential source of harm in
  the released software — never the pre-control state ("nothing is
  hash-pinned", "the manifest currently contains PLACEHOLDER"): that
  text describes a defect of a past build, not a hazard, and it reads as
  current in the RAR.
- **`## Risk controls`** and **`## Residual risk justification`** are
  rendered per record in the RAR. The residual argument is present on
  every accepted risk; **a residual accepted with an unchanged index**
  (same severity, same probability — 9 → 9) needs a stated rationale
  (why the risk is acceptable as is, or why the control does not move
  the index but is kept), not a bare `residual_acceptable: true`.

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
