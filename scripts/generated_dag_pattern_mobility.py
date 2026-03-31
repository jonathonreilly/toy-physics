#!/usr/bin/env python3
"""Can persistent patterns TRANSLATE on generated causal DAGs?

On rectangular grids, Life gliders translate because the grid has
exact translation symmetry. Generated DAGs have NO such symmetry —
irregular connectivity, random positions, forward-only causality.

This tests whether ANY self-maintenance rule + seed combination
produces a translating pattern on generated DAGs. If yes: inertial
motion is a property of the dynamics, not the lattice. If no:
mobility requires translation symmetry that random graphs lack.

Approach:
1. Generate DAGs with various parameters
2. Build undirected neighbor graphs from the DAG's spatial structure
3. Run various CA rules on these neighbor graphs
4. Track centroid motion — does anything translate?

The key challenge: on a generated DAG, the "neighbor" relation is
based on spatial proximity, not lattice adjacency. The CA rule
operates on whoever is nearby, regardless of the DAG's causal edges.

PStack experiment: generated-dag-mobility
"""

from __future__ import annotations
import math
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def build_spatial_neighbors(positions, radius):
    """Build undirected neighbor graph based on spatial proximity."""
    n = len(positions)
    neighbors: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if math.dist(positions[i], positions[j]) <= radius:
                neighbors[i].append(j)
                neighbors[j].append(i)
    return dict(neighbors)


def evolve_on_graph(
    n_nodes: int,
    neighbors: dict[int, list[int]],
    seed: frozenset[int],
    survive: frozenset[int],
    birth: frozenset[int],
    steps: int,
) -> list[frozenset[int]]:
    """Run CA rule on arbitrary graph with given neighbor structure."""
    active = set(seed)
    history = []

    for _ in range(steps):
        history.append(frozenset(active))
        counts: dict[int, int] = defaultdict(int)
        for node in active:
            for nb in neighbors.get(node, []):
                counts[nb] += 1

        new_active = set()
        # Check all nodes that are active or adjacent to active
        candidates = set(active)
        for node in active:
            candidates.update(neighbors.get(node, []))

        for node in candidates:
            c = counts.get(node, 0)
            if node in active and c in survive:
                new_active.add(node)
            elif node not in active and c in birth:
                new_active.add(node)

        active = new_active

    return history


def centroid(positions, state):
    if not state:
        return (0.0, 0.0)
    xs = [positions[i][0] for i in state]
    ys = [positions[i][1] for i in state]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def classify_motion(positions, history):
    if not history or len(history[-1]) == 0:
        return "DEAD", 0.0, 0.0
    centroids = [centroid(positions, s) for s in history]
    dx = centroids[-1][0] - centroids[0][0]
    dy = centroids[-1][1] - centroids[0][1]
    disp = math.sqrt(dx**2 + dy**2)

    if disp < 1.0:
        return "STATIC", disp, 0.0

    # Check persistence: do both halves move in the same direction?
    mid = len(centroids) // 2
    first_dx = centroids[mid][0] - centroids[0][0]
    first_dy = centroids[mid][1] - centroids[0][1]
    second_dx = centroids[-1][0] - centroids[mid][0]
    second_dy = centroids[-1][1] - centroids[mid][1]
    dot = first_dx * second_dx + first_dy * second_dy

    if dot > 0 and disp > 3.0:
        speed = disp / len(history)
        return "TRANSLATING", disp, speed
    elif disp > 2.0:
        return "DRIFTING", disp, disp / len(history)
    else:
        return "STATIC", disp, 0.0


def main() -> None:
    print("=" * 80)
    print("PATTERN MOBILITY ON GENERATED CAUSAL DAGs")
    print("  Can patterns translate without lattice symmetry?")
    print("=" * 80)
    print()

    rules = [
        ("S={2,3} B={3}", frozenset({2, 3}), frozenset({3})),
        ("S={3,4} B={3,4}", frozenset({3, 4}), frozenset({3, 4})),
        ("S={2,3,4} B={3}", frozenset({2, 3, 4}), frozenset({3})),
        ("S={2,3} B={3,6}", frozenset({2, 3}), frozenset({3, 6})),
        ("S={1,2,3} B={3}", frozenset({1, 2, 3}), frozenset({3})),
        ("S={2,3,4,5} B={4}", frozenset({2, 3, 4, 5}), frozenset({4})),
    ]

    graph_configs = [
        (25, 20, 8.0, 2.5, "dense-25"),
        (25, 20, 8.0, 1.8, "sparse-25"),
        (15, 30, 8.0, 2.0, "wide-15"),
        (30, 15, 6.0, 2.5, "long-30"),
    ]

    neighbor_radii = [1.5, 2.0, 2.5]
    steps = 60

    total_tested = 0
    translating_found = []

    for g_layers, g_npl, g_yr, g_cr, g_label in graph_configs:
        for graph_seed in range(5):
            positions, adj, arrival = generate_causal_dag(
                n_layers=g_layers, nodes_per_layer=g_npl,
                y_range=g_yr, connect_radius=g_cr, rng_seed=graph_seed,
            )
            n = len(positions)

            for nb_radius in neighbor_radii:
                spatial_nb = build_spatial_neighbors(positions, nb_radius)

                # Try various seed patterns (small clusters at different positions)
                seed_positions = [
                    (g_layers // 4, 0.0),
                    (g_layers // 4, 3.0),
                    (g_layers // 2, 0.0),
                ]

                for sx, sy in seed_positions:
                    # Find 5 nearest nodes to seed position
                    dists = [(i, math.dist(positions[i], (sx, sy))) for i in range(n)]
                    dists.sort(key=lambda x: x[1])
                    seed_nodes = frozenset(i for i, _ in dists[:5])

                    for rule_name, survive, birth in rules:
                        total_tested += 1
                        history = evolve_on_graph(
                            n, spatial_nb, seed_nodes, survive, birth, steps
                        )
                        motion, disp, speed = classify_motion(positions, history)

                        if motion == "TRANSLATING":
                            sizes = [len(s) for s in history]
                            c0 = centroid(positions, history[0])
                            cf = centroid(positions, history[-1])
                            translating_found.append({
                                "graph": g_label, "graph_seed": graph_seed,
                                "nb_radius": nb_radius, "rule": rule_name,
                                "seed_pos": (sx, sy), "disp": disp, "speed": speed,
                                "sizes": sizes[:10], "c0": c0, "cf": cf,
                            })

    print(f"Total configurations tested: {total_tested}")
    print(f"Translating patterns found: {len(translating_found)}")
    print()

    if translating_found:
        print("=" * 80)
        print("TRANSLATING PATTERNS ON GENERATED DAGs")
        print("=" * 80)
        print()
        for t in translating_found[:10]:
            print(f"  {t['graph']} seed={t['graph_seed']}, nb_r={t['nb_radius']}, "
                  f"{t['rule']}")
            print(f"    displacement={t['disp']:.2f}, speed={t['speed']:.4f}")
            print(f"    centroid: ({t['c0'][0]:.1f},{t['c0'][1]:.1f}) → "
                  f"({t['cf'][0]:.1f},{t['cf'][1]:.1f})")
            print(f"    sizes: {t['sizes']}")
            print()
    else:
        print("NO TRANSLATING PATTERNS found on generated DAGs.")
        print()
        print("This means mobility requires lattice translation symmetry")
        print("that random graphs don't have. Moving objects on generated")
        print("graphs would need a DIFFERENT mechanism than CA gliders.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
