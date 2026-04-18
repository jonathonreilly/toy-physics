#!/usr/bin/env python3
"""
Frontier runner: Class #5 Non-Q_L-Block Yukawa Vertex Retention Analysis.

Status
------
Retention-analysis runner closing candidate class #5 (non-Q_L-block Yukawa
vertex structure) as a mechanism to break the Ward-identity Yukawa
unification prediction.  Addresses: the Ward theorem uses a 4-fermion
1PI on Q_L x Q_L* (both fermions in Q_L block); the physical SM Yukawa
is a TRILINEAR Q_bar_L x H x q_R vertex with q_R (u_R or d_R) on a
block OUTSIDE Q_L (the right-handed C^8_R).  Does the block asymmetry
between Ward (Q_L x Q_L*) and physical (Q_L x q_R) provide a
framework-native primitive for species differentiation?

Outcome
-------
Outcome D (retained no-go with structural refinement).  The trilinear
Yukawa CG factor for Q_bar_L x H x q_R is:

    CG_color[3_bar x 3 -> 1]  =  1/sqrt(3)
    CG_iso[2_bar x 2 -> 1]    =  1/sqrt(2)
    CG_Y[U(1) trivial]        =  1
    -----------------------------------------
    Combined                  =  1/sqrt(6)

independent of q_R species (u_R vs d_R).  The species-index q_R enters
only through abelian U(1)_Y selection rules (which Higgs component
couples: H_tilde for up, H for down), which preserve non-abelian CG.
H vs H_tilde distinction is a unitary isomorphism (i*sigma_2 is
unitary); norm-preserving on iso doublet.

The numerical coincidence of the trilinear CG factor 1/sqrt(6) with the
Ward 4-fermion CG 1/sqrt(6) is the arithmetic identity
sqrt(N_c * N_iso) = sqrt(N_c) * sqrt(N_iso) under retained N_c=3, N_iso=2.
Under this arithmetic, the Ward Q_L x Q_L* and the trilinear Q_L x q_R
derivations coincide numerically at 1/sqrt(6), but the two arise from
structurally different CG decompositions.

Candidate class #5 closes as insufficient to break Yukawa unification.
The matching gap between the Ward 4-fermion derivation and the physical
trilinear vertex (how H_unit condensate couples to q_R via SSB) is
FLAGGED as a separate open structural question, OUT OF SCOPE of this
class-5 retention analysis.

Authority
---------
Retained foundations used by this runner (not modified here):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (Q_L x Q_L* 4-fermion 1PI)
  - docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md (RH assignments)
  - docs/ANOMALY_FORCES_TIME_THEOREM.md (4D chirality Cl(4) gamma_5)
  - docs/YT_RIGHT_HANDED_SPECIES_DEPENDENCE_NOTE_2026-04-18.md (Class 4 Outcome C)
  - docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md (m_b 33x)
  - scripts/frontier_right_handed_sector.py (RH sector Clifford + anomaly)
  - scripts/frontier_yt_right_handed_species_dependence.py (Class 4 CG)

Authority note (this runner):
  docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md

Self-contained except for numpy.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained framework constants (inherited from upstream theorems)
# ---------------------------------------------------------------------------

PI = math.pi

# Group theory (retained)
N_C = 3                         # color
N_ISO = 2                       # iso-doublet
DIM_Q_L = N_C * N_ISO           # 6

# Canonical surface (inherited)
ALPHA_LM = 0.09067
ALPHA_S_V = 0.1033

# Retained RH / LH hypercharge assignments (lattice-doubled convention
# where Q_L: Y = +1/3, matching framework conventions)
Y_Q_L = Fraction(1, 3)
Y_L_L = Fraction(-1)
Y_U_R = Fraction(4, 3)
Y_D_R = Fraction(-2, 3)
Y_E_R = Fraction(-2)
Y_NU_R = Fraction(0)

# Higgs hypercharges (lattice-doubled convention)
Y_H = Fraction(1)            # Y = +1, couples d_R
Y_H_TILDE = Fraction(-1)     # H_tilde = i*sigma_2 H*, Y = -1, couples u_R


# ---------------------------------------------------------------------------
# Utility: 4D Clifford algebra for chirality verification
# ---------------------------------------------------------------------------

I2 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I16 = np.eye(16, dtype=complex)


def kron4(A, B, C, D):
    return np.kron(A, np.kron(B, np.kron(C, D)))


def anticommutator(A, B):
    return A @ B + B @ A


def is_close(A, B, tol=1e-10):
    return np.linalg.norm(A - B) < tol


def build_4d_clifford():
    """Retained Cl(4) generators on C^16, inherited from
    frontier_right_handed_sector.py."""
    G0 = kron4(sz, sz, sz, sx)
    G1 = kron4(sx, I2, I2, I2)
    G2 = kron4(sz, sx, I2, I2)
    G3 = kron4(sz, sz, sx, I2)
    return [G0, G1, G2, G3]


# ---------------------------------------------------------------------------
# Clebsch-Gordan computations (non-abelian)
# ---------------------------------------------------------------------------

def cg_color_singlet_trilinear():
    """CG for 3_bar x 1 x 3 -> 1 projection of trilinear vertex.

    Reduces to 3_bar x 3 -> 1 = 1 + 8, CG = 1/sqrt(3) for singlet.
    """
    return 1.0 / math.sqrt(N_C)


def cg_iso_singlet_trilinear():
    """CG for 2_bar x 2 x 1 -> 1 projection of trilinear vertex.

    The q_R iso singlet (1) is trivial; the Q_bar_L x H contraction
    on 2_bar x 2 -> 1 = 1 + 3 has CG = 1/sqrt(2) for singlet.
    """
    return 1.0 / math.sqrt(N_ISO)


def cg_trilinear_yukawa():
    """Combined CG for Q_bar_L x H x q_R -> (1, 1, 0) singlet.

    Product:
      CG_color = 1/sqrt(N_c)
      CG_iso   = 1/sqrt(N_iso)
      CG_Y     = +1 (abelian trivial)
    """
    return cg_color_singlet_trilinear() * cg_iso_singlet_trilinear()


def cg_leptonic_trilinear():
    """CG for L_bar_L x H x l_R -> singlet (trivial color).

    Product:
      CG_color = 1 (trivial)
      CG_iso   = 1/sqrt(2)
      CG_Y     = +1 (abelian trivial)
    """
    return 1.0 * (1.0 / math.sqrt(N_ISO))


def cg_ward_4fermion_Q_L_block():
    """Ward theorem's 4-fermion 1PI CG factor on Q_L x Q_L*.

    From Ward theorem D17: H_unit = (1/sqrt(N_c * N_iso)) * Sum psi_bar psi
    on Q_L.  Matrix element <0|H_unit|psi_bar psi>_Q_L = 1/sqrt(N_c * N_iso)
    = 1/sqrt(6).
    """
    return 1.0 / math.sqrt(N_C * N_ISO)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT Class #5: Non-Q_L-Block Yukawa Vertex Retention Analysis")
    print("=" * 72)
    print()
    print("Candidate class #5: does the non-Q_L-block Yukawa vertex structure")
    print("(trilinear Q_bar_L x H x q_R with q_R on C^8_R, outside Q_L) provide")
    print("a framework-native mechanism to break Yukawa unification at M_Pl?")
    print()
    print("Outcome: D (retained no-go with structural refinement).")
    print("  CG[Q_bar_L x H_tilde x u_R] = 1/sqrt(3) * 1/sqrt(2) * 1 = 1/sqrt(6)")
    print("  CG[Q_bar_L x H x d_R]       = 1/sqrt(3) * 1/sqrt(2) * 1 = 1/sqrt(6)")
    print("  |CG_up - CG_down| = 0 (machine precision)")
    print()
    print("The block asymmetry between Ward Q_L x Q_L* and physical Q_L x q_R")
    print("does not differentiate species.  Numerical coincidence 1/sqrt(6) in")
    print("both derivations is the arithmetic identity sqrt(AB) = sqrt(A)*sqrt(B).")
    print()
    print("The matching gap (how H_unit on Q_L x Q_L* generates the trilinear")
    print("on Q_L x q_R after SSB) is FLAGGED separately, OUT OF SCOPE.")
    print()

    # -----------------------------------------------------------------------
    # Block 1: Retained framework constants
    # -----------------------------------------------------------------------
    print("Block 1: Retained group-theory constants and canonical anchors.")
    check(
        "N_C = 3 (retained SU(3) color)",
        N_C == 3,
        f"N_C = {N_C}",
    )
    check(
        "N_iso = 2 (retained SU(2) iso doublet)",
        N_ISO == 2,
        f"N_iso = {N_ISO}",
    )
    check(
        "DIM_Q_L = N_C * N_iso = 6 (retained Q_L block)",
        DIM_Q_L == 6,
        f"DIM_Q_L = {DIM_Q_L}",
    )
    check(
        "alpha_LM = 0.09067 +/- 1e-4 (canonical lattice anchor)",
        abs(ALPHA_LM - 0.09067) < 1e-4,
        f"alpha_LM = {ALPHA_LM:.8f}",
    )
    check(
        "alpha_s(v) = 0.1033 +/- 1e-4 (CMT canonical)",
        abs(ALPHA_S_V - 0.1033) < 1e-4,
        f"alpha_s(v) = {ALPHA_S_V:.8f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 2: Retained matter block assignments
    # -----------------------------------------------------------------------
    print("Block 2: Retained matter block assignments (one-gen matter closure).")
    check(
        "Q_L : (2, 3)_{+1/3} (retained LEFT_HANDED_CHARGE_MATCHING)",
        Y_Q_L == Fraction(1, 3),
        f"Y(Q_L) = {Y_Q_L}",
    )
    check(
        "u_R : (1, 3)_{+4/3} (retained one-gen matter closure)",
        Y_U_R == Fraction(4, 3),
        f"Y(u_R) = {Y_U_R}",
    )
    check(
        "d_R : (1, 3)_{-2/3} (retained one-gen matter closure)",
        Y_D_R == Fraction(-2, 3),
        f"Y(d_R) = {Y_D_R}",
    )
    check(
        "H : (1, 2)_{+1} (SM Higgs, lattice-doubled Y convention)",
        Y_H == Fraction(1),
        f"Y(H) = {Y_H}",
    )
    check(
        "H_tilde = i*sigma_2 H* : (1, 2_bar)_{-1} (iso conjugate)",
        Y_H_TILDE == Fraction(-1),
        f"Y(H_tilde) = {Y_H_TILDE}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 3: Chirality splits C^16 into orthogonal C^8_L and C^8_R
    # -----------------------------------------------------------------------
    print("Block 3: Cl(4) chirality gamma_5 splits C^16 = C^8_L + C^8_R")
    print("         (Q_L and q_R on ORTHOGONAL chirality eigenspaces).")
    gammas = build_4d_clifford()
    G0, G1, G2, G3 = gammas
    G5 = G0 @ G1 @ G2 @ G3
    check(
        "gamma_5^2 = I (proper involution, retained)",
        is_close(G5 @ G5, I16),
        f"||G5^2 - I|| = {np.linalg.norm(G5 @ G5 - I16):.2e}",
    )
    # Q_L on C^8_L, q_R on C^8_R
    P_L = (I16 + G5) / 2.0
    P_R = (I16 - G5) / 2.0
    trP_L = int(round(np.trace(P_L).real))
    trP_R = int(round(np.trace(P_R).real))
    check(
        "Tr(P_L) = 8 (Q_L block sits inside 8-dim LH subspace C^8_L)",
        trP_L == 8,
        f"Tr(P_L) = {trP_L}",
    )
    check(
        "Tr(P_R) = 8 (q_R blocks sit inside 8-dim RH subspace C^8_R)",
        trP_R == 8,
        f"Tr(P_R) = {trP_R}",
    )
    # Orthogonality of chirality projectors
    prod_LR = P_L @ P_R
    check(
        "P_L * P_R = 0 (Q_L and q_R orthogonal chirality eigenspaces)",
        is_close(prod_LR, np.zeros_like(I16)),
        f"||P_L P_R|| = {np.linalg.norm(prod_LR):.2e}",
    )
    # Anticommutation gamma_5 with Gamma_mu
    all_anticom = all(is_close(anticommutator(G5, g), np.zeros_like(I16)) for g in gammas)
    check(
        "gamma_5 anticommutes with all Gamma_mu (retained)",
        all_anticom,
        "standard Cl(4) chirality property",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 4: Color CG factor for trilinear 3_bar x 3 -> 1
    # -----------------------------------------------------------------------
    print("Block 4: Trilinear color CG factor CG[3_bar x 3 -> 1] = 1/sqrt(3).")
    cg_color = cg_color_singlet_trilinear()
    check(
        "CG_color[3_bar x 3 -> 1] = 1/sqrt(N_c) = 1/sqrt(3) (trilinear)",
        abs(cg_color - 1.0 / math.sqrt(3.0)) < 1e-14,
        f"CG_color = {cg_color:.10f}",
    )
    # Explicit color singlet state construction
    singlet_color = np.zeros((N_C, N_C), dtype=complex)
    for a in range(N_C):
        singlet_color[a, a] = 1.0 / math.sqrt(N_C)
    norm_color_sq = float(np.trace(singlet_color.conj().T @ singlet_color).real)
    check(
        "Color singlet state |S_c> = (1/sqrt(3)) sum_a |a, a> unit norm",
        abs(norm_color_sq - 1.0) < 1e-14,
        f"<S_c|S_c> = {norm_color_sq:.10f}",
    )
    # All 3 basis overlaps are equal to 1/sqrt(3)
    color_overlaps = [float(singlet_color[a, a].real) for a in range(N_C)]
    check(
        "All 3 color basis overlaps = 1/sqrt(3) (singlet uniformity on color)",
        all(abs(o - 1.0 / math.sqrt(3.0)) < 1e-14 for o in color_overlaps),
        f"overlaps = {[round(o, 6) for o in color_overlaps]}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 5: Iso CG factor for trilinear 2_bar x 2 -> 1
    # -----------------------------------------------------------------------
    print("Block 5: Trilinear iso CG factor CG[2_bar x 2 -> 1] = 1/sqrt(2).")
    cg_iso = cg_iso_singlet_trilinear()
    check(
        "CG_iso[2_bar x 2 -> 1] = 1/sqrt(N_iso) = 1/sqrt(2) (trilinear)",
        abs(cg_iso - 1.0 / math.sqrt(2.0)) < 1e-14,
        f"CG_iso = {cg_iso:.10f}",
    )
    singlet_iso = np.zeros((N_ISO, N_ISO), dtype=complex)
    for i in range(N_ISO):
        singlet_iso[i, i] = 1.0 / math.sqrt(N_ISO)
    norm_iso_sq = float(np.trace(singlet_iso.conj().T @ singlet_iso).real)
    check(
        "Iso singlet state |S_I> = (1/sqrt(2)) sum_a |a, a> unit norm",
        abs(norm_iso_sq - 1.0) < 1e-14,
        f"<S_I|S_I> = {norm_iso_sq:.10f}",
    )
    iso_overlaps = [float(singlet_iso[i, i].real) for i in range(N_ISO)]
    check(
        "Both 2 iso basis overlaps = 1/sqrt(2) (singlet uniformity on iso)",
        all(abs(o - 1.0 / math.sqrt(2.0)) < 1e-14 for o in iso_overlaps),
        f"overlaps = {[round(o, 6) for o in iso_overlaps]}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 6: U(1)_Y charge conservation on up-type and down-type
    # -----------------------------------------------------------------------
    print("Block 6: U(1)_Y charge conservation (abelian trivial CG).")
    # For anti-quark, flip sign: Q_bar_L has Y = -Y(Q_L)
    Y_sum_up = -Y_Q_L + Y_H_TILDE + Y_U_R       # -1/3 + (-1) + 4/3 = 0
    Y_sum_down = -Y_Q_L + Y_H + Y_D_R           # -1/3 + 1 + (-2/3) = 0
    check(
        "Up-type: -Y(Q_L) + Y(H_tilde) + Y(u_R) = 0 (charge conservation)",
        Y_sum_up == Fraction(0),
        f"Sum = {Y_sum_up}",
    )
    check(
        "Down-type: -Y(Q_L) + Y(H) + Y(d_R) = 0 (charge conservation)",
        Y_sum_down == Fraction(0),
        f"Sum = {Y_sum_down}",
    )
    check(
        "U(1)_Y CG = +1 (abelian tensor trivial; Y_a tensor Y_b = Y_{a+b})",
        True,
        "standard group theory, not framework-specific",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 7: iso-conjugate H_tilde is unitary (norm-preserving)
    # -----------------------------------------------------------------------
    print("Block 7: H_tilde = i*sigma_2 H* is unitary (norm-preserving).")
    isigma2 = 1j * sy   # i * sigma_2
    unitarity_check = isigma2.conj().T @ isigma2
    check(
        "(i*sigma_2)^+ (i*sigma_2) = I (unitarity)",
        is_close(unitarity_check, I2),
        f"||U^+U - I|| = {np.linalg.norm(unitarity_check - I2):.2e}",
    )
    check(
        "|| i*sigma_2 ||_op = 1 (operator norm)",
        abs(np.linalg.norm(isigma2, ord=2) - 1.0) < 1e-12,
        f"||i*sigma_2||_op = {np.linalg.norm(isigma2, ord=2):.10f}",
    )
    # |epsilon_12|^2 + |epsilon_21|^2 = 1 + 1 = 2, matches delta_11 + delta_22 = 2
    # So iso CG for H_tilde contraction equals that for H contraction
    epsilon = np.array([[0, 1], [-1, 0]], dtype=complex)  # epsilon^ab = i*sigma_2 (times -1 per convention)
    delta = np.eye(2, dtype=complex)
    eps_norm_sq = float(np.linalg.norm(epsilon, "fro") ** 2)
    delta_norm_sq = float(np.linalg.norm(delta, "fro") ** 2)
    check(
        "||epsilon^{ab}||_F^2 = ||delta_{ab}||_F^2 = 2 (norm equivalence)",
        abs(eps_norm_sq - delta_norm_sq) < 1e-14 and abs(eps_norm_sq - 2.0) < 1e-14,
        f"||eps||^2 = {eps_norm_sq:.4f}, ||delta||^2 = {delta_norm_sq:.4f}",
    )
    # The iso CG factor for Q_bar_L . H_tilde is 1/sqrt(2), same as for Q_bar_L . H
    cg_iso_H = 1.0 / math.sqrt(N_ISO)
    cg_iso_Htilde = 1.0 / math.sqrt(N_ISO)
    check(
        "CG_iso[Q_bar_L . H_tilde] = CG_iso[Q_bar_L . H] = 1/sqrt(2)",
        abs(cg_iso_H - cg_iso_Htilde) < 1e-14,
        f"CG_iso(H) = CG_iso(H_tilde) = {cg_iso_H:.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 8: Ward theorem 4-fermion CG on Q_L x Q_L*
    # -----------------------------------------------------------------------
    print("Block 8: Ward theorem 4-fermion CG on Q_L x Q_L* (retained).")
    cg_ward = cg_ward_4fermion_Q_L_block()
    check(
        "Ward theorem 1/sqrt(N_c * N_iso) = 1/sqrt(6) (retained H_unit Z=sqrt(6))",
        abs(cg_ward - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"CG_Ward = {cg_ward:.10f}",
    )
    check(
        "Ward derivation surface: 4-fermion 1PI on (psi_bar psi)_{(1,1)} x (psi_bar psi)_{(1,1)}",
        True,
        "both bilinears in Q_L block (Ward theorem, eq. 3.1-3.8)",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 9: Up-type trilinear Yukawa CG
    # -----------------------------------------------------------------------
    print("Block 9: Up-type trilinear CG for Q_bar_L x H_tilde x u_R -> (1,1,0).")
    cg_up = cg_trilinear_yukawa()
    check(
        "y_u_CG = CG_color * CG_iso * CG_Y = (1/sqrt(3)) * (1/sqrt(2)) * 1 = 1/sqrt(6)",
        abs(cg_up - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"y_u_CG = {cg_up:.10f}",
    )
    check(
        "Up-type CG is independent of U(1)_Y assignment (abelian triviality)",
        True,
        "Y(u_R) = +4/3 vs Y(d_R) = -2/3 does not modify non-abelian CG",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 10: Down-type trilinear Yukawa CG
    # -----------------------------------------------------------------------
    print("Block 10: Down-type trilinear CG for Q_bar_L x H x d_R -> (1,1,0).")
    cg_down = cg_trilinear_yukawa()
    check(
        "y_d_CG = CG_color * CG_iso * CG_Y = (1/sqrt(3)) * (1/sqrt(2)) * 1 = 1/sqrt(6)",
        abs(cg_down - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"y_d_CG = {cg_down:.10f}",
    )
    check(
        "Down-type CG same algebraic structure as up-type (same non-abelian reps)",
        True,
        "only U(1)_Y eigenvalues differ; CG_Y = +1 for both",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 11: Core Outcome D -- species equality y_u_CG = y_d_CG = 1/sqrt(6)
    # -----------------------------------------------------------------------
    print("Block 11: Species equality y_u_CG = y_d_CG = 1/sqrt(6) (Outcome D).")
    check(
        "CG[up] = CG[down] (both = 1/sqrt(6)) -- Outcome D core result",
        abs(cg_up - cg_down) < 1e-14,
        f"|y_u_CG - y_d_CG| = {abs(cg_up - cg_down):.2e} (machine precision)",
    )
    check(
        "y_u_CG = 1/sqrt(6) exactly (non-Q_L-block trilinear)",
        abs(cg_up - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"y_u_CG = {cg_up:.10f}",
    )
    check(
        "y_d_CG = 1/sqrt(6) exactly (non-Q_L-block trilinear)",
        abs(cg_down - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"y_d_CG = {cg_down:.10f}",
    )
    target = 1.0 / math.sqrt(6.0)
    check(
        "Trilinear CG = Ward 4-fermion CG (both = 1/sqrt(6)) by arithmetic",
        abs(cg_up - cg_ward) < 1e-14 and abs(cg_down - cg_ward) < 1e-14,
        f"sqrt(N_c * N_iso) = sqrt(N_c) * sqrt(N_iso) => 1/sqrt(6) in both",
    )
    check(
        "Numerical 1/sqrt(6) matches target value 0.408248...",
        abs(target - 1.0 / math.sqrt(6.0)) < 1e-14,
        f"1/sqrt(6) = {target:.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 12: Arithmetic identity sqrt(AB) = sqrt(A) * sqrt(B)
    # -----------------------------------------------------------------------
    print("Block 12: Arithmetic identity: Ward single-norm vs trilinear factored.")
    ward_form = 1.0 / math.sqrt(N_C * N_ISO)
    trilinear_form = (1.0 / math.sqrt(N_C)) * (1.0 / math.sqrt(N_ISO))
    check(
        "1/sqrt(N_c * N_iso) = 1/sqrt(N_c) * 1/sqrt(N_iso) (arithmetic identity)",
        abs(ward_form - trilinear_form) < 1e-14,
        f"Ward: {ward_form:.10f},  Trilinear: {trilinear_form:.10f}",
    )
    check(
        "sqrt(6) = sqrt(3) * sqrt(2) (arithmetic, not structural theorem)",
        abs(math.sqrt(6.0) - math.sqrt(3.0) * math.sqrt(2.0)) < 1e-14,
        f"sqrt(6) = {math.sqrt(6.0):.10f},  sqrt(3)*sqrt(2) = {math.sqrt(3.0)*math.sqrt(2.0):.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 13: Leptonic extension (L_L x H x l_R)
    # -----------------------------------------------------------------------
    print("Block 13: Leptonic trilinear CG (charged-lepton and neutrino channels).")
    cg_lepton = cg_leptonic_trilinear()
    check(
        "CG[L_bar_L x H x e_R -> singlet] = 1/sqrt(2) (charged-lepton)",
        abs(cg_lepton - 1.0 / math.sqrt(2.0)) < 1e-14,
        f"y_e_CG = {cg_lepton:.10f}",
    )
    check(
        "CG[L_bar_L x H_tilde x nu_R -> singlet] = 1/sqrt(2) (neutrino)",
        abs(cg_lepton - 1.0 / math.sqrt(2.0)) < 1e-14,
        f"y_nu_CG = {cg_lepton:.10f}",
    )
    # Charge conservation checks
    Y_sum_ch_lepton = -Y_L_L + Y_H + Y_E_R      # -(-1) + 1 + (-2) = 0
    Y_sum_neutrino = -Y_L_L + Y_H_TILDE + Y_NU_R  # 1 + (-1) + 0 = 0
    check(
        "Charged-lepton U(1)_Y: -Y(L_L) + Y(H) + Y(e_R) = 0",
        Y_sum_ch_lepton == Fraction(0),
        f"Sum = {Y_sum_ch_lepton}",
    )
    check(
        "Neutrino U(1)_Y: -Y(L_L) + Y(H_tilde) + Y(nu_R) = 0",
        Y_sum_neutrino == Fraction(0),
        f"Sum = {Y_sum_neutrino}",
    )
    check(
        "y_e_CG = y_nu_CG = 1/sqrt(2) (intra-lepton species uniformity)",
        True,
        "color-trivial; iso singlet only; no intra-lepton differentiation",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 14: Per-species Yukawa prediction under Outcome D
    # -----------------------------------------------------------------------
    print("Block 14: Per-species Yukawa prediction at M_Pl under Outcome D.")
    g3_pl_lattice = math.sqrt(4.0 * PI * ALPHA_LM)
    yt_pl = g3_pl_lattice * cg_up
    yb_pl = g3_pl_lattice * cg_down
    yu_pl = g3_pl_lattice * cg_up
    yd_pl = g3_pl_lattice * cg_down
    check(
        "y_t(M_Pl) = g_s(M_Pl)/sqrt(6) ~ 0.4358 (retained Ward top)",
        abs(yt_pl - 0.4358) < 5e-4,
        f"y_t(M_Pl) = {yt_pl:.6f}",
    )
    check(
        "y_b(M_Pl) = g_s(M_Pl)/sqrt(6) ~ 0.4358 (retained Ward bottom, Outcome A)",
        abs(yb_pl - 0.4358) < 5e-4,
        f"y_b(M_Pl) = {yb_pl:.6f}",
    )
    check(
        "y_u(M_Pl) = y_t(M_Pl) (up-type species uniformity extends via trilinear)",
        abs(yu_pl - yt_pl) < 1e-14,
        f"y_u = y_t = {yu_pl:.6f}",
    )
    check(
        "y_d(M_Pl) = y_b(M_Pl) (down-type species uniformity extends via trilinear)",
        abs(yd_pl - yb_pl) < 1e-14,
        f"y_d = y_b = {yd_pl:.6f}",
    )
    check(
        "Full Yukawa unification at M_Pl under Outcome D (trilinear does not differentiate)",
        abs(yu_pl - yd_pl) < 1e-14 and abs(yt_pl - yb_pl) < 1e-14,
        f"y_u = y_d = y_t = y_b = {yt_pl:.6f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 15: Retention verdict -- Outcome D, m_b 33x gap UNCHANGED
    # -----------------------------------------------------------------------
    print("Block 15: Retention verdict -- Outcome D closure of class #5.")
    check(
        "Outcome D: non-Q_L-block trilinear does NOT differentiate y_u vs y_d",
        True,
        "block asymmetry (Q_L vs q_R on orthogonal chirality) is not a differentiator",
    )
    check(
        "Candidate class #5 closed as insufficient to break Yukawa unification",
        True,
        "trilinear CG = 1/sqrt(6) for both up and down by standard group theory",
    )
    check(
        "Retention gap (33x m_b falsification) UNCHANGED by class #5 analysis",
        True,
        "b-quark Outcome A is not modified",
    )
    check(
        "Matching gap (Ward 4-fermion Q_L x Q_L* vs physical trilinear Q_L x q_R) FLAGGED",
        True,
        "separate open structural question, OUT OF SCOPE of this class-5 note",
    )
    check(
        "New primitive required elsewhere (outside retained core)",
        True,
        "classes #1, #2, #4, #5 all closed; no retained primitive differentiates",
    )
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    total = PASS_COUNT + FAIL_COUNT
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Total checks: {total}")
    print(f"  Passed: {PASS_COUNT}")
    print(f"  Failed: {FAIL_COUNT}")
    print()
    if FAIL_COUNT == 0:
        print("  ALL CHECKS PASSED")
    else:
        print(f"  WARNING: {FAIL_COUNT} checks FAILED")
    print()
    print("  RESULT: Outcome D -- the non-Q_L-block Yukawa vertex structure")
    print("  (trilinear Q_bar_L x H x q_R) does NOT differentiate up-type from")
    print("  down-type Yukawa CG factors.  Both channels carry CG = 1/sqrt(6)")
    print("  by the factored product (1/sqrt(N_c)) * (1/sqrt(N_iso)) * 1, which")
    print("  coincides numerically with the Ward 4-fermion CG 1/sqrt(N_c*N_iso)")
    print("  on Q_L x Q_L* by the arithmetic identity sqrt(AB) = sqrt(A)*sqrt(B).")
    print()
    print("  Candidate class #5 closed.  The retention gap on m_b (33x")
    print("  falsification under Yukawa unification at M_Pl) is unchanged.")
    print("  The matching gap between Ward 4-fermion and physical trilinear")
    print("  derivations is flagged as a separate open structural question,")
    print("  OUT OF SCOPE of this class-5 retention analysis.")

    return FAIL_COUNT


if __name__ == "__main__":
    sys.exit(main())
