#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test whether the localization signature
distinguishes SINGLETON defect components from larger defect
components in a mixed-defect graph.

Context
-------
Iter 21-22 established the edge-level localization signature for
2-singleton defects. Iter 26 extended it to 4-singleton defects.
But both had homogeneous defect sets (all components size 1).
Open question: in a shape with MIXED defect components (e.g., 1
singleton + 1 pair), does the signature still concentrate around
singletons specifically, or does it localize uniformly around all
removed sites?

Falsification vectors
---------------------
- If signature concentrates around singletons but NOT around pairs,
  the singleton hypothesis is corroborated with a finer structural
  signal -- the sign obstruction is tied specifically to singleton
  defect components.
- If signature concentrates uniformly around all removed sites,
  the signature is about defect presence generally, not singleton
  structure specifically. The singleton hypothesis would still
  stand but the localization claim weakens.
- If signature fails entirely on mixed-defect shapes, the signature
  was an artifact of pure-singleton shapes.

Test shapes
-----------
Shapes are designed with pairs/triples at the cuboid boundary so
that contractibility (chi = 1) is preserved. Interior-pair
removals create tunnels through the cuboid and break chi = 1;
those are excluded. Corner-adjacent pairs are the cleanest way
to introduce a non-singleton defect component while preserving
chi = 1.

M1: (4,3,2) minus {(0,0,0), (0,0,1), (3,0,0), (3,2,1)}.
  Components: 1 vertical corner pair {(0,0,0), (0,0,1)} + 2
  singletons {(3,0,0)}, {(3,2,1)}. Balanced: 2e + 2o.

M2: (4,4,2) minus {(0,0,0), (2,1,0), (2,2,0), (2,3,0)}.
  Components: 1 singleton {(0,0,0)} + 1 triple line on bottom
  face {(2,1,0), (2,2,0), (2,3,0)}. Balanced: 2e + 2o.

M3: (4,4,2) minus {(0,0,0), (0,0,1), (3,0,0), (3,3,0)}.
  Components: 1 vertical corner pair {(0,0,0), (0,0,1)} + 2
  singletons {(3,0,0)}, {(3,3,0)}. Balanced: 2e + 2o.

For each shape compute the localization signature AND the
component-class-resolved distances: what fraction of minority-
biased edges is closer to singleton sites vs closer to non-
singleton sites?

Reports
-------
Per shape:
- avg distance (top-5 min-biased) to nearest singleton
- avg distance (top-5 min-biased) to nearest non-singleton removed site
- avg distance (top-5 maj-biased) to nearest singleton
- avg distance (top-5 maj-biased) to nearest non-singleton

If top-5 min is MORE concentrated around singletons (smaller
distance) than top-5 maj, the signature targets singletons. If
equally concentrated around singletons and non-singletons, it
targets all removed sites uniformly.
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


def edge_midpoint(e_frozen):
    verts = list(e_frozen)
    return np.mean([np.array(v, dtype=float) for v in verts], axis=0)


def edge_min_dist_to_sites(e_frozen, target_sites):
    if not target_sites:
        return float("inf")
    mid = edge_midpoint(e_frozen)
    return float(min(np.linalg.norm(mid - np.array(r, dtype=float)) for r in target_sites))


def analyze_shape(label, bound, removed):
    G = build_graph(bound, removed)
    comps = defect_components(set(removed))
    comp_sizes = sorted(len(c) for c in comps)
    singleton_sites = [s for comp in comps for s in comp if len(comp) == 1]
    nonsingleton_sites = [s for comp in comps for s in comp if len(comp) > 1]

    if not G["balanced"]:
        return {"label": label, "bound": bound, "removed": removed,
                "balanced": False, "comp_sizes": comp_sizes,
                "V": G["V"], "chi": G["chi"]}

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
        dist_all = edge_min_dist_to_sites(e, list(removed))
        dist_single = edge_min_dist_to_sites(e, singleton_sites) if singleton_sites else float("inf")
        dist_nonsingle = edge_min_dist_to_sites(e, nonsingleton_sites) if nonsingleton_sites else float("inf")
        edge_stats.append((e, m, M, frac, dist_all, dist_single, dist_nonsingle))

    edge_stats.sort(key=lambda x: -x[3])
    K = 5
    top_min = edge_stats[:K]
    top_maj = edge_stats[-K:]

    avg_top_min_dist_all = float(np.mean([e[4] for e in top_min]))
    avg_top_maj_dist_all = float(np.mean([e[4] for e in top_maj]))
    avg_top_min_dist_single = float(np.mean([e[5] for e in top_min if np.isfinite(e[5])])) if singleton_sites else float("nan")
    avg_top_maj_dist_single = float(np.mean([e[5] for e in top_maj if np.isfinite(e[5])])) if singleton_sites else float("nan")
    avg_top_min_dist_nonsingle = float(np.mean([e[6] for e in top_min if np.isfinite(e[6])])) if nonsingleton_sites else float("nan")
    avg_top_maj_dist_nonsingle = float(np.mean([e[6] for e in top_maj if np.isfinite(e[6])])) if nonsingleton_sites else float("nan")

    fracs = np.array([e[3] for e in edge_stats])
    dists_all = np.array([e[4] for e in edge_stats])
    if len(fracs) > 1 and fracs.std() > 0 and dists_all.std() > 0:
        corr_all = float(np.corrcoef(fracs, dists_all)[0, 1])
    else:
        corr_all = 0.0

    # Correlation with distance to singletons specifically
    if singleton_sites:
        dists_single = np.array([e[5] for e in edge_stats if np.isfinite(e[5])])
        fracs_single = np.array([e[3] for e in edge_stats if np.isfinite(e[5])])
        if len(dists_single) > 1 and fracs_single.std() > 0 and dists_single.std() > 0:
            corr_single = float(np.corrcoef(fracs_single, dists_single)[0, 1])
        else:
            corr_single = 0.0
    else:
        corr_single = float("nan")

    if nonsingleton_sites:
        dists_nonsingle = np.array([e[6] for e in edge_stats if np.isfinite(e[6])])
        fracs_nonsingle = np.array([e[3] for e in edge_stats if np.isfinite(e[6])])
        if len(dists_nonsingle) > 1 and fracs_nonsingle.std() > 0 and dists_nonsingle.std() > 0:
            corr_nonsingle = float(np.corrcoef(fracs_nonsingle, dists_nonsingle)[0, 1])
        else:
            corr_nonsingle = 0.0
    else:
        corr_nonsingle = float("nan")

    # Signature direction on overall distance
    signature_direction_all = avg_top_min_dist_all < avg_top_maj_dist_all
    signature_correlation_all = corr_all < 0
    signature_holds_all = signature_direction_all and signature_correlation_all

    # Singleton-specific signature
    singleton_signature_direction = (
        avg_top_min_dist_single < avg_top_maj_dist_single
        if singleton_sites else False
    )
    nonsingleton_signature_direction = (
        avg_top_min_dist_nonsingle < avg_top_maj_dist_nonsingle
        if nonsingleton_sites else False
    )

    return {
        "label": label, "bound": bound, "removed": removed,
        "balanced": True, "V": G["V"], "E": G["E"], "F": G["F"],
        "cubes": G["cubes"], "chi": G["chi"], "n_bi": G["n_bi"],
        "comp_sizes": comp_sizes,
        "n_singletons": len(singleton_sites),
        "n_nonsingletons": len(nonsingleton_sites),
        "det_K3": det_K3,
        "n_PM": len(PMs), "n_plus": n_plus, "n_minus": n_minus,
        "was_capped": was_capped,
        "elapsed_enum": elapsed_enum,
        "avg_top_min_dist_all": avg_top_min_dist_all,
        "avg_top_maj_dist_all": avg_top_maj_dist_all,
        "avg_top_min_dist_single": avg_top_min_dist_single,
        "avg_top_maj_dist_single": avg_top_maj_dist_single,
        "avg_top_min_dist_nonsingle": avg_top_min_dist_nonsingle,
        "avg_top_maj_dist_nonsingle": avg_top_maj_dist_nonsingle,
        "corr_all": corr_all, "corr_single": corr_single,
        "corr_nonsingle": corr_nonsingle,
        "signature_holds_all": signature_holds_all,
        "singleton_signature_direction": singleton_signature_direction,
        "nonsingleton_signature_direction": nonsingleton_signature_direction,
    }


# ---------------------------------------------------------------------------
# Shapes
# ---------------------------------------------------------------------------

shapes = [
    # M1: corner vertical pair + 2 corner singletons on (4,3,2)
    ("M1_432_cornerpair_2singleton", (4, 3, 2),
     {(0, 0, 0), (0, 0, 1), (3, 0, 0), (3, 2, 1)}),
    # M2: corner singleton + triple line on face on (4,4,2)
    ("M2_442_1singleton_1triple", (4, 4, 2),
     {(0, 0, 0), (2, 1, 0), (2, 2, 0), (2, 3, 0)}),
    # M3: corner vertical pair + 2 corner singletons on (4,4,2)
    ("M3_442_cornerpair_2singleton", (4, 4, 2),
     {(0, 0, 0), (0, 0, 1), (3, 0, 0), (3, 3, 0)}),
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
        f"shape_{label}_mixed_components_present",
        info["n_singletons"] > 0 and info["n_nonsingletons"] > 0,
        f"{label}: comp_sizes={info['comp_sizes']}, "
        f"n_singletons={info['n_singletons']}, "
        f"n_nonsingletons={info['n_nonsingletons']}. Mixed? "
        f"{info['n_singletons'] > 0 and info['n_nonsingletons'] > 0}.",
    )
    record(
        f"shape_{label}_PM_enumeration_completed",
        not info["was_capped"],
        f"{label}: #PM={info['n_PM']}, elapsed={info['elapsed_enum']:.2f}s.",
    )
    record(
        f"shape_{label}_signed_sum_matches_det",
        abs(info["n_plus"] - info["n_minus"]) == info["det_K3"],
        f"{label}: n_plus={info['n_plus']}, n_minus={info['n_minus']}, "
        f"|sum|={abs(info['n_plus']-info['n_minus'])}, det_K3={info['det_K3']}.",
    )
    record(
        f"shape_{label}_K3_suboptimal_singleton_prediction",
        info["det_K3"] < info["n_PM"],
        f"{label}: K3 det={info['det_K3']}, #PM={info['n_PM']}. K3 suboptimal "
        f"(singleton-hypothesis predicts yes since singletons present)? "
        f"{info['det_K3'] < info['n_PM']}.",
    )
    record(
        f"shape_{label}_non_degenerate",
        info["det_K3"] > 0,
        f"{label}: det_K3={info['det_K3']}. Non-degenerate? {info['det_K3'] > 0}.",
    )
    if info["det_K3"] == 0:
        continue

    # Overall signature
    record(
        f"shape_{label}_overall_signature_holds",
        info["signature_holds_all"],
        f"{label}: avg_min_dist_all={info['avg_top_min_dist_all']:.3f}, "
        f"avg_maj_dist_all={info['avg_top_maj_dist_all']:.3f}, "
        f"corr_all={info['corr_all']:.3f}. Signature? {info['signature_holds_all']}.",
    )

    # Singleton-specific
    record(
        f"shape_{label}_signature_toward_singletons",
        info["singleton_signature_direction"],
        f"{label}: avg_min_dist_singleton={info['avg_top_min_dist_single']:.3f}, "
        f"avg_maj_dist_singleton={info['avg_top_maj_dist_single']:.3f}, "
        f"corr_singleton={info['corr_single']:.3f}. Localizes toward singletons? "
        f"{info['singleton_signature_direction']}.",
    )

    # Non-singleton-specific
    record(
        f"shape_{label}_signature_toward_nonsingletons",
        info["nonsingleton_signature_direction"],
        f"{label}: avg_min_dist_nonsingle={info['avg_top_min_dist_nonsingle']:.3f}, "
        f"avg_maj_dist_nonsingle={info['avg_top_maj_dist_nonsingle']:.3f}, "
        f"corr_nonsingle={info['corr_nonsingle']:.3f}. Localizes toward nonsingletons? "
        f"{info['nonsingleton_signature_direction']}.",
    )

    # Key question: does the signature prefer singletons over non-singletons?
    # If singleton-direction is True AND non-singleton-direction is False,
    # signature targets singletons specifically. If both True, it's defect-generic.
    prefers_singletons = (info["singleton_signature_direction"]
                          and not info["nonsingleton_signature_direction"])
    prefers_neither = (not info["singleton_signature_direction"]
                       and not info["nonsingleton_signature_direction"])
    prefers_both = (info["singleton_signature_direction"]
                    and info["nonsingleton_signature_direction"])
    record(
        f"shape_{label}_signature_class_preference",
        prefers_singletons or prefers_neither or prefers_both,
        f"{label}: prefers_singletons_specifically={prefers_singletons}, "
        f"prefers_both={prefers_both}, prefers_neither={prefers_neither}. "
        f"Singleton-specific signal? {prefers_singletons}.",
    )


# ---------------------------------------------------------------------------
# Cross-shape summary
# ---------------------------------------------------------------------------

non_degenerate = [r for r in results if r.get("balanced") and r.get("det_K3", 0) > 0]

n_signature_holds = sum(1 for r in non_degenerate if r["signature_holds_all"])
n_singleton_preferred = sum(1 for r in non_degenerate
                            if r["singleton_signature_direction"]
                            and not r["nonsingleton_signature_direction"])
n_both_localize = sum(1 for r in non_degenerate
                      if r["singleton_signature_direction"]
                      and r["nonsingleton_signature_direction"])
total = len(non_degenerate)

record(
    "overall_localization_signature_on_mixed_defects",
    n_signature_holds == total and total > 0,
    f"Overall signature (min_dist_all < maj_dist_all AND corr < 0) holds on "
    f"{n_signature_holds}/{total} mixed-defect shapes.",
)
record(
    "signature_targets_singletons_specifically",
    n_singleton_preferred == total and total > 0,
    f"Signature targets singletons SPECIFICALLY (singleton-direction but "
    f"NOT nonsingleton-direction) on {n_singleton_preferred}/{total} shapes.",
)
record(
    "signature_targets_all_removed_uniformly",
    n_both_localize == total and total > 0,
    f"Signature targets ALL removed sites (both singleton- and nonsingleton-"
    f"direction hold) on {n_both_localize}/{total} shapes.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_singleton_preferred == total and total > 0:
    document(
        "localization_signature_singleton_specific",
        f"On all {total} tested mixed-defect shapes (with both singletons"
        f" and non-singleton components), the edge-level localization"
        f" signature concentrates SPECIFICALLY around singletons, not"
        f" around non-singleton components. Top-5 minority-biased edges"
        f" are closer to singleton sites than top-5 majority-biased,"
        f" but minority-biased edges are NOT closer to non-singleton"
        f" sites. This is a strong refinement: the K3 sign obstruction"
        f" is structurally tied to singleton defect components, not to"
        f" removed sites generically. Corroborates the singleton"
        f" hypothesis with a finer structural signal.",
    )
elif n_both_localize == total and total > 0:
    document(
        "localization_signature_defect_generic",
        f"On all {total} tested mixed-defect shapes, the signature"
        f" localizes around ALL removed sites uniformly (both singleton"
        f" and non-singleton components). The signature is about defect"
        f" proximity generally, not singleton structure specifically."
        f" Still consistent with the singleton hypothesis (which is"
        f" about optimality, not localization of specific edges).",
    )
elif n_signature_holds >= total // 2 and total > 0:
    document(
        "localization_signature_mixed_pattern",
        f"Signature exhibits heterogeneous behavior across mixed-defect"
        f" shapes ({n_signature_holds}/{total} overall; "
        f"{n_singleton_preferred} singleton-specific, "
        f"{n_both_localize} defect-generic). Signature is real but its"
        f" preference between singleton and non-singleton components"
        f" depends on shape specifics.",
    )
else:
    document(
        "localization_signature_fails_on_mixed_defects",
        f"Signature fails on most mixed-defect shapes"
        f" ({n_signature_holds}/{total}). The iter 21-22 and iter 26"
        f" results relied on homogeneous (all-singleton) defect sets."
        f" Mixed-defect interactions break the signature.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: mixed-defect localization signature test")
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
