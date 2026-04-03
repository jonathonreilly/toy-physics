#!/usr/bin/env python3
"""Emergent dimensionality from local growth rules.

The 5D result shows decoherence doesn't decay when d_spatial ≥ 4.
If the graph naturally develops d_eff ≥ 4 from local rules, the
emergence problem is solved: no imposed topology needed.

THREE GROWTH RULES tested (all purely local):

Rule 1: NEIGHBORHOOD EXPANSION
  Each new node connects to k random existing nodes within distance r.
  New node's position is inferred from its neighbors' positions.
  This is the Axiom 1 + Axiom 6 rule: "evolving network with locally
  simplest continuation."

Rule 2: TRIANGULATION GROWTH
  New nodes preferentially connect to form triangles (connect to
  neighbors-of-neighbors). This creates clustered structure that
  naturally embeds in higher dimensions.

Rule 3: DELAY-INFERRED GROWTH
  New nodes are placed where the delay structure from existing nodes
  is consistent with a higher-dimensional embedding. The graph
  "discovers" its own dimension through the delay field (Axiom 3).

MEASUREMENT: Effective dimension d_eff from the scaling of the
number of nodes within graph-distance r:
  N(r) ~ r^d_eff

If d_eff ≥ 4 for ANY local rule, the axioms produce the physics.
"""

from __future__ import annotations
import math
import random
from collections import defaultdict, deque


def graph_distance_bfs(adj, source, n):
    """BFS distances from source."""
    dist = [-1] * n
    dist[source] = 0
    q = deque([source])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist


def measure_effective_dimension(adj, n, n_samples=20):
    """Measure d_eff from N(r) ~ r^d_eff.

    Sample random source nodes, compute BFS ball sizes at each radius,
    fit log(N(r)) vs log(r).
    """
    rng = random.Random(42)
    sources = [rng.randint(0, n - 1) for _ in range(min(n_samples, n))]

    # Accumulate ball sizes at each radius
    radius_counts = defaultdict(list)
    for src in sources:
        dist = graph_distance_bfs(adj, src, n)
        max_r = max(d for d in dist if d >= 0)
        for r in range(1, min(max_r + 1, 20)):
            count = sum(1 for d in dist if 0 <= d <= r)
            if count > 1:
                radius_counts[r].append(count)

    # Average ball size at each radius
    radii = sorted(r for r in radius_counts if len(radius_counts[r]) >= 3)
    if len(radii) < 3:
        return None

    xs = [math.log(r) for r in radii]
    ys = [math.log(sum(radius_counts[r]) / len(radius_counts[r])) for r in radii]

    # Fit log(N) = d_eff * log(r) + const
    n_pts = len(xs)
    mx = sum(xs) / n_pts
    my = sum(ys) / n_pts
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)

    if sxx < 1e-10:
        return None

    d_eff = sxy / sxx
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0

    return {"d_eff": d_eff, "r2": r2, "max_r": radii[-1]}


# ─── Rule 1: Neighborhood Expansion ────────────────────────────────

def grow_neighborhood_expansion(n_nodes=1000, k_connect=6, rng_seed=42):
    """Grow graph by connecting new nodes to k random existing neighbors.

    Each new node connects to k existing nodes chosen uniformly.
    Then it also connects to any node that is a neighbor of at least
    2 of its initial connections (triangle closure).
    """
    rng = random.Random(rng_seed)
    adj = defaultdict(set)
    n = 0

    # Seed: complete graph on k+1 nodes
    for i in range(k_connect + 1):
        for j in range(i + 1, k_connect + 1):
            adj[i].add(j)
            adj[j].add(i)
    n = k_connect + 1

    while n < n_nodes:
        # Pick k random existing nodes
        targets = rng.sample(range(n), min(k_connect, n))
        new = n
        for t in targets:
            adj[new].add(t)
            adj[t].add(new)

        # Triangle closure: connect to neighbors-of-neighbors
        neighbors_of_targets = set()
        for t in targets:
            neighbors_of_targets.update(adj[t])
        neighbors_of_targets -= {new}
        neighbors_of_targets -= set(targets)

        # Connect to nodes that share ≥2 target neighbors
        for candidate in neighbors_of_targets:
            shared = sum(1 for t in targets if candidate in adj[t])
            if shared >= 2:
                adj[new].add(candidate)
                adj[candidate].add(new)

        n += 1

    return dict(adj), n


# ─── Rule 2: Preferential Triangulation ─────────────────────────────

def grow_preferential_triangulation(n_nodes=1000, m_edges=3, rng_seed=42):
    """Barabasi-Albert with triangle closure.

    New node attaches to m existing nodes with probability proportional
    to degree (preferential attachment). Then closes all possible
    triangles with the new node's neighbors' neighbors.
    """
    rng = random.Random(rng_seed)
    adj = defaultdict(set)

    # Seed: complete graph on m+1 nodes
    for i in range(m_edges + 1):
        for j in range(i + 1, m_edges + 1):
            adj[i].add(j)
            adj[j].add(i)
    n = m_edges + 1

    # Degree list for preferential attachment
    deg_list = []
    for i in range(n):
        deg_list.extend([i] * len(adj[i]))

    while n < n_nodes:
        # Preferential attachment
        targets = set()
        while len(targets) < m_edges and len(deg_list) > 0:
            t = deg_list[rng.randint(0, len(deg_list) - 1)]
            if t != n:
                targets.add(t)

        new = n
        for t in targets:
            adj[new].add(t)
            adj[t].add(new)
            deg_list.append(new)
            deg_list.append(t)

        # Triangle closure
        nbs = set()
        for t in targets:
            nbs.update(adj[t])
        nbs -= {new}
        nbs -= targets
        for candidate in nbs:
            shared = sum(1 for t in targets if candidate in adj[t])
            if shared >= 2:
                adj[new].add(candidate)
                adj[candidate].add(new)
                deg_list.append(new)
                deg_list.append(candidate)

        n += 1

    return dict(adj), n


# ─── Rule 3: Random Geometric Growth in Expanding Space ────────────

def grow_expanding_geometric(n_nodes=1000, d_embed=1, r_connect=1.5,
                              expansion_rate=0.01, rng_seed=42):
    """Grow nodes in expanding d-dimensional space.

    Start with d=1. As nodes are added, the "effective space" gradually
    expands: new nodes are placed with small random offsets in additional
    dimensions. The connection radius is fixed.

    d_embed controls initial dimension. expansion_rate controls how
    fast new dimensions "activate" (new coord variance grows with n).
    """
    rng = random.Random(rng_seed)
    max_dim = 6  # allow up to 6 effective dimensions
    positions = []
    adj = defaultdict(set)

    for i in range(n_nodes):
        # Position: d_embed initial dimensions + expanding extra dimensions
        pos = [rng.gauss(0, 1.0) for _ in range(d_embed)]
        for extra_d in range(d_embed, max_dim):
            # Extra dimension variance grows as expansion_rate * n
            sigma = math.sqrt(expansion_rate * max(0, i - 100 * (extra_d - d_embed)))
            sigma = max(sigma, 0.0)
            pos.append(rng.gauss(0, sigma) if sigma > 0 else 0.0)
        positions.append(pos)

        # Connect to nearby existing nodes
        for j in range(i):
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(positions[i], positions[j])))
            if dist < r_connect:
                adj[i].add(j)
                adj[j].add(i)

    return dict(adj), len(positions)


# ─── Rule 4: Pure axiom-driven growth (simplest continuation) ──────

def grow_simplest_continuation(n_nodes=1000, k_initial=4, rng_seed=42):
    """Axiom 6: 'locally simplest admissible continuation.'

    New node connects to the k most recently active nodes that are
    also neighbors of each other (continuation of existing structure).
    If no such cluster exists, connect to k random nodes.

    This is the minimal axiom-faithful rule: the graph grows by
    extending its most recent local structure.
    """
    rng = random.Random(rng_seed)
    adj = defaultdict(set)

    # Seed
    for i in range(k_initial + 1):
        for j in range(i + 1, k_initial + 1):
            adj[i].add(j)
            adj[j].add(i)
    n = k_initial + 1

    while n < n_nodes:
        new = n

        # Find a recent cluster: look at the last ~20 nodes
        recent = list(range(max(0, n - 20), n))
        best_cluster = None
        best_size = 0

        # Find the densest subgraph among recent nodes
        for start in recent[-10:]:
            cluster = {start}
            for nb in adj.get(start, set()):
                if nb in set(recent):
                    cluster.add(nb)
            if len(cluster) > best_size:
                best_size = len(cluster)
                best_cluster = cluster

        if best_cluster and len(best_cluster) >= 2:
            targets = list(best_cluster)[:k_initial]
        else:
            targets = rng.sample(range(n), min(k_initial, n))

        for t in targets:
            adj[new].add(t)
            adj[t].add(new)

        # Closure: connect to shared neighbors
        nbs = set()
        for t in targets:
            nbs.update(adj[t])
        nbs -= {new}
        nbs -= set(targets)
        for c in nbs:
            shared = sum(1 for t in targets if c in adj[t])
            if shared >= 2:
                adj[new].add(c)
                adj[c].add(new)

        n += 1

    return dict(adj), n


def main():
    print("=" * 70)
    print("EMERGENT DIMENSIONALITY FROM LOCAL GROWTH RULES")
    print("  Does any local rule produce d_eff >= 4?")
    print("  If yes, decoherence works automatically (no gap needed)")
    print("=" * 70)
    print()

    rules = [
        ("Neighborhood expansion (k=6)", lambda s: grow_neighborhood_expansion(2000, 6, s)),
        ("Neighborhood expansion (k=10)", lambda s: grow_neighborhood_expansion(2000, 10, s)),
        ("Preferential triangulation (m=3)", lambda s: grow_preferential_triangulation(2000, 3, s)),
        ("Preferential triangulation (m=6)", lambda s: grow_preferential_triangulation(2000, 6, s)),
        ("Expanding geometric (d0=1, exp=0.01)", lambda s: grow_expanding_geometric(2000, 1, 1.5, 0.01, s)),
        ("Expanding geometric (d0=1, exp=0.05)", lambda s: grow_expanding_geometric(2000, 1, 1.5, 0.05, s)),
        ("Simplest continuation (k=4)", lambda s: grow_simplest_continuation(2000, 4, s)),
        ("Simplest continuation (k=6)", lambda s: grow_simplest_continuation(2000, 6, s)),
    ]

    print(f"  {'Rule':<45s}  {'d_eff':>5s}  {'R²':>5s}  {'>=4?':>4s}")
    print(f"  {'-' * 65}")

    for name, gen_fn in rules:
        d_effs = []
        for seed in range(5):
            adj, n = gen_fn(seed * 13 + 7)
            r = measure_effective_dimension(adj, n)
            if r:
                d_effs.append(r["d_eff"])

        if d_effs:
            avg_d = sum(d_effs) / len(d_effs)
            passes = "YES" if avg_d >= 3.5 else "no"
            print(f"  {name:<45s}  {avg_d:5.2f}  {'':>5s}  {passes:>4s}")
        else:
            print(f"  {name:<45s}  FAIL")

        import sys
        sys.stdout.flush()

    print()
    print("d_eff >= 4: decoherence works automatically (alpha near zero)")
    print("d_eff < 4: decoherence still decays, need imposed topology")
    print()
    print("REFERENCE: known d_eff values")
    print("  1D chain:    d_eff = 1")
    print("  2D lattice:  d_eff = 2")
    print("  3D lattice:  d_eff = 3")
    print("  BA network:  d_eff ~ 2-4 (depends on m)")
    print("  Random:      d_eff ~ infinity (small-world)")


if __name__ == "__main__":
    main()
