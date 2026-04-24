#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- search for the SH3-type PM-pairing
bijection that forces det_K3 = 0.

Context
-------
Iter 33 confirmed that on (4,4,2), all 128 line-3 + singleton
det=0 cases are NEITHER partial-reflection nor central-sigma
explained. These are SH3-type non-automorphism zero-det cases
(73% of all det=0 cases across 5 L3=2 cuboids). iter 30's H5
empirically characterizes them on (4,4,2) but without a
structural proof.

Goal
----
On SH3 = (4,4,2) \ {(1,0,0), (2,0,0), (3,0,0), (0,3,1)}:
- 1490 PMs, n_plus = n_minus = 745 exactly.
- No non-identity graph automorphism fixes the defect.
- Yet det_K3 = 0, so there must be SOME bijection phi on PMs
  with K3_sign(phi(M)) = -K3_sign(M).

Search strategies
-----------------
(A) Plaquette-4-cycle swap: for each PM M, check if there
exists a plaquette-face 4-cycle (2 M-edges + 2 non-M-edges on
a graph-2x2-face) whose swap flips K3 sign. Requires computing
plaquette swap sign factors.

(B) Longer alternating cycle swaps (length 6): for each PM M,
examine alternating cycles of length 6 involving the singleton
neighborhood.

(C) Statistical test: compute PM features (edge counts by
direction, edges near singleton, etc.) and check if plus/minus
PMs have identical feature distributions, implying a "local"
bijection.

For this iter: (A) + (C). If (A) shows plaquette swaps don't
flip K3 sign (as expected by K3 plaquette universality and
permutation accounting), move to (C).

Output
------
- Enumerate 1490 PMs.
- Classify by K3 sign.
- For each PM, count valid plaquette-4-cycle swaps; apply one;
  check resulting M' sign.
- Compute distributions of simple PM features (vertical edge
  count, edges incident to singleton-neighbors, etc.) for
  plus vs minus.
- Report any structural asymmetry.
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


def build_B(bound, removed):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    sites = [v for v in base if v not in removed]
    site_set = set(sites)
    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
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
    return B, B_un, evens, odds, idx_e, idx_o, n_bi, site_set


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
            stopped[0] = True; return
        if (time.time() - start) > time_cap_s:
            stopped[0] = True; return
        if i == n_bi:
            PMs.append(tuple(perm)); return
        for j in adj[i]:
            if not used[j]:
                perm[i] = j
                used[j] = True
                dfs(i + 1)
                if stopped[0]: return
                used[j] = False

    dfs(0)
    return PMs, stopped[0]


def pm_contrib(p, B, n_bi):
    s = sign_of_permutation(p)
    prod = 1
    for i in range(n_bi):
        prod *= int(B[i, p[i]])
    return s * prod


def pm_edges(p, evens, odds, n_bi):
    return [frozenset({evens[i], odds[p[i]]}) for i in range(n_bi)]


def edge_direction(e):
    a, b = tuple(e)
    for l in range(3):
        if a[l] != b[l]:
            return l + 1
    return None


# ---------------------------------------------------------------------------
# Build SH3 graph
# ---------------------------------------------------------------------------

SH3_bound = (4, 4, 2)
SH3_removed = {(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 3, 1)}

B, B_un, evens, odds, idx_e, idx_o, n_bi, site_set = build_B(SH3_bound, SH3_removed)

t0 = time.time()
PMs, capped = enumerate_PMs(n_bi, B_un)
t_enum = time.time() - t0

record(
    "sh3_pm_enumeration_1490",
    len(PMs) == 1490,
    f"SH3: enumerated {len(PMs)} PMs in {t_enum:.2f}s. Expected 1490? "
    f"{len(PMs) == 1490}.",
)

plus_PMs = []
minus_PMs = []
for p in PMs:
    c = pm_contrib(p, B, n_bi)
    if c > 0:
        plus_PMs.append(p)
    elif c < 0:
        minus_PMs.append(p)

record(
    "sh3_equal_split_745",
    len(plus_PMs) == 745 and len(minus_PMs) == 745,
    f"SH3: n_plus = {len(plus_PMs)}, n_minus = {len(minus_PMs)}. "
    f"Both 745? {len(plus_PMs) == 745 and len(minus_PMs) == 745}.",
)


# ---------------------------------------------------------------------------
# Strategy A: plaquette-4-cycle swap sign analysis
# ---------------------------------------------------------------------------

# Find all plaquettes in SH3 graph
plaquettes = []  # list of (A, B, C, D) tuples where A-B-D-C is the plaquette cycle
L1, L2, L3 = SH3_bound
base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
for n in base:
    for i in (1, 2, 3):
        for j in range(i + 1, 4):
            n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
            n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
            n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
            if all(c in site_set for c in (n, n_i, n_j, n_ij)):
                plaquettes.append((n, n_i, n_j, n_ij))

record(
    "sh3_plaquette_count",
    len(plaquettes) > 0,
    f"SH3 plaquettes: {len(plaquettes)}.",
)


# For each PM, count valid plaquette swaps and test one
def plaquette_swappable_for_PM(pm_edge_set, plaq):
    """Check if PM uses exactly 2 opposite edges of this plaquette."""
    A, B, C, D = plaq  # A, B, C, D with B = A+e_i, C = A+e_j, D = A+e_i+e_j
    edges = [
        frozenset({A, B}),
        frozenset({A, C}),
        frozenset({B, D}),
        frozenset({C, D}),
    ]
    in_pm = [e in pm_edge_set for e in edges]
    # Two opposite edges: {AB, CD} or {AC, BD}
    if in_pm[0] and in_pm[3] and not in_pm[1] and not in_pm[2]:
        return "AB_CD"
    if in_pm[1] and in_pm[2] and not in_pm[0] and not in_pm[3]:
        return "AC_BD"
    return None


def apply_plaquette_swap(pm_edge_set, plaq, mode):
    A, B, C, D = plaq
    edges_in = [frozenset({A, B}), frozenset({C, D})] if mode == "AB_CD" else [frozenset({A, C}), frozenset({B, D})]
    edges_out = [frozenset({A, C}), frozenset({B, D})] if mode == "AB_CD" else [frozenset({A, B}), frozenset({C, D})]
    new_set = set(pm_edge_set) - set(edges_in) | set(edges_out)
    return frozenset(new_set)


def pm_as_perm(pm_edge_set, evens, odds, idx_e, idx_o, n_bi):
    """Convert PM (set of edges) back to perm array."""
    perm = [-1] * n_bi
    for e in pm_edge_set:
        a, b = tuple(e)
        if a in idx_e:
            perm[idx_e[a]] = idx_o[b]
        else:
            perm[idx_e[b]] = idx_o[a]
    return tuple(perm)


# Test plaquette swap sign on a sample of PMs
plaquette_swap_flips = 0
plaquette_swap_preserves = 0
plaquette_swap_sample_size = min(50, len(plus_PMs))

for p_idx in range(plaquette_swap_sample_size):
    p = plus_PMs[p_idx]
    edges_of_p = frozenset(pm_edges(p, evens, odds, n_bi))
    # Find first swappable plaquette
    for plaq in plaquettes:
        mode = plaquette_swappable_for_PM(edges_of_p, plaq)
        if mode is None:
            continue
        new_edges = apply_plaquette_swap(edges_of_p, plaq, mode)
        new_perm = pm_as_perm(new_edges, evens, odds, idx_e, idx_o, n_bi)
        if -1 in new_perm:
            continue  # invalid
        new_contrib = pm_contrib(new_perm, B, n_bi)
        orig_contrib = pm_contrib(p, B, n_bi)
        if new_contrib * orig_contrib < 0:
            plaquette_swap_flips += 1
        else:
            plaquette_swap_preserves += 1
        break  # test only first found swap

record(
    "plaquette_4cycle_swap_preserves_sign",
    plaquette_swap_flips == 0 and plaquette_swap_preserves > 0,
    f"On {plaquette_swap_sample_size} sampled PMs: plaquette-4-cycle "
    f"swaps flip K3 sign {plaquette_swap_flips}, preserve sign "
    f"{plaquette_swap_preserves}. All preserve? "
    f"{plaquette_swap_flips == 0 and plaquette_swap_preserves > 0}.",
)


# ---------------------------------------------------------------------------
# Strategy C: feature distributions
# ---------------------------------------------------------------------------

def count_edges_by_direction(p, evens, odds, n_bi):
    counts = {1: 0, 2: 0, 3: 0}
    for i in range(n_bi):
        e = frozenset({evens[i], odds[p[i]]})
        mu = edge_direction(e)
        if mu:
            counts[mu] += 1
    return counts


def count_edges_incident_to_sites(p, evens, odds, n_bi, target_sites):
    count = 0
    target_set = set(target_sites)
    for i in range(n_bi):
        if evens[i] in target_set or odds[p[i]] in target_set:
            count += 1
    return count


# Singleton neighborhood
singleton = (0, 3, 1)
singleton_neighbors = set()
for mu in (1, 2, 3):
    for d in (-1, 1):
        v = list(singleton); v[mu - 1] += d; v = tuple(v)
        if v in site_set:
            singleton_neighbors.add(v)

# Line-3 neighborhood
line_sites = {(1, 0, 0), (2, 0, 0), (3, 0, 0)}
line_neighbors = set()
for n in line_sites:
    for mu in (1, 2, 3):
        for d in (-1, 1):
            v = list(n); v[mu - 1] += d; v = tuple(v)
            if v in site_set:
                line_neighbors.add(v)


# Compute feature histograms
plus_features = defaultdict(lambda: defaultdict(int))
minus_features = defaultdict(lambda: defaultdict(int))

for p in plus_PMs:
    dir_counts = count_edges_by_direction(p, evens, odds, n_bi)
    sn_edges = count_edges_incident_to_sites(p, evens, odds, n_bi, singleton_neighbors)
    ln_edges = count_edges_incident_to_sites(p, evens, odds, n_bi, line_neighbors)
    plus_features["dir_1"][dir_counts[1]] += 1
    plus_features["dir_2"][dir_counts[2]] += 1
    plus_features["dir_3"][dir_counts[3]] += 1
    plus_features["singleton_neighbor_edges"][sn_edges] += 1
    plus_features["line_neighbor_edges"][ln_edges] += 1

for p in minus_PMs:
    dir_counts = count_edges_by_direction(p, evens, odds, n_bi)
    sn_edges = count_edges_incident_to_sites(p, evens, odds, n_bi, singleton_neighbors)
    ln_edges = count_edges_incident_to_sites(p, evens, odds, n_bi, line_neighbors)
    minus_features["dir_1"][dir_counts[1]] += 1
    minus_features["dir_2"][dir_counts[2]] += 1
    minus_features["dir_3"][dir_counts[3]] += 1
    minus_features["singleton_neighbor_edges"][sn_edges] += 1
    minus_features["line_neighbor_edges"][ln_edges] += 1


for feat_name in ["dir_1", "dir_2", "dir_3", "singleton_neighbor_edges",
                  "line_neighbor_edges"]:
    plus_dist = dict(plus_features[feat_name])
    minus_dist = dict(minus_features[feat_name])
    all_keys = set(plus_dist.keys()) | set(minus_dist.keys())
    identical = all(plus_dist.get(k, 0) == minus_dist.get(k, 0) for k in all_keys)
    record(
        f"feature_{feat_name}_distribution_symmetric",
        identical,
        f"{feat_name}: plus={sorted(plus_dist.items())}, "
        f"minus={sorted(minus_dist.items())}. Symmetric? {identical}.",
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

all_features_symmetric = all(
    all(plus_features[f].get(k, 0) == minus_features[f].get(k, 0)
        for k in (set(plus_features[f].keys()) | set(minus_features[f].keys())))
    for f in ["dir_1", "dir_2", "dir_3", "singleton_neighbor_edges", "line_neighbor_edges"]
)

record(
    "sh3_all_tested_features_symmetric",
    all_features_symmetric,
    f"All 5 tested PM features have plus/minus distributions that match. "
    f"Symmetric overall? {all_features_symmetric}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if all_features_symmetric and plaquette_swap_flips == 0:
    document(
        "sh3_bijection_is_local_but_not_plaquette",
        "On SH3, all tested PM features (direction counts, edges"
        " incident to singleton neighbors, edges incident to"
        " line-3 neighbors) have IDENTICAL distributions between"
        " plus-PMs (745) and minus-PMs (745). This indicates the"
        " PM-pairing bijection that forces det=0 exists and is"
        " LOCAL (preserves these aggregate features) but is NOT"
        " the plaquette-4-cycle swap (which preserves K3 sign"
        " rather than flipping it). The bijection likely involves"
        " a more subtle alternating-cycle structure that flips"
        " sign while keeping direction counts balanced. This is"
        " a candidate direction for future proof work: find a"
        " specific alternating-6-cycle or alternating-path"
        " through the singleton/line-3 neighborhoods whose swap"
        " flips K3 sign.",
    )
elif not all_features_symmetric:
    document(
        "sh3_bijection_structure_asymmetric",
        "Some PM features distribute asymmetrically between plus"
        " and minus, suggesting the bijection is NOT a symmetric"
        " local swap. The asymmetric features pinpoint where the"
        " K3 obstruction concentrates.",
    )
else:
    document(
        "sh3_investigation_incomplete",
        "Feature analysis inconclusive; further structural"
        " investigation needed.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: SH3 PM-pairing bijection search")
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
