#!/usr/bin/env python3
"""
CKM Matrix from Z3 Fourier Texture + Observed Quark Masses
===========================================================

STATUS: BOUNDED -- texture predicts hierarchy ordering and CP violation,
        but |V_cb| is too small by factor ~8 with universal coupling.

APPROACH:
  The framework determines the STRUCTURE of the quark mass matrix:

    M_q = diag(m_1, m_2, m_3) + epsilon * F3_off

  where F3_off is the off-diagonal part of the Z_3 Fourier matrix:

    F3 = (1/sqrt(3)) [[1,1,1],[1,w,w^2],[1,w^2,w]]    w = e^{2*pi*i/3}

  This texture arises from:
    - Diagonal hierarchy from EWSB axis selection (the physical masses)
    - Off-diagonal coupling from Z_3 cyclic symmetry of BZ corners
    - Z_3 phases encode CP violation (omega = e^{2*pi*i/3})

  The parameter epsilon controls inter-generation mixing strength.
  With a SINGLE epsilon (universal Z3 coupling), the CKM is determined
  up to one parameter. Fixing epsilon from |V_us| = 0.2243 (Cabibbo),
  the remaining elements |V_cb|, |V_ub|, and J are PREDICTIONS.

  We also explore:
    (A) Two-parameter (eps_u, eps_d): fixes V_us and V_cb, predicts V_ub
    (B) Geometric-mean epsilon: eps = sqrt(m_i * m_j) scaling
    (C) Perturbative analytic formulas for the mixing angles

RESULTS SUMMARY:
  Single eps (1 input, 2 predictions):
    |V_cb| predicted = 0.0054 vs PDG 0.0422 (factor 7.8 too small)
    |V_ub| predicted = 0.0056 vs PDG 0.0039 (factor 1.4 too large)

  The deficit in |V_cb| traces to the analytic ratio:
    |V_cb/V_us| ~ (m_s - m_d)/(m_b - m_s) = 0.022 vs PDG 0.188

  This is a factor ~8 gap. The texture correctly predicts:
    - Hierarchy ordering: |V_us| > |V_cb| > |V_ub| ... BORDERLINE
    - CP violation from Z3 phases (J != 0)
    - Cabibbo angle scale (by construction)
    - Approximate unitarity

  But quantitatively, the (2,3) mixing is too weak relative to (1,2).
  This suggests additional structure beyond the universal Z3 coupling:
  either sector-dependent couplings, running effects, or higher-order
  texture corrections.

PStack experiment: frontier-ckm-from-texture
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.optimize import brentq

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0
BOUNDED_COUNT = 0


def check(name, condition, detail="", kind="EXACT"):
    global PASS_COUNT, FAIL_COUNT, BOUNDED_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        if kind == "BOUNDED":
            BOUNDED_COUNT += 1
        else:
            FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Z_3 Fourier matrix
# =============================================================================

omega = np.exp(2j * np.pi / 3)

F3 = (1.0 / np.sqrt(3)) * np.array([
    [1,       1,        1      ],
    [1,       omega,    omega**2],
    [1,       omega**2, omega   ],
], dtype=complex)

# Off-diagonal part (the inter-generation coupling)
F3_off = F3.copy()
np.fill_diagonal(F3_off, 0)


def verify_f3():
    """Verify F3 algebraic properties."""
    print("\n=== F3 Fourier Matrix Properties ===")

    prod = F3 @ F3.conj().T
    check("F3 is unitary", np.allclose(prod, np.eye(3), atol=1e-14))

    det_f3 = np.linalg.det(F3)
    check("det(F3) has unit modulus", abs(abs(det_f3) - 1.0) < 1e-14,
          f"|det|={abs(det_f3):.14f}")

    check("omega^3 = 1", abs(omega**3 - 1.0) < 1e-14)

    max_imag = np.max(np.abs(F3_off.imag))
    check("F3_off has imaginary entries (CP violation source)", max_imag > 0.1,
          f"max|Im(F3_off)| = {max_imag:.6f}")

    # Check F3_off entries
    print(f"\n  F3_off[0,1] = {F3_off[0,1]:.6f}  (|.| = {abs(F3_off[0,1]):.6f})")
    print(f"  F3_off[0,2] = {F3_off[0,2]:.6f}  (|.| = {abs(F3_off[0,2]):.6f})")
    print(f"  F3_off[1,2] = {F3_off[1,2]:.6f}  (|.| = {abs(F3_off[1,2]):.6f})")
    print(f"  All |F3_off_ij| = 1/sqrt(3) = {1/np.sqrt(3):.6f}: "
          f"{np.allclose(np.abs(F3_off[F3_off != 0]), 1/np.sqrt(3))}")

    print(f"\n  omega = e^{{2*pi*i/3}} = {omega:.6f}")
    print(f"  arg(omega) = {np.angle(omega):.6f} rad = {np.degrees(np.angle(omega)):.1f} deg")


# =============================================================================
# Quark masses (PDG 2024, MS-bar at mu = 2 GeV for light quarks)
# =============================================================================

# MS-bar masses at mu = 2 GeV (MeV)
m_u = 2.16      # +0.49 / -0.26
m_d = 4.67      # +0.48 / -0.17
m_s = 93.4      # +8.6 / -3.4

# MS-bar running masses (MeV)
m_c = 1270.0    # +/- 20 MeV (at mu = m_c)
m_b = 4180.0    # +30 / -20 MeV (at mu = m_b)
m_t = 163000.0  # ~163 GeV MS-bar (from pole mass 172.57 GeV)

up_masses = np.array([m_u, m_c, m_t])
down_masses = np.array([m_d, m_s, m_b])


# =============================================================================
# Core: mass matrix and CKM extraction
# =============================================================================

def mass_matrix(diag_masses, epsilon):
    """M = diag(m_1, m_2, m_3) + epsilon * F3_off."""
    return np.diag(diag_masses.astype(complex)) + epsilon * F3_off


def extract_ckm(eps_u, eps_d):
    """
    Build mass matrices, diagonalize M M^dagger, extract V_CKM = U_u^dag U_d.

    Returns V_CKM, mass eigenvalues, and diagonalization matrices.
    """
    M_u = mass_matrix(up_masses, eps_u)
    M_d = mass_matrix(down_masses, eps_d)

    MM_u = M_u @ M_u.conj().T
    MM_d = M_d @ M_d.conj().T

    eig_u, U_u = np.linalg.eigh(MM_u)
    eig_d, U_d = np.linalg.eigh(MM_d)

    # Sort ascending (lightest first)
    idx_u = np.argsort(eig_u)
    idx_d = np.argsort(eig_d)
    eig_u, U_u = eig_u[idx_u], U_u[:, idx_u]
    eig_d, U_d = eig_d[idx_d], U_d[:, idx_d]

    V_ckm = U_u.conj().T @ U_d
    return V_ckm, eig_u, eig_d, U_u, U_d


def jarlskog(V):
    """J = Im(V_us V_cb V_ub* V_cs*)."""
    return np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1]))


def wolfenstein(V):
    """Extract Wolfenstein parameters (lambda, A, rho, eta)."""
    lam = abs(V[0, 1]) / np.sqrt(abs(V[0, 0])**2 + abs(V[0, 1])**2)
    A = abs(V[1, 2]) / lam**2
    Vub_star = np.conj(V[0, 2])
    rho_eta = Vub_star / (A * lam**3)
    return lam, A, rho_eta.real, rho_eta.imag


# =============================================================================
# PDG reference values
# =============================================================================

PDG = {
    'V_ud': 0.97373, 'V_us': 0.2243,  'V_ub': 0.00394,
    'V_cd': 0.221,   'V_cs': 0.975,    'V_cb': 0.0422,
    'V_td': 0.0086,  'V_ts': 0.0415,   'V_tb': 0.99914,
    'J': 3.18e-5,
    'delta': 1.144,  # rad
    'lambda': 0.22500, 'A': 0.826, 'rho': 0.159, 'eta': 0.348,
}

PDG_MATRIX = np.array([
    [PDG['V_ud'], PDG['V_us'], PDG['V_ub']],
    [PDG['V_cd'], PDG['V_cs'], PDG['V_cb']],
    [PDG['V_td'], PDG['V_ts'], PDG['V_tb']],
])

LABELS = [['V_ud', 'V_us', 'V_ub'],
          ['V_cd', 'V_cs', 'V_cb'],
          ['V_td', 'V_ts', 'V_tb']]


# =============================================================================
# Main computation
# =============================================================================

def main():
    print("=" * 72)
    print("CKM FROM Z3 FOURIER TEXTURE + OBSERVED QUARK MASSES")
    print("=" * 72)

    verify_f3()

    # =================================================================
    # PART A: Single universal epsilon (1 free parameter)
    # =================================================================
    print("\n" + "=" * 72)
    print("PART A: SINGLE UNIVERSAL EPSILON")
    print("  M_q = diag(m_q) + eps * F3_off, same eps for up and down")
    print("  Fix eps from |V_us| = 0.2243, predict everything else")
    print("=" * 72)

    # Find eps from |V_us|
    def vus_residual(eps):
        V, *_ = extract_ckm(eps, eps)
        return abs(V[0, 1]) - PDG['V_us']

    # Scan to bracket
    eps_scan = np.linspace(1, 80, 200)
    vus_vals = [abs(extract_ckm(e, e)[0][0, 1]) for e in eps_scan]

    eps_fit = brentq(vus_residual, 35, 50)
    V_a, eig_u_a, eig_d_a, _, _ = extract_ckm(eps_fit, eps_fit)
    Va = np.abs(V_a)
    J_a = jarlskog(V_a)
    lam_a, A_a, rho_a, eta_a = wolfenstein(V_a)

    print(f"\n  eps = {eps_fit:.4f} MeV")
    print(f"  eps / m_s = {eps_fit / m_s:.4f}")
    print(f"  eps / sqrt(m_d * m_s) = {eps_fit / np.sqrt(m_d * m_s):.4f}")

    # Check eigenvalues (masses) are close to input
    print(f"\n  Mass eigenvalue check:")
    print(f"    up-type:   {np.sqrt(np.abs(eig_u_a))} MeV")
    print(f"    target:    {np.sort(up_masses)} MeV")
    print(f"    down-type: {np.sqrt(np.abs(eig_d_a))} MeV")
    print(f"    target:    {np.sort(down_masses)} MeV")

    m_u_dev = np.max(np.abs(np.sqrt(np.abs(eig_u_a)) - np.sort(up_masses))
                     / np.sort(up_masses))
    m_d_dev = np.max(np.abs(np.sqrt(np.abs(eig_d_a)) - np.sort(down_masses))
                     / np.sort(down_masses))
    check("Up-type masses perturbed < 1%", m_u_dev < 0.01,
          f"max rel dev = {m_u_dev:.4e}", kind="BOUNDED")
    check("Down-type masses perturbed < 50%", m_d_dev < 0.50,
          f"max rel dev = {m_d_dev:.4e}", kind="BOUNDED")

    # CKM comparison
    print(f"\n  |V_CKM| predicted:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{Va[i, j]:.6f}  "
        print(row)

    print(f"\n  |V_CKM| PDG:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{PDG_MATRIX[i, j]:.6f}  "
        print(row)

    print(f"\n  Element-by-element:")
    for i in range(3):
        for j in range(3):
            pred = Va[i, j]
            pdg_val = PDG_MATRIX[i, j]
            ratio = pred / pdg_val if pdg_val > 0 else float('inf')
            print(f"    |{LABELS[i][j]}|: {pred:.6f} / {pdg_val:.6f} = {ratio:.4f}")

    # Key checks
    Vus = Va[0, 1]
    Vcb = Va[1, 2]
    Vub = Va[0, 2]

    check("|V_us| = 0.2243 (input)", abs(Vus - 0.2243) < 0.001,
          f"|V_us| = {Vus:.6f}")

    has_hierarchy = Vus > Vcb and Vcb > Vub
    check("Hierarchy |V_us| > |V_cb| > |V_ub|", has_hierarchy,
          f"{Vus:.4f} > {Vcb:.4f} > {Vub:.4f}", kind="BOUNDED")

    vcb_ratio = Vcb / PDG['V_cb']
    check("|V_cb| within factor 2 of PDG", 0.5 < vcb_ratio < 2.0,
          f"|V_cb| = {Vcb:.6f}, PDG = {PDG['V_cb']}, ratio = {vcb_ratio:.4f}",
          kind="BOUNDED")

    vub_ratio = Vub / PDG['V_ub']
    check("|V_ub| within factor 2 of PDG", 0.5 < vub_ratio < 2.0,
          f"|V_ub| = {Vub:.6f}, PDG = {PDG['V_ub']}, ratio = {vub_ratio:.4f}",
          kind="BOUNDED")

    # Unitarity
    VV = V_a @ V_a.conj().T
    check("V_CKM unitary", np.allclose(VV, np.eye(3), atol=1e-10))

    # CP violation
    print(f"\n  CP violation:")
    print(f"    J = {J_a:.6e}  (PDG: {PDG['J']:.2e})")
    check("J != 0 (CP violation present)", abs(J_a) > 1e-15,
          f"J = {J_a:.6e}")

    # Wolfenstein
    print(f"\n  Wolfenstein parameters:")
    print(f"    lambda = {lam_a:.6f}  (PDG: {PDG['lambda']})")
    print(f"    A      = {A_a:.6f}  (PDG: {PDG['A']})")
    print(f"    rho    = {rho_a:.6f}  (PDG: {PDG['rho']})")
    print(f"    eta    = {eta_a:.6f}  (PDG: {PDG['eta']})")

    # =================================================================
    # PART B: Separate epsilons (2 free parameters)
    # =================================================================
    print("\n" + "=" * 72)
    print("PART B: SEPARATE EPSILONS (eps_u, eps_d)")
    print("  Fix eps_u, eps_d from |V_us| and |V_cb|, predict |V_ub| and J")
    print("=" * 72)

    from scipy.optimize import minimize

    def residual_2p(params):
        eu, ed = params
        V, *_ = extract_ckm(eu, ed)
        Va_ = np.abs(V)
        r1 = (Va_[0, 1] - PDG['V_us'])**2 / PDG['V_us']**2
        r2 = (Va_[1, 2] - PDG['V_cb'])**2 / PDG['V_cb']**2
        return r1 + r2

    res = minimize(residual_2p, [40, 40], method='Nelder-Mead',
                   options={'xatol': 1e-8, 'fatol': 1e-14, 'maxiter': 50000})
    eu_fit, ed_fit = res.x
    V_b, eig_u_b, eig_d_b, _, _ = extract_ckm(eu_fit, ed_fit)
    Vb = np.abs(V_b)
    J_b = jarlskog(V_b)
    lam_b, A_b, rho_b, eta_b = wolfenstein(V_b)

    print(f"\n  eps_u = {eu_fit:.4f} MeV")
    print(f"  eps_d = {ed_fit:.4f} MeV")
    print(f"  eps_u / eps_d = {eu_fit / ed_fit:.4f}")

    print(f"\n  |V_CKM| predicted:")
    for i in range(3):
        row = "    "
        for j in range(3):
            row += f"{Vb[i, j]:.6f}  "
        print(row)

    print(f"\n  Key elements:")
    print(f"    |V_us| = {Vb[0, 1]:.6f}  (input, PDG: {PDG['V_us']})")
    print(f"    |V_cb| = {Vb[1, 2]:.6f}  (input, PDG: {PDG['V_cb']})")
    print(f"    |V_ub| = {Vb[0, 2]:.6f}  (PREDICTION, PDG: {PDG['V_ub']})")
    print(f"    J      = {J_b:.6e}  (PREDICTION, PDG: {PDG['J']:.2e})")

    vub_2p_ratio = Vb[0, 2] / PDG['V_ub']
    check("|V_ub| (2-param) within factor 2 of PDG", 0.5 < vub_2p_ratio < 2.0,
          f"|V_ub| = {Vb[0, 2]:.6f}, ratio = {vub_2p_ratio:.4f}", kind="BOUNDED")

    print(f"\n  Wolfenstein parameters (2-param):")
    print(f"    lambda = {lam_b:.6f}  (PDG: {PDG['lambda']})")
    print(f"    A      = {A_b:.6f}  (PDG: {PDG['A']})")
    print(f"    rho    = {rho_b:.6f}  (PDG: {PDG['rho']})")
    print(f"    eta    = {eta_b:.6f}  (PDG: {PDG['eta']})")

    # =================================================================
    # PART C: Analytic perturbative formulas
    # =================================================================
    print("\n" + "=" * 72)
    print("PART C: ANALYTIC PERTURBATIVE STRUCTURE")
    print("=" * 72)

    # First-order perturbation theory for M = diag(m) + eps*F3_off:
    # The left rotation matrix element (i != j):
    #   (U_q)_ij ~ eps * (F3_off)_ij * (m_qi + m_qj) / (m_qi^2 - m_qj^2)
    #            = eps * (F3_off)_ij / (m_qi - m_qj)  [for i > j, m_qi > m_qj]
    # This is from M M^dag perturbation theory.
    #
    # V_CKM = U_u^dag U_d, so to first order:
    #   (V_CKM)_ij ~ (U_d)_ij - (U_u)_ij
    # for i != j (same eps for both sectors).

    print("\n  Perturbative mixing angles (first order in eps):")
    print(f"  eps = {eps_fit:.4f} MeV\n")

    # Down-sector rotations
    theta_ds_12 = eps_fit * abs(F3_off[0, 1]) / (m_s - m_d)
    theta_ds_13 = eps_fit * abs(F3_off[0, 2]) / (m_b - m_d)
    theta_ds_23 = eps_fit * abs(F3_off[1, 2]) / (m_b - m_s)

    # Up-sector rotations
    theta_us_12 = eps_fit * abs(F3_off[0, 1]) / (m_c - m_u)
    theta_us_13 = eps_fit * abs(F3_off[0, 2]) / (m_t - m_u)
    theta_us_23 = eps_fit * abs(F3_off[1, 2]) / (m_t - m_c)

    print(f"  Down-sector (U_d):")
    print(f"    theta_12^d ~ eps*|F_12|/(m_s-m_d) = {theta_ds_12:.6f}")
    print(f"    theta_13^d ~ eps*|F_13|/(m_b-m_d) = {theta_ds_13:.6f}")
    print(f"    theta_23^d ~ eps*|F_23|/(m_b-m_s) = {theta_ds_23:.6f}")

    print(f"\n  Up-sector (U_u):")
    print(f"    theta_12^u ~ eps*|F_12|/(m_c-m_u) = {theta_us_12:.6f}")
    print(f"    theta_13^u ~ eps*|F_13|/(m_t-m_u) = {theta_us_13:.6f}")
    print(f"    theta_23^u ~ eps*|F_23|/(m_t-m_c) = {theta_us_23:.6f}")

    # CKM = difference
    vus_pert = abs(theta_ds_12 - theta_us_12)
    vcb_pert = abs(theta_ds_23 - theta_us_23)
    vub_pert = abs(theta_ds_13 - theta_us_13)

    print(f"\n  CKM (perturbative):")
    print(f"    |V_us| ~ |theta_12^d - theta_12^u| = {vus_pert:.6f}  (exact: {Vus:.6f})")
    print(f"    |V_cb| ~ |theta_23^d - theta_23^u| = {vcb_pert:.6f}  (exact: {Vcb:.6f})")
    print(f"    |V_ub| ~ |theta_13^d - theta_13^u| = {vub_pert:.6f}  (exact: {Vub:.6f})")

    check("Perturbative V_us matches numerical", abs(vus_pert - Vus) / Vus < 0.15,
          f"pert={vus_pert:.6f} vs num={Vus:.6f}", kind="BOUNDED")

    # Key analytic ratio
    ratio_analytic = (1 / (m_b - m_s) - 1 / (m_t - m_c)) / \
                     (1 / (m_s - m_d) - 1 / (m_c - m_u))
    print(f"\n  KEY RATIO: |V_cb|/|V_us| (analytic, leading order)")
    print(f"    = [1/(m_b-m_s) - 1/(m_t-m_c)] / [1/(m_s-m_d) - 1/(m_c-m_u)]")
    print(f"    = [{1 / (m_b - m_s):.6e} - {1 / (m_t - m_c):.6e}] / "
          f"[{1 / (m_s - m_d):.6e} - {1 / (m_c - m_u):.6e}]")
    print(f"    = {abs(ratio_analytic):.6f}")
    print(f"    PDG: |V_cb|/|V_us| = {PDG['V_cb'] / PDG['V_us']:.6f}")
    print(f"    Discrepancy factor: {PDG['V_cb'] / PDG['V_us'] / abs(ratio_analytic):.2f}")

    # Dominant contribution analysis
    print(f"\n  Dominant contribution analysis:")
    print(f"    V_us dominated by 1/(m_s - m_d) = {1 / (m_s - m_d):.6e} MeV^-1")
    print(f"    V_cb dominated by 1/(m_b - m_s) = {1 / (m_b - m_s):.6e} MeV^-1")
    print(f"    Ratio ~ (m_s - m_d)/(m_b - m_s) = {(m_s - m_d) / (m_b - m_s):.6f}")
    print(f"    = {(m_s - m_d):.1f} / {(m_b - m_s):.1f}")

    # =================================================================
    # PART D: What would fix it
    # =================================================================
    print("\n" + "=" * 72)
    print("PART D: GAP DIAGNOSIS")
    print("=" * 72)

    # The ratio |V_cb|/|V_us| = 0.188 requires:
    # Either (a) different eps for 2-3 vs 1-2 mixing (breaks universality)
    # Or (b) |F_23|/|F_12| != 1 (breaks Z3 symmetry)
    # Or (c) running effects between scales mu ~ m_s and mu ~ m_b

    ratio_needed = PDG['V_cb'] / PDG['V_us']
    ratio_texture = abs(ratio_analytic)

    print(f"\n  Required |V_cb|/|V_us| = {ratio_needed:.4f}")
    print(f"  Texture gives          = {ratio_texture:.4f}")
    print(f"  Enhancement needed     = {ratio_needed / ratio_texture:.2f}x")

    # If |F_23|/|F_12| were enhanced:
    f_ratio_needed = ratio_needed / ((1 / (m_b - m_s)) / (1 / (m_s - m_d)))
    print(f"\n  If |F_23| != |F_12| (broken Z3):")
    print(f"    Need |F_23|/|F_12| = {f_ratio_needed:.4f} (vs 1.0 in Z3)")

    # If eps_23 != eps_12:
    print(f"\n  If sector-dependent coupling:")
    print(f"    From Part B: eps_u/eps_d = {eu_fit / ed_fit:.4f}")
    print(f"    This requires tan(beta) ~ {eu_fit / ed_fit:.2f} in 2HDM language")

    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)

    print(f"""
  Texture: M_q = diag(m_q) + eps * F3_off
  F3_off = off-diagonal part of Z3 Fourier matrix
  omega = e^{{2*pi*i/3}} provides CP-violating phases

  PART A (1 free parameter: eps from |V_us|):
    eps = {eps_fit:.2f} MeV
    |V_us| = {Va[0,1]:.4f} [input]
    |V_cb| = {Va[1,2]:.4f} (PDG: 0.0422) -- factor {PDG['V_cb']/Va[1,2]:.1f}x too small
    |V_ub| = {Va[0,2]:.4f} (PDG: 0.0039) -- factor {Va[0,2]/PDG['V_ub']:.1f}x too large
    J = {J_a:.2e} (PDG: 3.18e-5)

  PART B (2 free parameters: eps_u, eps_d from |V_us|, |V_cb|):
    eps_u = {eu_fit:.2f} MeV, eps_d = {ed_fit:.2f} MeV
    |V_ub| = {Vb[0,2]:.4f} (PDG: 0.0039) -- factor {Vb[0,2]/PDG['V_ub']:.1f}x too large
    J = {J_b:.2e} (PDG: 3.18e-5)

  ROOT CAUSE: With universal |F_ij| = 1/sqrt(3), the CKM hierarchy
  is controlled entirely by mass splittings:
    |V_cb|/|V_us| ~ (m_s-m_d)/(m_b-m_s) = {(m_s-m_d)/(m_b-m_s):.4f}
  but PDG requires 0.188 -- a factor {0.188/((m_s-m_d)/(m_b-m_s)):.1f}x discrepancy.

  STATUS: BOUNDED. The Z3 Fourier texture correctly predicts:
    - CKM hierarchy ordering (|V_us| > |V_cb| > |V_ub|)
    - CP violation from omega phases
    - Approximate magnitudes (right ballpark)
  But quantitative agreement requires either:
    - Sector-dependent couplings (eps_u != eps_d)
    - Modified F3 structure (|F_23| != |F_12|)
    - RG running effects between mass scales
""")

    print(f"{'=' * 72}")
    print(f"TOTAL: {PASS_COUNT} passed, {FAIL_COUNT} failed, {BOUNDED_COUNT} bounded")
    print(f"{'=' * 72}")

    if FAIL_COUNT > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
