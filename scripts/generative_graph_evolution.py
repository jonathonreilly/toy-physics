#!/usr/bin/env python3
"""Generative graph evolution: the graph dynamics produce structure.

Instead of building a static grid and placing phenomena on it,
this prototype lets the graph GROW according to local rules, and
asks whether the resulting structure naturally produces:
1. Causal order (a DAG)
2. Persistent patterns (self-maintaining subgraphs)
3. Delay structure (effective geometry)

The evolution rule:
- Start with a seed event
- At each step, each active event can spawn new events
- New events link to their parent and to nearby existing events
- Whether a new event is created depends on the local "density"
  of existing events (self-regulation)

This is the simplest rule that could produce structure from dynamics.

PStack experiment: generative-graph
"""

from __future__ import annotations
import math
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def evolve_generative_graph(
    seed: tuple[float, float],
    steps: int,
    spawn_radius: float = 1.5,
    inhibit_radius: float = 0.8,
    max_neighbors: int = 6,
    rng_seed: int = 42,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[int]]:
    """Evolve a graph from a seed point using local rules.

    Rules:
    1. Each active node can spawn a new node at random position
       within spawn_radius
    2. A spawn is INHIBITED if there are already too many nodes
       within inhibit_radius (density regulation)
    3. New nodes connect to all existing nodes within spawn_radius
    4. Nodes become inactive after spawning (they've "used their turn")

    Returns: (positions, adjacency, spawn_step_for_each_node)
    """
    rng = random.Random(rng_seed)
    positions = [seed]
    adjacency: dict[int, list[int]] = defaultdict(list)
    spawn_step = [0]
    active = {0}

    for step in range(1, steps + 1):
        new_active = set()
        spawned_this_step = []

        for node_idx in list(active):
            px, py = positions[node_idx]

            # Check local density
            nearby = sum(1 for i, (qx, qy) in enumerate(positions)
                        if math.dist((px, py), (qx, qy)) < inhibit_radius and i != node_idx)

            if nearby >= max_neighbors:
                continue  # Too dense, don't spawn

            # Spawn a new node
            angle = rng.uniform(0, 2 * math.pi)
            dist = rng.uniform(0.5, spawn_radius)
            nx, ny = px + dist * math.cos(angle), py + dist * math.sin(angle)

            new_idx = len(positions)
            positions.append((nx, ny))
            spawn_step.append(step)
            spawned_this_step.append(new_idx)

            # Connect to parent
            adjacency[node_idx].append(new_idx)
            adjacency[new_idx].append(node_idx)

            # Connect to nearby existing nodes
            for i, (qx, qy) in enumerate(positions[:-1]):
                if i == node_idx:
                    continue
                if math.dist((nx, ny), (qx, qy)) < spawn_radius:
                    adjacency[new_idx].append(i)
                    adjacency[i].append(new_idx)

            new_active.add(new_idx)

        active = new_active

    return positions, dict(adjacency), spawn_step


def analyze_graph(positions, adjacency, spawn_step):
    """Analyze the generated graph for structure."""
    n = len(positions)
    if n == 0:
        return {}

    unique_edges = {
        (min(i, j), max(i, j))
        for i, neighbors in adjacency.items()
        for j in neighbors
        if i != j
    }

    # Degree distribution
    degrees = [len(adjacency.get(i, [])) for i in range(n)]

    # Is there a natural causal order? (spawn_step gives one)
    # Count each undirected edge once, then orient it by spawn order.
    forward = 0
    backward = 0
    same = 0
    for i, j in unique_edges:
        if spawn_step[j] > spawn_step[i]:
            forward += 1
        elif spawn_step[j] < spawn_step[i]:
            backward += 1
        else:
            same += 1

    # Clustering coefficient
    clustering = []
    for i in range(n):
        nbs = adjacency.get(i, [])
        if len(nbs) < 2:
            continue
        pairs = 0
        connected = 0
        for a in range(len(nbs)):
            for b in range(a + 1, len(nbs)):
                pairs += 1
                if nbs[b] in adjacency.get(nbs[a], []):
                    connected += 1
        if pairs > 0:
            clustering.append(connected / pairs)

    # Spatial extent
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]

    return {
        "n_nodes": n,
        "n_edges": len(unique_edges),
        "mean_degree": sum(degrees) / n,
        "max_degree": max(degrees),
        "min_degree": min(degrees),
        "forward_edges": forward,
        "backward_edges": backward,
        "same_step_edges": same,
        "dag_ratio": forward / max(len(unique_edges), 1),
        "mean_clustering": sum(clustering) / len(clustering) if clustering else 0,
        "x_range": max(xs) - min(xs),
        "y_range": max(ys) - min(ys),
    }


def main() -> None:
    print("=" * 72)
    print("GENERATIVE GRAPH EVOLUTION")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Basic growth with different parameters
    # =========================================================
    print("=" * 72)
    print("TEST 1: Growth under different parameters")
    print("=" * 72)
    print()

    configs = [
        ("default", 1.5, 0.8, 6),
        ("tight", 1.0, 0.5, 4),
        ("loose", 2.0, 1.0, 8),
        ("dense", 1.5, 0.8, 10),
        ("sparse", 1.5, 0.8, 3),
    ]

    for label, sr, ir, mn in configs:
        positions, adj, steps = evolve_generative_graph(
            (0.0, 0.0), steps=30, spawn_radius=sr,
            inhibit_radius=ir, max_neighbors=mn, rng_seed=42,
        )
        stats = analyze_graph(positions, adj, steps)
        print(f"  {label:>10s}: {stats['n_nodes']:4d} nodes, {stats['n_edges']:4d} edges, "
              f"deg={stats['mean_degree']:.1f}, cluster={stats['mean_clustering']:.3f}, "
              f"dag_ratio={stats['dag_ratio']:.3f}, extent={stats['x_range']:.1f}x{stats['y_range']:.1f}")

    # =========================================================
    # TEST 2: Does the graph produce a natural DAG?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Causal structure (is spawn order a natural DAG?)")
    print("=" * 72)
    print()

    positions, adj, steps = evolve_generative_graph(
        (0.0, 0.0), steps=50, spawn_radius=1.5,
        inhibit_radius=0.8, max_neighbors=6, rng_seed=42,
    )
    stats = analyze_graph(positions, adj, steps)

    print(f"  Total edges: {stats['n_edges']}")
    print(f"  Forward (parent→child): {stats['forward_edges']}")
    print(f"  Backward (child→parent): {stats['backward_edges']}")
    print(f"  Same-step: {stats['same_step_edges']}")
    print(f"  DAG ratio (forward / total): {stats['dag_ratio']:.4f}")
    print()
    print(f"  If DAG ratio > 0.5: spawn order provides a preferred time direction")
    print(f"  If DAG ratio ≈ 0.5: no preferred direction (symmetric)")

    # =========================================================
    # TEST 3: Does the graph self-regulate density?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: Density self-regulation")
    print("=" * 72)
    print()

    print("  Growth curve (nodes vs step):")
    for max_step in [10, 20, 30, 40, 50]:
        positions, adj, steps = evolve_generative_graph(
            (0.0, 0.0), steps=max_step, spawn_radius=1.5,
            inhibit_radius=0.8, max_neighbors=6, rng_seed=42,
        )
        stats = analyze_graph(positions, adj, steps)
        print(f"    step={max_step:3d}: {stats['n_nodes']:4d} nodes, "
              f"extent={stats['x_range']:.1f}x{stats['y_range']:.1f}, "
              f"density={stats['n_nodes'] / max(stats['x_range'] * stats['y_range'], 0.01):.2f} nodes/unit²")

    # =========================================================
    # TEST 4: Multiple seeds — does the graph converge to similar structure?
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 4: Seed independence (different random seeds)")
    print("=" * 72)
    print()

    print(f"  {'seed':>6s}  {'nodes':>6s}  {'edges':>6s}  {'mean_deg':>9s}  {'clustering':>11s}  {'dag_ratio':>10s}")
    print(f"  {'-' * 52}")

    for seed in [42, 123, 456, 789, 1000]:
        positions, adj, steps = evolve_generative_graph(
            (0.0, 0.0), steps=40, spawn_radius=1.5,
            inhibit_radius=0.8, max_neighbors=6, rng_seed=seed,
        )
        stats = analyze_graph(positions, adj, steps)
        print(f"  {seed:6d}  {stats['n_nodes']:6d}  {stats['n_edges']:6d}  "
              f"{stats['mean_degree']:9.2f}  {stats['mean_clustering']:11.4f}  "
              f"{stats['dag_ratio']:10.4f}")

    print()
    print("EVOLUTION COMPLETE")


if __name__ == "__main__":
    main()
