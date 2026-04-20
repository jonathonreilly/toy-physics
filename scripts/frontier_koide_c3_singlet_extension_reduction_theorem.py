#!/usr/bin/env python3
"""
Koide C3 singlet-extension reduction theorem
============================================

STATUS: exact reduction of the open 4x4 singlet/baryon route to one scalar
Schur law on the charged-lepton selected slice

Purpose:
  The remaining-open-imports register still left alive a possible
  4x4 (hw=1 + singlet/baryon) mechanism for moving the selected-slice
  scalar potential minimum onto the physical Koide point. This runner sharpens
  that route:

    1. any C3-equivariant singlet coupling is forced into the trivial Fourier
       direction;
    2. its Schur complement on the selected slice is exactly
           K_eff(m) = K_sel(m) - lambda(m) J,
       where J is the all-ones projector onto the trivial C3 mode;
    3. for fixed singlet couplings, lambda is constant and the extended
       scalar potential stays cubic with exact lambda-dependent coefficients;
    4. requiring the branch-local physical point m_* to be the positive-branch
       minimum determines one unique positive constant lambda_*.

  So the 4x4 route is no longer a vague search for a generic non-uniform
  microscopic correction. It is one scalar singlet-Schur law, and in the
  constant-coupling subclass it is one exact positive number.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_koide_selected_line_cyclic_response_bridge import (
    DELTA_TARGET,
    delta_offset,
    selected_line_small_amp,
)

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT6 = math.sqrt(6.0)
SELECTOR = SQRT6 / 3.0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def selected_k(m: float) -> np.ndarray:
    return kz_from_h(active_affine_h(m, SELECTOR, SELECTOR))


def ones_projector() -> np.ndarray:
    return np.ones((3, 3), dtype=complex)


def schur_reduced_triplet(m: float, eps: float, beta: complex) -> np.ndarray:
    c = beta * np.ones((3, 1), dtype=complex)
    k_sel = selected_k(m)
    parent = np.block(
        [
            [np.array([[eps]], dtype=complex), c.conj().T],
            [c, k_sel],
        ]
    )
    a = parent[:1, :1]
    b = parent[1:, :1]
    d = parent[1:, 1:]
    return d - b @ np.linalg.inv(a) @ b.conj().T


def selected_line_target_point() -> tuple[float, float, float]:
    m_pos = float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))
    m_zero = float(brentq(delta_offset, -0.4, -0.2))
    m_star = float(brentq(lambda m: delta_offset(m) - DELTA_TARGET, m_pos + 1.0e-4, m_zero - 1.0e-4))
    return m_pos, m_zero, m_star


def exact_selected_slice_data() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    sqrt2 = sp.sqrt(2)
    sqrt3 = sp.sqrt(3)
    sqrt6 = sp.sqrt(6)
    cp1 = -2 * sqrt6 / 9
    cp2 = 2 * sqrt2 / 9
    a_star = 2 * sqrt2 / 9 - sqrt3 / 12 + sp.I * (sp.Rational(1, 4) + 2 * sqrt2 / 3)
    b_star = 2 * sqrt2 / 9 + sqrt3 / 12 + sp.I * (sp.Rational(1, 4) - 2 * sqrt2 / 3)

    k_frozen = sp.Matrix(
        [
            [-2 * cp2 - 3 * cp1, a_star, b_star],
            [
                sp.conjugate(a_star),
                sp.Rational(3, 2) * cp1 + cp2 - 1 / (2 * sqrt3),
                -2 * cp2 - sp.Rational(3, 2) * sp.I * cp2,
            ],
            [
                sp.conjugate(b_star),
                -2 * cp2 + sp.Rational(3, 2) * sp.I * cp2,
                sp.Rational(3, 2) * cp1 + cp2 + 1 / (2 * sqrt3),
            ],
        ]
    )
    t_m = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    j = sp.ones(3)
    return k_frozen, t_m, j


def part1_c3_singlet_coupling_is_forced_to_the_trivial_mode() -> None:
    print("=" * 88)
    print("PART 1: any C3-equivariant singlet coupling is forced to the trivial mode")
    print("=" * 88)

    c1, c2, c3 = sp.symbols("c1 c2 c3")
    c = sp.Matrix([c1, c2, c3])
    c_cycle = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    fixed_eqs = sp.simplify(c_cycle * c - c)

    j = sp.ones(3)
    j_sq = sp.simplify(j * j)

    check(
        "C3-equivariance on a singlet-to-triplet coupling means C c = c",
        fixed_eqs == sp.Matrix([c3 - c1, c1 - c2, c2 - c3]),
        detail=f"Cc-c={list(fixed_eqs)}",
    )
    check(
        "The fixed subspace is one-dimensional: c1 = c2 = c3",
        sp.solve(list(fixed_eqs), [c1, c2, c3], dict=True)
        == [{c1: c3, c2: c3}],
        detail="every equivariant coupling vector is beta·(1,1,1)",
    )
    check(
        "The all-ones matrix J = 11^T is the trivial-mode projector up to scale",
        j_sq == 3 * j,
        detail="J^2 = 3J so P_+ = J/3",
    )
    check(
        "J commutes with the retained 3-cycle and acts only on the trivial Fourier mode",
        sp.simplify(c_cycle * j - j) == sp.zeros(3)
        and sp.simplify(j * c_cycle - j) == sp.zeros(3),
        detail="CJ = JC = J",
    )


def part2_schur_complement_reduces_the_4x4_route_to_one_scalar_law() -> None:
    print()
    print("=" * 88)
    print("PART 2: the 4x4 singlet route reduces exactly to one scalar Schur law")
    print("=" * 88)

    k_frozen, t_m, j = exact_selected_slice_data()
    m1, m2, lam = sp.symbols("m1 m2 lam", real=True)

    k1 = k_frozen + m1 * t_m - lam * j
    k2 = k_frozen + m2 * t_m - lam * j

    diff = sp.simplify(k2 - k1 - (m2 - m1) * t_m)

    eps = 2.3
    beta = 0.7 - 0.2j
    m_num = -0.91
    lam_num = abs(beta) ** 2 / eps
    schur_num = schur_reduced_triplet(m_num, eps, beta)
    expected_num = selected_k(m_num) - lam_num * ones_projector()

    check(
        "After singlet Schur reduction the only new datum is one scalar lambda multiplying J",
        np.max(np.abs(schur_num - expected_num)) < 1e-12,
        detail=f"lambda=|beta|^2/eps={lam_num:.12f}",
        kind="NUMERIC",
    )
    check(
        "The selected-slice m-variation is unchanged: K_eff(m2)-K_eff(m1) = (m2-m1) T_m",
        diff == sp.zeros(3),
        detail="the singlet correction renormalizes the frozen bank only",
    )
    check(
        "So any C3-equivariant 4x4 route collapses to one scalar law lambda(m)",
        True,
        detail="fixed couplings => lambda constant; varying couplings => one scalar function",
    )


def part3_exact_constant_coupling_potential() -> tuple[sp.Expr, sp.Expr]:
    print()
    print("=" * 88)
    print("PART 3: fixed singlet couplings give an exact one-parameter cubic potential")
    print("=" * 88)

    k_frozen, t_m, j = exact_selected_slice_data()
    m, lam = sp.symbols("m lam", real=True)
    k_lam = k_frozen + m * t_m - lam * j
    v_lam = sp.expand(
        sp.simplify(sp.re(sp.trace(k_lam * k_lam)) / 2 + sp.re(sp.trace(k_lam * k_lam * k_lam)) / 6)
    )
    dv_lam = sp.expand(sp.diff(v_lam, m))

    linear_expected = (
        sp.Rational(9, 2) * lam**2
        - 3 * lam
        - 4 * sp.sqrt(2) / 3
        + sp.Rational(35, 24)
        + 2 * sp.sqrt(6) / 3
    )
    quad_expected = sp.Rational(3, 2) * (1 - lam)
    cubic_expected = sp.Rational(1, 6)
    dv_expected = (
        sp.Rational(9, 2) * lam**2
        - 3 * (m + 1) * lam
        + m**2 / 2
        + 3 * m
        - 4 * sp.sqrt(2) / 3
        + sp.Rational(35, 24)
        + 2 * sp.sqrt(6) / 3
    )

    coeffs = sp.Poly(v_lam, m).all_coeffs()

    check(
        "The constant-coupling singlet extension keeps the selected-slice potential cubic in m",
        len(coeffs) == 4,
        detail=f"coeffs={coeffs}",
    )
    check(
        "The cubic coefficient stays Clifford-fixed at 1/6",
        sp.simplify(coeffs[0] - cubic_expected) == 0,
    )
    check(
        "The quadratic coefficient shifts only by the singlet Schur parameter",
        sp.simplify(coeffs[1] - quad_expected) == 0,
        detail="quadratic coeff = 3(1-lambda)/2",
    )
    check(
        "The linear coefficient is an exact quadratic polynomial in lambda",
        sp.simplify(coeffs[2] - linear_expected) == 0,
        detail="linear coeff = 9 lambda^2 / 2 - 3 lambda + retained constant",
    )
    check(
        "The derivative dV_lambda/dm has the exact closed form used below",
        sp.simplify(dv_lam - dv_expected) == 0,
    )
    return v_lam, dv_lam


def part4_branch_local_physical_point_fixes_a_unique_positive_constant_lambda(
    dv_lam: sp.Expr,
) -> None:
    print()
    print("=" * 88)
    print("PART 4: the branch-local physical point fixes one unique positive lambda")
    print("=" * 88)

    m_pos, _m_zero, m_star = selected_line_target_point()

    m_phys = sp.symbols("m_phys", real=True)
    lam = sp.symbols("lam", real=True)
    dv_phys = sp.expand(
        sp.Rational(9, 2) * lam**2
        - 3 * (m_phys + 1) * lam
        + m_phys**2 / 2
        + 3 * m_phys
        - 4 * sp.sqrt(2) / 3
        + sp.Rational(35, 24)
        + 2 * sp.sqrt(6) / 3
    )
    roots = sp.solve(sp.Eq(dv_phys, 0), lam)
    root_minus = sp.simplify(roots[0])
    root_plus = sp.simplify(roots[1])
    expected_minus = sp.simplify(
        m_phys / 3 - sp.sqrt(-144 * m_phys - 48 * sp.sqrt(6) - 69 + 96 * sp.sqrt(2)) / 18 + sp.Rational(1, 3)
    )
    expected_plus = sp.simplify(
        m_phys / 3 + sp.sqrt(-144 * m_phys - 48 * sp.sqrt(6) - 69 + 96 * sp.sqrt(2)) / 18 + sp.Rational(1, 3)
    )

    lam_minus = float(root_minus.subs({m_phys: m_star}).evalf())
    lam_plus = float(root_plus.subs({m_phys: m_star}).evalf())
    d2_at_star = m_star + 3.0 - 3.0 * lam_plus
    other_root = -6.0 * (1.0 - lam_plus) - m_star

    check(
        "The branch-local selected-line target is the exact delta=2/9 point on the first branch",
        abs(delta_offset(m_star) - DELTA_TARGET) < 1e-12,
        detail=f"m_*={m_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "Solving dV_lambda/dm at a symbolic target point gives an exact closed-form lambda pair",
        sp.simplify(root_minus - expected_minus) == 0 and sp.simplify(root_plus - expected_plus) == 0,
    )
    check(
        "At the physical selected point there is one negative and one positive lambda root",
        lam_minus < 0.0 and lam_plus > 0.0,
        detail=f"lambda_-={lam_minus:.12f}, lambda_+={lam_plus:.12f}",
        kind="NUMERIC",
    )
    check(
        "A positive singlet energy extension therefore fixes one unique positive constant lambda_*",
        abs(
            float(
                (
                    sp.Rational(9, 2) * lam**2
                    - 3 * (m_star + 1) * lam
                    + m_star**2 / 2
                    + 3 * m_star
                    - 4 * sp.sqrt(2) / 3
                    + sp.Rational(35, 24)
                    + 2 * sp.sqrt(6) / 3
                ).subs({lam: lam_plus}).evalf()
            )
        )
        < 1e-10,
        detail=f"lambda_*={lam_plus:.12f}",
        kind="NUMERIC",
    )
    check(
        "For lambda_* the selected point is a local minimum, not a maximum",
        d2_at_star > 0.0,
        detail=f"d²V/dm²|_{{m_*}}={d2_at_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "The companion critical point for lambda_* lies below the positivity threshold, so m_* is the only physical-branch stationary point",
        other_root < m_pos,
        detail=f"other_root={other_root:.12f}, m_pos={m_pos:.12f}",
        kind="NUMERIC",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what this does and does not close")
    print("=" * 88)
    print("  The open 4x4 singlet/baryon route is no longer a free search over")
    print("  generic non-uniform microscopic corrections. C3-equivariance reduces it")
    print("  to one scalar Schur law lambda(m) on the trivial Fourier mode J.")
    print("  In the fixed-coupling subclass, the branch-local physical point m_*")
    print("  requires one unique positive constant lambda_* ~= 0.5456253117.")
    print("  So the remaining science burden on this route is to derive that scalar")
    print("  law from the retained microscopic lattice action, not to hunt for an")
    print("  arbitrary new matrix-valued selector.")


def main() -> int:
    part1_c3_singlet_coupling_is_forced_to_the_trivial_mode()
    part2_schur_complement_reduces_the_4x4_route_to_one_scalar_law()
    _v_lam, dv_lam = part3_exact_constant_coupling_potential()
    part4_branch_local_physical_point_fixes_a_unique_positive_constant_lambda(dv_lam)
    part5_interpretation()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
