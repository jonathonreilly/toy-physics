#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test K3 plaquette-uniqueness theorem on a
topologically NON-CONTRACTIBLE Z^3 subgraph.

Background
----------
Prior V2 iteration proved: on every Z^3 CUBOID, the plaquette-
satisfying gauge class is unique = K3, via Euler's formula
chi = |V| - |E| + |F| - |cubes| = 1 on contractible 3-space. This
gave plaquette_rank = gauge_dim = |E| - |V| + 1, hence uniqueness.

Claim under adversarial test
----------------------------
Remove the central column {(1,1,0), (1,1,1)} from a (3,3,2)
cuboid. The resulting "ring" graph is homotopy-equivalent to a
circle (not contractible), so chi = 0 and |F| - |cubes| <
|E| - |V| + 1. Hence MULTIPLE plaquette-satisfying gauge classes
should exist.

The question: do these multiple classes all achieve the SAME
|det(B)|? If yes, the "plaquette-satisfying => max |det|"
conjecture extends even to non-contractible cases. If they
DIFFER, the conjecture is tied to contractibility -- a scope
limit on K3 optimality.

V2 adversarial structure
------------------------
- Build the ring graph.
- Compute Euler characteristic (expect 0).
- Compute plaquette-incidence rank (expect < gauge_dim).
- Enumerate all 2^(gauge_dim) gauge classes.
- For each, check plaquette-satisfying status and |det(B)|.
- Among plaquette-satisfying classes: do all give same |det|?
- Among all classes: is the max |det| achieved ONLY by
  plaquette-satisfying, or do violating classes tie/exceed?

Any deviation from "multiple plaquette-satisfying classes all
agree on |det| and match the max" is falsification.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict, deque

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


def f2_rank(M: np.ndarray) -> int:
    """Rank over F_2 via Gaussian elimination."""
    A = (M.copy() % 2).astype(np.int8)
    n_rows, n_cols = A.shape
    rank = 0
    row = 0
    col = 0
    while row < n_rows and col < n_cols:
        pivot = None
        for r in range(row, n_rows):
            if A[r, col] == 1:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
        for r in range(n_rows):
            if r != row and A[r, col] == 1:
                A[r] = (A[r] + A[row]) % 2
        rank += 1
        row += 1
        col += 1
    return rank


# ---------------------------------------------------------------------------
# Build ring graph: (3,3,2) minus {(1,1,0), (1,1,1)}.
# ---------------------------------------------------------------------------

removed = {(1, 1, 0), (1, 1, 1)}
base_sites = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
sites = [v for v in base_sites if v not in removed]
site_set = set(sites)
n_V = len(sites)

edges = []
edge_index = {}
for n in sites:
    for mu in (1, 2, 3):
        nn = list(n)
        nn[mu - 1] += 1
        nn = tuple(nn)
        if nn in site_set:
            idx = len(edges)
            edges.append((n, nn, mu))
            edge_index[frozenset({n, nn})] = idx
n_E = len(edges)

# Plaquettes
plaquettes = []
for n in base_sites:
    for i in (1, 2, 3):
        for j in range(i + 1, 4):
            n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
            n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
            n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
            corners = {n, n_i, n_j, n_ij}
            if all(c in site_set for c in corners):
                e1 = frozenset({n, n_i})
                e2 = frozenset({n, n_j})
                e3 = frozenset({n_i, n_ij})
                e4 = frozenset({n_j, n_ij})
                if all(e in edge_index for e in (e1, e2, e3, e4)):
                    plaquettes.append(
                        [edge_index[e1], edge_index[e2], edge_index[e3], edge_index[e4]]
                    )
n_F = len(plaquettes)

# Cubes (1x1x1 blocks of 8 vertices all present)
cube_count = 0
for n in base_sites:
    i, j, k = n
    if i + 1 < 3 and j + 1 < 3 and k + 1 < 2:
        cube_corners = [
            (i + di, j + dj, k + dk)
            for di in (0, 1) for dj in (0, 1) for dk in (0, 1)
        ]
        if all(c in site_set for c in cube_corners):
            cube_count += 1

euler = n_V - n_E + n_F - cube_count

record(
    "ring_graph_vertex_edge_face_cube_counts",
    n_V == 16,
    f"Ring graph: V={n_V}, E={n_E}, F={n_F}, cubes={cube_count}. chi = V - E + F - cubes = {euler}.",
)

record(
    "ring_graph_is_non_contractible_chi_zero",
    euler == 0,
    f"Euler characteristic = {euler} (expected 0 for homotopy-circle).",
)


# ---------------------------------------------------------------------------
# Bipartite check
# ---------------------------------------------------------------------------

evens = [v for v in sites if sum(v) % 2 == 0]
odds = [v for v in sites if sum(v) % 2 == 1]
record(
    "ring_graph_bipartite_balanced",
    len(evens) == len(odds),
    f"|even|={len(evens)}, |odd|={len(odds)} (balanced required for PMs).",
)

idx_e = {v: i for i, v in enumerate(evens)}
idx_o = {v: i for i, v in enumerate(odds)}
n_bi = len(evens)
assert n_bi == 8

# Build B_0 and bipartite edges
bip_edges = []
for (n_lo, n_hi, mu) in edges:
    if n_lo in idx_e:
        bip_edges.append((idx_e[n_lo], idx_o[n_hi], eta(mu, n_lo)))
    else:
        bip_edges.append((idx_e[n_hi], idx_o[n_lo], -eta(mu, n_lo)))

B_0 = np.zeros((n_bi, n_bi), dtype=np.int64)
for (ie, jo, s) in bip_edges:
    B_0[ie, jo] = s

det_K3 = int(round(abs(np.linalg.det(B_0))))


# ---------------------------------------------------------------------------
# BFS spanning tree; gauge_dim; plaquette rank
# ---------------------------------------------------------------------------

adj = defaultdict(list)
for idx, (a, b, _) in enumerate(edges):
    adj[a].append((b, idx))
    adj[b].append((a, idx))
start = sites[0]
visited = {start}
tree_idx = set()
queue = deque([start])
while queue:
    u = queue.popleft()
    for (v, ei) in adj[u]:
        if v not in visited:
            visited.add(v)
            tree_idx.add(ei)
            queue.append(v)

connected = (len(visited) == n_V)
record(
    "ring_graph_connected",
    connected,
    f"BFS reached {len(visited)}/{n_V} vertices.",
)

chord_idx = [idx for idx in range(n_E) if idx not in tree_idx]
gauge_dim = len(chord_idx)
record(
    "ring_graph_gauge_dim_equals_E_minus_V_plus_1",
    gauge_dim == n_E - n_V + 1,
    f"gauge_dim = {gauge_dim} = |E|-|V|+1 = {n_E - n_V + 1}.",
)

# Plaquette-chord incidence matrix
chord_to_bit = {c: b for b, c in enumerate(chord_idx)}
M = np.zeros((n_F, gauge_dim), dtype=np.int8)
for p_idx, p_edges in enumerate(plaquettes):
    for e in p_edges:
        if e in chord_to_bit:
            M[p_idx, chord_to_bit[e]] = 1

plaq_rank = f2_rank(M)
n_sat = 2 ** (gauge_dim - plaq_rank)

record(
    "plaquette_rank_less_than_gauge_dim_as_predicted",
    plaq_rank < gauge_dim,
    f"plaquette_rank = {plaq_rank}, gauge_dim = {gauge_dim}. Predicted 2^{gauge_dim - plaq_rank} = {n_sat} plaquette-satisfying classes.",
)


# ---------------------------------------------------------------------------
# Enumerate all 2^gauge_dim classes; classify.
# ---------------------------------------------------------------------------

N = 2 ** gauge_dim
sat_classes = []  # list of (mask, |det|)
violating_dets = []

# Per-plaquette sign after flips: check via bit-popcount on chord membership.
plaq_chord_masks = []
for p_edges in plaquettes:
    pm = 0
    for e in p_edges:
        if e in chord_to_bit:
            pm |= (1 << chord_to_bit[e])
    plaq_chord_masks.append(pm)

# K3 satisfies all plaquettes. Flipping chords at bits of mask, a plaquette
# P's sign changes by (-1)^popcount(mask & plaq_chord_masks[p]).
# Plaquette still -1 iff popcount(mask & plaq_chord_masks[p]) is even.

t0 = time.time()
for mask in range(N):
    all_satisfying = True
    for pm in plaq_chord_masks:
        v = mask & pm
        # popcount parity
        parity = 0
        while v:
            parity ^= (v & 1)
            v >>= 1
        if parity:
            all_satisfying = False
            break

    # Compute |det|
    B = B_0.copy()
    for bit in range(gauge_dim):
        if (mask >> bit) & 1:
            idx = chord_idx[bit]
            # Find this edge in bip_edges
            ie, jo, s = bip_edges[idx]
            B[ie, jo] *= -1
    det_abs = int(round(abs(np.linalg.det(B))))

    if all_satisfying:
        sat_classes.append((mask, det_abs))
    else:
        violating_dets.append((mask, det_abs))
elapsed = time.time() - t0

record(
    "enumeration_finished",
    len(sat_classes) + len(violating_dets) == N,
    f"Enumerated {N} gauge classes in {elapsed:.2f}s. Satisfying: {len(sat_classes)}, violating: {len(violating_dets)}.",
)

record(
    "number_of_plaquette_satisfying_classes_matches_prediction",
    len(sat_classes) == n_sat,
    f"Observed {len(sat_classes)} plaquette-satisfying classes, predicted {n_sat}.",
)


# ---------------------------------------------------------------------------
# KEY adversarial test: do all plaquette-satisfying classes give same |det|?
# ---------------------------------------------------------------------------

if sat_classes:
    sat_dets = sorted(set(d for (_, d) in sat_classes))
    all_equal = len(sat_dets) == 1
    record(
        "all_plaquette_satisfying_classes_same_det",
        all_equal,
        f"Plaquette-satisfying |det| values: {sat_dets}. All equal? {all_equal}.",
    )

    # Max det over all classes
    max_violating = max((d for (_, d) in violating_dets), default=0)
    max_overall = max(max_violating, max(d for (_, d) in sat_classes))

    sat_max = max(d for (_, d) in sat_classes)
    record(
        "plaquette_satisfying_achieves_max_over_all_classes",
        sat_max == max_overall,
        f"Max |det| among satisfying = {sat_max}. Max over all classes = {max_overall}. Max among violating = {max_violating}.",
    )

    # Whether K3 (mask=0) is satisfying
    k3_is_satisfying = any(mask == 0 for (mask, _) in sat_classes)
    record(
        "K3_is_one_of_the_plaquette_satisfying_classes",
        k3_is_satisfying,
        f"K3 (mask=0) is plaquette-satisfying: {k3_is_satisfying}. Its |det| = {det_K3}.",
    )


# ---------------------------------------------------------------------------
# Interpretation.
# ---------------------------------------------------------------------------

if sat_classes:
    sat_dets_set = set(d for (_, d) in sat_classes)
    if len(sat_dets_set) == 1 and (sat_max == max_overall):
        document(
            "conjecture_extends_to_non_contractible",
            f"The 'plaquette-satisfying => max |det|' conjecture"
            f" EXTENDS to non-contractible Z^3 subgraphs. On the ring"
            f" graph (chi = 0), {len(sat_classes)} plaquette-satisfying"
            f" classes exist and ALL give |det| = {next(iter(sat_dets_set))}"
            f" -- equal to the maximum over all gauge classes. Hence the"
            f" conjecture is not tied to contractibility; it's a broader"
            f" structural property of the K3 orientation on bipartite"
            f" Z^3 subgraphs.",
        )
    else:
        document(
            "conjecture_FAILS_on_non_contractible",
            f"Adversarial test FALSIFIED the conjecture. On the ring"
            f" graph, plaquette-satisfying classes give multiple"
            f" different |det| values ({sorted(sat_dets_set)}), and/or"
            f" a violating class exceeds the satisfying max. Hence the"
            f" 'K3 optimal' conjecture is a FEATURE OF CONTRACTIBILITY,"
            f" not a universal property of K3 on Z^3 subgraphs.",
        )


# ---------------------------------------------------------------------------
# Emit.
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: ring graph (non-contractible) K3-optimality adversarial test")
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
