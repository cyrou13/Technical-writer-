---
name: traceability-matrix
description: Build the MAP ↔ SRS ↔ SDS ↔ TC traceability matrix from the frontmatter links and compute coverage, counting only tests that exist. Invoke after SRS/SDS/TC items are created.
---

## OUTPUT LANGUAGE — STRICT

Any traceability artifact produced while applying this skill
(`40_traceability.md`, coverage commentary, gap annotations) MUST be
written in **English**, regardless of the user's conversational
language or any global `CLAUDE.md` instruction.

# Traceability matrix — construction and reading

## Source of truth

Links live **only** in the `links:` block of each item (skill
`items-store`). This skill reads and aggregates; it never writes a link.

## Aggregation

For each `SRS-XYZ`:

- `implementedBy` = { SDS whose `links.implements` contains `SRS-XYZ` }
- `verifiedBy` = { TC whose `links.verifies` contains `SRS-XYZ` **and**
  whose `test_id` resolves to an existing test (SL-4) }
- `upstream` = `links.implements` of the SRS toward MAP items

Metrics (class A — useful, not mandatory):

- `implementation_rate` = #{SRS with ≥ 1 implementedBy} / #SRS
- `verification_rate` = #{SRS with ≥ 1 verifiedBy} / #SRS
- `planned_only` = SRS whose only TC are planned (`test_id: "[TODO]"`)
  — reported separately, never folded into `verification_rate`
- `orphan_sds`, `orphan_tc`, `unparented_srs` (no MAP upstream when MAP
  items exist), `deprecated_links`
- per `kind`: count of SRS and verification rate, so an empty kind
  (no `performance` requirement, say) is visible

## Output

`docs/generated/40_traceability.md`:

```markdown
# Traceability matrix

## Summary
| Metric | Value |
|---|---|
| Requirements (SRS) | 42 |
| Implementation coverage | 38/42 (90 %) |
| Verification coverage (existing tests) | 33/42 (79 %) |
| Verified by planned tests only | 2 |

## By requirement kind
| kind | SRS | verified |
|---|---|---|

## MAP → SRS → SDS → TC
| MAP | SRS | Title | kind | SDS | TC | Status |
|---|---|---|---|---|---|---|

## Orphans
### SDS without requirement
### TC without requirement
### SRS without upstream MAP
```

`docs/generated/coverage.json` (machine-readable):

```json
{
  "srs_count": 42,
  "implementation_rate": 0.90,
  "verification_rate": 0.79,
  "planned_only": ["SRS-…"],
  "by_kind": {"functional": {"count": 30, "verified": 26}},
  "orphans": {"sds": [], "tc": [], "srs_unparented": []}
}
```

## Implementation

`tools/build_docs.py` computes the matrix for the working build; the
reference exporters render the customer-facing matrix inside the SRS and
STDR deliverables. If the matrix logic changes, change both.
