#!/usr/bin/env python3
"""Exact Casimir block localization on the direct universal GR route.

This runner constructs the symmetric 3+1 polarization representation and the
SO(3) generators over exact SymPy radicals. It verifies that Pi_A1 fixes the
lapse/spatial-trace core and that the complement Casimir splits the remaining
channels into the shift vector and traceless spatial-shear blocks.

Scope: representation-level block localization only. This does not identify
the block-localized universal Hessian with Einstein/Regge dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def is_zero(mat: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in mat)


def sym(i: int, j: int, n: int = 4) -> sp.Matrix:
    m = sp.zeros(n, n)
    if i == j:
        m[i, j] = sp.Integer(1)
    else:
        m[i, j] = 1 / sp.sqrt(2)
        m[j, i] = 1 / sp.sqrt(2)
    return m


def diag(vals: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.diag(*vals)


def frob(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(a[i, j] * b[i, j] for i in range(a.rows) for j in range(a.cols)))


def canonical_polarization_frame() -> list[sp.Matrix]:
    """Orthonormal symmetric 3+1 polarization basis.

    Coordinate order is (t, x, y, z). Basis order:
      0 lapse h_tt
      1,2,3 shift h_tx, h_ty, h_tz
      4 spatial trace
      5,6,7,8,9 traceless spatial shear
    """

    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0, 1 / sp.sqrt(3), 1 / sp.sqrt(3), 1 / sp.sqrt(3))),
        diag((0, 1 / sp.sqrt(2), -1 / sp.sqrt(2), 0)),
        diag((0, 1 / sp.sqrt(6), 1 / sp.sqrt(6), -2 / sp.sqrt(6))),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def so3_generator(axis: str) -> sp.Matrix:
    """Infinitesimal spatial rotation matrix embedded in 3+1 dimensions."""

    a = sp.zeros(4, 4)
    if axis == "x":
        a[2, 3] = -1
        a[3, 2] = 1
    elif axis == "y":
        a[1, 3] = 1
        a[3, 1] = -1
    elif axis == "z":
        a[1, 2] = -1
        a[2, 1] = 1
    else:
        raise ValueError(axis)
    return a


def lifted_generator(axis: str) -> sp.Matrix:
    """Generator of h -> R(theta)^T h R(theta) on the 10D basis."""

    frame = canonical_polarization_frame()
    a = so3_generator(axis)
    out = sp.zeros(len(frame), len(frame))
    for j, basis in enumerate(frame):
        image = a.T * basis + basis * a
        for i, ref in enumerate(frame):
            out[i, j] = frob(ref, image)
    return sp.simplify(out)


def pi_a1() -> sp.Matrix:
    p = sp.zeros(10, 10)
    p[0, 0] = 1
    p[4, 4] = 1
    return p


def submatrix(mat: sp.Matrix, idx: list[int]) -> sp.Matrix:
    return mat.extract(idx, idx)


def lift_complement_projector(projector_c: sp.Matrix, comp_idx: list[int]) -> sp.Matrix:
    out = sp.zeros(10, 10)
    for i_c, i in enumerate(comp_idx):
        for j_c, j in enumerate(comp_idx):
            out[i, j] = projector_c[i_c, j_c]
    return out


def diagonal_projector_from_casimir(casimir: sp.Matrix, eigenvalue: int) -> sp.Matrix:
    diag_entries = [1 if sp.simplify(casimir[i, i] - eigenvalue) == 0 else 0 for i in range(casimir.rows)]
    return sp.diag(*diag_entries)


def compact_diag(mat: sp.Matrix) -> list[int]:
    return [int(sp.simplify(mat[i, i])) for i in range(mat.rows)]


def commutator(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.simplify(a * b - b * a)


def closes_so3(gx: sp.Matrix, gy: sp.Matrix, gz: sp.Matrix) -> bool:
    pairs = ((gx, gy, gz), (gy, gz, gx), (gz, gx, gy))
    return all(is_zero(commutator(a, b) - c) or is_zero(commutator(a, b) + c) for a, b, c in pairs)


def main() -> int:
    frame = canonical_polarization_frame()
    gram = sp.Matrix([[frob(a, b) for b in frame] for a in frame])
    gx = lifted_generator("x")
    gy = lifted_generator("y")
    gz = lifted_generator("z")
    pi = pi_a1()
    comp = sp.eye(10) - pi

    p_lapse = sp.zeros(10, 10)
    p_lapse[0, 0] = 1
    p_trace = sp.zeros(10, 10)
    p_trace[4, 4] = 1

    comp_idx = [i for i in range(10) if i not in (0, 4)]
    gc = [submatrix(g, comp_idx) for g in (gx, gy, gz)]
    casimir = sp.simplify(sum((g * g for g in gc), sp.zeros(8, 8)))
    casimir_diag = compact_diag(casimir)
    casimir_offdiag_zero = all(casimir[i, j] == 0 for i in range(8) for j in range(8) if i != j)

    p_shift_c = diagonal_projector_from_casimir(casimir, -2)
    p_shear_c = diagonal_projector_from_casimir(casimir, -6)
    p_shift = lift_complement_projector(p_shift_c, comp_idx)
    p_shear = lift_complement_projector(p_shear_c, comp_idx)

    p_sum = sp.simplify(p_lapse + p_trace + p_shift + p_shear)
    projectors = [p_lapse, p_trace, p_shift, p_shear]
    orthogonal = all(is_zero(projectors[i] * projectors[j]) for i in range(4) for j in range(i + 1, 4))
    idempotent = all(is_zero(p * p - p) for p in projectors)
    complete = is_zero(p_sum - sp.eye(10))

    comm_lapse = all(is_zero(commutator(p_lapse, g)) for g in (gx, gy, gz))
    comm_trace = all(is_zero(commutator(p_trace, g)) for g in (gx, gy, gz))
    comm_shift = all(is_zero(commutator(p_shift, g)) for g in (gx, gy, gz))
    comm_shear = all(is_zero(commutator(p_shear, g)) for g in (gx, gy, gz))
    a1_mixing_zero = all(is_zero(pi * g * comp) and is_zero(comp * g * pi) for g in (gx, gy, gz))
    closure_ok = closes_so3(gx, gy, gz)

    ranks = {
        "lapse": p_lapse.rank(),
        "shift": p_shift.rank(),
        "trace": p_trace.rank(),
        "shear": p_shear.rank(),
    }
    diag_shift = [int(p_shift[i, i]) for i in comp_idx]
    diag_shear = [int(p_shear[i, i]) for i in comp_idx]

    print("UNIVERSAL GR CASIMIR BLOCK LOCALIZATION")
    print("=" * 78)
    print("basis_order = [lapse, shift_x, shift_y, shift_z, trace, shear_1, shear_2, shear_xy, shear_xz, shear_yz]")
    print(f"basis_orthonormal = {gram == sp.eye(10)}")
    print(f"so3_closure_exact = {closure_ok}")
    print(f"A1_complement_mixing_zero = {a1_mixing_zero}")
    print(f"Casimir diagonal on complement = {casimir_diag}")
    print(f"Casimir off-diagonal zero on complement = {casimir_offdiag_zero}")
    print(f"ranks = {ranks}")
    print(f"projector complete = {complete}")
    print(f"projector orthogonal = {orthogonal}")
    print(f"projector idempotent = {idempotent}")
    print(f"commutes: lapse={comm_lapse}, trace={comm_trace}, shift={comm_shift}, shear={comm_shear}")
    print(f"diag P_shift on complement = {diag_shift}")
    print(f"diag P_shear on complement = {diag_shear}")

    record(
        "the displayed 10D polarization basis is exactly orthonormal",
        gram == sp.eye(10),
        "Frobenius Gram matrix equals the 10D identity",
    )
    record(
        "the lifted spatial generators close the SO(3) Lie algebra exactly",
        closure_ok,
        "all three commutators match the embedded generators up to orientation sign",
    )
    record(
        "Pi_A1 is invariant and its complement is an invariant subrepresentation",
        a1_mixing_zero,
        "Pi_A1 G (I-Pi_A1) and (I-Pi_A1) G Pi_A1 are zero for all generators",
    )
    record(
        "the complement Casimir has exactly the j=1 and j=2 split",
        casimir_diag == [-2, -2, -2, -6, -6, -6, -6, -6] and casimir_offdiag_zero,
        f"Casimir diagonal={casimir_diag}",
    )
    record(
        "the spectral projectors define a canonical shift/shear split on the complement",
        ranks == {"lapse": 1, "shift": 3, "trace": 1, "shear": 5},
        f"ranks={ranks}",
    )
    record(
        "the four block projectors are exact, orthogonal, and complete",
        complete and orthogonal and idempotent,
        f"complete={complete}, orthogonal={orthogonal}, idempotent={idempotent}",
    )
    record(
        "the block projectors commute with the universal SO(3) generators",
        comm_lapse and comm_trace and comm_shift and comm_shear,
        f"commutes=({comm_lapse},{comm_trace},{comm_shift},{comm_shear})",
    )
    record(
        "in the current canonical basis the Casimir projectors land on the expected coordinates",
        diag_shift == [1, 1, 1, 0, 0, 0, 0, 0] and diag_shear == [0, 0, 0, 1, 1, 1, 1, 1],
        "P_shift selects h0i and P_shear selects spatial traceless-symmetric channels",
    )

    print("\nBoundary:")
    print(
        "This proves the representation-level lapse/shift/trace/shear block split. "
        "It does not prove Einstein/Regge dynamics for the block-localized Hessian."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
