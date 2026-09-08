---
description: Génère le livrable STDR (Software Test Description and Reports) à partir des items TC/SRS et du fichier test-results.json émis par CI. Sortie dans docs/export/.
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (the STDR Markdown, the optional
`.docx`, the export log) MUST be written in **English**, regardless of
the user's conversational language or any global `CLAUDE.md` instruction.
Conversational replies MAY follow the user's language.

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

Exécute `python tools/build_stdr_export.py` à la racine du repo cible et
rapporte les résultats.

## Étapes

### 1. Vérifications préalables

```bash
# Items TC — bloquant si aucun
if ! ls docs/items/TC/*.md >/dev/null 2>&1; then
  echo "ERREUR : aucun item TC sous docs/items/TC/. Lance /doc-62304 d'abord." >&2
  exit 1
fi

# dt-config.yaml recommandé
if [ ! -f dt-config.yaml ]; then
  echo "Avertissement : dt-config.yaml manquant. Le rapport contiendra des [TODO]."
fi

# test-results.json — informatif
TR_PATH=$(python3 -c "
import sys, pathlib
p = pathlib.Path('dt-config.yaml')
if p.exists():
    import re
    m = re.search(r'test_results_path\s*:\s*(\S+)', p.read_text())
    print(m.group(1) if m else 'test-results.json')
else:
    print('test-results.json')
" 2>/dev/null || echo "test-results.json")

if [ ! -f "$TR_PATH" ]; then
  echo "Info : $TR_PATH absent. Tous les TC apparaîtront en 'not_run'."
  echo "  Pour peupler les résultats, émettre test-results.json depuis CI"
  echo "  (voir scaffold/test-results.example.json pour le format)."
fi
```

### 2. Lancer le build

```bash
python tools/build_stdr_export.py $ARGUMENTS
```

Fallback sur `python3` si nécessaire. Si le script échoue, afficher la
sortie d'erreur sans la masquer.

### 3. Synthèse à l'utilisateur (≤ 12 lignes)

- Chemin du Markdown produit,
- Chemin du `.docx` si produit, ou raison de non-production,
- Nombre de TC actifs inclus,
- Résumé : total / passed / failed / skipped / not_run,
- Nombre de sections [TODO] dans le rendu,
- Chemin du log.

## Arguments optionnels

`$ARGUMENTS` peut contenir :
- `--strict` : exit ≠ 0 si le rendu contient des [TODO] ou si ≥ 1 TC
  est en `failed`. Utile en CI post-run pour bloquer la soumission RAQA.
- `--md-only` : ne pas tenter le rendu `.docx` même si pandoc est dispo.

## Garde-fous

- Ne JAMAIS modifier les items sous `docs/items/`.
- Ne JAMAIS commit/push — sortie locale uniquement.
- Si `dt-config.yaml: approvals` contient encore des `[TODO]` ET le
  livrable est généré → [TODO] visibles dans le rendu, bloquants en `--strict`.
