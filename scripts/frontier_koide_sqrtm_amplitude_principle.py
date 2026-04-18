#!/usr/bin/env python3
"""
Koide sqrt(m) amplitude-principle runner
=======================================

STATUS: exact narrowing of the P1 ambiguity on the charged-lepton Koide lane

Purpose:
  Replace the vague identification "lambda = sqrt(m)" with a concrete internal
  candidate route:

      positive quadratic parent M  --->  one-leg amplitude Y = M^(1/2)

  where eig(Y) = sqrt(eig(M)).

Safe outcome:
  This runner does NOT derive the charged-lepton parent M. It proves that if
  such a positive C_3-covariant parent exists, then the sqrt(m) spectral
  readout follows exactly and preserves the circulant C_3 structure.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


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


def build_fourier():
    w = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    F = sp.Matrix(
        [
            [1, 1, 1],
            [1, w, w**2],
            [1, w**2, w],
        ]
    ) / sp.sqrt(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    return w, F, C


def koide_Q(masses: np.ndarray) -> float:
    masses = np.asarray(masses, dtype=float)
    return float(np.sum(masses) / np.sum(np.sqrt(masses)) ** 2)


def c3_ratio(v: np.ndarray) -> float:
    w = complex(-0.5, math.sqrt(3) / 2)
    a0 = (v[0] + v[1] + v[2]) / math.sqrt(3.0)
    z = (v[0] + np.conjugate(w) * v[1] + w * v[2]) / math.sqrt(3.0)
    return float((a0 * a0) / (2 * abs(z) ** 2))


def part1_convention_and_lsz():
    print("=" * 88)
    print("PART 1: square-root dictionary already present in the repo")
    print("=" * 88)

    zpsi, zphi, za = sp.symbols("Z_psi Z_phi Z_A", positive=True)
    amp_y = sp.sqrt(zpsi) * sp.sqrt(zphi) * sp.sqrt(zpsi)
    amp_g = sp.sqrt(zpsi) * sp.sqrt(za) * sp.sqrt(zpsi)
    ratio = sp.simplify(amp_y / amp_g)

    check(
        "LSZ ratio leaves one sqrt(Z_phi) factor per scalar external leg",
        sp.simplify(ratio - sp.sqrt(zphi / za)) == 0,
        detail=f"ratio={ratio}",
    )
    check(
        "A one-leg amplitude factor squares back to the quadratic residue",
        sp.simplify(sp.sqrt(zphi) ** 2 - zphi) == 0,
    )

    me, mmu, mtau = sp.symbols("m_e m_mu m_tau", positive=True)
    w = sp.Matrix([me**2, mmu**2, mtau**2])
    sqrt_w = sp.Matrix([sp.sqrt(w[i]) for i in range(3)])
    check(
        "Convention-B square root of the quadratic weights recovers the linear masses",
        sp.simplify(sqrt_w - sp.Matrix([me, mmu, mtau])) == sp.zeros(3, 1),
        detail="sqrt((m_e^2,m_mu^2,m_tau^2)) = (m_e,m_mu,m_tau)",
    )


def part2_positive_c3_parent():
    print()
    print("=" * 88)
    print("PART 2: positive C_3 parent -> positive C_3 square root")
    print("=" * 88)

    _, F, C = build_fourier()
    s0, s1, s2 = sp.symbols("s0 s1 s2", positive=True, real=True)

    Y = sp.simplify(F * sp.diag(s0, s1, s2) * F.H)
    M = sp.simplify(F * sp.diag(s0**2, s1**2, s2**2) * F.H)
    Cinv = C.T

    check(
        "Positive amplitude operator Y is Hermitian",
        sp.simplify(Y - Y.H) == sp.zeros(3),
    )
    check(
        "Quadratic parent M = Y^2 exactly",
        sp.simplify(Y * Y - M) == sp.zeros(3),
    )
    check(
        "Parent M commutes with the retained C_3 shift",
        sp.simplify(C * M * Cinv - M) == sp.zeros(3),
    )
    check(
        "Principal square root Y also commutes with the retained C_3 shift",
        sp.simplify(C * Y * Cinv - Y) == sp.zeros(3),
    )
    check(
        "Fourier basis diagonalizes Y with eigenvalues (sqrt masses)",
        sp.simplify(F.H * Y * F - sp.diag(s0, s1, s2)) == sp.zeros(3),
    )
    check(
        "Fourier basis diagonalizes M with eigenvalues (masses)",
        sp.simplify(F.H * M * F - sp.diag(s0**2, s1**2, s2**2)) == sp.zeros(3),
    )


def part3_observed_lepton_amplitude():
    print()
    print("=" * 88)
    print("PART 3: observed charged-lepton parent -> sqrt(m) amplitude vector")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    q = koide_Q(masses)
    ratio = c3_ratio(amps)

    check(
        "Observed charged-lepton Koide Q is 2/3 to PDG precision",
        abs(q - 2 / 3) < 1e-5,
        detail=f"Q={q:.10f}",
        kind="NUMERIC",
    )
    check(
        "Observed sqrt(m) amplitude vector satisfies a_0^2 = 2|z|^2 to 1e-4",
        abs(ratio - 1.0) < 1e-4,
        detail=f"ratio={ratio:.10f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_convention_and_lsz()
    part2_positive_c3_parent()
    part3_observed_lepton_amplitude()

    print()
    print("Interpretation:")
    print("  The repo already uses square roots to pass from positive quadratic")
    print("  parents to linear one-leg amplitudes. On the Koide lane, this means")
    print("  the sharp P1 blocker is not 'why sqrt(m)?' in the abstract, but")
    print("  'which positive C_3-covariant parent M has principal square root")
    print("  carrying the charged-lepton spectral amplitudes?'")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
