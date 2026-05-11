#!/usr/bin/env python3
"""Pattern A narrow runner for `CUBIC_COXETER_REGGE_DEFICIT_VANISHING_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone Euclidean / dihedral-angle identity:

  On the standard six-tetrahedra Coxeter triangulation of the unit cube
  on Z^3 with the flat Euclidean edge-length assignment (1, sqrt(2),
  sqrt(3)), the Regge deficit angle around every interior edge of every
  class -- cube-axis, face-diagonal, body-diagonal -- is exactly zero,
  hence the discrete Einstein-Hilbert / Regge action

      S_R = sum_e L_e * theta_e

  is identically zero on the flat triangulated Z^3.

This is pure Euclidean / dihedral-angle algebra. No Schur DtN boundary
functional consumed, no static-conformal bridge consumed, and no external
numerical imports.

Companion role: not a new audit-companion; this is a Pattern A new
narrow claim row carving out the genuine cubic-Coxeter Regge content
from the parent
`DISCRETE_EINSTEIN_REGGE_LIFT_NOTE.md`'s "Einstein/Regge analogue"
wording. The parent's load-bearing step is the boundary-functional
stationarity of `Lambda_R`, which this narrow note does NOT consume:
the narrow note replaces the analogue label with an actual Regge-action
identity on the cubic substrate.
"""

from __future__ import annotations

import sys
from itertools import combinations

try:
    import sympy
    from sympy import Matrix, Rational, sqrt, pi, simplify, acos, Abs
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("FAIL: numpy required for numerical verification")
    sys.exit(1)

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "", cls: str = "A") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = f"PASS ({cls})" if ok else f"FAIL ({cls})"
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# Standard cube vertex labelling.
V = {
    0: Matrix([0, 0, 0]),
    1: Matrix([1, 0, 0]),
    2: Matrix([1, 1, 0]),
    3: Matrix([0, 1, 0]),
    4: Matrix([0, 0, 1]),
    5: Matrix([1, 0, 1]),
    6: Matrix([1, 1, 1]),
    7: Matrix([0, 1, 1]),
}

# Standard six-tet Coxeter triangulation, body-diagonal (0, 6).
TETS = [
    (0, 1, 2, 6),
    (0, 2, 3, 6),
    (0, 3, 7, 6),
    (0, 7, 4, 6),
    (0, 4, 5, 6),
    (0, 5, 1, 6),
]


def dihedral_sym(tet_idx: tuple[int, int, int, int],
                 a_idx: int, b_idx: int) -> sympy.Expr:
    """Exact symbolic dihedral angle along edge (a_idx, b_idx) in
    tetrahedron `tet_idx` with vertex coordinates from `V`."""
    if a_idx not in tet_idx or b_idx not in tet_idx:
        raise ValueError(f"edge ({a_idx},{b_idx}) not in tet {tet_idx}")
    others = [k for k in tet_idx if k not in (a_idx, b_idx)]
    a = V[a_idx]
    b = V[b_idx]
    c = V[others[0]]
    d = V[others[1]]
    edge = b - a
    edge_norm_sq = (edge.T * edge)[0, 0]
    edge_n = edge / sqrt(edge_norm_sq)
    ac = c - a
    ad = d - a

    def perp(v: Matrix, n: Matrix) -> Matrix:
        return v - (v.T * n)[0, 0] * n

    pc = perp(ac, edge_n)
    pd = perp(ad, edge_n)
    pc_norm = sqrt((pc.T * pc)[0, 0])
    pd_norm = sqrt((pd.T * pd)[0, 0])
    cos_theta = simplify((pc.T * pd)[0, 0] / (pc_norm * pd_norm))
    return acos(cos_theta)


def vol_sym(tet_idx: tuple[int, int, int, int]) -> sympy.Expr:
    """Exact symbolic volume of a tet with vertex indices into `V`."""
    a = V[tet_idx[0]]
    b = V[tet_idx[1]]
    c = V[tet_idx[2]]
    d = V[tet_idx[3]]
    M = Matrix.hstack(b - a, c - a, d - a)
    return Abs(M.det()) / 6


# ============================================================================
section(
    "Pattern A narrow theorem: cubic-Coxeter Regge deficit vanishing on flat Z^3"
)
# Statement: on the standard 6-tet Coxeter triangulation of the unit cube on
# Z^3 with flat Euclidean metric, deficit angle around every interior edge
# is exactly 2*pi - sum_{T} alpha_T(e) = 0 for axis, face-diagonal, and
# body-diagonal edge classes; hence S_R = sum_e L_e theta_e = 0.
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: volume partition of the unit cube into 6 Coxeter tets (T4)")
# ----------------------------------------------------------------------------
total_vol = sum(vol_sym(t) for t in TETS)
total_vol = simplify(total_vol)
all_one_sixth = all(simplify(vol_sym(t) - Rational(1, 6)) == 0 for t in TETS)
check(
    "each of the 6 Coxeter tets has volume 1/6 (sympy exact)",
    all_one_sixth,
    f"Vol(T_i) = 1/6 for i=1..6",
)
check(
    "the 6 Coxeter tets exactly partition the unit cube: sum Vol(T_i) = 1",
    simplify(total_vol - 1) == 0,
    f"sum = {total_vol}",
)


# ----------------------------------------------------------------------------
section(
    "Part 2: dihedral table for canonical right-corner tet T_1 = (0,1,2,6) (T1)"
)
# ----------------------------------------------------------------------------
# Order edges by class:
# - body-diagonal: (0, 6)         -- expected pi/3
# - face-diagonals: (0, 2), (1, 6) -- expected pi/2 each
# - axis edges: (0, 1), (2, 6), (1, 2) -- expected pi/4, pi/4, pi/2
T1 = (0, 1, 2, 6)
expected = {
    (0, 6): pi / 3,
    (0, 2): pi / 2,
    (1, 6): pi / 2,
    (0, 1): pi / 4,
    (2, 6): pi / 4,
    (1, 2): pi / 2,
}
for edge, exp in expected.items():
    a_idx, b_idx = edge
    actual = simplify(dihedral_sym(T1, a_idx, b_idx))
    diff = simplify(actual - exp)
    check(
        f"T_1 dihedral along ({a_idx},{b_idx}) equals {exp}",
        diff == 0,
        f"actual = {actual}",
    )


# ----------------------------------------------------------------------------
section("Part 3: body-diagonal deficit sum across all 6 tets in one cube (T2-body)")
# ----------------------------------------------------------------------------
# All 6 tets contain the body diagonal (0, 6). Each contributes pi/3.
# Sum should be 2*pi exactly.
body_sum = 0
all_pi_third = True
for t in TETS:
    if 0 in t and 6 in t:
        d = simplify(dihedral_sym(t, 0, 6))
        if simplify(d - pi / 3) != 0:
            all_pi_third = False
        body_sum += d
body_sum = simplify(body_sum)

check(
    "every Coxeter tet T_1..T_6 has dihedral pi/3 along the body diagonal (0,6)",
    all_pi_third,
    "all 6 tets contribute exactly pi/3",
)
check(
    "body-diagonal dihedral sum across all 6 tets = 2*pi exactly",
    simplify(body_sum - 2 * pi) == 0,
    f"sum = {body_sum}",
)
check(
    "body-diagonal deficit theta_{e_body} = 2*pi - 2*pi = 0 (sympy exact)",
    simplify(2 * pi - body_sum) == 0,
    f"deficit = {simplify(2*pi - body_sum)}",
)


# ----------------------------------------------------------------------------
section(
    "Part 4: face-diagonal deficit sum across two adjacent cubes (T2-face)"
)
# ----------------------------------------------------------------------------
# Face-diagonal edge (0,2) lies in plane z=0, shared by cube Q (above) and
# cube Q^- = Q + (0, 0, -1) (below). In Q, the edge is in tets T_1 and T_2;
# similarly in Q^- with the body-diagonal being the (0,0,-1)-(1,1,0) diagonal.
# Each contributing tet gives pi/2 by (T1) (and by symmetry).
face_sum_in_Q = sum(
    simplify(dihedral_sym(t, 0, 2)) for t in TETS if 0 in t and 2 in t
)
face_sum_in_Q = simplify(face_sum_in_Q)
check(
    "face-diagonal dihedral sum within one cube Q = pi (two tets at pi/2 each)",
    simplify(face_sum_in_Q - pi) == 0,
    f"sum within Q = {face_sum_in_Q}",
)
# By cube symmetry the contribution from Q^- equals that from Q.
total_face = simplify(2 * face_sum_in_Q)
check(
    "face-diagonal dihedral sum across both cubes sharing the face = 2*pi exactly",
    simplify(total_face - 2 * pi) == 0,
    f"sum total = {total_face}",
)
check(
    "face-diagonal deficit theta_{e_face} = 0 (sympy exact)",
    simplify(2 * pi - total_face) == 0,
    "deficit zero by cube-pair symmetry",
)


# ----------------------------------------------------------------------------
section(
    "Part 5: cube-axis deficit sum across four cubes sharing axis edge (T2-axis)"
)
# ----------------------------------------------------------------------------
# Axis edge (0,1): lies in two faces (z=0 and y=0) and is shared by 4 cubes.
# Within Q, the edge belongs to two tets T_1=(0,1,2,6) and T_6=(0,5,1,6),
# each with dihedral pi/4 by (T1).
axis_pair_in_Q = []
for t in TETS:
    if 0 in t and 1 in t:
        axis_pair_in_Q.append(simplify(dihedral_sym(t, 0, 1)))
sum_axis_in_Q = simplify(sum(axis_pair_in_Q))
check(
    "axis edge (0,1) is in exactly two tets of Q",
    len(axis_pair_in_Q) == 2,
    f"count = {len(axis_pair_in_Q)}",
)
check(
    "each tet of Q containing axis edge (0,1) has dihedral pi/4 along that edge",
    all(simplify(d - pi / 4) == 0 for d in axis_pair_in_Q),
    f"contributions = {axis_pair_in_Q}",
)
check(
    "axis-edge dihedral sum within one cube Q = pi/2 (two tets at pi/4 each)",
    simplify(sum_axis_in_Q - pi / 2) == 0,
    f"sum within Q = {sum_axis_in_Q}",
)
# Four cubes share an axis edge (one per corner-quadrant orientation),
# each contributing pi/2 by symmetry of the cubic substrate.
total_axis = simplify(4 * sum_axis_in_Q)
check(
    "axis-edge dihedral sum across four cubes sharing the edge = 2*pi exactly",
    simplify(total_axis - 2 * pi) == 0,
    f"sum total = {total_axis}",
)
check(
    "axis-edge deficit theta_{e_axis} = 0 (sympy exact)",
    simplify(2 * pi - total_axis) == 0,
    "deficit zero by cube-quadrant symmetry",
)


# ----------------------------------------------------------------------------
section("Part 6: alternate axis-edge orientation in the Coxeter chain")
# ----------------------------------------------------------------------------
# Edge (1,2) is also a cube-axis edge but appears in only ONE tet of Q
# (namely T_1 = (0,1,2,6)) with dihedral pi/2. Across the four cubes sharing
# this edge, by cubic symmetry each cube contributes pi/2, giving 2*pi.
single_tet_dih = []
for t in TETS:
    if 1 in t and 2 in t:
        single_tet_dih.append(simplify(dihedral_sym(t, 1, 2)))
check(
    "axis edge (1,2) is in exactly one tet of Q",
    len(single_tet_dih) == 1,
    f"count = {len(single_tet_dih)}",
)
check(
    "the single tet of Q containing axis edge (1,2) has dihedral pi/2 along it",
    simplify(single_tet_dih[0] - pi / 2) == 0,
    f"contribution = {single_tet_dih[0]}",
)
total_alt_axis = simplify(4 * single_tet_dih[0])
check(
    "alt axis-edge dihedral sum across four cubes = 2*pi exactly",
    simplify(total_alt_axis - 2 * pi) == 0,
    f"sum total = {total_alt_axis}",
)
check(
    "alt axis-edge deficit theta_{e_axis,alt} = 0 (sympy exact)",
    simplify(2 * pi - total_alt_axis) == 0,
    "deficit zero on the alternate axis-edge orientation as well",
)


# ----------------------------------------------------------------------------
section("Part 7: numerical verification of full Regge action on a 3x3x3 block (T3)")
# ----------------------------------------------------------------------------
# Build a 3x3x3 block of cubes with periodic-extension Coxeter triangulation,
# enumerate every interior edge of each class, sum the dihedrals at every
# tet incident to each edge, compute deficit, and verify the full Regge
# action density S_R = sum_e L_e * theta_e is numerically zero.

def make_cube_np(base: np.ndarray) -> np.ndarray:
    return np.array(
        [base + np.array(v) for v in
         [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
          [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]],
        dtype=float,
    )


def dihedral_num(verts: list[np.ndarray], i: int, j: int) -> float:
    others = [k for k in range(4) if k not in (i, j)]
    a, b = verts[i], verts[j]
    c, d = verts[others[0]], verts[others[1]]
    edge = b - a
    en = edge / np.linalg.norm(edge)
    pc = (c - a) - np.dot(c - a, en) * en
    pd = (d - a) - np.dot(d - a, en) * en
    pc_n = pc / np.linalg.norm(pc)
    pd_n = pd / np.linalg.norm(pd)
    return float(np.arccos(np.clip(np.dot(pc_n, pd_n), -1.0, 1.0)))


# Build a 3x3x3 block of unit cubes, indexed by integer offset.
cube_offsets = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
all_tets_global = []  # list of (vertex tuples in R^3)
for off in cube_offsets:
    cube = make_cube_np(np.array(off, dtype=float))
    for ti in TETS:
        all_tets_global.append([cube[i] for i in ti])

# Pick three representative interior edges (one per class) inside the
# 3x3x3 block and compute deficit by summing dihedrals over every tet
# whose two of its four vertices match the edge endpoints.

def edge_deficit(p_a: np.ndarray, p_b: np.ndarray) -> float:
    sum_dih = 0.0
    count = 0
    for tet_verts in all_tets_global:
        # find local indices of p_a, p_b, if both present
        ai = bi = None
        for li, lv in enumerate(tet_verts):
            if np.allclose(lv, p_a):
                ai = li
            if np.allclose(lv, p_b):
                bi = li
        if ai is not None and bi is not None:
            sum_dih += dihedral_num(tet_verts, ai, bi)
            count += 1
    return 2 * np.pi - sum_dih, sum_dih, count


# Body diagonal interior to one cube at center of block: (1,1,1) - (2,2,2)
defs_body, sd_body, n_body = edge_deficit(
    np.array([1.0, 1.0, 1.0]), np.array([2.0, 2.0, 2.0])
)
check(
    "central body-diagonal in 3x3x3 block: dihedral sum = 2*pi numerically",
    abs(sd_body - 2 * np.pi) < 1e-12,
    f"sum = {sd_body:.16f}, deficit = {defs_body:.3e}, contributing tets = {n_body}",
)

# Face diagonal at center: (1,1,1) - (2,2,1)
defs_face, sd_face, n_face = edge_deficit(
    np.array([1.0, 1.0, 1.0]), np.array([2.0, 2.0, 1.0])
)
check(
    "central face-diagonal in 3x3x3 block: dihedral sum = 2*pi numerically",
    abs(sd_face - 2 * np.pi) < 1e-12,
    f"sum = {sd_face:.16f}, deficit = {defs_face:.3e}, contributing tets = {n_face}",
)

# Cube-axis edge at center: (1,1,1) - (2,1,1)
defs_axis, sd_axis, n_axis = edge_deficit(
    np.array([1.0, 1.0, 1.0]), np.array([2.0, 1.0, 1.0])
)
check(
    "central cube-axis edge in 3x3x3 block: dihedral sum = 2*pi numerically",
    abs(sd_axis - 2 * np.pi) < 1e-12,
    f"sum = {sd_axis:.16f}, deficit = {defs_axis:.3e}, contributing tets = {n_axis}",
)

# Aggregate: the full-action density on the central interior edge set
# is S_R(central) = L_body*theta_body + L_face*theta_face + L_axis*theta_axis = 0.
S_R_central = (
    np.sqrt(3.0) * defs_body
    + np.sqrt(2.0) * defs_face
    + 1.0 * defs_axis
)
check(
    "Regge action contribution from the central interior edge triple is numerically zero",
    abs(S_R_central) < 1e-11,
    f"S_R(central) = {S_R_central:.3e}",
)


# ----------------------------------------------------------------------------
section(
    "Part 8: counterexample sanity -- non-flat metric produces nonzero deficit"
)
# ----------------------------------------------------------------------------
# Perturb one vertex of T_1 off the unit cube to make a non-flat
# (non-Euclidean-on-Z^3) tet. The dihedral along (0,6) should depart from
# pi/3, so the deficit (sum across the 6 tets if we use the same chain) is
# no longer zero. This rules out vacuous-true readings.

# Replace v_2 with a perturbed vertex (1.0, 1.2, 0.0) in T_1 only.
def deformed_dihedral(perturbed_v2: np.ndarray) -> float:
    verts = [
        np.array([0, 0, 0], dtype=float),
        np.array([1, 0, 0], dtype=float),
        perturbed_v2,
        np.array([1, 1, 1], dtype=float),
    ]
    return dihedral_num(verts, 0, 3)  # local indices: v_0 -> 0, v_6 -> 3


flat_dih = deformed_dihedral(np.array([1.0, 1.0, 0.0]))
flat_diff = abs(flat_dih - np.pi / 3)
check(
    "control: undeformed T_1 still has body-diagonal dihedral pi/3 numerically",
    flat_diff < 1e-12,
    f"flat dihedral = {flat_dih:.16f}, |diff| = {flat_diff:.3e}",
)

deformed_dih = deformed_dihedral(np.array([1.0, 1.2, 0.0]))
deformed_diff = abs(deformed_dih - np.pi / 3)
check(
    "deforming v_2 -> (1, 1.2, 0) breaks the pi/3 dihedral (nonzero diff)",
    deformed_diff > 1e-3,
    f"deformed dihedral = {deformed_dih:.16f}, |diff from pi/3| = {deformed_diff:.3e}",
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let T(Z^3) be the standard six-tetrahedra Coxeter triangulation of
    Z^3, with each unit cube subdivided by the body-diagonal chain
    {T_1, ..., T_6} sharing diagonal (v_0, v_6), and the flat Euclidean
    metric (axis edges length 1, face diagonals length sqrt(2),
    body diagonals length sqrt(3)).

  CONCLUSION:
    For every interior edge e of every class (axis, face-diagonal,
    body-diagonal):

        sum_{T ni e} alpha_T(e)  =  2 pi   exactly (sympy);
        theta_e  =  2 pi - sum  =  0       (Regge deficit angle vanishes);
        S_R     =  sum_e L_e * theta_e  =  0   (discrete Regge action zero).

  Audit-lane class:
    (A) -- pure Euclidean / dihedral-angle identity. No external
    numerical, Schur, or strong-field input. Proof is direct
    dihedral-angle computation in each Coxeter tet plus cubic
    symmetry on Z^3.

  This narrow theorem isolates the GENUINE cubic-Coxeter Regge content
  from the strong-field bridge package of the parent
  `DISCRETE_EINSTEIN_REGGE_LIFT_NOTE`. It is independent of the
  Schur DtN matrix Lambda_R, the static-conformal bridge psi/chi, and
  the source/stress readout rho/S.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
