---
name: srs-extract
description: Extract software requirements (IEC 62304 §5.2) from TypeScript/JavaScript and Python code into SRS items — with requirement kinds, declared parameters, numbered criteria and normative-only text. Invoke to generate or enrich items in docs/items/SRS/.
---

## OUTPUT LANGUAGE — STRICT

Any SRS item produced while applying this skill (frontmatter values,
body sections, acceptance criteria, `[TODO]`/`[GAP-62304]` markers)
MUST be written in **English**, regardless of the user's conversational
language or any global `CLAUDE.md` instruction.

# SRS — extracting requirements from the code

## Sources of requirements, most reliable first

1. **Explicit tags** — TS/JS `// @req SRS-AUTH-001 …`, Python
   `# @req SRS-AUTH-001 …` or docstring `:req SRS-AUTH-001:`. The ID in
   the tag is authoritative.
2. **Public API** — exported functions and classes, `__all__`, HTTP
   routes (FastAPI, Express, Next.js handlers, NestJS controllers), CLI
   entry points (`argparse`, `click`, `commander`, `yargs`).
3. **Explicit error cases** — exception classes and their messages;
   `assert`, `invariant`, schema validation (`zod.parse`, Pydantic).
4. **Tests** — every `describe` / `it` / `test_*` states an expected
   behaviour; usually too fine, group them.
5. **Configuration and schemas** — Zod / Pydantic / JSON Schema, required
   environment variables, constant tables. **This is where the
   parameters come from.**

## Grouping heuristics

- One REST endpoint = one SRS (more if methods carry separate semantics).
- One CLI command = one SRS.
- One public class with a clear business responsibility = one SRS.
- N tests exercising the same rule = one SRS.

An SRS is an **observable property of the system**, not an implementation
detail.

## Requirement kind

Set `kind:` on every SRS. Ask "what would a reviewer look for this
under?":

| Evidence in the code | kind |
|---|---|
| handler / algorithm producing an output | `functional` |
| timeout, budget, tolerance, accuracy assertion, frame/size limit | `performance` |
| DICOM / HL7 / REST / file-format contract, external system call | `interface` |
| OS / runtime / GPU / memory check, OTS pin | `platform` |
| UI rule, label, display convention, IEC 62366 control | `usability` |
| guard derived from a RSK / PRSK (`links.mitigates`) | `safety` |
| authentication, integrity, signature, audit control from a THR | `security` |
| installer, updater, decommissioning, audit record, backup | `process` |

A mitigation SRS keeps the kind of its control (`safety` for RSK,
`security` for THR, `usability` for URSK).

## Parameters

Every literal the requirement quotes — a threshold, a series number, a
timeout, a default, a limit — is declared in `parameters:`:

```yaml
parameters:
  - name: min_frames
    value: 8                              # a list value is a list: [4, 6, 8, 10]
    unit: null
    settable: false
    interval: null
    source: ctperfusion.qc.frames.MIN_FRAMES   # prose or a dotted symbol — never a path
references: [DEFUSE3]                       # ids of dt-config.yaml `references`
```

Before declaring, `grep -r "name: <candidate>" docs/items/` — if the name
exists, **another item owns it**: reference it by name in your text and
do not redeclare it; if the code holds a different value, stop and
report the conflict. Quote the parameter in the text as
`` `min_frames` (8) ``. **Every frozen parameter you declare is described
in this requirement's text** — a registry row no requirement explains is
a defect; conversely a constant that two names describe
(`min_slice_visits` / `dynamic_min_visits_per_location`) is one
parameter. The registry is rendered in SRS §4.1 (and SDD §3.8), so
`source` is what a customer may read: `ctperfusion.common.config`, or
"configuration schema", not `ctperfusion/common/config.py`.

## References

Every clinical threshold (a DEFUSE-3 cut, an rCBF < 30 % core
definition) and every algorithm (oSVD, an oxygen-transport model) names
its source: an id of `dt-config.yaml: references` (`[{id, citation}]`)
in the item's `references:` list, quoted in the text as `[DEFUSE3]`.
The exporter renders one References section from the ids in use. A
requirement that says "the map published comparative studies found
accurate" with no id is unsourced.

## Body of an SRS item

```markdown
<!-- Exported (SRS). Normative: present-tense behaviour only. -->
## Description

The system **shall** <behaviour> when <condition>, and **shall**
<guarantee> in all cases.

<!-- Exported (SRS). Numbered, measurable behaviour, with the number. -->
## Acceptance criteria

1. <criterion, e.g. "A study with fewer than `min_frames` (8) frames is rejected with status code `QC_TOO_FEW_FRAMES`.">
2. <criterion with a tolerance taken from the test: "the core volume is within `core_volume_tol` (2 mL) of the reference">

<!-- Internal. -->
## Notes

<where the threshold comes from, what was considered and rejected>

<!-- Internal. -->
## Open questions

- <what the code does not answer>

<!-- Internal. -->
## History

- YYYY-MM-DD v1.0.0 — created from <source file>.
```

## Normative text rules

- `shall` + measurable criterion. No "fast", "easy", "intuitive".
- Present tense, present behaviour. **No dates, no decisions, no
  "re-assessed", no "since version", no commit hashes** — those go to
  `## History`.
- **No code paths, no test paths, no function names as the subject.**
  "The system shall reject …", not "`frames.py` rejects …". `source:` in
  the frontmatter carries the path.
- **No competitor names.** A requirement is not "as in <competitor>".
- **No tick-boxes.** Criteria are `1.`, `2.`, …
- Every number quoted is a declared parameter or a value of the standard
  it cites.
- **A criterion is a behaviour with a number.** Never a status
  ("confirmed by RAQA"), a test id ("TC-AIF-013 stays an expected
  failure"), a decision id, an "engineering action", a "placeholder
  until …", a statement about the module's source code. A tolerance is
  the number the test asserts — never "about 1.1", "~85 %", "small
  margin", "within tolerance", "non-worse".
- **Measurements are evidence, bounds are criteria.** "Measured peak
  20.6 GB" and "about 25 s on the 40-frame study" go to `## Notes`; the
  criterion is "peak resident memory at most `max_rss` (24 GB)". A
  limit set equal to the maximum of three measurements is a
  measurement, not a bound.
- **One glossary term per concept**, verbatim from the `## glossary`
  anchor; the labeling vocabulary wins ("Tmax > 6 s region", not also
  "hypoperfusion region" and "critically hypoperfused region"; the
  time-to-maximum map is not "arrival delay" in one item and "not an
  arrival delay" in another).
- **Kind matters**: a QC plausibility rule is `functional` or
  `performance`, not `interface`; a `safety` kind declared in the
  document and assigned to no requirement is a visible hole — either
  link the mitigation SRS to their RSK or say why there is none.

## Anti-patterns

- "The system shall be performant" — not measurable.
- "The system shall use PostgreSQL" — design (SDS), not requirement.
- Paraphrasing code as pseudo-code — describe behaviour, not
  implementation.
- "Threshold lowered from 10 to 5 after the ISLES sweep" in Description —
  that is History.
- "`- [ ] Tmax > 6 s`" — tick-box reads as an unverified status.

## Output

1. Check whether an item already cites the same `source:` file — if so,
   **update** it under the idempotence rules of `items-store`; never
   create a duplicate.
2. Otherwise create `docs/items/SRS/<ID>.md` with the next free `NNN` in
   the domain (respecting `dt-config.yaml: id_format`).
3. `source:` paths are relative to the project root; in multi-repo mode
   prefix them with the component name (`front/src/…`, `back/api/…`).
4. Leave `links:` empty except `implements` toward a MAP item when the
   upstream requirement is known — SDS→SRS and TC→SRS links are set by
   the other agents.

## Labeling vs specification

Read the labeling anchors of `docs/dt-clinical-context.md`
(`intended-use`, `warnings-and-precautions`) before writing. When a
warning names an output the requirements forbid, when the intended use
omits the indication the thresholds encode (stroke cuts with no stroke
indication), when the labeling names a configuration no requirement
specifies — **do not edit the labeling and do not bend the
requirement**: report it in your return as a DECISION-level finding for
the product owner / RAQA (`submission-readiness` DEC-1/2) and leave a
line in `## Open questions`.

## When in doubt

Write `[TODO …]` in `## Notes` or `## Open questions` — never in
`## Description` or `## Acceptance criteria` — and list the question.
**Do not invent.**
