---
description: Génère le livrable Software Design Description (équivalent Avicenna `AV-DP-XXX-SDD.docx`) — cover, intro, architecture, design détaillé, security assessment, COTS control. Sortie dans `docs/export/`.
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (the SDD Markdown, the
optional `.docx`, the export log) MUST be written in **English**,
regardless of the user's conversational language or any global
`CLAUDE.md` instruction. Conversational replies MAY follow the user's
language; written outputs are English-only.

## Modes and release gate

| Mode | Cover | Open points | `[TODO]` markers | Gate |
|---|---|---|---|---|
| (none) / `--strict` | `WORKING DRAFT — generated <date>` | omitted | yellow `<mark>` for the QMS author (`--strict` exits non-zero on any) | reported, never blocking |
| `--internal` | `WORKING DRAFT — generated <date>` | appended as a register | yellow `<mark>` | reported, never blocking |
| `--release` | document identifier (`documents.<x>`), version label, date and signatures from `dt-config.yaml` | never | refused | the gate of skill `submission-readiness` (DC-1…4, TL-1…14, SL-1…14) runs first; the export is **refused** and no file is written when any rule fails; DEC-1/2 are reported, never blocking |

`--release` and `--internal` are mutually exclusive. The rendering
follows the contract of skill `items-store`: internal sections
(`## Notes`, `## Open questions`, `## History`, a legacy
`## Changelog`) and HTML comments are stripped, each item is rendered
once, no per-item version is printed, and the unresolved-anomalies
appendix (a dated record) is exported in every mode while the
open-points register is `--internal` only. The scaffolded
`tools/build_*_export.py` are the working-draft generation and do not
implement `--release`; the reference exporters synced from the CINA-CTP
repository do (`tools/README.md`). Without them, `--release` states
that no deliverable can be produced.

Exécute `python tools/build_sdd_export.py` à la racine du repo cible.
Le script lit `dt-config.yaml`, `docs/dt-clinical-context.md` et les
items SDS / SRS / THR sous `docs/items/`, et écrit le livrable dans
`docs/export/`.

## Étapes

### 1. Vérifications préalables

```bash
if [ ! -f dt-config.yaml ]; then
  echo "Avertissement : dt-config.yaml manquant. Lance /doc-init pour le scaffolder."
fi
if [ ! -f docs/dt-clinical-context.md ]; then
  echo "Avertissement : docs/dt-clinical-context.md manquant."
fi
if ! ls docs/items/SDS/*.md >/dev/null 2>&1; then
  echo "ERREUR : aucun item SDS sous docs/items/SDS/. Lance /doc-62304 d'abord." >&2
  exit 1
fi
```

### 2. Lancer le build

```bash
python tools/build_sdd_export.py
```

Fallback sur `python3` si nécessaire.

### 3. Synthèse à l'utilisateur (≤ 12 lignes)

- Chemin du Markdown produit (`docs/export/<id>-<v>-SDD.md`),
- Chemin du `.docx` si produit, ou raison de non-production,
- Nombre d'items SDS / SRS / THR inclus,
- Nombre de `[TODO]` détectés (yellow markers) — alerter si > 0,
- Nombre de dépendances COTS détectées auto (§5.2) ou indication
  qu'aucun manifeste n'a été trouvé,
- Rappel : les sections narratives en yellow TODO peuvent être
  remplies soit dans `docs/dt-clinical-context.md`, soit via
  `dt-config.yaml: external_resources.<anchor>` qui pointe un fichier
  externe (Obsidian, QMS),
- Chemin du log.

## Argument optionnel

`$ARGUMENTS` peut contenir :
- `--strict` : exit 1 si ≥ 1 `[TODO]` reste dans le rendu. Utile en
  CI avant submission RAQA.
- `--md-only` : skip le rendu `.docx`.

## Garde-fous

- Ne JAMAIS modifier les items sous `docs/items/`.
- Ne JAMAIS commit/push — sortie locale.
- Si `dt-config.yaml: approvals` contient encore des `[TODO]` ET le
  livrable est généré → logger un warning bloquant en mode `--strict`.
