#!/usr/bin/env python3
"""Compute load-bearing metrics and criticality tier for every claim.

For each node in the citation graph:
  - direct_in_degree:        # of claims that directly cite this one
  - transitive_descendants:  # of claims reachable via reverse traversal
  - flagship_descendants:    descendants whose source note is flagship-tagged
  - gates_flagship:          flagship_descendants > 0
  - max_descendant_status:   strongest effective_status among descendants
  - load_bearing_score:      composite numeric score
  - criticality:             critical / high / medium / leaf

Criticality rules (set in CRITICALITY_THRESHOLDS):
  - critical: gates_flagship OR transitive_descendants >= 50
  - high:     transitive_descendants >= 10 (and not critical)
  - medium:   transitive_descendants >= 1
  - leaf:     transitive_descendants == 0

Writes results back into docs/audit/data/audit_ledger.json (per-row fields).
Writes summary to docs/audit/data/load_bearing_summary.json.

Pipeline order: run AFTER seed_audit_ledger.py and BEFORE
compute_effective_status.py. The criticality tier feeds the linter and
the audit queue.
"""
from __future__ import annotations

import json
import re
from collections import deque
from datetime import datetime, timezone
from math import log2
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
GRAPH_PATH = DATA_DIR / "citation_graph.json"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
SUMMARY_PATH = DATA_DIR / "load_bearing_summary.json"

# Detect flagship-tagged source notes by scanning their raw status text.
FLAGSHIP_PATTERN = re.compile(r"flagship|exact-target.*PMNS|3\+1\s+GR", re.IGNORECASE)

# Status strength rank used for max_descendant_status.
RANK = {
    "retained": 100,
    "promoted": 90,
    "proposed_retained": 80,
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
INV_RANK = {v: k for k, v in RANK.items()}

CRITICALITY_THRESHOLDS = {
    "critical_descendant_count": 50,
    "high_descendant_count": 10,
}


def is_flagship_node(node: dict) -> bool:
    raw = node.get("current_status_raw") or ""
    title = node.get("title") or ""
    return bool(FLAGSHIP_PATTERN.search(raw) or FLAGSHIP_PATTERN.search(title))


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


def criticality_for(transitive_count: int, gates_flagship: bool) -> str:
    if gates_flagship or transitive_count >= CRITICALITY_THRESHOLDS["critical_descendant_count"]:
        return "critical"
    if transitive_count >= CRITICALITY_THRESHOLDS["high_descendant_count"]:
        return "high"
    if transitive_count >= 1:
        return "medium"
    return "leaf"


def compute_score(direct_in: int, transitive: int, gates_flagship: bool, max_desc_rank: int) -> float:
    base = log2(1 + transitive)
    flagship_bump = 5.0 if gates_flagship else 0.0
    local = 0.5 * direct_in
    bounded_floor = max(0, max_desc_rank - RANK["bounded"]) / 10.0
    return round(base + flagship_bump + local + 2.0 * bounded_floor, 3)


def main() -> int:
    if not GRAPH_PATH.exists():
        raise SystemExit("citation_graph.json missing; run build_citation_graph.py first")
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    rev = reverse_adjacency(graph)
    nodes = graph["nodes"]

    # Identify flagship nodes once.
    flagship_set = {cid for cid, n in nodes.items() if is_flagship_node(n)}

    rows = ledger.get("rows", {})

    # Compute metrics per claim.
    metrics: dict[str, dict] = {}
    for cid in nodes:
        descendants = transitive_set(cid, rev)
        flagship_descendants = descendants & flagship_set
        # max descendant status from the ledger's current effective_status.
        # If effective_status hasn't been computed yet, fall back to current_status.
        max_rank = -1
        for d in descendants:
            row = rows.get(d, {})
            d_status = row.get("effective_status") or row.get("current_status") or "unknown"
            r = RANK.get(d_status, -1)
            if r > max_rank:
                max_rank = r
        if max_rank < 0:
            max_rank = RANK["unknown"]
        metrics[cid] = {
            "direct_in_degree": len(rev.get(cid, [])),
            "transitive_descendants": len(descendants),
            "flagship_descendants": len(flagship_descendants),
            "flagship_descendant_ids": sorted(flagship_descendants),
            "gates_flagship": len(flagship_descendants) > 0,
            "max_descendant_status": INV_RANK.get(max_rank, "unknown"),
            "max_descendant_status_rank": max_rank,
        }
        metrics[cid]["load_bearing_score"] = compute_score(
            direct_in=metrics[cid]["direct_in_degree"],
            transitive=metrics[cid]["transitive_descendants"],
            gates_flagship=metrics[cid]["gates_flagship"],
            max_desc_rank=metrics[cid]["max_descendant_status_rank"],
        )
        metrics[cid]["criticality"] = criticality_for(
            metrics[cid]["transitive_descendants"],
            metrics[cid]["gates_flagship"],
        )

    # Write metrics into the ledger rows.
    for cid, row in rows.items():
        m = metrics.get(cid)
        if m is None:
            continue
        for k, v in m.items():
            row[k] = v
        rows[cid] = row
    ledger["rows"] = rows
    ledger["load_bearing_computed_at"] = datetime.now(timezone.utc).isoformat()

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    # Summary.
    crit_counts: dict[str, int] = {}
    flagship_count = 0
    for m in metrics.values():
        crit_counts[m["criticality"]] = crit_counts.get(m["criticality"], 0) + 1
        if m["gates_flagship"]:
            flagship_count += 1

    top_load_bearing = sorted(
        ((cid, m["load_bearing_score"], m["criticality"], m["transitive_descendants"], m["gates_flagship"]) for cid, m in metrics.items()),
        key=lambda t: -t[1],
    )[:25]

    summary = {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "node_count": len(metrics),
        "flagship_node_count": len(flagship_set),
        "flagship_node_ids": sorted(flagship_set),
        "gates_flagship_count": flagship_count,
        "criticality_counts": crit_counts,
        "top_25_by_load_bearing_score": [
            {
                "claim_id": cid,
                "load_bearing_score": score,
                "criticality": crit,
                "transitive_descendants": td,
                "gates_flagship": gf,
            }
            for cid, score, crit, td, gf in top_load_bearing
        ],
        "thresholds": CRITICALITY_THRESHOLDS,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    print(f"Updated {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote   {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"  flagship-tagged source notes: {len(flagship_set)}")
    print(f"  gates_flagship claims: {flagship_count}")
    print(f"  criticality: {crit_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
