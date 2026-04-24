#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- push localization signature to (4,4,2),
testing multiple singleton configurations to avoid symmetry-forced
degeneracy.

Context
-------
Iter 21 established that the edge-level K3 Pfaffian localization
signature (top-5 minority-biased edges have smaller midpoint
distance to removed singletons than top-5 majority-biased, AND
Pearson correlation of (minority-fraction, distance) is negative)
scales from (3,3,2) minus 2 to (4,3,2) minus 2 corners.

Here we push to (4,4,2) minus 2 singletons. However, if both
removed sites are related by reflection through the cuboid center
AND the bipartite dimension is odd, K3 det can be forced to 0 by
symmetry (the per-row factor in the reflection has sign -1 coming
from eta_2 on even-L1, so for n_bi odd, det(B) = -det(B) => 0).
We test multiple shapes and ask whether localization holds on the
non-degenerate ones.

Test shapes on (4,4,2)
---------------------
T2a diagonal: {(0,0,0), (3,3,1)} -- reflection-paired, n_bi = 15
  odd, so K3 det = 0 expected.
T2b x-opposite: {(0,0,0), (3,0,0)} -- on bottom face, NOT
  reflection-paired through cuboid center.
T2c face-opposite: {(0,0,0), (0,3,0)} -- on bottom face, NOT
  reflection-paired through cuboid center.

Both T2b and T2c are balanced bipartite (parities 0+3 = even+odd),
contractible (corners removed), non-adjacent (distances 3 in L1).
If localization holds on T2b and T2c, signature scales across
three graph sizes despite the T2a degeneracy.
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
    balanced = (n_bi == len(odds))

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
        "evens": evens, "odds": odds, "n_bi": n_bi, "balanced": balanced,
        "V": len(sites), "E": len(edges), "F": plaquettes, "cubes": cubes,
        "chi": chi, "B": B, "B_un": B_un,
    }


def enumerate_PMs(n_bi, B_un, cap=2_000_000, time_cap_s=60.0):
    adj = [[] for _ in range(n_bi)]
    for i in range(n_bi):
        for j in range(n_bi):
            if B_un[i, j] != 0:
                adj[i].append(j)

    PMs = []
    perm = [0] * n_bi
    used = [False] * n_bi
    start = time.time()
    stopped = [False]

    def dfs(i):
        if stopped[0]:
            return
        if len(PMs) >= cap:
            stopped[0] = True
            return
        if (time.time() - start) > time_cap_s:
            stopped[0] = True
            return
        if i == n_bi:
            PMs.append(tuple(perm))
            return
        for j in adj[i]:
            if not used[j]:
                perm[i] = j
                used[j] = True
                dfs(i + 1)
                if stopped[0]:
                    return
                used[j] = False

    dfs(0)
    return PMs, stopped[0]


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


def analyze(label, bound, removed):
    G = build_graph(bound, removed)
    det_K3 = int(round(abs(np.linalg.det(G["B"]))))
    t0 = time.time()
    PMs, was_capped = enumerate_PMs(G["n_bi"], G["B_un"])
    elapsed_enum = time.time() - t0
    plus_PMs, minus_PMs = classify_PMs(PMs, G["B"], G["n_bi"])
    n_plus = len(plus_PMs); n_minus = len(minus_PMs)

    if n_plus <= n_minus:
        minority_PMs = plus_PMs; majority_PMs = minus_PMs
    else:
        minority_PMs = minus_PMs; majority_PMs = plus_PMs

    min_freq = edge_frequency(minority_PMs, G["evens"], G["odds"], G["n_bi"])
    maj_freq = edge_frequency(majority_PMs, G["evens"], G["odds"], G["n_bi"])
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

    avg_top_min_dist = float(np.mean([e[4] for e in top_min])) if top_min else 0.0
    avg_top_maj_dist = float(np.mean([e[4] for e in top_maj])) if top_maj else 0.0

    fracs = np.array([e[3] for e in edge_stats])
    dists = np.array([e[4] for e in edge_stats])
    if len(fracs) > 1 and fracs.std() > 0 and dists.std() > 0:
        corr = float(np.corrcoef(fracs, dists)[0, 1])
    else:
        corr = 0.0

    return {
        "label": label, "bound": bound, "removed": removed,
        "balanced": G["balanced"],
        "V": G["V"], "E": G["E"], "F": G["F"], "cubes": G["cubes"], "chi": G["chi"],
        "n_bi": G["n_bi"],
        "det_K3": det_K3,
        "n_PM": len(PMs),
        "n_plus": n_plus, "n_minus": n_minus,
        "was_capped": was_capped,
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
# Run tests on (4,4,2): diagonal (degenerate) + two non-diagonal.
# ---------------------------------------------------------------------------

T2a = analyze(
    "T2a_442_diagonal",
    (4, 4, 2),
    {(0, 0, 0), (3, 3, 1)},
)
T2b = analyze(
    "T2b_442_x_opposite",
    (4, 4, 2),
    {(0, 0, 0), (3, 0, 0)},
)
T2c = analyze(
    "T2c_442_y_opposite",
    (4, 4, 2),
    {(0, 0, 0), (0, 3, 0)},
)


# ---------------------------------------------------------------------------
# Per-shape records
# ---------------------------------------------------------------------------

for info in (T2a, T2b, T2c):
    label = info["label"]
    record(
        f"shape_{label}_balanced",
        info["balanced"],
        f"{label}: V={info['V']}, evens={info['n_bi']}, odds={info['V']-info['n_bi']}. Balanced? {info['balanced']}.",
    )
    record(
        f"shape_{label}_contractible",
        info["chi"] == 1,
        f"{label}: V={info['V']}, E={info['E']}, F={info['F']}, cubes={info['cubes']}, chi={info['chi']}.",
    )
    record(
        f"shape_{label}_PM_enumeration_completed",
        not info["was_capped"],
        f"{label}: #PM={info['n_PM']} (DFS {info['elapsed_enum']:.2f}s). Capped? {info['was_capped']}.",
    )
    record(
        f"shape_{label}_signed_sum_matches_det",
        abs(info["n_plus"] - info["n_minus"]) == info["det_K3"],
        f"{label}: n_plus={info['n_plus']}, n_minus={info['n_minus']}, "
        f"|signed_sum|={abs(info['n_plus']-info['n_minus'])}, det_K3={info['det_K3']}.",
    )


# ---------------------------------------------------------------------------
# Explicit symmetry-degeneracy record for T2a.
# ---------------------------------------------------------------------------

record(
    "T2a_diagonal_forces_det_zero_by_reflection_symmetry",
    T2a["det_K3"] == 0 and T2a["n_plus"] == T2a["n_minus"],
    f"T2a (4,4,2) minus {{(0,0,0), (3,3,1)}}: det_K3={T2a['det_K3']}, "
    f"n_plus={T2a['n_plus']}, n_minus={T2a['n_minus']}. "
    f"Reflection through center maps removed site pair to itself; combined with "
    f"odd bipartite dim n_bi={T2a['n_bi']} and eta_2 sign flip under "
    f"L1=4 reflection, det is forced to 0 (=> equal +/- split).",
)


# ---------------------------------------------------------------------------
# Localization analysis on non-degenerate T2b and T2c.
# ---------------------------------------------------------------------------

for info in (T2b, T2c):
    label = info["label"]
    record(
        f"shape_{label}_det_nonzero",
        info["det_K3"] > 0,
        f"{label}: det_K3={info['det_K3']}. Non-zero (non-degenerate)? {info['det_K3'] > 0}.",
    )
    record(
        f"shape_{label}_K3_suboptimal",
        info["det_K3"] < info["n_PM"],
        f"{label}: K3 det={info['det_K3']}, #PM={info['n_PM']}. Suboptimal? {info['det_K3'] < info['n_PM']}.",
    )
    record(
        f"shape_{label}_top_minority_biased_edges_5",
        len(info["top_min"]) == 5,
        f"{label}: top-5 minority-biased: {info['top_min']}.",
    )
    record(
        f"shape_{label}_top_majority_biased_edges_5",
        len(info["top_maj"]) == 5,
        f"{label}: top-5 majority-biased: {info['top_maj']}.",
    )
    record(
        f"shape_{label}_minority_biased_edges_closer",
        info["avg_top_min_dist"] < info["avg_top_maj_dist"],
        f"{label}: avg top-5 min dist={info['avg_top_min_dist']:.3f}, "
        f"top-5 maj dist={info['avg_top_maj_dist']:.3f}. Closer? "
        f"{info['avg_top_min_dist'] < info['avg_top_maj_dist']}.",
    )
    record(
        f"shape_{label}_negative_correlation",
        info["corr_frac_dist"] < 0,
        f"{label}: Pearson corr(min_frac, distance)={info['corr_frac_dist']:.3f}. "
        f"Localization if <0.",
    )


# ---------------------------------------------------------------------------
# Scaling across 3 sizes (3,3,2) / (4,3,2) / (4,4,2).
# ---------------------------------------------------------------------------

# Test: does localization hold on at least one (4,4,2) non-degenerate shape?
localization_442 = (
    T2b["avg_top_min_dist"] < T2b["avg_top_maj_dist"]
    and T2b["corr_frac_dist"] < 0
) or (
    T2c["avg_top_min_dist"] < T2c["avg_top_maj_dist"]
    and T2c["corr_frac_dist"] < 0
)
record(
    "localization_signature_on_some_442_non_degenerate",
    localization_442,
    f"Localization (min<maj AND corr<0) holds on T2b or T2c? {localization_442}. "
    f"T2b min={T2b['avg_top_min_dist']:.3f} maj={T2b['avg_top_maj_dist']:.3f} "
    f"corr={T2b['corr_frac_dist']:.3f}. "
    f"T2c min={T2c['avg_top_min_dist']:.3f} maj={T2c['avg_top_maj_dist']:.3f} "
    f"corr={T2c['corr_frac_dist']:.3f}.",
)

# Test: does localization hold on BOTH non-degenerate shapes?
localization_442_both = (
    T2b["avg_top_min_dist"] < T2b["avg_top_maj_dist"]
    and T2b["corr_frac_dist"] < 0
    and T2c["avg_top_min_dist"] < T2c["avg_top_maj_dist"]
    and T2c["corr_frac_dist"] < 0
)
record(
    "localization_signature_on_both_442_non_degenerate",
    localization_442_both,
    f"Both T2b and T2c show localization? {localization_442_both}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if localization_442_both:
    document(
        "localization_signature_three_scale_with_symmetry_caveat",
        "The edge-level K3 Pfaffian localization signature"
        " reproduces on non-degenerate (4,4,2) singleton shapes"
        " (T2b and T2c, both with K3 det nonzero). It becomes"
        " trivially non-informative on the diagonal T2a shape"
        " because reflection through the cuboid center combined"
        " with eta_2 sign flip on even L1 forces K3 det=0 when"
        " the bipartite dimension is odd -- so +/- matching"
        " counts are equal by symmetry and 'minority' / "
        "'majority' labels lose meaning. Restricting to"
        " non-degenerate configurations: localization holds at"
        " 3 scales (3,3,2)/(4,3,2)/(4,4,2). The Pfaffian"
        " obstruction around singleton defects is a"
        " scale-robust local property, with the caveat that"
        " symmetry-paired singleton configurations with odd"
        " bipartite dimension degenerate into equal +/- sum.",
    )
elif localization_442:
    document(
        "localization_partial_three_scale",
        "Localization holds on only one of the two (4,4,2)"
        " non-degenerate shapes. Signature is still present at"
        " 3 scales but the specific metric may require refinement"
        " for shapes where singletons lie on shape boundaries.",
    )
else:
    document(
        "localization_fails_at_442_non_degenerate",
        "Localization signature fails on both (4,4,2)"
        " non-degenerate shapes. The (3,3,2)-(4,3,2) result"
        " may be a 2-scale coincidence. Need different"
        " structural invariant.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: singleton localization scaling test at (4,4,2)")
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
