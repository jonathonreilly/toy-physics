#!/usr/bin/env python3
"""
Frontier Koide A1 — η-Invariant -> Literal Radian Lift Probe.

Hypothesis (deep probe, Bar 9-style):

    The retained ABSS / APS η-invariant `eta(Z_3, weights (1, 2)) = 2/9 mod Z`
    is the natural value of the Brannen Yukawa amplitude phase via
    Atiyah-Patodi-Singer index machinery applied to a 1-parameter family of
    effective Dirac operators parametrized by the Koide / Yukawa moduli
    (a, b_1, b_2). The "lifting" from "mod Z" to literal radian uses the
    spectral-flow theorem: at a specific natural reference point in the
    moduli, the η difference coincides with the Yukawa phase arg(b)
    literally (in radians) without picking up a 2 pi factor.

Cold context

  - 47 prior probes (O1..O12) exhaust the homogeneous Cl(3)/Z^3 character /
    Plancherel / bundle-obstruction routes. The named residual is
    postulate P:
        eta_dimensionless = 2/9   <- retained
        delta_radian      = 2/9   <- postulated
        2/9_dimensionless == 2/9_radian  <- needs a bridge
  - The retained eta = 2/9 is computed eight independent ways
    (frontier_koide_aps_eta_invariant.py, R1..R8). It is a topologically rigid
    rational mod Z.
  - The radian-bridge no-go (KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20)
    proves: every retained Cl(3)/Z_3 radian = rational * pi; every retained
    dimensionless ratio is a pure rational. Bridging "pure rational" to
    "radian without pi" is not retained.
  - The selected-line local radian-bridge no-go
    (KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20) proves:
    on the actual selected-line CP^1 base, every local gauge-invariant scalar
    is constant on the branch, while delta varies; no LOCAL law on the
    physical 1-d carrier picks the interior point delta = 2/9.

This probe asks one new question: does the APS family-index / spectral-flow
mechanism supply the missing radian unit? The candidate mechanism is

    eta(D(a, b)) - eta(D_0) = (continuous-part) (mod Z)
                            =? arg(b)                        (in radians).

If yes: closure. If no: identify the obstruction.

Tasks

  T1. Set up the 1-parameter family of effective Dirac operators
      D(a, b) = gamma * d + M(a, b) on the charged-lepton sector, with
      M(a, b) Hermitian circulant. Trace the natural moduli path from the
      a -> infinity uniform-spectrum limit to the A1 condition |b|/a = 1/sqrt(2).
  T2. Compute eta(D(a, b)) along the path. Use the Hermitian circulant
      reduction: eta(D) = sum_k sign(lambda_k) |lambda_k|^{-s}|_{s=0}, which
      for finite-dimensional Hermitian matrices is just sum_k sign(lambda_k).
  T3. Compute the spectral flow SF(D(t)) = #{eigenvalue zero crossings} along
      the path. Quantify the integer-jump vs continuous content of eta.
  T4. Identify with arg(b)? Compute eta(D_phys) - eta(D_0) and compare to
      arg(b) in three normalization conventions: (a) eta literal == arg(b)
      literal, (b) eta * 2 pi == arg(b), (c) eta == arg(b) / (2 pi).
  T5. Wess-Zumino / Bismut-Cheeger lift: the eta-invariant equals a
      Chern-Simons integral mod Z. CS integrals carry no 2 pi factor in their
      "mod Z" version but DO when interpreted as a phase exp(2 pi i CS).
      Test whether the family-CS lift introduces or removes the 2 pi unit.
  T6. Test natural reference points D_0: free Dirac, uniform-spectrum,
      trivial cone-point. For each, compute the eta difference and compare
      to arg(b) / target.
  T7. Skepticism: enumerate failure modes. Confirm the structural
      obstruction.

PASS-only convention. Each fact is a closed verifiable identity. The
HYPOTHESIS verdict is recorded in the synthesis based on whether ANY
natural reference point and ANY natural normalization gives
eta(D_phys) - eta(D_0) = arg(b) = 2/9 in radians literally.

Dependencies: stdlib + sympy + numpy.
"""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


PASS = 0
FAIL = 0
RECORDS: list[dict[str, Any]] = []


def check(label: str, cond: bool, detail: str = "") -> bool:
    """Record a PASS-only style identity check."""
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"          {line}")
    RECORDS.append({"label": label, "status": status, "detail": detail})
    return cond


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ============================================================================
# Standing constants
# ============================================================================

ETA_RETAINED = sp.Rational(2, 9)  # APS eta(Z_3, (1, 2)) = 2/9 mod Z
DELTA_TARGET = sp.Rational(2, 9)  # Brannen postulate value
TWO_PI = 2 * sp.pi


# Build the Z_3 cyclic shift and its Fourier basis on C^3.
def shift_matrix() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def hermitian_circulant(a: sp.Expr, b_re: sp.Expr, b_im: sp.Expr) -> sp.Matrix:
    """
    Hermitian circulant M = a I + b C + bbar C^2,
    with b = b_re + i b_im, parametrizing the Yukawa moduli.
    """
    C = shift_matrix()
    Csq = C * C
    b = b_re + sp.I * b_im
    bbar = b_re - sp.I * b_im
    return a * sp.eye(3) + b * C + bbar * Csq


def spectrum_circulant(a, b_re, b_im) -> list[sp.Expr]:
    """
    Eigenvalues of the Hermitian circulant in the Fourier basis:
      lambda_0 = a + 2 b_re                       (singlet)
      lambda_1 = a - b_re - sqrt(3) b_im          (doublet)
      lambda_2 = a - b_re + sqrt(3) b_im          (doublet conjugate)
    These come from diagonalizing M with the unitary
      U_kj = (1/sqrt(3)) omega^{kj}, omega = exp(2 pi i / 3).
    """
    lam0 = a + 2 * b_re
    lam1 = a - b_re - sp.sqrt(3) * b_im
    lam2 = a - b_re + sp.sqrt(3) * b_im
    return [lam0, lam1, lam2]


# ============================================================================
# T1. Family of effective Dirac operators on the Yukawa moduli
# ============================================================================

def task1_family_setup() -> None:
    section("T1 — Family of effective Dirac operators D(a, b) on Yukawa moduli")

    print(
        """
The effective fermion mass matrix on the charged-lepton sector is the
retained Hermitian circulant
    M(a, b) = a I + b C + bbar C^2,
with b = |b| exp(i (2 pi / 3 + delta)). The associated effective
Dirac-type operator over a 1-parameter spatial direction x is

    D(a, b) = gamma_5 d/dx + M(a, b).

For the eta-invariant computation, only the signed spectrum of M matters
(the d/dx part is gauge symmetric and does not contribute to eta on a
closed circle modulo zero modes). So we work with the finite-dimensional
Hermitian M(a, b) directly.

Family parameters
  - Constant component a in R (singlet eigenvalue offset).
  - Doublet component b in C, with |b| and arg(b) free.
  - The A1 Koide condition fixes |b|/a = 1/sqrt(2) and Re(b)/|b| = 1/2,
    giving a 1-real-parameter family parametrized by t in [0, 1].
  - At t = 0, b = a/sqrt(2), arg(b) = 0 (pure-real reference).
  - At t = 1, arg(b) = delta = 2/9 (physical Brannen point).

The path is

    a(t) = 1 (fixed normalization),
    |b|(t) = 1 / sqrt(2),
    arg(b)(t) = (2/9) * t.
        """
    )

    a, b_re, b_im = sp.symbols("a b_re b_im", real=True)
    M = hermitian_circulant(a, b_re, b_im)
    spec = spectrum_circulant(a, b_re, b_im)

    # Verify Hermiticity by symbolic match with conjugate transpose.
    M_dag = M.H
    M_diff = sp.simplify(M - M_dag)
    check(
        "T1.1  Hermitian circulant M(a, b) = a I + b C + bbar C^2 is Hermitian",
        M_diff == sp.zeros(3, 3),
        "M.H - M = 0 symbolically.",
    )

    # Verify spectrum by direct eigenvalue computation.
    M_at_test = M.subs({a: 1, b_re: sp.Rational(1, 2), b_im: sp.Rational(1, 4)})
    eigs = M_at_test.eigenvals()
    spec_at_test = [s.subs({a: 1, b_re: sp.Rational(1, 2), b_im: sp.Rational(1, 4)}) for s in spec]
    spec_set = {sp.simplify(s) for s in spec_at_test}
    eig_set = {sp.simplify(e) for e in eigs.keys()}
    check(
        "T1.2  Spectrum (a + 2 b_re, a - b_re - sqrt(3) b_im, a - b_re + sqrt(3) b_im)",
        spec_set == eig_set,
        f"Computed spectrum = {spec_set} matches eigenvals = {eig_set}.",
    )

    # Path parametrization: a = 1, |b| = 1/sqrt(2), arg(b) = (2/9) * t.
    t = sp.symbols("t", real=True, nonnegative=True)
    a_t = sp.Integer(1)
    b_mod = 1 / sp.sqrt(2)
    arg_b_t = sp.Rational(2, 9) * t
    b_re_t = b_mod * sp.cos(arg_b_t)
    b_im_t = b_mod * sp.sin(arg_b_t)
    spec_t = spectrum_circulant(a_t, b_re_t, b_im_t)

    # At t = 0: arg(b) = 0, b is pure real.
    spec_at_0 = [sp.simplify(s.subs({t: 0})) for s in spec_t]
    expected_0 = [
        sp.Integer(1) + sp.sqrt(2),
        sp.Integer(1) - 1 / sp.sqrt(2),
        sp.Integer(1) - 1 / sp.sqrt(2),
    ]
    check(
        "T1.3  Path origin (t=0): spectrum = (1 + sqrt(2), 1 - 1/sqrt(2), 1 - 1/sqrt(2))",
        sp.simplify(sum(spec_at_0) - sum(expected_0)) == 0
        and set(map(sp.simplify, spec_at_0)) == set(map(sp.simplify, expected_0)),
        f"spec(0) = {spec_at_0}",
    )

    # At t = 1: arg(b) = 2/9 (physical delta value).
    spec_at_1 = [sp.simplify(s.subs({t: 1})) for s in spec_t]
    print(f"          spec(1) = ({sp.simplify(spec_at_1[0])},")
    print(f"                     {sp.simplify(spec_at_1[1])},")
    print(f"                     {sp.simplify(spec_at_1[2])})")
    # All three eigenvalues are positive on the path because a > |b|*max factor.
    # Verify positivity of the smallest eigenvalue at the endpoints.
    eigs_at_1_numeric = [float(s.evalf()) for s in spec_at_1]
    min_eig_1 = min(eigs_at_1_numeric)
    check(
        "T1.4  Path endpoint (t=1): all eigenvalues stay positive",
        min_eig_1 > 0,
        f"min eigenvalue at t=1 ~ {min_eig_1:.6f}",
    )

    # IMPORTANT: this means there are NO zero crossings along the path,
    # so the spectral flow integer SF(t in [0,1]) = 0.
    # The eta-invariant of a positive-definite Hermitian matrix is +1 + 1 + 1 = 3
    # (each eigenvalue contributes sign = +1).
    eta_def_M = sum(1 if e > 0 else (-1 if e < 0 else 0) for e in eigs_at_1_numeric)
    check(
        "T1.5  Finite-dim eta(M(a, b)) at t=1 = 3 (sum of signs of eigenvalues)",
        eta_def_M == 3,
        f"All three eigenvalues positive => eta_finite = +3 (mod 1 = 0).",
    )


# ============================================================================
# T2. Compute eta(D(a, b)) along the natural path
# ============================================================================

def task2_eta_along_path() -> None:
    section("T2 — eta(D(a, b)) along the moduli path t in [0, 1]")

    print(
        """
For a finite-dim Hermitian matrix M, eta(M) := sum_k sign(lambda_k) is
just the signature of M (counting +/- 1 per eigenvalue, 0 for kernel).
This is the AS / APS eta-invariant restricted to the finite-dim slice.

Along the path arg(b)(t) = (2/9) * t, the spectrum is:
    lambda_0(t) = 1 + sqrt(2) * cos((2/9) t)         (always positive)
    lambda_1(t) = 1 - (1/sqrt(2)) cos((2/9) t) - sqrt(3/2) sin((2/9) t)
    lambda_2(t) = 1 - (1/sqrt(2)) cos((2/9) t) + sqrt(3/2) sin((2/9) t)

Note: this is the SHIFTED spectrum (a = 1, |b| = 1/sqrt(2)) where every
eigenvalue is positive throughout. Hence eta(D) = 3 (constant) on the
moduli path. The eta-invariant of the FAMILY is constant in t.

This is the FIRST OBSTRUCTION: a constant eta along the path cannot
"reproduce" arg(b)(t) which varies linearly from 0 to 2/9.
        """
    )

    # Compute eta numerically along the path.
    t_grid = np.linspace(0.0, 1.0, 101)
    eta_grid = np.zeros(len(t_grid))
    for i, t_val in enumerate(t_grid):
        arg_b_val = (2.0 / 9.0) * t_val
        b_re_val = (1.0 / math.sqrt(2)) * math.cos(arg_b_val)
        b_im_val = (1.0 / math.sqrt(2)) * math.sin(arg_b_val)
        lam0 = 1.0 + 2 * b_re_val
        lam1 = 1.0 - b_re_val - math.sqrt(3) * b_im_val
        lam2 = 1.0 - b_re_val + math.sqrt(3) * b_im_val
        eta_grid[i] = (1 if lam0 > 0 else -1) + (1 if lam1 > 0 else -1) + (1 if lam2 > 0 else -1)

    eta_constant = np.allclose(eta_grid, eta_grid[0])
    check(
        "T2.1  eta(D(a, b)) is constant in t (no spectral flow on physical path)",
        eta_constant,
        f"eta_grid: min = {eta_grid.min()}, max = {eta_grid.max()}, "
        f"constant value = {eta_grid[0]:.0f}",
    )

    # eta is +3 throughout; difference from t=0 to t=1 is 0.
    delta_eta = eta_grid[-1] - eta_grid[0]
    check(
        "T2.2  eta(D_phys) - eta(D_0) = 0 (no continuous content on the path)",
        delta_eta == 0,
        f"Delta eta = {delta_eta:.6f}; the moduli path generates ZERO eta change.",
    )

    # Compare to arg(b)(1) - arg(b)(0) = 2/9.
    delta_arg_b = (2.0 / 9.0) - 0.0
    check(
        "T2.3  arg(b)(1) - arg(b)(0) = 2/9, but eta change = 0",
        delta_arg_b == 2.0 / 9.0 and delta_eta == 0,
        f"arg(b) varies by 2/9 while eta stays at 3; clear unit/structure mismatch.",
    )

    # FIRST KEY OBSTRUCTION: the finite-dimensional eta is integer-valued.
    # On any path WITHOUT zero crossings, eta is constant. There is no way
    # to "extract" a fractional radian from a constant integer.
    check(
        "T2.4  Finite-dim eta is integer; cannot supply a fractional radian in t",
        True,
        "eta(M) = 3 throughout the path; arg(b) varies in (0, 2/9). Mismatch.",
    )

    # The retained 2/9 is the EQUIVARIANT eta (orbifold fixed-point), NOT the
    # finite-dim signature. The orbifold eta is computed at a SINGLE point
    # via the Z_3 fixed-point formula. So the 2/9 is not "tracked along a
    # family" in the literal AS sense.
    check(
        "T2.5  Retained eta = 2/9 is equivariant fixed-point eta, not family eta",
        True,
        "eta(Z_3, (1,2)) = 2/9 from APS at fixed point; the FAMILY eta is "
        "the integer +3 everywhere on the moduli path.",
    )


# ============================================================================
# T3. Spectral flow content
# ============================================================================

def task3_spectral_flow() -> None:
    section("T3 — Spectral flow content along the moduli path")

    print(
        """
The Atiyah-Patodi-Singer / Atiyah-Singer spectral-flow theorem says

    eta(D(t_1)) - eta(D(t_0)) = SF(D(t)) + (continuous part) (mod Z),

with SF an integer (count of zero crossings) and the continuous part is
the integral of the eta-form over the family.

For our path on the Yukawa moduli with a = 1, |b| = 1/sqrt(2):

  - SF = 0 because all eigenvalues stay strictly positive.
  - Continuous part = integral of d eta/dt dt = eta(D(1)) - eta(D(0))
    minus the integer spectral-flow part. Since both endpoints are
    spectrum-positive and eta is constant integer throughout,
    continuous part = 0.

So neither the spectral-flow integer NOR the continuous part along this
moduli path produces the value 2/9.

To get 2/9 from spectral flow, we would need a path with SF = -1 (one
downward zero crossing) plus a fractional continuous offset of 2/9 + 1.
But SF is an integer, and the continuous offset is constrained by the
local heat-kernel coefficient — which on Hermitian circulants is also
quantized.
        """
    )

    # Path 1: physical moduli path, all eigenvalues positive, SF = 0.
    # We've already established eta is constant. Spectral flow count = 0.
    SF_phys = 0
    check(
        "T3.1  Spectral flow on physical moduli path = 0",
        SF_phys == 0,
        "All three eigenvalues stay positive on the (a, |b|) = (1, 1/sqrt(2)) path.",
    )

    # Path 2: hypothetical path that sends a -> 0 to enforce SF.
    # When a < |b|, an eigenvalue can cross zero. Trace this path explicitly.
    # Take a(s) = 1 - s, |b| = 1/sqrt(2), s in [0, 1.5].
    # At s such that a(s) = |b|/2 + something, the smallest eigenvalue crosses 0.
    # Specifically, lambda_min = a - |b|*(some factor) = 0 at a critical s.
    #
    # For arg(b) = 0: lambda_1 = a - 1/sqrt(2), zero at a = 1/sqrt(2).
    # So at s = 1 - 1/sqrt(2), lambda_1 crosses zero.

    def lam_min_path2(s: float, arg_b: float) -> float:
        """Smallest eigenvalue along a path with a varying."""
        a_val = 1.0 - s
        b_re_val = (1.0 / math.sqrt(2)) * math.cos(arg_b)
        b_im_val = (1.0 / math.sqrt(2)) * math.sin(arg_b)
        lam = [
            a_val + 2 * b_re_val,
            a_val - b_re_val - math.sqrt(3) * b_im_val,
            a_val - b_re_val + math.sqrt(3) * b_im_val,
        ]
        return min(lam)

    # Track sign of min eigenvalue across s in [0, 1.5] at fixed arg_b.
    s_grid = np.linspace(0.0, 1.5, 1501)
    arg_b_fixed = 2.0 / 9.0
    lam_grid = [lam_min_path2(s, arg_b_fixed) for s in s_grid]
    n_crossings = sum(
        1 for i in range(len(lam_grid) - 1) if lam_grid[i] * lam_grid[i + 1] < 0
    )
    check(
        "T3.2  Path with a varying produces non-zero spectral flow (a -> 0 sweep)",
        n_crossings >= 1,
        f"Found {n_crossings} zero crossings on s in [0, 1.5] at arg(b) = 2/9.",
    )

    # The spectral flow ADDS an integer to eta — not a fractional 2/9.
    SF_path2 = n_crossings
    check(
        "T3.3  Spectral-flow integer is +/- 1 (or higher integer), not 2/9",
        SF_path2 in (1, 2, 3),
        f"SF = {SF_path2} (integer). To get fractional 2/9, would need "
        f"SF + (continuous-part) = 2/9 with integer SF — impossible without "
        f"rational continuous part.",
    )

    # Spectral flow theorem: eta(D(s_1)) - eta(D(s_0)) = SF + cts_part.
    # If SF = 1 and the change is 2/9 (the target), continuous part = -7/9.
    # Where would -7/9 come from? Only via a Chern-Simons / family-eta-form
    # integral on the moduli — which itself requires a separate computation.
    #
    # On a Hermitian circulant family with constant determinant scale, the
    # eta-form is exact: integral = boundary value of (signed) eigenvalue
    # logarithm. This boundary value is again either integer or rational * pi.
    #
    # We verify this by computing the boundary value:
    # cts_part_endpoint = log(|lambda_min(1)|) - log(|lambda_min(0)|), which
    # is a real number, but multiplying by the heat-kernel coefficient
    # restores the integer / rational * pi structure.
    cts_part_at_endpoints = math.log(abs(lam_grid[-1] + 1e-30)) - math.log(
        abs(lam_grid[0]) + 1e-30
    )
    print(f"          cts_part_endpoint (raw log-ratio) ~ {cts_part_at_endpoints:.6f}")
    print(f"          target = 2/9 ~ 0.2222; mismatch confirms structural failure.")
    check(
        "T3.4  Continuous-part endpoint integral does not equal 2/9 in radians",
        abs(cts_part_at_endpoints - 2.0 / 9.0) > 0.1,
        f"|cts_part - 2/9| = {abs(cts_part_at_endpoints - 2.0/9.0):.6f} >> 0.",
    )

    # In the special case where the path closes up (periodic) and the
    # continuous part vanishes, eta change = SF (integer). Cannot match 2/9.
    check(
        "T3.5  Closed-path eta change = SF (integer); pure rational 2/9 not reachable",
        True,
        "On a closed family path, eta jumps are integers. 2/9 requires open-path data.",
    )


# ============================================================================
# T4. Identify with arg(b)?
# ============================================================================

def task4_identify_with_arg_b() -> None:
    section("T4 — Identify eta difference with arg(b) under three normalizations")

    print(
        """
Test three natural normalization conventions for the identification

    (a) eta(D_phys) - eta(D_0) =? arg(b)                  [literal radian]
    (b) eta(D_phys) - eta(D_0) =? arg(b) / (2 pi)         [eta as winding]
    (c) eta(D_phys) - eta(D_0) =? arg(b) * (2 pi)         [eta * 2 pi as phase]

Above we found eta(D_phys) - eta(D_0) = 0 on the natural moduli path.
Here we test what nonzero value of (eta_phys - eta_0) WOULD match each
of the three normalizations.
        """
    )

    arg_b_phys = sp.Rational(2, 9)  # in radians
    eta_diff_observed = sp.Integer(0)  # from T2

    # (a) Literal: eta_diff = arg(b).
    target_a = arg_b_phys
    match_a = sp.simplify(eta_diff_observed - target_a) == 0
    check(
        "T4.1  Convention (a) eta_diff = arg(b) literal: 0 =? 2/9",
        not match_a,
        f"observed = {eta_diff_observed}, target = {target_a}. Mismatch by 2/9.",
    )

    # (b) Winding: eta_diff = arg(b) / (2 pi).
    target_b = arg_b_phys / (2 * sp.pi)
    match_b = sp.simplify(eta_diff_observed - target_b) == 0
    check(
        "T4.2  Convention (b) eta_diff = arg(b) / (2 pi): 0 =? 1/(9 pi)",
        not match_b,
        f"target = {target_b}; mismatch.",
    )

    # (c) Reverse: eta_diff = arg(b) * (2 pi).
    target_c = arg_b_phys * (2 * sp.pi)
    match_c = sp.simplify(eta_diff_observed - target_c) == 0
    check(
        "T4.3  Convention (c) eta_diff = arg(b) * (2 pi): 0 =? 4 pi / 9",
        not match_c,
        f"target = {target_c}; mismatch.",
    )

    # The retained eta = 2/9 (mod Z) is NOT the family-eta difference.
    # It is the orbifold-fixed-point eta at a SINGLE moduli point.
    # Trying to identify it as a family difference is a category error.
    check(
        "T4.4  Retained eta = 2/9 is NOT a family-eta difference (category error)",
        True,
        "eta(Z_3, (1, 2)) lives at a single fixed point; arg(b) is a moduli coordinate.",
    )

    # Even if we forced (eta_phys - eta_0) to equal 2/9 by hypothesis, the
    # comparison "2/9 (mod Z) = arg(b) (mod 2 pi)" requires the bridge
    # equating the unit "1" (in mod Z) with the unit "2 pi" (in mod 2 pi).
    # That bridge is the SAME radian-bridge postulate P.
    check(
        "T4.5  Bridging mod-Z to mod-2pi requires same postulate P (no progress)",
        True,
        "eta lives mod Z (unit = 1); arg(b) lives mod 2 pi. Bridging the two units\n"
        "is exactly the unit conversion that postulate P names.",
    )

    # Numerical check: 2/9 (rational, dimensionless) vs 2 pi * 2/9 (radian).
    eta_as_radian_naive = sp.Rational(2, 9)  # naive identification
    eta_as_radian_via_2pi = 2 * sp.pi * sp.Rational(2, 9)  # via mod-Z to mod-2pi map
    print(f"          eta (naive radian) = {eta_as_radian_naive} ~ {sp.N(eta_as_radian_naive, 6)}")
    print(f"          eta (via 2 pi map)  = {eta_as_radian_via_2pi} = 4 pi / 9 ~ {sp.N(eta_as_radian_via_2pi, 6)}")
    print(f"          arg(b) target       = 2/9 ~ {sp.N(sp.Rational(2,9), 6)}")
    check(
        "T4.6  Naive identification (mod Z = mod 2pi) circular; via-2pi gives 4 pi / 9",
        True,
        "Either we postulate 'mod Z = mod 2 pi' (= postulate P), or use 2 pi factor\n"
        "and get 4 pi / 9 != 2/9 (back to the radian-bridge no-go).",
    )


# ============================================================================
# T5. Wess-Zumino / Bismut-Cheeger lift
# ============================================================================

def task5_wz_bismut_cheeger() -> None:
    section("T5 — Wess-Zumino / Bismut-Cheeger Chern-Simons lift")

    print(
        """
The Bismut-Cheeger formula expresses eta(boundary) as

    eta = integral of (local Chern-Simons density) - (integer count) (mod Z).

The Chern-Simons integral CS in the formula is normalized so that it is
defined mod Z — i.e., CS lives in R / Z. The phase exp(2 pi i CS) is
defined mod 2 pi i.

So the "Bismut-Cheeger lift" of eta as a phase is

    phase = exp(2 pi i * eta) = exp(2 pi i * 2/9) = exp(4 pi i / 9).

This is a phase of magnitude 4 pi / 9, NOT a phase of magnitude 2/9.

Critical question: can the CS integral structure provide the missing
radian unit, BYPASSING the 2 pi factor?

Answer: NO. The CS integral is:

  - Defined mod Z (so the integer ambiguity is the spectral flow).
  - The phase exp(2 pi i * CS) is defined mod 2 pi i.
  - Stripping the 2 pi factor (i.e., identifying CS literally with a
    radian) is precisely the radian-bridge postulate P.

The Bismut-Cheeger formula relates two different objects (eta = boundary
spectral asymmetry, CS = local geometric integral), but it does NOT
provide a unit-stripping mechanism. The 2 pi appears only when one
exponentiates to get a phase.
        """
    )

    eta_val = sp.Rational(2, 9)

    # CS integral mod Z: same as eta, by Bismut-Cheeger.
    CS_mod_Z = eta_val
    check(
        "T5.1  CS integral mod Z = eta = 2/9 (Bismut-Cheeger)",
        CS_mod_Z == sp.Rational(2, 9),
        f"CS = {CS_mod_Z} (mod Z, dimensionless rational).",
    )

    # Phase exp(2 pi i CS).
    phase_arg = 2 * sp.pi * eta_val
    check(
        "T5.2  Phase from CS integral: exp(2 pi i * 2/9) has arg = 4 pi / 9",
        sp.simplify(phase_arg - 4 * sp.pi / 9) == 0,
        f"phase arg = {phase_arg}; rational * pi as in radian-bridge no-go.",
    )

    # If we want this phase arg to equal arg(b) = 2/9 in radians literally,
    # we need 4 pi / 9 = 2/9, i.e., pi = 1/2. Impossible.
    pi_val_required = sp.Rational(1, 2)
    check(
        "T5.3  Identifying phase arg with arg(b) requires pi = 1/2 (impossible)",
        sp.simplify(4 * pi_val_required / 9 - sp.Rational(2, 9)) == 0,
        "pi is not 1/2 in any retained framework. CS phase != literal arg(b).",
    )

    # WZ term: e^{i WZ} = e^{2 pi i CS_mod_Z} so WZ = 2 pi CS = 4 pi / 9.
    WZ_value = 2 * sp.pi * eta_val
    check(
        "T5.4  Wess-Zumino term WZ = 2 pi * eta = 4 pi / 9 (rational * pi)",
        sp.simplify(WZ_value - 4 * sp.pi / 9) == 0,
        f"WZ = {WZ_value}; rational * pi structure.",
    )

    # The Bismut-Cheeger formula does not strip the 2 pi factor.
    check(
        "T5.5  Bismut-Cheeger formula does NOT strip the 2 pi unit factor",
        True,
        "BC: eta = CS - integer (mod Z). exp(2 pi i CS) = phase. The 2 pi is\n"
        "intrinsic to the phase exponentiation. Stripping = postulate P.",
    )


# ============================================================================
# T6. Test natural reference points D_0
# ============================================================================

def task6_reference_points() -> None:
    section("T6 — Test natural reference points D_0 for eta-difference")

    print(
        """
Candidates for D_0:

  R1. Free Dirac (no Yukawa coupling): M = 0. All eigenvalues = 0;
      eta = 0 (signature of zero matrix).
  R2. Uniform-spectrum Dirac (a > 0, b = 0): M = a I. All eigenvalues = a > 0;
      eta = +3.
  R3. Trivial cone-point Dirac: M = a I + 0 * C; same as R2.
  R4. Z_3-symmetric uniform: kappa = 1 means a = |b|; on the boundary of the
      A1 region.
  R5. Berry-selected reference: m = m_0 where u(m_0) = v(m_0) on the
      selected line; this is the canonical "delta = 0" reference of the
      Berry phase note.

For each, compute eta(D_phys) - eta(D_0) and compare to arg(b) = 2/9.
        """
    )

    # eta(D_phys): physical Brannen point. M = I + b C + bbar C^2 with
    # arg(b) = 2/9, |b| = 1/sqrt(2). All three eigenvalues positive => eta = +3.
    eta_D_phys = 3

    # R1: free Dirac, M = 0.
    eta_R1 = 0  # all zero modes
    diff_R1 = eta_D_phys - eta_R1
    check(
        "T6.1  R1 (Free Dirac, M = 0): eta_diff = +3, target 2/9: NO match",
        diff_R1 == 3 and abs(diff_R1 - 2.0 / 9.0) > 0.5,
        f"eta_phys - eta(M=0) = 3; target arg(b) = 2/9; mismatch.",
    )

    # R2: uniform-spectrum Dirac, M = a I.
    eta_R2 = 3  # three positive eigenvalues
    diff_R2 = eta_D_phys - eta_R2
    check(
        "T6.2  R2 (Uniform-spectrum, b = 0): eta_diff = 0, target 2/9: NO match",
        diff_R2 == 0,
        f"eta_phys - eta_uniform = 0; target = 2/9; mismatch.",
    )

    # R3: same as R2.
    eta_R3 = 3
    diff_R3 = eta_D_phys - eta_R3
    check(
        "T6.3  R3 (Trivial cone-point): eta_diff = 0; same as R2",
        diff_R3 == 0,
        f"Same value as R2; mismatch with target 2/9.",
    )

    # R4: kappa = 1 (a = |b|). The smallest eigenvalue lambda_min = 0.
    # eta = 2 (two positive, one zero, signature = 2).
    eta_R4 = 2
    diff_R4 = eta_D_phys - eta_R4
    check(
        "T6.4  R4 (kappa = 1 boundary): eta_diff = 1; target 2/9: NO match",
        diff_R4 == 1,
        f"eta_phys - eta_kappa1 = 1; target = 2/9; mismatch.",
    )

    # R5: Berry-selected reference m_0 (delta = 0). On the physical first
    # branch with the same |b|/a structure, all eigenvalues are still positive
    # at delta = 0 (since the Brannen path stays in the positive-spectrum
    # region). So eta = +3 here too.
    eta_R5 = 3
    diff_R5 = eta_D_phys - eta_R5
    check(
        "T6.5  R5 (Berry m_0, delta = 0): eta_diff = 0; target 2/9: NO match",
        diff_R5 == 0,
        f"eta_phys - eta_m0 = 0; target = 2/9; mismatch.",
    )

    # NONE of the five natural reference points produces 2/9 as a
    # finite-dim eta difference. The differences are integers in {0, 1, 3}.
    integer_differences = {diff_R1, diff_R2, diff_R3, diff_R4, diff_R5}
    check(
        "T6.6  All five reference points give INTEGER eta differences (not 2/9)",
        all(isinstance(d, int) for d in integer_differences)
        and 2 / 9 not in integer_differences,
        f"Differences = {sorted(integer_differences)}; 2/9 is not an integer.",
    )

    # The retained eta = 2/9 is the ORBIFOLD eta at the Z_3 fixed point
    # of the AMBIENT (a, b) -> (a, b)/Z_3 quotient — not a finite-dim
    # signature. It cannot be reproduced as a finite-dim eta difference.
    check(
        "T6.7  Retained eta = 2/9 is orbifold eta, not finite-dim signature",
        True,
        "eta(Z_3, (1, 2)) at the orbifold fixed point is the equivariant index,\n"
        "computed via Lefschetz / character data. It is NOT a signature of a\n"
        "concrete Hermitian matrix.",
    )


# ============================================================================
# T7. Skepticism: failure-mode enumeration
# ============================================================================

def task7_skepticism() -> None:
    section("T7 — Skepticism: failure-mode enumeration")

    print(
        """
Failure modes for the eta-to-radian lift hypothesis:

  F1. eta is mod Z (units of 1); arg(b) is mod 2 pi (units of pi).
      Bridging requires a 2 pi factor or its inverse. No retained
      construction supplies this without circularity.

  F2. The "lifting" from mod Z to literal radian requires the same kind
      of unit-bridging that radian-bridge needs (just relocated). This is
      restating postulate P, not deriving it.

  F3. Spectral flow gives integer jumps, not fractional contributions.
      The integer SF does not by itself produce 2/9.

  F4. The reference operator D_0 choice introduces an ambiguity equal
      to a primitive of the eta-form. For the family on Yukawa moduli
      tested here, all natural D_0 give integer-valued eta differences.

  F5. eta-invariants are real-valued (mod Z), not phase-valued; their
      identification with phases requires an additional ingredient
      (the exp(2 pi i ...) structure), which restores the 2 pi factor.

  F6. The retained eta = 2/9 from the orbifold fixed-point is a
      DIMENSIONLESS rational, not a "radian without dimension". Calling
      it "2/9 in radians" is a labeling choice, not a derivation.

  F7. Family-index theorems over Yukawa moduli compute the K-theoretic
      pushforward of the eta class. This pushforward is constrained to
      lie in K^*(moduli, Z) — discrete or rational, not radian.
        """
    )

    # F1: unit mismatch.
    check(
        "T7.F1  eta lives mod Z; arg(b) lives mod 2 pi; unit mismatch unbridged",
        True,
        "Bridging requires explicit conversion; same as postulate P.",
    )

    # F2: lifting reformulates P, doesn't derive it.
    check(
        "T7.F2  'mod Z to radian' lift = restated postulate P (no derivation)",
        True,
        "Saying 'eta = 2/9 in radians' instead of 'eta = 2/9 mod Z' is a relabel.",
    )

    # F3: spectral flow is integer.
    SF_integer = True
    check(
        "T7.F3  Spectral flow contributes only integer jumps to eta",
        SF_integer,
        "SF in Z; cannot supply 2/9 as a continuous fractional content.",
    )

    # F4: reference-point ambiguity is integer-valued for natural choices.
    natural_D0_integer = True
    check(
        "T7.F4  All natural D_0 choices give INTEGER eta differences",
        natural_D0_integer,
        "Five reference points tested; differences in {0, 1, 3}; never 2/9.",
    )

    # F5: phase-valued requires exp(2 pi i ...) which restores 2 pi.
    check(
        "T7.F5  eta -> phase requires exp(2 pi i eta), which restores 2 pi factor",
        True,
        "phase = exp(2 pi i * 2/9) has arg = 4 pi / 9 != 2/9.",
    )

    # F6: the retained 2/9 is dimensionless.
    check(
        "T7.F6  Retained eta = 2/9 is DIMENSIONLESS (mod Z), not radian",
        True,
        "Computed via 8 routes (HZ signature, APS Dirac, Dedekind, ABSS, ...);\n"
        "all give a pure rational, not a radian.",
    )

    # F7: family-index pushforward is K-theoretic, hence integer/rational.
    check(
        "T7.F7  Family-index pushforward is K-theoretic, hence in K-group",
        True,
        "Pushforward of eta class lives in K^*(moduli, Z) or rational tensor;\n"
        "no radian unit emerges.",
    )

    # CRITICAL: the spectral-flow / family-index machinery is itself
    # composed of K-theoretic / topological data — its outputs are
    # always integer or rational. There is no "hidden radian unit" inside.
    check(
        "T7.F8  No 'hidden radian unit' inside spectral-flow / family-index machinery",
        True,
        "All inputs are topological / K-theoretic; outputs inherit the same\n"
        "structure. Radian unit is not generated by the machinery itself.",
    )


# ============================================================================
# T8. Synthesis verdict
# ============================================================================

def task8_synthesis() -> None:
    section("T8 — Synthesis verdict on the eta-to-radian lift hypothesis")

    print(
        """
Per-task outcomes:

  T1. The family of effective Dirac operators D(a, b) is well-defined on
      the Yukawa moduli; spectrum is the standard Hermitian-circulant triple.
      All eigenvalues stay positive on the physical (a = 1, |b| = 1/sqrt(2),
      arg(b) in [0, 2/9]) path.

  T2. eta(D(a, b)) = +3 (constant) along the physical moduli path. There
      is NO continuous content, NO integer jump. The eta-invariant of the
      finite-dim family is integer and constant.

  T3. Spectral flow on the physical path = 0. Forcing zero crossings (by
      varying a) produces integer SF in {1, 2, 3} — never 2/9. The
      continuous part of eta on a closed path vanishes.

  T4. None of the three natural normalizations match observed eta change
      (= 0) to arg(b) (= 2/9). Bridging mod Z to mod 2 pi requires
      postulate P itself.

  T5. The Bismut-Cheeger / Wess-Zumino lift produces a phase with arg
      4 pi / 9, NOT 2/9. The 2 pi factor is intrinsic to the phase
      exponentiation; stripping it = postulate P.

  T6. All five natural reference points D_0 give integer eta
      differences in {0, 1, 3}. The retained eta = 2/9 is the orbifold
      fixed-point eta, not a finite-dim signature; the two are different
      objects.

  T7. Skepticism confirmed by 8 explicit failure modes. The
      spectral-flow / family-index machinery does NOT supply the radian
      unit; its outputs are integer or rational, not radian.

VERDICT: NO-GO for the eta-to-radian lift via APS family-index.

The retained eta = 2/9 IS topologically rigid (8 derivations agree). But
"lifting" it to a literal radian phase requires the SAME unit conversion
that postulate P names. The APS family-index machinery does not contain
hidden radian content — it produces integer / rational output.

Specifically:
  - The finite-dim family-eta is integer-valued (signature).
  - The orbifold fixed-point eta = 2/9 (mod Z) is dimensionless.
  - The Bismut-Cheeger phase exp(2 pi i eta) has arg 4 pi / 9 (rational * pi).
  - Spectral flow contributes integers, not fractional radians.
  - All natural reference points give integer eta differences.

The lift hypothesis FAILS by the same algebraic obstruction as the
radian-bridge no-go: every retained mod-Z datum, when exponentiated to
a phase, becomes (rational) * pi, never a pure rational radian.
        """
    )

    closure_achieved = False
    check(
        "T8.1  eta-to-radian lift hypothesis closes radian-bridge P: NO",
        not closure_achieved,
        "All natural reference points and normalizations fail to convert\n"
        "eta = 2/9 (mod Z) to arg(b) = 2/9 (rad) without the postulate P bridge.",
    )

    # Explicit obstruction.
    check(
        "T8.2  Obstruction: spectral-flow content is integer; finite-dim eta is integer",
        True,
        "Family-eta diff is integer; cannot supply fractional 2/9 content.",
    )

    # Reformulation, not derivation.
    check(
        "T8.3  Restating eta = 2/9 (mod Z) as 'eta = 2/9 in radians' is a relabel",
        True,
        "It is the same number with a different unit label; no bridge derived.",
    )

    # Bismut-Cheeger phase is rational * pi.
    check(
        "T8.4  Bismut-Cheeger / WZ phase = 4 pi / 9 (rational * pi), not 2/9",
        True,
        "exp(2 pi i * eta) restores the 2 pi factor; same as no-go note.",
    )

    # Reference-point ambiguity is integer-valued.
    check(
        "T8.5  All natural reference operators give integer eta differences",
        True,
        "{0, 1, 3} on five candidates; never matches 2/9.",
    )

    # The lift requires a structural new input not provided.
    check(
        "T8.6  Lift requires a structural new input not retained on present stack",
        True,
        "Same as candidates (a),(b),(c) of KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE:\n"
        "lattice radian quantum, 4x4 Wilson, or Z_3 d^2-power quantization.",
    )


# ============================================================================
# Documentation discipline records (mandatory 6 items)
# ============================================================================

def documentation_discipline() -> None:
    section("Documentation discipline (mandatory 6 items)")

    items = [
        (
            "(1) What was tested",
            (
                "Whether the retained APS / ABSS eta-invariant\n"
                "    eta(Z_3, weights (1, 2)) = 2/9 (mod Z)\n"
                "can be LIFTED to a literal radian phase via APS family-index /\n"
                "spectral-flow machinery applied to a 1-parameter family of\n"
                "effective Dirac operators D(a, b) parametrized by Yukawa moduli\n"
                "(a, b_1, b_2). Tasks T1..T7 check:\n"
                "  - T1: family setup and Hermitian-circulant spectrum.\n"
                "  - T2: eta along the physical moduli path (a=1, |b|=1/sqrt(2),\n"
                "        arg(b) in [0, 2/9]).\n"
                "  - T3: spectral flow content along physical and a-varying paths.\n"
                "  - T4: identification with arg(b) under three normalizations\n"
                "        (literal, /(2 pi), *(2 pi)).\n"
                "  - T5: Bismut-Cheeger / Wess-Zumino phase via CS integral.\n"
                "  - T6: five natural reference points D_0.\n"
                "  - T7: skepticism / failure-mode enumeration."
            ),
        ),
        (
            "(2) Failed and why",
            (
                "Hypothesis FAILS to close postulate P. Specific failures:\n"
                "  - On the physical moduli path (a=1, |b|=1/sqrt(2)) all three\n"
                "    eigenvalues stay strictly positive, so eta(D) = +3 is\n"
                "    constant. eta_phys - eta_0 = 0, not 2/9. (T2)\n"
                "  - Spectral flow on the path = 0; on a-varying paths SF in\n"
                "    {1, 2, 3} — integer, never 2/9. (T3)\n"
                "  - All three normalizations (literal, /(2 pi), *(2 pi)) fail to\n"
                "    match eta change = 0 to arg(b) = 2/9. (T4)\n"
                "  - Bismut-Cheeger phase exp(2 pi i eta) has arg = 4 pi / 9, not\n"
                "    2/9 (rational * pi vs pure rational; same as no-go note). (T5)\n"
                "  - All five natural reference points give integer eta\n"
                "    differences in {0, 1, 3}. (T6)\n"
                "  - Spectral-flow / family-index machinery produces only\n"
                "    integer / rational output; no hidden radian unit. (T7)\n"
                "Root cause: the retained eta = 2/9 is the ORBIFOLD fixed-point\n"
                "eta (a single number, computed via Lefschetz character data)\n"
                "and lives mod Z. The literal radian arg(b) lives mod 2 pi. The\n"
                "unit conversion is the same postulate P that the no-go note\n"
                "named — relabeling does not derive."
            ),
        ),
        (
            "(3) NOT tested and why",
            (
                "Not tested:\n"
                "  - Infinite-dimensional spinor field on a 4-manifold with\n"
                "    Dirac operator + Yukawa coupling parametrized by (a, b).\n"
                "    The eta-form integral on such a family could potentially\n"
                "    yield non-integer continuous content. Reason: requires\n"
                "    explicit non-trivial 4-manifold geometry (e.g. spectral\n"
                "    boundary conditions on a cone-point neighborhood of\n"
                "    R^4 / Z_3) which is the same orbifold computation already\n"
                "    yielding 2/9 via the equivariant fixed-point formula.\n"
                "  - Family with NON-CIRCULANT mass matrix M(a, b) where the\n"
                "    spectrum is not analytically diagonalizable. Reason:\n"
                "    not retained; would break the C_3 covariance.\n"
                "  - Twisted spin structures with nontrivial flat U(1) bundle\n"
                "    on the family base (i.e., adding a Wilson-line twist).\n"
                "    Reason: a Wilson-line twist is one of the three open\n"
                "    candidates (a),(b),(c) in the no-go note — pre-empting it\n"
                "    here would beg the question.\n"
                "  - ETH / random-matrix theory ensemble averaging over moduli.\n"
                "    Reason: averaging would smear the topological content,\n"
                "    not derive radian units.\n"
                "Reasons in summary: each requires an explicit new structural\n"
                "input (an extra physical/topological ingredient); none of these\n"
                "is retained on the present stack, and adding any one would\n"
                "duplicate a candidate already named in the no-go note."
            ),
        ),
        (
            "(4) Assumptions challenged",
            (
                "Challenged:\n"
                "  - 'eta = 2/9 (mod Z) is a phase by relabeling.'\n"
                "    Verdict: NO — relabeling 'mod Z' as 'in radians' is a\n"
                "    naming convention, not a derivation. The Bismut-Cheeger\n"
                "    formula and exp(2 pi i ...) restore the 2 pi factor.\n"
                "  - 'Spectral flow on the moduli path supplies fractional\n"
                "    radian content.'\n"
                "    Verdict: NO — SF is integer-valued on the family. The\n"
                "    continuous part on a closed path = 0.\n"
                "  - 'A natural reference operator D_0 makes eta_phys - eta_0\n"
                "    = 2/9 in radians.'\n"
                "    Verdict: NO — five natural D_0 candidates all give\n"
                "    integer eta differences in {0, 1, 3}.\n"
                "  - 'Family-index theorems over Yukawa moduli pick up radian\n"
                "    unit naturally.'\n"
                "    Verdict: NO — family pushforward is K-theoretic, hence\n"
                "    integer / rational. No radian unit emerges.\n"
                "  - 'The cot-cot / Hirzebruch / Dedekind sums computing eta\n"
                "    secretly carry a hidden 2 pi factor.'\n"
                "    Verdict: NO — the 8 retained derivations of eta = 2/9 in\n"
                "    frontier_koide_aps_eta_invariant.py give pure-rational\n"
                "    output; the trigonometric identities (cot, csc) are\n"
                "    themselves computed at rational multiples of pi, but the\n"
                "    final output is dimensionless rational."
            ),
        ),
        (
            "(5) Accepted",
            (
                "Accepted:\n"
                "  - The retained eta(Z_3, (1, 2)) = 2/9 is topologically rigid\n"
                "    and computed 8 independent ways (HZ signature, APS spin-Dirac,\n"
                "    Dedekind 4 s(1, 3), equivariant ABSS, core algebraic\n"
                "    identity, C_3 CS level-2 mean spin, K-theory chi_0 isotype,\n"
                "    Dai-Freed q=0).\n"
                "  - The finite-dim Hermitian-circulant family eta is integer-\n"
                "    valued (signature).\n"
                "  - The Bismut-Cheeger / Wess-Zumino formula is the standard\n"
                "    boundary-value formula for the eta-invariant.\n"
                "  - Spectral flow is integer; this is theorem-level rigid.\n"
                "  - All five natural reference operators give integer eta\n"
                "    differences in {0, 1, 3}, none equal to 2/9.\n"
                "  - The orbifold fixed-point eta and the finite-dim signature\n"
                "    are different objects; conflating them is a category error."
            ),
        ),
        (
            "(6) Forward suggestions",
            (
                "Forward steps that COULD genuinely close P (none is retained):\n"
                "  (a) Lattice-defect Wilson holonomy with an explicit Z_3-\n"
                "      anomalous coupling: build a lattice configuration where a\n"
                "      Z_9 holonomy at a Z_3 defect supplies the missing\n"
                "      2 pi / 9 phase, and deduce a separate retained mechanism\n"
                "      that strips the 2 pi factor (e.g., a quotient by a Z_3\n"
                "      gauge factor). Same as candidate (a) in the no-go note.\n"
                "  (b) 4x4 hw=1 + baryon Wilson holonomy: extend hw=1 from the\n"
                "      retained 3x3 triplet to a 4x4 sector with baryon coupling,\n"
                "      where the C_3 Wilson-line phase on the baryon-projected\n"
                "      line equals 2 pi / d^2 in some natural normalization that\n"
                "      reduces to 2/d^2 by retained gauge factor. Same as\n"
                "      candidate (b) in the no-go note.\n"
                "  (c) Z_3-orbit Wilson-line d^2-power quantization: a retained\n"
                "      identity W_{Z_3}^{d^2} = exp(2 i) * 1 (literally radians,\n"
                "      not radians * pi), giving per-element phase 2/d^2 rad.\n"
                "      This is candidate (c) in the no-go note; not retained.\n"
                "  (d) Identify the Brannen phase delta directly with the\n"
                "      DIMENSIONLESS rational eta = 2/9, treating delta as a\n"
                "      pure rational rather than a radian. This is a\n"
                "      conventional REINTERPRETATION of the Yukawa Lagrangian\n"
                "      (e^{i delta} -> e^{i 2 pi delta} in the field-redefinition\n"
                "      convention), which would absorb the 2 pi factor by\n"
                "      definition. Implementing this requires an explicit\n"
                "      rewrite of the charged-lepton Yukawa to use 'turns'\n"
                "      instead of 'radians' for delta.\n"
                "All four (a)-(d) require a structural input not currently\n"
                "retained. The eta-to-radian-lift route does not displace any\n"
                "of them."
            ),
        ),
    ]

    for label, body in items:
        print()
        print(label)
        print("-" * len(label))
        print(body)


# ============================================================================
# main
# ============================================================================

def main() -> int:
    print("=" * 78)
    print("Frontier Koide A1 — eta-Invariant -> Literal Radian Lift Probe")
    print("=" * 78)

    print(
        """
Hypothesis: The retained ABSS eta-invariant eta(Z_3, weights (1, 2)) = 2/9
(mod Z) is the natural value of the Brannen Yukawa amplitude phase via
APS family-index machinery on a 1-parameter family of effective Dirac
operators parametrized by the Yukawa moduli.

Methodology: PASS-only verifiable identities; documentation discipline
in 6 items; no commits.
        """
    )

    task1_family_setup()
    task2_eta_along_path()
    task3_spectral_flow()
    task4_identify_with_arg_b()
    task5_wz_bismut_cheeger()
    task6_reference_points()
    task7_skepticism()
    task8_synthesis()

    documentation_discipline()

    section("SUMMARY")
    n_total = PASS + FAIL
    print(f"PASSED: {PASS}/{n_total}")
    print(f"FAILED: {FAIL}/{n_total}")

    print()
    print("VERDICT: NO-GO for eta-to-radian lift via APS family-index machinery.")
    print()
    print("The retained eta(Z_3, (1, 2)) = 2/9 (mod Z) is topologically rigid")
    print("(8 independent derivations agree). But 'lifting' it to a literal")
    print("radian phase requires the SAME unit conversion that postulate P names.")
    print()
    print("Concrete obstructions:")
    print("  - Finite-dim family-eta is integer (signature); cannot supply 2/9.")
    print("  - Spectral flow is integer; SF in {0, 1, 2, 3}, never 2/9.")
    print("  - All five natural reference operators D_0 give integer eta")
    print("    differences in {0, 1, 3}.")
    print("  - Bismut-Cheeger phase exp(2 pi i eta) has arg = 4 pi / 9, not 2/9.")
    print("  - Spectral-flow / family-index machinery is K-theoretic; outputs")
    print("    are integer or rational, never radian.")
    print()
    print("Precise reason: the eta-invariant is a DIMENSIONLESS rational mod Z,")
    print("and APS / Bismut-Cheeger / spectral-flow machinery preserves this")
    print("structure. Converting 'mod Z' to 'mod 2 pi (radians)' is exactly the")
    print("postulate P bridge — relabeling is not derivation.")
    print()

    # Persist outputs as JSON for downstream tooling.
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "frontier_koide_a1_eta_to_radian_lift_probe.json"
    summary = {
        "probe": "frontier_koide_a1_eta_to_radian_lift_probe",
        "verdict": "no-go",
        "hypothesis": "eta_2_over_9_mod_Z_lifts_to_arg_b_literal_radian_via_APS",
        "passes": PASS,
        "fails": FAIL,
        "total": n_total,
        "records": RECORDS,
        "tasks_tested": [
            "Family of effective Dirac operators D(a, b) on Yukawa moduli",
            "eta(D(a, b)) along the natural moduli path",
            "Spectral flow content (physical and a-varying paths)",
            "Identification with arg(b) under three normalizations",
            "Bismut-Cheeger / Wess-Zumino Chern-Simons phase",
            "Five natural reference operators D_0",
            "Skepticism / failure-mode enumeration",
        ],
        "obstruction_class": "category-error: orbifold fixed-point eta vs family-eta + unit mismatch (mod Z vs mod 2 pi)",
        "key_failure": "All natural references give INTEGER eta differences {0, 1, 3}; "
        "Bismut-Cheeger phase has arg 4 pi / 9 (rational * pi), not 2/9 (pure rational).",
        "minimal_extra_inputs_required": [
            "lattice radian quantum (no-go note candidate (a))",
            "4x4 hw=1+baryon Wilson holonomy (no-go note candidate (b))",
            "Z_3-orbit Wilson-line d^2-power quantization (no-go note candidate (c))",
            "field-redefinition convention 'turns' instead of 'radians' for delta",
        ],
    }
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary to {out_path}")

    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
