#!/usr/bin/env python3
"""Compute effective_status for every row in the audit ledger.

The propagation rule (from FRESH_LOOK_REQUIREMENTS.md):
  effective_status = the weaker of (this row's intrinsic status from its
  audit verdict, the minimum effective_status of all dependencies).

Intrinsic status mapping:
  - current_status=proposed_retained + audit_status=audited_clean -> retained
  - current_status=proposed_promoted + audit_status=audited_clean -> promoted
  - current_status=proposed_no_go    + audit_status=audited_clean -> retained_no_go
    (author declared a no-go theorem and the audit ratified it; symmetric
    path to `retained` for negative results — Coleman-Mandula, Kochen-Specker,
    Weinberg-Witten style claims born as no-gos rather than failed positives)
  - current_status=proposed_*        + audit_status=unaudited     -> proposed_*
  - audit_status=audited_failed AND note in archive_unlanded/      -> retained_no_go
    (legacy path: a positive claim failed audit and was archived. The audit
    verdict stays as audited_failed but the project-level interpretation
    lifts to retained_no_go. Going forward, prefer the proposed_no_go
    direct path above for new no-go theorems.)
  - current_status=proposed_*        + audit_status=audited_<fail> -> audited_<fail>
  - current_status in {support, bounded, open}                    -> as declared
  - current_status=unknown                                        -> unknown

Writes effective_status, effective_status_reason, and a summary back into
docs/audit/data/audit_ledger.json. Also emits docs/audit/data/effective_status_summary.json
with cluster statistics.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
SUMMARY_PATH = DATA_DIR / "effective_status_summary.json"

# Strength rank: higher = stronger publication-facing tier.
# retained_no_go sits at the same tier as retained: both are audit-ratified,
# durable scientific commitments. A retained no-go is a negative theorem
# (Coleman-Mandula, Kochen-Specker, Weinberg-Witten) that downstream rows
# can cite without weakening.
RANK = {
    "retained": 100,
    "retained_no_go": 100,
    "promoted": 90,
    "proposed_retained": 80,
    "proposed_no_go": 80,
    "proposed_promoted": 70,
    "bounded": 60,
    "support": 50,
    "open": 40,
    "unknown": 30,
    "audited_decoration": 20,
    "audited_numerical_match": 15,
    "audited_renaming": 10,
    "audited_conditional": 10,
    "audited_failed": 0,
}

AUDIT_PROMOTION = {
    "proposed_retained": "retained",
    "proposed_promoted": "promoted",
    "proposed_no_go": "retained_no_go",
}

# Verdicts that override the proposed tier and become the intrinsic status.
TERMINAL_AUDIT_STATUSES = {
    "audited_decoration",
    "audited_numerical_match",
    "audited_renaming",
    "audited_conditional",
    "audited_failed",
}


def intrinsic_status(row: dict) -> str:
    cs = row.get("current_status") or "unknown"
    a = row.get("audit_status") or "unaudited"
    if a == "audited_failed":
        # Terminal failed audits whose notes have been moved to archive_unlanded/
        # are retained as no-go theorems, not active failures. The audit verdict
        # stays as audited_failed (faithful to what Codex said about the
        # original positive claim), but the effective_status lifts to
        # retained_no_go to reflect that the project has accepted this lane is
        # closed and built it into institutional memory.
        note_path = row.get("note_path") or ""
        if note_path.startswith("archive_unlanded/"):
            if (REPO_ROOT / note_path).exists():
                return "retained_no_go"
    if a in TERMINAL_AUDIT_STATUSES:
        return a
    if a == "audited_clean":
        return AUDIT_PROMOTION.get(cs, cs)
    return cs  # unaudited / audit_in_progress: report what the author proposed


def weaker(a: str, b: str) -> str:
    """Return whichever of a, b has the lower rank. Ties prefer a."""
    return a if RANK.get(a, -1) <= RANK.get(b, -1) else b


def compute_effective(rows: dict[str, dict]) -> dict[str, dict]:
    """Compute effective_status for every row by topo-sorting on deps.

    Cycles are detected and broken by treating the cycle as a single
    component whose effective_status is the weakest intrinsic in the
    cycle, attributed reason 'cycle'.
    """
    # Index for quick lookup.
    intrinsic = {cid: intrinsic_status(r) for cid, r in rows.items()}

    # Use iterative DFS with a memo + WIP set to detect cycles.
    effective: dict[str, str] = {}
    reason: dict[str, str] = {}
    cycles: list[list[str]] = []

    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {cid: WHITE for cid in rows}

    def visit(start: str):
        stack = [(start, iter(rows[start].get("deps", [])))]
        path = [start]
        path_set = {start}
        color[start] = GRAY
        while stack:
            node, deps_iter = stack[-1]
            try:
                dep = next(deps_iter)
            except StopIteration:
                # Finalize this node.
                node_intrinsic = intrinsic[node]
                worst = node_intrinsic
                worst_source = "self"
                for d in rows[node].get("deps", []):
                    d_eff = effective.get(d, intrinsic.get(d, "unknown"))
                    if RANK.get(d_eff, -1) < RANK.get(worst, -1):
                        worst = d_eff
                        worst_source = f"inherited_from:{d}"
                effective[node] = worst
                reason[node] = worst_source
                color[node] = BLACK
                path.pop()
                path_set.discard(node)
                stack.pop()
                continue
            if dep not in rows:
                continue  # dangling citation; skip
            if color[dep] == GRAY:
                # Cycle detected.
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

    # Mark unfinished nodes (nodes inside cycles that didn't finalize).
    for cid in rows:
        if cid not in effective:
            effective[cid] = intrinsic[cid]
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
    for r in rows.values():
        e = r.get("effective_status", "unknown")
        eff_counts[e] = eff_counts.get(e, 0) + 1

    proposed_demoted_by_upstream = []
    for cid, r in rows.items():
        if r.get("intrinsic_status") in {
            "proposed_retained", "proposed_promoted", "proposed_no_go",
            "retained", "promoted", "retained_no_go",
        }:
            if r.get("effective_status") != r.get("intrinsic_status"):
                if r.get("effective_status_reason", "").startswith("inherited_from:"):
                    proposed_demoted_by_upstream.append(cid)

    return {
        "effective_status_counts": eff_counts,
        "proposed_demoted_by_upstream_count": len(proposed_demoted_by_upstream),
        "proposed_demoted_by_upstream_examples": sorted(proposed_demoted_by_upstream)[:25],
    }


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit(
            "audit_ledger.json missing; run seed_audit_ledger.py first"
        )
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    new_rows, cycles = compute_effective(rows)
    ledger["rows"] = new_rows
    ledger["effective_status_computed_at"] = datetime.now(timezone.utc).isoformat()

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    summary = summarize(new_rows)
    summary["computed_at"] = datetime.now(timezone.utc).isoformat()
    summary["cycles_detected"] = len(cycles)
    summary["cycle_examples"] = cycles[:5]
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(f"Updated {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote   {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"  effective_status counts: {summary['effective_status_counts']}")
    print(f"  proposed demoted by upstream: {summary['proposed_demoted_by_upstream_count']}")
    if summary["cycles_detected"]:
        print(f"  cycles detected: {summary['cycles_detected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
