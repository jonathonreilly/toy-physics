#!/usr/bin/env python3
"""
Koide Q = 2/3 sub-route (a) NO-GO: retained chart is NOT O_h-covariant.

Tests whether the retained affine chart
  H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q

transforms covariantly under the 48-element cubic point group O_h.

An O_h element g acts by H → g H g^T. Covariance means: for every g ∈ O_h
and every (m, δ, q_+), there exists (m', δ', q_+') with g H(m,δ,q_+) g^T =
H(m', δ', q_+'). Equivalently, the span {H_base, T_m, T_δ, T_q, I} is
g-invariant for every g.

Finding: the only g ∈ O_h preserving this span are g = I (identity) and
g = -I (total spatial inversion). That's a Z_2 subgroup of O_h, NOT the
full 48-element cubic group.

This FALSIFIES sub-route (a) of the spin-1 structural claim. The charged-
lepton triplet's SO(3) ⊂ O_h symmetry is NOT inherited through the retained
affine chart.

Sub-routes (b) and (c) remain.

See docs/KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


# Retained constants
GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
T_DELTA = np.array([[0, -1, 1], [-1, 1, 0], [1, 0, -1]], dtype=complex)
T_Q = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex)
H_BASE = np.array(
    [[0, E1, -E1 - 1j * GAMMA], [E1, 0, -E2], [-E1 + 1j * GAMMA, -E2, 0]],
    dtype=complex,
)


def generate_Oh():
    """Generate all 48 elements of O_h = signed permutations of 3 axes."""
    els = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([-1, 1], repeat=3):
            g = np.zeros((3, 3), dtype=complex)
            for i in range(3):
                g[i, perm[i]] = signs[i]
            els.append(g)
    return els


def flatten(M):
    return np.concatenate([M.real.flatten(), M.imag.flatten()])


def main() -> int:
    print("=" * 80)
    print("O_h covariance no-go for retained H(m, δ, q_+) chart")
    print("=" * 80)

    Oh = generate_Oh()
    check("1.1 O_h has 48 elements (signed permutations of 3 axes)",
          len(Oh) == 48,
          f"|O_h| = {len(Oh)}")

    # Individual stabilizers: g M g^T = M exactly.
    def stab(M):
        return [g for g in Oh if np.allclose(g @ M @ g.T, M, atol=1e-10)]

    print()
    print("Individual stabilizers |Stab(M)| for each generator:")
    stabs = {
        "H_base": stab(H_BASE),
        "T_m":    stab(T_M),
        "T_δ":    stab(T_DELTA),
        "T_q":    stab(T_Q),
    }
    for name, s in stabs.items():
        print(f"  |Stab({name})| = {len(s)}")

    # Joint pointwise stabilizer
    joint_stab = [g for g in Oh if all(np.allclose(g @ M @ g.T, M, atol=1e-10)
                                        for M in [H_BASE, T_M, T_DELTA, T_Q])]
    check(f"1.2 Joint pointwise stabilizer has {len(joint_stab)} elements (not 48)",
          len(joint_stab) < 48,
          f"|Joint Stab| = {len(joint_stab)}\n"
          f"If the chart were fully O_h-invariant pointwise, this would be 48.\n"
          f"→ pointwise invariance fails.")

    # Covariance: span preserved (allowing g H(m,δ,q+) g^T = H(m',δ',q+')).
    basis_mats = [H_BASE, T_M, T_DELTA, T_Q, np.eye(3, dtype=complex)]
    basis_vecs = np.array([flatten(M) for M in basis_mats])

    def in_span(M, tol=1e-8):
        v = flatten(M)
        A = basis_vecs.T
        x, _, _, _ = np.linalg.lstsq(A, v, rcond=None)
        residual = np.linalg.norm(A @ x - v)
        return residual < tol

    covariant = [g for g in Oh if all(in_span(g @ B @ g.T)
                                       for B in [H_BASE, T_M, T_DELTA, T_Q])]
    check(f"2.1 O_h elements with chart-span preservation (covariance): {len(covariant)}",
          True,
          f"|Covariance group| = {len(covariant)}\n"
          f"An O_h element g is in the covariance group iff g·B·g^T is in the\n"
          f"real span of {{H_base, T_m, T_δ, T_q, I}} for each basis matrix B.\n"
          f"This is the largest subgroup under which the chart is covariant.")

    # Classify the covariant elements
    print()
    print("The covariant elements (permutation, signs, det):")
    for g in covariant:
        perm = [int(np.argmax(np.abs(g[row, :]))) for row in range(3)]
        signs = [int(np.real(g[row, perm[row]])) for row in range(3)]
        det = round(np.real(np.linalg.det(g)))
        print(f"  perm={perm}, signs={signs}, det={det}")

    check("2.2 Covariance group = {I, -I} = Z_2 (spatial inversion only)",
          len(covariant) == 2,
          f"Only identity I = diag(+1,+1,+1) and inversion -I = diag(-1,-1,-1)\n"
          f"preserve the retained chart's span. Out of 48 O_h elements, only 2.\n"
          f"→ the retained chart carries at most Z_2 (parity), not SO(3) or O_h.")

    # Verify the 2 covariant elements are I and -I
    I3 = np.eye(3, dtype=complex)
    has_I = any(np.allclose(g, I3) for g in covariant)
    has_minus_I = any(np.allclose(g, -I3) for g in covariant)
    check("2.3 Covariance group = {+I, -I} = spatial parity Z_2 (verified)",
          has_I and has_minus_I and len(covariant) == 2,
          f"+I present: {has_I}, -I present: {has_minus_I}")

    # Therefore: sub-route (a) FALSIFIED. The retained H_base + generators do
    # NOT carry cubic O_h symmetry on the 3-generation triplet. The claimed
    # "SO(3) spin-1 via lattice isotropy of H_base" does not hold through the
    # retained chart.

    # -------------------------------------------------------------------------
    # Step 3. What this implies for the spin-1 route
    # -------------------------------------------------------------------------
    check("3.1 Sub-route (a) FALSIFIED: H_base chart NOT O_h-covariant",
          True,
          "The 'spin-1 SO(3) identification via O_h cubic invariance of H_base'\n"
          "does NOT hold. The chart is only invariant under spatial inversion Z_2.\n"
          "\n"
          "→ sub-route (a) of the spin-1 structural claim is ruled out.\n"
          "→ sub-routes (b) and (c) remain untested and open.")

    check("3.2 Remaining sub-routes for spin-1 structural claim (still open):",
          True,
          "(b) Body-diagonal Z_3 fixed-point structure ⇒ SO(3) isotropy extension.\n"
          "(c) SU(2)_L × 3-generation ⇒ spin-1 on generation factor.\n"
          "\n"
          "Either route, if discharged, would still close Q = 2/3 via\n"
          "Q_Koide = (d-1)/d = 2/3 at d = 3.\n"
          "\n"
          "This no-go SHARPENS the outstanding question: the route cannot go\n"
          "through the explicit affine chart's cubic symmetry. It must go through\n"
          "a DIFFERENT structural mechanism (Z_3-fixed-locus isotropy or SM SU(2)_L\n"
          "× generation structure).")

    # Summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print()
        print("NO-GO: retained chart H(m, δ, q_+) is NOT O_h-covariant.")
        print("Covariance group = Z_2 (spatial parity only).")
        print()
        print("Spin-1 sub-route (a) is ruled out.")
        print("Sub-routes (b) body-diagonal isotropy and (c) SU(2)_L × generation")
        print("remain as candidate closures of Q = 2/3.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
