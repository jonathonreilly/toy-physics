#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test whether the iter 21-22 localization
signature extends to 3+ singleton defect configurations.

Context
-------
The Kasteleyn thread has validated the edge-level localization
signature at 3 graph sizes with 2 singleton defects. An open
question asks whether the signature continues to hold with more
singletons, or whether multi-singleton interactions smear the
signal.

Parity constraint
-----------------
On a Z^3 cuboid, #PM > 0 requires |evens| = |odds| on the truncated
graph. Removing k singletons with e_k evens and o_k odds requires
e_k = o_k for balance. So k must be even. We test k = 4 (smallest
non-trivial beyond 2).

Test shapes
-----------
S1: (4,3,2) minus 4 corners on bottom face
    {(0,0,0), (3,0,0), (0,2,0), (3,2,0)}.
    Parities e, o, e, o -- balanced. All pairwise distances >= 2, so
    each site is isolated (singleton component).

S2: (4,4,2) minus 4 corners on bottom face
    {(0,0,0), (3,0,0), (0,3,0), (3,3,0)}.
    Parities e, o, o, e -- balanced. Not sigma-invariant (so
    reflection-degeneracy lemma does NOT apply).

S3: (4,4,2) minus sigma-invariant 4-set
    {(0,0,0), (3,0,0), (0,3,1), (3,3,1)}.
    sigma-swaps the pairs (0,0,0)<->(3,3,1) and (3,0,0)<->(0,3,1).
    n_bi = 14 (even), so reflection lemma doesn't force det=0 even
    though sigma is an automorphism.

For each shape
--------------
1. Verify balanced and contractible.
2. Verify all removed sites isolated (singletons).
3. DFS-enumerate PMs.
4. If |det_K3| > 0 (non-degenerate), compute top-5 vs bottom-5
   edge minority-fraction with midpoint distance comparison.
5. Pearson correlation of (frac, distance).
6. Report whether localization signature (min-dist < maj-dist AND
   corr < 0) holds.

If signature holds on at least 2 of 3 shapes, open question §6.3
is answered positively: the signature generalizes to 4-singleton
configurations. If it fails on all, the signal depends on small
defect count and smears with more singletons.
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


def defect_components(removed_set):
    """Partition removed set into connected components under Z^3
    nearest-neighbor adjacency."""
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
        return {"balanced": False, "V": len(sites), "evens": len(evens), "odds": len(odds),
                "chi": chi}

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
        "balanced": True, "evens_list": evens, "odds_list": odds,
        "V": len(sites), "E": len(edges), "F": plaquettes, "cubes": cubes, "chi": chi,
        "n_bi": n_bi, "B": B, "B_un": B_un,
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


def analyze_shape(label, bound, removed):
    G = build_graph(bound, removed)
    comps = defect_components(set(removed))
    comp_sizes = sorted(len(c) for c in comps)
    all_singletons = all(len(c) == 1 for c in comps)

    if not G["balanced"]:
        return {"label": label, "bound": bound, "removed": removed,
                "balanced": False, "comp_sizes": comp_sizes,
                "all_singletons": all_singletons, "V": G["V"]}

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

    min_freq = edge_frequency(minority_PMs, G["evens_list"], G["odds_list"], G["n_bi"])
    maj_freq = edge_frequency(majority_PMs, G["evens_list"], G["odds_list"], G["n_bi"])
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

    # Signature conditions
    signature_direction = (avg_top_min_dist < avg_top_maj_dist)
    signature_correlation = (corr < 0)
    signature_holds = signature_direction and signature_correlation

    return {
        "label": label, "bound": bound, "removed": removed,
        "balanced": True, "V": G["V"], "E": G["E"], "F": G["F"],
        "cubes": G["cubes"], "chi": G["chi"], "n_bi": G["n_bi"],
        "comp_sizes": comp_sizes, "all_singletons": all_singletons,
        "n_components": len(comps),
        "det_K3": det_K3,
        "n_PM": len(PMs), "n_plus": n_plus, "n_minus": n_minus,
        "was_capped": was_capped,
        "elapsed_enum": elapsed_enum,
        "avg_top_min_dist": avg_top_min_dist,
        "avg_top_maj_dist": avg_top_maj_dist,
        "top_min": [(tuple(sorted(e)), m, M, round(f, 4), round(d, 4))
                    for (e, m, M, f, d) in top_min],
        "top_maj": [(tuple(sorted(e)), m, M, round(f, 4), round(d, 4))
                    for (e, m, M, f, d) in top_maj],
        "corr_frac_dist": corr,
        "signature_direction": signature_direction,
        "signature_correlation": signature_correlation,
        "signature_holds": signature_holds,
    }


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

shapes = [
    ("S1_432_4corners_bottom", (4, 3, 2),
     {(0, 0, 0), (3, 0, 0), (0, 2, 0), (3, 2, 0)}),
    ("S2_442_4corners_bottom", (4, 4, 2),
     {(0, 0, 0), (3, 0, 0), (0, 3, 0), (3, 3, 0)}),
    ("S3_442_sigma_invariant_4set", (4, 4, 2),
     {(0, 0, 0), (3, 0, 0), (0, 3, 1), (3, 3, 1)}),
]

results = []
for (label, bound, removed) in shapes:
    info = analyze_shape(label, bound, removed)
    results.append(info)


# ---------------------------------------------------------------------------
# Per-shape records
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    record(
        f"shape_{label}_all_singletons",
        info["all_singletons"],
        f"{label}: defect components = {info['comp_sizes']}. "
        f"All singletons? {info['all_singletons']}.",
    )
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
        f"shape_{label}_PM_enumeration_completed",
        not info["was_capped"],
        f"{label}: #PM={info['n_PM']} (DFS {info['elapsed_enum']:.2f}s). "
        f"Capped? {info['was_capped']}.",
    )
    record(
        f"shape_{label}_signed_sum_matches_det",
        abs(info["n_plus"] - info["n_minus"]) == info["det_K3"],
        f"{label}: n_plus={info['n_plus']}, n_minus={info['n_minus']}, "
        f"|signed_sum|={abs(info['n_plus']-info['n_minus'])}, det_K3={info['det_K3']}.",
    )
    record(
        f"shape_{label}_K3_suboptimal_singleton",
        info["det_K3"] < info["n_PM"],
        f"{label}: K3 det={info['det_K3']}, #PM={info['n_PM']}. "
        f"Suboptimal (singleton-hypothesis)? {info['det_K3'] < info['n_PM']}.",
    )
    record(
        f"shape_{label}_non_degenerate",
        info["det_K3"] > 0,
        f"{label}: det_K3={info['det_K3']}. Non-degenerate (reflection lemma not acting)? "
        f"{info['det_K3'] > 0}.",
    )
    if info["det_K3"] == 0:
        continue  # Degenerate, localization meaningless
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
        f"shape_{label}_minority_biased_closer_to_removed",
        info["signature_direction"],
        f"{label}: avg top-5 min dist={info['avg_top_min_dist']:.3f}, "
        f"top-5 maj dist={info['avg_top_maj_dist']:.3f}. "
        f"Closer? {info['signature_direction']}.",
    )
    record(
        f"shape_{label}_negative_correlation",
        info["signature_correlation"],
        f"{label}: Pearson corr(min_frac, distance)={info['corr_frac_dist']:.3f}. "
        f"Localization (<0)? {info['signature_correlation']}.",
    )
    record(
        f"shape_{label}_localization_signature_holds",
        info["signature_holds"],
        f"{label}: signature (min<maj AND corr<0)? {info['signature_holds']}.",
    )


# ---------------------------------------------------------------------------
# Cross-shape summary
# ---------------------------------------------------------------------------

non_degenerate = [r for r in results if r.get("balanced") and r.get("det_K3", 0) > 0]
signature_count = sum(1 for r in non_degenerate if r["signature_holds"])
total_count = len(non_degenerate)

record(
    "localization_signature_extends_to_4_singletons",
    signature_count == total_count and total_count > 0,
    f"Signature holds on {signature_count}/{total_count} non-degenerate "
    f"4-singleton shapes. Open question 6.3 answered positively? "
    f"{signature_count == total_count and total_count > 0}.",
)

record(
    "localization_signature_holds_majority_4_singletons",
    signature_count >= (total_count + 1) // 2 and total_count > 0,
    f"Signature holds on at least majority of {total_count} tested shapes? "
    f"{signature_count >= (total_count + 1) // 2}. "
    f"({signature_count} of {total_count})",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if signature_count == total_count and total_count > 0:
    document(
        "localization_signature_extends_to_4_singletons",
        f"The edge-level K3 localization signature (top-5 minority-"
        f"biased edges have smaller midpoint distance to nearest"
        f" removed site than top-5 majority-biased, AND Pearson"
        f" correlation of (minority fraction, distance) is negative)"
        f" extends to all {total_count} tested 4-singleton shapes."
        f" The previously open question regarding multi-singleton"
        f" extension is answered positively: the signature is not"
        f" limited to 2-singleton configurations; it continues to"
        f" hold when the singleton count grows, with the 'near"
        f" removed sites' interpretation now spanning multiple"
        f" defect points. The structural signature is robust to"
        f" defect-count scaling for balanced singleton configurations.",
    )
elif signature_count > 0:
    document(
        "localization_signature_partially_extends",
        f"Signature holds on {signature_count} of {total_count} 4-singleton"
        f" shapes. Partial extension -- some configurations show signal"
        f" degrading. Need to identify which properties (distance between"
        f" singletons, symmetry class) determine signature strength.",
    )
else:
    document(
        "localization_signature_fails_at_4_singletons",
        f"Signature fails on all {total_count} tested 4-singleton shapes."
        f" The iter 21-22 result was specific to 2-singleton defects."
        f" Multi-singleton interactions smear the minority-biased"
        f" edge distribution. The localization claim must be restricted"
        f" to single or paired singletons.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: multi-singleton localization signature test")
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
