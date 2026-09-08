---
name: srs-export
description: Génère le livrable SRS habillé pour le dossier technique (cover page signataires, revision history, project references, sections cliniques inlinées, table de traçabilité §3) à partir des items et de `dt-config.yaml`. À invoquer pour produire `docs/export/<identifier>-SRS.md` (+ `.docx` optionnel via pandoc) après que les items SRS / MAP sont stables.
---

## OUTPUT LANGUAGE — STRICT

Every artifact produced while applying this skill (the exported SRS
Markdown, the optional `.docx` produced via pandoc, all section
headers and labels) MUST be written in **English**, regardless of the
user's conversational language or any global `CLAUDE.md` instruction.
The framing sections come verbatim from `docs/dt-clinical-context.md`
which is also authored in English.

## Modes and release gate (contract of skill `submission-readiness`)

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

# Dossier technique — SRS export

Ce skill produit un livrable de **dossier technique** au format
attendu par les RAQA medtech (Avicenna-style) à partir des items
stockés sous `docs/items/` et des métadonnées QMS-side capturées dans
`dt-config.yaml` + `docs/dt-clinical-context.md`.

## Pourquoi un livrable distinct de `10_SRS.md`

`docs/generated/10_SRS.md` (produit par `/doc-build`) est un **agrégat
technique** plat des items SRS, optimisé pour la revue de l'équipe
dev. Le livrable d'export, lui, est un **document QMS-ready** :

- page de garde signée (Written / Verified / Approved by),
- historique de révisions du document lui-même,
- introduction normative (overview, glossaire, project references,
  conventions),
- §2.1 introduction avec **intended use**, **warnings**, **connected
  devices** copiés depuis `dt-clinical-context.md`,
- corps §2.2+ : items SRS regroupés par `(SUITE × APP × DOMAIN)`,
- §3 REQUIREMENTS TRACEABILITY : table SRS → MAP parent.

Le livrable est ce qu'on **envoie au notified body** ; `10_SRS.md` est
ce qu'on **regarde en daily**.

## Inputs requis

| Input | Source | Obligatoire | Si absent |
|---|---|---|---|
| Items SRS | `docs/items/SRS/*.md` | oui | erreur |
| Items MAP | `docs/items/MAP/*.md` | non | §3 sans MAP parent column |
| Config QMS | `dt-config.yaml` | non | valeurs par défaut + `[TODO]` |
| Sections narratives | `docs/dt-clinical-context.md` | non | sections vides + `[TODO]` |
| Introductions des thématiques | `docs/srs-domain-introductions.md` (`## <DOMAIN>`) | non | thématique sans introduction |
| Template Word | `dt-config.yaml: rendering.reference_docx` — produit par `tools/make_reference_docx.py --from <livrable approuvé.docx>` | non | rendu .docx avec style pandoc par défaut |

## Outputs

| Fichier | Format | Toujours produit |
|---|---|---|
| `docs/export/<identifier>-SRS.md` | Markdown standalone | oui |
| `docs/export/<identifier>-SRS.docx` | Word | si pandoc installé |
| `docs/export/<identifier>-export.log` | rapport de génération | oui |

`<identifier>` = `dt-config.yaml: document.identifier` (ex.
`AV-DP-CINA-CSP-10-006`). La version label (V01, V02…) est appendée
automatiquement.

## Structure du livrable

```
COVER PAGE
  Title (from document.title)
  Identifier (from document.identifier + version_label)
  Date
  Signatures table (Written/Verified/Approved by)

REVISION HISTORY TABLE
  one row per entry in dt-config.yaml: revision_history

TABLE OF CONTENTS

§1 INTRODUCTION
  §1.1 Document overview        ← dt-clinical-context: ## document-overview
  §1.2 Abbreviations & Glossary ← dt-clinical-context: ## abbreviations + ## glossary
  §1.3 Project References       ← dt-config.yaml: project_references (table)
  §1.4 Conventions              ← derived from dt-config.yaml: id_format

§2 REQUIREMENTS
  §2.1 Introduction
    §2.1.1 Device description    ← (handled by clinical context section that lists it)
    §2.1.2 Intended use          ← dt-clinical-context: ## intended-use
    §2.1.3 Warnings & precautions ← dt-clinical-context: ## warnings-and-precautions
    §2.1.4 Connected devices     ← dt-clinical-context: ## connected-devices

  §2.2 Functionalities — for each DOMAIN extracted from SRS items:
    §2.2.<k> <Domain pretty name>
      <Introduction of the area>   ← docs/srs-domain-introductions.md: ## <DOMAIN> (if written)
      For each SRS item in that domain (sorted by NNN) — the house idiom:
        <ID>                       grey band, bold navy      (style RequirementId)
        <Title>                    italic navy, indented     (style RequirementTitle)
        <Description paragraph>    blue                      (style RequirementBody)
        V<major>.<minor>           the item's own version    (style RequirementVersion)
        | # | Acceptance criterion |        compact table (when the item has criteria)
        | Parameter | Value | Unit | Settable [| Interval] |   compact table (when the item declares parameters)
      No heading per requirement, no attribute row: kind/priority/verification
      are tabulated in §3 and the non-functional kinds listed from §2.3.

  §2.x Personnel and training   ← dt-clinical-context: ## personnel-and-training
  §2.x Packaging                ← dt-clinical-context: ## packaging

§3 REQUIREMENTS TRACEABILITY
  Table: SRS ID | SRS Title | MAP Parent ID | MAP Title
  Sorted by SRS ID. Rows where SRS has no parent get "(no parent)" — flagged in log.
```

## Règles d'omission

- Item SRS avec `status: Deprecated` → **exclu** du corps (§2.2+) mais
  apparaît en annexe (« Deprecated requirements ») avec la dernière
  version connue.
- Item MAP avec `status: Deprecated` → exclu de §3, mais les SRS qui
  pointaient encore vers lui sont flaggés en log.
- Section `## X` absente de `dt-clinical-context.md` → l'export
  insère `[TODO X]` à sa place et logge un warning.

## Conventions de domaine et pretty-names

Le **pretty name** d'un domaine (titre de la sous-section §2.2.k) est
choisi ainsi :

1. Si `dt-config.yaml: domains` contient une entrée `{code: ACQ, name:
   "Acquisition limitations"}`, utiliser ce mapping.
2. Sinon, dériver depuis le code domaine : `ACQ` → `Acquisition`,
   `CAD` → `Detection`, `EXE` → `Execution`, `ITR` → `Image triage` —
   logger le mapping appliqué.
3. Si pas de mapping plausible : utiliser le code domaine tel quel et
   logger un `[TODO domain_pretty_name: ACQ]` dans `dt-config.yaml`.

## Look & feel du .docx

Le modèle `docs/templates/avicenna-reference.docx` est construit par
`tools/make_reference_docx.py --from <SRS approuvé d'un autre produit CINA>` :
corps vidé, en-tête tokenisé (`{{PRODUCT}}`, `{{DOCTITLE}}`, `{{DOCID}}`,
`{{VERSION}}` — substitués par `_lib.docx_reference_for()`), jeu de styles complété
avec ceux de pandoc (sans eux LibreOffice rend les tableaux vides), titres au ras
de la marge (les exporteurs numérotent dans le texte), chapitre sur nouvelle page,
style `Table` à bordures simples et en-tête gris, quatre styles `Requirement*`.
Largeur et centrage des tableaux ne peuvent pas venir du modèle :
`_lib.finish_docx()` les fixe après pandoc (pleine largeur du texte, centré,
lignes insécables). Tous les exporteurs l'appellent.

## §4.1 — paramètres sans provenance code

La table des paramètres figés/bornés du SRS n'a pas de colonne « Source » (classe,
module) : une spécification se rédige avant le code. La provenance reste dans
`parameters[].source` du store et n'est rendue que dans le registre §3.8 du SDD
(`render_parameters_table(..., with_source=False)` côté SRS).

## Lint `altitude` (export SRS, `--release`)

Refuse un énoncé de plus de 90 mots, un énoncé portant une liste ou un `shall`,
plus de 8 critères d'acceptation. Les exigences `kind: process` sont exemptées de
la limite de mots. Règle de rédaction : agent `requirements-writer`, « Altitude ».

## Rendu .docx (optionnel)

Si `dt-config.yaml: rendering.reference_docx` est défini ET pandoc
est installé :

```bash
pandoc docs/export/<identifier>-SRS.md \
  --reference-doc=<reference_docx> \
  --toc --toc-depth=3 \
  -o docs/export/<identifier>-SRS.docx
```

Si pandoc absent → produire le `.md` seulement et logger un warning
non-bloquant. **Ne jamais** échouer l'export pour absence de pandoc.

### Diagrammes mermaid

Les blocs ```` ```mermaid ```` du livrable sont rendus en PNG et remplacés par
des images dans une **copie** du markdown que seul pandoc voit ; le `.md` livré
garde ses blocs mermaid. Sans ce rendu, pandoc recopie la source du diagramme
dans le `.docx` comme un bloc de code monospace — le relecteur lit
`participant P as Pipeline` en Courier au lieu d'un schéma.

Prérequis : `mermaid-cli` (`npm i -g @mermaid-js/mermaid-cli`). Variables
d'environnement reconnues :

| Variable | Rôle |
|---|---|
| `MMDC` | chemin du binaire `mmdc` si absent du `PATH` |
| `MERMAID_PUPPETEER_CONFIG` | config puppeteer JSON — typiquement `{"args": ["--no-sandbox"]}` en conteneur ; à défaut `tools/puppeteer.json` est lu s'il existe |

Absent → les blocs restent tels quels, une ligne INFO est loggée et l'export
n'échoue pas. Un diagramme qui ne compile pas est laissé en bloc de code : il ne
coûte pas les autres.

## Garde-fous

- L'export **ne modifie aucun item** sous `docs/items/`. Lecture seule.
- L'export **ne touche pas** `docs/generated/` (sortie de `/doc-build`).
- L'export écrit **uniquement** dans `docs/export/`.
- Idempotent : ré-exécuter `/doc-srs-export` deux fois de suite avec des
  items inchangés produit le même fichier byte-pour-byte (sauf la date
  de génération si présente dans le rendu — préférer une date stable
  depuis `dt-config.yaml: document.date`).
