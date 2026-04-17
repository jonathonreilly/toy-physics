#!/usr/bin/env python3
"""
Neutrino Bosonic Normalization Theorem
======================================

STATUS: EXACT normalization selector on the retained local Higgs family

Purpose:
  Resolve the remaining 1 versus 1/sqrt(2) ambiguity in the direct neutrino
  bridge normalization by importing the retained mainline observable-principle
  toolkit.

Combined retained inputs:

  1. The local post-EWSB scalar Higgs family is

       M(phi) = sum_i phi_i Gamma_i

     and the axis-selected bridge is Gamma_1.

  2. Physical local scalar observables are source-response coefficients of the
     unique additive CPT-even generator

       W[J] = log|det(D+J)| - log|det D|.

Exact conclusion:

  - the raw chiral bridge Y = P_R Gamma_1 P_L is nilpotent
  - on a scalar local baseline m I, Y has identically zero bosonic
    log|det|-response
  - its retained scalar Hermitian completion is exactly

        Y + Y^dagger = Gamma_1

  - Gamma_1 has nontrivial even source-response
  - therefore the physical normalization surface is the full bosonic
    Gamma_1 family, not the active chiral bridge by itself
  - in the branch's canonical trace normalization, that selects the full-space
    bridge ratio

        y_nu^(0) / g_weak = 1 / sqrt(2)

    rather than the active-space ratio 1

This closes the base-normalization ambiguity. The downstream retained local
Schur theorem now closes the exact second-order coefficient on `T_1`; the live
remaining blocker is the Majorana / `Z_3` activation law.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


I2 = np.eye(2, dtype=complex)
I16 = np.eye(16, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
G_SPATIAL = [G1, G2, G3]
GAMMA5_4D = G0 @ G1 @ G2 @ G3
P_L = (I16 + GAMMA5_4D) / 2.0
P_R = (I16 - GAMMA5_4D) / 2.0

Y = P_R @ G1 @ P_L
Y_DAG = Y.conj().T
SCALAR_COMPLETION = Y + Y_DAG
PSEUDOSCALAR_COMPLETION = 1j * (Y - Y_DAG)


def relative_generator(mass: float, source_coeff: float, operator: np.ndarray) -> float:
    """Exact additive CPT-even scalar generator on a local scalar baseline m I."""
    sign, logabs = np.linalg.slogdet(mass * I16 + source_coeff * operator)
    if abs(sign) == 0:
        raise ValueError("singular source-deformed block encountered")
    return float(logabs - 16.0 * math.log(abs(mass)))


def main() -> int:
    print("=" * 78)
    print("NEUTRINO BOSONIC NORMALIZATION THEOREM")
    print("=" * 78)
    print()

    print("Part 1: Exact bridge decomposition on C^16")
    check("direct chiral bridge is nilpotent", np.linalg.norm(Y @ Y) < 1e-12)
    check("Y + Y^dagger = Gamma_1", np.linalg.norm(SCALAR_COMPLETION - G1) < 1e-12)
    check(
        "i(Y - Y^dagger) = -i gamma_5 Gamma_1",
        np.linalg.norm(PSEUDOSCALAR_COMPLETION + 1j * GAMMA5_4D @ G1) < 1e-12,
    )
    check("Gamma_1 is Hermitian", np.linalg.norm(G1 - G1.conj().T) < 1e-12)
    check("Gamma_1 is an involution", np.linalg.norm(G1 @ G1 - I16) < 1e-12)

    pseudo_overlap = max(abs(np.trace(G.conj().T @ PSEUDOSCALAR_COMPLETION)) for G in G_SPATIAL)
    check(
        "pseudoscalar completion is orthogonal to the retained scalar Higgs family span{Gamma_i}",
        pseudo_overlap < 1e-12,
        detail=f"max overlap = {pseudo_overlap:.3e}",
    )

    print()
    print("Part 2: Observable-principle source response on a scalar local baseline m I")
    mass = 1.37
    w_y_max = 0.0
    w_g_max = 0.0
    w_p_max = 0.0
    w_quad_err = 0.0
    for j in (1e-3, 1e-2, 1e-1):
        w_y = relative_generator(mass, j, Y)
        w_g = relative_generator(mass, j, G1)
        w_p = relative_generator(mass, j, PSEUDOSCALAR_COMPLETION)
        exact_g = 8.0 * math.log(abs(1.0 - (j / mass) ** 2))
        quad_coeff = w_g / (j**2)
        exact_quad = -8.0 / (mass**2)
        w_y_max = max(w_y_max, abs(w_y))
        w_g_max = max(w_g_max, abs(w_g - exact_g))
        w_p_max = max(w_p_max, abs(w_p - exact_g))
        if j <= 1e-2:
            w_quad_err = max(w_quad_err, abs(quad_coeff - exact_quad))
        print(
            f"  j={j:g}: W[Y]={w_y:.6e}, W[Gamma_1]={w_g:.6e}, "
            f"W[pseudo]={w_p:.6e}, quad={quad_coeff:.6e}"
        )

    check(
        "raw chiral bridge has identically zero bosonic log|det| response",
        w_y_max < 1e-12,
        detail=f"max |W[Y]| = {w_y_max:.3e}",
    )
    check(
        "Gamma_1 source response matches the exact involution formula",
        w_g_max < 1e-12,
        detail=f"max |W - 8 log(1-j^2/m^2)| = {w_g_max:.3e}",
    )
    check(
        "the pseudoscalar companion has the same even determinant response",
        w_p_max < 1e-12,
        detail=f"max error = {w_p_max:.3e}",
    )
    check(
        "Gamma_1 carries nonzero quadratic bosonic curvature on the small-source surface",
        w_quad_err < 3e-4,
        detail=f"max small-j quadratic-coefficient error = {w_quad_err:.3e}",
    )

    print()
    print("Part 3: Canonical bridge ratio once the bosonic source family is fixed")
    trace_g = np.trace(G1.conj().T @ G1).real / 16.0
    trace_y = np.trace(Y_DAG @ Y).real / 16.0
    ratio_full = math.sqrt(trace_y / trace_g)
    trace_left_g = np.trace(P_L @ (G1.conj().T @ G1)).real / np.trace(P_L).real
    trace_left_y = np.trace(Y_DAG @ Y).real / np.trace(P_L).real
    ratio_active = math.sqrt(trace_left_y / trace_left_g)
    print(f"  Tr(Gamma_1^dag Gamma_1) / 16 = {trace_g:.6f}")
    print(f"  Tr(Y^dag Y) / 16            = {trace_y:.6f}")
    print(f"  full-space ratio            = {ratio_full:.6f}")
    print(f"  active-space ratio          = {ratio_active:.6f}")
    print()
    check("full-space canonical bridge ratio is 1/sqrt(2)",
          abs(ratio_full - 1.0 / math.sqrt(2.0)) < 1e-12,
          detail=f"ratio = {ratio_full:.12f}")
    check("active-space ratio remains 1 as a rejected non-bosonic comparator",
          abs(ratio_active - 1.0) < 1e-12,
          detail=f"ratio = {ratio_active:.12f}")

    g_weak_example = 0.653
    y_selected = g_weak_example / math.sqrt(2.0)
    y_active = g_weak_example
    print()
    print("Selected benchmark surface:")
    print(f"  if g_weak = {g_weak_example:.3f}, observable-principle normalization gives")
    print(f"    y_nu^(0) = g_weak / sqrt(2) = {y_selected:.6f}")
    print(f"  while the active-space comparator would be {y_active:.6f}")
    print()

    print("Honest read:")
    print("  1. The raw chiral bridge Y = P_R Gamma_1 P_L is exact, but by itself it")
    print("     carries no bosonic scalar source-response on a local scalar baseline.")
    print("  2. The retained local Higgs family fixes the physical scalar completion as")
    print("     Gamma_1 = Y + Y^dagger, not the active bridge alone.")
    print("  3. Once the physical source family is assigned on Gamma_1, the branch's")
    print("     canonical trace normalization selects the full-space bridge ratio")
    print("     y_nu^(0) / g_weak = 1/sqrt(2).")
    print("  4. So the base-normalization ambiguity is closed. The downstream")
    print("     retained local Schur theorem now fixes the exact T_1 return,")
    print("     and the live remaining blocker is the Majorana / Z3 activation law.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
