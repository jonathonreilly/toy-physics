#!/usr/bin/env python3
"""Render the audit ledger as a human-readable markdown table.

Writes docs/audit/AUDIT_LEDGER.md. The markdown is the publication-facing
view of the JSON ledger; downstream tables (CLAIMS_TABLE.md, etc.) should
read from this file or from the underlying JSON.

The renderer is read-only against the ledger JSON.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
SUMMARY_PATH = DATA_DIR / "effective_status_summary.json"
RUNNER_PATH = DATA_DIR / "runner_classification.json"
OUTPUT_PATH = REPO_ROOT / "docs" / "audit" / "AUDIT_LEDGER.md"

# Sort effective_status from strongest to weakest for the headline table.
STATUS_DISPLAY_ORDER = [
    "retained",
    "promoted",
    "proposed_retained",
    "proposed_promoted",
    "bounded",
    "support",
    "open",
    "unknown",
    "audited_decoration",
    "audited_numerical_match",
    "audited_renaming",
    "audited_conditional",
    "audited_failed",
]


def render_status_badge(s: str) -> str:
    """Visual differentiation for proposed vs ratified vs failure tiers."""
    if s == "retained" or s == "promoted":
        return f"**{s}**"
    if s.startswith("proposed_"):
        return f"_{s}_"  # italic = unratified
    if s.startswith("audited_"):
        return f"~~{s}~~"  # strikethrough = failed audit verdict
    return s


def short_path(p: str) -> str:
    return p.replace("docs/", "")


def render_audited_rows_table(rows: dict[str, dict]) -> str:
    audited = [r for r in rows.values() if r.get("audit_status", "unaudited") != "unaudited"]
    if not audited:
        return "_No audits applied yet._\n"
    audited.sort(key=lambda r: (r.get("audit_status"), r.get("claim_id")))
    lines = [
        "| claim_id | current | audit_status | effective | independence | auditor_family | load-bearing class | decoration parent |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in audited:
        lines.append(
            "| `{cid}` | {cs} | {a} | {e} | {ind} | {fam} | {cls} | {par} |".format(
                cid=r["claim_id"],
                cs=render_status_badge(r.get("current_status", "unknown")),
                a=render_status_badge(r.get("audit_status", "unaudited")),
                e=render_status_badge(r.get("effective_status", "unknown")),
                ind=r.get("independence") or "-",
                fam=r.get("auditor_family") or "-",
                cls=r.get("load_bearing_step_class") or "-",
                par=f"`{r['decoration_parent_claim_id']}`" if r.get("decoration_parent_claim_id") else "-",
            )
        )
    return "\n".join(lines) + "\n"


def render_audited_findings(rows: dict[str, dict]) -> str:
    audited = [r for r in rows.values() if r.get("audit_status", "unaudited") not in ("unaudited", "audit_in_progress")]
    if not audited:
        return ""
    audited.sort(key=lambda r: r.get("claim_id"))
    parts = []
    for r in audited:
        parts.append(f"### `{r['claim_id']}`\n")
        parts.append(f"- **Note:** [`{short_path(r['note_path'])}`](../../{r['note_path']})")
        parts.append(f"- **current_status:** {render_status_badge(r.get('current_status', 'unknown'))}")
        parts.append(f"- **audit_status:** {render_status_badge(r.get('audit_status', 'unaudited'))}")
        parts.append(f"- **effective_status:** {render_status_badge(r.get('effective_status', 'unknown'))}  "
                     f"(reason: `{r.get('effective_status_reason', 'self')}`)")
        parts.append(f"- **auditor:** `{r.get('auditor', '-')}`  "
                     f"({r.get('auditor_family', '-')}; independence={r.get('independence', '-')})")
        parts.append(f"- **load-bearing step:** {r.get('load_bearing_step', '-')}  _(class `{r.get('load_bearing_step_class', '-')}`)_")
        parts.append(f"- **chain closes:** {r.get('chain_closes', '-')} — {r.get('chain_closure_explanation', '')}")
        if r.get("verdict_rationale"):
            parts.append(f"- **rationale:** {r['verdict_rationale']}")
        if r.get("open_dependency_paths"):
            parts.append("- **open / conditional deps cited:**")
            for d in r["open_dependency_paths"]:
                parts.append(f"  - `{short_path(d)}`")
        if r.get("decoration_parent_claim_id"):
            parts.append(f"- **decoration parent:** `{r['decoration_parent_claim_id']}`")
        if r.get("auditor_confidence"):
            parts.append(f"- **auditor confidence:** {r['auditor_confidence']}")
        parts.append("")
    return "\n".join(parts) + "\n"


def render_summary_block(rows: dict[str, dict], summary: dict | None) -> str:
    counts = {s: 0 for s in STATUS_DISPLAY_ORDER}
    for r in rows.values():
        e = r.get("effective_status", "unknown")
        counts[e] = counts.get(e, 0) + 1
    audit_status_counts: dict[str, int] = {}
    crit_counts: dict[str, int] = {}
    for r in rows.values():
        a = r.get("audit_status", "unaudited")
        audit_status_counts[a] = audit_status_counts.get(a, 0) + 1
        c = r.get("criticality") or "leaf"
        crit_counts[c] = crit_counts.get(c, 0) + 1
    lines = [
        "| effective_status | count |",
        "|---|---:|",
    ]
    for s in STATUS_DISPLAY_ORDER:
        if counts.get(s, 0) > 0:
            lines.append(f"| {render_status_badge(s)} | {counts[s]} |")
    lines.append("")
    lines.append("| audit_status | count |")
    lines.append("|---|---:|")
    for k in sorted(audit_status_counts):
        lines.append(f"| `{k}` | {audit_status_counts[k]} |")
    lines.append("")
    lines.append("| criticality | count |")
    lines.append("|---|---:|")
    for k in ("critical", "high", "medium", "leaf"):
        if crit_counts.get(k, 0) > 0:
            lines.append(f"| `{k}` | {crit_counts[k]} |")
    if summary:
        lines.append("")
        lines.append(f"- **Proposed claims demoted by upstream:** "
                     f"{summary.get('proposed_demoted_by_upstream_count', 0)}")
        lines.append(f"- **Citation cycles detected:** {summary.get('cycles_detected', 0)}")
    return "\n".join(lines) + "\n"


def render_top_load_bearing(rows: dict[str, dict], n: int = 25) -> str:
    sortable = [
        r for r in rows.values()
        if r.get("load_bearing_score") is not None
    ]
    sortable.sort(key=lambda r: -float(r.get("load_bearing_score") or 0))
    top = sortable[:n]
    lines = [
        "| # | claim_id | criticality | desc | score | audit_status | effective |",
        "|---:|---|---|---:|---:|---|---|",
    ]
    for i, r in enumerate(top, 1):
        lines.append(
            "| {i} | `{cid}` | {crit} | {td} | {sc:.2f} | `{a}` | {e} |".format(
                i=i,
                cid=r.get("claim_id"),
                crit=r.get("criticality") or "leaf",
                td=r.get("transitive_descendants") or 0,
                sc=float(r.get("load_bearing_score") or 0),
                a=r.get("audit_status") or "unaudited",
                e=render_status_badge(r.get("effective_status") or "unknown"),
            )
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8")) if SUMMARY_PATH.exists() else None

    runner_cls = json.loads(RUNNER_PATH.read_text(encoding="utf-8")) if RUNNER_PATH.exists() else None

    out: list[str] = []
    out.append("# Audit Ledger")
    out.append("")
    out.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    out.append("**Source of truth:** `data/audit_ledger.json`")
    out.append("**Schema:** see [README.md](README.md), "
               "[FRESH_LOOK_REQUIREMENTS.md](FRESH_LOOK_REQUIREMENTS.md), and "
               "[ALGEBRAIC_DECORATION_POLICY.md](ALGEBRAIC_DECORATION_POLICY.md).")
    out.append("")
    out.append("This file is auto-generated. Do not edit by hand. Apply audits via "
               "`scripts/apply_audit.py`, then re-run `scripts/compute_effective_status.py` "
               "and `scripts/render_audit_ledger.py`.")
    out.append("")
    out.append("## Reading rule")
    out.append("")
    out.append("- **Bold** = audit-ratified (`retained`, `promoted`).")
    out.append("- _Italic_ = author-proposed but not yet audit-ratified "
               "(`proposed_retained`, `proposed_promoted`).")
    out.append("- ~~Strikethrough~~ = audit returned a failure verdict.")
    out.append("- Plain = `support`, `bounded`, `open`, or `unknown`.")
    out.append("")
    out.append("Publication-facing tables MUST read `effective_status`, not `current_status`.")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(render_summary_block(rows, summary))
    if runner_cls:
        s = runner_cls["stats"]
        out.append("### Runner classification (static heuristic)")
        out.append("")
        out.append(f"- runners classified: {s['runners_classified']}")
        out.append(f"- runners with (C) first-principles compute hits: {s['runners_with_C']}")
        out.append(f"- runners with (D) external comparator hits: {s['runners_with_D']}")
        out.append(f"- decoration candidates (no C, no D): {s['decoration_candidates']}")
        out.append("")
    out.append("## Top 25 by load-bearing score (topology only)")
    out.append("")
    out.append("Criticality and load-bearing score are computed from the citation "
               "graph alone. The audit lane intentionally does not use "
               "author-declared flagship status — that would let unratified "
               "framing drive audit cost on upstream support claims.")
    out.append("")
    out.append(render_top_load_bearing(rows, n=25))
    out.append("")
    out.append("## Applied audits")
    out.append("")
    out.append(render_audited_rows_table(rows))
    out.append("")
    out.append("## Audit findings (full)")
    out.append("")
    out.append(render_audited_findings(rows))

    while out and out[-1] == "":
        out.pop()
    OUTPUT_PATH.write_text("\n".join(out) + "\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
