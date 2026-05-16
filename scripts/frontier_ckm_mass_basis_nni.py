#!/usr/bin/env python3
"""
CKM Mass-Basis NNI: V_ub from Schur Complement + Mass-Ratio Suppression
========================================================================

STATUS: BOUNDED, historical / diagnostic only. Re-audited 2026-05-16 under
        ledger row work_history.ckm.ckm_mass_basis_nni_note (status
        audited_numerical_match, class G).

WHAT THIS RUNNER CERTIFIES (the scoped bounded statement, axiom-free):

  Let m_1 < m_2 < m_3 be any positive reals (three abstract eigenvalues)
  and let (c_12, c_23) be any geometric-mean NNI off-diagonal coefficients
  in the Hermitian NNI mass matrix M_ij = c_ij * sqrt(m_i * m_j).

  Define the mass-eigenvalue NNI normalization (Branco-Lavoura-Silva,
  "CP Violation", Ch. 6):

      c_ij^phys = c_ij^geom * sqrt(m_i / m_j)        for i < j.

  Then the following four identities hold IDENTICALLY in (m_i, c_ij),
  for arbitrary positive masses and coefficients:

    (T1) Chain rule: sqrt(m_1/m_3) = sqrt(m_1/m_2) * sqrt(m_2/m_3).
    (T2) Schur-complement closure in the geometric basis,
         c_13^geom = c_12 * c_23 (the structural Schur identity).
    (T3) The geom -> phys map is multiplicatively closed under (T1):
         c_13^phys = c_12^phys * c_23^phys.
    (T4) The gap-closure ratio is exactly the (1,3) mass-ratio:
         c_13^phys / c_13^geom = sqrt(m_1/m_3),
         independent of the choice of c_12, c_23.

  Identities (T1)-(T4) are pure algebra. They are the only theorem-grade
  content of this runner and they require no quark-mass or PDG input.

WHAT THIS RUNNER IMPORTS (and therefore does NOT derive):

  The runner also ILLUSTRATES (T4) numerically against an external
  calibration block. The illustration uses:

    - PDG 2024 quark masses (M_UP, M_CHARM, ... ): external import.
    - "Fitted" geometric-mean NNI coefficients C12_*, C23_*: numerical
      fits taken from frontier_ckm_schur_complement.py, themselves
      calibrated against observed CKM mixing angles.
    - PDG 2024 CKM comparators (V_US_PDG, ...): external import.

  The auditor (codex-cli-gpt-5.5, 2026-05-05) correctly flagged that any
  agreement of |V_ub|_pred with PDG in the calibrated block is a
  numerical match under imported inputs, NOT a first-principles closure.
  This patch keeps the calibrated block for diagnostic continuity but
  brackets it as an imports-dependent illustration, separates it from
  the structural identities (T1)-(T4), and removes the earlier prose
  that asserted "all mass ratios are framework-derived."

BUILDS ON (citation, not load-bearing for the source theorems above):
  - scripts/frontier_ckm_schur_complement.py  (provides the geometric
    Schur identity and the fitted O(1) coefficients used in the
    calibrated illustration block).

OPEN FRONTIER (NOT addressed by this patch):
  - A retained derivation of the geometric-mean NNI coefficients
    (c_12, c_23) from framework axioms.
  - A retained derivation of the up/down quark mass hierarchies.
  - Either would be required to upgrade the calibrated illustration
    block from numerical match to a first-principles closure.

PStack experiment: frontier-ckm-mass-basis-nni
Self-contained: numpy + scipy.
"""

from __future__ import annotations

import sys
import numpy as np
from scipy.optimize import brentq

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
    return condition


# =============================================================================
# Constants
#
# IMPORTANT: every numerical constant below is an EXTERNAL IMPORT.
# These are NOT derived by this runner or by retained framework axioms.
# They are used ONLY in the calibrated illustration block (Parts 1, 2, 4,
# 5, 6, 7); the structural identity block (Part 0) ignores them entirely
# and uses arbitrary symbolic masses + coefficients drawn at random.
# =============================================================================

PI = np.pi

# ---- External import: PDG 2024 quark masses ----
# Source: Particle Data Group, "Review of Particle Physics," Prog. Theor.
# Exp. Phys. 2024, 083C01 (and 2024 partial update). MSbar at 2 GeV for
# light quarks; MSbar at m_q for charm/bottom; pole mass for top.
M_UP = 2.16e-3         # GeV  -- PDG 2024 import
M_CHARM = 1.27         # GeV  -- PDG 2024 import
M_TOP = 172.76         # GeV  -- PDG 2024 import
M_DOWN = 4.67e-3       # GeV  -- PDG 2024 import
M_STRANGE = 0.0934     # GeV  -- PDG 2024 import
M_BOTTOM = 4.18        # GeV  -- PDG 2024 import

# (Note: prior revisions of this runner carried a block of unused
# EW/Planck-scale parameters (SIN2_TW, C_F, N_C, ALPHA_S_PL, ALPHA_2_PL,
# M_PL, V_EW) that were referenced only in a prose commentary asserting
# an EWSB-cascade origin for the mass hierarchy. The auditor flagged
# that commentary as unsupported; the unused constants and the prose
# were removed in the 2026-05-16 patch.)

# ---- External import: PDG 2024 CKM comparators ----
LAMBDA_PDG = 0.2243    # PDG 2024 import
A_PDG = 0.790          # PDG 2024 import
RHO_BAR_PDG = 0.141    # PDG 2024 import
ETA_BAR_PDG = 0.357    # PDG 2024 import
V_US_PDG = 0.2243      # PDG 2024 import
V_CB_PDG = 0.0422      # PDG 2024 import
V_UB_PDG = 0.00382     # PDG 2024 import
J_PDG = 3.08e-5        # PDG 2024 import
DELTA_PDG_DEG = 65.5   # degrees -- PDG 2024 import

# PDG 2024 1-sigma uncertainties (used for sigma reporting; not for any
# load-bearing tolerance gate in the source theorems T1-T4)
V_US_ERR = 0.0008
V_CB_ERR = 0.0011
V_UB_ERR = 0.00024
J_ERR = 0.12e-5

# ---- External import: fitted O(1) geometric-mean NNI coefficients ----
# These are the up- and down-sector coefficients quoted in
# scripts/frontier_ckm_schur_complement.py (constants C12_U_FIT etc.,
# lines ~139-142 of that file). That ancestor runner itself fits them
# against observed CKM mixing angles; they are not derived from any
# retained axiom in the present package. They appear here ONLY as
# numerical inputs to the calibrated illustration block.
C12_U_FIT = 1.48       # imported from frontier_ckm_schur_complement.py
C23_U_FIT = 0.65       # imported from frontier_ckm_schur_complement.py
C12_D_FIT = 0.91       # imported from frontier_ckm_schur_complement.py
C23_D_FIT = 0.65       # imported from frontier_ckm_schur_complement.py


# =============================================================================
# NNI matrix infrastructure
# =============================================================================

def build_nni_complex(m1, m2, m3, c12, c23, c13, delta):
    """Build Hermitian NNI mass matrix with CP phase in the 1-3 element.

    M_ij = c_ij * sqrt(m_i * m_j) for off-diagonal elements.
    The 1-3 element carries the CP phase exp(i*delta).
    """
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


def diag_hermitian(M):
    """Diagonalize Hermitian matrix, return sorted eigenvalues and eigenvectors."""
    eigvals, U = np.linalg.eigh(M)
    idx = np.argsort(eigvals)
    return eigvals[idx], U[:, idx]


def compute_ckm(M_u, M_d):
    """CKM matrix from two NNI mass matrices (via Hermitian squares)."""
    H_u = M_u @ M_u.conj().T
    H_d = M_d @ M_d.conj().T
    _, U_u = diag_hermitian(H_u)
    _, U_d = diag_hermitian(H_d)
    return U_u.conj().T @ U_d


def extract_jarlskog(V):
    """Extract Jarlskog invariant from CKM matrix."""
    return abs(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))


def extract_wolfenstein(V):
    """Extract Wolfenstein parameters from CKM matrix."""
    lam = abs(V[0, 1])
    A = abs(V[1, 2]) / lam**2
    Vub = V[0, 2]
    vub_mag = abs(Vub)
    delta = np.angle(-V[0, 0] * V[0, 2].conj() * V[2, 0].conj() * V[2, 2])
    rho_bar = (vub_mag / (A * lam**3)) * np.cos(delta)
    eta_bar = (vub_mag / (A * lam**3)) * np.sin(delta)
    return lam, A, rho_bar, eta_bar


# =============================================================================
# PART 0: SOURCE THEOREMS T1-T4 (structural identities, axiom-free)
#
# Everything in this block is pure algebra over arbitrary positive masses
# and arbitrary geometric-mean coefficients. NO PDG inputs are used.
# These identities are the only theorem-grade content of this runner.
# =============================================================================

def part0_source_theorems(rng_seed: int = 20260516, n_random: int = 200):
    """
    Verify the four structural identities (T1)-(T4) at machine precision
    over n_random random triples (m_1, m_2, m_3) with 0 < m_1 < m_2 < m_3
    and random positive geometric-mean coefficients (c_12, c_23).

    These checks do NOT use any PDG quark mass, any PDG CKM value, or
    any fitted NNI coefficient. They certify pure algebraic identities.
    """
    print("\n" + "=" * 72)
    print("PART 0: SOURCE THEOREMS T1-T4  (structural, axiom-free)")
    print("=" * 72)
    print("  No PDG inputs are read in this block.")
    print(f"  Sampling {n_random} random ordered mass triples and coefficient pairs.")
    print(f"  rng_seed = {rng_seed}")

    rng = np.random.default_rng(rng_seed)

    worst_T1 = 0.0
    worst_T2 = 0.0
    worst_T3 = 0.0
    worst_T4 = 0.0

    for _ in range(n_random):
        # Draw 3 positive masses across many decades and sort ascending
        masses = np.sort(10.0 ** rng.uniform(-4.0, 3.0, size=3))
        m1, m2, m3 = masses[0], masses[1], masses[2]

        # Draw arbitrary positive O(1) coefficients
        c12 = rng.uniform(0.1, 3.0)
        c23 = rng.uniform(0.1, 3.0)

        # (T1) chain rule for sqrt(m_i/m_j)
        r12 = np.sqrt(m1 / m2)
        r23 = np.sqrt(m2 / m3)
        r13 = np.sqrt(m1 / m3)
        err_T1 = abs(r13 - r12 * r23) / r13
        worst_T1 = max(worst_T1, err_T1)

        # (T2) Schur-complement closure in the geometric basis
        # For our purposes "Schur" means: c_13^geom is the structural
        # combination c_12 * c_23 that the rank-1 Schur reduction of
        # a Hermitian NNI mass matrix generates in the (1,3) block.
        c13_geom = c12 * c23
        # Trivially "verified" by construction; the nontrivial check is
        # that the geometric-mean off-diagonal magnitude inherits the
        # product structure under sqrt(m_i*m_j) normalization.
        M13_geom = c13_geom * np.sqrt(m1 * m3)
        M12_geom = c12 * np.sqrt(m1 * m2)
        M23_geom = c23 * np.sqrt(m2 * m3)
        # Structural identity: M_13^geom / (M_12^geom * M_23^geom) =
        # sqrt(m_1*m_3) / (sqrt(m_1*m_2) * sqrt(m_2*m_3)) = 1/m_2.
        expected_ratio = 1.0 / m2
        actual_ratio = M13_geom / (M12_geom * M23_geom)
        err_T2 = abs(actual_ratio - expected_ratio) / abs(expected_ratio)
        worst_T2 = max(worst_T2, err_T2)

        # (T3) geom -> phys map closed under the chain rule:
        # c_13^phys = c_13^geom * sqrt(m_1/m_3) = c_12*c_23*sqrt(m_1/m_3)
        # c_12^phys * c_23^phys = c_12*sqrt(m_1/m_2) * c_23*sqrt(m_2/m_3)
        #                       = c_12 * c_23 * sqrt(m_1/m_3)  (by T1)
        c12_phys = c12 * r12
        c23_phys = c23 * r23
        c13_phys = c13_geom * r13
        prod = c12_phys * c23_phys
        err_T3 = abs(c13_phys - prod) / abs(c13_phys)
        worst_T3 = max(worst_T3, err_T3)

        # (T4) gap-closure ratio is exactly sqrt(m_1/m_3)
        gap = c13_phys / c13_geom
        err_T4 = abs(gap - r13) / r13
        worst_T4 = max(worst_T4, err_T4)

    print(f"\n  Worst relative deviation across {n_random} random triples:")
    print(f"    T1 (chain rule):              {worst_T1:.3e}")
    print(f"    T2 (geom Schur normalization): {worst_T2:.3e}")
    print(f"    T3 (geom -> phys closure):     {worst_T3:.3e}")
    print(f"    T4 (gap = sqrt(m_1/m_3)):      {worst_T4:.3e}")

    check("T1: chain rule sqrt(m1/m3) = sqrt(m1/m2)*sqrt(m2/m3) holds identically",
          worst_T1 < 1e-12,
          f"worst relative deviation = {worst_T1:.3e}")
    check("T2: geom Schur identity M_13^geom * m_2 = M_12^geom * M_23^geom",
          worst_T2 < 1e-12,
          f"worst relative deviation = {worst_T2:.3e}")
    check("T3: c_13^phys = c_12^phys * c_23^phys for arbitrary masses/coefficients",
          worst_T3 < 1e-12,
          f"worst relative deviation = {worst_T3:.3e}")
    check("T4: gap-closure ratio c_13^phys/c_13^geom = sqrt(m_1/m_3) identically",
          worst_T4 < 1e-12,
          f"worst relative deviation = {worst_T4:.3e}")

    return {
        'worst_T1': worst_T1, 'worst_T2': worst_T2,
        'worst_T3': worst_T3, 'worst_T4': worst_T4,
    }


# =============================================================================
# PART 1: Calibrated illustration -- mass-ratio suppressions from PDG masses
#
# IMPORTS PDG quark masses. The numbers in this block are not derived;
# they are the application of identity (T1) to imported values for the
# purpose of computing the imported-vs-imported illustration in Parts
# 4-7. Nothing here lifts the bounded status of the note.
# =============================================================================

def part1_mass_ratios():
    """
    Compute the mass-ratio factors that (T4) identifies as the gap-closure
    ratio between geometric-mean and mass-eigenvalue NNI bases.

    All numerical values are functions of the PDG 2024 quark masses
    imported at the top of this file. No derivation is claimed.
    """
    print("\n" + "=" * 72)
    print("PART 1: Mass-Ratio Suppression Factors (PDG-imported illustration)")
    print("=" * 72)
    print("  This block evaluates identity (T1) at imported PDG 2024 masses.")
    print("  All input numbers are external imports; see header.")

    # --- Up sector mass ratios ---
    r_uc = np.sqrt(M_UP / M_CHARM)
    r_ct = np.sqrt(M_CHARM / M_TOP)
    r_ut = np.sqrt(M_UP / M_TOP)

    print(f"\n  Up-sector mass ratios (from imported PDG masses):")
    print(f"    sqrt(m_u/m_c) = sqrt({M_UP:.4f}/{M_CHARM:.2f}) = {r_uc:.5f}")
    print(f"    sqrt(m_c/m_t) = sqrt({M_CHARM:.2f}/{M_TOP:.2f}) = {r_ct:.5f}")
    print(f"    sqrt(m_u/m_t) = sqrt({M_UP:.4f}/{M_TOP:.2f}) = {r_ut:.6f}")

    # --- Down sector mass ratios ---
    r_ds = np.sqrt(M_DOWN / M_STRANGE)
    r_sb = np.sqrt(M_STRANGE / M_BOTTOM)
    r_db = np.sqrt(M_DOWN / M_BOTTOM)

    print(f"\n  Down-sector mass ratios (from imported PDG masses):")
    print(f"    sqrt(m_d/m_s) = sqrt({M_DOWN:.4f}/{M_STRANGE:.4f}) = {r_ds:.5f}")
    print(f"    sqrt(m_s/m_b) = sqrt({M_STRANGE:.4f}/{M_BOTTOM:.2f}) = {r_sb:.5f}")
    print(f"    sqrt(m_d/m_b) = sqrt({M_DOWN:.4f}/{M_BOTTOM:.2f}) = {r_db:.6f}")

    # --- (T1) chain-rule sanity check on the imported numbers ---
    print(f"\n  (T1) sanity check at imported values:")
    print(f"    Up:   sqrt(m_u/m_c) * sqrt(m_c/m_t) = {r_uc * r_ct:.6f}")
    print(f"          sqrt(m_u/m_t)                  = {r_ut:.6f}")
    check("(T1) holds at PDG imported up-sector masses",
          abs(r_ut - r_uc * r_ct) / r_ut < 1e-10,
          f"difference = {abs(r_ut - r_uc * r_ct):.2e}")

    print(f"    Down: sqrt(m_d/m_s) * sqrt(m_s/m_b) = {r_ds * r_sb:.6f}")
    print(f"          sqrt(m_d/m_b)                  = {r_db:.6f}")
    check("(T1) holds at PDG imported down-sector masses",
          abs(r_db - r_ds * r_sb) / r_db < 1e-10,
          f"difference = {abs(r_db - r_ds * r_sb):.2e}")

    print(f"\n  NOTE: this block does NOT claim a framework derivation of")
    print(f"  the quark mass hierarchy. It is an imports-dependent")
    print(f"  illustration of the structural identities certified in Part 0.")

    return {
        'r_uc': r_uc, 'r_ct': r_ct, 'r_ut': r_ut,
        'r_ds': r_ds, 'r_sb': r_sb, 'r_db': r_db,
    }


# =============================================================================
# PART 2: Mass-eigenvalue NNI coefficients
# =============================================================================

def part2_mass_basis_coefficients(mass_ratios):
    """
    Evaluate the mass-eigenvalue normalization map on the imported O(1)
    geometric-mean coefficients (C12_*_FIT, C23_*_FIT) and imported
    PDG quark masses. The factorization checks at the end re-verify
    identity (T3) at the imported values.

    Everything here is an imports-dependent illustration of Part 0.
    """
    print("\n" + "=" * 72)
    print("PART 2: Mass-Eigenvalue NNI Coefficients (calibrated illustration)")
    print("=" * 72)
    print("  Inputs: imported C12_*_FIT, C23_*_FIT (fitted O(1) values from")
    print("    scripts/frontier_ckm_schur_complement.py) and imported PDG masses.")

    r_uc = mass_ratios['r_uc']
    r_ct = mass_ratios['r_ct']
    r_ut = mass_ratios['r_ut']
    r_ds = mass_ratios['r_ds']
    r_sb = mass_ratios['r_sb']
    r_db = mass_ratios['r_db']

    # --- Up sector ---
    c12_u_phys = C12_U_FIT * r_uc
    c23_u_phys = C23_U_FIT * r_ct
    c13_u_geom = C12_U_FIT * C23_U_FIT  # Schur complement
    c13_u_phys = c13_u_geom * r_ut

    print(f"\n  Up sector (geometric-mean -> mass-eigenvalue):")
    print(f"    c_12^geom = {C12_U_FIT:.3f}")
    print(f"    c_12^phys = {C12_U_FIT:.3f} * sqrt(m_u/m_c) = {C12_U_FIT:.3f} * {r_uc:.5f} = {c12_u_phys:.5f}")
    print(f"    c_23^geom = {C23_U_FIT:.3f}")
    print(f"    c_23^phys = {C23_U_FIT:.3f} * sqrt(m_c/m_t) = {C23_U_FIT:.3f} * {r_ct:.5f} = {c23_u_phys:.5f}")
    print(f"    c_13^geom = c_12 * c_23 = {c13_u_geom:.4f}  [Schur complement]")
    print(f"    c_13^phys = {c13_u_geom:.4f} * sqrt(m_u/m_t) = {c13_u_geom:.4f} * {r_ut:.6f} = {c13_u_phys:.6f}")

    # --- Down sector ---
    c12_d_phys = C12_D_FIT * r_ds
    c23_d_phys = C23_D_FIT * r_sb
    c13_d_geom = C12_D_FIT * C23_D_FIT  # Schur complement
    c13_d_phys = c13_d_geom * r_db

    print(f"\n  Down sector (geometric-mean -> mass-eigenvalue):")
    print(f"    c_12^geom = {C12_D_FIT:.3f}")
    print(f"    c_12^phys = {C12_D_FIT:.3f} * sqrt(m_d/m_s) = {C12_D_FIT:.3f} * {r_ds:.5f} = {c12_d_phys:.5f}")
    print(f"    c_23^geom = {C23_D_FIT:.3f}")
    print(f"    c_23^phys = {C23_D_FIT:.3f} * sqrt(m_s/m_b) = {C23_D_FIT:.3f} * {r_sb:.5f} = {c23_d_phys:.5f}")
    print(f"    c_13^geom = c_12 * c_23 = {c13_d_geom:.4f}  [Schur complement]")
    print(f"    c_13^phys = {c13_d_geom:.4f} * sqrt(m_d/m_b) = {c13_d_geom:.4f} * {r_db:.6f} = {c13_d_phys:.6f}")

    # --- Verify that mass-basis c_13 factorizes correctly ---
    c13_u_product = c12_u_phys * c23_u_phys
    c13_d_product = c12_d_phys * c23_d_phys

    print(f"\n  Factorization check (c_13^phys = c_12^phys * c_23^phys):")
    print(f"    Up:   c_12^phys * c_23^phys = {c12_u_phys:.5f} * {c23_u_phys:.5f} = {c13_u_product:.6f}")
    print(f"          c_13^phys             = {c13_u_phys:.6f}")
    check("(T3) holds at imported up-sector inputs: c_13^phys = c_12^phys * c_23^phys",
          abs(c13_u_phys - c13_u_product) / c13_u_phys < 1e-10,
          f"ratio = {c13_u_product/c13_u_phys:.10f}")

    print(f"    Down: c_12^phys * c_23^phys = {c12_d_phys:.5f} * {c23_d_phys:.5f} = {c13_d_product:.6f}")
    print(f"          c_13^phys             = {c13_d_phys:.6f}")
    check("(T3) holds at imported down-sector inputs: c_13^phys = c_12^phys * c_23^phys",
          abs(c13_d_phys - c13_d_product) / c13_d_phys < 1e-10,
          f"ratio = {c13_d_product/c13_d_phys:.10f}")

    return {
        'c12_u_phys': c12_u_phys, 'c23_u_phys': c23_u_phys,
        'c13_u_geom': c13_u_geom, 'c13_u_phys': c13_u_phys,
        'c12_d_phys': c12_d_phys, 'c23_d_phys': c23_d_phys,
        'c13_d_geom': c13_d_geom, 'c13_d_phys': c13_d_phys,
    }


# =============================================================================
# PART 3: Full CKM from mass-basis NNI
# =============================================================================

def part3_full_ckm(mass_ratios, coeffs):
    """
    Build 3x3 CKM matrices using the mass-basis NNI coefficients and
    compare to PDG values.

    The key insight: instead of using the geometric-mean NNI coefficients
    directly in the mass matrix, we use c_13^phys which incorporates the
    mass-ratio suppression from the conversion to mass eigenvalue basis.

    The geometric-mean NNI matrix has M_ij = c_ij^geom * sqrt(m_i * m_j).
    The mass-eigenvalue basis rescales: c_ij^phys = c_ij^geom * sqrt(m_i/m_j).
    Substituting back: M_ij^phys = c_ij^phys * m_j (for i < j).

    But the CKM depends on the MISMATCH between up and down sector rotations.
    The physical mixing angles are:
      sin(theta_12) ~ c_12^phys ~ sqrt(m_d/m_s) or sqrt(m_u/m_c)
      sin(theta_23) ~ c_23^phys ~ sqrt(m_s/m_b) or sqrt(m_c/m_t)
      sin(theta_13) ~ c_13^phys ~ sqrt(m_d/m_b) or sqrt(m_u/m_t)

    For the CKM (misalignment of up/down), the dominant contribution
    comes from whichever sector has the larger mixing angle.
    """
    print("\n" + "=" * 72)
    print("PART 3: Full CKM from Mass-Basis NNI Coefficients")
    print("=" * 72)

    # The CKM mixing angles depend on the DIFFERENCE between up and down
    # sector rotations. In the mass-eigenvalue NNI basis, the physical
    # mixing angles are directly the c_ij^phys values.

    # --- Analytic estimates from mass-basis NNI ---

    # |V_us| comes primarily from the down-sector 1-2 rotation
    # (since sqrt(m_d/m_s) > sqrt(m_u/m_c)):
    vus_down = coeffs['c12_d_phys']
    vus_up = coeffs['c12_u_phys']
    vus_analytic = abs(vus_down - vus_up)  # misalignment

    print(f"\n  Analytic estimates (mass-basis NNI):")
    print(f"\n  |V_us|:")
    print(f"    Down sector: c_12^phys = {vus_down:.5f}")
    print(f"    Up sector:   c_12^phys = {vus_up:.5f}")
    print(f"    |V_us| ~ |c_12^d - c_12^u| = {vus_analytic:.5f}")
    print(f"    PDG:  {V_US_PDG}")

    # |V_cb| from the 2-3 sector misalignment:
    vcb_down = coeffs['c23_d_phys']
    vcb_up = coeffs['c23_u_phys']
    vcb_analytic = abs(vcb_down - vcb_up)

    print(f"\n  |V_cb|:")
    print(f"    Down sector: c_23^phys = {vcb_down:.5f}")
    print(f"    Up sector:   c_23^phys = {vcb_up:.5f}")
    print(f"    |V_cb| ~ |c_23^d - c_23^u| = {vcb_analytic:.5f}")
    print(f"    PDG:  {V_CB_PDG}")

    # |V_ub| from the 1-3 sector misalignment (Schur complement + mass basis):
    vub_down = coeffs['c13_d_phys']
    vub_up = coeffs['c13_u_phys']
    vub_analytic = abs(vub_down - vub_up)

    print(f"\n  |V_ub|:")
    print(f"    Down sector: c_13^phys = {vub_down:.6f}")
    print(f"    Up sector:   c_13^phys = {vub_up:.6f}")
    print(f"    |V_ub| ~ |c_13^d - c_13^u| = {vub_analytic:.6f}")
    print(f"    PDG:  {V_UB_PDG}")

    # --- Comparison to naive geometric-mean Schur complement ---
    vub_geom = abs(coeffs['c13_d_geom'] - coeffs['c13_u_geom'])
    vub_geom_naive = coeffs['c13_u_geom']  # single-sector estimate

    print(f"\n  Gap closure:")
    print(f"    |V_ub| (geometric-mean NNI, naive) ~ c_13^geom ~ {vub_geom_naive:.4f}")
    print(f"    |V_ub| (mass-basis NNI)            ~ {vub_analytic:.6f}")
    print(f"    PDG                                 = {V_UB_PDG:.5f}")
    suppression = vub_geom_naive / vub_analytic if vub_analytic > 0 else float('inf')
    print(f"    Suppression factor: {suppression:.1f}x")

    return {
        'vus_analytic': vus_analytic, 'vcb_analytic': vcb_analytic,
        'vub_analytic': vub_analytic,
    }


# =============================================================================
# PART 4: Numerical CKM from mass-basis NNI mass matrices
# =============================================================================

def part4_numerical_ckm(mass_ratios, coeffs):
    """
    Build the full 3x3 NNI mass matrices with mass-basis-corrected c_13
    and compute the CKM numerically.
    """
    print("\n" + "=" * 72)
    print("PART 4: Numerical CKM with Mass-Basis c_13")
    print("=" * 72)

    # CP phase from Z_3 Berry phase
    delta_berry = 2 * PI / 3  # 120 degrees

    # Use the mass-basis c_13 in the geometric-mean NNI matrix.
    # The mass matrix M_ij = c_ij^geom * sqrt(m_i * m_j) uses geom coefficients.
    # The mass-basis c_13^phys = c_13^geom * sqrt(m_i/m_j) gives the physical
    # c_13 in the mass-eigenvalue NNI. To use it in the geometric-mean matrix
    # we need: c_13^{for matrix} = c_13^phys / sqrt(m_i/m_j) = c_13^phys * sqrt(m_j/m_i)
    #
    # But actually the point is simpler: we use c_13^phys AS the coefficient
    # that determines the physical CKM. The geometric-mean NNI matrix already
    # has the Schur complement generating c_13^geom = c_12*c_23, and the
    # mass-basis normalization tells us the PHYSICAL mixing angle involves
    # c_13^phys = c_13^geom * sqrt(m_1/m_3).
    #
    # For the numerical computation, we build the NNI matrix with the
    # mass-basis-corrected c_13 inserted directly.

    c13_u_phys = coeffs['c13_u_phys']
    c13_d_phys = coeffs['c13_d_phys']

    print(f"\n  Building NNI matrices:")
    print(f"    Up sector:   c_12={C12_U_FIT:.3f}, c_23={C23_U_FIT:.3f}, c_13={c13_u_phys:.6f}")
    print(f"    Down sector: c_12={C12_D_FIT:.3f}, c_23={C23_D_FIT:.3f}, c_13={c13_d_phys:.6f}")
    print(f"    CP phase (Berry): delta = {np.degrees(delta_berry):.1f} deg")

    M_u = build_nni_complex(M_UP, M_CHARM, M_TOP,
                            C12_U_FIT, C23_U_FIT, c13_u_phys, delta_berry)
    M_d = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM,
                            C12_D_FIT, C23_D_FIT, c13_d_phys, delta_berry)

    V_ckm = compute_ckm(M_u, M_d)

    vus = abs(V_ckm[0, 1])
    vcb = abs(V_ckm[1, 2])
    vub = abs(V_ckm[0, 2])
    J = extract_jarlskog(V_ckm)
    lam, A, rho_bar, eta_bar = extract_wolfenstein(V_ckm)

    print(f"\n  CKM matrix (magnitudes):")
    for i in range(3):
        row = "    |"
        for j in range(3):
            row += f" {abs(V_ckm[i, j]):.6f} "
        row += "|"
        print(row)

    print(f"\n  Key elements:")
    print(f"    |V_us| = {vus:.5f}  (PDG: {V_US_PDG})  ratio: {vus/V_US_PDG:.3f}")
    print(f"    |V_cb| = {vcb:.5f}  (PDG: {V_CB_PDG})  ratio: {vcb/V_CB_PDG:.3f}")
    print(f"    |V_ub| = {vub:.6f}  (PDG: {V_UB_PDG})  ratio: {vub/V_UB_PDG:.3f}")
    print(f"    J      = {J:.3e}  (PDG: {J_PDG:.3e})  ratio: {J/J_PDG:.3f}")

    print(f"\n  Wolfenstein parameters:")
    print(f"    lambda  = {lam:.5f}  (PDG: {LAMBDA_PDG})")
    print(f"    A       = {A:.4f}  (PDG: {A_PDG})")
    print(f"    rho_bar = {rho_bar:.4f}  (PDG: {RHO_BAR_PDG})")
    print(f"    eta_bar = {eta_bar:.4f}  (PDG: {ETA_BAR_PDG})")

    # --- Checks ---
    check("|V_us| within 50% of PDG",
          abs(vus / V_US_PDG - 1.0) < 0.50,
          f"|V_us| = {vus:.5f}, ratio = {vus/V_US_PDG:.3f}",
          kind="BOUNDED")

    check("|V_cb| within 50% of PDG",
          abs(vcb / V_CB_PDG - 1.0) < 0.50,
          f"|V_cb| = {vcb:.5f}, ratio = {vcb/V_CB_PDG:.3f}",
          kind="BOUNDED")

    check("|V_ub| within factor 3 of PDG (mass-basis corrected)",
          0.33 < vub / V_UB_PDG < 3.0,
          f"|V_ub| = {vub:.6f}, ratio = {vub/V_UB_PDG:.3f}",
          kind="BOUNDED")

    check("J within order of magnitude of PDG",
          0.1 < J / J_PDG < 10.0,
          f"J = {J:.3e}, ratio = {J/J_PDG:.3f}",
          kind="BOUNDED")

    return {
        'V_ckm': V_ckm,
        'vus': vus, 'vcb': vcb, 'vub': vub, 'J': J,
        'lam': lam, 'A': A, 'rho_bar': rho_bar, 'eta_bar': eta_bar,
    }


# =============================================================================
# PART 5: Scan over c_13 to show gap closure
# =============================================================================

def part5_gap_closure_scan(mass_ratios, coeffs):
    """
    Show exactly how the mass-ratio suppression closes the factor-6 gap.

    Scan c_13 from the geometric-mean value down to the mass-basis value,
    plotting the trajectory in |V_ub| space.
    """
    print("\n" + "=" * 72)
    print("PART 5: Gap Closure -- Geometric-Mean to Mass-Basis")
    print("=" * 72)

    delta_berry = 2 * PI / 3
    c13_geom_u = coeffs['c13_u_geom']
    c13_geom_d = coeffs['c13_d_geom']
    c13_phys_u = coeffs['c13_u_phys']
    c13_phys_d = coeffs['c13_d_phys']

    # The suppression factor
    supp_u = mass_ratios['r_ut']
    supp_d = mass_ratios['r_db']

    print(f"\n  Suppression factors:")
    print(f"    Up sector:   sqrt(m_u/m_t) = {supp_u:.6f}")
    print(f"    Down sector: sqrt(m_d/m_b) = {supp_d:.6f}")
    print(f"    Geometric-mean overshoot factor (up):   {1.0/supp_u:.1f}x")
    print(f"    Geometric-mean overshoot factor (down): {1.0/supp_d:.1f}x")

    # Scan: interpolate suppression from 1.0 (geometric) to sqrt(m_1/m_3) (mass-basis)
    print(f"\n  Scan: c_13 suppression from 1.0 to sqrt(m_1/m_3)")
    print(f"  {'suppression':>12s}  {'c13_u':>10s}  {'c13_d':>10s}  {'|V_ub|':>10s}  {'V_ub/PDG':>8s}")
    print(f"  {'-'*12}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}")

    suppression_values = [1.0, 0.5, 0.1, 0.05, 0.01, supp_u, 0.001]
    suppression_values = sorted(set(suppression_values), reverse=True)

    for s in suppression_values:
        c13_u_s = c13_geom_u * s
        c13_d_s = c13_geom_d * s
        M_u = build_nni_complex(M_UP, M_CHARM, M_TOP,
                                C12_U_FIT, C23_U_FIT, c13_u_s, delta_berry)
        M_d = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM,
                                C12_D_FIT, C23_D_FIT, c13_d_s, delta_berry)
        V = compute_ckm(M_u, M_d)
        vub = abs(V[0, 2])
        marker = " <-- mass basis" if abs(s - supp_u) / supp_u < 0.1 else ""
        marker = " <-- geometric" if s == 1.0 else marker
        print(f"  {s:>12.6f}  {c13_u_s:>10.6f}  {c13_d_s:>10.6f}  {vub:>10.6f}  {vub/V_UB_PDG:>8.3f}{marker}")

    # --- Build CKM at the exact mass-basis suppression ---
    M_u_mb = build_nni_complex(M_UP, M_CHARM, M_TOP,
                               C12_U_FIT, C23_U_FIT, c13_phys_u, delta_berry)
    M_d_mb = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM,
                               C12_D_FIT, C23_D_FIT, c13_phys_d, delta_berry)
    V_mb = compute_ckm(M_u_mb, M_d_mb)
    vub_mb = abs(V_mb[0, 2])

    # --- Build CKM at geometric-mean (no suppression) ---
    M_u_gm = build_nni_complex(M_UP, M_CHARM, M_TOP,
                               C12_U_FIT, C23_U_FIT, c13_geom_u, delta_berry)
    M_d_gm = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM,
                               C12_D_FIT, C23_D_FIT, c13_geom_d, delta_berry)
    V_gm = compute_ckm(M_u_gm, M_d_gm)
    vub_gm = abs(V_gm[0, 2])

    print(f"\n  Summary:")
    print(f"    |V_ub| (geometric-mean NNI):  {vub_gm:.5f}  (ratio to PDG: {vub_gm/V_UB_PDG:.2f})")
    print(f"    |V_ub| (mass-basis NNI):      {vub_mb:.6f}  (ratio to PDG: {vub_mb/V_UB_PDG:.2f})")
    print(f"    |V_ub| (PDG):                 {V_UB_PDG:.5f}")
    print(f"    Gap closure: {vub_gm/V_UB_PDG:.1f}x -> {vub_mb/V_UB_PDG:.2f}x")

    check("Mass-basis NNI closes the geometric-mean gap in V_ub",
          vub_mb / V_UB_PDG < vub_gm / V_UB_PDG,
          f"geometric: {vub_gm/V_UB_PDG:.1f}x, mass-basis: {vub_mb/V_UB_PDG:.2f}x",
          kind="EXACT")

    # --- Find optimal suppression that matches PDG V_ub ---
    print(f"\n  Finding optimal suppression to match PDG |V_ub|...")
    def vub_residual(log_s):
        s = 10**log_s
        M_u_t = build_nni_complex(M_UP, M_CHARM, M_TOP,
                                  C12_U_FIT, C23_U_FIT, c13_geom_u * s, delta_berry)
        M_d_t = build_nni_complex(M_DOWN, M_STRANGE, M_BOTTOM,
                                  C12_D_FIT, C23_D_FIT, c13_geom_d * s, delta_berry)
        V_t = compute_ckm(M_u_t, M_d_t)
        return abs(V_t[0, 2]) - V_UB_PDG

    try:
        log_s_opt = brentq(vub_residual, -5, 0)
        s_opt = 10**log_s_opt
        print(f"    Optimal suppression: {s_opt:.6f}")
        print(f"    Mass-basis prediction: sqrt(m_u/m_t) = {supp_u:.6f}")
        print(f"    Mass-basis prediction: sqrt(m_d/m_b) = {supp_d:.6f}")
        print(f"    Ratio (optimal / sqrt(m_u/m_t)): {s_opt/supp_u:.2f}")
        print(f"    Ratio (optimal / sqrt(m_d/m_b)): {s_opt/supp_d:.2f}")

        check("Optimal suppression within factor 3 of sqrt(m_d/m_b)",
              0.33 < s_opt / supp_d < 3.0,
              f"optimal={s_opt:.5f}, sqrt(m_d/m_b)={supp_d:.5f}, ratio={s_opt/supp_d:.2f}",
              kind="BOUNDED")
    except ValueError:
        print("    Brentq failed -- V_ub does not cross PDG in range")

    return {
        'vub_geom': vub_gm,
        'vub_mass_basis': vub_mb,
    }


# =============================================================================
# PART 6: Wolfenstein identification
# =============================================================================

def part6_wolfenstein(mass_ratios, coeffs, ckm_results):
    """
    Numerically check that the mass-basis NNI evaluated at the imported
    down-sector inputs reproduces a Wolfenstein-like hierarchy
    V_us ~ lambda, V_cb ~ A*lambda^2, V_ub ~ A*lambda^3.

    This is NOT a derivation of the Wolfenstein parametrization from
    framework axioms. It is a numerical correspondence between the
    imported PDG mass ratios and the conventional Wolfenstein powers,
    conditional on the imported fitted O(1) coefficients C12_D_FIT,
    C23_D_FIT. The structural content reduces to identity (T3) at the
    down-sector imported values.
    """
    print("\n" + "=" * 72)
    print("PART 6: Wolfenstein Correspondence (imports-dependent)")
    print("=" * 72)

    c12_d_phys = coeffs['c12_d_phys']
    c23_d_phys = coeffs['c23_d_phys']
    c13_d_phys = coeffs['c13_d_phys']

    # The Wolfenstein parameters in terms of mass-basis NNI:
    # lambda ~ c_12^phys ~ c_12^geom * sqrt(m_d/m_s)
    # A ~ c_23^phys / lambda^2 ~ c_23^geom * sqrt(m_s/m_b) / (c_12^geom * sqrt(m_d/m_s))^2
    # V_ub ~ c_13^phys ~ c_12^geom * c_23^geom * sqrt(m_d/m_b)
    #       = lambda * (A * lambda^2) factored through the mass hierarchy

    lam_est = c12_d_phys
    A_est = c23_d_phys / lam_est**2 if lam_est > 0 else 0
    vub_wolf = A_est * lam_est**3

    print(f"\n  Wolfenstein from mass-basis NNI:")
    print(f"    lambda  ~ c_12^phys (down) = {lam_est:.5f}  (PDG: {LAMBDA_PDG})")
    print(f"    A       ~ c_23^phys / lambda^2 = {A_est:.4f}  (PDG: {A_PDG})")
    print(f"    A*lambda^3 = {vub_wolf:.6f}  (PDG V_ub: {V_UB_PDG})")

    # The Schur complement chain:
    # c_13^phys = c_12^geom * c_23^geom * sqrt(m_1/m_3)
    #           = (c_12^phys / sqrt(m_d/m_s)) * (c_23^phys / sqrt(m_s/m_b)) * sqrt(m_d/m_b)
    #           = c_12^phys * c_23^phys * [sqrt(m_d/m_b) / (sqrt(m_d/m_s) * sqrt(m_s/m_b))]
    #           = c_12^phys * c_23^phys  [chain rule!]
    # So c_13^phys = c_12^phys * c_23^phys = lambda * A*lambda^2 = A*lambda^3

    print(f"\n  Schur chain in mass basis (identity T3 at down-sector imports):")
    print(f"    c_13^phys = c_12^phys * c_23^phys  [chain rule for sqrt(m_i/m_j)]")
    print(f"    = {c12_d_phys:.5f} * {c23_d_phys:.5f} = {c12_d_phys * c23_d_phys:.6f}")
    print(f"    = lambda_est * (A_est * lambda_est^2) = A_est * lambda_est^3")
    print(f"    Numerical correspondence to a Wolfenstein-like hierarchy,")
    print(f"    conditional on the imported fitted coefficients and PDG masses.")

    check("Numerical Wolfenstein correspondence at imported inputs: c_13^phys ~ A*lambda^3",
          abs(c13_d_phys - vub_wolf) / V_UB_PDG < 0.5,
          f"c_13^phys = {c13_d_phys:.6f}, A*lambda^3 = {vub_wolf:.6f}",
          kind="BOUNDED")

    # --- The mass-ratio origin of each power of lambda ---
    print(f"\n  Mass-ratio origin of each Wolfenstein power:")
    print(f"    lambda   ~ sqrt(m_d/m_s) = {mass_ratios['r_ds']:.5f} * c_12^geom")
    print(f"    lambda^2 ~ (m_d/m_s)     = {M_DOWN/M_STRANGE:.5f} * (c_12^geom)^2")
    print(f"    lambda^3 ~ (m_d/m_s)^{3/2:.1f} = {(M_DOWN/M_STRANGE)**1.5:.6f} * (c_12^geom)^3")
    print(f"    A*lambda^3 includes extra sqrt(m_s/m_b) from c_23")

    check("lambda_est = sqrt(m_d/m_s) * C12_D_FIT (algebraic check at imports)",
          abs(lam_est / (mass_ratios['r_ds'] * C12_D_FIT) - 1.0) < 0.01,
          f"lambda/(r_ds*c12) = {lam_est/(mass_ratios['r_ds'] * C12_D_FIT):.4f}",
          kind="EXACT")

    return {}


# =============================================================================
# PART 7: Full scorecard
# =============================================================================

def part7_scorecard(ckm_results, gap_results):
    """Final comparison table: all CKM elements and invariants."""
    print("\n" + "=" * 72)
    print("SCORECARD: Mass-Basis NNI vs PDG")
    print("=" * 72)

    params = [
        ("|V_us|", ckm_results['vus'], V_US_PDG, V_US_ERR),
        ("|V_cb|", ckm_results['vcb'], V_CB_PDG, V_CB_ERR),
        ("|V_ub|", ckm_results['vub'], V_UB_PDG, V_UB_ERR),
        ("J", ckm_results['J'], J_PDG, J_ERR),
    ]

    print(f"\n  {'Element':>8s}  {'Mass-NNI':>12s}  {'PDG':>12s}  {'Ratio':>8s}  {'sigma':>6s}  {'Status':>8s}")
    print(f"  {'-'*8}  {'-'*12}  {'-'*12}  {'-'*8}  {'-'*6}  {'-'*8}")

    for name, derived, pdg, err in params:
        ratio = derived / pdg
        sigma = abs(derived - pdg) / err if err > 0 else float('inf')
        if abs(ratio - 1.0) < 0.30:
            status = "GOOD"
        elif abs(ratio - 1.0) < 0.50:
            status = "OK"
        else:
            status = "BOUNDED"
        print(f"  {name:>8s}  {derived:>12.5e}  {pdg:>12.5e}  {ratio:>8.3f}  {sigma:>6.1f}  {status:>8s}")

    # Wolfenstein
    print(f"\n  Wolfenstein parameters:")
    wolf = [
        ("lambda", ckm_results['lam'], LAMBDA_PDG),
        ("A", ckm_results['A'], A_PDG),
        ("rho_bar", ckm_results['rho_bar'], RHO_BAR_PDG),
        ("eta_bar", ckm_results['eta_bar'], ETA_BAR_PDG),
    ]
    for name, derived, pdg in wolf:
        ratio = derived / pdg if pdg != 0 else float('inf')
        print(f"    {name:>8s}  = {derived:>8.4f}  (PDG: {pdg})  ratio: {ratio:.3f}")

    # Gap closure summary
    print(f"\n  V_ub Gap Closure Summary:")
    print(f"    Geometric-mean NNI |V_ub|: {gap_results['vub_geom']:.5f} ({gap_results['vub_geom']/V_UB_PDG:.1f}x PDG)")
    print(f"    Mass-basis NNI |V_ub|:     {gap_results['vub_mass_basis']:.6f} ({gap_results['vub_mass_basis']/V_UB_PDG:.2f}x PDG)")
    print(f"    PDG |V_ub|:                {V_UB_PDG:.5f}")

    overshoot_geom = gap_results['vub_geom'] / V_UB_PDG
    overshoot_mass = gap_results['vub_mass_basis'] / V_UB_PDG

    check("Mass-basis NNI reduces V_ub overshoot by > 2x",
          overshoot_geom / overshoot_mass > 2.0 if overshoot_mass > 0 else False,
          f"geometric: {overshoot_geom:.1f}x, mass-basis: {overshoot_mass:.2f}x, improvement: {overshoot_geom/overshoot_mass:.1f}x",
          kind="EXACT")

    return {}


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 72)
    print("CKM Mass-Basis NNI: structural identities + calibrated illustration")
    print("=" * 72)
    print("  Source theorems (T1-T4) are pure algebra and use no imports.")
    print("  Parts 1-7 are an imports-dependent illustration (PDG masses,")
    print("  PDG CKM, fitted O(1) coefficients from the Schur runner).")
    print()

    # ---- Source theorems: axiom-free structural identities ----
    part0_results = part0_source_theorems()

    # ---- Imports-dependent illustration ----
    mass_ratios = part1_mass_ratios()
    coeffs = part2_mass_basis_coefficients(mass_ratios)
    analytic = part3_full_ckm(mass_ratios, coeffs)
    ckm_results = part4_numerical_ckm(mass_ratios, coeffs)
    gap_results = part5_gap_closure_scan(mass_ratios, coeffs)
    part6_wolfenstein(mass_ratios, coeffs, ckm_results)
    part7_scorecard(ckm_results, gap_results)

    # Final summary
    print("\n" + "=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print(f"  Total checks: {PASS_COUNT + FAIL_COUNT}")
    print(f"  Passed: {PASS_COUNT} ({EXACT_PASS} exact, {BOUNDED_PASS} bounded)")
    print(f"  Failed: {FAIL_COUNT} ({EXACT_FAIL} exact, {BOUNDED_FAIL} bounded)")
    print()
    print(f"  Source theorems T1-T4 worst relative deviations:")
    print(f"    T1 = {part0_results['worst_T1']:.3e}")
    print(f"    T2 = {part0_results['worst_T2']:.3e}")
    print(f"    T3 = {part0_results['worst_T3']:.3e}")
    print(f"    T4 = {part0_results['worst_T4']:.3e}")
    print()
    print(f"  Scope reminder: T1-T4 are axiom-free algebraic identities.")
    print(f"  Parts 1-7 numerical agreement with PDG is an imports-conditional")
    print(f"  illustration (audited 2026-05-05 as audited_numerical_match,")
    print(f"  class G; see docs/work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md).")

    if FAIL_COUNT > 0:
        print(f"\n  WARNING: {FAIL_COUNT} check(s) failed")
        sys.exit(1)
    else:
        print(f"\n  All checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
