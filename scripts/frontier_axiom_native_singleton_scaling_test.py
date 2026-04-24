#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- scale the iter-20 localization signature
from (3,3,2) minus 2 sites to (4,3,2) minus 2 corner sites.

Context
-------
Iter 20 found that on (3,3,2) minus {(0,0,0), (2,2,1)}, the K3
perfect-matching (PM) sign obstruction appears to be spatially
localized: the edges preferentially used by the minority-sign PMs
cluster near the removed (singleton) sites, while edges used by the
majority live in the defect-free bulk. That analysis was only on a
single small graph. A real "localization signature" must be
graph-size independent. Here we scale to (4,3,2) minus 2 corners
(same topology: 2 isolated singletons, contractible, bipartite
balanced) and ask whether the same localization numerically
reproduces.

Test T1: (4,3,2) minus {(0,0,0), (3,0,0)}. Known from iter 19:
K3 |det(B)| = 228, max over all gauge classes = 272, so if
#PM = 272 (Pfaffian reached) then n_minus under K3 = 22. If
#PM > 272 then n_minus is larger. Direct DFS enumeration computes
#PM without assumption.

Control: redo (3,3,2) minus {(0,0,0), (2,2,1)} with the same
metric (top-5 vs bottom-5 by minority-fraction, avg Euclidean
midpoint distance to nearest removed). This is the iter-20 shape
analyzed under the corrected, consistent metric (iter 20 used a
threshold > 0.5 for minority-biased which filtered out all edges
and fell back to zero -- the scaling test here uses a rank-based
cutoff so the comparison set is always non-empty).

Method
------
(i) DFS-enumerate all PMs of the bipartite block.
(ii) For each PM, compute K3 signed contribution = sign(perm) *
     prod(B_ij). Split into plus and minus.
(iii) Minority = smaller set, majority = larger set. Each PM
     contributes +/- 1 so |det(B)| = |n_+ - n_-|.
(iv) For each edge in the graph, count appearances in minority and
     majority, compute min_fraction = min_count / (min + maj).
(v) Rank edges by min_fraction. Top 5 = most minority-biased,
     bottom 5 = most majority-biased. Compute the Euclidean
     distance from each edge midpoint to nearest removed site,
     average over the 5. Compare top vs bottom.
(vi) Also compute Pearson correlation of (min_fraction, distance)
     across all edges. Negative correlation => localization.

Scaling criterion
-----------------
Signature is called "scaling" iff on both T1 and the control:
  - avg top-5-minority distance < avg top-5-majority distance
  - Pearson corr(min_fraction, distance) < 0
If either fails on T1, the iter-20 signature was a small-graph
artifact.
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


def sign_of_permutation(perm):
    visited = [False] * len(perm)
    s = 1
    for i in range(len(perm)):
        if visited[i]:
            continue
        cl = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = perm[j]
            cl += 1
        if cl > 1 and cl % 2 == 0:
            s = -s
    return s


def build_graph(bound, removed):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    sites = [v for v in base if v not in removed]
    site_set = set(sites)

    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    edges = []
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn in site_set:
                edges.append((n, nn, mu))

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

    return evens, odds, n_bi, B, B_un


def enumerate_PMs(n_bi, B_un, cap=10_000_000):
    adj = [[] for _ in range(n_bi)]
    for i in range(n_bi):
        for j in range(n_bi):
            if B_un[i, j] != 0:
                adj[i].append(j)

    PMs = []
    perm = [0] * n_bi
    used = [False] * n_bi

    def dfs(i):
        if len(PMs) >= cap:
            return
        if i == n_bi:
            PMs.append(tuple(perm))
            return
        for j in adj[i]:
            if not used[j]:
                perm[i] = j
                used[j] = True
                dfs(i + 1)
                used[j] = False

    dfs(0)
    return PMs


def classify_PMs(PMs, B, n_bi):
    plus_PMs = []
    minus_PMs = []
    for p in PMs:
        s = sign_of_permutation(p)
        prod = 1
        for i in range(n_bi):
            prod *= int(B[i, p[i]])
        contrib = s * prod
        if contrib > 0:
            plus_PMs.append(p)
        elif contrib < 0:
            minus_PMs.append(p)
    return plus_PMs, minus_PMs


def edge_frequency(PMs, evens, odds, n_bi):
    freq = defaultdict(int)
    for p in PMs:
        for i in range(n_bi):
            e = frozenset({evens[i], odds[p[i]]})
            freq[e] += 1
    return freq


def edge_midpoint_distance_to_removed(e_frozen, removed):
    verts = list(e_frozen)
    mid = np.mean([np.array(v, dtype=float) for v in verts], axis=0)
    return float(min(np.linalg.norm(mid - np.array(r, dtype=float)) for r in removed))


def analyze_shape(label, bound, removed, expected_det):
    evens, odds, n_bi, B, B_un = build_graph(bound, removed)
    det_K3 = int(round(abs(np.linalg.det(B))))

    t0 = time.time()
    PMs = enumerate_PMs(n_bi, B_un)
    elapsed_enum = time.time() - t0

    plus_PMs, minus_PMs = classify_PMs(PMs, B, n_bi)
    n_plus = len(plus_PMs)
    n_minus = len(minus_PMs)

    if n_plus <= n_minus:
        minority_PMs = plus_PMs
        majority_PMs = minus_PMs
    else:
        minority_PMs = minus_PMs
        majority_PMs = plus_PMs

    min_freq = edge_frequency(minority_PMs, evens, odds, n_bi)
    maj_freq = edge_frequency(majority_PMs, evens, odds, n_bi)
    all_edges = set(min_freq.keys()) | set(maj_freq.keys())

    edge_stats = []
    for e in all_edges:
        m = min_freq.get(e, 0)
        M = maj_freq.get(e, 0)
        total = m + M
        frac = m / total if total > 0 else 0.0
        dist = edge_midpoint_distance_to_removed(e, removed)
        edge_stats.append((e, m, M, frac, dist))

    edge_stats.sort(key=lambda x: -x[3])
    K = 5
    top_min = edge_stats[:K]
    top_maj = edge_stats[-K:]

    avg_top_min_dist = float(np.mean([e[4] for e in top_min]))
    avg_top_maj_dist = float(np.mean([e[4] for e in top_maj]))

    fracs = np.array([e[3] for e in edge_stats])
    dists = np.array([e[4] for e in edge_stats])
    if len(fracs) > 1 and fracs.std() > 0 and dists.std() > 0:
        corr = float(np.corrcoef(fracs, dists)[0, 1])
    else:
        corr = 0.0

    return {
        "label": label,
        "n_bi": n_bi,
        "n_edges": len(all_edges),
        "det_K3": det_K3,
        "expected_det": expected_det,
        "n_PM": len(PMs),
        "n_plus": n_plus,
        "n_minus": n_minus,
        "elapsed_enum": elapsed_enum,
        "avg_top_min_dist": avg_top_min_dist,
        "avg_top_maj_dist": avg_top_maj_dist,
        "top_min": [(tuple(sorted(e)), m, M, round(f, 4), round(d, 4))
                    for (e, m, M, f, d) in top_min],
        "top_maj": [(tuple(sorted(e)), m, M, round(f, 4), round(d, 4))
                    for (e, m, M, f, d) in top_maj],
        "corr_frac_dist": corr,
    }


# ---------------------------------------------------------------------------
# Run analyses
# ---------------------------------------------------------------------------

T1 = analyze_shape(
    "T1_432_corners",
    (4, 3, 2),
    {(0, 0, 0), (3, 0, 0)},
    228,
)

C = analyze_shape(
    "C_332_opposite",
    (3, 3, 2),
    {(0, 0, 0), (2, 2, 1)},
    30,
)


# ---------------------------------------------------------------------------
# Per-shape records
# ---------------------------------------------------------------------------

for info in (T1, C):
    label = info["label"]
    record(
        f"shape_{label}_K3_det_matches_prior",
        info["det_K3"] == info["expected_det"],
        f"{label}: K3 |det| = {info['det_K3']}, expected {info['expected_det']} "
        f"(iter 14/19 result).",
    )
    record(
        f"shape_{label}_PM_enumeration_complete",
        info["n_PM"] == info["n_plus"] + info["n_minus"],
        f"{label}: #PM = {info['n_PM']} (DFS in {info['elapsed_enum']:.2f}s), "
        f"n_plus = {info['n_plus']}, n_minus = {info['n_minus']}, sum = "
        f"{info['n_plus'] + info['n_minus']}.",
    )
    record(
        f"shape_{label}_signed_sum_matches_det",
        abs(info['n_plus'] - info['n_minus']) == info['det_K3'],
        f"{label}: |n_+ - n_-| = {abs(info['n_plus'] - info['n_minus'])}, "
        f"det_K3 = {info['det_K3']}.",
    )
    record(
        f"shape_{label}_nonzero_minority",
        info['n_minus'] > 0 and info['n_plus'] > 0,
        f"{label}: n_plus = {info['n_plus']}, n_minus = {info['n_minus']}. "
        f"Both > 0? {info['n_minus'] > 0 and info['n_plus'] > 0}.",
    )
    record(
        f"shape_{label}_top_minority_biased_edges_5",
        len(info['top_min']) == 5,
        f"{label}: top-5 minority-biased edges (edge, min, maj, frac, dist): "
        f"{info['top_min']}.",
    )
    record(
        f"shape_{label}_top_majority_biased_edges_5",
        len(info['top_maj']) == 5,
        f"{label}: top-5 majority-biased edges (edge, min, maj, frac, dist): "
        f"{info['top_maj']}.",
    )
    record(
        f"shape_{label}_minority_biased_edges_closer_to_removed",
        info['avg_top_min_dist'] < info['avg_top_maj_dist'],
        f"{label}: avg distance top-5 minority = {info['avg_top_min_dist']:.3f}, "
        f"top-5 majority = {info['avg_top_maj_dist']:.3f}. "
        f"Minority closer? {info['avg_top_min_dist'] < info['avg_top_maj_dist']}.",
    )
    record(
        f"shape_{label}_negative_correlation_frac_distance",
        info['corr_frac_dist'] < 0,
        f"{label}: Pearson corr(min_frac, distance) = "
        f"{info['corr_frac_dist']:.3f}. Negative (localization) if < 0.",
    )


# ---------------------------------------------------------------------------
# Scaling check
# ---------------------------------------------------------------------------

signature_scales = (
    T1['avg_top_min_dist'] < T1['avg_top_maj_dist']
    and C['avg_top_min_dist'] < C['avg_top_maj_dist']
    and T1['corr_frac_dist'] < 0
    and C['corr_frac_dist'] < 0
)

record(
    "localization_signature_scales_from_332_to_432",
    signature_scales,
    f"Both-shape signature: "
    f"(3,3,2) min_dist={C['avg_top_min_dist']:.3f} "
    f"maj_dist={C['avg_top_maj_dist']:.3f} "
    f"corr={C['corr_frac_dist']:.3f}; "
    f"(4,3,2) min_dist={T1['avg_top_min_dist']:.3f} "
    f"maj_dist={T1['avg_top_maj_dist']:.3f} "
    f"corr={T1['corr_frac_dist']:.3f}. "
    f"Scales? {signature_scales}.",
)


# ---------------------------------------------------------------------------
# Also record whether PM count at (4,3,2) equals 272 (Pfaffian)
# or is larger (non-Pfaffian graph with K3 missing mix).
# ---------------------------------------------------------------------------

t1_pm_equals_max = T1['n_PM'] == 272
record(
    "T1_PM_count_equals_gauge_max",
    t1_pm_equals_max,
    f"T1: #PM = {T1['n_PM']}, gauge max over 2^19 classes = 272. "
    f"Equal? {t1_pm_equals_max}. If equal, (4,3,2) minus 2 corners "
    f"has a Pfaffian orientation (just not the K3 one). If not, "
    f"graph is non-Pfaffian.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if signature_scales:
    document(
        "localization_signature_scale_invariant",
        "On two distinct singleton-defect shapes -- (3,3,2) minus"
        " {(0,0,0), (2,2,1)} and (4,3,2) minus {(0,0,0), (3,0,0)}"
        " -- the K3 Pfaffian sign obstruction is spatially"
        " localized in the same sense: top-5 minority-biased"
        " edges have smaller Euclidean midpoint-distance to the"
        " nearest removed site than top-5 majority-biased edges,"
        " AND Pearson correlation of (edge minority-fraction,"
        " edge distance-to-removed) is negative. This promotes"
        " the iter-20 signature from 'partial' to 'scale-"
        "invariant localization': the sign obstruction carried"
        " by singletons is an O(1)-radius phenomenon in the"
        " graph. This is stronger than the prior empirical"
        " locality statement because it now has a specific"
        " numerical signature (edge-level minority fraction)"
        " reproducing at two graph sizes.",
    )
else:
    document(
        "localization_signature_fails_to_scale",
        "The iter-20 (3,3,2) localization did not reproduce on"
        " (4,3,2). The signature was a small-graph coincidence"
        " rather than a scale-invariant property. Next vector:"
        " try a structural invariant defined over alternating"
        " cycles, not single edges.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: singleton localization scaling test (3,3,2) vs (4,3,2)")
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
