#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- map scope boundary of K3 optimality
across multiple contractible non-cuboid Z^3 shapes.

Background
----------
K3 optimality:
- Holds on planar (L-shape, (3,2,2), plaquette, cube).
- Holds on cuboids incl. non-planar (3,3,2), (4,3,2), (4,4,2).
- FAILS on clipped-(3,3,2) with opposite-diagonal corners removed
  (contractible non-planar non-cuboid).

Claims under adversarial test
-----------------------------
C1. K3 optimality also fails on (3,3,2) with ADJACENT corner
    pairs removed. If K3 is optimal on some, scope is subtler.
C2. K3 optimality fails on contractible non-cuboid non-planar
    graphs generically; the failure is driven by the non-cuboidal
    shape, not by specific placement of removed sites.

Shapes tested
-------------
Each is (3,3,2) with two specific sites removed, giving
contractible non-cuboid non-planar graphs:
- Shape A: minus {(0,0,0), (1,0,0)} (x-adjacent at z=0 corner)
- Shape B: minus {(0,0,0), (0,1,0)} (y-adjacent at z=0 corner)
- Shape C: minus {(0,0,0), (0,0,1)} (z-adjacent = vertical pair)
- Shape D: minus {(0,0,0), (2,2,1)} (opposite-diagonal = clipped)

For each: verify contractibility, balanced bipartite, compute K3
|det|, exhaustive max |det|, report whether K3 = max.
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
    A = (M.copy() % 2).astype(np.int8)
    nr, nc = A.shape
    rank, row, col = 0, 0, 0
    while row < nr and col < nc:
        pivot = None
        for r in range(row, nr):
            if A[r, col] == 1:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
        for r in range(nr):
            if r != row and A[r, col] == 1:
                A[r] = (A[r] + A[row]) % 2
        rank += 1
        row += 1
        col += 1
    return rank


def test_shape(label: str, removed: set):
    base_sites = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
    sites = [v for v in base_sites if v not in removed]
    site_set = set(sites)

    # Edges
    edges = []
    edge_index = {}
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n)
            nn[mu - 1] += 1
            nn = tuple(nn)
            if nn in site_set:
                edges.append((n, nn, mu))
                edge_index[frozenset({n, nn})] = len(edges) - 1

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
                    e_list = [
                        edge_index[frozenset({n, n_i})],
                        edge_index[frozenset({n, n_j})],
                        edge_index[frozenset({n_i, n_ij})],
                        edge_index[frozenset({n_j, n_ij})],
                    ]
                    plaquettes.append(e_list)

    # Cubes
    cube_count = 0
    for n in base_sites:
        i, j, k = n
        if i + 1 < 3 and j + 1 < 3 and k + 1 < 2:
            corners = [(i + di, j + dj, k + dk)
                       for di in (0, 1) for dj in (0, 1) for dk in (0, 1)]
            if all(c in site_set for c in corners):
                cube_count += 1

    V, E, F = len(sites), len(edges), len(plaquettes)
    chi = V - E + F - cube_count

    # Bipartite block
    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    balanced = len(evens) == len(odds)

    if not balanced:
        return {
            "label": label, "V": V, "E": E, "F": F, "cubes": cube_count, "chi": chi,
            "balanced": False, "skipped": True,
        }

    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    B_0 = np.zeros((n_bi, n_bi), dtype=np.int64)
    edge_to_bip = {}
    for idx, (n_lo, n_hi, mu) in enumerate(edges):
        if n_lo in idx_e:
            ie, jo = idx_e[n_lo], idx_o[n_hi]
            s = eta(mu, n_lo)
        else:
            ie, jo = idx_e[n_hi], idx_o[n_lo]
            s = -eta(mu, n_lo)
        B_0[ie, jo] = s
        edge_to_bip[idx] = (ie, jo)
    det_K3 = int(round(abs(np.linalg.det(B_0))))

    # Spanning tree, chords
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
    chord_idx = [idx for idx in range(E) if idx not in tree_idx]
    gauge_dim = len(chord_idx)

    # Plaquette-chord matrix
    chord_bit = {c: b for b, c in enumerate(chord_idx)}
    M = np.zeros((F, gauge_dim), dtype=np.int8)
    for p_idx, p_edges in enumerate(plaquettes):
        for e in p_edges:
            if e in chord_bit:
                M[p_idx, chord_bit[e]] = 1
    plaq_rank = f2_rank(M)

    # Enumerate if feasible
    max_det = det_K3
    n_optimal = 0
    sat_dets_set = set()
    n_sat = 0
    if gauge_dim <= 16:
        plaq_chord_masks = []
        for p_edges in plaquettes:
            pm = 0
            for e in p_edges:
                if e in chord_bit:
                    pm |= (1 << chord_bit[e])
            plaq_chord_masks.append(pm)

        for mask in range(2 ** gauge_dim):
            all_sat = True
            for pm in plaq_chord_masks:
                v = mask & pm
                par = 0
                while v:
                    par ^= (v & 1)
                    v >>= 1
                if par:
                    all_sat = False
                    break
            B_m = B_0.copy()
            for bit in range(gauge_dim):
                if (mask >> bit) & 1:
                    idx = chord_idx[bit]
                    ie, jo = edge_to_bip[idx]
                    B_m[ie, jo] *= -1
            det_abs = int(round(abs(np.linalg.det(B_m))))
            if all_sat:
                n_sat += 1
                sat_dets_set.add(det_abs)
            if det_abs > max_det:
                max_det = det_abs
                n_optimal = 1
            elif det_abs == max_det:
                n_optimal += 1

    k3_is_optimal = det_K3 == max_det

    return {
        "label": label,
        "V": V, "E": E, "F": F, "cubes": cube_count, "chi": chi,
        "balanced": balanced,
        "gauge_dim": gauge_dim, "plaq_rank": plaq_rank,
        "det_K3": det_K3, "max_det": max_det, "n_optimal": n_optimal,
        "n_sat": n_sat, "sat_dets": sorted(sat_dets_set),
        "k3_optimal": k3_is_optimal,
    }


# ---------------------------------------------------------------------------
# Test the shapes
# ---------------------------------------------------------------------------

shapes = [
    ("A_x_adjacent", {(0, 0, 0), (1, 0, 0)}),
    ("B_y_adjacent", {(0, 0, 0), (0, 1, 0)}),
    ("C_z_adjacent", {(0, 0, 0), (0, 0, 1)}),
    ("D_diagonal", {(0, 0, 0), (2, 2, 1)}),
]

results = []
for (label, removed) in shapes:
    t0 = time.time()
    info = test_shape(label, removed)
    info["elapsed"] = time.time() - t0
    results.append(info)


# ---------------------------------------------------------------------------
# Record results per shape
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    if not info.get("balanced", False):
        record(
            f"shape_{label}_balanced",
            False,
            f"{label}: unbalanced (|even|!=|odd|), skipped."
        )
        continue

    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, cubes={info['cubes']}, chi={info['chi']}."
    )

    record(
        f"shape_{label}_plaquette_uniqueness",
        info["plaq_rank"] == info["gauge_dim"] and info["n_sat"] == 1,
        f"{label}: gauge_dim={info['gauge_dim']}, plaq_rank={info['plaq_rank']}, n_sat={info['n_sat']}, sat_dets={info['sat_dets']}."
    )

    record(
        f"shape_{label}_K3_optimal",
        info["k3_optimal"],
        f"{label}: K3 det={info['det_K3']}, max={info['max_det']}, n_optimal={info['n_optimal']}, K3 optimal? {info['k3_optimal']}."
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

k3_fails_on_all_non_cuboid = all(
    not info.get("k3_optimal", True)
    for info in results
    if info.get("balanced", False)
)

record(
    "K3_fails_on_all_tested_non_cuboid_contractibles",
    k3_fails_on_all_non_cuboid,
    f"K3 optimality on tested non-cuboid contractible shapes: {[(info['label'], info.get('k3_optimal')) for info in results if info.get('balanced', False)]}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if k3_fails_on_all_non_cuboid:
    document(
        "K3_scope_boundary_tightened",
        "On all tested contractible non-cuboid non-planar Z^3 shapes"
        " (3 adjacent-pair removals + 1 diagonal), K3 is NOT"
        " Pfaffian-optimal. Combined with K3 optimality on all tested"
        " cuboids and planar shapes: the scope boundary is likely"
        " 'planar or cuboid' -- not 'contractible'. Cuboid regularity"
        " is necessary beyond planarity for K3 to achieve the max.",
    )
else:
    document(
        "K3_optimal_on_some_non_cuboid",
        "On at least one contractible non-cuboid non-planar shape,"
        " K3 remains optimal. The scope boundary is more subtle than"
        " 'planar or cuboid'. Investigate the specific shape where"
        " K3 works to find a structural explanation.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: scope map of K3 optimality on contractible non-cuboids")
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
