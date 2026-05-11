#!/usr/bin/env python3
"""Narrow runner for `SU3_WIGNER_BLOCK4_STAGING_BLOCK5_ORIENTATION_DIAGNOSTICS_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the geometry-only Block 5 orientation-diagnostics core (claims 6-7
of the narrow theorem note). This is the cleanable-core narrow split of the
combined Block 4/5 note's `audit-conditional scope narrowing 2026-05-10`
section — the bridge-gap inequality limb (which imports unaudited open-gate
numerics) is NOT in scope here.

Specifically, this runner verifies on the L_s = 2 PBC cube:

  Claim (6) — all-forward `+d1+d2+d1+d2` plaquette enumeration:
    - 12 unique unordered plaquettes,
    - 24 unique directed links,
    - each directed link in exactly 2 plaquettes,
    - index identification graph: 48 nodes, 48 edges, 8 connected components.

  Claim (7) — standard Wilson `+d1+d2-d1-d2` plaquette traversal:
    - 12 unique unordered plaquettes,
    - 20 unique directed links (NOT 24),
    - link multiplicities `{1: 4, 2: 8, 3: 4, 4: 4}`,
    - 24 forward leg occurrences and 24 backward leg occurrences.

This runner does NOT compute, import, or compare any Perron value, bridge-
support target, witness threshold, or P-value gap. It does NOT import any
constants from
`scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py`,
`scripts/frontier_su3_wigner_l2_cube_orientation_verification.py`, or
any other framework module. The geometry checks here are independent of
those open-gate numerics.

Forbidden imports: numpy + Python stdlib only. No scipy.special needed.

Run:
    python3 scripts/frontier_su3_wigner_block5_orientation_diagnostics_narrow.py
"""

from __future__ import annotations

import sys
from collections import Counter
from typing import Dict, List, Tuple


L = 2  # spatial extent of the PBC cube under test


# ============================================================================
# Section A. Plaquette enumerations (geometry only, no open-gate imports).
# ============================================================================

def all_forward_plaquettes() -> List[Tuple]:
    """All-forward enumeration: traversal +d1 +d2 +d1 +d2 on L=2 PBC.

    Each plaquette traversal closes after 4 forward steps via PBC wrap.
    Returns the list of unique unordered plaquettes (deduplicated by
    underlying directed-link set).
    """
    plaquettes: List[Tuple] = []
    for plane_dir1, plane_dir2 in [(0, 1), (0, 2), (1, 2)]:
        orth = ({0, 1, 2} - {plane_dir1, plane_dir2}).pop()
        for orth_val in range(L):
            for start_in_plane_idx in range(L):
                site = [0, 0, 0]
                site[plane_dir1] = start_in_plane_idx
                site[plane_dir2] = 0
                site[orth] = orth_val
                cur = list(site)
                links = []
                for direction in [plane_dir1, plane_dir2,
                                  plane_dir1, plane_dir2]:
                    links.append(((cur[0], cur[1], cur[2], direction), +1))
                    cur[direction] = (cur[direction] + 1) % L
                plaquettes.append((tuple(site), plane_dir1, plane_dir2,
                                   links))
    seen = set()
    unique: List[Tuple] = []
    for p in plaquettes:
        link_set = frozenset(link for (link, _) in p[3])
        if link_set not in seen:
            seen.add(link_set)
            unique.append(p)
    return unique


def standard_wilson_plaquettes() -> List[Tuple]:
    """Standard Wilson enumeration: traversal +d1 +d2 -d1 -d2 on L=2 PBC."""
    plaquettes: List[Tuple] = []
    for plane_dir1, plane_dir2 in [(0, 1), (0, 2), (1, 2)]:
        orth = ({0, 1, 2} - {plane_dir1, plane_dir2}).pop()
        for orth_val in range(L):
            for start_in_plane_idx in range(L):
                site = [0, 0, 0]
                site[plane_dir1] = start_in_plane_idx
                site[plane_dir2] = 0
                site[orth] = orth_val
                site_p_d1 = list(site)
                site_p_d1[plane_dir1] = (site_p_d1[plane_dir1] + 1) % L
                site_p_d2 = list(site)
                site_p_d2[plane_dir2] = (site_p_d2[plane_dir2] + 1) % L
                links = [
                    ((site[0], site[1], site[2], plane_dir1), +1),
                    ((site_p_d1[0], site_p_d1[1], site_p_d1[2],
                      plane_dir2), +1),
                    ((site_p_d2[0], site_p_d2[1], site_p_d2[2],
                      plane_dir1), -1),
                    ((site[0], site[1], site[2], plane_dir2), -1),
                ]
                plaquettes.append((tuple(site), plane_dir1, plane_dir2,
                                   links))
    seen = set()
    unique: List[Tuple] = []
    for p in plaquettes:
        link_set = frozenset(link for (link, _) in p[3])
        if link_set not in seen:
            seen.add(link_set)
            unique.append(p)
    return unique


def link_to_plaquette_slots_signed(plaquettes: List[Tuple]) -> Dict:
    out: Dict = {}
    for p_idx, (_, _, _, links) in enumerate(plaquettes):
        for slot, (link, sign) in enumerate(links):
            out.setdefault(link, []).append((p_idx, slot, sign))
    return out


# ============================================================================
# Section B. Index identification graph (used only for claim 6).
# ============================================================================

def signed_indices_for_slot(p_idx: int, slot: int, sign: int
                            ) -> Tuple[int, int]:
    """Return (row, col) global indices in the plaquette cycle:
       sign=+1 (forward leg): row=alpha_(slot), col=alpha_(slot+1)
       sign=-1 (backward leg, matrix is U^T): row=alpha_(slot+1), col=alpha_(slot)
    """
    base = 4 * p_idx
    pos_in = slot
    pos_out = (slot + 1) % 4
    if sign == +1:
        return (base + pos_in, base + pos_out)
    return (base + pos_out, base + pos_in)


def build_index_graph(plaquettes: List[Tuple]
                      ) -> Tuple[int, List[Tuple[int, int]]]:
    n_nodes = 4 * len(plaquettes)
    edges: List[Tuple[int, int]] = []
    link_dict = link_to_plaquette_slots_signed(plaquettes)
    for link, occurrences in link_dict.items():
        if len(occurrences) != 2:
            raise RuntimeError(
                f"Link {link} appears {len(occurrences)} times "
                f"(expected 2); cannot build index graph."
            )
        (p_a, slot_a, sign_a), (p_b, slot_b, sign_b) = occurrences
        row_a, col_a = signed_indices_for_slot(p_a, slot_a, sign_a)
        row_b, col_b = signed_indices_for_slot(p_b, slot_b, sign_b)
        edges.append((row_a, row_b))
        edges.append((col_a, col_b))
    return n_nodes, edges


def count_connected_components(n_nodes: int,
                               edges: List[Tuple[int, int]]) -> int:
    parent = list(range(n_nodes))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in edges:
        union(a, b)
    return len({find(i) for i in range(n_nodes)})


# ============================================================================
# Section C. Driver — geometry-only PASS/FAIL bookkeeping.
# ============================================================================

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


def main() -> int:
    print("=" * 78)
    print("SU(3) Wigner Block 5 Orientation Diagnostics — narrow runner")
    print("(geometry-only; no open-gate numerics imported)")
    print("=" * 78)

    # ===== Claim 6: all-forward L_s=2 PBC enumeration =====
    section("Claim (6): all-forward +d1+d2+d1+d2 plaquette enumeration")
    p_af = all_forward_plaquettes()
    check("12 unique unordered plaquettes",
          len(p_af) == 12,
          detail=f"got {len(p_af)}")
    link_dict_af = link_to_plaquette_slots_signed(p_af)
    check("24 unique directed links",
          len(link_dict_af) == 24,
          detail=f"got {len(link_dict_af)}")
    leg_counts_af = [len(occs) for occs in link_dict_af.values()]
    check("each directed link in exactly 2 plaquettes",
          all(n == 2 for n in leg_counts_af),
          detail=f"observed multiplicities = {sorted(set(leg_counts_af))}")
    n_nodes_af, edges_af = build_index_graph(p_af)
    n_comp_af = count_connected_components(n_nodes_af, edges_af)
    check("index graph: 48 nodes",
          n_nodes_af == 48,
          detail=f"got {n_nodes_af}")
    check("index graph: 48 edges",
          len(edges_af) == 48,
          detail=f"got {len(edges_af)}")
    check("index graph: 8 connected components",
          n_comp_af == 8,
          detail=f"got {n_comp_af}")

    # ===== Claim 7: standard Wilson L_s=2 PBC orientation diagnostics =====
    section("Claim (7): standard Wilson +d1+d2-d1-d2 plaquette traversal")
    p_w = standard_wilson_plaquettes()
    check("12 unique unordered plaquettes",
          len(p_w) == 12,
          detail=f"got {len(p_w)}")
    link_dict_w = link_to_plaquette_slots_signed(p_w)
    check("20 unique directed links (NOT 24)",
          len(link_dict_w) == 20,
          detail=f"got {len(link_dict_w)}")
    leg_counts_w = [len(occs) for occs in link_dict_w.values()]
    mult_count = Counter(leg_counts_w)
    expected_mults = {1: 4, 2: 8, 3: 4, 4: 4}
    check("link multiplicities = {1: 4, 2: 8, 3: 4, 4: 4}",
          dict(mult_count) == expected_mults,
          detail=f"got {dict(sorted(mult_count.items()))}")
    forward_w = sum(1 for occs in link_dict_w.values()
                    for (_, _, s) in occs if s == +1)
    backward_w = sum(1 for occs in link_dict_w.values()
                     for (_, _, s) in occs if s == -1)
    check("24 forward leg occurrences",
          forward_w == 24,
          detail=f"got {forward_w}")
    check("24 backward leg occurrences",
          backward_w == 24,
          detail=f"got {backward_w}")

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
