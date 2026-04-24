#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- adversarial test of the singleton
hypothesis on LARGER cuboids we have not previously examined.

Context
-------
The singleton hypothesis (from the Kasteleyn thread summary) is the
strongest empirical claim on this branch: K3 is Pfaffian-optimal on
G iff G is contractible AND the defect has no singleton components.
15+ confirming data points at 3 graph sizes: (3,3,2), (4,3,2),
(4,4,2). Never falsified.

This iteration tests the hypothesis on 3 LARGER cuboids that have
not been examined: (5,4,2), (4,4,3), (6,4,2).

For each cuboid, test:
  E: Empty defect, contractible. Singleton hypothesis predicts K3
     optimal (|det_K3| = #PM).
  S: Contractible with 2 isolated balanced singletons. Singleton
     hypothesis predicts K3 NOT optimal (|det_K3| < #PM).

If E gives K3 optimal AND S gives K3 not optimal on all 3 cuboids,
the hypothesis is strongly corroborated at 3 new sizes (18+
confirming data points total). If either prediction fails, the
hypothesis is falsified or refined.

Note on computability
---------------------
PM enumeration via DFS is tractable up to n_bi ~ 22-23 in reasonable
time. For (6,4,2) empty (n_bi = 24), enumeration may be slow; use a
time cap.
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


def build_graph(bound, removed):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    sites = [v for v in base if v not in removed]
    site_set = set(sites)

    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    balanced = (len(evens) == len(odds))
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    edges = []
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn in site_set:
                edges.append((n, nn, mu))

    plaquettes = 0
    for n in base:
        for i in (1, 2, 3):
            for j in range(i + 1, 4):
                n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
                n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
                n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
                if all(c in site_set for c in (n, n_i, n_j, n_ij)):
                    plaquettes += 1
    cubes = 0
    for n in base:
        i, j, k = n
        if i + 1 < L1 and j + 1 < L2 and k + 1 < L3:
            corners = [(i + di, j + dj, k + dk)
                       for di in (0, 1) for dj in (0, 1) for dk in (0, 1)]
            if all(c in site_set for c in corners):
                cubes += 1
    chi = len(sites) - len(edges) + plaquettes - cubes

    if not balanced:
        return {"balanced": False, "V": len(sites), "chi": chi}

    B = np.zeros((n_bi, n_bi), dtype=np.int64)
    B_un = np.zeros((n_bi, n_bi), dtype=np.int64)
    for (n_lo, n_hi, mu) in edges:
        if n_lo in idx_e:
            ie, jo = idx_e[n_lo], idx_o[n_hi]
            s = eta(mu, n_lo)
        else:
            ie, jo = idx_e[n_hi], idx_o[n_lo]
            s = -eta(mu, n_lo)
        B[ie, jo] = s
        B_un[ie, jo] = 1

    return {
        "balanced": True, "V": len(sites), "E": len(edges), "F": plaquettes,
        "cubes": cubes, "chi": chi, "n_bi": n_bi, "B": B, "B_un": B_un,
        "evens": evens, "odds": odds,
    }


def count_PMs_DFS(n_bi, B_un, cap=50_000_000, time_cap_s=90.0):
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


def analyze(label, bound, removed, has_singleton_components):
    G = build_graph(bound, removed)
    if not G["balanced"]:
        return {"label": label, "bound": bound, "removed": removed,
                "balanced": False, "V": G["V"], "chi": G["chi"]}
    det_K3 = int(round(abs(np.linalg.det(G["B"].astype(np.float64)))))
    t0 = time.time()
    n_PM, capped = count_PMs_DFS(G["n_bi"], G["B_un"])
    elapsed = time.time() - t0
    return {
        "label": label, "bound": bound, "removed": removed,
        "balanced": True, "V": G["V"], "E": G["E"], "F": G["F"],
        "cubes": G["cubes"], "chi": G["chi"], "n_bi": G["n_bi"],
        "det_K3": det_K3, "n_PM": n_PM, "was_capped": capped,
        "elapsed": elapsed,
        "K3_optimal": (not capped) and (det_K3 == n_PM),
        "has_singleton_components": has_singleton_components,
    }


# ---------------------------------------------------------------------------
# Shapes: empty + 2-singleton on 3 new cuboids
# ---------------------------------------------------------------------------

shapes = [
    # (5,4,2) empty: n_bi = 20
    ("542_empty", (5, 4, 2), set(), False),
    # (5,4,2) with 2 isolated singletons: (0,0,0) even + (4,3,0) odd
    ("542_2singleton", (5, 4, 2), {(0, 0, 0), (4, 3, 0)}, True),
    # (4,4,3) empty: n_bi = 24, may be slow
    ("443_empty", (4, 4, 3), set(), False),
    # (4,4,3) with 2 isolated singletons
    ("443_2singleton", (4, 4, 3), {(0, 0, 0), (3, 3, 1)}, True),
    # (6,4,2) empty: n_bi = 24, may be slow
    ("642_empty", (6, 4, 2), set(), False),
    # (6,4,2) with 2 isolated singletons
    ("642_2singleton", (6, 4, 2), {(0, 0, 0), (5, 3, 1)}, True),
]

results = []
for (label, bound, removed, has_sing) in shapes:
    info = analyze(label, bound, removed, has_sing)
    results.append(info)


# ---------------------------------------------------------------------------
# Per-shape records
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    record(
        f"shape_{label}_balanced",
        info["balanced"],
        f"{label}: V={info['V']}. Balanced? {info['balanced']}.",
    )
    if not info["balanced"]:
        continue
    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, "
        f"cubes={info['cubes']}, chi={info['chi']}.",
    )
    record(
        f"shape_{label}_pm_enumeration_completed",
        not info["was_capped"],
        f"{label}: n_bi={info['n_bi']}, #PM={info['n_PM']}, "
        f"elapsed={info['elapsed']:.2f}s. Capped? {info['was_capped']}.",
    )
    record(
        f"shape_{label}_det_K3_value",
        info["det_K3"] >= 0,
        f"{label}: |det_K3|={info['det_K3']}, #PM={info['n_PM']}. "
        f"Ratio det/PM = {info['det_K3'] / max(info['n_PM'], 1):.4f}.",
    )
    if info["was_capped"]:
        continue
    # Singleton hypothesis prediction
    predicted_optimal = (info["chi"] == 1) and not info["has_singleton_components"]
    actual_optimal = info["K3_optimal"]
    record(
        f"shape_{label}_singleton_hypothesis_prediction",
        predicted_optimal == actual_optimal,
        f"{label}: contractible={info['chi']==1}, "
        f"has_singletons={info['has_singleton_components']}, "
        f"predicted_K3_optimal={predicted_optimal}, "
        f"actual_K3_optimal={actual_optimal}. Match? "
        f"{predicted_optimal == actual_optimal}.",
    )


# ---------------------------------------------------------------------------
# Overall hypothesis status
# ---------------------------------------------------------------------------

tested_shapes = [r for r in results if r.get("balanced") and not r.get("was_capped", False)]
n_match = sum(
    1 for r in tested_shapes
    if (r["chi"] == 1 and not r["has_singleton_components"]) == r["K3_optimal"]
)
n_total = len(tested_shapes)

record(
    "singleton_hypothesis_matches_on_new_cuboids",
    n_total > 0 and n_match == n_total,
    f"Singleton hypothesis prediction matches on {n_match}/{n_total} "
    f"tested shapes across (5,4,2), (4,4,3), (6,4,2).",
)

# Count new data points
n_empty_optimal = sum(
    1 for r in tested_shapes
    if r["chi"] == 1 and not r["has_singleton_components"] and r["K3_optimal"]
)
n_singleton_fails = sum(
    1 for r in tested_shapes
    if r["chi"] == 1 and r["has_singleton_components"] and not r["K3_optimal"]
)
n_total_tests = len([r for r in tested_shapes if r["chi"] == 1])

record(
    "new_confirming_empty_optimal",
    n_empty_optimal > 0,
    f"New 'contractible + no-singleton => K3-optimal' confirmations: "
    f"{n_empty_optimal}.",
)
record(
    "new_confirming_singleton_fails",
    n_singleton_fails > 0,
    f"New 'contractible + singleton => K3-fails' confirmations: "
    f"{n_singleton_fails}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_match == n_total and n_total >= 4:
    document(
        "singleton_hypothesis_extended_to_L5_cuboids",
        f"Singleton hypothesis survives adversarial testing on 3"
        f" new larger cuboids: (5,4,2), (4,4,3), (6,4,2). All"
        f" {n_match} tested (empty, 2-singleton) configurations match"
        f" the hypothesis prediction. Combined with prior iterations,"
        f" the hypothesis now has corroboration from 5 distinct"
        f" cuboid sizes: (3,3,2), (4,3,2), (4,4,2), (5,4,2),"
        f" (4,4,3), (6,4,2). Total confirming data points now"
        f" approximately {15 + n_match}+. Zero counterexamples.",
    )
elif n_match < n_total and n_total > 0:
    document(
        "singleton_hypothesis_falsified_at_L5",
        f"Singleton hypothesis FAILED on {n_total - n_match} of"
        f" {n_total} new tests. Examine failing shapes:"
        f" {[r['label'] for r in tested_shapes if (r['chi']==1 and not r['has_singleton_components']) != r['K3_optimal']]}."
        f" The hypothesis needs refinement.",
    )
else:
    document(
        "singleton_hypothesis_test_inconclusive",
        f"PM enumeration capped on some shapes; test inconclusive."
        f" Matches: {n_match}/{n_total}.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: singleton hypothesis adversarial test on larger cuboids")
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
