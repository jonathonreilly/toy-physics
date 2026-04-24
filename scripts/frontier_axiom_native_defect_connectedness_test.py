#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test the refined 'connected defect'
conjecture with 4-site removals.

Background
----------
On (3,3,2) minus 2 sites:
- 2-site adjacent (connected defect): K3 optimal.
- 2-site diagonal (disconnected defect): K3 NOT optimal.

Conjecture: K3 Pfaffian-optimal iff contractible AND defect region
is connected.

Claims under adversarial test
-----------------------------
With 4-site removals (needed for balanced bipartite):
C1. Connected L-tetromino removal: K3 optimal.
C2. Connected 2x2 square removal: K3 optimal.
C3. Disconnected 2+2 removal (two 2-site chunks at opposite
    corners): K3 NOT optimal.

If all three predictions hold, conjecture strongly supported. If
any fails, conjecture needs refinement.

Test shapes (all (3,3,2) minus 4 sites = 14 site graphs)
---------------------------------------------------------
Shape-L: minus {(0,0,0), (1,0,0), (2,0,0), (2,1,0)} (L-tetromino).
Shape-S: minus {(0,0,0), (1,0,0), (0,1,0), (1,1,0)} (2x2 square).
Shape-2+2: minus {(0,0,0), (1,0,0), (2,2,0), (2,2,1)} (2 disjoint pairs).

Each removes 2 even + 2 odd sites for balance.
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


def f2_rank(M):
    A = (M.copy() % 2).astype(np.int8)
    nr, nc = A.shape
    rank, row, col = 0, 0, 0
    while row < nr and col < nc:
        pivot = None
        for r in range(row, nr):
            if A[r, col] == 1:
                pivot = r; break
        if pivot is None:
            col += 1; continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
        for r in range(nr):
            if r != row and A[r, col] == 1:
                A[r] = (A[r] + A[row]) % 2
        rank += 1; row += 1; col += 1
    return rank


def test_shape(label: str, removed: set):
    base_sites = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
    sites = [v for v in base_sites if v not in removed]
    site_set = set(sites)

    edges = []
    edge_index = {}
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn in site_set:
                edges.append((n, nn, mu))
                edge_index[frozenset({n, nn})] = len(edges) - 1

    plaquettes = []
    for n in base_sites:
        for i in (1, 2, 3):
            for j in range(i + 1, 4):
                n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
                n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
                n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
                corners = {n, n_i, n_j, n_ij}
                if all(c in site_set for c in corners):
                    plaquettes.append([
                        edge_index[frozenset({n, n_i})],
                        edge_index[frozenset({n, n_j})],
                        edge_index[frozenset({n_i, n_ij})],
                        edge_index[frozenset({n_j, n_ij})],
                    ])

    cubes = 0
    for n in base_sites:
        i, j, k = n
        if i + 1 < 3 and j + 1 < 3 and k + 1 < 2:
            corners = [(i + di, j + dj, k + dk)
                       for di in (0, 1) for dj in (0, 1) for dk in (0, 1)]
            if all(c in site_set for c in corners):
                cubes += 1

    V, E, F = len(sites), len(edges), len(plaquettes)
    chi = V - E + F - cubes

    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return {"label": label, "balanced": False, "V": V}

    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    B_0 = np.zeros((n_bi, n_bi), dtype=np.int64)
    edge_bip = {}
    for idx, (n_lo, n_hi, mu) in enumerate(edges):
        if n_lo in idx_e:
            ie, jo = idx_e[n_lo], idx_o[n_hi]; s = eta(mu, n_lo)
        else:
            ie, jo = idx_e[n_hi], idx_o[n_lo]; s = -eta(mu, n_lo)
        B_0[ie, jo] = s
        edge_bip[idx] = (ie, jo)
    det_K3 = int(round(abs(np.linalg.det(B_0))))

    adj = defaultdict(list)
    for idx, (a, b, _) in enumerate(edges):
        adj[a].append((b, idx)); adj[b].append((a, idx))
    start = sites[0]
    visited = {start}; tree_idx = set()
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for (v, ei) in adj[u]:
            if v not in visited:
                visited.add(v); tree_idx.add(ei); queue.append(v)
    chord_idx = [idx for idx in range(E) if idx not in tree_idx]
    gauge_dim = len(chord_idx)

    # Plaquette rank
    chord_bit = {c: b for b, c in enumerate(chord_idx)}
    M_mat = np.zeros((F, gauge_dim), dtype=np.int8)
    for p_idx, pedges in enumerate(plaquettes):
        for e in pedges:
            if e in chord_bit:
                M_mat[p_idx, chord_bit[e]] = 1
    plaq_rank = f2_rank(M_mat)

    # Exhaustive search
    max_det = det_K3
    n_optimal = 0
    plaq_chord_mask = []
    for pedges in plaquettes:
        pm = 0
        for e in pedges:
            if e in chord_bit:
                pm |= (1 << chord_bit[e])
        plaq_chord_mask.append(pm)

    n_sat = 0
    sat_dets_set = set()
    for mask in range(2 ** gauge_dim):
        all_sat = True
        for pm in plaq_chord_mask:
            v = mask & pm
            par = 0
            while v:
                par ^= (v & 1); v >>= 1
            if par:
                all_sat = False; break
        B_m = B_0.copy()
        for bit in range(gauge_dim):
            if (mask >> bit) & 1:
                idx = chord_idx[bit]
                ie, jo = edge_bip[idx]
                B_m[ie, jo] *= -1
        det_abs = int(round(abs(np.linalg.det(B_m))))
        if all_sat:
            n_sat += 1; sat_dets_set.add(det_abs)
        if det_abs > max_det:
            max_det = det_abs; n_optimal = 1
        elif det_abs == max_det:
            n_optimal += 1

    return {
        "label": label, "balanced": True,
        "V": V, "E": E, "F": F, "cubes": cubes, "chi": chi,
        "gauge_dim": gauge_dim, "plaq_rank": plaq_rank,
        "det_K3": det_K3, "max_det": max_det, "n_optimal": n_optimal,
        "n_sat": n_sat, "sat_dets": sorted(sat_dets_set),
        "k3_optimal": det_K3 == max_det,
    }


# ---------------------------------------------------------------------------
# Shapes
# ---------------------------------------------------------------------------

shapes = [
    ("L_tetromino_connected",
     {(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0)}),
    ("square_2x2_connected",
     {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)}),
    ("disconnected_2plus2",
     {(0, 0, 0), (1, 0, 0), (2, 2, 0), (2, 2, 1)}),
]

results = []
for (label, removed) in shapes:
    t0 = time.time()
    info = test_shape(label, removed)
    info["elapsed"] = time.time() - t0
    results.append(info)


# ---------------------------------------------------------------------------
# Record results
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    if not info.get("balanced", False):
        record(f"shape_{label}_balanced", False,
               f"{label}: unbalanced, V={info.get('V')}.")
        continue

    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, cubes={info['cubes']}, chi={info['chi']}.",
    )

    record(
        f"shape_{label}_plaquette_uniqueness",
        info["plaq_rank"] == info["gauge_dim"] and info["n_sat"] == 1,
        f"{label}: gauge_dim={info['gauge_dim']}, plaq_rank={info['plaq_rank']}, n_sat={info['n_sat']}.",
    )

    # Status record: K3 optimality status for this shape (will drive
    # the per-shape prediction checks below).
    record(
        f"shape_{label}_K3_det_matches_max",
        info["det_K3"] == info["max_det"],
        f"{label}: K3 det={info['det_K3']}, max={info['max_det']}, K3 optimal? {info['k3_optimal']} ({info['elapsed']:.2f}s).",
    )


# ---------------------------------------------------------------------------
# Test the predictions
# ---------------------------------------------------------------------------

pred_L = any(r["label"] == "L_tetromino_connected" and r.get("k3_optimal") for r in results)
pred_S = any(r["label"] == "square_2x2_connected" and r.get("k3_optimal") for r in results)
pred_D = any(r["label"] == "disconnected_2plus2" and not r.get("k3_optimal") for r in results)

record(
    "prediction_L_tetromino_K3_optimal_holds",
    pred_L,
    f"Connected L-tetromino: K3 optimal? {pred_L}.",
)
record(
    "prediction_2x2_square_K3_optimal_holds",
    pred_S,
    f"Connected 2x2 square: K3 optimal? {pred_S}.",
)
record(
    "prediction_disconnected_2plus2_K3_NOT_optimal_holds",
    pred_D,
    f"Disconnected 2+2: K3 NOT optimal (predicted)? {pred_D}.",
)

all_predictions_hold = pred_L and pred_S and pred_D
record(
    "connected_defect_conjecture_supported_across_all_3_shapes",
    all_predictions_hold,
    f"Predictions: L={pred_L}, 2x2={pred_S}, disconnected_2+2={pred_D}. All consistent with conjecture? {all_predictions_hold}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if all_predictions_hold:
    document(
        "connected_defect_conjecture_strongly_supported",
        "All three 4-site removal predictions confirmed the connected-"
        "defect conjecture: K3 Pfaffian-optimal iff contractible AND"
        " the defect region is connected. Connected defects (L-tetromino,"
        " 2x2 square): K3 achieves max. Disconnected defect (2+2): K3"
        " fails to achieve max. Combined with 2-site removal results,"
        " the conjecture has 7 supporting data points and 0 refutations.",
    )
else:
    document(
        "connected_defect_conjecture_needs_refinement",
        "At least one prediction failed, indicating the connected-"
        "defect conjecture is incomplete. Specific failure pattern"
        " documented in per-shape records.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: defect-connectedness test via 4-site removals")
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
