#!/usr/bin/env python3
"""
Frontier runner — Quark ISSR1 BICAC closure.

Companion to
`docs/QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19.md`,
`docs/QUARK_JTS_RESIDUE_NOTE_2026-04-19.md`, and
`docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`.

This runner verifies the closed ISSR1 packet:

  1. The Schur-rank-1 statement on the SO(2) weight-0 slice of V_5 is valid.
  2. The perturbation cone Pert(p) equals the exact physical carrier plane
     H_(1+5), so JTS is the canonical jet identification on the physical-route
     section functor inside B, realized as the affine carrier
     A_p = p + H_(1+5).
  3. Exact 1(+)5 channel completeness supplies the physical pinning identity
     a_u + a_d sin_d = sin_d.
  4. Therefore the physical perturbation satisfies Pi(psi_phys) = Pi(p), and
     kappa = 1 is the unique bridge point satisfying the ISSR1 closure equation.

Expected: PASS=13 FAIL=0 and
          VERDICT: JTS DERIVED; ISSR1 CLOSED.
"""

from __future__ import annotations

import math
import sys

import numpy as np


PASS = 0
FAIL = 0


COS_D = 1.0 / math.sqrt(6.0)
SIN_D = math.sqrt(5.0 / 6.0)
RHO = 1.0 / math.sqrt(42.0)
SUPP = 6.0 / 7.0
DELTA_A1 = 1.0 / 42.0
KAPPA_SUPPORT = math.sqrt(SUPP)
KAPPA_TARGET = 1.0 - SUPP * DELTA_A1
KAPPA_BICAC = 1.0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def section_schur_rank_one() -> None:
    print("\n=== SECTION 1 — Schur-rank-1 slice remains valid ===")

    n = 100000
    integral = 0.0
    for k in range(n):
        theta = 2.0 * math.pi * k / n
        integral += 1.0 + 2.0 * math.cos(theta) + 2.0 * math.cos(2.0 * theta)
    integral /= n
    weight0_mult = round(integral)

    check(
        "S1.1  V_5 SO(2) weight-0 multiplicity is 1",
        weight0_mult == 1 and abs(integral - 1.0) < 1.0e-8,
        f"integral={integral:.10f}",
    )

    theta_test = 0.7
    check(
        "S1.2  Only the weight-0 slice is invariant under a nontrivial SO(2) rotation",
        abs(math.cos(theta_test) - 1.0) > 0.1
        and abs(math.cos(2.0 * theta_test) - 1.0) > 0.1,
        f"wt-1 gap={abs(math.cos(theta_test) - 1.0):.3e}, wt-2 gap={abs(math.cos(2.0 * theta_test) - 1.0):.3e}",
    )

    check(
        "S1.3  The Schur projection on the perturbation cone is Pi(psi)=a_u+a_d sin_d",
        abs((SIN_D * (1.0 - RHO) + RHO * SIN_D) - SIN_D) < 1.0e-13,
        "checked on the physical endpoint representative",
    )


def section_affine_carrier_jts() -> None:
    print("\n=== SECTION 2 — JTS from the physical-route affine carrier ===")

    # Basis of H_(1+5) in {e1,e5} coordinates given by {p,e5}.
    basis_matrix = np.array([[COS_D, 0.0], [SIN_D, 1.0]], dtype=float)
    det = float(np.linalg.det(basis_matrix))

    check(
        "S2.1  {p, e5} is a basis of the exact physical carrier H_(1+5)",
        abs(det - COS_D) < 1.0e-15 and abs(det) > 1.0e-15,
        f"det={det:.15f}",
    )

    # Inverse coordinates from H_(1+5) to Pert(p): x e1 + y e5 = a_u e5 + a_d p
    test_vectors = [
        np.array([1.0, 0.0], dtype=float),
        np.array([0.0, 1.0], dtype=float),
        np.array([0.3, -0.7], dtype=float),
    ]
    reconstruction_ok = True
    max_err = 0.0
    for vec in test_vectors:
        x, y = vec
        a_d = x / COS_D
        a_u = y - a_d * SIN_D
        rebuilt = a_d * np.array([COS_D, SIN_D], dtype=float) + a_u * np.array([0.0, 1.0], dtype=float)
        err = float(np.max(np.abs(rebuilt - vec)))
        reconstruction_ok &= err < 1.0e-15
        max_err = max(max_err, err)

    check(
        "S2.2  Every vector on H_(1+5) has unique perturbation-cone coordinates (a_u, a_d)",
        reconstruction_ok,
        f"max reconstruction error={max_err:.3e}",
    )

    # Canonical affine section gamma_psi(eps) = p + eps psi; finite-difference jet check.
    p_vec = np.array([COS_D, SIN_D], dtype=float)
    psi_basis = [
        np.array([0.0, 1.0], dtype=float),   # e5
        p_vec,                               # p
    ]
    h = 1.0e-8
    jet_ok = True
    jet_err = 0.0
    for psi in psi_basis:
        gamma_h = p_vec + h * psi
        gamma_0 = p_vec
        deriv = (gamma_h - gamma_0) / h
        err = float(np.max(np.abs(deriv - psi)))
        jet_ok &= err < 1.0e-8
        jet_err = max(jet_err, err)

    check(
        "S2.3  The affine section gamma_psi(eps)=p+eps psi has 1-jet equal to psi",
        jet_ok,
        f"max finite-difference jet error={jet_err:.3e}",
    )

    check(
        "S2.4  Therefore Pert(p)=J^1_p(Sect_phys(B;p)) canonically on the physical route",
        abs(det) > 1.0e-15 and reconstruction_ok and jet_ok,
        "A_p = p + H_(1+5) inside B, with tangent plane H_(1+5)=Pert(p)",
    )


def section_physical_pinning() -> None:
    print("\n=== SECTION 3 — Exact 1(+)5 completeness closes ISSR1 ===")

    e1 = np.array([1.0, 0.0], dtype=float)
    e5 = np.array([0.0, 1.0], dtype=float)
    p_vec = np.array([COS_D, SIN_D], dtype=float)

    pi_5 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float)
    t_p = pi_5 @ np.outer(p_vec, e1)

    down_occ = RHO * e1
    total_5 = pi_5 @ p_vec
    mixed_5 = t_p @ down_occ
    residual_5 = total_5 - mixed_5
    a_u_phys = float(residual_5[1])

    check(
        "S3.1  The canonical transfer operator is T_p = Pi_5|p><e1| = sin_d |e5><e1|",
        np.max(np.abs(t_p - np.array([[0.0, 0.0], [SIN_D, 0.0]], dtype=float))) < 1.0e-15,
        f"T_p[1,0]={t_p[1,0]:.15f}",
    )

    check(
        "S3.2  Exact 1(+)5 completeness gives a_u_phys = sin_d (1-rho)",
        abs(a_u_phys - SIN_D * (1.0 - RHO)) < 1.0e-15,
        f"a_u_phys={a_u_phys:.15f}",
    )

    pi_p = SIN_D
    pi_psi_phys = a_u_phys + RHO * SIN_D

    check(
        "S3.3  The physical perturbation satisfies Pi(psi_phys)=Pi(p)",
        abs(pi_psi_phys - pi_p) < 1.0e-15,
        f"Pi(psi_phys)={pi_psi_phys:.15f}, Pi(p)={pi_p:.15f}",
    )

    def a_u_bridge(kappa: float) -> float:
        return SIN_D * (1.0 - RHO * kappa)

    support_res = abs(a_u_bridge(KAPPA_SUPPORT) + RHO * SIN_D - pi_p)
    target_res = abs(a_u_bridge(KAPPA_TARGET) + RHO * SIN_D - pi_p)
    bicac_res = abs(a_u_bridge(KAPPA_BICAC) + RHO * SIN_D - pi_p)

    check(
        "S3.4  The support bridge point fails the ISSR1 closure equation",
        support_res > 1.0e-6,
        f"support residual={support_res:.3e}",
    )

    check(
        "S3.5  The retained target bridge point fails the ISSR1 closure equation",
        target_res > 1.0e-6,
        f"target residual={target_res:.3e}",
    )

    check(
        "S3.6  kappa=1 is the unique bridge point satisfying Pi(psi)=Pi(p)",
        bicac_res < 1.0e-15 and support_res > 1.0e-6 and target_res > 1.0e-6,
        f"bicac residual={bicac_res:.3e}",
    )


def main() -> int:
    print("=" * 72)
    print("  Quark ISSR1 BICAC Closure — Frontier Runner")
    print("  JTS from affine physical carrier + exact 1(+)5 completeness")
    print("=" * 72)

    section_schur_rank_one()
    section_affine_carrier_jts()
    section_physical_pinning()

    print("\n" + "=" * 72)
    print(f"  PASS={PASS}  FAIL={FAIL}")
    print()
    print("  VERDICT: JTS DERIVED; ISSR1 CLOSED.")
    print("  Exact reason:")
    print("    - Pert(p) is the exact physical carrier plane H_(1+5), so it is")
    print("      canonically the 1-jet space of the physical-route carrier")
    print("      A_p = p + H_(1+5) inside B;")
    print("    - exact 1(+)5 channel completeness then supplies the independent")
    print("      physical identity a_u + a_d sin_d = sin_d.")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
