#!/usr/bin/env python3
"""Reset the docs/items store to a clean design-phase baseline.

In design phase the goal is a single coherent baseline, not a history of
patches. This tool collapses the in-session versioning noise the writers
accumulate:

    - version: <any>            -> versioning.baseline_version (default 1.0.0)
    - remove any `## Changelog` body section (nothing to change before V1)

`id`, `created`, `updated`, `status` and every other field are left untouched.
Deprecated items are skipped (their historical version is preserved). Idempotent.

`updated:` is deliberately NOT normalised. It is the only record of when an item
was last read against the code, and it is what the next `/doc-update` staleness
scan subtracts the source mtimes from. Stamping it across the whole store makes
every item look freshly reviewed, including the ones the pass never opened, and
the following pass then re-reads nothing. Pass `--stamp-updated YYYY-MM-DD` to
opt into the old behaviour for a genuine full-store review.

Driven by `dt-config.yaml: versioning`:

    versioning:
      mode: design            # design | maintenance
      baseline_version: "1.0.0"

Refuses to run when `mode` is `maintenance` (a released project keeps its
per-item versions) unless `--force` is given.

Stdlib only. Python 3.12+.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import parse_yaml  # noqa: E402

ROOT = Path.cwd()
CONFIG_PATH = ROOT / "dt-config.yaml"
ITEMS_DIR = ROOT / "docs" / "items"

FM_RE = re.compile(r"(---\n.*?\n---\n)(.*)", re.S)
CHANGELOG_RE = re.compile(r"\n*^## Changelog\b.*?(?=\n## |\Z)", re.S | re.M)


def normalize_text(text: str, baseline_version: str, baseline_date: str | None) -> tuple[str, bool, bool, bool]:
    m = FM_RE.match(text)
    if not m:
        return text, False, False, False
    fm, body = m.group(1), m.group(2)
    if re.search(r"^status:\s*Deprecated\s*$", fm, re.M):
        return text, False, False, False

    v_changed = bool(re.search(rf"^version:\s*(?!{re.escape(baseline_version)}\s*$)\S+", fm, re.M))
    fm = re.sub(r"^version:\s*\S+", f"version: {baseline_version}", fm, count=1, flags=re.M)

    u_changed = False
    if baseline_date is not None:
        u_changed = bool(re.search(rf"^updated:\s*(?!{re.escape(baseline_date)}\s*$)\S+", fm, re.M))
        fm = re.sub(r"^updated:\s*\S+", f"updated: {baseline_date}", fm, count=1, flags=re.M)

    new_body = CHANGELOG_RE.sub("\n", body)
    c_changed = new_body != body
    body = new_body.rstrip() + "\n"

    return fm + body, v_changed, u_changed, c_changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset docs/items to a clean design baseline.")
    parser.add_argument("--stamp-updated", metavar="YYYY-MM-DD", nargs="?", const="today",
                        help="Also stamp `updated:` on every item (default: leave it alone). "
                             "Use only for a genuine full-store review — it erases the staleness "
                             "signal the next /doc-update pass reads.")
    parser.add_argument("--force", action="store_true", help="Run even when versioning.mode is maintenance.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing.")
    args = parser.parse_args()

    config: dict = {}
    if CONFIG_PATH.is_file():
        config = parse_yaml(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    versioning = (config.get("versioning") or {}) if config else {}
    mode = str(versioning.get("mode") or "maintenance")
    baseline_version = str(versioning.get("baseline_version") or "1.0.0")
    baseline_date = args.stamp_updated
    if baseline_date == "today":
        baseline_date = date.today().isoformat()

    if mode != "design" and not args.force:
        print(
            f"ERROR: versioning.mode is '{mode}', not 'design'. This tool collapses "
            "per-item versions and is meant for pre-release design phase. Re-run with "
            "--force only if you really mean to reset a maintenance-mode project.",
            file=sys.stderr,
        )
        return 1

    if not ITEMS_DIR.is_dir():
        print(f"ERROR: {ITEMS_DIR} not found — run from the repo root.", file=sys.stderr)
        return 1

    nv = nu = nc = nfiles = 0
    for p in sorted(ITEMS_DIR.glob("*/*.md")):
        original = p.read_text(encoding="utf-8")
        result, v, u, c = normalize_text(original, baseline_version, baseline_date)
        nv += v
        nu += u
        nc += c
        if result != original:
            nfiles += 1
            if not args.dry_run:
                p.write_text(result, encoding="utf-8")

    verb = "would change" if args.dry_run else "changed"
    stamp = baseline_date if baseline_date else "left untouched"
    print(f"baseline: version={baseline_version} updated={stamp} (mode={mode})")
    print(f"files {verb}: {nfiles}")
    print(f"  versions -> {baseline_version}: {nv}")
    if baseline_date:
        print(f"  updated  -> {baseline_date}: {nu}")
    print(f"  Changelog sections removed: {nc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
