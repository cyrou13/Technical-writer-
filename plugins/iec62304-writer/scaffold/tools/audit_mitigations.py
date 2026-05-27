#!/usr/bin/env python3
"""Audit code-vs-mitigation coverage for unacceptable residual risks.

For every risk item (RSK / URSK / THR / PRSK) whose `residual_acceptable`
is False, list the controls that mitigate it and surface the static
state of each control (does the SRS item exist? does it have a
`source:` pointer? is `[TODO]` still in its body? is a TC verifying
it?).

This script does NOT read source code. It produces a structured
report that a downstream agent (`mitigation-auditor`) consumes to
issue an IMPLEMENTED / PARTIAL / ABSENT verdict per control after
inspecting the cited code.

Reads:
    docs/items/<CAT>/*.md           (every category)
    dt-config.yaml                  (optional, not required)

Writes:
    docs/generated/_mitigation_audit.json   (machine-readable)
    docs/generated/_mitigation_audit.md     (human-readable summary)

CLI:
    python tools/audit_mitigations.py [--all] [--cat RSK,URSK,THR,PRSK]

Modes:
    Default            : only items with residual_acceptable == False
    --all              : every risk item, regardless of acceptance
    --cat <list>       : restrict to the given comma-separated categories

Stdlib only. Python 3.12+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import Item, load_items  # noqa: E402

ROOT = Path.cwd()
ITEMS_DIR = ROOT / "docs" / "items"
GEN_DIR = ROOT / "docs" / "generated"

RISK_CATEGORIES = ("RSK", "URSK", "THR", "PRSK")
CONTROL_CATEGORIES = ("SRS", "SDS", "TC")

# Match item IDs in any free-text section.
# Supports 3-segment (SRS-AUTH-001) and 5-segment (SRS-CINA-CSP-AUTH-001) forms.
ID_RE = re.compile(r"\b((?:SRS|SDS|TC)-[A-Z0-9][A-Z0-9-]*?-\d{3,4})\b")
TODO_RE = re.compile(r"\[TODO\b", re.IGNORECASE)


@dataclass
class ControlStatus:
    id: str
    linked: bool  # present in links.mitigates of an SRS/SDS/TC
    mentioned_in_body: bool  # appears in the risk item's body
    item_exists: bool  # the SRS/SDS/TC item exists on disk
    source_files: list[str] = field(default_factory=list)
    source_files_present: list[str] = field(default_factory=list)
    source_files_missing: list[str] = field(default_factory=list)
    implementation_status: str = "unknown"  # absent | partial | implemented | unknown
    has_todo_marker: bool = False
    verified_by: list[str] = field(default_factory=list)  # TC IDs that verifies this SRS
    static_verdict: str = "needs_agent_review"  # see _static_verdict()
    note: str = ""


@dataclass
class RiskAudit:
    id: str
    category: str
    title: str
    residual_acceptable: bool | None
    residual_risk_level: str | None
    controls: list[ControlStatus] = field(default_factory=list)


def _static_verdict(cs: ControlStatus) -> str:
    """Heuristic verdict before the agent reads the code."""
    if not cs.item_exists:
        return "control_referenced_but_no_item"
    if not cs.source_files:
        return "no_source_pointer"
    if cs.source_files_missing and not cs.source_files_present:
        return "all_sources_missing"
    if cs.has_todo_marker:
        return "marked_todo_in_body"
    if not cs.verified_by:
        return "implementation_claimed_no_tc"
    return "implementation_claimed_with_tc"


def _collect_controls_for_risk(
    risk: Item,
    by_cat: dict[str, dict[str, Item]],
    src_root: Path,
) -> list[ControlStatus]:
    """For one risk item, walk its mitigators and body mentions and
    compile a ControlStatus per cited control."""
    # 1. Formal links: items pointing at this risk via links.mitigates
    linked: dict[str, Item] = {}
    for cat in CONTROL_CATEGORIES:
        for item in by_cat.get(cat, {}).values():
            if risk.id in item.mitigates:
                linked[item.id] = item

    # 2. Free-text mentions in the risk body (catches [TODO] SRS-MIT-XXX)
    body_mentions = set(ID_RE.findall(risk.body or ""))

    # 3. Union of both
    all_ids = set(linked.keys()) | body_mentions

    controls: list[ControlStatus] = []
    all_items = {**by_cat.get("SRS", {}), **by_cat.get("SDS", {}), **by_cat.get("TC", {})}
    tcs = by_cat.get("TC", {})

    for cid in sorted(all_ids):
        item = all_items.get(cid)
        cs = ControlStatus(
            id=cid,
            linked=cid in linked,
            mentioned_in_body=cid in body_mentions,
            item_exists=item is not None,
        )
        if item is not None:
            sources = item.fm.get("source") or []
            cs.source_files = [str(s) for s in sources if isinstance(s, str)]
            for f in cs.source_files:
                if (src_root / f).is_file():
                    cs.source_files_present.append(f)
                else:
                    cs.source_files_missing.append(f)
            cs.has_todo_marker = bool(TODO_RE.search(item.body or ""))
            cs.implementation_status = str(
                item.fm.get("implementation_status") or "unknown"
            )
            # TCs that verify this control (only meaningful for SRS)
            if cid.startswith("SRS-"):
                cs.verified_by = sorted(
                    tc.id for tc in tcs.values() if cid in (tc.fm.get("links") or {}).get("verifies", []) or []
                )
        else:
            cs.note = "Mentioned in risk body but no matching SRS/SDS/TC item on disk."

        cs.static_verdict = _static_verdict(cs)
        controls.append(cs)

    return controls


def audit(
    items_dir: Path,
    src_root: Path,
    only_unacceptable: bool,
    categories: tuple[str, ...],
) -> list[RiskAudit]:
    by_cat: dict[str, dict[str, Item]] = {}
    for cat in ("SRS", "SDS", "TC", *RISK_CATEGORIES):
        by_cat[cat] = {item.id: item for item in load_items(cat, items_dir)}

    out: list[RiskAudit] = []
    for cat in categories:
        for risk in by_cat.get(cat, {}).values():
            if risk.status == "Deprecated":
                continue
            residual = risk.fm.get("residual_acceptable")
            if only_unacceptable and residual is not False:
                continue
            out.append(
                RiskAudit(
                    id=risk.id,
                    category=cat,
                    title=risk.title,
                    residual_acceptable=residual,
                    residual_risk_level=risk.fm.get("residual_risk_level"),
                    controls=_collect_controls_for_risk(risk, by_cat, src_root),
                )
            )
    out.sort(key=lambda r: r.id)
    return out


VERDICT_LABEL = {
    "control_referenced_but_no_item": "Control referenced in risk body but no SRS/SDS/TC item exists",
    "no_source_pointer": "Control item exists but has no `source:` pointer",
    "all_sources_missing": "Every cited source file is missing from the repo",
    "marked_todo_in_body": "Control item still carries a `[TODO]` marker",
    "implementation_claimed_no_tc": "Control item points at code but no TC verifies it yet",
    "implementation_claimed_with_tc": "Control item points at code AND has at least one TC — agent verifies depth",
    "needs_agent_review": "Generic — agent should inspect",
}


def render_markdown(audits: list[RiskAudit], only_unacceptable: bool) -> str:
    lines: list[str] = []
    title_scope = (
        "Unacceptable residual risks" if only_unacceptable else "All residual risks"
    )
    lines.append(f"# Mitigation audit — {title_scope}")
    lines.append("")
    lines.append(
        "This report is the static cadrage produced by "
        "`tools/audit_mitigations.py`. It enumerates, for every risk in "
        "scope, the controls cited in its body or linked via "
        "`links.mitigates`, and assigns a static verdict to each — without "
        "reading the source code. The `mitigation-auditor` agent picks up "
        "this report and produces the per-control IMPLEMENTED / PARTIAL / "
        "ABSENT verdict by inspecting the cited code, then proposes "
        "frontmatter updates on the relevant SRS items."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Risks in scope: **{len(audits)}**")
    total_controls = sum(len(a.controls) for a in audits)
    lines.append(f"- Controls cited (total): **{total_controls}**")
    verdict_counts: dict[str, int] = {}
    for a in audits:
        for c in a.controls:
            verdict_counts[c.static_verdict] = verdict_counts.get(c.static_verdict, 0) + 1
    for v, n in sorted(verdict_counts.items()):
        lines.append(f"  - `{v}`: {n}")
    lines.append("")

    for a in audits:
        lines.append(f"## {a.id} — {a.title}")
        lines.append("")
        lines.append(
            f"`category: {a.category}` · "
            f"`residual_acceptable: {a.residual_acceptable}` · "
            f"`residual_risk_level: {a.residual_risk_level}`"
        )
        lines.append("")
        if not a.controls:
            lines.append("_No controls cited._")
            lines.append("")
            continue
        lines.append(
            "| Control | Linked | In body | Exists | Sources | TODO? | TCs | Static verdict |"
        )
        lines.append("|---|---|---|---|---|---|---|---|")
        for c in a.controls:
            src_summary = (
                f"{len(c.source_files_present)}/{len(c.source_files)} present"
                if c.source_files
                else "—"
            )
            tcs_summary = ", ".join(c.verified_by) if c.verified_by else "—"
            lines.append(
                f"| `{c.id}` "
                f"| {'✓' if c.linked else '·'} "
                f"| {'✓' if c.mentioned_in_body else '·'} "
                f"| {'✓' if c.item_exists else '✗'} "
                f"| {src_summary} "
                f"| {'✓' if c.has_todo_marker else '·'} "
                f"| {tcs_summary} "
                f"| `{c.static_verdict}` |"
            )
        lines.append("")
        # Detail for controls needing source inspection
        needs_review = [
            c for c in a.controls
            if c.static_verdict.startswith("implementation_claimed")
            or c.static_verdict == "marked_todo_in_body"
        ]
        if needs_review:
            lines.append("**Agent review queue for this risk:**")
            for c in needs_review:
                src_list = ", ".join(f"`{s}`" for s in c.source_files_present) or "(none)"
                lines.append(f"- `{c.id}` → inspect: {src_list}")
            lines.append("")

    lines.append("## Static verdict legend")
    lines.append("")
    for k, v in VERDICT_LABEL.items():
        lines.append(f"- `{k}` — {v}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Audit every risk item, not just residual_acceptable=False.",
    )
    parser.add_argument(
        "--cat",
        default=",".join(RISK_CATEGORIES),
        help=f"Comma-separated risk categories (default: {','.join(RISK_CATEGORIES)}).",
    )
    args = parser.parse_args()

    cats = tuple(c.strip().upper() for c in args.cat.split(",") if c.strip())
    invalid = [c for c in cats if c not in RISK_CATEGORIES]
    if invalid:
        print(f"ERROR: unknown categor{'y' if len(invalid)==1 else 'ies'}: {invalid}", file=sys.stderr)
        return 2

    if not ITEMS_DIR.is_dir():
        print(f"ERROR: {ITEMS_DIR} not found. Run from a /doc-init-ed repo.", file=sys.stderr)
        return 2

    GEN_DIR.mkdir(parents=True, exist_ok=True)

    audits = audit(
        items_dir=ITEMS_DIR,
        src_root=ROOT,
        only_unacceptable=not args.all,
        categories=cats,
    )

    json_path = GEN_DIR / "_mitigation_audit.json"
    md_path = GEN_DIR / "_mitigation_audit.md"
    json_path.write_text(
        json.dumps([asdict(a) for a in audits], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(audits, only_unacceptable=not args.all), encoding="utf-8")

    total_controls = sum(len(a.controls) for a in audits)
    print(f"OK — risks in scope: {len(audits)} · controls cited: {total_controls}")
    print(f"  → {md_path}")
    print(f"  → {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
