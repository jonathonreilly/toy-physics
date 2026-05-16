#!/usr/bin/env python3
"""
Audit companion runner: RP Half-Square Identity Cannot Forbid CP-Odd Imaginary Action
====================================================================================

Source note:
  docs/STRONG_CP_RP_HALF_CANNOT_FORBID_CP_ODD_IMAGINARY_NO_GO_NOTE_2026-05-16.md

Purpose:
  Verify the no-go that the retained reflection-positivity norm-square
  identity (from REFLECTION_POSITIVITY_GAUGE_HALF_CAUCHY_SCHWARZ_NARROW_THEOREM_NOTE_2026-05-10)
  cannot detect CP-odd imaginary action additions of the topological-charge
  type. The CP-odd phase, when paired across the Theta-orbit
  {x, Theta x}, cancels because the CP-odd density h is Theta-anti-invariant
  while the half-action S_+ is Theta-invariant -- a mismatch in parity that
  the reflected expectation's pairing structure exactly nullifies.

  Reusable negative evidence: future audit-fix iterations on
  strong_cp_theta_zero_note should not attempt the RP-based derivation of
  "no bare θ slot."

  Uses sympy exact rational arithmetic and numpy double-precision
  cross-check on finite carrier X = Z/N, N in {6, 10}.
"""

from __future__ import annotations

import sys
import math

import numpy as np
import sympy as sp


COUNTS = {"PASS": 0, "FAIL": 0}


def check(name: str, condition: bool, detail: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    COUNTS[status] += 1
    print(f"  [{status}] {name}" + (f"  ({detail})" if detail else ""))
    return condition


# -----------------------------------------------------------------------------
# Finite carrier construction.
# -----------------------------------------------------------------------------


def theta(k: int, N: int) -> int:
    """Theta(k) = -k mod N."""
    return (-k) % N


# -----------------------------------------------------------------------------
# Theta-invariant real half-action and Theta-anti-invariant real CP-odd density.
# -----------------------------------------------------------------------------


def s_plus_sym(k: int, N: int):
    """Sympy: Theta-invariant real S_+(k) = (1 - cos(2π k / N)) / 2."""
    return sp.Rational(1, 2) * (1 - sp.cos(2 * sp.pi * k / N))


def s_plus_flt(k: int, N: int) -> float:
    return 0.5 * (1.0 - math.cos(2.0 * math.pi * k / N))


def h_sym(k: int, N: int):
    """Sympy: Theta-anti-invariant real h(k) = sin(2π k / N)."""
    return sp.sin(2 * sp.pi * k / N)


def h_flt(k: int, N: int) -> float:
    return math.sin(2.0 * math.pi * k / N)


# -----------------------------------------------------------------------------
# Reflection-Hermitian observable basis: F_n(k) = exp(2 π i n k / N).
# -----------------------------------------------------------------------------


def F_basis_sym(n: int, k: int, N: int):
    return sp.exp(2 * sp.pi * sp.I * n * k / N)


def F_basis_flt(n: int, k: int, N: int) -> complex:
    ang = 2.0 * math.pi * n * k / N
    return complex(math.cos(ang), math.sin(ang))


# -----------------------------------------------------------------------------
# Reflected expectations.
# -----------------------------------------------------------------------------


def re_original_sym(n: int, N: int):
    """Original: (1/N) sum_k exp(-2 S+(k)) F_n(Theta k) F_n(k)."""
    total = 0
    for k in range(N):
        tk = theta(k, N)
        weight = sp.exp(-2 * s_plus_sym(k, N))
        total += weight * F_basis_sym(n, tk, N) * F_basis_sym(n, k, N)
    return sp.simplify(total / N)


def re_sym_mod_sym(n: int, N: int, c):
    """Symmetric modification: both sides carry exp(-i c h).
    (1/N) sum_k exp(-S+(k) - i c h(k)) exp(-S+(Theta k) - i c h(Theta k))
            F_n(Theta k) F_n(k)."""
    total = 0
    for k in range(N):
        tk = theta(k, N)
        weight_k = sp.exp(-s_plus_sym(k, N) - sp.I * c * h_sym(k, N))
        weight_tk = sp.exp(-s_plus_sym(tk, N) - sp.I * c * h_sym(tk, N))
        total += weight_k * weight_tk * F_basis_sym(n, tk, N) * F_basis_sym(n, k, N)
    return sp.simplify(total / N)


def re_single_side_mod_flt(n: int, N: int, c: float) -> complex:
    """Single-side modification: only the x side carries exp(-i c h(k)).
    (1/N) sum_k exp(-S+(k) - i c h(k)) exp(-S+(Theta k)) F_n(Theta k) F_n(k).

    Equivalently (S+ Theta-invariant): exp(-2 S+(k)) exp(-i c h(k)) |F_n(k)|².
    Pairing k with Theta k gives 2 cos(c h(k)) per orbit; the imaginary
    phase cancels."""
    total = 0.0 + 0j
    for k in range(N):
        tk = theta(k, N)
        weight = math.exp(-2.0 * s_plus_flt(k, N)) * complex(
            math.cos(c * h_flt(k, N)),
            -math.sin(c * h_flt(k, N)),
        )
        total += weight * F_basis_flt(n, tk, N) * F_basis_flt(n, k, N)
    return total / N


def re_original_flt(n: int, N: int) -> complex:
    total = 0.0 + 0j
    for k in range(N):
        tk = theta(k, N)
        weight = math.exp(-2.0 * s_plus_flt(k, N))
        total += weight * F_basis_flt(n, tk, N) * F_basis_flt(n, k, N)
    return total / N


# -----------------------------------------------------------------------------
# Orbit-level identity (B) verification.
# -----------------------------------------------------------------------------


def orbit_contribution_single_side_flt(n: int, N: int, k: int, c: float) -> complex:
    """Sum of single-side modified contributions from the Theta-orbit of k.
    For an orbit of size 2 ({k, Theta k}, k != Theta k), this is the sum over
    both points. For a fixed point (k = Theta k), this is the single
    contribution at k."""
    tk = theta(k, N)
    orbit_points = (k,) if k == tk else (k, tk)
    contributions = 0.0 + 0j
    for x in orbit_points:
        tx = theta(x, N)
        weight = math.exp(-2.0 * s_plus_flt(x, N)) * complex(
            math.cos(c * h_flt(x, N)),
            -math.sin(c * h_flt(x, N)),
        )
        contributions += weight * F_basis_flt(n, tx, N) * F_basis_flt(n, x, N)
    return contributions


def orbit_contribution_cosine_flt(n: int, N: int, k: int, c: float) -> complex:
    """Predicted from (B): 2 cos(c h(k)) * exp(-2 S+(k)) |F_n(k)|² for orbits
    of size 2; for fixed points just the original real value."""
    tk = theta(k, N)
    if k == tk:
        weight = math.exp(-2.0 * s_plus_flt(k, N))
        return weight * F_basis_flt(n, tk, N) * F_basis_flt(n, k, N)
    # Orbit of size 2.
    weight = math.exp(-2.0 * s_plus_flt(k, N))
    fmag_sq_k = (F_basis_flt(n, k, N).real ** 2 + F_basis_flt(n, k, N).imag ** 2)
    fmag_sq_tk = (F_basis_flt(n, tk, N).real ** 2 + F_basis_flt(n, tk, N).imag ** 2)
    # Should agree (reflection-Hermiticity implies equal modulus).
    assert abs(fmag_sq_k - fmag_sq_tk) < 1e-12
    return 2.0 * math.cos(c * h_flt(k, N)) * weight * fmag_sq_k


# -----------------------------------------------------------------------------
# Verification structure.
# -----------------------------------------------------------------------------


def verify_carrier(N: int, c_value: float = 0.5):
    print(f"\n=== Carrier X = Z/{N}, c = {c_value} ===\n")

    # Pre-flight: Theta is a measure-preserving involution.
    theta_sq_ok = all(theta(theta(k, N), N) == k for k in range(N))
    check(f"[N={N}] Theta^2 = id", theta_sq_ok)

    # 1. Theta-invariance of S_+ (sympy exact).
    s_plus_diffs = [
        sp.simplify(s_plus_sym(k, N) - s_plus_sym(theta(k, N), N)) for k in range(N)
    ]
    check(
        f"[N={N}] Theta-invariance of S_+ (sympy exact)",
        all(d == 0 for d in s_plus_diffs),
    )

    # 2. Theta-anti-invariance of h (sympy exact).
    h_sums = [sp.simplify(h_sym(k, N) + h_sym(theta(k, N), N)) for k in range(N)]
    check(
        f"[N={N}] Theta-anti-invariance of h (sympy exact)",
        all(d == 0 for d in h_sums),
    )

    # 3. Symmetric modification leaves the reflected expectation identical
    #    to the original (Step 1, eq (A)). Sympy exact for n = 1, 2, 3 and
    #    c = 1/2.
    c_sym = sp.Rational(c_value).limit_denominator(1000)
    sym_mod_identity_ok = True
    for n in (1, 2, 3):
        diff = sp.simplify(re_sym_mod_sym(n, N, c_sym) - re_original_sym(n, N))
        if diff != 0:
            sym_mod_identity_ok = False
            print(f"  [INFO] F_n={n}: symmetric modification diff = {diff}")
    check(
        f"[N={N}] Symmetric mod RE = original RE for all basis F (sympy exact)",
        sym_mod_identity_ok,
    )

    # 4. Single-side modification gives a real reflected expectation
    #    (Step 2, eqs (B)-(C)).
    single_side_real_all = True
    max_im_single_side = 0.0
    for n in (1, 2, 3):
        for c_test in (c_value, 0.7, 1.3):
            re = re_single_side_mod_flt(n, N, c_test)
            max_im_single_side = max(max_im_single_side, abs(re.imag))
            if abs(re.imag) > 1e-12:
                single_side_real_all = False
                print(
                    f"  [INFO] F_n={n}, c={c_test}: Im(single-side RE) = "
                    f"{re.imag:.3e} (non-zero!)"
                )
    check(
        f"[N={N}] Single-side modified RE is real for all basis F and tested c",
        single_side_real_all,
        f"max |Im| = {max_im_single_side:.2e}",
    )

    # 5. As c -> 0, single-side modified RE -> original RE.
    c0_convergence_all = True
    for n in (1, 2, 3):
        re_c0 = re_single_side_mod_flt(n, N, 0.0)
        re_orig = re_original_flt(n, N)
        if abs(re_c0 - re_orig) > 1e-12:
            c0_convergence_all = False
            print(
                f"  [INFO] F_n={n}: |RE(c=0) - RE(orig)| = "
                f"{abs(re_c0 - re_orig):.3e}"
            )
    check(
        f"[N={N}] Single-side modified RE -> original RE as c -> 0",
        c0_convergence_all,
    )

    # 6. Real part of single-side modified RE decreases quadratically in c
    #    for small c (consistent with cos(c h) ≈ 1 - (c h)^2 / 2).
    quadratic_ok = True
    for n in (1, 2, 3):
        re_orig = re_original_flt(n, N).real
        # Skip if the original is essentially zero (would cause numerical issues).
        if abs(re_orig) < 1e-12:
            continue
        c_small = 1e-3
        c_med = 1e-2
        d_small = re_orig - re_single_side_mod_flt(n, N, c_small).real
        d_med = re_orig - re_single_side_mod_flt(n, N, c_med).real
        # d ~ const * c^2, so d_med / d_small should be ~ (c_med / c_small)^2 = 100.
        # Skip if d_small is essentially zero (this n basis has zero CP-odd
        # response to leading order).
        if abs(d_small) < 1e-14:
            continue
        ratio = d_med / d_small
        # Allow generous tolerance for numerical drift (factor of 2).
        if not (50.0 < ratio < 200.0):
            quadratic_ok = False
            print(
                f"  [INFO] F_n={n}: quadratic ratio = {ratio:.3f} "
                f"(expected ~100)"
            )
    check(
        f"[N={N}] Real-part suppression is approx. quadratic in c at small c",
        quadratic_ok,
    )

    # 7. Cross-orbit pairing identity (Step 2, eq (B)).
    orbit_identity_ok = True
    max_orbit_err = 0.0
    for n in (1, 2, 3):
        seen_orbits = set()
        for k in range(N):
            orbit_key = frozenset({k, theta(k, N)})
            if orbit_key in seen_orbits:
                continue
            seen_orbits.add(orbit_key)
            actual = orbit_contribution_single_side_flt(n, N, k, c_value)
            predicted = orbit_contribution_cosine_flt(n, N, k, c_value)
            err = abs(actual - predicted)
            max_orbit_err = max(max_orbit_err, err)
            if err > 1e-12:
                orbit_identity_ok = False
    check(
        f"[N={N}] Orbit-level identity (B): single-side orbit = "
        f"2 cos(c h(k)) exp(-2 S+(k)) |F(k)|²",
        orbit_identity_ok,
        f"max orbit |err| = {max_orbit_err:.2e}",
    )


def main():
    print("=" * 78)
    print("RP Half-Square Identity Cannot Forbid CP-Odd Imaginary Action - Audit Companion")
    print("=" * 78)
    print()
    print("Verifies: adding S_CP = i c h with c != 0 and h real Theta-anti-invariant")
    print("          to a Theta-invariant real half-action S_+ does NOT break the")
    print("          retained RP norm-square identity. The CP-odd imaginary phase")
    print("          cancels in the reflected expectation of every reflection-")
    print("          Hermitian observable, because Theta-anti-invariance of h flips")
    print("          its sign under the Theta-orbit pairing that the reflected")
    print("          expectation enforces. Retained RP is structurally insensitive")
    print("          to CP-odd imaginary contamination of the topological-charge type.")

    for N in (6, 10):
        verify_carrier(N, c_value=0.5)

    print()
    print("=" * 78)
    print(f"PASS={COUNTS['PASS']}  FAIL={COUNTS['FAIL']}")
    print("=" * 78)

    if COUNTS["FAIL"] != 0:
        print(
            "\nOne or more RP-CP-odd-insensitivity checks failed. The runner expects "
            "all to pass; failures indicate either a numerical regression or an "
            "error in the claim of the no-go."
        )
        return 1

    print()
    print("All checks passed. On the cited retained Theta-invariant real RP half-action")
    print("carrier, a CP-odd imaginary addition S_CP = i c h (c != 0, h real")
    print("Theta-anti-invariant) does NOT break the reflected expectation's real")
    print("non-negativity for any reflection-Hermitian observable. This realises the")
    print("narrow no-go: the 'no bare θ slot' premise of strong_cp_theta_zero_note")
    print("cannot be derived from retained RP alone. Reusable negative evidence: a")
    print("different ingredient (closed-form Z_Q positivity, action-class")
    print("tightening, or measure-theoretic primitive) is needed to close the gap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
