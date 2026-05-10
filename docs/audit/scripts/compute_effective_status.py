#!/usr/bin/env python3
"""Compute effective_status for every row in the audit ledger.

Scope-aware rule:
  - `claim_type` is auditor-owned and determines which retained-grade bucket
    a clean audit may enter.
  - clean theorem/no-go/bounded rows become retained-grade only when every
    one-hop dependency is already retained-grade.
  - open gates, decorations, metadata, and terminal non-clean audit verdicts
    have explicit effective statuses and never become retained by author tier.

Writes effective_status, intrinsic_status, effective_status_reason, and a
summary back into docs/audit/data/audit_ledger.json.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
SUMMARY_PATH = DATA_DIR / "effective_status_summary.json"

RETAINED_GRADES = {"retained", "retained_no_go", "retained_bounded"}
TERMINAL_AUDIT_STATUSES = {
    "audited_renaming",
    "audited_conditional",
    "audited_failed",
    "audited_numerical_match",
}
CLAIM_TYPE_TO_RETAINED = {
    "positive_theorem": "retained",
    "no_go": "retained_no_go",
    "bounded_theorem": "retained_bounded",
}

# Strength rank: higher = stronger publication-facing tier. Dynamic
# decoration_under_<claim_id> values are ranked by status_rank().
RANK = {
    "retained": 100,
    "retained_no_go": 100,
    "retained_bounded": 95,
    "retained_pending_chain": 80,
    "open_gate": 40,
    "unaudited": 30,
    "audit_in_progress": 30,
    "meta": 25,
    "audited_decoration": 20,
    "audited_numerical_match": 15,
    "audited_renaming": 10,
    "audited_conditional": 10,
    "audited_failed": 0,
}


def status_rank(status: str | None) -> int:
    if status and status.startswith("decoration_under_"):
        return 70
    return RANK.get(status or "unaudited", -1)


def is_retained_grade(status: str | None) -> bool:
    return status in RETAINED_GRADES


def archived_failed_is_retained_no_go(row: dict) -> bool:
    if row.get("audit_status") != "audited_failed":
        return False
    note_path = row.get("note_path") or ""
    return note_path.startswith("archive_unlanded/") and (REPO_ROOT / note_path).exists()


def decoration_status(row: dict, dep_effective: dict[str, str]) -> tuple[str, str]:
    parent = row.get("decoration_parent_claim_id")
    if not parent:
        return "audited_decoration", "decoration_missing_parent"
    parent_status = dep_effective.get(parent)
    if parent_status is None:
        parent_status = "unknown"
    if is_retained_grade(parent_status):
        return f"decoration_under_{parent}", "decoration_parent_retained"
    return "retained_pending_chain", f"decoration_waiting_on:{parent}"


def clean_status(row: dict, dep_effective: dict[str, str]) -> tuple[str, str]:
    claim_type = row.get("claim_type")
    if claim_type == "open_gate":
        return "open_gate", "audited_open_gate"
    if claim_type == "meta":
        return "meta", "metadata"
    if claim_type == "decoration":
        return decoration_status(row, dep_effective)

    retained_status = CLAIM_TYPE_TO_RETAINED.get(claim_type)
    if retained_status is None:
        return "retained_pending_chain", "missing_or_unknown_claim_type"

    for dep_id in sorted(row.get("deps", [])):
        dep_status = dep_effective.get(dep_id, "unaudited")
        if not is_retained_grade(dep_status):
            return "retained_pending_chain", f"chain_waiting_on:{dep_id}"
    return retained_status, "self"


def is_criticality_bump_soft_reset(row: dict) -> bool:
    """True iff the row is in the criticality-bump soft-reset state:
    `audit_status = audit_in_progress`, `blocker = awaiting_cross_confirmation`,
    `claim_type_provenance` flags it as a criticality-bump soft-reset, and
    `cross_confirmation.first_audit` is present with `status = awaiting_second`.

    Set by `invalidate_stale_audits.soft_reset_to_cross_confirmation_pending`
    when an existing audited_clean row's criticality bumps to `critical`
    without prior cross-confirmation. The first-pass clean evidence remains
    live in `cross_confirmation.first_audit`; the lane is just awaiting the
    independent second auditor at the new tier.

    For chain-closure purposes we treat such rows as if they were still at
    their prior `audited_clean` effective_status: downstream rows whose
    audits closed against this row's first-pass clean evidence are not
    forced to re-audit just because the row's criticality changed. Once
    cross-confirmation lands clean, nothing changes; if it disagrees, the
    row exits this state (`cc.status = disagreement`) and downstream
    chain closure is reassessed normally.
    """
    if row.get("audit_status") != "audit_in_progress":
        return False
    if row.get("blocker") != "awaiting_cross_confirmation":
        return False
    if row.get("claim_type_provenance") != "audited_pending_cross_confirmation_after_criticality_bump":
        return False
    cc = row.get("cross_confirmation") or {}
    if not isinstance(cc, dict):
        return False
    if cc.get("status") != "awaiting_second":
        return False
    return cc.get("first_audit") is not None


def intrinsic_status(row: dict, dep_effective: dict[str, str]) -> tuple[str, str]:
    if archived_failed_is_retained_no_go(row):
        return "retained_no_go", "archived_failed_no_go"

    claim_type = row.get("claim_type")
    audit_status = row.get("audit_status") or "unaudited"

    if claim_type == "meta" and audit_status in {"unaudited", "audit_in_progress"}:
        return "meta", "metadata"
    if audit_status == "audit_in_progress" and is_criticality_bump_soft_reset(row):
        # First-pass clean evidence is preserved; treat as still-clean for
        # chain closure so downstream rows aren't forced to re-audit while
        # the row awaits its second-tier cross-confirmation.
        clean_es, clean_reason = clean_status(row, dep_effective)
        return clean_es, f"awaiting_cross_confirmation_after_criticality_bump:{clean_reason}"
    if audit_status in {"unaudited", "audit_in_progress"}:
        return audit_status, "awaiting_audit"
    if audit_status == "audited_decoration":
        return decoration_status(row, dep_effective)
    if audit_status in TERMINAL_AUDIT_STATUSES:
        return audit_status, "terminal_audit"
    if audit_status == "audited_clean":
        return clean_status(row, dep_effective)
    return "unaudited", "unknown_audit_status"


def compute_effective(rows: dict[str, dict]) -> tuple[dict[str, dict], list[list[str]]]:
    """Compute effective_status by resolving dependencies first.

    Cycles are reported and treated conservatively: any clean row waiting on
    an unresolved cycle member remains retained_pending_chain.
    """
    effective: dict[str, str] = {}
    reason: dict[str, str] = {}
    intrinsic: dict[str, str] = {}
    cycles: list[list[str]] = []

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {cid: WHITE for cid in rows}

    def visit(start: str) -> None:
        stack = [(start, iter(rows[start].get("deps", [])))]
        path = [start]
        path_set = {start}
        color[start] = GRAY
        while stack:
            node, deps_iter = stack[-1]
            try:
                dep = next(deps_iter)
            except StopIteration:
                dep_effective = {
                    d: effective.get(d, "unaudited")
                    for d in rows[node].get("deps", [])
                    if d in rows
                }
                status, why = intrinsic_status(rows[node], dep_effective)
                intrinsic[node] = status
                effective[node] = status
                reason[node] = why
                color[node] = BLACK
                path.pop()
                path_set.discard(node)
                stack.pop()
                continue
            if dep not in rows:
                continue
            if color[dep] == GRAY:
                if dep in path_set:
                    cycle_start = path.index(dep)
                    cycles.append(list(path[cycle_start:]))
                continue
            if color[dep] == BLACK:
                continue
            color[dep] = GRAY
            path.append(dep)
            path_set.add(dep)
            stack.append((dep, iter(rows[dep].get("deps", []))))

    for cid in rows:
        if color[cid] == WHITE:
            visit(cid)

    for cid in rows:
        if cid not in effective:
            intrinsic[cid] = "retained_pending_chain"
            effective[cid] = "retained_pending_chain"
            reason[cid] = "cycle_unresolved"

    out: dict[str, dict] = {}
    for cid, row in rows.items():
        new_row = dict(row)
        new_row["intrinsic_status"] = intrinsic[cid]
        new_row["effective_status"] = effective[cid]
        new_row["effective_status_reason"] = reason[cid]
        out[cid] = new_row
    return out, cycles


def summarize(rows: dict[str, dict]) -> dict:
    eff_counts: dict[str, int] = {}
    claim_type_counts: dict[str, int] = {}
    pending_chain = []
    for cid, r in rows.items():
        e = r.get("effective_status", "unaudited")
        eff_counts[e] = eff_counts.get(e, 0) + 1
        ct = r.get("claim_type") or "unset"
        claim_type_counts[ct] = claim_type_counts.get(ct, 0) + 1
        if e == "retained_pending_chain":
            pending_chain.append(cid)

    return {
        "effective_status_counts": eff_counts,
        "claim_type_counts": claim_type_counts,
        "retained_pending_chain_count": len(pending_chain),
        "retained_pending_chain_examples": sorted(pending_chain)[:25],
    }


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    new_rows, cycles = compute_effective(rows)
    ledger["rows"] = new_rows

    # Defensive cleanup: drop any stale top-level timestamp keys left behind
    # by older pipeline versions. The current pipeline does not write these.
    # Without this, pre-existing keys round-trip through every save and fire
    # PR drift gate noise even though no script is generating them.
    for stale_key in (
        "generated_at",
        "effective_status_computed_at",
        "invalidation_run_at",
        "load_bearing_computed_at",
    ):
        ledger.pop(stale_key, None)

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    summary = summarize(new_rows)
    summary["cycles_detected"] = len(cycles)
    summary["cycle_examples"] = cycles[:5]
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(f"Updated {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote   {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"  effective_status counts: {summary['effective_status_counts']}")
    print(f"  retained pending chain: {summary['retained_pending_chain_count']}")
    if summary["cycles_detected"]:
        print(f"  cycles detected: {summary['cycles_detected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
