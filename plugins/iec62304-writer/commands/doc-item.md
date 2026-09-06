---
description: Creates or updates a single documentation item (MAP/SRS/SDS/TC/RSK/PRSK/THR/USC/URSK) from the templates, with a conforming frontmatter. Usage — /doc-item SRS-AUTH-001 [title]
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (every file under `docs/`, item
frontmatter values such as `title`/`description`, body content,
`[TODO]`/`[GAP-...]` markers, and aggregated reports) MUST be written
in **English**, regardless of the user's conversational language or
any global `CLAUDE.md` instruction. Conversational replies to the user
MAY follow the user's language; written outputs are English-only.

The user wants to create or edit **one** documentation item.

`$ARGUMENTS` is `<ID> [optional title]`.

## Steps

1. Parse: `ID` (form `<CAT>-<DOMAIN>-<NNN>`, or the `id_format` of
   `dt-config.yaml`), the rest is the title.

2. Malformed `ID` → explain the format (skill `items-store`) and stop.

3. Category from the prefix: `MAP`, `SRS`, `SDS`, `TC`, `RSK`, `PRSK`,
   `THR`, `USC`, `URSK`.

4. Target: `docs/items/<CAT>/<ID>.md`.

5. File exists → read it, propose the requested change, apply it under
   the `items-store` idempotence rules: `updated` set, `version` bumped,
   `Approved` → `Draft`, one line added at the top of `## History`
   (create the section at the end if absent; rename a legacy
   `## Changelog` header to `## History` while there). **Never write a
   date, a decision or a change note into a normative section**; never
   turn a numbered criterion into a tick-box.

6. Otherwise **create** from `docs/templates/<cat-lower>-item.template.md`
   (keep the per-section header comments) and pre-fill:
   - `id`, `title`, `created`, `updated` (today),
   - `version: 1.0.0` (or `baseline_version` in design mode),
     `status: Draft`,
   - SRS: `kind` (ask if not inferable), `parameters: []`,
   - `source:`, `links:` empty,
   - body: template sections, `[TODO]` only in `## Notes` and
     `## Open questions`, a first `## History` line.

7. Show the path and the sections to complete; remind that every
   constant quoted must be declared in `parameters:` and that
   third-party components are named by their `docs/ots.yaml` key.

## Rules

- **Never reuse** an allocated ID, even if the file was deleted: check
  every `docs/items/**` frontmatter.
- Do not create a category folder without confirmation when it does not
  exist yet.
