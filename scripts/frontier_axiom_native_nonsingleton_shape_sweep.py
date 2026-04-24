#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- map non-singleton shape types by whether
they preserve the singleton-specific localization signal (iter 27).

Context
-------
Iter 27 showed that in mixed-defect shapes, the edge-level
localization signature targets singletons SPECIFICALLY: minority-
biased edges concentrate around singleton defect components AND
anti-concentrate around non-singleton components (opposite
correlation signs). However, iter 27's M2 shape (singleton +
triple line) showed the signature drowning overall. Open question:
which non-singleton component shapes preserve the singleton-
specific signal vs drown it?

Test sweep
----------
For each shape, the defect contains:
- at least one singleton component, AND
- at least one non-singleton component of a specified type.

Non-singleton types tested:
- pair (2 adjacent sites)
- L-triple (3 sites in L-shape on face)
- line-3 (3 sites in a row, y-direction)
- line-4 (4 sites in a row)
- 2x2 square (4 sites in face)
- 2 pairs (two separate 2-site components)

All shapes use corner/edge/boundary placement to preserve
contractibility (chi = 1). Shapes that fail chi = 1 are reported
as such and excluded from the signal analysis (since singleton
hypothesis is conditional on contractibility).

Predictions
-----------
If "non-singleton components act as absorbers" (iter 27
interpretation), larger non-singleton components should absorb
MORE signal and be more likely to drown the singleton-specific
signature. Smaller components (pairs) preserve it.

If the prediction holds: shape types by size should map to
signature strength, with pairs preserving signal and 2x2
squares / line-4 drowning it.

If prediction fails: need a different structural story.

Report: for each shape, overall signature (holds/fails), and
signature-preference (singleton-specific, defect-generic,
neither). Cross-tab by non-singleton component type.
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


def enumerate_PMs(n_bi, B_un, cap=2_000_000, time_cap_s=90.0):
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


def analyze_shape(label, bound, removed, nonsingleton_type):
    G = build_graph(bound, removed)
    comps = defect_components(set(removed))
    comp_sizes = sorted(len(c) for c in comps)
    singleton_sites = [s for comp in comps for s in comp if len(comp) == 1]
    nonsingleton_sites = [s for comp in comps for s in comp if len(comp) > 1]
    has_mixed = (len(singleton_sites) > 0) and (len(nonsingleton_sites) > 0)

    base_info = {
        "label": label, "bound": bound, "removed": removed,
        "nonsingleton_type": nonsingleton_type,
        "comp_sizes": comp_sizes,
        "n_singletons": len(singleton_sites),
        "n_nonsingletons": len(nonsingleton_sites),
        "has_mixed": has_mixed,
    }

    if not G["balanced"]:
        return {**base_info, "balanced": False, "V": G["V"], "chi": G["chi"]}

    base_info.update({
        "balanced": True, "V": G["V"], "E": G["E"], "F": G["F"],
        "cubes": G["cubes"], "chi": G["chi"], "n_bi": G["n_bi"],
    })

    if G["chi"] != 1:
        return {**base_info, "contractible": False}

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

    if singleton_sites:
        avg_top_min_dist_single = float(np.mean([e[5] for e in top_min]))
        avg_top_maj_dist_single = float(np.mean([e[5] for e in top_maj]))
    else:
        avg_top_min_dist_single = float("nan")
        avg_top_maj_dist_single = float("nan")

    if nonsingleton_sites:
        avg_top_min_dist_nonsingle = float(np.mean([e[6] for e in top_min]))
        avg_top_maj_dist_nonsingle = float(np.mean([e[6] for e in top_maj]))
    else:
        avg_top_min_dist_nonsingle = float("nan")
        avg_top_maj_dist_nonsingle = float("nan")

    fracs = np.array([e[3] for e in edge_stats])
    dists_single = np.array([e[5] for e in edge_stats])
    dists_nonsingle = np.array([e[6] for e in edge_stats])

    if len(fracs) > 1 and fracs.std() > 0:
        if dists_single.std() > 0:
            corr_single = float(np.corrcoef(fracs, dists_single)[0, 1])
        else:
            corr_single = 0.0
        if dists_nonsingle.std() > 0:
            corr_nonsingle = float(np.corrcoef(fracs, dists_nonsingle)[0, 1])
        else:
            corr_nonsingle = 0.0
    else:
        corr_single = 0.0
        corr_nonsingle = 0.0

    singleton_direction = (
        avg_top_min_dist_single < avg_top_maj_dist_single
        if singleton_sites else False
    )
    nonsingle_direction = (
        avg_top_min_dist_nonsingle < avg_top_maj_dist_nonsingle
        if nonsingleton_sites else False
    )
    prefers_singletons = singleton_direction and not nonsingle_direction
    signal_survives = singleton_direction and corr_single < 0

    return {
        **base_info,
        "contractible": True,
        "det_K3": det_K3,
        "n_PM": len(PMs), "n_plus": n_plus, "n_minus": n_minus,
        "was_capped": was_capped,
        "elapsed_enum": elapsed_enum,
        "avg_top_min_dist_single": avg_top_min_dist_single,
        "avg_top_maj_dist_single": avg_top_maj_dist_single,
        "avg_top_min_dist_nonsingle": avg_top_min_dist_nonsingle,
        "avg_top_maj_dist_nonsingle": avg_top_maj_dist_nonsingle,
        "corr_single": corr_single,
        "corr_nonsingle": corr_nonsingle,
        "singleton_direction": singleton_direction,
        "nonsingle_direction": nonsingle_direction,
        "prefers_singletons": prefers_singletons,
        "signal_survives": signal_survives,
    }


# ---------------------------------------------------------------------------
# Sweep shapes
# ---------------------------------------------------------------------------

shapes = [
    # SH1: pair + 2 singletons on (4,4,2). Pair at corner (not
    # iter 27 shape -- different singletons).
    ("SH1_pair_plus_2singleton", (4, 4, 2),
     {(0, 0, 0), (0, 0, 1), (3, 2, 0), (2, 3, 1)},
     "pair"),
    # SH2: L-triple on x=0 face + singleton.
    ("SH2_L_triple_plus_1singleton", (4, 4, 2),
     {(0, 0, 0), (0, 0, 1), (0, 1, 1), (3, 0, 0)},
     "L_triple"),
    # SH3: line-3 on y-direction on an edge + singleton (different from iter 27 M2).
    ("SH3_line3_yx0z0_plus_1singleton", (4, 4, 2),
     {(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 3, 1)},
     "line3_horizontal"),
    # SH4: line-4 (full y-edge at x=0, z=0) + 2 singletons.
    ("SH4_line4_plus_2singleton", (4, 4, 2),
     {(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 3, 0), (3, 0, 0), (3, 2, 1)},
     "line4"),
    # SH5: 2x2 face-square (on x=0 face) + 2 singletons.
    ("SH5_2x2square_plus_2singleton", (4, 4, 2),
     {(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (3, 0, 0), (3, 3, 0)},
     "2x2_square"),
    # SH6: 2 corner pairs + 2 singletons (mixed multi-pair defect).
    ("SH6_2pairs_plus_2singleton", (4, 4, 2),
     {(0, 0, 0), (0, 0, 1), (3, 3, 0), (3, 3, 1), (3, 0, 0), (0, 3, 1)},
     "two_pairs"),
]

results = []
for (label, bound, removed, ns_type) in shapes:
    info = analyze_shape(label, bound, removed, ns_type)
    results.append(info)


# ---------------------------------------------------------------------------
# Per-shape records
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    record(
        f"shape_{label}_has_mixed_components",
        info["has_mixed"],
        f"{label}: comp_sizes={info['comp_sizes']}, "
        f"n_singletons={info['n_singletons']}, "
        f"n_nonsingletons={info['n_nonsingletons']}. Mixed? {info['has_mixed']}.",
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
        info["contractible"],
        f"{label}: chi={info['chi']}. Contractible? {info['contractible']}.",
    )
    if not info["contractible"]:
        continue
    record(
        f"shape_{label}_K3_suboptimal_as_predicted",
        info["det_K3"] < info["n_PM"],
        f"{label}: K3 det={info['det_K3']}, #PM={info['n_PM']}. "
        f"K3 suboptimal (singletons present)? {info['det_K3'] < info['n_PM']}.",
    )
    record(
        f"shape_{label}_non_degenerate",
        info["det_K3"] > 0,
        f"{label}: det={info['det_K3']}. Non-degenerate? {info['det_K3'] > 0}.",
    )
    if info["det_K3"] == 0:
        continue
    record(
        f"shape_{label}_singleton_direction",
        info["singleton_direction"],
        f"{label}: avg_min_dist_singleton={info['avg_top_min_dist_single']:.3f}, "
        f"avg_maj_dist_singleton={info['avg_top_maj_dist_single']:.3f}. "
        f"Toward singletons? {info['singleton_direction']}.",
    )
    record(
        f"shape_{label}_singleton_correlation_negative",
        info["corr_single"] < 0,
        f"{label}: corr(frac, dist-to-singleton)={info['corr_single']:.3f}. "
        f"Negative (localizes)? {info['corr_single'] < 0}.",
    )
    record(
        f"shape_{label}_nonsingleton_direction",
        info["nonsingle_direction"],
        f"{label}: avg_min_dist_nonsingle={info['avg_top_min_dist_nonsingle']:.3f}, "
        f"avg_maj_dist_nonsingle={info['avg_top_maj_dist_nonsingle']:.3f}. "
        f"Toward nonsingletons? {info['nonsingle_direction']}.",
    )
    record(
        f"shape_{label}_singleton_specific",
        info["prefers_singletons"],
        f"{label}: prefers_singletons_specifically={info['prefers_singletons']}. "
        f"(toward singletons=True AND toward nonsingletons=False)",
    )
    record(
        f"shape_{label}_signal_survives",
        info["signal_survives"],
        f"{label}: singleton-direction AND corr-single negative? "
        f"{info['signal_survives']}.",
    )


# ---------------------------------------------------------------------------
# Cross-shape summary
# ---------------------------------------------------------------------------

valid_results = [r for r in results if r.get("balanced") and r.get("contractible")
                 and r.get("has_mixed") and r.get("det_K3", 0) > 0]
n_signal_survives = sum(1 for r in valid_results if r["signal_survives"])
n_singleton_specific = sum(1 for r in valid_results if r["prefers_singletons"])
n_total = len(valid_results)

record(
    "signal_survives_on_valid_shapes",
    n_total > 0 and n_signal_survives > 0,
    f"Signal survives on {n_signal_survives}/{n_total} valid (balanced + "
    f"contractible + mixed + non-degenerate) shapes. Any survivals? "
    f"{n_signal_survives > 0}.",
)
record(
    "signal_is_singleton_specific_on_majority",
    n_total > 0 and n_singleton_specific >= (n_total + 1) // 2,
    f"Signal is singleton-specific (prefers singletons over nonsingletons) "
    f"on {n_singleton_specific}/{n_total} valid shapes. Majority? "
    f"{n_singleton_specific >= (n_total + 1) // 2}.",
)

# Breakdown by non-singleton type
type_breakdown = defaultdict(lambda: {"total": 0, "survives": 0, "specific": 0})
for r in valid_results:
    t = r["nonsingleton_type"]
    type_breakdown[t]["total"] += 1
    if r["signal_survives"]:
        type_breakdown[t]["survives"] += 1
    if r["prefers_singletons"]:
        type_breakdown[t]["specific"] += 1

for t, counts in sorted(type_breakdown.items()):
    record(
        f"breakdown_{t}_has_at_least_one_valid_shape",
        counts["total"] > 0,
        f"{t}: {counts['survives']}/{counts['total']} signal survives, "
        f"{counts['specific']}/{counts['total']} singleton-specific.",
    )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_total > 0 and n_signal_survives == n_total and n_singleton_specific == n_total:
    document(
        "singleton_specific_signal_universal",
        f"On all {n_total} tested mixed-defect shapes (with various"
        f" non-singleton component types: pair, L-triple, line-3, line-4,"
        f" 2x2 square, 2 pairs), the edge-level localization signature"
        f" is specifically singleton-targeted: minority-biased edges"
        f" concentrate around singletons AND anti-concentrate around"
        f" non-singleton components. The iter 27 sharpening that"
        f" 'non-singleton components act as absorbers' holds across"
        f" all non-singleton shape types tested.",
    )
elif n_total > 0 and n_signal_survives >= (n_total + 1) // 2:
    document(
        "singleton_specific_signal_mostly_holds",
        f"Signal survives on {n_signal_survives}/{n_total} valid shapes,"
        f" is singleton-specific on {n_singleton_specific}/{n_total}."
        f" Non-singleton component type affects preservation; some"
        f" shape classes drown the signal. See breakdown records for"
        f" which non-singleton types preserve the signal.",
    )
else:
    document(
        "singleton_specific_signal_breaks",
        f"Signal survives on only {n_signal_survives}/{n_total} valid"
        f" shapes. The iter 27 signature is fragile beyond simple pair"
        f" non-singletons.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: non-singleton shape sweep for singleton-specific signal")
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
