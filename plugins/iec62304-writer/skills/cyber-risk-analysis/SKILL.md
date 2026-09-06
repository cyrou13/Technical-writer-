---
name: cyber-risk-analysis
description: IEC 81001-5-1 + AAMI TIR57 + STRIDE reference for the cybersecurity analysis of medical device software, including the four cybersecurity architecture views the FDA 2023 premarket guidance expects and the OTS registry as the supply-chain baseline. Invoke to identify threats, derive controls and produce THR items distinct from safety RSK.
---

## OUTPUT LANGUAGE — STRICT

Any artifact produced while applying this skill (THR items, derived
SRS, frontmatter values, body sections, `[GAP-CYBER]` markers) MUST be
written in **English**, regardless of the user's conversational
language or any global `CLAUDE.md` instruction.

# Cyber risk analysis — reference

Distinct from and complementary to the safety analysis (ISO 14971 /
62304 §7). Frameworks:

- **IEC 81001-5-1** — security in the health software life cycle.
- **AAMI TIR57** — principles for medical device security risk
  management.
- **FDA, Cybersecurity in Medical Devices: Quality System
  Considerations and Content of Premarket Submissions (September 2023)**
  — expects a threat model, an SBOM, and **architecture views**.
- **MDCG 2019-16** (EU).

A threat may **trigger** a safety hazard: `links.triggers: [RSK-…]` on
the THR. Any control (`links.mitigates`) may address THR, RSK, PRSK or
URSK alike.

## Vocabulary

Asset, threat, vulnerability, attack, security control, residual risk —
IEC 81001-5-1 §3.

## Attacker model

| `attacker` | Assumed capability |
|---|---|
| `external_unauth` | Internet attacker, no account |
| `external_auth` | legitimate but malicious user |
| `internal` | employee / operator with internal access |
| `supply_chain` | compromised dependency, base image or registry |
| `physical` | physical access to the device or workstation |

## STRIDE

| | Category | Property violated | Examples |
|---|---|---|---|
| **S** | Spoofing | authenticity | fixed session, forged JWT, credential replay |
| **T** | Tampering | integrity | mass assignment, parameter altered in transit, tampered image |
| **R** | Repudiation | non-repudiation | user action without an audit record |
| **I** | Information disclosure | confidentiality | verbose error, PII in log, side channel |
| **D** | Denial of service | availability | catastrophic regex, OOM, unbounded queue |
| **E** | Elevation of privilege | authorisation | IDOR, RBAC bypass, missing authz check |

Apply S-T-R-I-D-E **systematically** to every entry point, trust boundary
and sensitive asset drawn on the architecture views.

## The four cybersecurity architecture views — all four required

The security-analyst produces (or completes) these sections of
`docs/dt-clinical-context.md`; each THR names the view it is drawn on in
`architecture_view:`. The SDD export requires **all four** non-empty
(SL-13); a product with a single deployment form still has an
updateability view and a multi-patient view (one instance processing
studies in sequence is a multi-patient boundary).

| Anchor | View | What it must show |
|---|---|---|
| `security-global-view` | Global system view | every network interface, port and protocol; trust boundaries; authentication points; each data store with its protection at rest and in transit; where secrets live |
| `security-multi-patient-view` | Multi-patient harm view | how one patient's data and results are isolated from another's on the same instance: session scope, identifiers, storage separation, cleanup, what a cross-patient failure would look like |
| `security-updateability-view` | Updateability / patchability view | how software and OTS updates are delivered, authenticated, applied and rolled back; who can trigger one; device behaviour during an update; OTS end-of-life handling |
| `security-use-case-views` | Security use-case views | one diagram per security-relevant use case (ingest, export, administer, update, support access): actors, data crossing each boundary, the control that protects the crossing |

Diagrams are Mermaid; each view has a paragraph per boundary. No dates,
no markers — the sections are exported into the SDD.

## Method (in the agent)

1. **Assets** — credentials, session tokens, PII and clinical data,
   critical side-effecting functions, configuration and secrets, signing
   keys, images.
2. **Entry points and boundaries** — from the codemap and the global
   view: routes, webhooks, sockets, CLI, DICOM listeners, file imports,
   environment variables, pub/sub.
3. **STRIDE per entry point** — one THR per plausible combination
   anchored in a real file or registry entry.
4. **Supply chain from the OTS registry** — `docs/ots.yaml` is the
   baseline. For each component with `safety_relevant: true` or in the
   auth / crypto / parsing / network perimeter, create a THR
   `attacker: supply_chain` only with a concrete reason (audit finding,
   known vulnerable version, `eol_status: end-of-life`). Otherwise
   recommend the audit in the return; never invent a CVE. Production and
   delivery threats become **PRSK** items (skill `risk-analysis`) rather
   than THR.
5. **Likelihood × impact** — Low / Medium / High each; `risk_level` from
   the 3×3 matrix below, **applied identically to every THR** (Low ×
   High is `Medium` on every record, not `High` on three and `Medium`
   on the fourth). Fill the CIA severities and `residual_risk_level`.
6. **Safety link** — `links.triggers: [RSK-…]` when exploitation reaches
   a clinical output or availability of a critical function.
7. **Controls** — elimination > technical measure > information.
   Mitigation SRS have `kind: security`, `priority: Must`,
   `links.mitigates: [THR-…]`.

## 3×3 matrix

|              | Impact Low | Impact Medium | Impact High |
|---|---|---|---|
| **Likelihood Low**    | Low | Low | Medium |
| **Likelihood Medium** | Low | Medium | High |
| **Likelihood High**   | Medium | High | High |

`risk_level: High` that cannot be reduced escalates to the quality system.

## CIA impact dimensions (IEC 81001-5-1)

### Why rate CIA separately from STRIDE

STRIDE classifies the **attack vector** — what the attacker does. CIA
measures the **impact on the security properties** — what is lost for
the protected asset. The same STRIDE category yields different CIA
profiles depending on the asset (spoofing a session token hits
Confidentiality + Integrity; spoofing a log entry mainly Integrity).
The separation matches the "Cybersecurity" tab of the 4-tab risk table
(`/doc-risk-xlsx`) and IEC TR 60601-4-5.

### Allowed values

`n/a` | `Low` | `Medium` | `High` for `confidentiality_severity`,
`integrity_severity`, `availability_severity` and their `residual_*`
counterparts. `n/a` means the dimension is not affected (a
denial-of-service threat typically has `confidentiality_severity: n/a`
and `integrity_severity: n/a`).

### Projection of CIA onto `risk_level`

`impact = max(C, I, A)` with `n/a` treated as `Low`; `risk_level` then
comes from the 3×3 matrix above with `likelihood`. A `High` on any
single dimension gives `impact: High`. The `impact` field stays the
single label a reader sees before the CIA table; once the dimensions
are filled it must equal their maximum.

### Typical STRIDE → CIA projection (indicative — justify per asset)

| STRIDE | Confidentiality | Integrity | Availability |
|---|---|---|---|
| S — Spoofing | Medium–High (identity assumed) | High (actions under a wrong identity) | n/a |
| T — Tampering | n/a–Low | High (data altered) | Low–Medium (corrupted data may block processing) |
| R — Repudiation | Low (audit log missing) | High (non-repudiation broken) | n/a |
| I — Information disclosure | High | n/a | n/a |
| D — Denial of service | n/a | n/a | High |
| E — Elevation of privilege | High (elevated access) | High (may modify anything) | Medium–High (may disrupt as admin) |

The `## CIA impact analysis` section justifies each dimension
(`### Confidentiality`, `### Integrity`, `### Availability`; "Not
affected" when `n/a`).

## THR body — what goes where

The normative sections state the threat **as currently assessed** and
are rendered as the threat record of the RAR and of the SDD:

| Section | Content |
|---|---|
| `## Threat description` | what the attacker achieves against which asset — a reviewer must understand the threat from this paragraph alone, not from the STRIDE letter and the CIA table |
| `## Attack path and preconditions` | the entry interface of the global view, the boundary crossed, every precondition (access, a prior failure, a configuration), the step that compromises the asset |
| `## Level justification` | why this likelihood and impact, the matrix result |
| `## Controls` | **requirement ids** (SRS, SDS for a design constraint), one line each with what the control does. **A TC id is verification of a control, never a control** — the exporter prints each control's bound TC status next to it |
| `## Residual` | the residual level and the condition under which it is accepted; when `residual_acceptable: false`, the condition that would make it acceptable and the owner — it then appears in the unresolved anomalies appendix |
| `## CIA impact analysis` | per dimension |

Re-assessments after a code change, decisions, and revised arguments are
dated lines in `## History`. `[GAP-CYBER]` goes in `## Open questions`
and `## History` only, with `residual_acceptable: false` in the
frontmatter. CVE / CWE references and audit recommendations go in
`## Notes`. A THR whose title names a deleted surface ("Debug UI") is
Deprecated, not left as is.

## Acceptability

A THR is **addressed** when `risk_level: Low` and `acceptable: true`, or
at least one item mitigates it and `residual_acceptable: true`. Otherwise
it appears in `_to_implement.md` (group B, Cyber).

## Guard rails

- No invented threats: anchor in a file or a registry entry.
- No active scanning, fuzzing or intrusion testing from the agent.
- No safety/cyber duplication: one hazard appears once, as RSK or THR;
  `triggers` connects the two.
- OTS versions and suppliers are read from `docs/ots.yaml`, never
  repeated in a THR body. `docs/ots.yaml` has one row per installed
  component at its exact version; when pip and conda both carry a name
  the pip row is the component and says so in `supersedes`;
  `hazard_review` states what the scanner does not cover (pip-audit
  does not scan conda or OS packages).
