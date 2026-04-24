#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- adversarial test of the refined
'balanced defect components' conjecture.

Conjecture under test
---------------------
K3 Pfaffian-optimal iff:
  (a) graph is contractible (chi = 1), AND
  (b) each connected component of the defect region has equal
      even and odd parity sites.

This runner tests the CRITICAL case where (a) holds but (b) fails:
connected defect components with unbalanced parity. The conjecture
predicts K3 fails here. If K3 is still optimal, conjecture is
falsified.

Shapes
------
Shape X (ADVERSARIAL): two 3-site line defects.
  Line A: {(0,0,0), (1,0,0), (2,0,0)} at y=0, z=0. 2e + 1o unbalanced.
  Line B: {(0,2,1), (1,2,1), (2,2,1)} at y=2, z=1. 1e + 2o unbalanced.
  Total: 3e + 3o (overall balanced). 2 disconnected components, each
  component is unbalanced.
  CONJECTURE PREDICTS: K3 FAILS.

Shape Y (CONTROL): one 2x3 connected strip defect.
  Strip: {(i, j, 0) for i in 0..1, j in 0..2}. 3e + 3o (balanced).
  1 connected component, balanced.
  CONJECTURE PREDICTS: K3 OPTIMAL.

Both shapes leave 12 sites and should be contractible. If BOTH
predictions match, the conjecture survives the sharpest test so
far. If either fails, conjecture is falsified concretely.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict, deque

import numpy as np


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name, ok, detail):
    RECORDS.append((name, bool(ok), detail))


def document(name, note):
    DOCS.append((name, note))


def eta(mu, n):
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


def defect_components(removed_set):
    comps = []
    visited = set()
    for start in sorted(removed_set):
        if start in visited:
            continue
        comp = []
        stack = [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            comp.append(u)
            for mu in (1, 2, 3):
                for d in (-1, 1):
                    v = list(u)
                    v[mu - 1] += d
                    v = tuple(v)
                    if v in removed_set and v not in visited:
                        stack.append(v)
        comps.append(comp)
    return comps


def test_shape(label, removed, bound=(3, 3, 2)):
    L1, L2, L3 = bound
    base_sites = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
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
                if all(c in site_set for c in (n, n_i, n_j, n_ij)):
                    plaquettes.append([
                        edge_index[frozenset({n, n_i})],
                        edge_index[frozenset({n, n_j})],
                        edge_index[frozenset({n_i, n_ij})],
                        edge_index[frozenset({n_j, n_ij})],
                    ])

    cubes = 0
    for n in base_sites:
        i, j, k = n
        if i + 1 < L1 and j + 1 < L2 and k + 1 < L3:
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
    if gauge_dim > 18:
        return {"label": label, "balanced": True, "too_large": True, "gauge_dim": gauge_dim,
                "V": V, "E": E, "F": F, "cubes": cubes, "chi": chi,
                "det_K3": det_K3}

    max_det = det_K3
    n_optimal = 1  # K3 itself
    for mask in range(1, 2 ** gauge_dim):
        B_m = B_0.copy()
        for bit in range(gauge_dim):
            if (mask >> bit) & 1:
                idx = chord_idx[bit]
                ie, jo = edge_bip[idx]
                B_m[ie, jo] *= -1
        det_abs = int(round(abs(np.linalg.det(B_m))))
        if det_abs > max_det:
            max_det = det_abs; n_optimal = 1
        elif det_abs == max_det:
            n_optimal += 1

    # Defect component analysis
    comps = defect_components(set(removed))
    comp_parities = []
    all_comps_balanced = True
    for comp in comps:
        e = sum(1 for v in comp if sum(v) % 2 == 0)
        o = len(comp) - e
        comp_parities.append((len(comp), e, o))
        if e != o:
            all_comps_balanced = False

    return {
        "label": label, "balanced": True,
        "V": V, "E": E, "F": F, "cubes": cubes, "chi": chi,
        "gauge_dim": gauge_dim, "plaq_rank": plaq_rank,
        "det_K3": det_K3, "max_det": max_det, "n_optimal": n_optimal,
        "k3_optimal": det_K3 == max_det,
        "n_defect_components": len(comps),
        "comp_parities": comp_parities,
        "all_comps_balanced": all_comps_balanced,
    }


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

shape_X = ("two_unbalanced_lines",
           {(0, 0, 0), (1, 0, 0), (2, 0, 0),
            (0, 2, 1), (1, 2, 1), (2, 2, 1)})

shape_Y = ("connected_2x3_strip",
           {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 2, 0), (1, 2, 0)})

results = []
for (label, removed) in [shape_X, shape_Y]:
    t0 = time.time()
    info = test_shape(label, removed)
    info["elapsed"] = time.time() - t0
    results.append(info)


# ---------------------------------------------------------------------------
# Record and check predictions
# ---------------------------------------------------------------------------

info_X = results[0]
info_Y = results[1]

for info in results:
    label = info["label"]
    if not info.get("balanced", False):
        record(f"shape_{label}_balanced", False, f"{label}: unbalanced.")
        continue
    if info.get("too_large", False):
        record(f"shape_{label}_too_large", False, f"{label}: gauge_dim too large for exhaustive.")
        continue

    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, cubes={info['cubes']}, chi={info['chi']}."
    )

    record(
        f"shape_{label}_defect_components",
        True == (info["n_defect_components"] >= 1),
        f"{label}: {info['n_defect_components']} defect components, parities (size,e,o) = {info['comp_parities']}, all balanced: {info['all_comps_balanced']}."
    )

    record(
        f"shape_{label}_K3_optimality",
        info["k3_optimal"] == (True if info["all_comps_balanced"] else False),
        f"{label}: K3 det={info['det_K3']}, max={info['max_det']}, K3 optimal? {info['k3_optimal']}. Expected by conjecture: {info['all_comps_balanced']}.",
    )


# ---------------------------------------------------------------------------
# Adversarial prediction checks
# ---------------------------------------------------------------------------

X_predicted_fail = not info_X.get("k3_optimal", True)  # predict K3 NOT optimal
Y_predicted_optimal = info_Y.get("k3_optimal", False)  # predict K3 optimal

record(
    "shape_X_unbalanced_components_K3_fails_as_predicted",
    X_predicted_fail,
    f"Shape X (two unbalanced 3-line components): K3 det={info_X.get('det_K3')}, max={info_X.get('max_det')}. Fails? {X_predicted_fail}. Predicted fail.",
)

record(
    "shape_Y_balanced_component_K3_optimal_as_predicted",
    Y_predicted_optimal,
    f"Shape Y (one balanced 2x3 strip): K3 det={info_Y.get('det_K3')}, max={info_Y.get('max_det')}. Optimal? {Y_predicted_optimal}. Predicted optimal.",
)


# ---------------------------------------------------------------------------
# Conjecture status
# ---------------------------------------------------------------------------

conjecture_holds = X_predicted_fail and Y_predicted_optimal
record(
    "balanced_components_conjecture_survives_adversarial_test",
    conjecture_holds,
    f"Shape X predicted fail: {X_predicted_fail}. Shape Y predicted optimal: {Y_predicted_optimal}. Both match? {conjecture_holds}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if conjecture_holds:
    document(
        "balanced_components_conjecture_survives_sharpest_test",
        "The refined 'balanced defect components' conjecture survived"
        " the sharpest adversarial test so far: K3 fails on a shape"
        " with contractibility and overall balance but UNBALANCED"
        " defect components, while K3 succeeds on a contractible shape"
        " with a single balanced defect component. The conjecture now"
        " has 10+ consistent data points and is the strongest"
        " characterization of K3 optimality found.",
    )
else:
    document(
        "balanced_components_conjecture_FAILS",
        "Adversarial test refuted the balanced-components conjecture."
        " Specific data in per-shape records. Conjecture needs further"
        " refinement.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: unbalanced-component adversarial test of balance-conjecture")
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
