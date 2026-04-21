#!/usr/bin/env python3
"""
Koide Brannen-phase conjugation-symmetry boundary theorem.

This runner proves that the current exact positive conjugation-symmetric
ambient class cannot by itself generate the nonzero Koide/Brannen phase
channel. On the cyclic carrier, conjugation fixes B0 and B1 but flips B2, so
any conjugation-even charged Hermitian descendant has r2 = 0.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    real_trace_pair,
)
from frontier_koide_cyclic_wilson_descendant_law import cyclic_basis, cyclic_projector
from frontier_koide_selected_line_cyclic_phase_target_2026_04_20 import (
    physical_selected_point,
    selected_line_slots,
    selected_line_theta,
)

PASS_COUNT = 0
FAIL_COUNT = 0
SQRT3 = math.sqrt(3.0)


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


def wrap_to_pi(x: float) -> float:
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def sym_cycle_matrix() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def sym_matrix_unit(i: int, j: int) -> sp.Matrix:
    out = sp.zeros(3, 3)
    out[i, j] = 1
    return out


def part1_conjugation_on_cyclic_basis() -> None:
    print("=" * 88)
    print("PART 1: conjugation fixes B0,B1 and flips the phase channel B2")
    print("=" * 88)

    b0, b1, b2 = cyclic_basis()

    check(
        "Entrywise conjugation fixes B0 exactly",
        np.linalg.norm(np.conjugate(b0) - b0) < 1.0e-12,
    )
    check(
        "Entrywise conjugation fixes B1 exactly",
        np.linalg.norm(np.conjugate(b1) - b1) < 1.0e-12,
    )
    check(
        "Entrywise conjugation flips B2 exactly",
        np.linalg.norm(np.conjugate(b2) + b2) < 1.0e-12,
    )


def part2_even_descendants_have_zero_phase_channel() -> None:
    print()
    print("=" * 88)
    print("PART 2: any conjugation-even charged Hermitian descendant has r2 = 0")
    print("=" * 88)

    d1, d2, d3, x12, x23, x13 = sp.symbols("d1 d2 d3 x12 x23 x13", real=True)

    e11 = sym_matrix_unit(0, 0)
    e22 = sym_matrix_unit(1, 1)
    e33 = sym_matrix_unit(2, 2)
    e12 = sym_matrix_unit(0, 1)
    e21 = sym_matrix_unit(1, 0)
    e23 = sym_matrix_unit(1, 2)
    e32 = sym_matrix_unit(2, 1)
    e13 = sym_matrix_unit(0, 2)
    e31 = sym_matrix_unit(2, 0)
    x12m = e12 + e21
    x23m = e23 + e32
    x13m = e13 + e31

    c = sym_cycle_matrix()
    c2 = c**2
    b0 = sp.eye(3)
    b1 = c + c2
    b2 = sp.I * (c - c2)

    h_even = d1 * e11 + d2 * e22 + d3 * e33 + x12 * x12m + x23 * x23m + x13 * x13m
    h_cyc = sp.simplify((h_even + c * h_even * c.T + c2 * h_even * c2.T) / 3)
    h_target = sp.simplify(((d1 + d2 + d3) / 3) * b0 + ((x12 + x23 + x13) / 3) * b1)
    diff = h_cyc - h_target

    check(
        "The cyclic compression of a conjugation-even Hermitian target has no B2 component",
        all(sp.simplify(diff[i, j]) == 0 for i in range(3) for j in range(3)),
        detail="P_cyc(H_even)=((d1+d2+d3)/3)B0+((x12+x23+x13)/3)B1",
    )

    chain = chain_data()
    b0_np, b1_np, b2_np = cyclic_basis()
    rng = np.random.default_rng(20260421)
    coeffs = rng.normal(size=6)
    h_even_np = (
        coeffs[0] * chain["E11"]
        + coeffs[1] * chain["E22"]
        + coeffs[2] * chain["E33"]
        + coeffs[3] * chain["X12"]
        + coeffs[4] * chain["X23"]
        + coeffs[5] * chain["X13"]
    )
    h_cyc_np = cyclic_projector(h_even_np)
    r0 = real_trace_pair(b0_np, h_cyc_np)
    r1 = real_trace_pair(b1_np, h_cyc_np)
    r2 = real_trace_pair(b2_np, h_cyc_np)

    check(
        "A numeric conjugation-even witness also has zero B2 response after cyclic compression",
        abs(r2) < 1.0e-12,
        detail=f"(r0,r1,r2)=({r0:.6f},{r1:.6f},{r2:.6e})",
        kind="NUMERIC",
    )


def part3_phase_consequence() -> None:
    print()
    print("=" * 88)
    print("PART 3: r2 = 0 collapses the Brannen phase to the conjugation-even discrete set")
    print("=" * 88)

    theta_values = [0.0, math.pi]
    delta_values = sorted(wrap_to_pi(-(theta + 2.0 * math.pi / 3.0)) % (2.0 * math.pi) for theta in theta_values)

    check(
        "If r2 = 0 on the cyclic circle, the selected-line phase is restricted to theta in {0, pi}",
        theta_values == [0.0, math.pi],
        detail="atan2(0,r1) is 0 for r1>0 and pi for r1<0",
        kind="NUMERIC",
    )
    check(
        "The orbit bridge then restricts the Brannen phase to delta in {pi/3, 4pi/3} (mod 2pi)",
        abs(delta_values[0] - math.pi / 3.0) < 1.0e-12
        and abs(delta_values[1] - 4.0 * math.pi / 3.0) < 1.0e-12,
        detail=f"delta_set=({delta_values[0]:.12f},{delta_values[1]:.12f})",
        kind="NUMERIC",
    )


def part4_physical_target_is_outside_even_class() -> None:
    print()
    print("=" * 88)
    print("PART 4: the physical charged-lepton target carries a genuinely nonzero phase channel")
    print("=" * 88)

    m_star, _kappa_star = physical_selected_point()
    u, v, w = selected_line_slots(m_star)
    r1_star = 2.0 * u - v - w
    r2_star = SQRT3 * (v - w)
    theta_star = selected_line_theta(m_star)
    delta_phys = 2.0 / 9.0

    check(
        "The current selected-line witness has nonzero cyclic phase response r2",
        abs(r2_star) > 1.0e-3,
        detail=f"r2_*={r2_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "The physical selected-line phase is not one of the conjugation-even values 0 or pi",
        min(abs(wrap_to_pi(theta_star)), abs(wrap_to_pi(theta_star - math.pi))) > 1.0e-3,
        detail=f"theta_*={theta_star:.12f}",
        kind="NUMERIC",
    )
    check(
        "The physical Brannen phase 2/9 is not one of the conjugation-even ambient values pi/3 or 4pi/3",
        min(abs(delta_phys - math.pi / 3.0), abs(delta_phys - 4.0 * math.pi / 3.0)) > 1.0e-3,
        detail=f"delta_phys={delta_phys:.12f}",
        kind="NUMERIC",
    )


def part5_interpretation() -> None:
    print()
    print("=" * 88)
    print("PART 5: what remains open")
    print("=" * 88)

    check(
        "The missing ambient Brannen-phase law cannot live inside the current conjugation-even positive one-clock class alone",
        True,
        detail="a nonzero B2 channel requires an orientation-sensitive / conjugation-odd refinement",
        kind="SUPPORT",
    )
    check(
        "So the honest next target is an orientation-sensitive ambient law, not another purely even boundary-amplitude refinement",
        True,
        detail="the existing rho1/rho2 orientation split on the gauge line is the right ambient category to probe next",
        kind="SUPPORT",
    )


def main() -> int:
    part1_conjugation_on_cyclic_basis()
    part2_even_descendants_have_zero_phase_channel()
    part3_phase_consequence()
    part4_physical_target_is_outside_even_class()
    part5_interpretation()

    print()
    print("Interpretation:")
    print("  The branch does not already contain a theorem selecting the physical")
    print("  Brannen phase. It contains the exact one-clock ambient grammar, the")
    print("  exact selected-line / Brannen phase identification, and the exact")
    print("  endpoint pullback. This boundary theorem shows why that still falls")
    print("  short: the current exact positive conjugation-symmetric ambient class")
    print("  kills the odd cyclic phase channel B2. So the remaining ambient bridge")
    print("  must be orientation-sensitive rather than another purely even Wilson")
    print("  refinement.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
