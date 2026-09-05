---
description: Scaffolds the current repository for the 62304 pipeline — copies tools/build_docs.py, docs/templates/, docs/test_plan_intro.md, docs/ots.yaml, docs/dt-clinical-context.md (six required sections, empty), dt-config.yaml, and creates docs/items/. Run once per target repository.
---

The user wants to initialise a repository with the IEC 62304
documentation pipeline.

`$ARGUMENTS` may contain:
- `--update` — replace `tools/build_docs.py` even if it exists.
- `--with-examples` — copy the example items into `docs/items/`.

## What the scaffold establishes

The store follows the contract of skills `items-store` and
`submission-readiness`: normative vs internal sections, `kind` and
`parameters` on SRS/SDS, `## History` (never `## Changelog`), numbered
criteria, third-party components in `docs/ots.yaml` only, the
cybersecurity architecture in four views of `docs/dt-clinical-context.md`,
and a document-control block in `dt-config.yaml` that the `--release`
export checks. The reference exporters are **not** copied — see
`scaffold/tools/README.md`.

## Steps

### 1. Pre-checks

**Git is not a prerequisite.** The detection below is informational.

```bash
if [ -d .claude-plugin ]; then
  echo "ERROR: this directory is the plugin itself. Run /doc-init in the TARGET repository." >&2
  exit 1
fi

GIT_REPOS=()
if git rev-parse --git-dir >/dev/null 2>&1; then
  GIT_REPOS+=("$(pwd) (top-level)")
fi
while IFS= read -r d; do
  GIT_REPOS+=("${d%/.git}/")
done < <(find . -maxdepth 3 -type d -name .git 2>/dev/null | grep -v "^\./\.git$" || true)

if [ ${#GIT_REPOS[@]} -eq 0 ]; then
  echo "Info: no git repository detected. Scaffolding continues."
else
  echo "Git repositories detected:"
  printf '  - %s\n' "${GIT_REPOS[@]}"
  if [ ${#GIT_REPOS[@]} -gt 1 ]; then
    echo "Multi-repo mode: agents prefix source: paths with the component name (e.g. 'front/src/auth/oauth.ts')."
  fi
fi
echo "OK — target repository: $(pwd)"
```

**Strict instruction:** whatever the git detection prints, **go to
step 2 without asking**. The only stop is the explicit
`[ -d .claude-plugin ]` error.

### 2. Copy the scaffold

```bash
ARGS="$ARGUMENTS"
UPDATE=0
WITH_EXAMPLES=0
case " $ARGS " in *" --update "*) UPDATE=1 ;; esac
case " $ARGS " in *" --with-examples "*) WITH_EXAMPLES=1 ;; esac

CATS="MAP SRS SDS TC RSK PRSK THR USC URSK"
mkdir -p tools docs/templates
for cat in $CATS; do mkdir -p "docs/items/$cat"; done

CREATED=()
SKIPPED=()

# build_docs.py — overwritten only with --update
if [ ! -f tools/build_docs.py ] || [ "$UPDATE" = "1" ]; then
  cp "${CLAUDE_PLUGIN_ROOT}/scaffold/tools/build_docs.py" tools/build_docs.py
  CREATED+=("tools/build_docs.py")
else
  SKIPPED+=("tools/build_docs.py (exists — use --update to replace)")
fi

# tools/README.md — where the reference exporters live; never overwritten
if [ ! -f tools/README.md ]; then
  cp "${CLAUDE_PLUGIN_ROOT}/scaffold/tools/README.md" tools/README.md
  CREATED+=("tools/README.md")
fi

# Templates — never overwritten
for tpl in map-item srs-item sds-item tc-item rsk-item prsk-item thr-item usc-item ursk-item; do
  src="${CLAUDE_PLUGIN_ROOT}/scaffold/docs/templates/${tpl}.template.md"
  dst="docs/templates/${tpl}.template.md"
  if [ ! -f "$dst" ]; then
    cp "$src" "$dst"; CREATED+=("$dst")
  else
    SKIPPED+=("$dst (exists)")
  fi
done

# Hand-maintained files — NEVER overwritten
for f in docs/test_plan_intro.md docs/ots.yaml docs/dt-clinical-context.md dt-config.yaml; do
  if [ ! -f "$f" ]; then
    cp "${CLAUDE_PLUGIN_ROOT}/scaffold/$f" "$f"; CREATED+=("$f")
  else
    SKIPPED+=("$f (exists — hand-maintained)")
  fi
done

# .gitkeep per category
for cat in $CATS; do
  if [ ! -f "docs/items/$cat/.gitkeep" ]; then
    : > "docs/items/$cat/.gitkeep"; CREATED+=("docs/items/$cat/.gitkeep")
  fi
done

# Examples
if [ "$WITH_EXAMPLES" = "1" ]; then
  for cat in $CATS; do
    for src in "${CLAUDE_PLUGIN_ROOT}/examples/$cat"/*.md; do
      [ -f "$src" ] || continue
      dst="docs/items/$cat/$(basename "$src")"
      if [ ! -f "$dst" ]; then cp "$src" "$dst"; CREATED+=("$dst"); else SKIPPED+=("$dst (exists)"); fi
    done
  done
fi

# .gitignore — append without duplicating
touch .gitignore
for line in "__pycache__/" "*.pyc" ".venv/" "venv/"; do
  if ! grep -qxF "$line" .gitignore; then
    echo "$line" >> .gitignore; CREATED+=(".gitignore (+ $line)")
  fi
done

echo; echo "=== Created ==="; printf '  %s\n' "${CREATED[@]}"
echo; echo "=== Skipped ==="; printf '  %s\n' "${SKIPPED[@]}"
```

### 3. Summary to the user

8 lines or fewer:
- files created vs skipped,
- key locations (`tools/build_docs.py`, `docs/items/`,
  `docs/templates/`, `docs/ots.yaml`, `docs/dt-clinical-context.md`,
  `dt-config.yaml`),
- what to fill by hand: `dt-config.yaml` (document identifier, version
  label, date, `revision_history`, `lint.forbidden_terms`),
  `docs/test_plan_intro.md`, the six empty sections of
  `docs/dt-clinical-context.md` (the architecture-writer and
  security-analyst fill them from the code, a human reviews),
- next step: `/doc-62304`, or `/doc-item SRS-XXX-001 "…"`,
- the reference exporters must be synced from the CINA-CTP repository
  (`tools/README.md`) before `/doc-build --release` can produce a
  deliverable.

## Guard rails

- **Never** overwrite `docs/test_plan_intro.md`, `docs/ots.yaml`,
  `docs/dt-clinical-context.md`, `dt-config.yaml`, the templates, or
  user items.
- `--update` touches ONLY `tools/build_docs.py`.
- A failing bash block → show the error, do not hide it.
