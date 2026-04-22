#!/usr/bin/env python3
"""
Koide C3 constant singlet reparameterization theorem
====================================================

STATUS: exact sharpening of the fixed-coupling singlet-Schur route

Purpose:
  The companion singlet-extension reduction theorem showed that any
  C3-equivariant 4x4 singlet route collapses to one scalar Schur law

      K_eff(m) = K_sel(m) - lambda J.

  In the fixed-coupling subclass lambda is constant, and imposing the physical
  point m_* determines one positive value lambda_*.

  This runner asks the sharper question:

      does constant lambda actually SELECT m_*?

  Answer:
      no. On the physical first branch, the stationarity condition can be
      solved exactly for lambda as a function of m. The positive branch of
      that solution sweeps a whole interval of candidate physical stationary
      points, and over the upper part of the interval there are two positive
      lambda values for the same m.

  So fixed-coupling singlet dressing does not close the Koide scalar gap.
  It reparameterizes a continuum of branch points.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

from frontier_koide_selected_line_cyclic_response_bridge import (
    DELTA_TARGET,
    delta_offset,
    selected_line_small_amp,
)


PASS_COUNT = 0
FAIL_COUNT = 0

SQRT2 = math.sqrt(2.0)
SQRT6 = math.sqrt(6.0)


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


def positive_threshold() -> float:
    return float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))


def selected_line_target_point(m_pos: float) -> tuple[float, float]:
    m_zero = float(brentq(delta_offset, -0.4, -0.2))
    m_star = float(
        brentq(lambda m: delta_offset(m) - DELTA_TARGET, m_pos + 1.0e-4, m_zero - 1.0e-4)
    )
    return m_zero, m_star


def stationary_poly(m: float, lam: float) -> float:
    return (
        4.5 * lam * lam
        - 3.0 * (m + 1.0) * lam
        + 0.5 * m * m
        + 3.0 * m
        - 4.0 * SQRT2 / 3.0
        + 35.0 / 24.0
        + 2.0 * SQRT6 / 3.0
    )


def discriminant(m: float) -> float:
    return -144.0 * m - 48.0 * SQRT6 - 69.0 + 96.0 * SQRT2


def lambda_roots(m: float) -> tuple[float, float]:
    disc = discriminant(m)
    if disc < 0.0:
        raise ValueError("stationary lambda roots are not real at this m")
    rad = math.sqrt(disc)
    return (
        m / 3.0 + 1.0 / 3.0 - rad / 18.0,
        m / 3.0 + 1.0 / 3.0 + rad / 18.0,
    )


def other_stationary_root(m: float, lam: float) -> float:
    return -6.0 * (1.0 - lam) - m


def part1_exact_stationary_root_formulas() -> tuple[float, float]:
    print("=" * 88)
    print("PART 1: exact stationary lambda roots on the selected line")
    print("=" * 88)

    m = sp.symbols("m", real=True)
    lam = sp.symbols("lam", real=True)
    disc = -144 * m - 48 * sp.sqrt(6) - 69 + 96 * sp.sqrt(2)
    dv = (
        sp.Rational(9, 2) * lam**2
        - 3 * (m + 1) * lam
        + m**2 / 2
        + 3 * m
        - 4 * sp.sqrt(2) / 3
        + sp.Rational(35, 24)
        + 2 * sp.sqrt(6) / 3
    )
    roots = sp.solve(sp.Eq(dv, 0), lam)
    root_minus = sp.simplify(roots[0])
    root_plus = sp.simplify(roots[1])
    expected_minus = sp.simplify(m / 3 + sp.Rational(1, 3) - sp.sqrt(disc) / 18)
    expected_plus = sp.simplify(m / 3 + sp.Rational(1, 3) + sp.sqrt(disc) / 18)

    m_disc_expr = sp.simplify((96 * sp.sqrt(2) - 48 * sp.sqrt(6) - 69) / 144)
    m_v_expr = sp.simplify(-3 + sp.sqrt(-48 * sp.sqrt(6) + 96 * sp.sqrt(2) + 219) / 6)

    m_disc = float(m_disc_expr.evalf())
    m_v = float(m_v_expr.evalf())

    check(
        "The fixed-coupling stationary condition is an exact quadratic in lambda",
        sp.Poly(dv, lam).degree() == 2,
        detail=f"dV/dm = {sp.expand(dv)}",
    )
    check(
        "Its exact roots are lambda_-(m), lambda_+(m) with one linear discriminant",
        sp.simplify(root_minus - expected_minus) == 0 and sp.simplify(root_plus - expected_plus) == 0,
        detail=f"Delta(m) = {sp.expand(disc)}",
    )
    check(
        "The real-root endpoint is the exact discriminant zero m_disc",
        sp.simplify(disc.subs({m: m_disc_expr})) == 0,
        detail=f"m_disc={m_disc:.12f}",
    )
    check(
        "The lower root hits zero exactly at the zero-coupling selected-slice minimum m_V",
        sp.simplify(expected_minus.subs({m: m_v_expr})) == 0,
        detail=f"m_V={m_v:.12f}",
    )
    return m_disc, m_v


def part2_branch_interval_structure(m_disc: float, m_v: float) -> tuple[float, float, float]:
    print()
    print("=" * 88)
    print("PART 2: physical-branch interval structure")
    print("=" * 88)

    m_pos = positive_threshold()
    m_zero, m_star = selected_line_target_point(m_pos)

    check(
        "The physical delta=2/9 point lies strictly inside the constant-lambda real-root interval",
        m_pos < m_star < m_disc < m_zero,
        detail=f"m_pos={m_pos:.12f}, m_*={m_star:.12f}, m_disc={m_disc:.12f}, m_0={m_zero:.12f}",
        kind="NUMERIC",
    )

    lower_samples = np.linspace(m_pos + 1.0e-4, m_v - 1.0e-4, 200)
    upper_samples = np.linspace(m_v + 1.0e-4, m_disc - 1.0e-4, 200)

    lower_ok = all(lambda_roots(float(x))[0] < 0.0 < lambda_roots(float(x))[1] for x in lower_samples)
    upper_ok = all(lambda_roots(float(x))[0] > 0.0 and lambda_roots(float(x))[1] > 0.0 for x in upper_samples)

    check(
        "Below m_V there is exactly one positive constant-coupling root",
        lower_ok,
        detail="lambda_- < 0 < lambda_+ on (m_pos, m_V)",
        kind="NUMERIC",
    )
    check(
        "Above m_V and below m_disc there are two positive constant-coupling roots",
        upper_ok,
        detail="0 < lambda_- < lambda_+ on (m_V, m_disc)",
        kind="NUMERIC",
    )
    return m_pos, m_zero, m_star


def part3_monotone_reparameterization(m_pos: float, m_disc: float, m_v: float) -> None:
    print()
    print("=" * 88)
    print("PART 3: the constant-coupling family reparameterizes a continuum")
    print("=" * 88)

    xs_plus = np.linspace(m_pos + 1.0e-4, m_disc - 1.0e-4, 500)
    l_plus = np.array([lambda_roots(float(x))[1] for x in xs_plus])
    d_plus = np.diff(l_plus)

    xs_minus = np.linspace(m_v + 1.0e-4, m_disc - 1.0e-4, 500)
    l_minus = np.array([lambda_roots(float(x))[0] for x in xs_minus])
    d_minus = np.diff(l_minus)

    check(
        "The positive lambda_+(m) branch is strictly decreasing across the whole admissible interval",
        bool(np.all(d_plus < 0.0)),
        detail=f"lambda_+ range=({l_plus[-1]:.12f}, {l_plus[0]:.12f})",
        kind="NUMERIC",
    )
    check(
        "The second branch lambda_-(m) is strictly increasing once it becomes positive",
        bool(np.all(d_minus > 0.0)),
        detail=f"lambda_- range=({l_minus[0]:.12f}, {l_minus[-1]:.12f})",
        kind="NUMERIC",
    )

    other_plus = np.array([other_stationary_root(float(x), float(lam)) for x, lam in zip(xs_plus, l_plus)])
    other_minus = np.array([other_stationary_root(float(x), float(lam)) for x, lam in zip(xs_minus, l_minus)])

    check(
        "For every lambda_+(m), the companion stationary point stays below the positivity threshold",
        bool(np.all(other_plus < m_pos)),
        detail=f"max companion root={float(np.max(other_plus)):.12f}",
        kind="NUMERIC",
    )
    check(
        "For every positive lambda_-(m), the companion stationary point also stays below threshold",
        bool(np.all(other_minus < m_pos)),
        detail=f"max companion root={float(np.max(other_minus)):.12f}",
        kind="NUMERIC",
    )


def part4_physical_point_is_an_interior_member_not_a_selector_endpoint(
    m_pos: float, m_disc: float, m_v: float, m_star: float
) -> None:
    print()
    print("=" * 88)
    print("PART 4: the physical point is one interior member of the family")
    print("=" * 88)

    lam_minus_star, lam_plus_star = lambda_roots(m_star)
    lam_plus_pos = lambda_roots(m_pos)[1]
    lam_plus_v = lambda_roots(m_v)[1]
    lam_plus_disc = lambda_roots(m_disc)[1]

    check(
        "The branch-local physical point still solves the exact delta=2/9 condition",
        abs(delta_offset(m_star) - DELTA_TARGET) < 1.0e-12,
        detail=f"m_*={m_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "Its singlet value is exactly the previously found positive root lambda_*",
        abs(lam_plus_star - 0.5456253116876681) < 1.0e-12 and lam_minus_star < 0.0,
        detail=f"lambda_*={lam_plus_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "lambda_* is an interior value of the decreasing lambda_+(m) family, not an endpoint fixed by branch geometry alone",
        lam_plus_disc < lam_plus_v < lam_plus_star < lam_plus_pos,
        detail=f"lambda_+(m_pos)={lam_plus_pos:.12f}, lambda_+(m_V)={lam_plus_v:.12f}, lambda_+(m_disc)={lam_plus_disc:.12f}",
        kind="NUMERIC",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: scientific interpretation")
    print("=" * 88)
    print("  The fixed-coupling singlet route does not select the Koide point by itself.")
    print("  It gives an exact reparameterization of a whole interval of first-branch")
    print("  stationary points by one or two positive lambda values.")
    print("  So the remaining object on this route is still a microscopic law fixing")
    print("  lambda (equivalently m), not the mere existence of a constant singlet")
    print("  Schur correction.")


def main() -> int:
    m_disc, m_v = part1_exact_stationary_root_formulas()
    m_pos, _m_zero, m_star = part2_branch_interval_structure(m_disc, m_v)
    part3_monotone_reparameterization(m_pos, m_disc, m_v)
    part4_physical_point_is_an_interior_member_not_a_selector_endpoint(m_pos, m_disc, m_v, m_star)
    part5_interpretation()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
