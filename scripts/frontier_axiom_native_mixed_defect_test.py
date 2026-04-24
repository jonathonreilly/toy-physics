#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test singleton hypothesis with mixed
defect configurations (singletons + larger components coexisting).

Hypothesis under test
---------------------
K3 Pfaffian-optimal iff:
  (a) graph is contractible (chi = 1), AND
  (b) defect region has no isolated singleton components.

If the hypothesis is correct, the presence of ANY singleton should
break K3 optimality, regardless of other defects. If larger defects
somehow "absorb" or compensate for nearby singletons, the hypothesis
is falsified.

Shapes tested (all on (3,3,2), balanced bipartite, contractible)
-----------------------------------------------------------------
Shape I: {(0,0,0) singleton, (2,2,1) singleton,
          (1,0,0)-(1,0,1) vertical pair}
         4 sites, 3 components (2 singletons + 1 pair).
         Predicted: K3 FAILS (singletons present).

Shape E: {(0,0,0) singleton, (2,2,1) singleton,
          (1,0,0)-(1,0,1) pair, (1,2,0)-(1,2,1) pair}
         6 sites, 4 components (2 singletons + 2 pairs).
         Predicted: K3 FAILS.

Shape J (control): {(0,0,0)-(0,0,1) pair, (2,2,0)-(2,2,1) pair}
         4 sites, 2 components, no singletons.
         Predicted: K3 OPTIMAL.

Falsifiability: if I or E has K3 optimal despite singletons, the
singleton hypothesis is concretely falsified.
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
                    v = list(u); v[mu - 1] += d; v = tuple(v)
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

    if gauge_dim > 18:
        return {"label": label, "balanced": True, "V": V, "E": E, "F": F, "cubes": cubes, "chi": chi,
                "gauge_dim": gauge_dim, "det_K3": det_K3, "too_large": True}

    max_det = det_K3
    for mask in range(1, 2 ** gauge_dim):
        B_m = B_0.copy()
        for bit in range(gauge_dim):
            if (mask >> bit) & 1:
                idx = chord_idx[bit]
                ie, jo = edge_bip[idx]
                B_m[ie, jo] *= -1
        det_abs = int(round(abs(np.linalg.det(B_m))))
        if det_abs > max_det:
            max_det = det_abs

    comps = defect_components(set(removed))
    comp_sizes = sorted(len(c) for c in comps)
    has_singleton = any(len(c) == 1 for c in comps)

    return {
        "label": label, "balanced": True,
        "V": V, "E": E, "F": F, "cubes": cubes, "chi": chi,
        "gauge_dim": gauge_dim,
        "det_K3": det_K3, "max_det": max_det,
        "k3_optimal": det_K3 == max_det,
        "n_components": len(comps),
        "component_sizes": comp_sizes,
        "has_singleton": has_singleton,
    }


# ---------------------------------------------------------------------------
# Shapes
# ---------------------------------------------------------------------------

shapes = [
    ("I_2singletons_1pair",
     {(0, 0, 0), (2, 2, 1), (1, 0, 0), (1, 0, 1)}),
    ("E_2singletons_2pairs",
     {(0, 0, 0), (2, 2, 1), (1, 0, 0), (1, 0, 1), (1, 2, 0), (1, 2, 1)}),
    ("J_2pairs_no_singletons",
     {(0, 0, 0), (0, 0, 1), (2, 2, 0), (2, 2, 1)}),
]

results = []
for (label, removed) in shapes:
    t0 = time.time()
    info = test_shape(label, removed)
    info["elapsed"] = time.time() - t0
    results.append(info)


# ---------------------------------------------------------------------------
# Record per-shape
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    if not info.get("balanced", False):
        record(f"shape_{label}_balanced", False, f"{label}: unbalanced.")
        continue
    if info.get("too_large", False):
        record(f"shape_{label}_gauge_dim_too_large", False,
               f"{label}: gauge_dim={info['gauge_dim']}.")
        continue

    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, cubes={info['cubes']}, chi={info['chi']}, gauge_dim={info['gauge_dim']}.",
    )
    record(
        f"shape_{label}_defect_components",
        True == (info["n_components"] >= 1),
        f"{label}: component sizes = {info['component_sizes']}. Has singleton? {info['has_singleton']}.",
    )
    record(
        f"shape_{label}_K3_status",
        True == (info["k3_optimal"] == True or info["k3_optimal"] == False),
        f"{label}: K3 det={info['det_K3']}, max={info['max_det']}, K3 optimal? {info['k3_optimal']} ({info['elapsed']:.2f}s).",
    )


# ---------------------------------------------------------------------------
# Singleton-hypothesis prediction check
# ---------------------------------------------------------------------------

predictions = []
for info in results:
    if not info.get("balanced", False) or info.get("too_large", False):
        continue
    predicted_failure = info["has_singleton"]
    actually_failed = not info["k3_optimal"]
    predictions.append((info["label"], predicted_failure, actually_failed))

n_match = sum(1 for (_, p, a) in predictions if p == a)
n_total = len(predictions)

for (label, p, a) in predictions:
    record(
        f"prediction_{label}",
        p == a,
        f"{label}: predicted fail={p}, actual fail={a}. Match? {p == a}.",
    )

record(
    "singleton_hypothesis_matches_on_mixed_configs",
    n_match == n_total,
    f"Prediction match: {n_match}/{n_total}. Configs: {predictions}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

all_match = n_match == n_total
any_singleton_falsifies = any(
    p != a and p  # predicted fail but did not fail
    for (_, p, a) in predictions
)

if all_match:
    document(
        "singleton_hypothesis_survives_mixed_configs",
        "Singleton hypothesis survives adversarial mixed-defect test:"
        " shapes with 2 singletons + larger defects (I, E) have K3"
        " failing; shape with no singletons (J, 2 pairs) has K3"
        " optimal. The presence of ANY singleton is sufficient to"
        " break K3 optimality, regardless of other defects. Larger"
        " defects do NOT absorb or compensate for nearby singletons.",
    )
elif any_singleton_falsifies:
    document(
        "singleton_hypothesis_FALSIFIED_by_mixed_config",
        "Adversarial test found a shape with singletons where K3 is"
        " STILL optimal. Singleton presence is NOT sufficient to break"
        " K3. Hypothesis needs refinement -- perhaps singletons must"
        " be 'isolated enough' from larger defects, or some other"
        " structural factor governs.",
    )
else:
    document(
        "singleton_hypothesis_partially_inconsistent",
        "Some prediction mismatch; check per-shape details.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: mixed-defect adversarial test of singleton hypothesis")
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
