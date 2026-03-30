#!/usr/bin/env python3
"""Quantify how much the causal DAG changes when barrier nodes are
added or removed.

Measures: edge count difference, affected node fraction, arrival time
shifts, and whether the DAG change magnitude correlates with the
Sorkin I_3 magnitude.

PStack experiment: dag-reconfiguration
"""

from __future__ import annotations
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
)


def build_dag_for_slits(
    width: int, height: int, open_slits: set[int],
) -> tuple[dict, dict[tuple[int, int], float], set[tuple[int, int]]]:
    """Build DAG with specific slits open. Returns (dag, arrival_times, nodes)."""
    barrier_x = width // 2
    blocked = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in open_slits
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked)
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    source = (1, 0)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    return dag, arrival_times, nodes


def dag_edges(dag: dict) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    """Extract all edges as a set of (from, to) tuples."""
    edges = set()
    for node, neighbors in dag.items():
        for nb in neighbors:
            edges.add((node, nb))
    return edges


def compare_dags(
    dag_a: dict, times_a: dict, nodes_a: set,
    dag_b: dict, times_b: dict, nodes_b: set,
    label: str,
) -> dict:
    """Compare two DAGs and return metrics."""
    edges_a = dag_edges(dag_a)
    edges_b = dag_edges(dag_b)

    shared_nodes = nodes_a & nodes_b
    only_a = nodes_a - nodes_b
    only_b = nodes_b - nodes_a

    edges_only_a = edges_a - edges_b
    edges_only_b = edges_b - edges_a
    edges_shared = edges_a & edges_b

    # Arrival time shifts on shared nodes
    time_diffs = []
    for node in shared_nodes:
        if node in times_a and node in times_b:
            time_diffs.append(abs(times_a[node] - times_b[node]))

    max_time_shift = max(time_diffs) if time_diffs else 0.0
    mean_time_shift = sum(time_diffs) / len(time_diffs) if time_diffs else 0.0
    nonzero_shifts = sum(1 for d in time_diffs if d > 1e-10)

    result = {
        "label": label,
        "nodes_a": len(nodes_a),
        "nodes_b": len(nodes_b),
        "nodes_only_a": len(only_a),
        "nodes_only_b": len(only_b),
        "edges_a": len(edges_a),
        "edges_b": len(edges_b),
        "edges_only_a": len(edges_only_a),
        "edges_only_b": len(edges_only_b),
        "edges_shared": len(edges_shared),
        "edge_change_frac": (len(edges_only_a) + len(edges_only_b)) / max(len(edges_a) + len(edges_b), 1),
        "max_time_shift": max_time_shift,
        "mean_time_shift": mean_time_shift,
        "nonzero_time_shifts": nonzero_shifts,
        "frac_nodes_shifted": nonzero_shifts / max(len(shared_nodes), 1),
    }
    return result


def main() -> None:
    width = 20
    height = 10

    print("=" * 80)
    print("DAG RECONFIGURATION MEASUREMENT")
    print("=" * 80)
    print(f"width={width}, height={height}")
    print()

    # Define the three slits
    configs = [
        ("SYMMETRIC", -4, 0, 4),
        ("CLOSE", -2, 0, 2),
        ("WIDE", -6, 0, 6),
    ]

    for label, ya, yb, yc in configs:
        print(f"\n{'=' * 70}")
        print(f"CONFIG: {label} (A={ya}, B={yb}, C={yc})")
        print(f"{'=' * 70}")

        # Build DAGs for all 7 Sorkin combinations
        dag_ABC, t_ABC, n_ABC = build_dag_for_slits(width, height, {ya, yb, yc})
        dag_AB, t_AB, n_AB = build_dag_for_slits(width, height, {ya, yb})
        dag_AC, t_AC, n_AC = build_dag_for_slits(width, height, {ya, yc})
        dag_BC, t_BC, n_BC = build_dag_for_slits(width, height, {yb, yc})
        dag_A, t_A, n_A = build_dag_for_slits(width, height, {ya})
        dag_B, t_B, n_B = build_dag_for_slits(width, height, {yb})
        dag_C, t_C, n_C = build_dag_for_slits(width, height, {yc})

        # Compare: how much does DAG change when adding one slit?
        comparisons = [
            ("AB → ABC (add C)", dag_AB, t_AB, n_AB, dag_ABC, t_ABC, n_ABC),
            ("AC → ABC (add B)", dag_AC, t_AC, n_AC, dag_ABC, t_ABC, n_ABC),
            ("BC → ABC (add A)", dag_BC, t_BC, n_BC, dag_ABC, t_ABC, n_ABC),
            ("A → AB (add B)", dag_A, t_A, n_A, dag_AB, t_AB, n_AB),
            ("A → ABC (add B,C)", dag_A, t_A, n_A, dag_ABC, t_ABC, n_ABC),
        ]

        print(f"\n  {'comparison':>25s}  {'Δnodes':>7s}  {'Δedges':>7s}  {'edge_chg%':>9s}  "
              f"{'max_Δt':>8s}  {'mean_Δt':>8s}  {'shifted%':>8s}")
        print(f"  {'-' * 85}")

        for comp_label, d1, t1, n1, d2, t2, n2 in comparisons:
            r = compare_dags(d1, t1, n1, d2, t2, n2, comp_label)
            delta_nodes = r["nodes_only_b"] - r["nodes_only_a"]
            delta_edges = r["edges_only_b"] - r["edges_only_a"]
            print(f"  {comp_label:>25s}  {delta_nodes:7d}  {delta_edges:7d}  "
                  f"{r['edge_change_frac']*100:8.2f}%  "
                  f"{r['max_time_shift']:8.4f}  {r['mean_time_shift']:8.4f}  "
                  f"{r['frac_nodes_shifted']*100:7.2f}%")

        # Also measure: full DAG stats
        print(f"\n  DAG statistics:")
        for slabel, d, t, n in [("ABC", dag_ABC, t_ABC, n_ABC),
                                  ("A", dag_A, t_A, n_A),
                                  ("B", dag_B, t_B, n_B)]:
            e = dag_edges(d)
            print(f"    {slabel:>5s}: {len(n)} nodes, {len(e)} edges, "
                  f"mean_degree={2*len(e)/max(len(n),1):.2f}")

    # Compare the DAG change magnitude across configs
    print(f"\n\n{'=' * 70}")
    print("CROSS-CONFIG COMPARISON: DAG change vs I_3 magnitude")
    print(f"{'=' * 70}")
    print()
    print("From original Sorkin test:")
    print("  Symmetric: I_3/P = 1.67e+06")
    print("  Close:     I_3/P = 9.19e+01")
    print("  Wide:      I_3/P = 4.61e+09")
    print()
    print("DAG change when adding third slit (AB → ABC):")

    for label, ya, yb, yc in configs:
        dag_AB, t_AB, n_AB = build_dag_for_slits(width, height, {ya, yb})
        dag_ABC, t_ABC, n_ABC = build_dag_for_slits(width, height, {ya, yb, yc})
        r = compare_dags(dag_AB, t_AB, n_AB, dag_ABC, t_ABC, n_ABC, label)
        print(f"  {label:>12s}: edge_change={r['edge_change_frac']*100:.2f}%, "
              f"max_Δt={r['max_time_shift']:.4f}, shifted_nodes={r['frac_nodes_shifted']*100:.1f}%")

    print("\n\nMEASUREMENT COMPLETE")


if __name__ == "__main__":
    main()
