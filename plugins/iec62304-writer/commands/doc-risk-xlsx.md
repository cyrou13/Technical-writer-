---
description: Génère l'inventaire Excel 4-onglets (Design / Production / Usability / Cybersecurity) équivalent du fichier Avicenna `annex1-RISK-TABLE.xlsx`. Nécessite `openpyxl` (`pip install openpyxl`). Sortie dans `docs/export/`.
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (the .xlsx headers, cell
contents, log) MUST be written in **English**, regardless of the
user's conversational language or any global `CLAUDE.md` instruction.
Conversational replies MAY follow the user's language; written
outputs are English-only.

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

Exécute `python tools/build_risk_xlsx.py` à la racine du repo cible.
Le script lit `dt-config.yaml` et les items sous `docs/items/{RSK,PRSK,
URSK,THR}/`, et écrit le livrable `.xlsx` dans `docs/export/`.

## Étapes

### 1. Vérifications préalables

```bash
# openpyxl requis — vérifier avant de lancer
if ! python3 -c "import openpyxl" 2>/dev/null; then
  echo "openpyxl manquant. Installer : pip install openpyxl"
  echo "Le CSV produit par /doc-risk-export reste disponible comme fallback."
  exit 1
fi

# Au moins une catégorie de risque doit exister
if ! ls docs/items/RSK/*.md docs/items/PRSK/*.md docs/items/URSK/*.md docs/items/THR/*.md >/dev/null 2>&1; then
  echo "ERREUR : aucun item de risque (RSK/PRSK/URSK/THR). Lance /doc-62304 d'abord." >&2
  exit 1
fi
```

### 2. Lancer le build

```bash
python tools/build_risk_xlsx.py
```

Fallback sur `python3` si nécessaire.

### 3. Synthèse à l'utilisateur (≤ 10 lignes)

- Chemin du fichier `.xlsx` produit,
- Nombre de risques par onglet : Design / Production / Usability / Cybersecurity,
- Nombre de cellules surlignées rouge (risque résiduel non-acceptable) — alerte si > 0,
- Chemin du log : `docs/export/<id>-<v>-risk-xlsx.log`,
- Rappel : ce fichier est destiné à l'**audit** du notified body. Il est
  complémentaire au Risk Report (`.md` / `.docx` narratif) produit par
  `/doc-risk-export`.

## Argument optionnel

`$ARGUMENTS` peut contenir `--strict` : exit ≠ 0 si ≥ 1 risque a
`residual_acceptable: False`. Utile en CI avant submission RAQA.

## Garde-fous

- Ne JAMAIS modifier les items sous `docs/items/`.
- Ne JAMAIS commit/push — sortie locale.
- Ne PAS écraser un .xlsx édité à la main dans `docs/export/` : si
  l'utilisateur a annoté manuellement le fichier, lui recommander de
  le renommer avant de relancer (la regen écrase la cellule sans avertir).
