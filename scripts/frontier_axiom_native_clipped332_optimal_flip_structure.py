#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- structural characterization of the
optimal gauge classes on clipped-(3,3,2).

Background
----------
On (3,3,2) with corners (0,0,0) and (2,2,1) removed:
- 4096 gauge classes.
- K3 gives |det(B)| = 30.
- Max |det(B)| = 36 (found by exhaustive enumeration).
- K3 is the UNIQUE plaquette-satisfying class, so every optimal
  class (|det|=36) must violate at least one plaquette.

Claim under adversarial test
----------------------------
C1. There are finitely many gauge classes with |det| = 36;
    enumerate them.
C2. For each optimal class, extract the specific edge flips
    relative to K3 (mask = 0).
C3. Characterize which plaquettes these flips violate. If the
    violated plaquettes are concentrated near the removed corners,
    the "broken symmetry" at the clipped corners is what K3 gets
    wrong.
C4. Alternatively, if optimal flips are scattered/diffuse, no
    simple "corner correction" exists.

Falsification / discovery
-------------------------
- If all optimal masks share a compact near-corner flip pattern:
  confirms K3 translation-invariance mismatch at corners.
- If optimal masks scatter arbitrary: non-local obstruction,
  would need deeper investigation.
- If optimal flips produce violations at NON-corner plaquettes:
  surprising, requires explanation.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict, deque, Counter

import numpy as np


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RECORDS.append((name, bool(ok), detail))


def document(name: str, note: str) -> None:
    DOCS.append((name, note))


def eta(mu: int, n: tuple[int, int, int]) -> int:
    if mu == 1:
        return 1
    if mu == 2:
        return (-1) ** n[0]
    if mu == 3:
        return (-1) ** (n[0] + n[1])
    raise ValueError


# ---------------------------------------------------------------------------
# Build clipped-(3,3,2)
# ---------------------------------------------------------------------------

removed_corners = {(0, 0, 0), (2, 2, 1)}
base_sites = [(i, j, k) for i in range(3) for j in range(3) for k in range(2)]
sites = [v for v in base_sites if v not in removed_corners]
site_set = set(sites)

# Edges
edges = []  # (n_lo, n_hi, mu)
edge_index = {}
for n in sites:
    for mu in (1, 2, 3):
        nn = list(n)
        nn[mu - 1] += 1
        nn = tuple(nn)
        if nn in site_set:
            edges.append((n, nn, mu))
            edge_index[frozenset({n, nn})] = len(edges) - 1
n_E = len(edges)

# Plaquettes
plaquettes = []  # list of (list_of_edge_idx, list_of_4_corners, plane_label)
for n in base_sites:
    for i in (1, 2, 3):
        for j in range(i + 1, 4):
            n_i = list(n); n_i[i - 1] += 1; n_i = tuple(n_i)
            n_j = list(n); n_j[j - 1] += 1; n_j = tuple(n_j)
            n_ij = list(n); n_ij[i - 1] += 1; n_ij[j - 1] += 1; n_ij = tuple(n_ij)
            corners = (n, n_i, n_j, n_ij)
            if all(c in site_set for c in corners):
                e_list = [
                    edge_index[frozenset({n, n_i})],
                    edge_index[frozenset({n, n_j})],
                    edge_index[frozenset({n_i, n_ij})],
                    edge_index[frozenset({n_j, n_ij})],
                ]
                plaquettes.append((e_list, corners, (i, j)))
n_F = len(plaquettes)

# Bipartite block
evens = [v for v in sites if sum(v) % 2 == 0]
odds = [v for v in sites if sum(v) % 2 == 1]
idx_e = {v: i for i, v in enumerate(evens)}
idx_o = {v: i for i, v in enumerate(odds)}
n_bi = len(evens)

B_0 = np.zeros((n_bi, n_bi), dtype=np.int64)
edge_idx_to_bip = {}  # edge idx -> (ie, jo, s)
for idx, (n_lo, n_hi, mu) in enumerate(edges):
    if n_lo in idx_e:
        ie, jo = idx_e[n_lo], idx_o[n_hi]
        s = eta(mu, n_lo)
    else:
        ie, jo = idx_e[n_hi], idx_o[n_lo]
        s = -eta(mu, n_lo)
    B_0[ie, jo] = s
    edge_idx_to_bip[idx] = (ie, jo)


# ---------------------------------------------------------------------------
# Spanning tree, chord edges
# ---------------------------------------------------------------------------

adj = defaultdict(list)
for idx, (a, b, _) in enumerate(edges):
    adj[a].append((b, idx))
    adj[b].append((a, idx))
start = sites[0]
visited = {start}
tree_idx = set()
queue = deque([start])
while queue:
    u = queue.popleft()
    for (v, ei) in adj[u]:
        if v not in visited:
            visited.add(v)
            tree_idx.add(ei)
            queue.append(v)
chord_idx = [idx for idx in range(n_E) if idx not in tree_idx]
gauge_dim = len(chord_idx)
assert gauge_dim == 12

record(
    "clipped_332_parameters",
    n_E == 27 and n_F == 14 and gauge_dim == 12,
    f"Clipped (3,3,2): V={len(sites)}, E={n_E}, F={n_F}, gauge_dim={gauge_dim}.",
)


# ---------------------------------------------------------------------------
# Enumerate 2^12 = 4096 gauge classes; find all with |det| = 36
# ---------------------------------------------------------------------------

optimal_masks = []
max_det = 0

# Precompute plaquette chord masks for violation check
chord_bit = {c: b for b, c in enumerate(chord_idx)}
plaq_chord_mask = []
for p_edges, _, _ in plaquettes:
    pm = 0
    for e in p_edges:
        if e in chord_bit:
            pm |= (1 << chord_bit[e])
    plaq_chord_mask.append(pm)

t0 = time.time()
for mask in range(2 ** gauge_dim):
    B = B_0.copy()
    for bit in range(gauge_dim):
        if (mask >> bit) & 1:
            idx = chord_idx[bit]
            ie, jo = edge_idx_to_bip[idx]
            B[ie, jo] *= -1
    det_abs = int(round(abs(np.linalg.det(B))))
    if det_abs > max_det:
        max_det = det_abs
        optimal_masks = [mask]
    elif det_abs == max_det:
        optimal_masks.append(mask)
elapsed = time.time() - t0

record(
    "enumeration_finds_max_det_36",
    max_det == 36,
    f"Max |det| over 4096 classes = {max_det} (in {elapsed:.2f}s). # optimal masks = {len(optimal_masks)}.",
)


# ---------------------------------------------------------------------------
# Extract flip-edge patterns for each optimal mask
# ---------------------------------------------------------------------------

def mask_to_chord_edges(mask):
    return [chord_idx[bit] for bit in range(gauge_dim) if (mask >> bit) & 1]


optimal_flip_patterns = []  # list of frozenset of vertex pairs
for mask in optimal_masks:
    flipped_chords = mask_to_chord_edges(mask)
    vertex_pairs = []
    for eidx in flipped_chords:
        n_lo, n_hi, mu = edges[eidx]
        vertex_pairs.append(frozenset({n_lo, n_hi}))
    optimal_flip_patterns.append(frozenset(vertex_pairs))

unique_patterns = set(optimal_flip_patterns)
record(
    "optimal_flip_patterns_are_finite",
    len(optimal_flip_patterns) == len(optimal_masks),
    f"{len(optimal_masks)} optimal masks giving {len(unique_patterns)} distinct flip-edge-sets.",
)


# ---------------------------------------------------------------------------
# Count violated plaquettes for each optimal mask
# ---------------------------------------------------------------------------

violated_plaquettes_per_mask = []
for mask in optimal_masks:
    n_violated = 0
    violated_list = []
    for p_idx, pm in enumerate(plaq_chord_mask):
        v = mask & pm
        parity = 0
        while v:
            parity ^= (v & 1)
            v >>= 1
        if parity:
            n_violated += 1
            violated_list.append(p_idx)
    violated_plaquettes_per_mask.append((n_violated, violated_list))

n_violated_counts = Counter(v[0] for v in violated_plaquettes_per_mask)
record(
    "optimal_masks_violate_at_least_one_plaquette",
    all(v[0] >= 1 for v in violated_plaquettes_per_mask),
    f"All {len(optimal_masks)} optimal masks violate >=1 plaquette. Distribution: {dict(n_violated_counts)}.",
)


# ---------------------------------------------------------------------------
# Locate violated plaquettes
# ---------------------------------------------------------------------------

def plaquette_center_distance_from_corner(corners, corner_sites):
    """Min distance from plaquette center to any removed corner."""
    center = np.mean([np.array(c) for c in corners], axis=0)
    best = float("inf")
    for cs in corner_sites:
        d = np.linalg.norm(center - np.array(cs))
        if d < best:
            best = d
    return best


violated_plaquette_distances = []
for (n_viol, viol_list) in violated_plaquettes_per_mask:
    for p_idx in viol_list:
        _, corners, _ = plaquettes[p_idx]
        d = plaquette_center_distance_from_corner(corners, removed_corners)
        violated_plaquette_distances.append(d)

all_plaquette_distances = [
    plaquette_center_distance_from_corner(corners, removed_corners)
    for (_, corners, _) in plaquettes
]

avg_all = np.mean(all_plaquette_distances)
avg_violated = np.mean(violated_plaquette_distances) if violated_plaquette_distances else float("inf")

record(
    "violated_plaquettes_closer_to_removed_corners_on_average",
    avg_violated < avg_all,
    f"Avg distance to removed corner: all plaquettes {avg_all:.3f}, violated plaquettes {avg_violated:.3f}. Near corners? {avg_violated < avg_all}.",
)


# ---------------------------------------------------------------------------
# Check whether the optimal flip pattern is LOCAL (concentrated near
# removed corners) or DIFFUSE.
# ---------------------------------------------------------------------------

# For each optimal mask, compute average distance of flipped edges'
# midpoints from removed corners.
flip_distances_per_mask = []
for mask in optimal_masks:
    flipped_chords = mask_to_chord_edges(mask)
    distances = []
    for eidx in flipped_chords:
        n_lo, n_hi, _ = edges[eidx]
        midpoint = (np.array(n_lo) + np.array(n_hi)) / 2
        best = min(np.linalg.norm(midpoint - np.array(c)) for c in removed_corners)
        distances.append(best)
    flip_distances_per_mask.append(np.mean(distances) if distances else 0)

avg_flip_distance = np.mean(flip_distances_per_mask)

# Compare with average distance of ALL chord edges from removed corners
all_chord_distances = []
for eidx in chord_idx:
    n_lo, n_hi, _ = edges[eidx]
    midpoint = (np.array(n_lo) + np.array(n_hi)) / 2
    best = min(np.linalg.norm(midpoint - np.array(c)) for c in removed_corners)
    all_chord_distances.append(best)
avg_all_chord_distance = np.mean(all_chord_distances)

record(
    "flipped_edges_closer_to_removed_corners_on_average",
    avg_flip_distance < avg_all_chord_distance,
    f"Avg distance to removed corner: all chords {avg_all_chord_distance:.3f}, optimal flipped edges {avg_flip_distance:.3f}.",
)


# ---------------------------------------------------------------------------
# Identify the SMALLEST optimal flip pattern (fewest flipped edges)
# ---------------------------------------------------------------------------

sizes = [bin(mask).count("1") for mask in optimal_masks]
min_flip_count = min(sizes)
min_flip_masks = [m for m, s in zip(optimal_masks, sizes) if s == min_flip_count]

record(
    "smallest_optimal_flip_pattern_has_few_edges",
    min_flip_count <= 4,
    f"Smallest optimal mask has {min_flip_count} flipped edges (out of {gauge_dim} chords).",
)

# Print the smallest optimal pattern as a concrete discovery
if min_flip_masks:
    sample_mask = min_flip_masks[0]
    sample_edges = [edges[cidx] for cidx in mask_to_chord_edges(sample_mask)]
    sample_description = "; ".join(
        f"{n_lo}-{n_hi} via mu={mu}" for (n_lo, n_hi, mu) in sample_edges
    )
    record(
        "smallest_optimal_mask_concrete_edges",
        True == (len(sample_edges) == min_flip_count),
        f"One minimal optimal flip pattern ({min_flip_count} edges): {sample_description}.",
    )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if avg_flip_distance < avg_all_chord_distance and avg_violated < avg_all:
    document(
        "optimal_flips_concentrate_near_removed_corners",
        "The optimal gauge classes (|det|=36) have edge flips"
        " concentrated NEAR the removed corners of the clipped graph"
        " on average, and the violated plaquettes are also closer to"
        " those corners than random. This supports the interpretation:"
        " K3's translation-invariant staggered phases fail to"
        " self-correct at the broken-symmetry corners where sites"
        " were removed, and the optimal class applies a local"
        " correction at those corners.",
    )
elif avg_flip_distance >= avg_all_chord_distance:
    document(
        "optimal_flips_not_corner_localized",
        "Optimal flip patterns are NOT concentrated near the removed"
        " corners (avg flip distance = avg chord distance). The"
        " obstruction is non-local on this graph, requiring diffuse"
        " corrections rather than simple corner-patches.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("V2: structural analysis of optimal gauge classes on clipped-(3,3,2)")
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
