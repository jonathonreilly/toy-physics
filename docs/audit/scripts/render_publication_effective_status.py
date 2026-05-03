#!/usr/bin/env python3
"""Render audit-derived effective-status views of publication tables.

For each table-style publication doc, walk every markdown link to a note
inside docs/, look up the cited note's audit row in audit_ledger.json,
and produce a parallel `<NAME>_EFFECTIVE_STATUS.md` view that annotates
each link with the audit-derived `effective_status` and `audit_status`.

Author-side prose (Status / claim columns) is preserved; audit verdict
is appended in `[ ]` brackets after each link.

Also emits PUBLICATION_AUDIT_DIVERGENCE.md — a single-page report listing
every cited note in publication tables whose audit-derived status is NOT
retained-grade. This is the work queue for "which retained claims aren't
actually retained yet."

Outputs (all under docs/publication/ci3_z3/):
  CLAIMS_TABLE_EFFECTIVE_STATUS.md
  DERIVATION_ATLAS_EFFECTIVE_STATUS.md
  PUBLICATION_MATRIX_EFFECTIVE_STATUS.md
  FULL_CLAIM_LEDGER_EFFECTIVE_STATUS.md
  USABLE_DERIVED_VALUES_INDEX_EFFECTIVE_STATUS.md
  RESULTS_INDEX_EFFECTIVE_STATUS.md
  QUANTITATIVE_SUMMARY_TABLE_EFFECTIVE_STATUS.md
  DERIVATION_VALIDATION_MAP_EFFECTIVE_STATUS.md
  PUBLICATION_AUDIT_DIVERGENCE.md

This script is mechanical and idempotent. Re-run via run_pipeline.sh.
"""
from __future__ import annotations

import json
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS = REPO_ROOT / "docs"
PUB_DIR = DOCS / "publication" / "ci3_z3"
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

# Tables to render. Each entry: (source_basename, output_basename, scope_label)
TABLES = [
    ("CLAIMS_TABLE.md", "CLAIMS_TABLE_EFFECTIVE_STATUS.md",
     "manuscript claim surface"),
    ("DERIVATION_ATLAS.md", "DERIVATION_ATLAS_EFFECTIVE_STATUS.md",
     "atlas of reusable derivations"),
    ("PUBLICATION_MATRIX.md", "PUBLICATION_MATRIX_EFFECTIVE_STATUS.md",
     "publication matrix"),
    ("FULL_CLAIM_LEDGER.md", "FULL_CLAIM_LEDGER_EFFECTIVE_STATUS.md",
     "full claim ledger"),
    ("USABLE_DERIVED_VALUES_INDEX.md", "USABLE_DERIVED_VALUES_INDEX_EFFECTIVE_STATUS.md",
     "usable derived values index"),
    ("RESULTS_INDEX.md", "RESULTS_INDEX_EFFECTIVE_STATUS.md",
     "results index"),
    ("QUANTITATIVE_SUMMARY_TABLE.md", "QUANTITATIVE_SUMMARY_TABLE_EFFECTIVE_STATUS.md",
     "quantitative summary table"),
    ("DERIVATION_VALIDATION_MAP.md", "DERIVATION_VALIDATION_MAP_EFFECTIVE_STATUS.md",
     "derivation / validation map"),
]
DIVERGENCE_OUT = "PUBLICATION_AUDIT_DIVERGENCE.md"

# Match markdown links whose target ends in .md (with optional anchor)
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s#]+\.md)(#[^)]*)?\)")

RETAINED_GRADE = {
    "retained",
    "retained_bounded",
    "retained_no_go",
}


def load_ledger() -> dict[str, dict]:
    if not LEDGER_PATH.exists():
        raise SystemExit(f"FATAL: {LEDGER_PATH} missing; run pipeline first")
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def index_by_path(rows: dict[str, dict]) -> dict[Path, tuple[str, dict]]:
    out: dict[Path, tuple[str, dict]] = {}
    for cid, r in rows.items():
        np = r.get("note_path") or ""
        if not np:
            continue
        try:
            out[(REPO_ROOT / np).resolve()] = (cid, r)
        except Exception:
            continue
    return out


def resolve_link(target: str, source: Path) -> Path | None:
    """Replicate the citation-graph builder's resolver semantics: handle
    legacy absolute paths via the /docs/ marker; URL-decode."""
    decoded = urllib.parse.unquote(target)
    if decoded.startswith("/"):
        marker = "/docs/"
        idx = decoded.find(marker)
        if idx < 0:
            return None
        candidate = (DOCS / decoded[idx + len(marker):]).resolve()
    else:
        candidate = (source.parent / decoded).resolve()
    return candidate if candidate.exists() else None


def status_badge(eff: str | None, ast: str | None) -> str:
    """Compact one-cell badge for inline annotation."""
    eff = eff or "?"
    ast = ast or "?"
    if eff in RETAINED_GRADE:
        return f"[audit:{eff}]"
    if eff.startswith("decoration_under_"):
        return f"[audit:{eff}]"
    if eff == "retained_pending_chain":
        return f"[audit:retained_pending_chain]"
    if eff == "meta":
        return f"[audit:meta]"
    if eff == "open_gate":
        return f"[audit:open_gate]"
    return f"[audit:{eff}]"


def annotate_links(body: str, source: Path,
                   by_path: dict[Path, tuple[str, dict]]) -> tuple[str, list[dict]]:
    """Append a status badge after every markdown link to a docs/ note.
    Returns the rewritten body and a list of per-link audit lookups."""
    lookups: list[dict] = []

    def repl(m: re.Match[str]) -> str:
        whole = m.group(0)
        target = m.group(2)
        resolved = resolve_link(target, source)
        if resolved is None:
            return whole
        try:
            resolved.relative_to(DOCS)
        except ValueError:
            return whole
        match = by_path.get(resolved)
        if not match:
            return whole
        cid, row = match
        eff = row.get("effective_status")
        ast = row.get("audit_status")
        crit = row.get("criticality")
        lookups.append({
            "claim_id": cid,
            "note_path": str(resolved.relative_to(REPO_ROOT)),
            "audit_status": ast,
            "effective_status": eff,
            "criticality": crit,
        })
        badge = status_badge(eff, ast)
        # Append the badge AFTER the link, with a thin space
        return f"{whole}&nbsp;{badge}"

    new_body = LINK_RE.sub(repl, body)
    return new_body, lookups


def render_table(source_name: str, output_name: str, scope_label: str,
                 by_path: dict[Path, tuple[str, dict]],
                 generated_at: str) -> tuple[Path, list[dict]]:
    src = PUB_DIR / source_name
    if not src.exists():
        return None, []
    body = src.read_text(encoding="utf-8")
    annotated, lookups = annotate_links(body, src, by_path)

    header = (
        f"<!-- AUTO-GENERATED by docs/audit/scripts/render_publication_effective_status.py -->\n"
        f"<!-- Source: {source_name}  generated_at: {generated_at} -->\n"
        f"<!-- DO NOT EDIT THIS FILE BY HAND. Edit the source above; this view auto-refreshes. -->\n\n"
        f"# {scope_label.title()} — Audit-Derived Effective-Status View\n\n"
        f"**Auto-generated.** This is a parallel view of [`{source_name}`]({source_name}) "
        f"with each linked note annotated with its audit-derived `effective_status` "
        f"badge `[audit:STATUS]`. Edit the source file; this view refreshes via "
        f"`docs/audit/scripts/run_pipeline.sh`.\n\n"
        f"**Retained-grade values:** `retained`, `retained_bounded`, `retained_no_go`. "
        f"Anything else means the audit lane has NOT confirmed the claim, regardless of "
        f"the author-side status text in the row.\n\n"
        f"---\n\n"
    )

    out_path = PUB_DIR / output_name
    out_path.write_text(header + annotated, encoding="utf-8")
    return out_path, lookups


def render_divergence(all_lookups: dict[str, list[dict]],
                      generated_at: str) -> Path:
    """Build a single divergence report: every distinct (table, note) pair
    whose audit verdict is NOT retained-grade."""
    distinct_non_retained: dict[str, dict] = {}  # claim_id -> row
    for table, lookups in all_lookups.items():
        for L in lookups:
            eff = L.get("effective_status") or ""
            if eff in RETAINED_GRADE or eff.startswith("decoration_under_") or eff == "meta":
                continue
            cid = L["claim_id"]
            entry = distinct_non_retained.setdefault(cid, {
                "claim_id": cid,
                "note_path": L["note_path"],
                "effective_status": eff,
                "audit_status": L.get("audit_status"),
                "criticality": L.get("criticality"),
                "appearing_in": set(),
            })
            entry["appearing_in"].add(table)

    rows = sorted(distinct_non_retained.values(),
                  key=lambda r: (
                      0 if r["criticality"] == "critical" else
                      1 if r["criticality"] == "high" else
                      2 if r["criticality"] == "medium" else 3,
                      r["claim_id"],
                  ))

    lines: list[str] = []
    lines.append("<!-- AUTO-GENERATED by docs/audit/scripts/render_publication_effective_status.py -->")
    lines.append(f"<!-- generated_at: {generated_at} -->\n")
    lines.append("# Publication Audit Divergence Report")
    lines.append("")
    lines.append(f"**Auto-generated.** Every distinct cited note in any tracked")
    lines.append(f"publication table whose audit-derived `effective_status` is NOT")
    lines.append(f"retained-grade. This is the work queue for closing the gap between")
    lines.append(f"author-side claim language and audit-lane verdicts.\n")
    lines.append(f"**Retained-grade values:** `retained`, `retained_bounded`, `retained_no_go`,")
    lines.append(f"plus `decoration_under_*` (boxed under retained parent). Anything else")
    lines.append(f"means the audit has not confirmed the claim, regardless of how the")
    lines.append(f"publication tables phrase it.\n")
    lines.append(f"## Summary by criticality\n")

    by_crit_eff: dict[tuple[str, str], int] = {}
    for r in rows:
        key = (r["criticality"] or "?", r["effective_status"] or "?")
        by_crit_eff[key] = by_crit_eff.get(key, 0) + 1

    lines.append("| criticality | effective_status | count |")
    lines.append("|---|---|---:|")
    for (c, e), n in sorted(by_crit_eff.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {c} | `{e}` | {n} |")
    lines.append("")
    lines.append(f"**Total non-retained-grade rows in publication tables:** {len(rows)}\n")
    lines.append("## Per-row breakdown\n")
    lines.append("| criticality | claim_id | effective_status | audit_status | appearing in |")
    lines.append("|---|---|---|---|---|")
    for r in rows:
        tables = ", ".join(sorted(r["appearing_in"]))
        lines.append(
            f"| {r['criticality'] or '?'} | "
            f"`{r['claim_id']}` | "
            f"`{r['effective_status'] or '?'}` | "
            f"`{r['audit_status'] or '?'}` | "
            f"{tables} |"
        )

    out_path = PUB_DIR / DIVERGENCE_OUT
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def main() -> int:
    ledger = load_ledger()
    rows = ledger.get("rows", {})
    by_path = index_by_path(rows)
    generated_at = datetime.now(timezone.utc).isoformat()

    all_lookups: dict[str, list[dict]] = {}
    rendered: list[Path] = []
    for src, out, scope in TABLES:
        result, lookups = render_table(src, out, scope, by_path, generated_at)
        if result is None:
            print(f"  [skip] {src} not found")
            continue
        all_lookups[src] = lookups
        rendered.append(result)
        print(f"  rendered {result.relative_to(REPO_ROOT)}  ({len(lookups)} link annotations)")

    div = render_divergence(all_lookups, generated_at)
    print(f"  wrote    {div.relative_to(REPO_ROOT)}")
    print(f"\nDone. {len(rendered)} effective-status views + 1 divergence report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
