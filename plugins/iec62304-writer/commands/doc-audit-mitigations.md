---
description: Audite la couverture code-vs-mitigation pour les risques résiduels non-acceptable. Lance `tools/audit_mitigations.py` (cadrage statique) puis l'agent `mitigation-auditor` (verdict implementation_status par contrôle). Annote les SRS de mitigation. Optionnel — `--apply` pour basculer les `residual_acceptable` éligibles.
---

## OUTPUT LANGUAGE — STRICT

All artifacts written by this command (`_mitigation_audit.{md,json}`,
`_mitigation_audit_verdicts.md`, SRS frontmatter additions
`implementation_status` / `implementation_evidence` /
`implementation_gap`, `[TODO]` / `[GAP-IMPL]` markers) MUST be written
in **English**, regardless of the user's conversational language or
any global `CLAUDE.md` instruction. Conversational replies MAY follow
the user's language.

L'utilisateur veut **valider, code en main**, si les contrôles cités
par les risques résiduels non-acceptable sont déjà implémentés. À
défaut, l'audit produit un rapport actionnable (verdicts
`absent | partial | implemented` par contrôle) qui ferme le débat
"est-ce que c'est un gap de doc ou un gap de code ?".

Argument optionnel dans `$ARGUMENTS` :

- `--all` : auditer tous les risques (pas seulement
  `residual_acceptable: false`).
- `--apply` : après l'audit, basculer en `residual_acceptable: true`
  les risques que l'agent recommande pour flip (et bump leurs versions).
  Sans ce flag, l'agent annote les SRS mais le risk item reste
  inchangé.
- `--cat RSK,URSK,THR,PRSK` : restreindre aux catégories listées.

## Étapes

### 1. Pré-flight

Vérifier :

```bash
# Python 3
python3 --version 2>&1 || { echo "Python 3 requis"; exit 1; }

# Le repo a été init
if [ ! -d "docs/items" ]; then
  echo "ERROR: docs/items/ absent. Lance /doc-init d'abord." >&2
  exit 1
fi

# Le tool est scaffoldé
if [ ! -f "tools/audit_mitigations.py" ]; then
  echo "ERROR: tools/audit_mitigations.py absent. Lance /doc-init pour le scaffolder, ou /doc-migrate si tu as upgradé le plugin." >&2
  exit 1
fi
```

### 2. Cadrage statique

```bash
python tools/audit_mitigations.py [--all] [--cat <list>]
```

Produit :
- `docs/generated/_mitigation_audit.md` (humain)
- `docs/generated/_mitigation_audit.json` (agent)

Si le script retourne ≠ 0 → afficher la sortie, arrêter.

Si le rapport est vide (0 risque en scope) → afficher "No risk in
scope — `residual_acceptable` is true for all items" et sauter à
l'étape 6.

### 3. Verdict agent

Lancer le sub-agent `mitigation-auditor`. Il :
- lit `_mitigation_audit.json`,
- pour chaque contrôle de chaque risque en scope, lit le code de
  `source:` et juge `implementation_status`,
- annote les SRS concernés (édition additive du frontmatter — ne
  touche aucun champ existant),
- bump version patch + update `updated:` + `Approved → Draft` sur les
  SRS modifiés,
- écrit `docs/generated/_mitigation_audit_verdicts.md`,
- retourne la liste des risques `recommend_flip` / `escalate`.

**Bloquant.** Lire le rapport de l'agent avant l'étape 4.

### 4. Flip des `residual_acceptable` (uniquement si `--apply`)

Pour chaque risque dans la liste `recommend_flip` retournée par
l'agent :

- Vérifier une dernière fois que **tous** les contrôles linkés ont
  bien `implementation_status: implemented` (relecture stricte).
- Si OK : éditer l'item risque :
  - `residual_acceptable: true`
  - bump `version` minor (ex. 1.0.3 → 1.1.0 — c'est un changement de
    sens, pas une reformulation)
  - update `updated:`
  - `Approved → Draft`
  - ajouter au `## Notes` ou `## Changelog` :
    ```markdown
    - YYYY-MM-DD vX.Y.Z : residual flipped to acceptable after
      mitigation-audit verdict (all controls verified implemented:
      <list of SRS IDs>).
    ```

Si la relecture stricte échoue pour un risque (incohérence entre la
recommandation de l'agent et l'état des SRS), NE PAS flipper et logger
l'incohérence dans la synthèse finale.

**Sans `--apply`**, sauter cette étape. Les SRS sont quand même annotés
par l'agent — c'est utile en soi.

### 5. Rebuild

`python tools/build_docs.py`. Les agrégats répercutent les nouveaux
champs `implementation_status` et les éventuels flips de risque.

Si `tools/build_risk_xlsx.py` existe, le relancer aussi pour
rafraîchir le `.xlsx` audit-notified-body.

### 6. Synthèse à l'utilisateur (≤ 14 lignes)

- Risks in scope : N.
- Controls audited : N.
- Verdict breakdown : `implemented=A · partial=B · absent=C · unknown=D`.
- SRS items annotated : N.
- Risks recommended for flip : N.
- Risks flipped (uniquement avec `--apply`) : N.
- Risks requiring RAQA escalation (verdict `unknown`) : N.
- Coverage metrics before/after si lisibles depuis `coverage.json` /
  git history.
- Chemins des rapports :
  - `docs/generated/_mitigation_audit.md`
  - `docs/generated/_mitigation_audit_verdicts.md`

## Garde-fous

- **Lecture seule du code.** Ni tests ni runtime. L'audit est statique
  + agent-driven.
- **Édition additive sur SRS.** L'agent n'ajoute QUE les trois champs
  `implementation_*`. Aucun autre champ touché.
- **Pas de flip sans `--apply`.** Sans le flag explicite, les risk
  items restent intouchés — seules les annotations SRS sont écrites.
- **Strict double-check avant flip.** L'agent recommande, le command
  re-vérifie. Si incohérence, log + skip ce risque.
- **Pas de mass-translation.** Les items existants en français
  gardent leur corps en français ; seuls les champs anglais
  d'audit sont ajoutés.
- **Idempotence.** Relancer le command sans changement de code → 0
  modification d'item, rapport identique au précédent.
- Ne jamais commit/push (sauf demande explicite).
