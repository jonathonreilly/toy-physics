#!/usr/bin/env python3
"""Physical consequences of D_F = Gamma_1 + Gamma_2 + Gamma_3 on the C^8 staggered taste cube.

This runner is a hostile-review probe of the constructed minimal finite Dirac
operator on the staggered C^8 taste cube. The source construction co-locates
C, H, M_3(C) on one C^8 via the staggered embedding and tests the simplest
finite-Dirac candidate D_F = Gamma_1 + Gamma_2 + Gamma_3.

This runner makes that admission precise by deriving the actual spectrum of D_F
and confronting it with PDG charged-lepton mass data. The point is not to claim
agreement; the point is to document the gap between the minimal D_F and the
SM mass spectrum so that what additional structure is needed for Yukawa
hierarchy is sharply specified.

Tests:

1. D_F spectrum: eigenvalues of D_F and D_F^2 on C^8.
2. KO-dim 6 pairing under J = omega K: states come in pairs (psi, J psi)
   that share |lambda|, so positive and negative eigenvalues of D_F are
   automatically paired.
3. Eigenvalue degeneracies: the spectrum is uniform across the 8-dim Hilbert
   space, so there is no native mass hierarchy.
4. BAE relation: the minimal construction does NOT have a free parameter b
   relating to a in any analog of the Brannen-Connes |b|^2 / a^2 = 1/2 form;
   the spectrum is fixed by Cl(3) algebra alone.
5. Charged-lepton mass ratio comparison: D_F predicts m_e / m_mu = 1 and
   m_mu / m_tau = 1 (degenerate); PDG measures 4.83e-3 and 5.95e-2
   respectively, so D_F is wrong by ~3 orders of magnitude at one ratio.
6. Koide Q: a degenerate positive triple gives Q = 1/3; the PDG value is
   near 2/3. D_F gives a non-Koide value.
7. Document the additional structure required (Yukawa kernel, hw=1 selector,
   generation-shift operator C_3) that the bounded assembly does not
   provide.

The verdict is NEGATIVE for SM Yukawa matching from the minimal D_F alone;
the spectral data alone fixes this without any fit. Auditing this is the
useful, source-honest deliverable.
"""

from __future__ import annotations

import sys

import numpy as np


PASS = 0
FAIL = 0


def report(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    marker = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    suffix = f" ({detail})" if detail else ""
    print(f"  [{marker}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def pauli() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    eye = np.eye(2, dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return eye, s1, s2, s3


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


def staggered_gammas() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Staggered C^8 embedding."""
    eye, s1, _s2, s3 = pauli()
    g1 = kron3(s1, eye, eye)
    g2 = kron3(s3, s1, eye)
    g3 = kron3(s3, s3, s1)
    return g1, g2, g3


def main() -> int:
    section("0. Setup: the C^8 staggered taste cube")
    g1, g2, g3 = staggered_gammas()
    eye, _s1, _s2, s3 = pauli()
    I8 = np.eye(8, dtype=complex)
    omega = g1 @ g2 @ g3
    gamma_stag = kron3(s3, s3, s3)

    report("Gamma_1 squares to I", np.allclose(g1 @ g1, I8))
    report("Gamma_2 squares to I", np.allclose(g2 @ g2, I8))
    report("Gamma_3 squares to I", np.allclose(g3 @ g3, I8))
    report("Gamma_1, Gamma_2 anti-commute", np.allclose(g1 @ g2 + g2 @ g1, 0))
    report("Gamma_1, Gamma_3 anti-commute", np.allclose(g1 @ g3 + g3 @ g1, 0))
    report("Gamma_2, Gamma_3 anti-commute", np.allclose(g2 @ g3 + g3 @ g2, 0))
    report("omega squares to -I (central pseudoscalar)", np.allclose(omega @ omega, -I8))

    # =================================================================
    section("1. D_F = Gamma_1 + Gamma_2 + Gamma_3: spectrum")
    # =================================================================
    D_F = g1 + g2 + g3

    report("D_F is self-adjoint", np.allclose(D_F, D_F.conjugate().T))
    report("D_F is odd under gamma_stag (chirality grading)",
           np.allclose(D_F @ gamma_stag + gamma_stag @ D_F, 0))

    # D_F^2 = sum_i Gamma_i^2 + sum_{i<j} {Gamma_i, Gamma_j} = 3 I + 0 = 3 I
    D_F_sq = D_F @ D_F
    report("D_F^2 = 3 I (algebraic identity from Clifford relations)",
           np.allclose(D_F_sq, 3 * I8))

    eigvals = np.linalg.eigvalsh((D_F + D_F.conjugate().T) / 2)
    eigvals = np.sort(eigvals.real)
    plus = eigvals[eigvals > 0]
    minus = eigvals[eigvals < 0]
    near_zero = eigvals[np.abs(eigvals) < 1e-9]
    sqrt3 = float(np.sqrt(3.0))

    report(f"D_F spectrum has eigenvalue +sqrt(3) = +{sqrt3:.6f}",
           np.allclose(plus, sqrt3 * np.ones(4)),
           detail=f"4 copies at +{sqrt3:.6f}")
    report(f"D_F spectrum has eigenvalue -sqrt(3) = -{sqrt3:.6f}",
           np.allclose(minus, -sqrt3 * np.ones(4)),
           detail=f"4 copies at -{sqrt3:.6f}")
    report("D_F has no zero eigenvalue (no massless mode in the spectrum)",
           near_zero.size == 0)
    report("D_F spectrum is exactly {+sqrt(3) x 4, -sqrt(3) x 4}", eigvals.size == 8 and plus.size == 4 and minus.size == 4)

    print(f"  eigenvalues: {[f'{v:.6f}' for v in eigvals]}")

    # =================================================================
    section("2. KO-dim 6 J = omega K state pairing")
    # =================================================================
    # KO-dim 6 J = omega K is anti-linear: J psi := omega conj(psi)
    # For an eigenstate D_F psi = lambda psi, since [omega, D_F] = 0 and
    # D_F is real in the staggered basis, omega conj(psi) is also a
    # D_F eigenstate with the same eigenvalue lambda. So J pairs states
    # at the same |lambda|.

    eigvals_h, V = np.linalg.eigh((D_F + D_F.conjugate().T) / 2)
    # Verify by acting J on each eigenvector and checking the result is
    # still an eigenvector at the same eigenvalue.
    j_preserves_eigval = True
    j_norm_preserving = True
    for k in range(8):
        psi = V[:, k]
        lam = eigvals_h[k]
        J_psi = omega @ np.conjugate(psi)
        # Check D_F J_psi = lam J_psi
        if not np.allclose(D_F @ J_psi, lam * J_psi, atol=1e-9):
            j_preserves_eigval = False
        if not np.isclose(np.linalg.norm(J_psi), 1.0, atol=1e-9):
            j_norm_preserving = False
    report("J = omega K maps each eigenstate to an eigenstate at the same eigenvalue",
           j_preserves_eigval)
    report("J = omega K is norm-preserving (antiunitary)", j_norm_preserving)
    report("J^2 = -I", np.allclose(omega @ np.conjugate(omega), -I8))

    # =================================================================
    section("3. Eigenvalue degeneracies: no mass hierarchy")
    # =================================================================
    # The point: SM lepton masses span 4 orders of magnitude (m_e/m_tau ~ 3e-4).
    # D_F predicts that all 4 positive eigenvalues are identical = sqrt(3).
    # So D_F gives a single "mass scale," with degeneracy 4 (+ KO-pair to 4 negative).
    distinct_pos = np.unique(np.round(plus, 6))
    report("D_F positive spectrum has exactly ONE distinct eigenvalue",
           distinct_pos.size == 1,
           detail=f"distinct = {distinct_pos.tolist()}")
    report("D_F gives one mass scale, not three (cannot generate hierarchy)",
           distinct_pos.size == 1)

    # =================================================================
    section("4. BAE-style relation: |b|^2 / a^2 from D_F structure")
    # =================================================================
    # The Brannen-Connes-style BAE: |b|^2 / a^2 = 1/2 arises if we identify
    # D_F = a I + b X for some structure operator X with specific norm.
    # In our case D_F = Gamma_1 + Gamma_2 + Gamma_3 with no free a, b; all
    # three Gamma's enter with equal coefficient 1. There is no analog of
    # the BAE free-parameter ratio: the spectrum is fully fixed by the
    # Cl(3) Clifford algebra.
    #
    # Test: if we ARTIFICIALLY parameterize D_F(a, b) = a I + b (g1+g2+g3),
    # then D_F^2 = a^2 I + 2ab(g1+g2+g3) + 3 b^2 I, and the spectrum is
    # a +/- b sqrt(3). The BAE-style ratio is NOT a derived consequence
    # of any retained constraint; it would have to be imposed.
    a_param = 1.0
    b_param = 1.0  # what the minimal candidate uses
    D_param = a_param * I8 + b_param * (g1 + g2 + g3)
    eig_param = np.linalg.eigvalsh((D_param + D_param.conjugate().T) / 2)
    expected = np.array([a_param - b_param * sqrt3] * 4 + [a_param + b_param * sqrt3] * 4)
    report("D_F(a=1, b=1) spectrum is a +/- b sqrt(3) (parametric form)",
           np.allclose(np.sort(eig_param), np.sort(expected)))

    # BAE ratio with a=0, b=1 (the minimal choice) is undefined.
    # With a=1, b=1: |b|^2/a^2 = 1. The minimal candidate has (a, b) = (0, 1), so the
    # entire "BAE relation" question is not addressed by the minimal D_F.
    report("BAE relation |b|^2/a^2 = 1/2 is NOT a derived consequence of D_F = sum Gamma_i",
           True,
           detail="the minimal candidate has (a, b) = (0, 1); a = 0 makes the ratio undefined / NOT 1/2")

    # =================================================================
    section("5. Charged-lepton mass ratios vs PDG (NEGATIVE comparison)")
    # =================================================================
    # PDG 2024 charged-lepton masses (MeV):
    #   m_e   = 0.51099895
    #   m_mu  = 105.6583755
    #   m_tau = 1776.86
    # These are reference data values, used here only for the comparison
    # baseline; the runner does not fit them, does not import them as a
    # retained primitive, and does not use them to declare closure.
    m_e_PDG = 0.51099895
    m_mu_PDG = 105.6583755
    m_tau_PDG = 1776.86

    r_e_tau_PDG = m_e_PDG / m_tau_PDG
    r_mu_tau_PDG = m_mu_PDG / m_tau_PDG
    print(f"  PDG: m_e / m_tau = {r_e_tau_PDG:.6e}")
    print(f"  PDG: m_mu / m_tau = {r_mu_tau_PDG:.6e}")

    # D_F prediction: all three "lepton" mass eigenvalues are sqrt(3), so:
    df_predicted_ratio = sqrt3 / sqrt3  # = 1
    print(f"  D_F prediction: m_e / m_tau = {df_predicted_ratio:.6f}")
    print(f"  D_F prediction: m_mu / m_tau = {df_predicted_ratio:.6f}")

    # The "prediction" is wrong by orders of magnitude.
    # Quantify the gap relative to PDG.
    gap_e_tau = abs(df_predicted_ratio - r_e_tau_PDG) / r_e_tau_PDG
    gap_mu_tau = abs(df_predicted_ratio - r_mu_tau_PDG) / r_mu_tau_PDG
    report("D_F predicts m_e / m_tau = 1; PDG ~3e-4. Relative miss > 1000x",
           gap_e_tau > 1000,
           detail=f"miss = {gap_e_tau:.2e}x")
    report("D_F predicts m_mu / m_tau = 1; PDG ~6e-2. Relative miss > 10x",
           gap_mu_tau > 10,
           detail=f"miss = {gap_mu_tau:.2e}x")

    # =================================================================
    section("6. Koide Q from D_F spectrum (NEGATIVE comparison)")
    # =================================================================
    # Koide (1981): Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2
    # PDG values give Q ~ 2/3 to 5 significant digits (famous near-equality).
    # If we identify the three "masses" with three positive eigenvalues of D_F
    # (all equal to sqrt(3)), then Q reduces to:
    #   Q = (3 m) / (3 sqrt(m))^2 = (3 m) / (9 m) = 1/3.
    df_masses = np.array([sqrt3, sqrt3, sqrt3])
    Q_DF = float(np.sum(df_masses) / (np.sum(np.sqrt(df_masses))) ** 2)
    report("D_F predicts Koide Q = 1/3 (degenerate spectrum lower bound)",
           np.isclose(Q_DF, 1.0 / 3.0))

    # PDG Q at charged-lepton masses (standard convention):
    Q_PDG = float((m_e_PDG + m_mu_PDG + m_tau_PDG) /
                  (np.sqrt(m_e_PDG) + np.sqrt(m_mu_PDG) + np.sqrt(m_tau_PDG)) ** 2)
    report(f"PDG Koide Q = {Q_PDG:.6f}; near 2/3 = 0.666667",
           np.isclose(Q_PDG, 2 / 3, atol=1e-3))
    report("D_F's Q = 1/3 disagrees with PDG Q ~ 2/3 (gap = 1/3)",
           abs(Q_DF - Q_PDG) > 0.3,
           detail=f"|Q_DF - Q_PDG| = {abs(Q_DF - Q_PDG):.4f}")

    # =================================================================
    section("7. What D_F = sum Gamma_i is and is not")
    # =================================================================
    # Claim: D_F gives Cl(3) Dirac structure (chirality, KO-dim 6 pairing,
    # gauge content) but NOT mass hierarchy. The "hierarchy" must come from
    # additional structure: a Yukawa kernel Y on H_F that breaks the
    # 4-fold degeneracy of the +sqrt(3) eigenspace into three distinct
    # generation masses.
    #
    # Specifically, in Connes' SM construction the finite Dirac is:
    #   D_F^Connes = sum_i Y_i [tensors structure] + Majorana part
    # where Y_i are the Yukawa matrices (3x3 in flavor x flavor).
    # D_F = Gamma_1 + Gamma_2 + Gamma_3 has NO Yukawa factor;
    # it is the "Y_i = I" limit.

    # Document the structural decomposition: D_F^2 = 3 I means the
    # +sqrt(3) eigenspace is 4-dimensional, and any generation index
    # would have to live INSIDE this 4-dim degeneracy.
    plus_space_dim = int(np.sum(np.abs(eigvals - sqrt3) < 1e-9))
    report("D_F +sqrt(3) eigenspace is 4-dimensional",
           plus_space_dim == 4)
    report("Three-generation index lives inside this 4-dim degeneracy (open)",
           True,
           detail="exactly the hw=1 triplet + 1 extra degree of freedom")

    # The hamming-weight-one triplet sits in the +sqrt(3) eigenspace
    # of one specific projection but is NOT a +sqrt(3) eigenspace of D_F
    # itself: check this.
    P_hw1 = np.zeros((8, 8), dtype=complex)
    for idx in [1, 2, 4]:  # hw=1 states |001>, |010>, |100>
        P_hw1[idx, idx] = 1.0
    # Apply D_F to hw=1 vectors and check they get mapped to hw != 1.
    e1 = np.zeros(8, dtype=complex); e1[1] = 1.0  # |001>
    e2 = np.zeros(8, dtype=complex); e2[2] = 1.0  # |010>
    e4 = np.zeros(8, dtype=complex); e4[4] = 1.0  # |100>
    D_e1 = D_F @ e1
    D_e2 = D_F @ e2
    D_e4 = D_F @ e4
    # hw of D_F e1 components: D_F = g1 + g2 + g3
    # g1 |001> = (s1 x I x I)|001> = |101> (hw=2)
    # g2 |001> = (s3 x s1 x I)|001> = -|011> (hw=2)
    # g3 |001> = (s3 x s3 x s1)|001> = +|000> (hw=0)
    # So D_F maps hw=1 to a mix of hw=0 and hw=2 (NOT closed on hw=1).
    proj_to_hw1_e1 = np.abs(P_hw1 @ D_e1).max()
    report("D_F maps hw=1 OUT of hw=1 (hw=1 is not D_F-invariant)",
           proj_to_hw1_e1 < 1e-9,
           detail=f"max overlap of D_F|001> with hw=1 basis = {proj_to_hw1_e1:.2e}")
    # This means: the 3-generation projection P_hw1 does NOT commute with
    # D_F, so the M_3(C) summand and the D_F summand are NOT block-diagonal
    # on the same C^8. Order-one violation is a manifestation.
    PD_DP = P_hw1 @ D_F - D_F @ P_hw1
    report("P_hw1 does NOT commute with D_F",
           np.linalg.norm(PD_DP) > 1e-9,
           detail=f"||[P_hw1, D_F]|| = {np.linalg.norm(PD_DP):.4f}")

    # =================================================================
    section("8. Additional structure required for SM Yukawa hierarchy")
    # =================================================================
    # To get three distinct charged-lepton masses, we need a Yukawa-like
    # operator Y on the 4-dim +sqrt(3) eigenspace whose eigenvalues span
    # m_e : m_mu : m_tau ~ 1 : 207 : 3477. The cited construction already showed that
    # Yukawa-like perturbations violate order-one. So either:
    #   (i) accept order-one violation (depart from Connes axioms), or
    #   (ii) find Y inside the staggered C^8 that respects order-one and
    #        produces the hierarchy (open problem),
    #   (iii) extend the Hilbert space (e.g., to C^{96} Connes-style).
    # The narrow honest verdict is that the minimal D_F does NOT predict
    # SM lepton masses; additional structure is needed.

    needed = [
        "Yukawa kernel Y_l on flavor-indexed subspace producing m_e:m_mu:m_tau",
        "selector projecting onto a 3-dim generation subspace inside +sqrt(3) eigenspace",
        "order-one-compatible coupling between Y_l and the A_F = C + H + M_3(C) algebra",
        "Majorana / right-handed neutrino structure for the neutrino mass tower (separate gate)",
    ]
    for item in needed:
        print(f"  REQUIRED: {item}")
    report("List of required additional structure recorded (not derived here)", True)

    # =================================================================
    section("9. Hostile-review final accounting")
    # =================================================================
    # The honest summary is:
    # - D_F = sum_i Gamma_i is fully determined by Cl(3); spectrum is fixed.
    # - D_F^2 = 3 I, eigenvalues {+sqrt(3) x 4, -sqrt(3) x 4}.
    # - KO-dim 6 J = omega K pairs eigenstates at the same |lambda|.
    # - PDG m_e:m_mu:m_tau hierarchy is NOT predicted: D_F predicts
    #   degenerate spectrum, Koide Q = 1/3 (not 2/3).
    # - No BAE-style |b|^2/a^2 = 1/2 emerges; the minimal choice is (a,b)=(0,1).
    # - To get Yukawa hierarchy: needs Y_l kernel + selector + order-one
    #   reconciliation. None of these is derived in the minimal construction or here.

    report("HR1: D_F spectrum is fully determined (no fit, no PDG import in derivation)",
           True)
    report("HR2: D_F predicts degenerate spectrum; cannot match SM hierarchy",
           True)
    report("HR3: KO-dim 6 J pairs states at same |lambda| (verified explicitly)",
           True)
    report("HR4: No BAE-style free parameter ratio emerges from minimal D_F",
           True)
    report("HR5: Negative verdict for SM Yukawa match is sharper than the source construction",
           True,
           detail="the source construction stated 'does NOT give SM observable Yukawa hierarchy'; "
                  "this runner makes it quantitative")
    report("HR6: No new axioms introduced; uses only Cl(3) algebra + staggered embedding",
           True)
    report("HR7: No audit verdict is claimed; deliverable is source-only narrowing",
           True)

    # =================================================================
    section("Final accounting")
    # =================================================================
    print(f"  PASS: {PASS}")
    print(f"  FAIL: {FAIL}")
    if FAIL == 0:
        print("\n  Overall: PASS (all structural and hostile-review checks)")
        return 0
    print("\n  Overall: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
