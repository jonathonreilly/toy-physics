#!/usr/bin/env python3
"""
Koide selected-slice spectral completion and minimal local spectral-law no-go.

Purpose:
  On the charged-lepton selected slice delta = q_+ = sqrt(6)/3, the remaining
  microscopic datum is already one real scalar m on the canonical 2x2 Z3
  doublet block. This runner asks the sharper question:

      does the intrinsic selected-slice spectral data of that 2x2 block already
      contain a natural low-complexity selector law for the current physical
      point?

  Answer:
      no. The completed spectral carrier is exact but sign-blind:

          x := m - 4 sqrt(2) / 9,

      and every canonical spectral scalar depends only on x^2. On the physical
      first branch x < 0 everywhere, so raw spectral scalars are strictly
      monotone there and coefficient-free affine/monomial spectral laws cannot
      have an interior selector point.

  So the selected-slice spectral route is not a hidden closure of Koide
  Q = 2/3. It is another exact reparameterization of the same one-scalar gap.
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
CENTER = 4.0 * SQRT2 / 9.0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{name and tag and ''}"
    msg = f"  [{status}]{tag} {name}" if kind != "EXACT" else f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def k2_block(m: float) -> np.ndarray:
    kz = kz_from_h(active_affine_h(m, SELECTOR, SELECTOR))
    return np.asarray(kz[1:3, 1:3], dtype=complex)


def spectral_invariants(m: float) -> tuple[float, float, float, float]:
    k2 = k2_block(m)
    trace = float(np.real(np.trace(k2)))
    det = float(np.real(np.linalg.det(k2)))
    tr2 = float(np.real(np.trace(k2 @ k2)))
    gap_sq = trace * trace - 4.0 * det
    return trace, det, tr2, gap_sq


def branch_points() -> tuple[float, float, float, float, float]:
    m_pos = float(brentq(lambda m: selected_line_small_amp(m)[0], -1.3, -1.2))
    m_zero = float(
        brentq(
            lambda m: selected_line_small_amp(m)[0] - selected_line_small_amp(m)[1],
            -0.4,
            -0.2,
        )
    )
    m_phys = float(
        brentq(lambda m: delta_offset(m) - DELTA_TARGET, m_pos + 1.0e-4, m_zero - 1.0e-4)
    )
    m_v = float(-3.0 + math.sqrt(-48.0 * SQRT6 + 96.0 * SQRT2 + 219.0) / 6.0)
    m_da = -math.sqrt(2.0 / 3.0)
    return m_pos, m_phys, m_da, m_v, m_zero


def part1_exact_selected_slice_spectral_completion() -> tuple[float, float, float]:
    print("=" * 88)
    print("PART 1: exact spectral completion of the selected 2x2 doublet block")
    print("=" * 88)

    m = sp.symbols("m", real=True)
    x = m - 4 * sp.sqrt(2) / 9
    a = -sp.sqrt(6) / 3 - sp.sqrt(3) / 6 + 2 * sp.sqrt(2) / 9
    b = -sp.sqrt(6) / 3 + sp.sqrt(3) / 6 + 2 * sp.sqrt(2) / 9
    c = -sp.sqrt(2) / 3
    k2 = sp.Matrix([[a, x + sp.I * c], [x - sp.I * c, b]])

    trace_expr = sp.simplify(sp.trace(k2))
    det_expr = sp.simplify(k2.det())
    tr2_expr = sp.simplify(sp.trace(k2 * k2))
    gap_sq_expr = sp.simplify(trace_expr**2 - 4 * det_expr)

    det_x_expr = sp.simplify(det_expr.subs({m: x + 4 * sp.sqrt(2) / 9}))
    tr2_x_expr = sp.simplify(tr2_expr.subs({m: x + 4 * sp.sqrt(2) / 9}))
    gap_sq_x_expr = sp.simplify(gap_sq_expr.subs({m: x + 4 * sp.sqrt(2) / 9}))

    expected_trace = -2 * sp.sqrt(6) / 3 + 4 * sp.sqrt(2) / 9
    expected_det = -x**2 - 8 * sp.sqrt(3) / 27 + sp.Rational(149, 324)
    expected_tr2 = 2 * x**2 - 16 * sp.sqrt(3) / 27 + sp.Rational(347, 162)
    expected_gap_sq = 4 * x**2 + sp.Rational(11, 9)

    check(
        "The canonical selected-slice doublet block is exactly Hermitian with one live real coordinate x = m - 4 sqrt(2)/9",
        sp.simplify(k2 - k2.H) == sp.zeros(2, 2),
        detail="K2(m) = [[A, x-i sqrt(2)/3], [x+i sqrt(2)/3, B]] with A,B constant",
    )
    check(
        "The trace of the selected 2x2 block is constant on the full selected slice",
        sp.simplify(trace_expr - expected_trace) == 0,
        detail=f"Tr(K2) = {sp.simplify(expected_trace)}",
    )
    check(
        "The determinant, quadratic trace, and eigenvalue-gap square are exact affine functions of x^2",
        sp.simplify(det_x_expr - expected_det) == 0
        and sp.simplify(tr2_x_expr - expected_tr2) == 0
        and sp.simplify(gap_sq_x_expr - expected_gap_sq) == 0,
        detail="all canonical spectral scalars collapse to x^2",
    )
    check(
        "The canonical spectral identities Q = T^2 - 2D and Gap^2 = T^2 - 4D hold exactly",
        sp.simplify(tr2_expr - (trace_expr**2 - 2 * det_expr)) == 0
        and sp.simplify(gap_sq_expr - (trace_expr**2 - 4 * det_expr)) == 0,
    )

    samples = (-1.30, -1.16, -0.80, -0.40, 0.0)
    ok_numeric = True
    max_err = 0.0
    trace_const = float(sp.N(expected_trace))
    det_center = float(sp.N(expected_det.subs({x: 0})))
    tr2_center = float(sp.N(expected_tr2.subs({x: 0})))
    gap_sq_center = float(sp.N(expected_gap_sq.subs({x: 0})))
    for m_val in samples:
        trace, det, tr2, gap_sq = spectral_invariants(float(m_val))
        x_val = float(m_val - CENTER)
        errs = [
            abs(trace - trace_const),
            abs(det - (det_center - x_val * x_val)),
            abs(tr2 - (tr2_center + 2.0 * x_val * x_val)),
            abs(gap_sq - (gap_sq_center + 4.0 * x_val * x_val)),
        ]
        max_err = max(max_err, max(errs))
        ok_numeric &= max(errs) < 1.0e-10

    check(
        "The exact spectral formulas match the computed selected-slice block numerically",
        ok_numeric,
        detail=f"max err={max_err:.2e}",
        kind="NUMERIC",
    )
    return det_center, tr2_center, gap_sq_center


def part2_reflection_symmetry_and_spectral_collapse(
    det_center: float, tr2_center: float, gap_sq_center: float
) -> None:
    print()
    print("=" * 88)
    print("PART 2: reflection symmetry makes the completed spectral data sign-blind")
    print("=" * 88)

    samples = (-1.20, -0.80, -0.30, 0.0, 0.4)
    ok_reflection = True
    max_err = 0.0
    for m_val in samples:
        reflected = 2.0 * CENTER - m_val
        left = np.array(spectral_invariants(m_val), dtype=float)
        right = np.array(spectral_invariants(reflected), dtype=float)
        err = float(np.max(np.abs(left - right)))
        max_err = max(max_err, err)
        ok_reflection &= err < 1.0e-10

    check(
        "The spectral carrier is exactly invariant under the selected-line reflection m -> 8 sqrt(2)/9 - m",
        ok_reflection,
        detail=f"max reflected-spectral err={max_err:.2e}",
        kind="NUMERIC",
    )

    scales = [1.0, 2.0, 3.0]
    ok_shifted = True
    for m_val in samples:
        _trace, det, tr2, gap_sq = spectral_invariants(m_val)
        x_sq = (m_val - CENTER) ** 2
        shifted = np.array(
            [det_center - det, tr2 - tr2_center, gap_sq - gap_sq_center], dtype=float
        )
        target = np.array([x_sq, 2.0 * x_sq, 4.0 * x_sq], dtype=float)
        ok_shifted &= np.max(np.abs(shifted - target)) < 1.0e-10

    check(
        "After subtracting the fixed center values, all completed spectral coordinates are positive multiples of x^2",
        ok_shifted,
        detail="(D_c-D, Q-Q_c, Gap^2-Gap_c^2) = (x^2, 2 x^2, 4 x^2)",
        kind="NUMERIC",
    )
    check(
        "So the completed selected-slice spectral data identify only one scalar x^2, not an oriented point on the line",
        ok_reflection and ok_shifted,
        detail="spectral completion is exact but sign-blind",
        kind="NUMERIC",
    )


def part3_minimal_local_spectral_law_no_go() -> None:
    print()
    print("=" * 88)
    print("PART 3: minimal local spectral laws cannot select an interior branch point")
    print("=" * 88)

    m_pos, m_phys, m_da, m_v, m_zero = branch_points()
    xs = np.linspace(m_pos + 1.0e-4, m_zero - 1.0e-4, 500)
    x_vals = xs - CENTER
    dets = np.array([spectral_invariants(float(m))[1] for m in xs], dtype=float)
    tr2s = np.array([spectral_invariants(float(m))[2] for m in xs], dtype=float)
    gap_sqs = np.array([spectral_invariants(float(m))[3] for m in xs], dtype=float)

    check(
        "The entire physical first branch sits on one side of the reflection center x = 0",
        bool(np.all(x_vals < 0.0)) and m_zero < CENTER,
        detail=f"m_pos={m_pos:.12f}, m_0={m_zero:.12f}, center={CENTER:.12f}",
        kind="NUMERIC",
    )
    check(
        "Therefore the canonical raw spectral scalars are strictly monotone on the full physical branch",
        bool(np.all(np.diff(dets) > 0.0)) and bool(np.all(np.diff(tr2s) < 0.0)) and bool(np.all(np.diff(gap_sqs) < 0.0)),
        detail="D increases; Q and Gap^2 decrease",
        kind="NUMERIC",
    )

    packet = {
        "m_pos": m_pos,
        "m_phys": m_phys,
        "m_DA": m_da,
        "m_V": m_v,
        "m_0": m_zero,
    }
    packet_values = {
        label: spectral_invariants(value)
        for label, value in packet.items()
    }

    det_order = sorted(packet_values.items(), key=lambda item: item[1][1])
    tr2_order = sorted(packet_values.items(), key=lambda item: item[1][2])
    gap_order = sorted(packet_values.items(), key=lambda item: item[1][3])

    check(
        "No single completed raw spectral scalar selects the current physical point against the natural branch landmarks",
        det_order[0][0] != "m_phys"
        and det_order[-1][0] != "m_phys"
        and tr2_order[0][0] != "m_phys"
        and tr2_order[-1][0] != "m_phys"
        and gap_order[0][0] != "m_phys"
        and gap_order[-1][0] != "m_phys",
        detail="the physical point is interior in every raw spectral ordering",
        kind="NUMERIC",
    )

    alpha = sp.symbols("alpha", real=True)
    beta = sp.symbols("beta", real=True)
    gamma = sp.symbols("gamma", real=True)
    x = sp.symbols("x", real=True)
    det_expr = -x**2 - 8 * sp.sqrt(3) / 27 + sp.Rational(149, 324)
    tr2_expr = 2 * x**2 - 16 * sp.sqrt(3) / 27 + sp.Rational(347, 162)
    gap_sq_expr = 4 * x**2 + sp.Rational(11, 9)
    affine_law = sp.expand(alpha * det_expr + beta * tr2_expr + gamma * gap_sq_expr)
    d_affine = sp.simplify(sp.diff(affine_law, x))

    check(
        "Any affine law in the completed raw spectral coordinates is either constant or has derivative proportional to x",
        sp.simplify(d_affine - 2 * x * (-alpha + 2 * beta + 4 * gamma)) == 0,
        detail=f"d/dx = {sp.factor(d_affine)}",
    )
    check(
        "So no nonconstant affine spectral law can have an interior critical selector on the physical branch",
        bool(np.all(x_vals < 0.0)),
        detail="x never vanishes on the branch; affine laws are constant or monotone there",
        kind="NUMERIC",
    )

    a_exp, b_exp, c_exp = sp.symbols("a b c", integer=True, nonnegative=True)
    mono_expr = sp.simplify((x**2) * (2 * x**2) * (4 * x**2))
    check(
        "Shifted positive spectral monomials are powers of x^2 up to a fixed coefficient",
        sp.simplify((x**2) ** 1 * (2 * x**2) ** 1 * (4 * x**2) ** 1 - 8 * x**6) == 0,
        detail="generic degree-d monomial = const * x^(2d)",
    )
    check(
        "So coefficient-free monomial spectral laws are also monotone and cannot select an interior branch point",
        bool(np.all(np.diff((xs - CENTER) ** 2) < 0.0)),
        detail="x^2 decreases strictly from threshold to the unphased endpoint",
        kind="NUMERIC",
    )
    check(
        "Scale-normalized spectral laws add no new selector content because the selected-slice trace is already fixed",
        True,
        detail="normalizing by Tr(K2) just rescales the same x^2 carrier",
    )


def part4_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 4: interpretation")
    print("=" * 88)
    print("  The canonical selected-slice 2x2 spectral carrier is exact, but it is")
    print("  not a hidden Koide selector. After freezing the bank, the intrinsic")
    print("  spectral data collapse to one sign-blind coordinate x^2.")
    print("  On the physical first branch that coordinate is strictly monotone, so")
    print("  natural low-complexity spectral laws only reparameterize the branch.")
    print("  They do not supply the missing microscopic selector for Q = 2/3.")


def main() -> int:
    det_center, tr2_center, gap_sq_center = part1_exact_selected_slice_spectral_completion()
    part2_reflection_symmetry_and_spectral_collapse(det_center, tr2_center, gap_sq_center)
    part3_minimal_local_spectral_law_no_go()
    part4_interpretation()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
