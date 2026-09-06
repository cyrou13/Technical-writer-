---
description: Génère le livrable SRS habillé pour le dossier technique (cover, signatures, références, sections cliniques, traçabilité §3) à partir des items et de `dt-config.yaml`. Sortie dans `docs/export/`.
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (the exported SRS Markdown, the
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

Exécute `python tools/build_srs_export.py` à la racine du repo cible et
rapporte les résultats. Le script lit `dt-config.yaml`,
`docs/dt-clinical-context.md` et les items sous `docs/items/`, et
écrit le livrable dans `docs/export/`.

## Étapes

### 1. Vérifications préalables

```bash
# dt-config.yaml requis (le script peut tourner sans, mais on prévient l'utilisateur)
if [ ! -f dt-config.yaml ]; then
  echo "Avertissement : dt-config.yaml manquant. Lance /doc-init pour le scaffolder."
  echo "L'export va utiliser des valeurs par défaut et insérer [TODO] partout."
fi

# dt-clinical-context.md fortement recommandé
if [ ! -f docs/dt-clinical-context.md ]; then
  echo "Avertissement : docs/dt-clinical-context.md manquant. Les sections cliniques"
  echo "(intended use, warnings, connected devices) seront vides dans l'export."
fi

# Items SRS — bloquant si aucun
if ! ls docs/items/SRS/*.md >/dev/null 2>&1; then
  echo "ERREUR : aucun item SRS sous docs/items/SRS/. Lance /doc-62304 d'abord." >&2
  exit 1
fi
```

### 2. Lancer le build

```bash
python tools/build_srs_export.py
```

Si `python3` est nécessaire à la place de `python`, ré-essayer
automatiquement. Si le script échoue : afficher la sortie d'erreur,
ne pas masquer.

### 3. Rendu .docx (si applicable)

Le script `build_srs_export.py` invoque pandoc lui-même si
`dt-config.yaml: rendering.reference_docx` est défini et pandoc est
disponible. Pas d'action côté Claude.

### 4. Synthèse à l'utilisateur (≤ 12 lignes)

- Chemin du livrable Markdown produit (`docs/export/<identifier>-SRS.md`),
- Chemin du `.docx` si produit, ou raison de non-production (pandoc
  absent, reference_docx non défini),
- Nombre d'items SRS inclus / exclus (deprecated),
- Nombre de SRS sans parent MAP (alerter si > 0 — indique une traçabilité incomplète),
- Sections `[TODO]` détectées dans le rendu (alerter si > 0),
- Chemin du log : `docs/export/<identifier>-export.log`.

## Argument optionnel

`$ARGUMENTS` peut contenir :
- `--strict` : exit ≠ 0 si l'export contient des `[TODO]` ou des SRS
  sans parent MAP. Utile en CI avant submission RAQA.
- `--md-only` : ne pas tenter le rendu .docx même si pandoc est dispo.

## Garde-fous

- Ne JAMAIS modifier les items sous `docs/items/` ni les sorties de
  `/doc-build` sous `docs/generated/`.
- L'export est **complémentaire** à `/doc-build`, pas un remplacement —
  `/doc-build` produit les agrégats internes, `/doc-srs-export` produit le
  livrable QMS.
- Ne JAMAIS commit ou push automatiquement — la sortie reste locale.
- Si `dt-config.yaml: approvals` contient encore des `[TODO]` ET le
  livrable est généré → logger un warning bloquant en mode `--strict`.
