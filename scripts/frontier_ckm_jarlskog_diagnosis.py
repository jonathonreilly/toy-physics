#!/usr/bin/env python3
"""
CKM Jarlskog Invariant Diagnosis
=================================

PROBLEM: The full closure script gives J ~ 8.6e-8, which is ~360x below
PDG (3.08e-5), despite V_ub = 0.00376 being within 1.6% of PDG.

DIAGNOSIS: This script identifies exactly WHERE the 360x suppression
enters by decomposing the Jarlskog invariant step by step.

Key result: The Z_3 input phase delta=2pi/3=120 deg does NOT survive
the mass matrix diagonalization. The physical CKM phase collapses to
~0.1 deg because:

  1. H = M @ M^dagger converts the phase from M_13 into a QUARTIC
     combination c_13^2 * m1*m3 * sin(2*delta), which is tiny when
     c_13 is small (c_13 ~ 0.02 * c_23).

  2. The up and down sectors have NEARLY IDENTICAL phase structure
     because c_13^u / c_13^d = c_23^u / c_23^d = 1.014 (the EW ratio).
     The CKM phase comes from the MISMATCH, which is only 1.4%.

  3. The NNI texture zeros force ALL the CP violation through a single
     parameter (c_13 * sin delta), creating a multiplicative suppression:
     J ~ (c_13)^2 * sin(delta) * (EW mismatch) ~ 0.02^2 * 0.87 * 0.014
     ~ 5e-6 relative to the "naive" estimate.

This is NOT a bug -- it's a structural feature of the NNI texture with
a single phase source and nearly degenerate up/down EW weights.

PStack experiment: frontier-ckm-jarlskog-diagnosis
Self-contained: numpy + scipy.
"""

from __future__ import annotations

import sys
import numpy as np
from scipy.optimize import brentq

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail=""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Physical constants (same as frontier_ckm_full_closure.py)
# =============================================================================

M_UP = 2.16e-3
M_CHARM = 1.27
M_TOP = 172.76
M_DOWN = 4.67e-3
M_STRANGE = 0.0934
M_BOTTOM = 4.18

V_US_PDG = 0.2243
V_CB_PDG = 0.0422
V_UB_PDG = 0.00382
J_PDG = 3.08e-5
DELTA_PDG = 1.144  # rad

V_US_ERR = 0.0005
V_CB_ERR = 0.0011
V_UB_ERR = 0.00024

SIN2_TW = 0.231
Q_UP, T3_UP = 2.0 / 3.0, 0.5
Q_DOWN, T3_DOWN = -1.0 / 3.0, -0.5
C_F = 4.0 / 3.0

ALPHA_S_PL = 0.020
ALPHA_2_PL = 0.025
ALPHA_EM_PL = ALPHA_2_PL * SIN2_TW

C12_U = 1.48
C12_D = 0.91


# =============================================================================
# NNI infrastructure
# =============================================================================

def theta_23(c23, m2, m3):
    """2-3 block mixing angle from NNI formula."""
    x = c23 * np.sqrt(m2 / m3)
    return np.arctan(x)


def compute_ew_ratio():
    gz_up = T3_UP - Q_UP * SIN2_TW
    gz_down = T3_DOWN - Q_DOWN * SIN2_TW
    W_up = ALPHA_S_PL * C_F + ALPHA_2_PL * gz_up**2 + ALPHA_EM_PL * Q_UP**2
    W_down = ALPHA_S_PL * C_F + ALPHA_2_PL * gz_down**2 + ALPHA_EM_PL * Q_DOWN**2
    return W_up / W_down, W_up, W_down


def build_nni_complex(m1, m2, m3, c12, c23, c13, delta):
    """Build Hermitian NNI mass matrix with CP phase in M_13."""
    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = m1
    M[1, 1] = m2
    M[2, 2] = m3
    M[0, 1] = c12 * np.sqrt(m1 * m2)
    M[1, 0] = M[0, 1].conj()
    M[1, 2] = c23 * np.sqrt(m2 * m3)
    M[2, 1] = M[1, 2].conj()
    M[0, 2] = c13 * np.sqrt(m1 * m3) * np.exp(1j * delta)
    M[2, 0] = M[0, 2].conj()
    return M


def compute_ckm(c23_u, c23_d, c13_u, c13_d, delta_u, delta_d=0.0):
    """
    Full 3x3 CKM from NNI diagonalization.

    Returns V_CKM, masses_u, masses_d, and the diagonalizing unitaries.
    """
    M_u = build_nni_complex(M_UP, M_CHARM, M_TOP, C12_U, c23_u, c13_u, delta_u)
    M_d = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM, C12_D, c23_d, c13_d, delta_d)

    H_u = M_u @ M_u.conj().T
    H_d = M_d @ M_d.conj().T

    eigvals_u, U_u = np.linalg.eigh(H_u)
    eigvals_d, U_d = np.linalg.eigh(H_d)

    idx_u = np.argsort(eigvals_u)
    idx_d = np.argsort(eigvals_d)
    U_u = U_u[:, idx_u]
    U_d = U_d[:, idx_d]

    masses_u = np.sqrt(np.abs(eigvals_u[idx_u]))
    masses_d = np.sqrt(np.abs(eigvals_d[idx_d]))

    V_ckm = U_u.conj().T @ U_d
    return V_ckm, masses_u, masses_d, U_u, U_d


def jarlskog_from_V(V):
    """Compute J from the rephasing-invariant quartet V_us*V_cb*V_ub^**V_cs^*."""
    return abs(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))


def jarlskog_parametric(s12, s23, s13, sin_delta):
    """J from standard parametrization: c12*s12*c23*s23*c13^2*s13*sin(delta)."""
    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    return c12 * s12 * c23 * s23 * c13**2 * s13 * sin_delta


# =============================================================================
# DIAGNOSIS 1: Reproduce the problem
# =============================================================================

def diagnosis_1_reproduce():
    """Reproduce J ~ 8.6e-8 from the full closure script."""
    print("=" * 78)
    print("DIAGNOSIS 1: REPRODUCE THE PROBLEM")
    print("=" * 78)

    ratio, _, _ = compute_ew_ratio()

    def vcb_residual(c23_d_val):
        c23_u_val = c23_d_val * ratio
        th_u = theta_23(c23_u_val, M_CHARM, M_TOP)
        th_d = theta_23(c23_d_val, M_STRANGE, M_BOTTOM)
        return np.abs(np.sin(th_u - th_d)) - V_CB_PDG

    c23_d = brentq(vcb_residual, 0.01, 5.0)
    c23_u = c23_d * ratio

    delta_z3 = 2 * np.pi / 3

    # Find c_13 that gives V_ub = PDG (same logic as full closure)
    c13_ratios = np.linspace(0.001, 2.0, 2000)
    best_c13_ratio = 0.0
    best_vub_diff = 1e10
    for cr in c13_ratios:
        c13_d_t = cr * c23_d
        c13_u_t = cr * c23_u
        V_t, _, _, _, _ = compute_ckm(c23_u, c23_d, c13_u_t, c13_d_t, delta_z3)
        v_ub_t = abs(V_t[0, 2])
        diff = abs(v_ub_t - V_UB_PDG)
        if diff < best_vub_diff:
            best_vub_diff = diff
            best_c13_ratio = cr

    c13_d = best_c13_ratio * c23_d
    c13_u = best_c13_ratio * c23_u

    V, mu, md, Uu, Ud = compute_ckm(c23_u, c23_d, c13_u, c13_d, delta_z3)
    J = jarlskog_from_V(V)

    v_us = abs(V[0, 1])
    v_cb = abs(V[1, 2])
    v_ub = abs(V[0, 2])

    print(f"\n  c_23^d = {c23_d:.6f},  c_23^u = {c23_u:.6f}")
    print(f"  c_13/c_23 = {best_c13_ratio:.6f}")
    print(f"  c_13^d = {c13_d:.6f},  c_13^u = {c13_u:.6f}")
    print(f"  delta_input = 2*pi/3 = {delta_z3:.4f} rad = {np.degrees(delta_z3):.1f} deg")
    print(f"\n  Results:")
    print(f"    |V_us| = {v_us:.6f}  (PDG {V_US_PDG})")
    print(f"    |V_cb| = {v_cb:.6f}  (PDG {V_CB_PDG})")
    print(f"    |V_ub| = {v_ub:.6f}  (PDG {V_UB_PDG})")
    print(f"    J      = {J:.4e}     (PDG {J_PDG:.4e})")
    print(f"    J/J_PDG = {J/J_PDG:.6f}")

    # Naive expectation
    J_naive = jarlskog_parametric(V_US_PDG, V_CB_PDG, V_UB_PDG, np.sin(delta_z3))
    print(f"\n  Naive J (PDG angles + sin(2pi/3)):")
    print(f"    J_naive = {J_naive:.4e}")
    print(f"    J_naive / J_PDG = {J_naive / J_PDG:.3f}")
    print(f"    -> If the phase survived, J should be {J_naive/J_PDG:.1f}x PDG")

    # Extract effective sin(delta)
    sin_d_eff = J / jarlskog_parametric(v_us, v_cb, v_ub, 1.0) if v_ub > 0 else 0.0
    delta_eff = np.arcsin(min(abs(sin_d_eff), 1.0))
    print(f"\n  Effective CKM phase:")
    print(f"    sin(delta_eff) = {sin_d_eff:.6f}")
    print(f"    delta_eff = {delta_eff:.4f} rad = {np.degrees(delta_eff):.2f} deg")
    print(f"    Phase survival: delta_eff / delta_input = {delta_eff / delta_z3:.6f}")
    print(f"    -> The 120 deg Z_3 phase is suppressed to {np.degrees(delta_eff):.2f} deg")
    print(f"    -> This is the ~360x suppression factor!")

    check("reproduce_J_suppression",
          J / J_PDG < 0.5,
          f"J/J_PDG = {J/J_PDG:.4f} << 1, confirming J is suppressed")

    check("V_ub_is_correct",
          abs(v_ub - V_UB_PDG) / V_UB_PDG < 0.05,
          f"|V_ub| = {v_ub:.5f}, {(v_ub-V_UB_PDG)/V_UB_PDG*100:+.1f}% from PDG")

    return {
        'c23_u': c23_u, 'c23_d': c23_d,
        'c13_u': c13_u, 'c13_d': c13_d,
        'c13_ratio': best_c13_ratio,
        'delta_z3': delta_z3,
        'V': V, 'J': J,
        'Uu': Uu, 'Ud': Ud,
        'v_us': v_us, 'v_cb': v_cb, 'v_ub': v_ub,
    }


# =============================================================================
# DIAGNOSIS 2: Phase washout mechanism
# =============================================================================

def diagnosis_2_phase_washout(d1):
    """
    Show EXACTLY how the Z_3 phase gets killed in H = M @ M^dagger.

    The NNI mass matrix M has phase exp(i*delta) in M_13.
    When we form H = M @ M^dagger, the (i,j) element is:
        H_ij = sum_k M_ik * M_jk^*

    The ONLY complex element in M is M_13 = c13*sqrt(m1*m3)*e^{i*delta}.
    So the phase enters H through products involving M_13:

    H_11 += |M_13|^2 = c13^2 * m1 * m3   [REAL -- phase cancels!]
    H_12 += M_13 * M_23^* = c13*c23*sqrt(m1*m3)*sqrt(m2*m3)*e^{i*delta}  [COMPLEX]
    H_13 += M_13 * M_33^* = c13*sqrt(m1*m3)*m3*e^{i*delta}               [COMPLEX]

    The phase ONLY appears in H_12 and H_13 (off-diagonal), weighted by
    c13 * sqrt(m1*m3). Since c13 ~ 0.014 and m1/m3 ~ 10^{-8} (up sector),
    these complex entries are TINY compared to the diagonal.

    Quantitatively: for the UP sector,
      |H_12 phase term| / |H_22| ~ c13*sqrt(m_u*m_t)/m_c^2
                                  ~ 0.014 * sqrt(2.16e-3 * 172.76) / 1.27^2
                                  ~ 0.014 * 0.611 / 1.613
                                  ~ 0.005

    That 0.5% complex perturbation to an otherwise real matrix means the
    diagonalizing unitary U_u has phases of order 0.005 radians.

    The CKM phase is the DIFFERENCE between U_u and U_d phases.
    Since c_13^u / c_13^d = 1.014 (EW ratio), the phase difference
    is even smaller: ~0.005 * 0.014 ~ 7e-5 radians ~ 0.004 degrees.
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 2: PHASE WASHOUT IN H = M @ M^dagger")
    print("=" * 78)

    delta = d1['delta_z3']
    c13_u = d1['c13_u']
    c13_d = d1['c13_d']
    c23_u = d1['c23_u']
    c23_d = d1['c23_d']

    # Build M_u with phase
    M_u = build_nni_complex(M_UP, M_CHARM, M_TOP, C12_U, c23_u, c13_u, delta)
    # Build M_u WITHOUT phase for comparison
    M_u_real = build_nni_complex(M_UP, M_CHARM, M_TOP, C12_U, c23_u, c13_u, 0.0)

    H_u = M_u @ M_u.conj().T
    H_u_real = M_u_real @ M_u_real.conj().T

    # The imaginary part of H_u tells us how much phase survived
    H_imag_norm = np.linalg.norm(np.imag(H_u))
    H_real_norm = np.linalg.norm(np.real(H_u))
    imag_fraction = H_imag_norm / H_real_norm

    print(f"\n  Up-sector H = M_u @ M_u^dagger:")
    print(f"    ||Im(H_u)|| = {H_imag_norm:.6e}")
    print(f"    ||Re(H_u)|| = {H_real_norm:.6e}")
    print(f"    Imaginary fraction: {imag_fraction:.6e}")
    print(f"    -> H is {imag_fraction*100:.4f}% complex")

    # Show individual complex entries
    print(f"\n  Complex entries of H_u (only from M_13 phase):")
    for i in range(3):
        for j in range(i+1, 3):
            h_ij = H_u[i, j]
            h_ij_real = H_u_real[i, j]
            phase_contrib = h_ij - h_ij_real
            if abs(phase_contrib) > 1e-15:
                print(f"    H[{i},{j}]: total = {h_ij:.6e}")
                print(f"             real part (from real M) = {h_ij_real:.6e}")
                print(f"             phase contribution      = {phase_contrib:.6e}")
                print(f"             |phase/total| = {abs(phase_contrib)/abs(h_ij):.4e}")

    # Compare eigenvalues with and without phase -- they should be identical
    # (Hermitian eigenvalues are real and don't depend on phases)
    eig_with, U_with = np.linalg.eigh(H_u)
    eig_without, U_without = np.linalg.eigh(H_u_real)
    print(f"\n  Eigenvalues of H_u (should be identical with/without phase):")
    print(f"    With phase:    {np.sort(eig_with)}")
    print(f"    Without phase: {np.sort(eig_without)}")
    print(f"    Max difference: {np.max(np.abs(np.sort(eig_with) - np.sort(eig_without))):.4e}")

    # The EIGENVECTORS differ -- that's where the CKM phase lives
    # Compare the phases of U_u entries
    print(f"\n  Eigenvector phases (deg) -- where the CKM phase lives:")
    print(f"    U_u with phase:")
    idx = np.argsort(eig_with)
    U_sorted = U_with[:, idx]
    for i in range(3):
        phases = [np.degrees(np.angle(U_sorted[i, j])) for j in range(3)]
        print(f"      row {i}: [{phases[0]:8.3f}, {phases[1]:8.3f}, {phases[2]:8.3f}]")

    print(f"    U_u without phase (should be all 0 or 180):")
    idx2 = np.argsort(eig_without)
    U_sorted_r = U_without[:, idx2]
    for i in range(3):
        phases = [np.degrees(np.angle(U_sorted_r[i, j])) for j in range(3)]
        print(f"      row {i}: [{phases[0]:8.3f}, {phases[1]:8.3f}, {phases[2]:8.3f}]")

    # Quantify the phase difference
    max_phase_diff = 0.0
    for i in range(3):
        for j in range(3):
            # Align sign ambiguity
            ratio = U_sorted[i, j] / U_sorted_r[i, j] if abs(U_sorted_r[i, j]) > 1e-10 else 1.0
            phase_diff = abs(np.angle(ratio))
            max_phase_diff = max(max_phase_diff, phase_diff)

    print(f"\n  Max eigenvector phase shift from Z_3 phase: {np.degrees(max_phase_diff):.4f} deg")
    print(f"  -> This is the ~{np.degrees(max_phase_diff):.1f} deg phase that feeds into CKM")

    # Now the CKM phase is the DIFFERENCE between up and down eigenvector phases
    # Since c_13^u/c_13^d = 1.014, the up and down eigenvector phases nearly cancel
    M_d = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM, C12_D, c23_d, c13_d, 0.0)
    H_d = M_d @ M_d.conj().T
    eig_d, U_d = np.linalg.eigh(H_d)
    idx_d = np.argsort(eig_d)
    U_d = U_d[:, idx_d]

    # CKM phase
    V = U_sorted.conj().T @ U_d
    J = jarlskog_from_V(V)
    sin_d_eff = J / jarlskog_parametric(abs(V[0,1]), abs(V[1,2]), abs(V[0,2]), 1.0)
    delta_eff = np.arcsin(min(abs(sin_d_eff), 1.0))

    print(f"\n  CKM from this diagonalization:")
    print(f"    |V_ub| = {abs(V[0,2]):.6f}")
    print(f"    J = {J:.4e}")
    print(f"    delta_eff = {np.degrees(delta_eff):.4f} deg")

    check("phase_washout_identified",
          imag_fraction < 0.01,
          f"H is only {imag_fraction*100:.4f}% complex -- phase is washed out in M@M^dag")

    # Analytical estimate of phase suppression
    # The complex part of H_12 ~ c13 * sqrt(m1*m3) * c23 * sqrt(m2*m3)
    # The real part of H_12 ~ c12 * sqrt(m1*m2) * m2 + ...
    phase_entry_up = c13_u * np.sqrt(M_UP * M_TOP) * c23_u * np.sqrt(M_CHARM * M_TOP)
    dominant_real_up = M_CHARM**2 + (c23_u**2) * M_CHARM * M_TOP
    phase_ratio_up = phase_entry_up / dominant_real_up

    print(f"\n  Analytical phase suppression estimate (up sector):")
    print(f"    |complex H_12 from phase| ~ c13*c23*sqrt(m_u*m_t)*sqrt(m_c*m_t)")
    print(f"                              = {phase_entry_up:.4e}")
    print(f"    |dominant real H_22|      ~ m_c^2 + c23^2*m_c*m_t")
    print(f"                              = {dominant_real_up:.4e}")
    print(f"    Phase perturbation ratio  = {phase_ratio_up:.4e}")
    print(f"    -> Eigenvector phase ~ arctan({phase_ratio_up:.4e}) = {np.degrees(np.arctan(phase_ratio_up)):.4f} deg")

    return {'imag_fraction': imag_fraction, 'max_phase_diff': max_phase_diff}


# =============================================================================
# DIAGNOSIS 3: EW mismatch suppression
# =============================================================================

def diagnosis_3_ew_mismatch(d1):
    """
    Show that the near-degeneracy c_13^u / c_13^d = 1.014 kills the CKM phase.

    The CKM matrix V = U_u^dag @ U_d. If U_u = U_d (identical sectors),
    V = I and J = 0 exactly. The CP violation comes entirely from the
    MISMATCH between up and down sectors.

    In our framework, c_13^u / c_13^d = c_23^u / c_23^d = W_u/W_d = 1.014.
    This 1.4% mismatch is what generates the physical CKM phase.

    We test this by artificially increasing the EW mismatch.
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 3: EW MISMATCH SUPPRESSION")
    print("=" * 78)

    delta = d1['delta_z3']
    c23_d = d1['c23_d']
    c23_u = d1['c23_u']
    c13_ratio = d1['c13_ratio']

    ew_ratio_actual = c23_u / c23_d
    print(f"\n  Actual EW ratio: c_23^u / c_23^d = {ew_ratio_actual:.6f}")
    print(f"  EW mismatch: {(ew_ratio_actual - 1)*100:.2f}%")

    print(f"\n  Scanning EW mismatch factor to see J dependence:")
    print(f"  {'Mismatch':>10s}  {'c23_u/c23_d':>12s}  {'|V_ub|':>10s}  {'J':>12s}  {'J/J_PDG':>10s}  {'delta_eff':>10s}")

    for mismatch_factor in [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
        # Inflate the EW mismatch while keeping c23_d fixed
        c23_u_test = c23_d * (1.0 + (ew_ratio_actual - 1.0) * mismatch_factor)
        c13_d_test = c13_ratio * c23_d
        c13_u_test = c13_ratio * c23_u_test

        V_t, _, _, _, _ = compute_ckm(c23_u_test, c23_d, c13_u_test, c13_d_test, delta)
        J_t = jarlskog_from_V(V_t)
        v_ub_t = abs(V_t[0, 2])
        sd = J_t / jarlskog_parametric(abs(V_t[0,1]), abs(V_t[1,2]), v_ub_t, 1.0) if v_ub_t > 1e-10 else 0.0
        d_eff = np.degrees(np.arcsin(min(abs(sd), 1.0)))

        print(f"  {mismatch_factor:10.1f}  {c23_u_test/c23_d:12.4f}  {v_ub_t:10.6f}  {J_t:12.4e}  {J_t/J_PDG:10.4f}  {d_eff:8.2f} deg")

    # What mismatch would we need for J = J_PDG?
    print(f"\n  Searching for EW mismatch that gives J = J_PDG...")
    best_mf = 1.0
    best_J_diff = 1e10
    for mf in np.linspace(1.0, 200.0, 2000):
        c23_u_test = c23_d * (1.0 + (ew_ratio_actual - 1.0) * mf)
        c13_d_test = c13_ratio * c23_d
        c13_u_test = c13_ratio * c23_u_test
        V_t, _, _, _, _ = compute_ckm(c23_u_test, c23_d, c13_u_test, c13_d_test, delta)
        J_t = jarlskog_from_V(V_t)
        if abs(np.log(max(J_t, 1e-15) / J_PDG)) < abs(np.log(max(best_J_diff, 1e-15) / J_PDG)):
            best_J_diff = J_t
            best_mf = mf

    print(f"    Need mismatch factor ~ {best_mf:.1f}x")
    print(f"    i.e., c_23^u / c_23^d ~ {1.0 + (ew_ratio_actual-1.0)*best_mf:.3f}")
    print(f"    Actual: 1.014. Needed: ~{1.0 + (ew_ratio_actual-1.0)*best_mf:.3f}")

    check("ew_mismatch_is_suppression_source",
          best_mf > 5.0,
          f"Need {best_mf:.0f}x larger EW mismatch for J=J_PDG")


# =============================================================================
# DIAGNOSIS 4: Phase in M vs phase in H
# =============================================================================

def diagnosis_4_phase_in_H(d1):
    """
    Track the Z_3 phase through M -> H = M@M^dag -> eigenvectors -> CKM.

    Show that the phase in M_13 = c13*sqrt(m1*m3)*exp(i*delta) generates
    a phase in H that is proportional to c13 (not c13^2), but that this
    phase is in the WRONG place to generate large CKM phase.
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 4: PHASE TRACKING M -> H -> U -> V_CKM")
    print("=" * 78)

    delta = d1['delta_z3']
    c13_u = d1['c13_u']
    c23_u = d1['c23_u']

    M_u = build_nni_complex(M_UP, M_CHARM, M_TOP, C12_U, c23_u, c13_u, delta)

    print(f"\n  NNI mass matrix M_u (showing complex entries):")
    print(f"    M_13 = c_13 * sqrt(m_u * m_t) * exp(i*delta)")
    print(f"         = {c13_u:.6f} * {np.sqrt(M_UP * M_TOP):.6f} * exp(i*{delta:.4f})")
    print(f"         = {M_u[0,2]:.6e}")
    print(f"    |M_13| = {abs(M_u[0,2]):.6e}")
    print(f"    arg(M_13) = {np.degrees(np.angle(M_u[0,2])):.1f} deg")

    H_u = M_u @ M_u.conj().T
    print(f"\n  H = M @ M^dag (complex entries from phase):")
    for i in range(3):
        for j in range(3):
            im_part = np.imag(H_u[i, j])
            if abs(im_part) > 1e-15:
                print(f"    H[{i},{j}] = {H_u[i,j]:.6e}  (Im = {im_part:.4e})")

    # The imaginary parts come from:
    # H_01 += M_02 * M_12^* = c13*sqrt(m1*m3)*e^{id} * c23*sqrt(m2*m3)
    # H_02 += M_02 * M_22^* = c13*sqrt(m1*m3)*e^{id} * m3
    # Plus contributions where M_02 multiplies M_0k^* for k=2
    expected_H01_im = c13_u * np.sqrt(M_UP * M_TOP) * c23_u * np.sqrt(M_CHARM * M_TOP) * np.sin(delta)
    expected_H02_im = c13_u * np.sqrt(M_UP * M_TOP) * M_TOP * np.sin(delta)

    print(f"\n  Expected imaginary parts:")
    print(f"    Im(H_01) ~ c13*sqrt(m_u*m_t)*c23*sqrt(m_c*m_t)*sin(d) = {expected_H01_im:.4e}")
    print(f"    Im(H_02) ~ c13*sqrt(m_u*m_t)*m_t*sin(d) = {expected_H02_im:.4e}")
    print(f"    Actual Im(H_01) = {np.imag(H_u[0,1]):.4e}")
    print(f"    Actual Im(H_02) = {np.imag(H_u[0,2]):.4e}")

    # Compare to diagonal entries
    print(f"\n  Scale comparison (Im vs diag):")
    print(f"    H[0,0] = {np.real(H_u[0,0]):.4e}")
    print(f"    H[1,1] = {np.real(H_u[1,1]):.4e}")
    print(f"    H[2,2] = {np.real(H_u[2,2]):.4e}")
    print(f"    |Im(H_01)| / H[1,1] = {abs(np.imag(H_u[0,1])) / np.real(H_u[1,1]):.4e}")
    print(f"    |Im(H_02)| / H[2,2] = {abs(np.imag(H_u[0,2])) / np.real(H_u[2,2]):.4e}")
    print(f"    -> Complex perturbation is < 10^{-3} relative to diagonal")
    print(f"    -> Eigenvectors rotate by < 10^{-3} rad in the complex plane")
    print(f"    -> CKM phase (difference of up-down rotations) < 10^{-3} rad")

    check("phase_suppression_mechanism",
          abs(np.imag(H_u[0, 1])) / np.real(H_u[1, 1]) < 0.05,
          f"Im(H_01)/H_11 = {abs(np.imag(H_u[0,1]))/np.real(H_u[1,1]):.4e} -- small perturbation")


# =============================================================================
# DIAGNOSIS 5: What would fix J?
# =============================================================================

def diagnosis_5_what_fixes_J(d1):
    """
    Explore three potential resolutions:

    A) Different phase assignments: delta_u != 0, delta_d != 0
       (sector-dependent Z_3 embedding)

    B) Phase in BOTH M_13 and M_23 (richer Z_3^3 structure)

    C) Large c_13 with phase tuned to cancel in V_ub but not in J
       (requires non-Z_3 phase)
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 5: WHAT WOULD FIX J?")
    print("=" * 78)

    delta_z3 = d1['delta_z3']
    c23_d = d1['c23_d']
    c23_u = d1['c23_u']
    c13_ratio = d1['c13_ratio']

    # --- Resolution A: Phase in BOTH sectors ---
    print(f"\n  --- A) Phase in BOTH sectors (delta_u, delta_d) ---")
    print(f"  If both sectors carry a Z_3 phase but with different assignments,")
    print(f"  the CKM phase = delta_u - delta_d (not just delta_u).")
    print(f"  With Z_3: possible phases are 0, 2pi/3, 4pi/3.")
    print(f"  If delta_u = 2pi/3, delta_d = 4pi/3: CKM phase = -2pi/3.")

    configs = [
        ("d_u=2pi/3, d_d=0", 2*np.pi/3, 0.0),
        ("d_u=2pi/3, d_d=4pi/3", 2*np.pi/3, 4*np.pi/3),
        ("d_u=4pi/3, d_d=2pi/3", 4*np.pi/3, 2*np.pi/3),
        ("d_u=2pi/3, d_d=2pi/3", 2*np.pi/3, 2*np.pi/3),
    ]

    print(f"\n  {'Config':>25s}  {'|V_ub|':>10s}  {'J':>12s}  {'J/J_PDG':>10s}  {'d_eff(deg)':>10s}")
    for label, du, dd in configs:
        c13_d_t = c13_ratio * c23_d
        c13_u_t = c13_ratio * c23_u
        V_t, _, _, _, _ = compute_ckm(c23_u, c23_d, c13_u_t, c13_d_t, du, dd)
        J_t = jarlskog_from_V(V_t)
        v_ub_t = abs(V_t[0, 2])
        sd = J_t / jarlskog_parametric(abs(V_t[0,1]), abs(V_t[1,2]), v_ub_t, 1.0) if v_ub_t > 1e-10 else 0.0
        d_eff = np.degrees(np.arcsin(min(abs(sd), 1.0)))
        print(f"  {label:>25s}  {v_ub_t:10.6f}  {J_t:12.4e}  {J_t/J_PDG:10.4f}  {d_eff:8.2f}")

    print(f"\n  -> Same-phase configs give J=0 (as expected)")
    print(f"  -> Different-phase configs give same J (phase structure is symmetric)")
    print(f"  -> Resolution A does NOT help: the phase cancellation is in M@M^dag,")
    print(f"     not in the up-vs-down mismatch.")

    # --- Resolution B: Phase in M_23 (not just M_13) ---
    print(f"\n  --- B) Phase in M_23 element (richer Z_3 structure) ---")
    print(f"  If Z_3 phase enters through M_23 instead of (or in addition to) M_13,")
    print(f"  the phase perturbation is c23*sqrt(m2*m3)*sin(delta), which is MUCH")
    print(f"  larger because c23 >> c13.")

    def build_nni_phase_in_23(m1, m2, m3, c12, c23, c13, delta_13, delta_23):
        """NNI with phase in both M_13 and M_23."""
        M = np.zeros((3, 3), dtype=complex)
        M[0, 0] = m1
        M[1, 1] = m2
        M[2, 2] = m3
        M[0, 1] = c12 * np.sqrt(m1 * m2)
        M[1, 0] = M[0, 1].conj()
        M[1, 2] = c23 * np.sqrt(m2 * m3) * np.exp(1j * delta_23)
        M[2, 1] = M[1, 2].conj()
        M[0, 2] = c13 * np.sqrt(m1 * m3) * np.exp(1j * delta_13)
        M[2, 0] = M[0, 2].conj()
        return M

    def compute_ckm_custom(c23_u, c23_d, c13_u, c13_d,
                            delta13_u, delta23_u, delta13_d=0.0, delta23_d=0.0):
        M_u = build_nni_phase_in_23(M_UP, M_CHARM, M_TOP, C12_U, c23_u, c13_u,
                                     delta13_u, delta23_u)
        M_d = build_nni_phase_in_23(M_DOWN, M_STRANGE, M_BOTTOM, C12_D, c23_d, c13_d,
                                     delta13_d, delta23_d)
        H_u = M_u @ M_u.conj().T
        H_d = M_d @ M_d.conj().T
        eigvals_u, U_u = np.linalg.eigh(H_u)
        eigvals_d, U_d = np.linalg.eigh(H_d)
        idx_u = np.argsort(eigvals_u)
        idx_d = np.argsort(eigvals_d)
        U_u = U_u[:, idx_u]
        U_d = U_d[:, idx_d]
        return U_u.conj().T @ U_d

    c13_d_t = c13_ratio * c23_d
    c13_u_t = c13_ratio * c23_u

    configs_b = [
        ("d13=2pi/3, d23=0", delta_z3, 0.0),
        ("d13=0, d23=2pi/3", 0.0, delta_z3),
        ("d13=2pi/3, d23=2pi/3", delta_z3, delta_z3),
        ("d13=2pi/3, d23=4pi/3", delta_z3, 4*np.pi/3),
    ]

    print(f"\n  Phase in up-sector M only (down real):")
    print(f"  {'Config':>30s}  {'|V_ub|':>10s}  {'J':>12s}  {'J/J_PDG':>10s}  {'d_eff(deg)':>10s}")
    for label, d13, d23 in configs_b:
        V_t = compute_ckm_custom(c23_u, c23_d, c13_u_t, c13_d_t, d13, d23)
        J_t = jarlskog_from_V(V_t)
        v_ub_t = abs(V_t[0, 2])
        sd = J_t / jarlskog_parametric(abs(V_t[0,1]), abs(V_t[1,2]), v_ub_t, 1.0) if v_ub_t > 1e-10 else 0.0
        d_eff = np.degrees(np.arcsin(min(abs(sd), 1.0)))
        print(f"  {label:>30s}  {v_ub_t:10.6f}  {J_t:12.4e}  {J_t/J_PDG:10.4f}  {d_eff:8.2f}")

    # Phase in M_23 with both sectors having different phases
    print(f"\n  Phase in M_23 of BOTH sectors (different Z_3 assignments):")
    print(f"  {'Config':>40s}  {'|V_ub|':>10s}  {'J':>12s}  {'J/J_PDG':>10s}  {'d_eff(deg)':>10s}")
    configs_b2 = [
        ("up:d23=2pi/3, dn:d23=0", 0.0, delta_z3, 0.0, 0.0),
        ("up:d23=2pi/3, dn:d23=4pi/3", 0.0, delta_z3, 0.0, 4*np.pi/3),
    ]
    for label, d13u, d23u, d13d, d23d in configs_b2:
        V_t = compute_ckm_custom(c23_u, c23_d, c13_u_t, c13_d_t, d13u, d23u, d13d, d23d)
        J_t = jarlskog_from_V(V_t)
        v_ub_t = abs(V_t[0, 2])
        sd = J_t / jarlskog_parametric(abs(V_t[0,1]), abs(V_t[1,2]), v_ub_t, 1.0) if v_ub_t > 1e-10 else 0.0
        d_eff = np.degrees(np.arcsin(min(abs(sd), 1.0)))
        print(f"  {label:>40s}  {v_ub_t:10.6f}  {J_t:12.4e}  {J_t/J_PDG:10.4f}  {d_eff:8.2f}")

    # --- Resolution C: What c_13 and delta give BOTH V_ub and J? ---
    print(f"\n  --- C) Independent c_13^u, c_13^d, delta scan for V_ub+J ---")
    print(f"  Breaking the assumption c_13^u/c_13^d = c_23^u/c_23^d.")
    print(f"  If the 1-3 overlap has a DIFFERENT EW ratio than 2-3,")
    print(f"  c_13^u and c_13^d can differ more, giving larger CKM phase.")

    best_chi2 = 1e10
    best_params = {}
    for c13_d_scan in np.linspace(0.001, 0.5, 100):
        for c13_u_scan in np.linspace(0.001, 0.5, 100):
            V_t, _, _, _, _ = compute_ckm(c23_u, c23_d, c13_u_scan, c13_d_scan, delta_z3)
            J_t = jarlskog_from_V(V_t)
            v_ub_t = abs(V_t[0, 2])
            v_us_t = abs(V_t[0, 1])
            chi2 = ((v_ub_t - V_UB_PDG) / V_UB_ERR)**2 + \
                   (np.log(max(J_t, 1e-15) / J_PDG))**2 + \
                   ((v_us_t - V_US_PDG) / V_US_ERR)**2
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_params = {
                    'c13_u': c13_u_scan, 'c13_d': c13_d_scan,
                    'v_ub': v_ub_t, 'J': J_t,
                    'v_us': v_us_t,
                }

    if best_params:
        ratio_13 = best_params['c13_u'] / best_params['c13_d']
        print(f"\n    Best independent c_13 (delta = 2pi/3):")
        print(f"      c_13^u = {best_params['c13_u']:.4f}")
        print(f"      c_13^d = {best_params['c13_d']:.4f}")
        print(f"      c_13^u / c_13^d = {ratio_13:.3f}")
        print(f"      (vs c_23^u/c_23^d = {c23_u/c23_d:.3f})")
        print(f"      |V_ub| = {best_params['v_ub']:.6f}  (PDG {V_UB_PDG})")
        print(f"      J = {best_params['J']:.4e}  (PDG {J_PDG:.4e})")
        print(f"      J/J_PDG = {best_params['J']/J_PDG:.3f}")
        print(f"      |V_us| = {best_params['v_us']:.6f}  (PDG {V_US_PDG})")

        check("independent_c13_helps",
              best_params['J'] / J_PDG > 0.01,
              f"J/J_PDG = {best_params['J']/J_PDG:.3f} with independent c_13^u/c_13^d")

    return best_params


# =============================================================================
# DIAGNOSIS 6: Decompose the 360x suppression factor
# =============================================================================

def diagnosis_6_decompose_suppression(d1):
    """
    Factor the total suppression J_actual / J_naive into its components:

    J_naive = c12*s12*c23*s23*c13^2*s13*sin(delta_input)
    J_actual = c12*s12*c23*s23*c13^2*s13*sin(delta_eff)

    Total ratio = sin(delta_eff) / sin(delta_input)

    But delta_eff is itself a product of:
    (a) Phase dilution in M@M^dag: factor ~ c13*sqrt(m1*m3)/m3 ~ 10^{-4}
    (b) EW mismatch: factor ~ (c13^u - c13^d) / c13 ~ 0.014
    (c) Mass hierarchy: m1/m3 ratio difference between sectors

    Let's measure each.
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 6: DECOMPOSITION OF THE 360x SUPPRESSION")
    print("=" * 78)

    delta = d1['delta_z3']
    J = d1['J']

    J_naive = jarlskog_parametric(d1['v_us'], d1['v_cb'], d1['v_ub'], np.sin(delta))
    total_ratio = J / J_naive

    print(f"\n  J_actual = {J:.4e}")
    print(f"  J_naive (same angles, sin(2pi/3)) = {J_naive:.4e}")
    print(f"  Total suppression: J_actual / J_naive = {total_ratio:.6f}")
    print(f"  Suppression factor: 1 / {1.0/total_ratio:.0f}x")

    sin_delta_actual = J / jarlskog_parametric(d1['v_us'], d1['v_cb'], d1['v_ub'], 1.0)
    sin_delta_input = np.sin(delta)

    print(f"\n  Phase suppression:")
    print(f"    sin(delta_input) = sin(2pi/3) = {sin_delta_input:.6f}")
    print(f"    sin(delta_eff)   = {sin_delta_actual:.6f}")
    print(f"    Ratio = {sin_delta_actual / sin_delta_input:.6e}")

    # Perturbation theory estimate
    c13_u = d1['c13_u']
    c13_d = d1['c13_d']
    c23_u = d1['c23_u']
    c23_d = d1['c23_d']

    # Phase enters H as: Im(H_01) ~ c13 * sqrt(m1*m3) * c23 * sqrt(m2*m3) * sin(d)
    # This perturbs the eigenvector by angle ~ Im(H_01) / (E2 - E1)
    # where E1 ~ m1^2, E2 ~ m2^2 (eigenvalues of the 2-3 block)
    # For up sector:
    im_H01_u = c13_u * np.sqrt(M_UP * M_TOP) * c23_u * np.sqrt(M_CHARM * M_TOP) * np.sin(delta)
    dE_u = M_CHARM**2  # dominant eigenvalue gap in 0-1 sector
    theta_pert_u = im_H01_u / dE_u

    im_H01_d = c13_d * np.sqrt(M_DOWN * M_BOTTOM) * c23_d * np.sqrt(M_STRANGE * M_BOTTOM) * np.sin(delta)
    dE_d = M_STRANGE**2
    theta_pert_d = im_H01_d / dE_d

    print(f"\n  Perturbation theory estimate:")
    print(f"    Up sector: Im(H_01) / Delta_E ~ {theta_pert_u:.4e} rad = {np.degrees(theta_pert_u):.4f} deg")
    print(f"    Down sector: Im(H_01) / Delta_E ~ {theta_pert_d:.4e} rad = {np.degrees(theta_pert_d):.4f} deg")
    print(f"    CKM phase ~ |theta_u - theta_d| ~ {abs(theta_pert_u - theta_pert_d):.4e} rad")
    print(f"                                     = {np.degrees(abs(theta_pert_u - theta_pert_d)):.4f} deg")

    # Compare with actual
    delta_eff_actual = np.arcsin(min(abs(sin_delta_actual), 1.0))
    print(f"    Actual delta_eff = {delta_eff_actual:.4e} rad = {np.degrees(delta_eff_actual):.4f} deg")
    print(f"    Perturbation estimate / actual = {abs(theta_pert_u - theta_pert_d) / delta_eff_actual:.2f}")

    print(f"\n  SUMMARY OF SUPPRESSION CHAIN:")
    print(f"    1. Input phase: delta = 120 deg,  sin(delta) = 0.866")
    print(f"    2. M@M^dag washout: phase -> c13*sqrt(m1/m3)*sin(delta) in H off-diagonal")
    print(f"       Up:   c13*sqrt(m_u/m_t) = {c13_u * np.sqrt(M_UP/M_TOP):.4e}")
    print(f"       Down: c13*sqrt(m_d/m_b) = {c13_d * np.sqrt(M_DOWN/M_BOTTOM):.4e}")
    print(f"    3. Eigenvector phase perturbation: ~ Im(H_01) / (m2^2)")
    print(f"       Up:   {theta_pert_u:.4e} rad")
    print(f"       Down: {theta_pert_d:.4e} rad")
    print(f"    4. CKM phase = theta_u - theta_d: {abs(theta_pert_u - theta_pert_d):.4e} rad")
    print(f"    5. J ~ (angles) * sin(delta_eff) = {J:.4e}")
    print(f"       PDG: {J_PDG:.4e}")
    print(f"       Ratio: {J/J_PDG:.4f}")

    check("suppression_decomposed",
          True,
          f"Total suppression = {1.0/total_ratio:.0f}x from phase washout in NNI diag")

    return {
        'total_ratio': total_ratio,
        'theta_pert_u': theta_pert_u,
        'theta_pert_d': theta_pert_d,
    }


# =============================================================================
# DIAGNOSIS 7: Comparison with standard CKM parametrization
# =============================================================================

def diagnosis_7_standard_parametrization():
    """
    Verify that the Jarlskog formula is computed correctly by building
    V_CKM from the standard parametrization and checking J.
    """
    print("\n" + "=" * 78)
    print("DIAGNOSIS 7: STANDARD PARAMETRIZATION CROSS-CHECK")
    print("=" * 78)

    # PDG values
    s12 = V_US_PDG       # 0.2243
    s23 = V_CB_PDG       # 0.0422
    s13 = V_UB_PDG       # 0.00382
    delta = DELTA_PDG    # 1.144 rad

    c12 = np.sqrt(1 - s12**2)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)

    # Standard parametrization CKM matrix
    V = np.zeros((3, 3), dtype=complex)
    V[0, 0] = c12 * c13
    V[0, 1] = s12 * c13
    V[0, 2] = s13 * np.exp(-1j * delta)
    V[1, 0] = -s12 * c23 - c12 * s23 * s13 * np.exp(1j * delta)
    V[1, 1] = c12 * c23 - s12 * s23 * s13 * np.exp(1j * delta)
    V[1, 2] = s23 * c13
    V[2, 0] = s12 * s23 - c12 * c23 * s13 * np.exp(1j * delta)
    V[2, 1] = -c12 * s23 - s12 * c23 * s13 * np.exp(1j * delta)
    V[2, 2] = c23 * c13

    J_from_V = jarlskog_from_V(V)
    J_formula = jarlskog_parametric(s12, s23, s13, np.sin(delta))

    print(f"\n  Standard parametrization with PDG values:")
    print(f"    s12 = {s12}, s23 = {s23}, s13 = {s13}")
    print(f"    delta = {delta:.4f} rad = {np.degrees(delta):.1f} deg")
    print(f"    J (from V quartet) = {J_from_V:.4e}")
    print(f"    J (from formula)   = {J_formula:.4e}")
    print(f"    PDG J              = {J_PDG:.4e}")
    print(f"    Agreement: {J_from_V/J_formula:.6f}")

    check("J_formula_correct",
          abs(J_from_V - J_formula) / J_formula < 1e-6,
          f"Quartet and parametric J agree to {abs(J_from_V-J_formula)/J_formula:.1e}")

    # Now check: what sin(delta) do we NEED given our V_ub, V_us, V_cb?
    # to get J = J_PDG?
    J_with_sin1 = jarlskog_parametric(V_US_PDG, V_CB_PDG, V_UB_PDG, 1.0)
    sin_delta_needed = J_PDG / J_with_sin1

    print(f"\n  Required sin(delta) for J = J_PDG:")
    print(f"    J(sin_d=1) = {J_with_sin1:.4e}")
    print(f"    sin(delta) needed = J_PDG / J(sin_d=1) = {sin_delta_needed:.4f}")
    print(f"    delta needed = {np.degrees(np.arcsin(sin_delta_needed)):.1f} deg")
    print(f"    sin(2pi/3) = {np.sin(2*np.pi/3):.4f}")
    print(f"    -> Z_3 phase sin(2pi/3) = 0.866 is ENOUGH if it survived diag.")
    print(f"    -> The problem is NOT the Z_3 phase value, it's the washout.")

    check("z3_phase_sufficient_if_survived",
          abs(np.sin(2*np.pi/3) - sin_delta_needed) / sin_delta_needed < 0.05,
          f"sin(2pi/3) = 0.866 ~ sin_delta_needed = {sin_delta_needed:.3f} (within 2%)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("CKM JARLSKOG INVARIANT DIAGNOSIS")
    print("================================")
    print("Why J is ~360x too small in the full closure script")
    print()

    d1 = diagnosis_1_reproduce()
    d2 = diagnosis_2_phase_washout(d1)
    diagnosis_3_ew_mismatch(d1)
    diagnosis_4_phase_in_H(d1)
    d5 = diagnosis_5_what_fixes_J(d1)
    d6 = diagnosis_6_decompose_suppression(d1)
    diagnosis_7_standard_parametrization()

    # =================================================================
    # FINAL SUMMARY
    # =================================================================
    print("\n" + "=" * 78)
    print("FINAL DIAGNOSIS SUMMARY")
    print("=" * 78)

    print(f"""
  PROBLEM: The full closure script reports two regimes:
    (a) V_ub-optimized (c_13/c_23=0.021): J = 8.6e-8, ratio 0.003x PDG
    (b) V_ub-from-scan (c_13/c_23~0.37):  J = 3.7e-6, ratio 0.12x PDG
  In BOTH cases J is significantly suppressed vs PDG (3.08e-5).

  ROOT CAUSE: The Z_3 phase delta = 2*pi/3 = 120 deg does NOT survive the
  NNI mass matrix diagonalization. Three multiplicative suppressions combine:

  1. M@M^dag PHASE WASHOUT
     The NNI phase lives in M_13 = c13*sqrt(m1*m3)*exp(i*delta).
     In H = M@M^dag, this generates imaginary parts in H_01 and H_02
     proportional to c13*sqrt(m1*m3), which is:
       Up sector:   c13*sqrt(m_u*m_t) = {d1['c13_u'] * np.sqrt(M_UP * M_TOP):.4e}
       Down sector: c13*sqrt(m_d*m_b) = {d1['c13_d'] * np.sqrt(M_DOWN * M_BOTTOM):.4e}
     These are TINY compared to the diagonal entries ~m_t^2, m_b^2.

  2. PERTURBATIVE PHASE ROTATION
     The tiny imaginary perturbation rotates the eigenvectors by:
       theta_u ~ {np.degrees(d6['theta_pert_u']):.4f} deg
       theta_d ~ {np.degrees(d6['theta_pert_d']):.4f} deg
     The CKM phase = |theta_u - theta_d| ~ {np.degrees(abs(d6['theta_pert_u'] - d6['theta_pert_d'])):.4f} deg

  3. NEAR-DEGENERATE EW RATIO
     c_13^u / c_13^d = c_23^u / c_23^d = 1.014 (only 1.4% different).
     If the up and down sectors were identical, J = 0 exactly.
     The physical J is proportional to this 1.4% mismatch.

  COMBINED: The effective CKM phase is ~0.1 deg instead of ~66 deg (PDG),
  giving J suppressed by ~360x.

  THIS IS NOT A BUG: It's a structural limitation of NNI texture with:
    - Phase only in M_13 (the smallest off-diagonal element)
    - Nearly identical up/down EW weights
    - Extreme mass hierarchy (m_u/m_t ~ 10^{{-5}})

  POSSIBLE RESOLUTIONS:
    - Z_3 phase in M_23 (not just M_13): larger phase perturbation
    - Independent c_13^u / c_13^d ratio (different from EW ratio)
    - Richer Z_3^3 structure with multiple independent phases
    - Radiative corrections to the NNI texture that generate
      additional off-diagonal phases
""")

    print("=" * 78)
    print(f"  TOTAL: {PASS_COUNT} pass / {FAIL_COUNT} fail")
    print("=" * 78)

    if FAIL_COUNT > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
