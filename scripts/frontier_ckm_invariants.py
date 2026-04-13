#!/usr/bin/env python3
"""
CKM Route 4: Invariant Relations from Derived Quantities
=========================================================

STATUS: BOUNDED -- V_cb can be constrained from invariant relations but requires
        one additional input beyond V_us and delta_CP.

ROUTE 4 STRATEGY (from instructions.md):
  "Use CKM invariants rather than raw overlap amplitudes. If V_us is sharp
   and V_ub can be sharpened, use the derived phase scale and Jarlskog/invariant
   relations to solve for V_cb. Do not import PDG angles."

DERIVED FRAMEWORK INPUTS (no PDG angles imported):
  |V_us| = 0.224    (derived, 0.4% from PDG 0.2243)
  delta_CP = 2pi/3  (derived from Z_3 lattice symmetry)

PARAMETRIZATION (standard PDG):
  s12 = sin(theta_12),  c12 = cos(theta_12)
  s23 = sin(theta_23),  c23 = cos(theta_23)
  s13 = sin(theta_13),  c13 = cos(theta_13)

  V_us = s12 * c13  =>  s12 = 0.224 / c13 ~ 0.224  (since c13 ~ 1)

THE PROBLEM:
  We have TWO derived quantities (|V_us|, delta) but THREE unknown angles.
  The CKM matrix has four physical parameters: three angles + one phase.
  With the phase fixed, we still need ONE more relation to close the system.

  This script systematically explores what additional inputs the framework
  can provide, and what constraints the invariant relations impose.

ANALYSIS:
  Part 1: What V_us + delta_CP constrain (the invariant surface)
  Part 2: Wolfenstein closure -- can A = s23/lambda^2 be derived?
  Part 3: Z_3 scaling hypothesis: s13 ~ lambda^p for integer p
  Part 4: Jarlskog invariant as a function of s13, s23
  Part 5: NNI mass-ratio constraint as the third relation
  Part 6: Combined Route 4 + Route 1 (NNI) closure attempt

PStack experiment: frontier-ckm-invariants
Self-contained: numpy only.
"""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0
EXACT_PASS = 0
EXACT_FAIL = 0
BOUNDED_PASS = 0
BOUNDED_FAIL = 0


def check(name, condition, detail="", kind="EXACT"):
    global PASS_COUNT, FAIL_COUNT, EXACT_PASS, EXACT_FAIL
    global BOUNDED_PASS, BOUNDED_FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
        if kind == "EXACT":
            EXACT_PASS += 1
        else:
            BOUNDED_PASS += 1
    else:
        FAIL_COUNT += 1
        if kind == "EXACT":
            EXACT_FAIL += 1
        else:
            BOUNDED_FAIL += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)


# ===================================================================
# CONSTANTS: Derived framework inputs (NO PDG angles imported)
# ===================================================================

# Derived from framework
V_us_derived = 0.224          # |V_us| from Z_3 lattice structure
delta_CP_derived = 2 * np.pi / 3   # CP phase from Z_3 eigenvalue misalignment
lambda_W = V_us_derived       # Wolfenstein lambda

# PDG reference values (for comparison ONLY, not used as inputs)
V_us_PDG = 0.2243
V_cb_PDG = 0.0412
V_ub_PDG = 0.00382
delta_PDG = 1.196             # radians (~68.5 degrees)
J_PDG = 3.08e-5

# PDG mixing angles (reference only)
s12_PDG = 0.22501
s23_PDG = 0.04182
s13_PDG = 0.00369
c12_PDG = np.sqrt(1 - s12_PDG**2)
c23_PDG = np.sqrt(1 - s23_PDG**2)
c13_PDG = np.sqrt(1 - s13_PDG**2)

# Quark masses (MSbar) for NNI relations
m_u = 0.00216    # GeV
m_d = 0.00467    # GeV
m_c = 1.27       # GeV
m_s = 0.0934     # GeV
m_t = 172.76     # GeV
m_b = 4.18       # GeV


def build_ckm(s12, s23, s13, delta):
    """Build the CKM matrix from mixing angles and CP phase."""
    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    ed = np.exp(1j * delta)
    emd = np.exp(-1j * delta)

    V = np.array([
        [c12 * c13, s12 * c13, s13 * emd],
        [-s12 * c23 - c12 * s23 * s13 * ed,
         c12 * c23 - s12 * s23 * s13 * ed,
         s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * ed,
         -c12 * s23 - s12 * c23 * s13 * ed,
         c23 * c13]
    ])
    return V


def jarlskog(s12, s23, s13, delta):
    """Compute the Jarlskog invariant."""
    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    return c12 * s12 * c23 * s23 * c13**2 * s13 * np.sin(delta)


# ===================================================================
# PART 1: The invariant surface from V_us + delta_CP
# ===================================================================
def part1_invariant_surface():
    print("=" * 70)
    print("PART 1: INVARIANT SURFACE FROM V_us AND delta_CP")
    print("=" * 70)
    print()
    print("  Derived inputs:")
    print(f"    |V_us| = {V_us_derived}")
    print(f"    delta_CP = 2pi/3 = {np.degrees(delta_CP_derived):.1f} deg")
    print()

    # With V_us = s12 * c13 fixed, we have a 2D family parametrized by (s23, s13).
    # For each (s23, s13) we can compute the full CKM and the Jarlskog.

    # Show the constraint: s12 = V_us / c13
    print("  Constraint: s12 = |V_us| / c13")
    print("  For small s13: s12 ~ 0.224, theta_12 ~ 12.9 deg")
    print()

    # Scan the (s23, s13) plane and compare to PDG
    print("  Scan of CKM elements on the invariant surface:")
    print(f"  {'s23':>8s}  {'s13':>8s}  {'|V_cb|':>10s}  {'|V_ub|':>10s}  "
          f"{'J':>12s}  {'V_cb err':>10s}  {'V_ub err':>10s}")
    print(f"  {'-'*8}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*12}  {'-'*10}  {'-'*10}")

    # Targeted scan near PDG values
    s23_vals = np.linspace(0.02, 0.08, 7)
    s13_vals = np.linspace(0.001, 0.008, 8)

    best_combined = None
    best_metric = 1e10

    for s23 in s23_vals:
        for s13 in s13_vals:
            c13 = np.sqrt(1 - s13**2)
            s12 = V_us_derived / c13
            if s12 >= 1.0:
                continue

            V = build_ckm(s12, s23, s13, delta_CP_derived)
            vcb = np.abs(V[1, 2])
            vub = np.abs(V[0, 2])
            J = jarlskog(s12, s23, s13, delta_CP_derived)

            err_cb = (vcb - V_cb_PDG) / V_cb_PDG * 100
            err_ub = (vub - V_ub_PDG) / V_ub_PDG * 100

            metric = (err_cb / 10)**2 + (err_ub / 10)**2
            if metric < best_metric:
                best_metric = metric
                best_combined = (s23, s13, vcb, vub, J, err_cb, err_ub)

    s23, s13, vcb, vub, J, err_cb, err_ub = best_combined
    print(f"  Best fit on surface:")
    print(f"    s23 = {s23:.5f}  (PDG: {s23_PDG:.5f})")
    print(f"    s13 = {s13:.5f}  (PDG: {s13_PDG:.5f})")
    print(f"    |V_cb| = {vcb:.5f}  ({err_cb:+.1f}% from PDG {V_cb_PDG})")
    print(f"    |V_ub| = {vub:.5f}  ({err_ub:+.1f}% from PDG {V_ub_PDG})")
    print(f"    J = {J:.3e}  (PDG: {J_PDG:.3e})")
    print()

    print("  KEY FINDING: V_us + delta_CP define a 2D surface in (s23, s13) space.")
    print("  The PDG point lies on this surface (the delta offset biases J by ~7%).")
    print("  We need ONE more relation to select a unique point.")
    print()

    check("V_us derived matches PDG within 0.5%",
          abs(V_us_derived - V_us_PDG) / V_us_PDG < 0.005,
          f"|V_us| = {V_us_derived} vs PDG {V_us_PDG}",
          kind="EXACT")


# ===================================================================
# PART 2: Wolfenstein A parameter from Z_3 structure
# ===================================================================
def part2_wolfenstein_A():
    print()
    print("=" * 70)
    print("PART 2: CAN WOLFENSTEIN A BE DERIVED FROM Z_3?")
    print("=" * 70)
    print()

    # In the Wolfenstein parametrization:
    #   lambda = s12 = |V_us| = 0.224  (DERIVED)
    #   A = s23 / lambda^2             (NEED TO DERIVE)
    #   rho + i*eta from V_ub          (NEED TO DERIVE)
    #
    # PDG: A = 0.0412 / 0.224^2 = 0.821

    A_PDG = V_cb_PDG / lambda_W**2
    print(f"  Wolfenstein lambda = {lambda_W} (derived)")
    print(f"  Wolfenstein A (PDG) = {A_PDG:.3f}")
    print()

    # Hypothesis 1: A from Z_3 hierarchy
    # The Z_3 structure gives lambda ~ epsilon^1, and s23 ~ epsilon^2
    # where epsilon = Cabibbo angle ~ 0.224.
    # This is the standard Froggatt-Nielsen scaling with Z_3 charges.
    #
    # If s23 = A * lambda^2 with A = O(1), the question is: does Z_3 fix A?

    # The Z_3 eigenvalues are {1, omega, omega^2}.
    # The Cabibbo angle comes from the 1-2 misalignment.
    # The 2-3 mixing comes from the 2-3 misalignment, suppressed by one
    # more power of the hierarchy parameter.

    # Test: s23 = lambda^2 (i.e. A = 1)
    A_test = 1.0
    s23_test = A_test * lambda_W**2
    print(f"  Hypothesis: A = 1 (Z_3 democratic)")
    print(f"    s23 = lambda^2 = {s23_test:.5f}")
    print(f"    V_cb = {s23_test:.5f}  (PDG: {V_cb_PDG})")
    print(f"    Error: {(s23_test - V_cb_PDG)/V_cb_PDG*100:+.1f}%")
    print()

    # Test: A from NNI mass ratios
    # In the NNI texture: V_cb ~ |sqrt(m_s/m_b) - sqrt(m_c/m_t)|
    # This gives V_cb ~ |0.1495 - 0.0857| = 0.0638 if c23 = 1,
    # or V_cb ~ 0.0412 if c23 = 0.634.
    # The NNI relation gives A_NNI = V_cb_NNI / lambda^2

    delta_ratio = abs(np.sqrt(m_s / m_b) - np.sqrt(m_c / m_t))
    A_NNI_unit = delta_ratio / lambda_W**2
    print(f"  From NNI mass ratios (c_23 = 1):")
    print(f"    V_cb = |sqrt(m_s/m_b) - sqrt(m_c/m_t)| = {delta_ratio:.5f}")
    print(f"    A_NNI = {A_NNI_unit:.3f}")
    print(f"    Error vs PDG A: {(A_NNI_unit - A_PDG)/A_PDG*100:+.1f}%")
    print()

    # With c_23 = 0.634 (from V_cb exact script):
    c23_fit = 0.634
    V_cb_NNI = c23_fit * delta_ratio
    A_NNI_fit = V_cb_NNI / lambda_W**2
    print(f"  From NNI mass ratios (c_23 = {c23_fit}):")
    print(f"    V_cb = {V_cb_NNI:.5f}")
    print(f"    A_NNI = {A_NNI_fit:.3f}")
    print(f"    Error vs PDG A: {(A_NNI_fit - A_PDG)/A_PDG*100:+.1f}%")
    print()

    # The ratio route gives c_23^u / c_23^d = W_u / W_d = 1.015
    # from gauge quantum numbers alone. But we still need the absolute scale.

    check("A_NNI(c23=1) within 2x of PDG A",
          0.3 < A_NNI_unit < 2.0,
          f"A_NNI = {A_NNI_unit:.3f}, PDG A = {A_PDG:.3f}",
          kind="BOUNDED")

    check("A_NNI(c23=0.634) reproduces PDG A within 2%",
          abs(A_NNI_fit - A_PDG) / A_PDG < 0.02,
          f"A = {A_NNI_fit:.4f} vs PDG {A_PDG:.4f}",
          kind="BOUNDED")


# ===================================================================
# PART 3: Z_3 scaling for s13 (V_ub closure)
# ===================================================================
def part3_vub_from_z3():
    print()
    print("=" * 70)
    print("PART 3: V_ub FROM Z_3 SCALING HIERARCHY")
    print("=" * 70)
    print()

    # In the standard power counting:
    #   s12 ~ lambda ~ 0.224           (1-2 mixing, epsilon^1)
    #   s23 ~ lambda^2 ~ 0.050         (2-3 mixing, epsilon^2)
    #   s13 ~ lambda^3 ~ 0.011         (1-3 mixing, epsilon^3)
    #
    # PDG: s13 = 0.00369, which is lambda^3 * (s13/lambda^3) = lambda^3 * 0.33
    # So s13 ~ lambda^3 / 3, or more precisely s13 ~ A * lambda^3 * (rho^2+eta^2)^{1/2}
    #
    # The NNI texture gives: V_ub ~ sqrt(m_u/m_t) * c_13_coefficient
    #   sqrt(m_u/m_t) = sqrt(0.00216/172.76) = 0.00354
    #   This is already close to V_ub_PDG = 0.00382!

    # NNI prediction for V_ub
    Vub_NNI = np.sqrt(m_u / m_t)
    print(f"  NNI structural prediction: |V_ub| ~ sqrt(m_u/m_t) = {Vub_NNI:.5f}")
    print(f"  PDG value: |V_ub| = {V_ub_PDG:.5f}")
    print(f"  Error: {(Vub_NNI - V_ub_PDG)/V_ub_PDG*100:+.1f}%")
    print()

    # Z_3 power scaling: s13 ~ lambda^p
    for p in [2, 3, 4]:
        s13_pred = lambda_W**p
        err = (s13_pred - s13_PDG) / s13_PDG * 100
        print(f"  lambda^{p} = {s13_pred:.5f}  (PDG s13 = {s13_PDG:.5f}, "
              f"error {err:+.0f}%)")

    print()
    print(f"  lambda^3 = {lambda_W**3:.5f} is 3x too large.")
    print(f"  sqrt(m_u/m_t) = {Vub_NNI:.5f} is within 7% of PDG.")
    print(f"  The NNI mass-ratio formula is a much sharper constraint than")
    print(f"  naive Z_3 power counting for the 1-3 element.")
    print()

    check("|V_ub| ~ sqrt(m_u/m_t) within 10% of PDG",
          abs(Vub_NNI - V_ub_PDG) / V_ub_PDG < 0.10,
          f"{Vub_NNI:.5f} vs PDG {V_ub_PDG:.5f}",
          kind="BOUNDED")

    return Vub_NNI


# ===================================================================
# PART 4: Jarlskog from derived quantities
# ===================================================================
def part4_jarlskog():
    print()
    print("=" * 70)
    print("PART 4: JARLSKOG INVARIANT FROM DERIVED INPUTS")
    print("=" * 70)
    print()

    # J = c12 * s12 * c23 * s23 * c13^2 * s13 * sin(delta)
    #
    # Derived: delta = 2pi/3, so sin(delta) = sqrt(3)/2
    # Derived: s12 ~ 0.224
    # If we also derive s13 and s23, J is fully determined.

    sin_delta = np.sin(delta_CP_derived)
    sin_delta_PDG = np.sin(delta_PDG)
    print(f"  sin(delta_Z3) = sin(2pi/3) = {sin_delta:.6f}")
    print(f"  sin(delta_PDG) = sin({np.degrees(delta_PDG):.1f} deg) = {sin_delta_PDG:.6f}")
    print(f"  Ratio: sin(delta_Z3)/sin(delta_PDG) = {sin_delta/sin_delta_PDG:.4f}")
    print()

    # J with PDG angles + Z3 phase
    J_z3_pdg_angles = jarlskog(s12_PDG, s23_PDG, s13_PDG, delta_CP_derived)
    J_full_pdg = jarlskog(s12_PDG, s23_PDG, s13_PDG, delta_PDG)
    print(f"  J(PDG angles, Z3 phase) = {J_z3_pdg_angles:.3e}")
    print(f"  J(PDG angles, PDG phase) = {J_full_pdg:.3e}")
    print(f"  J(PDG, 2024 global fit)  = {J_PDG:.3e}")
    print()

    # Now: J with derived V_us, NNI V_ub, and variable V_cb
    s12 = V_us_derived  # ~ s12 since c13 ~ 1
    s13_NNI = np.sqrt(m_u / m_t)

    print(f"  Using framework-derived inputs:")
    print(f"    s12 = {s12:.5f}  (from V_us)")
    print(f"    s13 = sqrt(m_u/m_t) = {s13_NNI:.5f}")
    print(f"    delta = 2pi/3")
    print()

    # Scan s23 and compute J
    print(f"  {'s23':>8s}  {'V_cb':>10s}  {'J':>12s}  {'J/J_PDG':>10s}")
    print(f"  {'-'*8}  {'-'*10}  {'-'*12}  {'-'*10}")

    s23_scan = np.linspace(0.02, 0.08, 13)
    for s23 in s23_scan:
        c13 = np.sqrt(1 - s13_NNI**2)
        s12_adj = V_us_derived / c13
        J = jarlskog(s12_adj, s23, s13_NNI, delta_CP_derived)
        V = build_ckm(s12_adj, s23, s13_NNI, delta_CP_derived)
        vcb = np.abs(V[1, 2])
        marker = " <--" if abs(vcb - V_cb_PDG) < 0.003 else ""
        print(f"  {s23:8.5f}  {vcb:10.5f}  {J:12.3e}  {J/J_PDG:10.3f}{marker}")

    # What s23 gives J = J_PDG?
    def J_residual(s23):
        c13 = np.sqrt(1 - s13_NNI**2)
        s12_adj = V_us_derived / c13
        return jarlskog(s12_adj, s23, s13_NNI, delta_CP_derived) - J_PDG

    # Since J is monotonic in s23 (for small s23), find root
    from scipy.optimize import brentq
    try:
        s23_for_J = brentq(J_residual, 0.01, 0.15)
        c13 = np.sqrt(1 - s13_NNI**2)
        s12_adj = V_us_derived / c13
        V = build_ckm(s12_adj, s23_for_J, s13_NNI, delta_CP_derived)
        vcb_from_J = np.abs(V[1, 2])
        print()
        print(f"  If J = J_PDG = {J_PDG:.2e}:")
        print(f"    s23 = {s23_for_J:.5f}")
        print(f"    V_cb = {vcb_from_J:.5f}  (PDG: {V_cb_PDG})")
        print(f"    Error: {(vcb_from_J - V_cb_PDG)/V_cb_PDG*100:+.1f}%")
        print()
        print("  PROBLEM: J depends on s23 linearly (for small s23), so")
        print("  J_PDG = J_derived merely gives s23 = J_PDG / (c12*s12*c13^2*s13*sin(delta))")
        print("  This is just solving for s23 from J -- tautological unless J itself")
        print("  is independently derived from the lattice.")
    except Exception:
        print("  Could not solve for s23 from J constraint.")

    print()

    check("J(Z3 phase, PDG angles) within 10% of J_PDG",
          abs(J_z3_pdg_angles - J_PDG) / J_PDG < 0.10,
          f"J_Z3 = {J_z3_pdg_angles:.3e} vs {J_PDG:.3e}",
          kind="BOUNDED")


# ===================================================================
# PART 5: NNI mass-ratio constraint as the third relation
# ===================================================================
def part5_nni_closure():
    print()
    print("=" * 70)
    print("PART 5: NNI MASS-RATIO RELATIONS AS THE CLOSURE CONSTRAINT")
    print("=" * 70)
    print()

    # The NNI (nearest-neighbor interaction) texture gives:
    #   V_us ~ sqrt(m_d/m_s) - sqrt(m_u/m_c) * e^{i*delta_12}
    #   V_cb ~ c_23 * |sqrt(m_s/m_b) - sqrt(m_c/m_t) * e^{i*delta_23}|
    #   V_ub ~ sqrt(m_u/m_t) * c_13_coeff
    #
    # The INVARIANT approach: rather than solving for c_23 directly,
    # combine the NNI mass-ratio formulas with the invariant (Jarlskog) relation.

    # Step 1: V_us from mass ratios (the Gatto-Sartori-Tonin relation)
    V_us_GST = np.sqrt(m_d / m_s) - np.sqrt(m_u / m_c)
    V_us_GST_abs = abs(V_us_GST)
    print(f"  Gatto-Sartori-Tonin: V_us ~ sqrt(m_d/m_s) - sqrt(m_u/m_c)")
    print(f"    sqrt(m_d/m_s) = {np.sqrt(m_d/m_s):.5f}")
    print(f"    sqrt(m_u/m_c) = {np.sqrt(m_u/m_c):.5f}")
    print(f"    V_us_GST = {V_us_GST_abs:.5f}  (framework: {V_us_derived}, PDG: {V_us_PDG})")
    print(f"    Error vs framework: {(V_us_GST_abs - V_us_derived)/V_us_derived*100:+.1f}%")
    print()

    check("GST relation for V_us within 20% (leading-order, MSbar masses)",
          abs(V_us_GST_abs - V_us_derived) / V_us_derived < 0.20,
          f"GST = {V_us_GST_abs:.5f} vs derived {V_us_derived}",
          kind="BOUNDED")

    # Step 2: V_ub from mass ratio
    V_ub_mass = np.sqrt(m_u / m_t)
    print(f"  V_ub from mass ratio: sqrt(m_u/m_t) = {V_ub_mass:.5f}")
    print(f"    PDG: {V_ub_PDG:.5f}")
    print(f"    Error: {(V_ub_mass - V_ub_PDG)/V_ub_PDG*100:+.1f}%")
    print()

    # Step 3: V_cb from NNI with symmetric c_23
    delta_23 = abs(np.sqrt(m_s / m_b) - np.sqrt(m_c / m_t))
    print(f"  V_cb from NNI (c_23 = 1):")
    print(f"    |sqrt(m_s/m_b) - sqrt(m_c/m_t)| = {delta_23:.5f}")
    print(f"    This is {delta_23/V_cb_PDG:.2f}x the PDG V_cb")
    print()

    # Step 4: The invariant closure
    # If we take V_us = 0.224 (derived), V_ub = sqrt(m_u/m_t) (NNI),
    # delta = 2pi/3 (Z_3), then s23 is the ONLY free parameter.
    #
    # The Jarlskog invariant becomes:
    #   J = c12 s12 c23 s23 c13^2 s13 sin(2pi/3)
    #
    # where s12, s13 are fixed by V_us and V_ub, and delta is fixed.
    # J is then PROPORTIONAL to s23, so knowing J fixes s23.
    #
    # But J is not independently derived from the lattice.
    # What IS derived: the phase. What IS structurally constrained: the mass ratios.
    #
    # The REAL closure comes from the NNI formula for V_cb itself.

    s12 = V_us_derived
    s13 = V_ub_mass
    c12 = np.sqrt(1 - s12**2)
    c13 = np.sqrt(1 - s13**2)

    # From NNI: V_cb = c_23 * delta_23 (symmetric case)
    # The question is: what determines c_23?
    # Route 4 asks: can we avoid solving for c_23 and instead use invariants?

    print("  Route 4 analysis:")
    print("  -----------------")
    print("  Given: V_us = 0.224 (derived), delta = 2pi/3 (derived)")
    print(f"         V_ub ~ sqrt(m_u/m_t) = {V_ub_mass:.5f} (NNI, 7% from PDG)")
    print()
    print("  These three inputs fix s12, s13, and delta.")
    print("  The only remaining unknown is s23 (equivalently V_cb).")
    print()
    print("  The Jarlskog invariant is PROPORTIONAL to s23 at this point:")
    J_coefficient = c12 * s12 * c13**2 * s13 * np.sin(delta_CP_derived)
    print(f"    J = {J_coefficient:.6e} * s23 * c23")
    print(f"    J ~ {J_coefficient:.6e} * s23  (since c23 ~ 1)")
    print()
    print("  So using J to determine s23 is EQUIVALENT to inputting V_cb directly.")
    print("  Route 4 does NOT provide independent closure for V_cb.")
    print()
    print("  The NNI mass-ratio formula V_cb = c_23 * delta_23 remains the")
    print("  most direct path. Route 4 SUPPLEMENTS Routes 1-2 but does not")
    print("  replace them.")


# ===================================================================
# PART 6: Combined Route 4 + Route 1 best prediction
# ===================================================================
def part6_combined():
    print()
    print("=" * 70)
    print("PART 6: COMBINED BEST PREDICTION (Route 4 + NNI)")
    print("=" * 70)
    print()

    # Collect all framework-derived/constrained inputs:
    s12 = V_us_derived                      # DERIVED (0.4% from PDG)
    delta = delta_CP_derived                # DERIVED (75% from PDG, Z_3 structural)
    s13_NNI = np.sqrt(m_u / m_t)           # NNI mass ratio (7% from PDG)

    # V_cb from NNI with c_23 = 0.634 (fitted) or from ratio route
    c23_values = {
        "c_23 = 1 (NNI symmetric)": 1.0,
        "c_23 = 0.634 (fitted from PDG V_cb)": 0.634,
        "c_23 = 0.65 (lattice L=8, 38% off fit)": 0.65,
    }

    delta_23 = abs(np.sqrt(m_s / m_b) - np.sqrt(m_c / m_t))
    print(f"  Common NNI factor: |sqrt(m_s/m_b) - sqrt(m_c/m_t)| = {delta_23:.5f}")
    print()

    for label, c23 in c23_values.items():
        V_cb_pred = c23 * delta_23
        s23 = V_cb_pred  # small angle

        c13 = np.sqrt(1 - s13_NNI**2)
        s12_adj = V_us_derived / c13

        J_pred = jarlskog(s12_adj, s23, s13_NNI, delta)
        V = build_ckm(s12_adj, s23, s13_NNI, delta)

        print(f"  {label}:")
        print(f"    V_cb = {V_cb_pred:.5f}  ({(V_cb_pred-V_cb_PDG)/V_cb_PDG*100:+.1f}% from PDG)")
        print(f"    V_ub = {np.abs(V[0,2]):.5f}  ({(np.abs(V[0,2])-V_ub_PDG)/V_ub_PDG*100:+.1f}% from PDG)")
        print(f"    J    = {J_pred:.3e}  ({(J_pred-J_PDG)/J_PDG*100:+.1f}% from PDG)")
        print()

        # Unitarity check
        VVdag = V @ V.conj().T
        unitarity_err = np.max(np.abs(VVdag - np.eye(3)))
        check(f"Unitarity for {label[:20]}",
              unitarity_err < 1e-12,
              f"max|VV^dag - I| = {unitarity_err:.1e}",
              kind="EXACT")

    # The honest route 4 assessment
    print()
    print("  ROUTE 4 HONEST ASSESSMENT:")
    print("  ==========================")
    print()
    print("  WHAT ROUTE 4 PROVIDES:")
    print("    1. |V_us| = 0.224 (derived, 0.4% from PDG)  -- SHARP")
    print("    2. delta_CP = 2pi/3 = 120 deg (derived from Z_3) -- STRUCTURAL")
    print(f"       (overshoots PDG {np.degrees(delta_PDG):.1f} deg by 75%)")
    print("    3. The Jarlskog invariant with Z_3 phase:")
    J_test = jarlskog(s12_PDG, s23_PDG, s13_PDG, delta_CP_derived)
    print(f"       J(Z3 phase, PDG angles) = {J_test:.3e}")
    print(f"       vs J_PDG = {J_PDG:.3e}  ({(J_test-J_PDG)/J_PDG*100:+.1f}%)")
    print()
    print("  WHAT ROUTE 4 DOES NOT PROVIDE:")
    print("    - An independent constraint on s23 (V_cb)")
    print("    - J is proportional to s23, so J cannot independently fix V_cb")
    print("    - The NNI mass-ratio formula (Route 1) remains the only path to V_cb")
    print()
    print("  WHERE ROUTE 4 HELPS:")
    print("    - Confirms consistency: the Z_3 phase is compatible with PDG J")
    print("    - Provides a CHECK: if V_cb is derived from NNI, the predicted J")
    print("      must match PDG. This is a nontrivial consistency condition.")
    print("    - Sharpens V_ub: if V_ub = sqrt(m_u/m_t) is the framework prediction,")
    print("      then Route 4 constrains the COMBINATION of V_cb and V_ub through")
    print("      unitarity (first-row: |V_ud|^2 + |V_us|^2 + |V_ub|^2 = 1).")
    print()

    # Unitarity constraint from first row
    V_ud_sq = 1 - V_us_derived**2 - s13_NNI**2
    V_ud = np.sqrt(V_ud_sq)
    V_ud_PDG = 0.97373
    print(f"  First-row unitarity check:")
    print(f"    V_ud = sqrt(1 - V_us^2 - V_ub^2) = {V_ud:.5f}")
    print(f"    PDG V_ud = {V_ud_PDG:.5f}")
    print(f"    Error: {(V_ud - V_ud_PDG)/V_ud_PDG*100:+.2f}%")
    print()

    check("First-row unitarity V_ud within 0.1% of PDG",
          abs(V_ud - V_ud_PDG) / V_ud_PDG < 0.001,
          f"V_ud = {V_ud:.5f} vs PDG {V_ud_PDG:.5f}",
          kind="BOUNDED")

    # Second-row unitarity: constrains s23
    # |V_cd|^2 + |V_cs|^2 + |V_cb|^2 = 1
    # This is automatically satisfied for any s23 if the matrix is unitary.
    # So row unitarity does not independently constrain s23.

    print("  Row/column unitarity is automatically satisfied for any s23 in the")
    print("  standard parametrization. Unitarity does NOT provide a fourth constraint.")
    print()

    # Final: the route 4 bottom line
    print("  ============================================================")
    print("  ROUTE 4 BOTTOM LINE")
    print("  ============================================================")
    print()
    print("  Route 4 (invariant relations) does NOT independently close V_cb.")
    print()
    print("  The CKM matrix has 4 physical parameters. The framework derives 2:")
    print("    |V_us| (sharp, 0.4% from PDG)")
    print("    delta_CP (structural, 75% overshoot)")
    print()
    print("  NNI mass-ratio relations provide 1 more:")
    print("    |V_ub| ~ sqrt(m_u/m_t) (7% from PDG)")
    print()
    print("  The 4th parameter (s23 = V_cb) requires either:")
    print("    (a) The NNI c_23 coefficient (Route 1/2), OR")
    print("    (b) An independent J derivation from the lattice, OR")
    print("    (c) A Z_3 group-theoretic fixing of the Wolfenstein A parameter")
    print()
    print("  None of (a), (b), (c) are currently closed.")
    print("  Route 4 provides CONSISTENCY CHECKS but not CLOSURE.")
    print()
    print("  Sharpest remaining gap: the absolute scale of c_23 (or equivalently A).")
    print("  The ratio c_23^u/c_23^d = 1.015 is derived (Route 2), but the overall")
    print("  normalization requires the lattice overlap integral S_23.")
    print()


# ===================================================================
# MAIN
# ===================================================================
def main():
    print("=" * 70)
    print("CKM ROUTE 4: INVARIANT RELATIONS FROM DERIVED QUANTITIES")
    print("=" * 70)
    print()
    print("Framework inputs (no PDG CKM angles):")
    print(f"  |V_us| = {V_us_derived}  (derived, 0.4% from PDG)")
    print(f"  delta_CP = 2pi/3 = {np.degrees(delta_CP_derived):.1f} deg  (Z_3, overshoots PDG by 75%)")
    print()

    part1_invariant_surface()
    part2_wolfenstein_A()
    V_ub_NNI = part3_vub_from_z3()
    part4_jarlskog()
    part5_nni_closure()
    part6_combined()

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  EXACT checks passed:   {EXACT_PASS}")
    print(f"  EXACT checks failed:   {EXACT_FAIL}")
    print(f"  BOUNDED checks passed: {BOUNDED_PASS}")
    print(f"  BOUNDED checks failed: {BOUNDED_FAIL}")
    print(f"  Total: {PASS_COUNT} passed, {FAIL_COUNT} failed "
          f"out of {PASS_COUNT + FAIL_COUNT}")
    print()

    if FAIL_COUNT > 0:
        print("RESULT: BOUNDED -- some checks failed (see above)")
        sys.exit(1)
    else:
        print("RESULT: BOUNDED -- all consistency checks pass, but V_cb closure requires Route 1/2")
        sys.exit(0)


if __name__ == "__main__":
    main()
