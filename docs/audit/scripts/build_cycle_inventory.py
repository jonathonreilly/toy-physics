#!/usr/bin/env python3
"""Inventory citation-graph cycles using the audit lane's DFS color walk.

This intentionally mirrors the inline cycle detection in
compute_effective_status.py and audit_lint.py: a cycle is recorded whenever a
DFS edge reaches a GRAY node already on the active path. The output is an
archaeology worklist, not a graph-theory canonical cycle basis.
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
GRAPH_PATH = DATA_DIR / "citation_graph.json"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
OUT_PATH = DATA_DIR / "cycle_inventory.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def detect_cycles(nodes: dict[str, dict]) -> list[list[str]]:
    adj = {cid: list(node.get("deps", [])) for cid, node in nodes.items()}
    white, gray, black = 0, 1, 2
    color = {cid: white for cid in adj}
    cycles: list[list[str]] = []

    for start in adj:
        if color[start] != white:
            continue
        stack = [(start, iter(adj[start]))]
        path = [start]
        path_set = {start}
        color[start] = gray

        while stack:
            node, deps_iter = stack[-1]
            try:
                dep = next(deps_iter)
            except StopIteration:
                color[node] = black
                path.pop()
                path_set.discard(node)
                stack.pop()
                continue

            if dep not in adj:
                continue
            if color[dep] == gray:
                if dep in path_set:
                    cycle_start = path.index(dep)
                    cycles.append(list(path[cycle_start:]))
                continue
            if color[dep] == black:
                continue

            color[dep] = gray
            path.append(dep)
            path_set.add(dep)
            stack.append((dep, iter(adj[dep])))

    return cycles


def cycle_edges(cycle: list[str]) -> list[dict[str, str]]:
    if not cycle:
        return []
    return [
        {"from": src, "to": cycle[(idx + 1) % len(cycle)]}
        for idx, src in enumerate(cycle)
    ]


def main() -> int:
    graph = load_json(GRAPH_PATH)
    ledger = load_json(LEDGER_PATH)
    graph_nodes = graph.get("nodes", {})
    rows = ledger.get("rows", {})

    raw_cycles = detect_cycles(graph_nodes)
    inventory = []
    length_counts: Counter[int] = Counter()

    for cycle in raw_cycles:
        length = len(cycle)
        length_counts[length] += 1
        row_subset = [rows.get(cid, {}) for cid in cycle]
        max_desc = (
            max((row.get("transitive_descendants") or 0) for row in row_subset)
            if row_subset
            else 0
        )
        inventory.append(
            {
                "cycle_id": None,
                "length": length,
                "max_transitive_descendants": max_desc,
                "requires_lemma_extraction": False,
                "nodes": [
                    {
                        "claim_id": cid,
                        "note_path": rows.get(cid, {}).get("note_path")
                        or graph_nodes.get(cid, {}).get("path"),
                        "claim_type": rows.get(cid, {}).get("claim_type"),
                        "audit_status": rows.get(cid, {}).get("audit_status"),
                        "effective_status": rows.get(cid, {}).get("effective_status"),
                        "transitive_descendants": rows.get(cid, {}).get(
                            "transitive_descendants"
                        ),
                        "title": rows.get(cid, {}).get("title")
                        or graph_nodes.get(cid, {}).get("title"),
                    }
                    for cid in cycle
                ],
                "edges": cycle_edges(cycle),
                "decision": None,
            }
        )

    inventory.sort(
        key=lambda item: (
            -(item["max_transitive_descendants"] or 0),
            item["length"],
            [node["claim_id"] for node in item["nodes"]],
        )
    )
    for idx, item in enumerate(inventory, start=1):
        item["cycle_id"] = f"cycle-{idx:04d}"

    out = {
        "cycle_count": len(inventory),
        "length_counts": {str(k): v for k, v in sorted(length_counts.items())},
        "sort": [
            "max_transitive_descendants descending",
            "length ascending",
            "claim_id list ascending",
        ],
        "cycles": inventory,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  cycles: {len(inventory)}")
    print(f"  by length: {dict(sorted(length_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
