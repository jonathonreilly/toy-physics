#!/usr/bin/env python3
"""Compute load-bearing metrics and criticality tier for every claim.

The audit lane intentionally does NOT use author-declared flagship status
to drive criticality. The "flagship" concept is a publication-marketing
designation; if it were used here, unratified author judgment would set
the audit cost on everything upstream — exactly the bootstrap problem
the audit lane exists to break.

Criticality is therefore pure graph topology: how many other claims
(transitively) inherit from this one.

For each node:
  - direct_in_degree:        # of claims that directly cite this one
  - transitive_descendants:  # of claims reachable via reverse traversal
  - max_descendant_status:   strongest effective_status among descendants
  - load_bearing_score:      composite numeric score (topology only)
  - criticality:             critical / high / medium / leaf

Criticality thresholds (CRITICALITY_THRESHOLDS): a node is in a tier if
EITHER its direct in-degree OR its transitive-descendant count crosses
the corresponding threshold. The two-axis test exists because the
framework's citation graph is bimodal — most "high reach" nodes have
~100-280 descendants, with a wide gap below — so transitive count alone
puts hundreds of mid-graph claims in the same bucket as the actual roots.
Combining with direct in-degree distinguishes citation hubs from
inheritors.

  - critical: direct_in_degree >= 15  OR  transitive_descendants >= 250
  - high:     direct_in_degree >=  5  OR  transitive_descendants >= 100
  - medium:   direct_in_degree >=  2  OR  transitive_descendants >=   5
  - leaf:     everything else

Pipeline order: AFTER seed_audit_ledger.py and BEFORE
compute_effective_status.py. The criticality tier feeds the linter and
the audit queue.
"""
from __future__ import annotations

import json
from collections import deque
from datetime import datetime, timezone
from math import log2
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
GRAPH_PATH = DATA_DIR / "citation_graph.json"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
SUMMARY_PATH = DATA_DIR / "load_bearing_summary.json"

# Status strength rank used for max_descendant_status reporting only.
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
INV_RANK = {v: k for k, v in RANK.items()}

CRITICALITY_THRESHOLDS = {
    "critical_in_degree": 15,
    "critical_descendants": 250,
    "high_in_degree": 5,
    "high_descendants": 100,
    "medium_in_degree": 2,
    "medium_descendants": 5,
}


def rank_for_status(status: str | None) -> int:
    if status and status.startswith("decoration_under_"):
        return 70
    return RANK.get(status or "unaudited", -1)


def reverse_adjacency(graph: dict) -> dict[str, list[str]]:
    rev: dict[str, list[str]] = {cid: [] for cid in graph["nodes"]}
    for edge in graph["edges"]:
        rev[edge["to"]].append(edge["from"])
    return rev


def transitive_set(start: str, rev: dict[str, list[str]]) -> set[str]:
    """Return the set of all nodes reachable from start by walking reverse edges."""
    seen: set[str] = set()
    queue = deque([start])
    while queue:
        n = queue.popleft()
        for parent in rev.get(n, []):
            if parent in seen or parent == start:
                continue
            seen.add(parent)
            queue.append(parent)
    return seen


def criticality_for(transitive_count: int, direct_in_degree: int) -> str:
    t = CRITICALITY_THRESHOLDS
    if direct_in_degree >= t["critical_in_degree"] or transitive_count >= t["critical_descendants"]:
        return "critical"
    if direct_in_degree >= t["high_in_degree"] or transitive_count >= t["high_descendants"]:
        return "high"
    if direct_in_degree >= t["medium_in_degree"] or transitive_count >= t["medium_descendants"]:
        return "medium"
    return "leaf"


def compute_score(direct_in: int, transitive: int, max_desc_rank: int) -> float:
    """Topology-only score. No flagship bump.

    Rewards reach (log of descendant count), local importance (in-degree),
    and the strength of what you feed (max_desc_rank above bounded gets a
    small bonus so a node feeding strong claims ranks above a node feeding
    only weak ones at the same descendant count).
    """
    base = log2(1 + transitive)
    local = 0.5 * direct_in
    bounded_floor = max(0, max_desc_rank - RANK["retained_pending_chain"]) / 10.0
    return round(base + local + 2.0 * bounded_floor, 3)


def main() -> int:
    if not GRAPH_PATH.exists():
        raise SystemExit("citation_graph.json missing; run build_citation_graph.py first")
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    rev = reverse_adjacency(graph)
    nodes = graph["nodes"]
    rows = ledger.get("rows", {})

    # Compute metrics per claim.
    metrics: dict[str, dict] = {}
    for cid in nodes:
        descendants = transitive_set(cid, rev)
        max_rank = -1
        for d in descendants:
            row = rows.get(d, {})
            d_status = row.get("effective_status") or "unaudited"
            r = rank_for_status(d_status)
            if r > max_rank:
                max_rank = r
        if max_rank < 0:
            max_rank = RANK["unaudited"]
        metrics[cid] = {
            "direct_in_degree": len(rev.get(cid, [])),
            "transitive_descendants": len(descendants),
            "max_descendant_status": INV_RANK.get(max_rank, "unknown"),
            "max_descendant_status_rank": max_rank,
        }
        metrics[cid]["load_bearing_score"] = compute_score(
            direct_in=metrics[cid]["direct_in_degree"],
            transitive=metrics[cid]["transitive_descendants"],
            max_desc_rank=metrics[cid]["max_descendant_status_rank"],
        )
        metrics[cid]["criticality"] = criticality_for(
            metrics[cid]["transitive_descendants"],
            metrics[cid]["direct_in_degree"],
        )

    # Write metrics into the ledger rows. Strip any old flagship fields
    # left over from prior pipeline runs.
    OLD_FLAGSHIP_FIELDS = {
        "flagship_descendants",
        "flagship_descendant_ids",
        "gates_flagship",
    }
    for cid, row in rows.items():
        for k in OLD_FLAGSHIP_FIELDS:
            row.pop(k, None)
        m = metrics.get(cid)
        if m is None:
            continue
        for k, v in m.items():
            row[k] = v
        rows[cid] = row
    ledger["rows"] = rows
    # Do not write a timestamp here. The audit PR gate compares generated
    # files byte-for-byte, so ornamental timestamps make every run look stale.

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    crit_counts: dict[str, int] = {}
    for m in metrics.values():
        crit_counts[m["criticality"]] = crit_counts.get(m["criticality"], 0) + 1

    top_load_bearing = sorted(
        ((cid, m["load_bearing_score"], m["criticality"], m["transitive_descendants"]) for cid, m in metrics.items()),
        key=lambda t: -t[1],
    )[:25]

    summary = {
        "node_count": len(metrics),
        "criticality_counts": crit_counts,
        "top_25_by_load_bearing_score": [
            {
                "claim_id": cid,
                "load_bearing_score": score,
                "criticality": crit,
                "transitive_descendants": td,
            }
            for cid, score, crit, td in top_load_bearing
        ],
        "thresholds": CRITICALITY_THRESHOLDS,
        "flagship_signal_used": False,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(f"Updated {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote   {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"  thresholds: {CRITICALITY_THRESHOLDS}")
    print(f"  criticality (topology-only): {crit_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
