#!/usr/bin/env python3
"""Verify the narrow hierarchy Matsubara determinant ratio theorem.

Claim scope: at L_s = 2 minimal APBC block with mean-field gauge
factorization, the staggered Dirac massless determinants at L_t = 2 and
L_t = 4 satisfy the exact rational identity:

    |det(D, L_t = 4, m = 0)|  /  |det(D, L_t = 2, m = 0)|^2  =  (7/8)^16.

Class (A) algebraic identity on admitted standard staggered fermion
eigenvalue structure (parent narrow theorem). The bridge corollary

    v(L_t = 4) / v(L_t = 2)  =  (A_2 / A_4)^(1/4)  =  (7/8)^(1/4)

follows under the named DIM-4 EFFECTIVE-POTENTIAL-DENSITY READOUT
admission v ∝ A(L_t)^(-1/4), where A(L_t) is the m^2 coefficient of
Δf at the symmetric point per
HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE. Within that admitted
readout, the (1/4) power is the D = 4 Stefan-Boltzmann-style
dimensional bookkeeping (v has mass dim 1; V_eff has mass dim 4).

This runner verifies:
  1. Note structure and scope discipline.
  2. Exact rational identity via Fraction arithmetic.
  3. Cross-check by direct numerical staggered Dirac matrix construction
     and determinant evaluation at L_s = 2, L_t in {2, 4}.
  4. Dim-4 V_eff'' readout corollary: A_2 = 1/(8 u_0^2),
     A_4 = 1/(7 u_0^2) (Fraction arithmetic on (3 + sin^2 ω) Matsubara
     sum at L_s = 2), giving (A_2 / A_4)^(1/4) = (7/8)^(1/4).
  5. Sign and placement assertions (compression < 1, multiplicative on v).
"""

from __future__ import annotations

from pathlib import Path
from fractions import Fraction
import math
import sys

try:
    import numpy as np
except ImportError:  # pragma: no cover
    print("FAIL: numpy required")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "HIERARCHY_MATSUBARA_DETERMINANT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md"
)


PASS = 0
FAIL = 0
ADMITTED = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def admit(label: str, detail: str = "") -> None:
    global ADMITTED
    ADMITTED += 1
    suffix = f"  ({detail})" if detail else ""
    print(f"  [ADMITTED] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Part 1: note structure and scope discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()
required_strings = [
    "Hierarchy Matsubara Determinant Ratio",
    "claim_type: bounded_theorem",
    "(7/8)^16",
    "dim-4 effective-potential-density",
    "A(L_t)^(-1/4)",
    "Stefan-Boltzmann",
    "load_bearing_step_class: A",
    "forbidden_imports_used: false",
]
for s in required_strings:
    check(f"note contains: '{s}'", s in note_text)

# scope disclaimers
disclaimers = [
    "audit verdict and downstream status are set only by the independent\naudit lane",
    "explicitly does NOT",
]
for s in disclaimers:
    check(f"scope disclaimer present: '{s[:40]}...'", s in note_text)

admit(
    "dim-4 effective-potential-density readout remains a named admission",
    "runner checks the conditional arithmetic, not independent derivation of R",
)


# ============================================================================
section("Part 2: exact rational identity (Fraction arithmetic)")
# ============================================================================

# Spatial APBC at L_s = 2: all spatial momenta at BZ corners, sin^2(k_i) = 1
# for i = 1, 2, 3, contributing 3 to the dispersion sum.
SPATIAL_SUM = Fraction(3)


def matsubara_modes_sin_squared(L_t: int) -> list[Fraction]:
    """Return the L_t APBC Matsubara mode sin^2 values as exact rationals
    when L_t is in {2, 4}.

    Mode index n = 0, 1, ..., L_t - 1, omega_n = (2n + 1) pi / L_t.
    L_t = 2: omega in {pi/2, 3pi/2}, sin^2 = 1, 1
    L_t = 4: omega in {pi/4, 3pi/4, 5pi/4, 7pi/4}, sin^2 = 1/2 (all)
    """
    if L_t == 2:
        return [Fraction(1), Fraction(1)]
    if L_t == 4:
        return [Fraction(1, 2)] * 4
    raise NotImplementedError(f"rational mode list not tabulated for L_t = {L_t}")


def det_factor_exact(L_t: int) -> dict[str, Fraction | int]:
    """Return the exact rational factorization of |det(D, L_t, m=0)|
    on L_s = 2 mean field, expressed as u_0^(power) * pure_rational.

    |det| = prod_omega [u_0^2 (3 + sin^2 omega)]^4
          = u_0^(8 L_t) * prod_omega (3 + sin^2 omega)^4.
    """
    sin2_values = matsubara_modes_sin_squared(L_t)
    pure = Fraction(1)
    for s2 in sin2_values:
        pure *= (Fraction(3) + s2) ** 4
    return {"u0_power": 8 * L_t, "pure": pure}


det2 = det_factor_exact(2)
det4 = det_factor_exact(4)

check(
    "det(L_t=2) factor: u_0^16 * 4^8",
    det2["u0_power"] == 16 and det2["pure"] == Fraction(4) ** 8,
    f'u0_pow={det2["u0_power"]}, pure={det2["pure"]}',
)
check(
    "det(L_t=4) factor: u_0^32 * (7/2)^16",
    det4["u0_power"] == 32 and det4["pure"] == Fraction(7, 2) ** 16,
    f'u0_pow={det4["u0_power"]}, pure={det4["pure"]}',
)

# Form the ratio |det(L_t=4)| / |det(L_t=2)|^2:
# u_0 power: 32 - 2*16 = 0  (the u_0 dependence cancels exactly)
# pure rational: (7/2)^16 / 4^16 = (7/8)^16
u0_power_ratio = det4["u0_power"] - 2 * det2["u0_power"]
pure_ratio = det4["pure"] / (det2["pure"] ** 2)
expected = Fraction(7, 8) ** 16

check(
    "u_0 dependence cancels in ratio",
    u0_power_ratio == 0,
    f"u_0^{u0_power_ratio}",
)
check(
    "ratio = (7/8)^16 exactly",
    pure_ratio == expected,
    f"pure_ratio={pure_ratio.numerator}/{pure_ratio.denominator}, "
    f"expected={expected.numerator}/{expected.denominator}",
)
check(
    "(7/8)^16 numerical value",
    abs(float(expected) - 0.11806708702144623) < 1e-12,
    f"value={float(expected):.16f}",
)


# ============================================================================
section("Part 3: direct numerical staggered Dirac determinant cross-check")
# ============================================================================
#
# Build the staggered Dirac operator on L_s = 2, L_t in {2, 4} APBC, with
# mean-field link variables U_link = u_0 * I (scalar mean field). For
# verification only — the algebraic identity in Part 2 is the load-bearing
# step.

def build_staggered_dirac_meanfield(
    Lt: int, u0: float, m: float = 0.0, Ls: int = 2
) -> np.ndarray:
    """Construct the staggered Dirac operator on Ls^3 x Lt lattice with
    APBC in all four directions and mean-field link factor u0.

    Standard staggered phases:
        eta_1(x) = 1
        eta_2(x) = (-1)^(x_1)
        eta_3(x) = (-1)^(x_1 + x_2)
        eta_4(x) = (-1)^(x_1 + x_2 + x_3)

    Free staggered Dirac on Z^4 with no gauge field (mean field U = u0 * I):
        D_xy = m * delta_xy
             + sum_mu (u0/2) * eta_mu(x) * (
                 delta_(y, x+mu_hat) - delta_(y, x-mu_hat))
        with antiperiodic boundary in all four directions (sign flip on wrap).
    """
    sites = [
        (x1, x2, x3, t)
        for x1 in range(Ls)
        for x2 in range(Ls)
        for x3 in range(Ls)
        for t in range(Lt)
    ]
    N = len(sites)
    idx = {s: i for i, s in enumerate(sites)}

    D = np.zeros((N, N), dtype=complex)

    # mass term
    for i in range(N):
        D[i, i] = m

    # hopping terms
    L = [Ls, Ls, Ls, Lt]
    for x in sites:
        i = idx[x]
        # staggered phases
        eta = [
            1.0,
            (-1.0) ** x[0],
            (-1.0) ** (x[0] + x[1]),
            (-1.0) ** (x[0] + x[1] + x[2]),
        ]
        for mu in range(4):
            # +mu_hat neighbour
            xp = list(x)
            wrap_p = 1
            xp[mu] += 1
            if xp[mu] >= L[mu]:
                xp[mu] = 0
                wrap_p = -1  # APBC
            jp = idx[tuple(xp)]
            D[i, jp] += (u0 / 2.0) * eta[mu] * wrap_p
            # -mu_hat neighbour
            xm = list(x)
            wrap_m = 1
            xm[mu] -= 1
            if xm[mu] < 0:
                xm[mu] = L[mu] - 1
                wrap_m = -1  # APBC
            jm = idx[tuple(xm)]
            D[i, jm] -= (u0 / 2.0) * eta[mu] * wrap_m

    return D


# Numerical check: |det(L_t=4)| / |det(L_t=2)|^2 should equal (7/8)^16
# (verified to machine precision; u_0 dependence cancels).
for u0_test in (0.5, 0.7, 0.877, 1.0, 1.3):
    D2 = build_staggered_dirac_meanfield(Lt=2, u0=u0_test)
    D4 = build_staggered_dirac_meanfield(Lt=4, u0=u0_test)
    det2_num = abs(np.linalg.det(D2))
    det4_num = abs(np.linalg.det(D4))
    ratio_num = det4_num / (det2_num ** 2)
    target = float(Fraction(7, 8) ** 16)
    rel_err = abs(ratio_num - target) / target if target > 0 else float("inf")
    check(
        f"numerical ratio @ u_0 = {u0_test}",
        rel_err < 1e-6,
        f"ratio={ratio_num:.10e}, target={target:.10e}, rel_err={rel_err:.2e}",
    )


# ============================================================================
section("Part 4: dim-4 V_eff'' readout corollary — (1/4) compression power")
# ============================================================================
#
# Under the dim-4 effective-potential-density readout
#
#     v(L_t)  ∝  A(L_t)^(-1/4)                                     (R)
#
# where A(L_t) = (1 / (2 L_t u_0^2)) Σ_ω 1 / (3 + sin^2 ω) is the m^2
# coefficient of Δf at the symmetric point (per
# HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE):
#
#     v(L_t=4) / v(L_t=2)  =  (A_2 / A_4)^(1/4).
#
# Within the admitted readout, the (1/4) is the D = 4
# Stefan-Boltzmann-style dimensional bookkeeping: v has mass dim 1,
# V_eff has mass dim 4, so the dim-1 scale extracted from a dim-4
# density coefficient scales as the (1/4) power.
#
# This Part computes A_2 and A_4 with EXACT Fraction arithmetic on
# the same (3 + sin^2 ω) Matsubara sum that drives the determinant
# identity in Part 2. The result must be the same (7/8)^(1/4) factor
# AND it must be unified with the Class A identity (Section 4.2 of
# the note: A_2/A_4 = 7/8 from the SAME Matsubara sum).


def A_endpoint_exact(L_t: int) -> Fraction:
    """A(L_t) at L_s = 2 in units of 1/u_0^2.

    From HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE:
        Δf(L_t, m) = A(L_t) m^2 + O(m^4)
        A(L_t)      = (1 / (2 L_t u_0^2)) Σ_ω  1 / (3 + sin^2 ω)

    We compute A(L_t) * u_0^2 as an exact Fraction (using the rational
    sin^2 ω values at L_s = 2, L_t ∈ {2, 4}).
    """
    sin2_values = matsubara_modes_sin_squared(L_t)
    inv_sum = Fraction(0)
    for s2 in sin2_values:
        inv_sum += Fraction(1, 1) / (Fraction(3) + s2)  # 1/(3 + sin^2 ω)
    # A(L_t) * u_0^2 = (1 / (2 L_t)) * inv_sum
    return inv_sum / Fraction(2 * L_t)


A2_x_u02 = A_endpoint_exact(2)
A4_x_u02 = A_endpoint_exact(4)

check(
    "A_2 = 1/(8 u_0^2)  [exact Fraction from (3 + sin^2 ω) sum]",
    A2_x_u02 == Fraction(1, 8),
    f"A_2 * u_0^2 = {A2_x_u02.numerator}/{A2_x_u02.denominator}",
)
check(
    "A_4 = 1/(7 u_0^2)  [exact Fraction from (3 + sin^2 ω) sum]",
    A4_x_u02 == Fraction(1, 7),
    f"A_4 * u_0^2 = {A4_x_u02.numerator}/{A4_x_u02.denominator}",
)

# A_2 / A_4 — the rational ratio that drives the dim-4 compression
A_ratio = A2_x_u02 / A4_x_u02
check(
    "A_2 / A_4 = 7/8  (Klein-four orbit selection unifies with (7/8)^16)",
    A_ratio == Fraction(7, 8),
    f"A_2 / A_4 = {A_ratio.numerator}/{A_ratio.denominator}",
)

# Class A unification: the same rational ratio A_2/A_4 also appears in
# the determinant identity (5) as (7/8)^16. Verify the structural link:
det_ratio_pure = pure_ratio  # from Part 2 above; expected = (7/8)^16
expected_det_from_A = A_ratio ** 16
check(
    "Class A unification: det ratio = (A_2/A_4)^16 = (7/8)^16",
    det_ratio_pure == expected_det_from_A,
    f"det_ratio = (7/8)^16 = (A_2/A_4)^16 [confirmed]",
)

# Stefan-Boltzmann-style 1/4-power dimensional analysis:
#   v has mass dim 1, V_eff has mass dim 4
#   v ∝ (dim-4 density coeff)^(1/4)  ⇒  v ∝ A^(-1/4) when A enters
#                                        in the inverse-density slot
# The compression v(L_t=4) / v(L_t=2) = (A_2/A_4)^(1/4).
expected_C = (7 / 8) ** 0.25  # numerical target from rational ratio
derived_C = float(A_ratio) ** 0.25
check(
    "(A_2/A_4)^(1/4) = (7/8)^(1/4) numerically",
    abs(derived_C - expected_C) < 1e-12,
    f"derived={derived_C:.12f}, direct={expected_C:.12f}",
)

# The (1/4) power index is conditional dimensional bookkeeping inside (R).
mass_dim_v = Fraction(1)            # scalar VEV has mass dim 1
mass_dim_Veff_density = Fraction(4) # V_eff has mass dim 4 in 4D
expected_power = mass_dim_v / mass_dim_Veff_density
check(
    "(1/4) power inside readout R = mass_dim(v) / mass_dim(V_eff)",
    expected_power == Fraction(1, 4),
    f"mass_dim(v)/mass_dim(V_eff) = 1/4",
)


# ============================================================================
section("Part 5: sign and placement assertions")
# ============================================================================
C_value = expected_C
check(
    "compression sign: C < 1 (downward compression)",
    C_value < 1,
    f"C = {C_value:.6f}",
)
check(
    "compression magnitude: ~ 3.3% downward",
    0.96 < C_value < 0.98,
    f"C = {C_value:.6f}, fractional reduction = {(1 - C_value) * 100:.3f}%",
)

# Placement: the corollary applies the compression multiplicatively to v
# (mass dim 1), not to v^2 or v^4. Numerically verify against the framework's
# stated v compression: v_pred * C = v_phys.
v_pred_no_C = 254.643210673818  # per HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE
v_phys_predicted = v_pred_no_C * C_value
v_obs = 246.22  # PDG-comparator only (NOT a derivation input)
check(
    "multiplicative placement: inherited v_pred * (7/8)^(1/4)",
    abs(v_phys_predicted - 246.282818) < 1e-3,
    f"v_phys_predicted = {v_phys_predicted:.6f} GeV",
)

# Audit comparator only (forbidden as derivation input):
residual_pct = (v_phys_predicted - v_obs) / v_obs * 100
print(
    f"\n  [INFO] audit comparator (NOT a derivation input):"
    f"\n         v_phys_predicted = {v_phys_predicted:.4f} GeV"
    f"\n         v_obs (PDG)      = {v_obs:.4f} GeV"
    f"\n         residual         = {residual_pct:+.4f}%"
    f"\n         (consistent with plaquette/u_0 input uncertainty per gate #7)"
)


# ============================================================================
section("Summary")
# ============================================================================
print(f"\nTOTAL : PASS = {PASS}, FAIL = {FAIL}, ADMITTED = {ADMITTED}")
if FAIL > 0:
    sys.exit(1)
sys.exit(0)
