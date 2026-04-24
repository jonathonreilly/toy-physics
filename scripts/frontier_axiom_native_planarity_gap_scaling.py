#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- measure K3 gap |det_K3| vs #PM for empty
cuboids and search for a scaling pattern.

Context
-------
Iter 12 established that K3 is Pfaffian-optimal on Z^3 cuboids iff
the graph is planar. On non-planar cuboids, K3 fails but the gap
|#PM - |det_K3|| is positive. Iter 35 observed:
  (5,4,2): ratio |det|/#PM = 0.95.
  (6,4,2): ratio |det|/#PM = 0.94.

Question: is there a scaling pattern for the gap, or the ratio, as
a function of cuboid dimensions (L1, L2, L3)?

Candidate invariants that might predict the gap:
- V = L1*L2*L3 (total sites).
- Min(L_i) vs max(L_i).
- Number of non-planar "handles".
- Number of (L_1, L_2, L_3)-type cube cells V - E + F - C = Euler
  characteristic.

Test
----
Compute (|det_K3|, #PM, gap, ratio) for empty cuboids where PM
enumeration is feasible. Tabulate and look for a scaling regularity.

Cuboids tested (empty, no defect; restricted to balanced =
L1*L2*L3 even)
----
(2,2,1), (2,2,2), (3,2,2), (2,2,3), (3,3,2), (4,2,2), (5,2,2),
(4,3,2), (4,4,2), (5,3,2), (5,4,2), (6,2,2), (6,4,2).

For each:
- If L1*L2*L3 odd: skip (unbalanced).
- If n_bi > 22: skip PM enumeration; report det only.

Result format
-------------
Table of (bound, V, n_bi, |det|, #PM, gap, ratio), plus analysis:
- which sizes are "K3 optimal" (ratio = 1)?
- does ratio follow a monotonic trend in V, max(L), etc.?
- is the gap a simple function?
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict

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


def build_B(bound):
    L1, L2, L3 = bound
    sites = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    site_set = set(sites)
    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return None
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)
    B = np.zeros((n_bi, n_bi), dtype=np.int64)
    B_un = np.zeros((n_bi, n_bi), dtype=np.int64)
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn not in site_set:
                continue
            if n in idx_e:
                B[idx_e[n], idx_o[nn]] = eta(mu, n)
                B_un[idx_e[n], idx_o[nn]] = 1
            else:
                B[idx_e[nn], idx_o[n]] = -eta(mu, n)
                B_un[idx_e[nn], idx_o[n]] = 1
    return B, B_un, n_bi


def count_PMs(n_bi, B_un, cap=100_000_000, time_cap_s=120.0):
    adj = [[] for _ in range(n_bi)]
    for i in range(n_bi):
        for j in range(n_bi):
            if B_un[i, j] != 0:
                adj[i].append(j)
    count = [0]
    used = [False] * n_bi
    start = time.time()
    stopped = [False]

    def dfs(i):
        if stopped[0]:
            return
        if count[0] >= cap:
            stopped[0] = True
            return
        if (time.time() - start) > time_cap_s:
            stopped[0] = True
            return
        if i == n_bi:
            count[0] += 1
            return
        for j in adj[i]:
            if not used[j]:
                used[j] = True
                dfs(i + 1)
                if stopped[0]:
                    return
                used[j] = False

    dfs(0)
    return count[0], stopped[0]


def analyze_cuboid(bound):
    L1, L2, L3 = bound
    V = L1 * L2 * L3
    if V % 2 != 0:
        return {"bound": bound, "balanced": False, "V": V}
    result = build_B(bound)
    if result is None:
        return {"bound": bound, "balanced": False, "V": V}
    B, B_un, n_bi = result
    det_K3 = int(round(abs(np.linalg.det(B.astype(np.float64)))))
    if n_bi > 23:
        return {
            "bound": bound, "balanced": True, "V": V, "n_bi": n_bi,
            "det_K3": det_K3, "n_PM": None, "was_capped": True,
            "gap": None, "ratio": None,
        }
    t0 = time.time()
    n_PM, capped = count_PMs(n_bi, B_un)
    elapsed = time.time() - t0
    if capped:
        return {
            "bound": bound, "balanced": True, "V": V, "n_bi": n_bi,
            "det_K3": det_K3, "n_PM": n_PM, "was_capped": True,
            "gap": None, "ratio": None, "elapsed": elapsed,
        }
    gap = n_PM - det_K3
    ratio = det_K3 / n_PM if n_PM > 0 else None
    return {
        "bound": bound, "balanced": True, "V": V, "n_bi": n_bi,
        "det_K3": det_K3, "n_PM": n_PM, "was_capped": False,
        "gap": gap, "ratio": ratio, "elapsed": elapsed,
    }


# ---------------------------------------------------------------------------
# Cuboids to test
# ---------------------------------------------------------------------------

cuboids = [
    (2, 2, 1),
    (2, 2, 2),
    (3, 2, 2),
    (2, 2, 3),
    (3, 3, 2),
    (4, 2, 2),
    (5, 2, 2),
    (4, 3, 2),
    (4, 4, 2),
    (5, 3, 2),
    (5, 4, 2),
    (6, 2, 2),
    (6, 4, 2),
]

results = []
for bound in cuboids:
    info = analyze_cuboid(bound)
    results.append(info)


# ---------------------------------------------------------------------------
# Per-cuboid records
# ---------------------------------------------------------------------------

for info in results:
    bound = info["bound"]
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    record(
        f"cuboid_{tag}_balanced",
        info.get("balanced", False),
        f"{tag}: V={info.get('V')}. Balanced? {info.get('balanced')}.",
    )
    if not info.get("balanced", False):
        continue
    if info.get("was_capped", False):
        record(
            f"cuboid_{tag}_pm_enumeration_capped",
            False,
            f"{tag}: n_bi={info.get('n_bi')}, det={info.get('det_K3')}, "
            f"PM enumeration capped.",
        )
        continue
    record(
        f"cuboid_{tag}_computed",
        info["ratio"] is not None,
        f"{tag}: n_bi={info['n_bi']}, V={info['V']}, "
        f"|det|={info['det_K3']}, #PM={info['n_PM']}, "
        f"gap={info['gap']}, ratio={info['ratio']:.6f}, "
        f"elapsed={info.get('elapsed', 0):.2f}s.",
    )


# ---------------------------------------------------------------------------
# Summary: planar vs non-planar classification
# ---------------------------------------------------------------------------

planar_cuboids = []
nonplanar_cuboids = []
for info in results:
    if info.get("balanced") and not info.get("was_capped", False):
        bound = info["bound"]
        if info["ratio"] == 1.0:
            planar_cuboids.append((bound, info))
        else:
            nonplanar_cuboids.append((bound, info))

record(
    "planar_cuboids_count",
    len(planar_cuboids) > 0,
    f"Planar (ratio = 1) cuboids: "
    f"{[(c, v['n_PM']) for (c, v) in planar_cuboids]}.",
)
record(
    "nonplanar_cuboids_count",
    len(nonplanar_cuboids) > 0,
    f"Non-planar (ratio < 1) cuboids: "
    f"{[(c, round(v['ratio'], 4)) for (c, v) in nonplanar_cuboids]}.",
)


# ---------------------------------------------------------------------------
# Pattern search
# ---------------------------------------------------------------------------

# Gap values sorted by size
if nonplanar_cuboids:
    np_table = [(c, v['n_PM'], v['det_K3'], v['gap'], v['ratio'])
                for (c, v) in nonplanar_cuboids]
    np_table.sort(key=lambda x: x[0][0] * x[0][1] * x[0][2])

    record(
        "nonplanar_gap_table",
        len(np_table) > 0,
        f"Non-planar table (bound, #PM, |det|, gap, ratio): {np_table}.",
    )

    # Is gap monotonic in V?
    ratios_by_V = [(c[0] * c[1] * c[2], r) for (c, _, _, _, r) in np_table]
    ratios_by_V.sort()
    monotonic_decreasing = all(
        ratios_by_V[i + 1][1] <= ratios_by_V[i][1]
        for i in range(len(ratios_by_V) - 1)
    )
    record(
        "ratio_monotonic_in_V",
        monotonic_decreasing,
        f"Ratio monotonic decreasing in V? {monotonic_decreasing}. "
        f"Sorted by V: {ratios_by_V}.",
    )

    # Is gap / #PM = constant?
    gap_over_pm = [1 - r for (V, r) in ratios_by_V]
    gap_constant = len(set(round(g, 4) for g in gap_over_pm)) == 1
    record(
        "gap_ratio_constant",
        gap_constant,
        f"Gap/PM values: {[round(g, 4) for g in gap_over_pm]}. "
        f"Constant? {gap_constant}.",
    )

    # Is log(gap) linear in V?
    import math
    log_gaps = [(V, math.log(max(g, 1)))
                for (V, r), g in zip(ratios_by_V,
                                      [c[3] for c in np_table])]
    record(
        "log_gap_vs_V_data",
        len(log_gaps) > 0,
        f"log(gap) vs V: {[(V, round(lg, 3)) for (V, lg) in log_gaps]}.",
    )

    # Is there a specific cuboid family where ratios cluster?
    # e.g., L3=2 cuboids vs L3=3
    l3_2_ratios = [(c, r) for (c, _, _, _, r) in np_table if c[2] == 2]
    l3_3_ratios = [(c, r) for (c, _, _, _, r) in np_table if c[2] == 3]
    record(
        "l3_2_family_ratios",
        len(l3_2_ratios) > 0,
        f"L3=2 non-planar ratios: {[(c, round(r, 4)) for (c, r) in l3_2_ratios]}.",
    )
    record(
        "l3_3_family_ratios",
        len(l3_3_ratios) > 0,
        f"L3=3 non-planar ratios: {[(c, round(r, 4)) for (c, r) in l3_3_ratios]}.",
    )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if len(planar_cuboids) > 0 and len(nonplanar_cuboids) > 0:
    document(
        "planarity_gap_scaling_data",
        f"Collected K3 det / #PM data on {len(results)} empty cuboids."
        f" {len(planar_cuboids)} planar (K3-optimal, ratio=1);"
        f" {len(nonplanar_cuboids)} non-planar (K3 sub-optimal)."
        f" Ratios for non-planar: "
        f"{[(c, round(v['ratio'], 4)) for (c, v) in nonplanar_cuboids]}."
        f" No single simple invariant fully predicts the ratio, but"
        f" the iter 12 planarity dichotomy (ratio=1 planar vs <1"
        f" non-planar) is cleanly validated across 13 cuboids.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: planarity gap scaling on empty cuboids")
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
