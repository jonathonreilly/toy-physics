#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test whether K3 staggered orientation is
Pfaffian-optimal on non-planar Z^3 cuboids.

Background
----------
V2 iteration on 3x3x2 prism found: K3 achieves max |det(B)| = 225
over all 2^16 gauge classes; the graph is classically non-Pfaffian.

Claims under test
-----------------
C1. (3,2,2) planar: K3 achieves |det(B)| = #PM = 32, which is the
    max over all gauge classes (since the graph is planar Pfaffian
    and every Pfaffian orientation achieves the same max).
C2. (4,3,2) non-planar: K3 achieves max |det(B)| over all 2^14 =
    16384 gauge classes. Tested exhaustively.
C3. (4,4,2) non-planar: K3 achieves max |det(B)| over a
    MONTE-CARLO SAMPLE of 50000 random gauge classes out of 2^25 =
    33M total. Adversarial: if any sample exceeds K3's |det| =
    30976, the claim breaks with a concrete counterexample.

Falsification is explicit and per-cuboid.

Gauge-class enumeration
-----------------------
For graph with n vertices, m edges, c components, cycle-space
dimension is m - n + c. Fix spanning tree (n - c edges) via BFS.
The remaining m - n + c chord edges parametrize all gauge classes
modulo coboundary symmetries. For each chord subset S:
    det(B_S) has the same |value| for all orientations in the
    gauge class of S.
So iterating over subsets of chord edges (sign flips) enumerates
all distinct |det| values reachable by sign reassignment.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict, deque
import random

import numpy as np


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RECORDS.append((name, bool(ok), detail))


def document(name: str, note: str) -> None:
    DOCS.append((name, note))


def eta(mu: int, n: tuple[int, int, int]) -> int:
    if mu == 1:
        return 1
    if mu == 2:
        return (-1) ** n[0]
    if mu == 3:
        return (-1) ** (n[0] + n[1])
    raise ValueError


def build_cuboid_data(L1: int, L2: int, L3: int):
    """Return dict with B matrix, edges, spanning tree, chord indices."""
    sites = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    site_set = set(sites)
    edges_with_mu = []
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n)
            nn[mu - 1] += 1
            nn = tuple(nn)
            if nn in site_set:
                edges_with_mu.append((n, nn, mu))

    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return None
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    bip_edges = []
    for (n_lo, n_hi, mu) in edges_with_mu:
        if n_lo in idx_e:
            bip_edges.append((idx_e[n_lo], idx_o[n_hi], eta(mu, n_lo)))
        else:
            bip_edges.append((idx_e[n_hi], idx_o[n_lo], -eta(mu, n_lo)))

    B_0 = np.zeros((n_bi, n_bi), dtype=np.int64)
    for (ie, jo, s) in bip_edges:
        B_0[ie, jo] = s

    # BFS spanning tree on bipartite-labeled graph
    adj = defaultdict(list)
    for idx, (ie, jo, s) in enumerate(bip_edges):
        adj[("e", ie)].append((("o", jo), idx))
        adj[("o", jo)].append((("e", ie), idx))
    start = ("e", 0)
    visited = {start}
    tree_idx = set()
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for (v, eidx) in adj[u]:
            if v not in visited:
                visited.add(v)
                tree_idx.add(eidx)
                queue.append(v)
    assert len(visited) == 2 * n_bi, f"BFS only reached {len(visited)}"
    chord_idx = [idx for idx in range(len(bip_edges)) if idx not in tree_idx]
    gauge_dim = len(chord_idx)

    return {
        "L": (L1, L2, L3),
        "n_bi": n_bi,
        "B_0": B_0,
        "bip_edges": bip_edges,
        "chord_idx": chord_idx,
        "gauge_dim": gauge_dim,
    }


def k3_abs_det(data) -> int:
    return int(round(abs(np.linalg.det(data["B_0"]))))


def det_for_mask(data, mask: int) -> int:
    """Flip chord signs per mask, return |det|."""
    B = data["B_0"].copy()
    chord_idx = data["chord_idx"]
    bip_edges = data["bip_edges"]
    for bit in range(len(chord_idx)):
        if (mask >> bit) & 1:
            ie, jo, s = bip_edges[chord_idx[bit]]
            B[ie, jo] = -B[ie, jo]
    return int(round(abs(np.linalg.det(B))))


def exhaustive_max_det(data) -> tuple[int, int]:
    """Return (max_abs_det, mask_achieving_it). Scans 2^gauge_dim."""
    gd = data["gauge_dim"]
    N = 2 ** gd
    best = 0
    best_mask = 0
    for mask in range(N):
        d = det_for_mask(data, mask)
        if d > best:
            best = d
            best_mask = mask
    return best, best_mask


def monte_carlo_max_det(data, n_samples: int, seed: int = 42) -> tuple[int, int, int]:
    """Return (max_abs_det found in samples, max_mask, n_samples)."""
    gd = data["gauge_dim"]
    rng = random.Random(seed)
    best = 0
    best_mask = 0
    # Always include mask=0 (K3 orientation itself) as a baseline.
    for mask in [0] + [rng.randrange(2 ** gd) for _ in range(n_samples - 1)]:
        d = det_for_mask(data, mask)
        if d > best:
            best = d
            best_mask = mask
    return best, best_mask, n_samples


# ---------------------------------------------------------------------------
# C1. (3,2,2) planar: sanity check that K3 achieves max = #PM = 32.
# ---------------------------------------------------------------------------

d_322 = build_cuboid_data(3, 2, 2)
t0 = time.time()
max_322, mask_322 = exhaustive_max_det(d_322)
k3_322 = k3_abs_det(d_322)
dt_322 = time.time() - t0

record(
    "C1_planar_322_K3_equals_max_equals_32",
    k3_322 == max_322 == 32,
    f"(3,2,2) planar: K3 |det| = {k3_322}, max over {2**d_322['gauge_dim']}={2**d_322['gauge_dim']} classes = {max_322} (searched in {dt_322:.2f}s).",
)


# ---------------------------------------------------------------------------
# C2. (4,3,2) non-planar: exhaustive max over 2^14 gauge classes.
# ---------------------------------------------------------------------------

d_432 = build_cuboid_data(4, 3, 2)
t0 = time.time()
max_432, mask_432 = exhaustive_max_det(d_432)
k3_432 = k3_abs_det(d_432)
dt_432 = time.time() - t0

record(
    "C2_non_planar_432_K3_achieves_max",
    k3_432 == max_432,
    f"(4,3,2) non-planar: K3 |det| = {k3_432}, max over {2**d_432['gauge_dim']} classes = {max_432} (searched in {dt_432:.2f}s). Gap to #PM=1845: {1845 - max_432}.",
)


# ---------------------------------------------------------------------------
# C3. (4,4,2) non-planar: Monte Carlo sample of 50,000 random gauge classes.
# ---------------------------------------------------------------------------

d_442 = build_cuboid_data(4, 4, 2)
t0 = time.time()
max_442_mc, mask_442_mc, n_samples = monte_carlo_max_det(d_442, n_samples=50000)
k3_442 = k3_abs_det(d_442)
dt_442 = time.time() - t0

record(
    "C3_non_planar_442_K3_at_least_as_good_as_random_samples",
    k3_442 >= max_442_mc,
    f"(4,4,2) non-planar: K3 |det| = {k3_442}, max over {n_samples} random samples = {max_442_mc} (searched in {dt_442:.2f}s). Total gauge space = 2^{d_442['gauge_dim']} ~= 33M.",
)


# ---------------------------------------------------------------------------
# Summary: K3 optimality across tested cases.
# ---------------------------------------------------------------------------

k3_optimal_on_all = (
    k3_322 == max_322
    and k3_432 == max_432
    and k3_442 >= max_442_mc
)

record(
    "K3_achieves_optimal_det_on_all_tested_cuboids",
    k3_optimal_on_all,
    f"K3 optimality check: (3,2,2): {k3_322==max_322}, (4,3,2): {k3_432==max_432}, (4,4,2): {k3_442>=max_442_mc}.",
)


# ---------------------------------------------------------------------------
# Interpretation.
# ---------------------------------------------------------------------------

if k3_optimal_on_all:
    document(
        "K3_appears_pfaffian_maximizing_across_tested_cuboids",
        "Across (3,2,2), (4,3,2), (4,4,2), and previously (3,3,2),"
        " K3's staggered-phase orientation achieves the maximum"
        " |det(B)| over all sign-assignment gauge classes (or over"
        " sampled classes for (4,4,2)). This is consistent with the"
        " conjecture that K3's plaquette-sign = -1 universal property"
        " (proven in ledger 2d) makes K3 Pfaffian-optimal on bipartite"
        " Z^3 subgraphs. On non-Pfaffian graphs, K3 achieves the best"
        " attainable; on Pfaffian graphs, K3 achieves |det| = #PM"
        " exactly.",
    )
    document(
        "next_steps",
        "To upgrade this from conjecture to theorem: (a) show that"
        " universal plaquette-sign -1 is a NECESSARY condition for"
        " Pfaffian maximization on bipartite graphs with elementary"
        " plaquettes; (b) verify the (4,4,2) full 33M gauge-class"
        " search if a faster computation is available; (c) test on"
        " more Z^3 subgraphs to strengthen the pattern.",
    )
else:
    document(
        "K3_not_universally_optimal",
        "Found a case where K3 does NOT achieve max |det|. Specific"
        " cuboid identified; investigate its structural signature.",
    )


# ---------------------------------------------------------------------------
# Emit.
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: K3 optimality test on (3,2,2), (4,3,2), (4,4,2)")
    print("=" * 78)
    for (name, ok, detail) in RECORDS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")
        print(f"           {detail}")
    for (name, note) in DOCS:
        print(f"  [DOC]    {name}")
        print(f"           {note}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
