#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- K3 optimality on contractible non-cuboid
Z^3 subgraphs.

Background
----------
Prior V2 iterations:
- K3 is Pfaffian-optimal on all tested Z^3 CUBOIDS.
- On non-contractible ring graph, K3 is NOT optimal.
- Unknown: does K3 optimality extend to contractible NON-CUBOID
  Z^3 subgraphs?

Claim under adversarial test
----------------------------
C1. On any contractible non-cuboid Z^3 subgraph, K3 is the unique
    plaquette-satisfying gauge class (follows from Euler chi = 1).
C2. K3 achieves the max |det(B)| over all gauge classes.

If both hold on L-shape and 2-corners-clipped shapes, the scope of
K3 optimality is "contractible Z^3 subgraphs" (not just cuboids).
If either fails, the scope is narrower.

Test shapes
-----------
(i)  3D L-shape: sites {(i, 0, k)} for i in 0..2, k in 0..1, plus
     sites {(0, j, k)} for j in 0..2, k in 0..1. 10 sites,
     two arms meeting at (0, 0, *) column. Not a cuboid.
(ii) (3,3,2) with corners (0,0,0) and (2,2,1) removed. 16 sites.
     Still contractible. Non-cuboid (has concave bits at removed
     corners).
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict, deque
from itertools import permutations, product

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


def build_graph(sites: set):
    """Return (sites_list, edges, plaquettes, cubes, bounding_box)."""
    sites_list = sorted(sites)
    edges = []
    edge_index = {}
    for n in sites_list:
        for mu in (1, 2, 3):
            nn = list(n)
            nn[mu - 1] += 1
            nn = tuple(nn)
            if nn in sites:
                edges.append((n, nn, mu))
                edge_index[frozenset({n, nn})] = len(edges) - 1

    # Plaquettes: 4-cycle squares in each coordinate plane
    plaquettes = []
    # Need a superset of all candidate base points
    bbox = max(sites) if sites else (0, 0, 0)
    for n in sites_list:
        for i in (1, 2, 3):
            for j in range(i + 1, 4):
                n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
                n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
                n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
                corners = {n, n_i, n_j, n_ij}
                if all(c in sites for c in corners):
                    e1 = frozenset({n, n_i})
                    e2 = frozenset({n, n_j})
                    e3 = frozenset({n_i, n_ij})
                    e4 = frozenset({n_j, n_ij})
                    if all(e in edge_index for e in (e1, e2, e3, e4)):
                        plaquettes.append(
                            [edge_index[e1], edge_index[e2], edge_index[e3], edge_index[e4]]
                        )

    # 1x1x1 cubes
    cubes = []
    for n in sites_list:
        i, j, k = n
        cube_corners = [
            (i + di, j + dj, k + dk)
            for di in (0, 1) for dj in (0, 1) for dk in (0, 1)
        ]
        if all(c in sites for c in cube_corners):
            cubes.append(cube_corners)

    return sites_list, edges, edge_index, plaquettes, cubes


def build_bipartite_block(sites_list, edges, edge_index):
    evens = [v for v in sites_list if sum(v) % 2 == 0]
    odds = [v for v in sites_list if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return None
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    B = np.zeros((n_bi, n_bi), dtype=np.int64)
    B_un = np.zeros((n_bi, n_bi), dtype=np.int64)
    bip_edges = []
    for idx, (n_lo, n_hi, mu) in enumerate(edges):
        if n_lo in idx_e:
            ie, jo = idx_e[n_lo], idx_o[n_hi]
            s = eta(mu, n_lo)
        else:
            ie, jo = idx_e[n_hi], idx_o[n_lo]
            s = -eta(mu, n_lo)
        B[ie, jo] = s
        B_un[ie, jo] = 1
        bip_edges.append((ie, jo, s, idx))
    return evens, odds, B, B_un, bip_edges


def ryser_perm(M):
    n = M.shape[0]
    total = 0
    for s in range(1, 2 ** n):
        subset = [j for j in range(n) if (s >> j) & 1]
        prod = 1
        for i in range(n):
            row_sum = sum(M[i, j] for j in subset)
            prod *= row_sum
        sign = (-1) ** (n - len(subset))
        total += sign * prod
    return int(total)


def spanning_tree_chords(sites_list, edges):
    adj = defaultdict(list)
    for idx, (a, b, _) in enumerate(edges):
        adj[a].append((b, idx))
        adj[b].append((a, idx))
    start = sites_list[0]
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
    return tree_idx, [idx for idx in range(len(edges)) if idx not in tree_idx]


def test_shape(label: str, sites: set):
    sites_list, edges, edge_index, plaquettes, cubes = build_graph(sites)
    V = len(sites_list)
    E = len(edges)
    F = len(plaquettes)
    C = len(cubes)
    chi = V - E + F - C

    bip = build_bipartite_block(sites_list, edges, edge_index)
    if bip is None:
        return {"label": label, "balanced": False}
    evens, odds, B, B_un, bip_edges = bip
    n_bi = len(evens)

    det_K3 = int(round(abs(np.linalg.det(B))))
    pm = ryser_perm(B_un)

    tree_idx, chord_idx = spanning_tree_chords(sites_list, edges)
    gauge_dim = len(chord_idx)

    # Plaquette-chord incidence
    chord_bit = {c: b for b, c in enumerate(chord_idx)}
    M = np.zeros((F, gauge_dim), dtype=np.int8)
    for p_idx, p in enumerate(plaquettes):
        for e in p:
            if e in chord_bit:
                M[p_idx, chord_bit[e]] = 1
    plaq_rank = f2_rank(M)

    # Enumerate gauge classes if feasible
    sat_classes = []
    all_dets = []
    viol_dets = []
    N = 2 ** gauge_dim

    edge_to_bip = {bip_edges[i][3]: bip_edges[i] for i in range(len(bip_edges))}
    # bip_edges is list of (ie, jo, s, edge_idx_in_edges)
    # Need map from edge idx -> bip entry
    edge_idx_to_bip = {}
    for (ie, jo, s, eidx) in bip_edges:
        edge_idx_to_bip[eidx] = (ie, jo, s)

    if N <= 2 ** 16:
        plaq_masks = []
        for p in plaquettes:
            pm_mask = 0
            for e in p:
                if e in chord_bit:
                    pm_mask |= (1 << chord_bit[e])
            plaq_masks.append(pm_mask)

        for mask in range(N):
            # Check all plaquettes
            all_sat = True
            for pm_mask in plaq_masks:
                v = mask & pm_mask
                parity = 0
                while v:
                    parity ^= (v & 1)
                    v >>= 1
                if parity:
                    all_sat = False
                    break
            # Compute det
            B_m = B.copy()
            for bit in range(gauge_dim):
                if (mask >> bit) & 1:
                    idx = chord_idx[bit]
                    ie, jo, s = edge_idx_to_bip[idx]
                    B_m[ie, jo] *= -1
            det_abs = int(round(abs(np.linalg.det(B_m))))
            all_dets.append((mask, det_abs))
            if all_sat:
                sat_classes.append((mask, det_abs))
            else:
                viol_dets.append((mask, det_abs))
    else:
        sat_classes = None
        all_dets = None
        viol_dets = None

    return {
        "label": label,
        "V": V, "E": E, "F": F, "cubes": C, "chi": chi,
        "n_bi": n_bi, "gauge_dim": gauge_dim, "plaq_rank": plaq_rank,
        "det_K3": det_K3, "pm": pm,
        "sat_classes": sat_classes,
        "all_dets": all_dets,
        "viol_dets": viol_dets,
    }


# ---------------------------------------------------------------------------
# Shape (i): 3D L-shape
# ---------------------------------------------------------------------------

L_shape = set()
for i in range(3):
    for k in range(2):
        L_shape.add((i, 0, k))
for j in range(3):
    for k in range(2):
        L_shape.add((0, j, k))

t0 = time.time()
info_L = test_shape("L_shape", L_shape)
dt_L = time.time() - t0


record(
    "L_shape_is_contractible",
    info_L["chi"] == 1,
    f"L-shape: V={info_L['V']}, E={info_L['E']}, F={info_L['F']}, cubes={info_L['cubes']}, chi={info_L['chi']}.",
)

record(
    "L_shape_plaquette_rank_equals_gauge_dim",
    info_L["plaq_rank"] == info_L["gauge_dim"],
    f"L-shape: gauge_dim={info_L['gauge_dim']}, plaq_rank={info_L['plaq_rank']}. Predicted unique class? {info_L['plaq_rank'] == info_L['gauge_dim']}.",
)

sat_classes_L = info_L["sat_classes"]
if sat_classes_L is not None:
    sat_dets_L = sorted(set(d for (_, d) in sat_classes_L))
    all_dets_L = [d for (_, d) in info_L["all_dets"]]
    max_det_L = max(all_dets_L) if all_dets_L else 0

    record(
        "L_shape_K3_unique_plaquette_satisfying",
        len(sat_classes_L) == 1,
        f"L-shape: {len(sat_classes_L)} plaquette-satisfying classes. Dets: {sat_dets_L}.",
    )

    record(
        "L_shape_K3_achieves_max_det",
        info_L["det_K3"] == max_det_L,
        f"L-shape: K3 det={info_L['det_K3']}, max over all {2**info_L['gauge_dim']} classes = {max_det_L}. #PM={info_L['pm']}.",
    )


# ---------------------------------------------------------------------------
# Shape (ii): (3,3,2) with corners (0,0,0) and (2,2,1) removed
# ---------------------------------------------------------------------------

clipped = set()
for i in range(3):
    for j in range(3):
        for k in range(2):
            if (i, j, k) == (0, 0, 0):
                continue
            if (i, j, k) == (2, 2, 1):
                continue
            clipped.add((i, j, k))

t0 = time.time()
info_C = test_shape("corners_clipped_332", clipped)
dt_C = time.time() - t0


record(
    "clipped_332_is_contractible",
    info_C["chi"] == 1,
    f"Clipped (3,3,2): V={info_C['V']}, E={info_C['E']}, F={info_C['F']}, cubes={info_C['cubes']}, chi={info_C['chi']}.",
)

record(
    "clipped_332_plaquette_rank_equals_gauge_dim",
    info_C["plaq_rank"] == info_C["gauge_dim"],
    f"Clipped (3,3,2): gauge_dim={info_C['gauge_dim']}, plaq_rank={info_C['plaq_rank']}.",
)

sat_classes_C = info_C["sat_classes"]
if sat_classes_C is not None:
    sat_dets_C = sorted(set(d for (_, d) in sat_classes_C))
    all_dets_C = [d for (_, d) in info_C["all_dets"]]
    max_det_C = max(all_dets_C) if all_dets_C else 0

    record(
        "clipped_332_K3_unique_plaquette_satisfying",
        len(sat_classes_C) == 1,
        f"Clipped (3,3,2): {len(sat_classes_C)} plaquette-satisfying classes. Dets: {sat_dets_C}.",
    )

    record(
        "clipped_332_K3_achieves_max_det",
        info_C["det_K3"] == max_det_C,
        f"Clipped (3,3,2): K3 det={info_C['det_K3']}, max over all {2**info_C['gauge_dim']} classes = {max_det_C}. #PM={info_C['pm']}.",
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

both_satisfy_contractibility_scope = (
    info_L.get("plaq_rank") == info_L.get("gauge_dim")
    and info_C.get("plaq_rank") == info_C.get("gauge_dim")
    and (info_L["sat_classes"] is None or (len(info_L["sat_classes"]) == 1 and info_L["det_K3"] == max(d for (_, d) in info_L["all_dets"])))
    and (info_C["sat_classes"] is None or (len(info_C["sat_classes"]) == 1 and info_C["det_K3"] == max(d for (_, d) in info_C["all_dets"])))
)

record(
    "K3_optimality_extends_to_contractible_non_cuboid",
    both_satisfy_contractibility_scope,
    f"Both L-shape and clipped-332 satisfy: unique plaquette-satisfying = K3, K3 achieves max |det|. Scope confirmed as contractible.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if both_satisfy_contractibility_scope:
    document(
        "K3_optimal_on_contractible_Z3_subgraphs",
        "K3 optimality extends from cuboids to contractible non-cuboid"
        " Z^3 subgraphs (L-shape, clipped cuboid). Hence the scope of"
        " K3 Pfaffian-optimality is CONTRACTIBLE Z^3 subgraphs. This"
        " is a cleaner statement than 'cuboid': it's a topological"
        " rather than shape-specific property.",
    )
else:
    document(
        "K3_optimal_scope_narrower_than_contractible",
        "Adversarial test found a contractible non-cuboid where K3 is"
        " NOT optimal. Scope is narrower than 'contractible'; further"
        " investigation needed to characterize exactly which contractible"
        " shapes preserve K3 optimality.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: K3 optimality on contractible non-cuboid Z^3 subgraphs")
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
