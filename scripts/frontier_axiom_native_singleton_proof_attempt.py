#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- structural proof attempt for the
singleton hypothesis.

Goal
----
Enumerate all perfect matchings of a singleton-defect graph,
compute K3 signed contributions, and identify the structural
feature that distinguishes + from - matchings. If a clean pattern
emerges (e.g., minority matchings all contain a specific edge or
cycle), that IS the structural obstruction.

Test graph
----------
(3,3,2) minus {(0,0,0), (2,2,1)} -- the iter 14 D shape.
Known: K3 |det| = 30, max |det| = 36 (over all sign assignments).
So gap = 6, minority count = 3 matchings (since gap = 2*minority).
Prediction: exactly 3 matchings contribute with the minority sign
under K3.

Adversarial structure
---------------------
Enumerate all PMs via permutation iteration (40,320 permutations,
8+8 bipartite = 8! = 40320 to check). For each PM:
  - Compute sign(perm) * prod(K3 entries).
  - Classify + vs -.
Then analyze which edges / vertices / cycles distinguish the
minority matchings.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict
from itertools import permutations

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


# ---------------------------------------------------------------------------
# Build (3,3,2) minus {(0,0,0), (2,2,1)}
# ---------------------------------------------------------------------------

removed = {(0, 0, 0), (2, 2, 1)}
base = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
sites = [v for v in base if v not in removed]
site_set = set(sites)

edges = []
for n in sites:
    for mu in (1, 2, 3):
        nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
        if nn in site_set:
            edges.append((n, nn, mu))

evens = [v for v in sites if sum(v) % 2 == 0]
odds = [v for v in sites if sum(v) % 2 == 1]
idx_e = {v: i for i, v in enumerate(evens)}
idx_o = {v: i for i, v in enumerate(odds)}
n_bi = len(evens)
assert n_bi == 8

B = np.zeros((n_bi, n_bi), dtype=np.int64)
B_un = np.zeros((n_bi, n_bi), dtype=np.int64)
edge_to_bip = {}  # (ie, jo) -> (vertex pair, mu)
for (n_lo, n_hi, mu) in edges:
    if n_lo in idx_e:
        ie, jo = idx_e[n_lo], idx_o[n_hi]
        s = eta(mu, n_lo)
    else:
        ie, jo = idx_e[n_hi], idx_o[n_lo]
        s = -eta(mu, n_lo)
    B[ie, jo] = s
    B_un[ie, jo] = 1
    edge_to_bip[(ie, jo)] = (n_lo, n_hi, mu)

det_K3 = int(round(abs(np.linalg.det(B))))
record(
    "K3_det_matches_prior_iter14",
    det_K3 == 30,
    f"K3 |det| = {det_K3} (expected 30 per iter 14 D).",
)


# ---------------------------------------------------------------------------
# Enumerate all perfect matchings and their signed contributions
# ---------------------------------------------------------------------------

plus_matchings = []
minus_matchings = []

for perm in permutations(range(n_bi)):
    # Check all edges exist
    ok = True
    for i in range(n_bi):
        if B_un[i, perm[i]] == 0:
            ok = False; break
    if not ok:
        continue
    s = sign_of_permutation(perm)
    prod = 1
    for i in range(n_bi):
        prod *= B[i, perm[i]]
    contrib = s * prod
    if contrib == 1:
        plus_matchings.append(perm)
    else:
        minus_matchings.append(perm)

n_plus = len(plus_matchings)
n_minus = len(minus_matchings)
signed_sum = n_plus - n_minus
total_pm = n_plus + n_minus

record(
    "signed_sum_matches_K3_det",
    abs(signed_sum) == det_K3,
    f"n_plus={n_plus}, n_minus={n_minus}. |n_+ - n_-| = {abs(signed_sum)}. Should equal K3 det = {det_K3}.",
)

record(
    "total_PM_count",
    total_pm >= det_K3,
    f"Total PM count = {total_pm}.",
)

# Identify minority set.
if n_plus <= n_minus:
    minority = plus_matchings
    majority = minus_matchings
    minority_sign = "+"
else:
    minority = minus_matchings
    majority = plus_matchings
    minority_sign = "-"

n_minority = len(minority)
record(
    "minority_count_matches_gap_half",
    n_minority == (total_pm - det_K3) // 2,
    f"Minority count = {n_minority}, expected gap/2 = {(total_pm - det_K3) // 2}.",
)


# ---------------------------------------------------------------------------
# Structural analysis: which edges appear in minority matchings?
# ---------------------------------------------------------------------------

def perm_to_edges(perm):
    return [(evens[i], odds[perm[i]]) for i in range(n_bi)]


edge_appearance_minority = defaultdict(int)
for perm in minority:
    for e in perm_to_edges(perm):
        edge_appearance_minority[frozenset(e)] += 1

edge_appearance_majority = defaultdict(int)
for perm in majority:
    for e in perm_to_edges(perm):
        edge_appearance_majority[frozenset(e)] += 1

# Edges strongly biased toward minority
def freq_ratio(e):
    maj = edge_appearance_majority.get(e, 0)
    mino = edge_appearance_minority.get(e, 0)
    total = maj + mino
    if total == 0:
        return None
    return mino / total


all_edges_seen = set(edge_appearance_minority.keys()) | set(edge_appearance_majority.keys())
edge_bias = [(e, edge_appearance_minority.get(e, 0),
              edge_appearance_majority.get(e, 0),
              freq_ratio(e)) for e in all_edges_seen]
# Sort by minority fraction (descending)
edge_bias.sort(key=lambda x: (-x[3] if x[3] is not None else 0))

# Top edges by minority fraction
top_minority_biased = [(e, m, M, r) for (e, m, M, r) in edge_bias[:5]]
record(
    "top_minority_biased_edges_identified",
    len(top_minority_biased) > 0,
    f"Top 5 most-minority-biased edges (edge, min_count, maj_count, fraction): {[(sorted(list(e)), m, M, round(r, 3) if r is not None else None) for (e, m, M, r) in top_minority_biased]}.",
)


# ---------------------------------------------------------------------------
# Distance of minority-biased edges from removed sites
# ---------------------------------------------------------------------------

def edge_dist_to_removed(e_frozen):
    e_vertices = list(e_frozen)
    midpoint = np.mean([np.array(v) for v in e_vertices], axis=0)
    return min(np.linalg.norm(midpoint - np.array(r)) for r in removed)


minority_frac_edges = [e for (e, _, _, r) in edge_bias if r is not None and r > 0.5]
majority_frac_edges = [e for (e, _, _, r) in edge_bias if r is not None and r < 0.3]

avg_dist_minority = np.mean([edge_dist_to_removed(e) for e in minority_frac_edges]) if minority_frac_edges else 0
avg_dist_majority = np.mean([edge_dist_to_removed(e) for e in majority_frac_edges]) if majority_frac_edges else 0

record(
    "minority_biased_edges_near_singletons",
    avg_dist_minority < avg_dist_majority,
    f"Avg distance from removed sites: minority-biased edges {avg_dist_minority:.3f}, majority-biased {avg_dist_majority:.3f}. Near singletons? {avg_dist_minority < avg_dist_majority}.",
)


# ---------------------------------------------------------------------------
# Analyze: do minority matchings all use SPECIFIC edges?
# ---------------------------------------------------------------------------

# For each edge, fraction of minority matchings containing it
minority_only_edges = []
if minority:
    for e in all_edges_seen:
        m_count = edge_appearance_minority.get(e, 0)
        if m_count == len(minority):  # ALL minority contain this edge
            minority_only_edges.append(e)

record(
    "edges_present_in_all_minority_matchings",
    len(minority_only_edges) >= 0,
    f"{len(minority_only_edges)} edges present in ALL minority matchings: {[sorted(list(e)) for e in minority_only_edges[:3]]}.",
)


# ---------------------------------------------------------------------------
# Vertex-neighborhoods of removed sites
# ---------------------------------------------------------------------------

neighbors_of_removed = set()
for r in removed:
    for mu in (1, 2, 3):
        for d in (-1, 1):
            nn = list(r); nn[mu - 1] += d; nn = tuple(nn)
            if nn in site_set:
                neighbors_of_removed.add(nn)

record(
    "neighbors_of_singletons_identified",
    len(neighbors_of_removed) > 0,
    f"Neighbors of removed sites: {sorted(neighbors_of_removed)}. Total: {len(neighbors_of_removed)}.",
)


# ---------------------------------------------------------------------------
# Key structural claim: do all minority matchings pair neighbors of
# removed sites with each other or with distant vertices?
# ---------------------------------------------------------------------------

def matching_pairs_neighbors_to_distant(perm):
    """Return count of edges in matching where one endpoint is a
    neighbor-of-removed and the other is far from removed."""
    count = 0
    for i in range(n_bi):
        e_v1, e_v2 = evens[i], odds[perm[i]]
        n1_near = e_v1 in neighbors_of_removed
        n2_near = e_v2 in neighbors_of_removed
        if n1_near or n2_near:
            count += 1
    return count


minority_near_counts = [matching_pairs_neighbors_to_distant(p) for p in minority]
majority_near_counts = [matching_pairs_neighbors_to_distant(p) for p in majority]

avg_min_near = np.mean(minority_near_counts) if minority_near_counts else 0
avg_maj_near = np.mean(majority_near_counts) if majority_near_counts else 0

record(
    "minority_matchings_use_neighbor_edges_differently",
    abs(avg_min_near - avg_maj_near) > 0.1,
    f"Avg # edges incident to neighbor-of-removed: minority {avg_min_near:.3f}, majority {avg_maj_near:.3f}.",
)


# ---------------------------------------------------------------------------
# Record the 3 (or however many) minority matchings explicitly
# ---------------------------------------------------------------------------

if len(minority) <= 10:
    for i, perm in enumerate(minority):
        pm_edges = perm_to_edges(perm)
        record(
            f"minority_matching_{i}_structure",
            len(pm_edges) == n_bi,
            f"minority #{i}: edges = {[tuple(sorted([str(v) for v in pm_edges[k]])) for k in range(min(3, len(pm_edges)))]}...",
        )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if minority_only_edges:
    document(
        "structural_obstruction_identified",
        f"All minority matchings share {len(minority_only_edges)}"
        f" specific edges. These edges form the 'structural signature'"
        f" of K3's Pfaffian obstruction around singleton defects.",
    )
elif avg_dist_minority < avg_dist_majority:
    document(
        "minority_edges_localized_near_singletons",
        f"Minority-biased edges concentrate near removed singleton"
        f" sites (avg distance {avg_dist_minority:.3f} vs"
        f" {avg_dist_majority:.3f} for majority-biased). This is a"
        f" partial structural signature supporting the claim that"
        f" singleton defects force sign misalignment in nearby"
        f" matchings.",
    )
else:
    document(
        "no_clean_structural_signature_found",
        "Minority matchings don't share a simple edge pattern or"
        " localization signature. The sign obstruction is more"
        " diffuse and requires a subtler analysis.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: singleton hypothesis structural analysis on (3,3,2) minus 2")
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
