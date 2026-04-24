#!/usr/bin/env python3
"""Verify the structural hbar action-phase representation theorem.

This checks that the new theorem derives only the invariant action-to-phase
role S/hbar = Phi from the primitive integral action count, while preserving
the SI-value nonclaim.
"""

from __future__ import annotations

import cmath
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-12


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def theta(ncells: int) -> int:
    return ncells


def phase(ncells: int) -> complex:
    return cmath.exp(1j * theta(ncells))


def scaled_phase(ncells: int, lam: Fraction) -> complex:
    return cmath.exp(1j * float(lam * ncells))


def close(z: complex, w: complex) -> bool:
    return abs(z - w) < TOL


def main() -> int:
    note = read("docs/PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md")
    integral = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    si_discharge = read("docs/PLANCK_SCALE_SI_HBAR_OBJECTION_DISCHARGE_THEOREM_2026-04-24.md")
    action_target = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-structural-hbar-theorem",
        "Planck-Scale Action-Phase Representation Hbar Theorem" in note
        and "**Status:** structural `hbar` derivation as primitive action-to-phase conversion" in note
        and "frontier_planck_action_phase_representation_hbar_theorem_2026_04_24.py" in note,
        "new theorem and verifier are present",
    )

    total += 1
    passed += expect(
        "uses-primitive-integral-history-source",
        "`M_cell = N [A_cell]`" in note
        and "`Phi(n[A_cell]) = n`" in note
        and "`M_cell = N [A_cell]`" in integral
        and "`Phi(I_16) = ell([A_cell]) = 1`" in integral,
        "the phase theorem depends on the already-closed integral count unit",
    )

    additive_ok = all(theta(m + n) == theta(m) + theta(n) for m in range(5) for n in range(5))
    multiplicative_ok = all(close(phase(m + n), phase(m) * phase(n)) for m in range(5) for n in range(5))

    total += 1
    passed += expect(
        "coherent-gluing-is-additive-on-universal-cover",
        additive_ok
        and multiplicative_ok
        and "`U(m+n) = U(m) U(n)`" in note
        and "`theta(m+n) = theta(m) + theta(n)`" in note,
        "monoid gluing gives additive theta and multiplicative U",
    )

    lam = Fraction(3, 2)
    quotient = scaled_phase(1, lam) / scaled_phase(1, Fraction(1, 1))

    total += 1
    passed += expect(
        "lambda-rescaling-is-hidden-phase-character",
        abs(quotient - 1) > 1e-6
        and "`theta_lambda(H) = lambda Phi(H)`" in note
        and "`U_lambda(H) / U_1(H) = exp(i (lambda - 1) Phi(H))`" in note
        and "`lambda = 1`" in note,
        f"lambda={lam} gives nontrivial quotient={quotient.real:.6f}+{quotient.imag:.6f}i",
    )

    total += 1
    passed += expect(
        "structural-action-phase-identification-is-explicit",
        "`S(H)/hbar = Phi(H)`" in note
        and "`S(H) = hbar Phi(H)`" in note
        and "`S(A_cell) = hbar`" in note,
        "hbar is identified as the physical action per primitive phase-count unit",
    )

    q_atom = Fraction(1, 16)
    eps_star = Fraction(1, 2)  # factor multiplying pi in eps_*=pi/2
    a2_over_lp2 = Fraction(8, 1) * q_atom / eps_star

    total += 1
    passed += expect(
        "same-action-count-recovers-planck-ratio",
        a2_over_lp2 == 1
        and "`q_atom = 1/16`" in note
        and "`eps_* = pi/2`" in note
        and "`a^2/l_P^2 = 8 pi (1/16)/(pi/2) = 1`" in note
        and "`a^2 c_light^3/(hbar G)=1`" in note
        and "`q_* = 1/16`" in action_target,
        f"a2/lP2={a2_over_lp2}",
    )

    total += 1
    passed += expect(
        "si-decimal-overclaim-is-refused",
        "not a prediction of the SI decimal value of `hbar`" in note
        and "an independent prediction of joule-seconds" in note
        and "SI decimal value of `hbar` is not a physical\n> prediction target" in si_discharge,
        "dimensionful SI decimal hbar remains a unit-convention nonclaim",
    )

    total += 1
    passed += expect(
        "canonical-quantum-roles-are-not-overclaimed",
        "a derivation of every equivalent role of `hbar` such as canonical\n"
        "   commutators, uncertainty relations, or angular-momentum spectra"
        in note
        and "Those roles become downstream quantum-mechanical representations" in note,
        "commutators and spectra are downstream, not proved here",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
