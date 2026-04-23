#!/usr/bin/env python3
"""Audit the time-locked gravitational transfer-operator lane honestly.

This lane does not claim exact Planck closure. It sharpens the surviving
boundary route into one theorem class:

  - derived time gives one exact clock and fixes a_s = c a_t;
  - any surviving same-surface boundary transfer law should therefore be a
    one-clock semigroup T_grav(tau) = exp(tau G_Sigma);
  - if it is induced from the admitted 3+1 gravity carrier, the effective
    boundary generator should arise from a collective boundary Schur
    complement of a positive one-clock completion of the global operator;
  - exact conventional Planck on this route becomes the additive target
    sup spec(G_Sigma) = 1/4.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
BOUNDARY = ROOT / "docs/PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md"
LOCAL = ROOT / "docs/PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md"
GLOBAL = ROOT / "docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md"
TENSOR = ROOT / "docs/S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def spectral_radius(matrix: sp.Matrix) -> sp.Expr:
    vals = matrix.eigenvals()
    return max(vals, key=lambda expr: abs(complex(sp.N(expr, 50))))


def schur_complement(m_bb: sp.Matrix, m_bi: sp.Matrix, m_ii: sp.Matrix) -> sp.Matrix:
    return sp.simplify(m_bb - m_bi * m_ii.inv() * m_bi.T)


def main() -> int:
    note = normalized(NOTE)
    timelock_note = normalized(TIMELOCK)
    boundary_note = normalized(BOUNDARY)
    local_note = normalized(LOCAL)
    global_note = normalized(GLOBAL)
    tensor_note = normalized(TENSOR)

    n_pass = 0
    n_fail = 0

    print("Planck time-locked gravitational transfer-operator lane audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY EVIDENCE")
    p = check(
        "time-lock note still fixes a_s = c a_t exactly",
        "a_s = c a_t" in timelock_note and "beta = 1" in timelock_note,
        "the transfer-operator lane starts from the exact locked spacetime pair, not a free anisotropy",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "boundary note still identifies the surviving target as rho(T_grav) = e^(1/4)",
        "rho(t_grav) = e^(1/4)" in boundary_note,
        "the new lane should refine the surviving target rather than replace it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "local boundary-density note still rules out local geometry and naive cell counting",
        "not a local geometric density" in local_note
        and "not naive integer cell counting" in local_note,
        "the surviving transfer class must remain genuinely collective",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "global 3+1 gravity carrier is still available on the branch",
        "k_gr(d) = h_d ⊗ lambda_r" in global_note
        and "exact route-2 spacetime carrier" in tensor_note,
        "the candidate boundary transfer class is induced from the admitted gravity side",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT TIME-LOCK RECASTS THE TARGET AS A GENERATOR PROBLEM")
    retained_ratio = sp.Integer(2) / sp.sqrt(3)
    beta = sp.simplify(3 * retained_ratio**2 - 3)
    p = check(
        "the retained exact scalar ratio still forces beta = 1",
        beta == 1,
        "time-lock leaves one exact clock step and removes the hidden space/time calibration",
    )
    n_pass += int(p)
    n_fail += int(not p)

    projector = sp.Matrix(
        [[sp.Rational(1, 2), sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Rational(1, 2)]]
    )
    generator = sp.Rational(1, 4) * projector
    transfer_one = sp.eye(2) + (sp.exp(sp.Rational(1, 4)) - 1) * projector
    transfer_two = sp.eye(2) + (sp.exp(sp.Rational(1, 2)) - 1) * projector
    p = check(
        "one-clock semigroup law converts rho(T) = exp(1/4) into sup spec(G) = 1/4",
        spectral_radius(generator) == sp.Rational(1, 4)
        and sp.simplify(spectral_radius(transfer_one) - sp.exp(sp.Rational(1, 4))) == 0
        and sp.simplify(transfer_one * transfer_one - transfer_two) == sp.zeros(2),
        (
            "for the rank-one witness G = (1/4) P, T(1) = exp(G) has spectral radius exp(1/4) "
            "and T(2) = T(1)^2 exactly"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: BULK ELIMINATION PRODUCES A GENUINELY COLLECTIVE BOUNDARY OPERATOR")
    m_bb = sp.Matrix([[2, 0], [0, 2]])
    m_bi = sp.Matrix([[1, 0], [0, 1]])
    m_ii = sp.Matrix([[2, 1], [1, 2]])
    l_sigma = schur_complement(m_bb, m_bi, m_ii)

    expected = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    p = check(
        "the exact Schur witness matches the stated collective boundary operator",
        sp.simplify(l_sigma - expected) == sp.zeros(2),
        "bulk elimination creates the exact rational witness L_Sigma = [[4/3,1/3],[1/3,4/3]]",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "a diagonal local boundary block becomes nonlocal after exact bulk elimination",
        m_bb[0, 1] == 0 and l_sigma[0, 1] != 0,
        "the Schur term M_BI M_II^(-1) M_IB creates collective boundary coupling",
    )
    n_pass += int(p)
    n_fail += int(not p)

    evals = sorted(sp.Matrix(l_sigma).eigenvals().keys(), key=lambda x: float(sp.N(x)))
    p = check(
        "the Schur witness remains positive definite after bulk elimination",
        evals == [1, sp.Rational(5, 3)],
        "the collective boundary reduction can stay positive while ceasing to be local",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE HONESTY")
    p = check(
        "the note states the surviving class as a one-clock boundary semigroup",
        "t_grav(tau) = exp(tau g_sigma)" in note
        and "one-clock semigroup" in note,
        "time-lock should appear as a structural constraint, not just a comment",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the boundary generator as a Schur-complement reduction",
        "schur-complement reduction" in note and "l_sigma(d)" in note,
        "the surviving class should be induced from the same-surface gravity carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the additive pressure target sup spec(G_Sigma) = 1/4",
        "sup spec(g_sigma) = 1/4" in note,
        "the transcendental Perron target is recast as an additive generator theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim exact closure",
        "does **not** prove" in note and "it gives the sharper target class only" in note,
        "this lane should remain a candidate-class theorem rather than a fake close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Time-lock narrows the surviving boundary route to a specific class: "
        "a one-clock collective boundary semigroup whose generator is a "
        "same-surface gravitational Schur reduction. Exact conventional "
        "Planck would then be the additive pressure theorem sup spec(G_Sigma) = 1/4."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
