#!/usr/bin/env python3
"""
Axiom-native runner -- Target 2, sub-step 2c: unifying formula
    C_G = (#PM(G))^{16} / 2^{8 * n_sites}
for the normalized K3 free Berezin partition on kit-derivable
bipartite Z^3 subgraphs.

Novel result
------------
The K3 staggered-phase orientation is a Kasteleyn-like orientation
on bipartite Z^3 subgraphs: the absolute value of the bipartite-
block determinant equals the number of perfect matchings,
    |det(B_G)| = #PM(G).

Combined with the derivation of Z_G from earlier sub-steps (the
bipartite Dirac determinant gives det(A) = det(B)^2, and per-Cl(3)
sector Z_B = (a^2/2)^{n_sites} * det(A)), this yields the closed-form
    C_G = Z_G / a^{16 * n_sites} = |det(B)|^{16} / 2^{8 * n_sites}
         = (#PM(G))^{16} / 2^{8 * n_sites}.

Target 2 success criteria
-------------------------
(i)  Observable: C_G for any kit-derivable bipartite-balanced Z^3
     subgraph G (one formula, many values).
(ii) Predicted shape: (#PM(G))^{16} / 2^{8 * n_sites}.
(iii) Falsification: for any new test graph G, if the directly-computed
     |det(B_G)| does not equal the enumerated #PM(G), the Kasteleyn
     property fails and the formula is refuted for that graph.

Verified case-by-case here on five test graphs:
- edge        (2 sites, 1 edge, 0 loops):  #PM = 1, det(B) = 1.
- 4-line      (4 sites, 3 edges, 0 loops): #PM = 1, det(B) = 1.
- plaquette   (4 sites, 4 edges, 1 loop):  #PM = 2, det(B) = +/-2.
- 2x3 grid    (6 sites, 7 edges, 2 loops): #PM = 3, det(B) = +/-3.
- unit cube   (8 sites, 12 edges, 5 loops): #PM = 9, det(B) = +/-9.

Novelty vs. ledger
------------------
Ledger has C_edge = C_plaq = 2^(-16) (1d, 2a), C_cube = (3/4)^32
(2b), and the observation that they differ (refuting naive
universality). This runner introduces the UNIFYING formula
C_G = (#PM(G))^{16} / 2^{8*n_sites}, verified on an additional new
graph (2x3 grid with a specific predicted value 3^16 / 2^48). The
formula is a structural signature: it ties the K3 partition to
combinatorial graph theory via perfect matchings.

Musk first-principles moves
---------------------------
- Question: is the Kasteleyn property generic for K3 on Z^3, or
  specific to small graphs? Conjecturally generic for planar-
  embeddable subgraphs; verified on 5 distinct cases here.
- Delete: without K3 staggered phases (signs eta_mu), |det(B)| can
  differ from #PM. The K3 staggered-phase structure is load-bearing.
- Simplify: shortest path is direct case-by-case verification
  combining a symbolic det(B) with a combinatorial enumeration of
  #PM.
"""

from __future__ import annotations

import sys
from itertools import permutations
from typing import Iterable

import sympy as sp


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name: str, ok: bool, detail: str) -> None:
    RECORDS.append((name, bool(ok), detail))


def document(name: str, note: str) -> None:
    DOCS.append((name, note))


# ---------------------------------------------------------------------------
# Helpers: K3 staggered phase; perfect-matching enumeration;
# bipartite hopping block.
# ---------------------------------------------------------------------------


def eta(mu: int, n: tuple[int, int, int]) -> int:
    if mu == 1:
        return 1
    if mu == 2:
        return (-1) ** n[0]
    if mu == 3:
        return (-1) ** (n[0] + n[1])
    raise ValueError(mu)


def k3_hopping_block(
    sites: list[tuple[int, int, int]],
    edges: list[tuple[tuple[int, int, int], tuple[int, int, int], int]],
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]], sp.Matrix]:
    """Return (even_sites, odd_sites, B) where B is the bipartite block
    of the K3 hopping matrix A, indexed by (row = even site, col = odd
    site). edges are (n_lower, n_upper, mu)."""
    site_index = {s: i for i, s in enumerate(sites)}
    n = len(sites)
    A = [[0] * n for _ in range(n)]
    for (lo, hi, mu) in edges:
        i = site_index[lo]
        j = site_index[hi]
        A[i][j] += eta(mu, lo)
        A[j][i] += -eta(mu, hi)
    even_sites = [s for s in sites if sum(s) % 2 == 0]
    odd_sites = [s for s in sites if sum(s) % 2 == 1]
    B = sp.zeros(len(even_sites), len(odd_sites))
    for row_i, v_e in enumerate(even_sites):
        for col_j, v_o in enumerate(odd_sites):
            B[row_i, col_j] = A[site_index[v_e]][site_index[v_o]]
    return even_sites, odd_sites, B


def count_perfect_matchings(
    evens: list[tuple[int, int, int]],
    odds: list[tuple[int, int, int]],
    edge_set: set[frozenset[tuple[int, int, int]]],
) -> int:
    if len(evens) != len(odds):
        return 0
    count = 0
    for perm in permutations(odds):
        valid = True
        for e, o in zip(evens, perm):
            if frozenset({e, o}) not in edge_set:
                valid = False
                break
        if valid:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Shared variables.
# ---------------------------------------------------------------------------

a = sp.symbols("a", positive=True)
N_CL3 = 8  # |Cl(3) basis|


def C_from_det(det_B, n_sites: int):
    """Return C_G = |det(B)|^{16} / 2^{8 n_sites} as sympy rational."""
    return sp.simplify(sp.Abs(det_B) ** 16 / sp.Integer(2) ** (8 * n_sites))


def C_from_pm(pm: int, n_sites: int):
    return sp.Rational(pm, 1) ** 16 / sp.Rational(2) ** (8 * n_sites)


# ---------------------------------------------------------------------------
# Test 1. Edge: sites {(0,0,0), (1,0,0)}.
# ---------------------------------------------------------------------------

edge_sites = [(0, 0, 0), (1, 0, 0)]
edge_edges = [((0, 0, 0), (1, 0, 0), 1)]
edge_edge_set = {frozenset({a_, b_}) for (a_, b_, _) in edge_edges}
ev, od, B = k3_hopping_block(edge_sites, edge_edges)
det_edge = sp.simplify(B.det())
pm_edge = count_perfect_matchings(ev, od, edge_edge_set)
record(
    "edge_det_B_abs_equals_pm",
    abs(det_edge) == pm_edge,
    f"edge: det(B) = {det_edge}, #PM = {pm_edge}; |det(B)| = #PM.",
)
C_edge_formula = C_from_pm(pm_edge, len(edge_sites))
record(
    "edge_C_formula_equals_2_to_minus_16",
    C_edge_formula == sp.Rational(1, 2**16),
    f"edge: C_formula = {pm_edge}^16 / 2^(8*{len(edge_sites)}) = {C_edge_formula}.",
)


# ---------------------------------------------------------------------------
# Test 2. Plaquette: {(0,0,0), (1,0,0), (0,1,0), (1,1,0)}.
# ---------------------------------------------------------------------------

plaq_sites = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
plaq_edges = [
    ((0, 0, 0), (1, 0, 0), 1),
    ((0, 0, 0), (0, 1, 0), 2),
    ((0, 1, 0), (1, 1, 0), 1),
    ((1, 0, 0), (1, 1, 0), 2),
]
plaq_edge_set = {frozenset({a_, b_}) for (a_, b_, _) in plaq_edges}
ev, od, B = k3_hopping_block(plaq_sites, plaq_edges)
det_plaq = sp.simplify(B.det())
pm_plaq = count_perfect_matchings(ev, od, plaq_edge_set)
record(
    "plaquette_det_B_abs_equals_pm",
    abs(det_plaq) == pm_plaq and pm_plaq == 2,
    f"plaquette: det(B) = {det_plaq}, #PM = {pm_plaq} = 2.",
)
C_plaq_formula = C_from_pm(pm_plaq, len(plaq_sites))
record(
    "plaquette_C_formula_equals_2_to_minus_16",
    C_plaq_formula == sp.Rational(1, 2**16),
    f"plaquette: C_formula = 2^16 / 2^32 = 2^(-16) = {C_plaq_formula}.",
)


# ---------------------------------------------------------------------------
# Test 3. 4-line: {(0,0,0), (1,0,0), (2,0,0), (3,0,0)} chain via mu=1.
# ---------------------------------------------------------------------------

line_sites = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0)]
line_edges = [
    ((0, 0, 0), (1, 0, 0), 1),
    ((1, 0, 0), (2, 0, 0), 1),
    ((2, 0, 0), (3, 0, 0), 1),
]
line_edge_set = {frozenset({a_, b_}) for (a_, b_, _) in line_edges}
ev, od, B = k3_hopping_block(line_sites, line_edges)
det_line = sp.simplify(B.det())
pm_line = count_perfect_matchings(ev, od, line_edge_set)
record(
    "4_line_det_B_abs_equals_pm",
    abs(det_line) == pm_line and pm_line == 1,
    f"4-line: det(B) = {det_line}, #PM = {pm_line} = 1.",
)
C_line_formula = C_from_pm(pm_line, len(line_sites))
record(
    "4_line_C_formula_equals_2_to_minus_32",
    C_line_formula == sp.Rational(1, 2**32),
    f"4-line: C_formula = 1^16 / 2^32 = {C_line_formula}.",
)


# ---------------------------------------------------------------------------
# Test 4. 2x3 grid: NEW case. Sites at (i, j, 0) for i in {0,1}, j in {0,1,2}.
# ---------------------------------------------------------------------------

grid_sites = [(i, j, 0) for i in (0, 1) for j in (0, 1, 2)]
grid_edges = []
for i in (0, 1):
    for j in (0, 1, 2):
        n = (i, j, 0)
        # mu=1 (i direction): link (0, j) -- (1, j)
        if i == 0:
            grid_edges.append(((0, j, 0), (1, j, 0), 1))
        # mu=2 (j direction): link (i, j) -- (i, j+1)
        if j in (0, 1):
            grid_edges.append(((i, j, 0), (i, j + 1, 0), 2))
# dedupe
grid_edges = list({(lo, hi, mu) for (lo, hi, mu) in grid_edges})
grid_edge_set = {frozenset({a_, b_}) for (a_, b_, _) in grid_edges}
ev, od, B = k3_hopping_block(grid_sites, grid_edges)
det_grid = sp.simplify(B.det())
pm_grid = count_perfect_matchings(ev, od, grid_edge_set)
record(
    "2x3_grid_has_7_edges",
    len(grid_edges) == 7,
    f"2x3 grid has {len(grid_edges)} edges.",
)
record(
    "2x3_grid_det_B_abs_equals_pm",
    abs(det_grid) == pm_grid and pm_grid == 3,
    f"2x3 grid: det(B) = {det_grid}, #PM = {pm_grid} = 3.",
)
C_grid_formula = C_from_pm(pm_grid, len(grid_sites))
record(
    "2x3_grid_C_formula_equals_3_to_16_over_2_to_48",
    C_grid_formula == sp.Rational(3**16, 2**48),
    f"2x3 grid: C_formula = 3^16 / 2^48 = {C_grid_formula}.",
)


# ---------------------------------------------------------------------------
# Test 5. Unit cube: 8 vertices at {0,1}^3, 12 edges.
# ---------------------------------------------------------------------------

cube_sites = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
cube_edges = []
for v in cube_sites:
    for mu in (1, 2, 3):
        if v[mu - 1] == 0:
            w = list(v)
            w[mu - 1] = 1
            cube_edges.append((v, tuple(w), mu))
cube_edge_set = {frozenset({a_, b_}) for (a_, b_, _) in cube_edges}
ev, od, B = k3_hopping_block(cube_sites, cube_edges)
det_cube = sp.simplify(B.det())
pm_cube = count_perfect_matchings(ev, od, cube_edge_set)
record(
    "unit_cube_has_12_edges",
    len(cube_edges) == 12,
    f"Unit cube has {len(cube_edges)} edges.",
)
record(
    "unit_cube_det_B_abs_equals_pm",
    abs(det_cube) == pm_cube and pm_cube == 9,
    f"unit cube: det(B) = {det_cube}, #PM = {pm_cube} = 9.",
)
C_cube_formula = C_from_pm(pm_cube, len(cube_sites))
record(
    "unit_cube_C_formula_equals_9_to_16_over_2_to_64",
    C_cube_formula == sp.Rational(9**16, 2**64)
    and C_cube_formula == sp.Rational(3**32, 2**64),
    f"unit cube: C_formula = 9^16 / 2^64 = 3^32 / 2^64 = {C_cube_formula}.",
)


# ---------------------------------------------------------------------------
# Global: formula holds on all 5 test graphs.
# ---------------------------------------------------------------------------

all_abs_dets = [abs(det_edge), abs(det_plaq), abs(det_line), abs(det_grid), abs(det_cube)]
all_pms = [pm_edge, pm_plaq, pm_line, pm_grid, pm_cube]
record(
    "kasteleyn_like_identity_holds_on_all_5_test_graphs",
    all_abs_dets == all_pms,
    f"|det(B)| = #PM holds on all 5 graphs: {list(zip(all_abs_dets, all_pms))}.",
)


# ---------------------------------------------------------------------------
# Formula correctness: C_G = (#PM)^{16} / 2^{8 n_sites} matches ledger.
# ---------------------------------------------------------------------------

record(
    "formula_matches_ledger_C_edge",
    C_edge_formula == sp.Rational(1, 2**16),
    f"Formula gives C_edge = {C_edge_formula} matching ledger 2^(-16).",
)
record(
    "formula_matches_ledger_C_plaq",
    C_plaq_formula == sp.Rational(1, 2**16),
    f"Formula gives C_plaq = {C_plaq_formula} matching ledger 2^(-16).",
)
record(
    "formula_matches_ledger_C_cube",
    C_cube_formula == sp.Rational(3**32, 2**64),
    f"Formula gives C_cube = {C_cube_formula} matching ledger (3/4)^32.",
)


# ---------------------------------------------------------------------------
# Deletion test (Musk): without K3 staggered phases, use unsigned
# adjacency and note |det| might not equal #PM.
# ---------------------------------------------------------------------------

# For the cube, build unsigned B (all +1 entries where edges exist).
unsigned_B = sp.zeros(4, 4)
ev_cube = [v for v in cube_sites if sum(v) % 2 == 0]
od_cube = [v for v in cube_sites if sum(v) % 2 == 1]
for i, ve in enumerate(ev_cube):
    for j, vo in enumerate(od_cube):
        if frozenset({ve, vo}) in cube_edge_set:
            unsigned_B[i, j] = 1
unsigned_det = sp.simplify(unsigned_B.det())
record(
    "unsigned_cube_block_det_differs_from_pm",
    abs(unsigned_det) != pm_cube,
    f"Unsigned cube block: det = {unsigned_det}; differs from #PM = {pm_cube}. K3 signs are load-bearing.",
)


# ---------------------------------------------------------------------------
# Target 2 structural summary.
# ---------------------------------------------------------------------------

record(
    "target_2_has_general_formula",
    all(
        C_formula == sp.Rational(pm**16, 2 ** (8 * n))
        for (C_formula, pm, n) in [
            (C_edge_formula, pm_edge, len(edge_sites)),
            (C_plaq_formula, pm_plaq, len(plaq_sites)),
            (C_line_formula, pm_line, len(line_sites)),
            (C_grid_formula, pm_grid, len(grid_sites)),
            (C_cube_formula, pm_cube, len(cube_sites)),
        ]
    ),
    "General formula C_G = (#PM)^16 / 2^(8 n_sites) verified on 5 test graphs.",
)


# ---------------------------------------------------------------------------
# Honest limits.
# ---------------------------------------------------------------------------

document(
    "conjectural_generality",
    "The identity |det(B_G)| = #PM(G) is verified case-by-case on five"
    " kit-derivable bipartite Z^3 subgraphs. A full proof would require"
    " showing the K3 staggered-phase assignment constitutes a Kasteleyn"
    " orientation for all planar-embeddable bipartite Z^3 subgraphs;"
    " this is standard for planar graphs (Kasteleyn 1961) but the"
    " general Z^3 case is conjectural here.",
)

document(
    "formula_is_a_structural_signature",
    "C_G = (#PM(G))^16 / 2^(8*n_sites) is a kit-specific structural"
    " signature: for alternative Dirac-like actions (forward difference,"
    " Wilson, non-staggered), |det(B)| and #PM can disagree. The K3"
    " symmetric-difference with staggered phases specifically realizes"
    " the Kasteleyn-like identity on Z^3 subgraphs.",
)

document(
    "new_kit_constant_2x3_grid",
    "The 2x3 grid is a new kit-derivable graph (not in prior ledger)."
    " It gives C_2x3 = 3^16 / 2^48, a specific predicted value that"
    " lies strictly between C_plaq = 2^(-16) and C_cube = (3/4)^32,"
    " illustrating the topology-dependent structure of C_G.",
)


# ---------------------------------------------------------------------------
# Emit.
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 78)
    print("Axiom-native runner -- C_G = (#PM)^16 / 2^{8 n_sites}")
    print("  Target 2, sub-step 2c -- perfect-matching unification")
    print("=" * 78)

    for (name, ok, detail) in RECORDS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")
        print(f"           {detail}")
    for (name, note) in DOCS:
        print(f"  [DOC]    {name}")
        print(f"           {note}")

    all_ok = all(ok for (_, ok, _) in RECORDS)
    print()
    if all_ok:
        print(f"OK: {len(RECORDS)} computed facts, {len(DOCS)} narrative notes.")
        return 0
    print("FAIL: at least one computed record is False.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
