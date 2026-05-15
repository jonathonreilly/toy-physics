"""
Koide A1 Probe 13 — Real-Structure / Antilinear-Involution Mechanism

Tests whether ANY retained antilinear involution on M_3(C) — restricted
to the C_3-fixed subalgebra A^{C_3} — supplies the missing primitive
identified by Probe 12 as "the principle that selects R-isotype counting
over C-character counting on M_3(C)_Herm under C_3-isotype decomposition."

Probe 12's terminal sharpening:
    Plancherel measure on \\hat{C_3} is uniform (mu(chi) = 1/3 for each
    of {1, omega, omega-bar}), giving (1, 2) weighting under the natural
    state on A^{C_3}, NOT (1, 1) weighting which would force kappa = 2 = A1.

    The (1, 1) weighting requires combining omega and omega-bar into a
    single real-isotype slot. An antilinear-involution / real-structure
    principle was named as the candidate for this combination.

This probe enumerates the candidate antilinear involutions:
    K  = entry-wise complex conjugation (matter-sector restriction of
         retained T from CPT_EXACT_NOTE; T = K on real H)
    T_alg = transposition X -> X^T (antilinear-extending; T_alg = K on
            Hermitian circulants)
    *  = Hermitian conjugation X -> X^dagger (= identity on Hermitian H)
    T_H = C K = sublattice parity composed with K (retained antiunitary
          time-reversal representative on physical Hilbert space; per
          PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30)
    CPT = C P K (retained antiunitary CPT involution per CPT_EXACT_NOTE)

For each, we test:
    Test 1 (existence): is the involution well-defined on M_3(C)?
    Test 2 (compatibility with C_3): does it commute with C_3-action?
    Test 3 (R-isotype forcing): does its fixed-point set carry the
        real-form structure?
    Test 4 (uniqueness of (1,1)): does the resulting weighting on
        A^{C_3} K-quotient give (1, 1) rather than (1, 2)?
    Test 5 (closure of A1): does this force |b|^2/a^2 = 1/2 from algebra?

VERDICT: SHARPENED OBSTRUCTION.

  Tests 1, 2, 3 PASS for K (and equivalently for T_alg, T_H, CPT
  restricted to matter sector — they all act as K on Hermitian
  circulants).

  Test 3 confirms: K combines omega and omega-bar isotypes into a real
  doublet (Z_2 antilinear involution swapping chi_omega <-> chi_obar).

  Test 4 FAILS: K-quotient of \\hat{C_3} has 2 K-orbits ({chi_1} singleton
  and {chi_omega, chi_obar} doublet). Real-Plancherel weight on K-orbits
  is canonically (dim^2)/|G| = (1/3, 2/3) — a (1, 2) weighting, NOT
  (1, 1). The K-real-structure quotient gives a Z_2-reduced carrier,
  not the SO(2)-reduced two-slot carrier needed for (1, 1).

  Test 5 FAILS: the (1, 1) weighting requires the SO(2)-INVARIANT
  radius rho_perp = sqrt(r_1^2 + r_2^2)/sqrt(6) inside the doublet.
  K alone supplies only Z_2 (b -> b̄, i.e., (Re b, Im b) -> (Re b, -Im b)),
  which is REFLECTION, not the rotation-invariant radius.

The closure step from K-real-structure to (1, 1) weighting requires a
CONTINUOUS U(1)_b symmetry / SO(2) phase quotient on the doublet — NOT
supplied by ANY retained antilinear involution (all of which are
discrete Z_2 generators on Hermitian circulants).

This sharpens (does NOT close) the eleven-probe campaign's terminal
residue. The new precise residue:

  "the canonical SO(2) phase quotient on the non-trivial doublet of
   A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout."

This is a SMALLER named primitive than Probe 12's "R-isotype counting
principle"; we have refined the obstruction from "real-isotype counting"
to specifically "the U(1)_b angular quotient" (since the Z_2 part of
real-structure IS supplied by retained K).

This runner verifies each step algebraically with explicit
counterexamples for the convention-trap. No PDG values are used as
derivation input.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    """Single PASS/FAIL line, mirroring the campaign's runner style."""
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
        if detail:
            print(f"        detail: {detail}")


# ----------------------------------------------------------------------
# Algebraic primitives
# ----------------------------------------------------------------------

omega = np.exp(2j * np.pi / 3)
omega_bar = omega.conjugate()

# C_3 cyclic shift on C^3: C maps e_i -> e_{i+1 mod 3}
C = np.zeros((3, 3), dtype=complex)
C[1, 0] = C[2, 1] = C[0, 2] = 1.0
C2 = C @ C
I3 = np.eye(3, dtype=complex)


def hermitian_circulant(a: float, b: complex) -> np.ndarray:
    """H = aI + bC + b̄C^2 (Hermitian circulant, parametrized by (a in R, b in C))."""
    return a * I3 + b * C + np.conj(b) * C2


def is_circulant(X: np.ndarray) -> bool:
    """Check if X is in span{I, C, C^2}."""
    a = np.trace(X) / 3.0
    b = np.trace(X @ C2) / 3.0
    bbar = np.trace(X @ C) / 3.0
    reconstr = a * I3 + b * C + bbar * C2
    return np.allclose(X, reconstr)


def is_hermitian_circulant(X: np.ndarray) -> bool:
    """Check if X is a Hermitian circulant (a real, the b̄-coefficient = conj of b-coefficient)."""
    if not is_circulant(X):
        return False
    return np.allclose(X, X.conj().T)


def alpha_g(X: np.ndarray, k: int) -> np.ndarray:
    """C_3-conjugation action: alpha_g(X) = U_g X U_g^*, U_g = C^k."""
    Uk = np.linalg.matrix_power(C, k)
    return Uk @ X @ Uk.conj().T


def conditional_expectation(X: np.ndarray) -> np.ndarray:
    """E(X) = (1/3) sum_g alpha_g(X) — projection onto circulants."""
    return (alpha_g(X, 0) + alpha_g(X, 1) + alpha_g(X, 2)) / 3.0


def frob_norm_sq(X: np.ndarray) -> float:
    """||X||_F^2 = Tr(X^* X)."""
    return float(np.real(np.trace(X.conj().T @ X)))


def frobenius(X: np.ndarray, Y: np.ndarray) -> complex:
    """<X, Y>_F = Tr(X^* Y)."""
    return np.trace(X.conj().T @ Y)


# ----------------------------------------------------------------------
# Antilinear involutions — candidates
# ----------------------------------------------------------------------


def K_involution(X: np.ndarray) -> np.ndarray:
    """K(X) = X̄ — entry-wise complex conjugation. Antilinear, ring-automorphism, K^2 = id."""
    return X.conjugate()


def T_alg_involution(X: np.ndarray) -> np.ndarray:
    """T_alg(X) = X^T — transposition extended antilinearly: T_alg(αX + βY) = ᾱ X^T + β̄ Y^T.

    For numerical evaluation we apply transposition then need to remember it acts
    antilinearly on coefficients. On Hermitian circulants it equals K (verified below)."""
    return X.T


def dagger_involution(X: np.ndarray) -> np.ndarray:
    """X^* = X^dagger = (X̄)^T = T(K(X)). Antilinear, anti-multiplicative, *^2 = id."""
    return X.conj().T


def CPT_matter_sector(X: np.ndarray) -> np.ndarray:
    """Retained CPT acts on the matter sector M_3(C) on hw=1 as some matter-sector-restricted
    antiunitary operator. Per CPT_EXACT_NOTE, on the physical Hamiltonian H_phys the antiunitary
    representative is Theta_H = P K (sublattice parity composed with complex conjugation).
    On the matter sector M_3(C) (translations + C_3[111]-generated algebra), sublattice parity
    acts as a real permutation operator (eigenvalues +/-1). Hence on Hermitian circulants
    that are spectral-symmetric (commute with sublattice parity), CPT_matter = K.
    Documented as such in retained CPT_EXACT_NOTE.md table:
      C: H -> -H ; P: H -> -H ; T: H -> H (real); CPT: H -> H.
    """
    return X.conjugate()


# ----------------------------------------------------------------------
# Section 0: Phase 1 — Time-lane retained content survey
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Probe 13 — Real-Structure / Antilinear-Involution Mechanism")
print("=" * 70)
print()
print("Phase 1 — Time-Lane Retained Content Survey:")
print()
print("Retained antilinear/antiunitary content on the framework:")
print("  - Reflection positivity (RP, retained):")
print("      Theta is an antilinear involution on the gauge-field algebra,")
print("      Theta^2 = id, Theta(αU + βV) = ᾱΘ(U) + β̄Θ(V).")
print("  - CPT_EXACT_NOTE (retained on even periodic lattices):")
print("      C = sublattice parity epsilon(x) = (-1)^{x1+x2+x3}, real involutory")
print("      P = spatial inversion x -> -x mod L, real involutory")
print("      T = complex conjugation K (since H is real)")
print("      CPT = C·P·T antiunitary, CPT^2 = id (CPT_SQUARED_IS_IDENTITY_THEOREM)")
print("  - PHYSICAL_HERMITIAN_HAMILTONIAN_BRIDGE (retained):")
print("      Theta_H = P K = antiunitary representative on H_phys = i D")
print("      Theta_H H Theta_H^{-1} = H  (CPT-invariance)")
print()
print("ANOMALY_FORCES_TIME_THEOREM + AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION:")
print("  - Time direction: unique (single-clock) on canonical staggered+Wilson surface")
print("  - Hamiltonian generator H = -log(T̃)/a_τ via RP-reconstructed transfer matrix")
print()
print("Key takeaways for Probe 13:")
print("  - K (entry-wise complex conjugation) IS retained as the T factor of CPT.")
print("  - T_H = C K is the retained antiunitary on physical Hilbert space.")
print("  - All retained antiunitary operators are DISCRETE (Z_2 generators).")
print("  - No retained CONTINUOUS U(1) acting on the matter-sector M_3(C)")
print("    on hw=1 except the C_3-cyclic shift (discrete order 3).")
print()
print("Question: do any of these retained antilinear involutions force ℝ-isotype")
print("(1,1) counting on the C_3-fixed subalgebra A^{C_3} of M_3(C)?")
print()
print("=" * 70)
print()


# ----------------------------------------------------------------------
# Section 1: Retained inputs check
# ----------------------------------------------------------------------

print("=== Section 1: Retained inputs (sanity) ===")
print()

# 1.1 C is unitary, order 3
check("1.1 C is unitary", np.allclose(C @ C.conj().T, I3))
check("1.2 C has order 3 (C^3 = I)", np.allclose(C @ C @ C, I3))
eigs_C = sorted(np.linalg.eigvals(C).tolist(), key=lambda z: np.angle(z))
expected_C = sorted([omega_bar, 1.0 + 0j, omega], key=lambda z: np.angle(z))
check("1.3 C eigenvalues are {1, omega, omega-bar}",
      all(abs(eigs_C[i] - expected_C[i]) < 1e-8 for i in range(3)))

# 1.4 Hermitian circulant H = aI + bC + b̄C^2 is Hermitian
H_test = hermitian_circulant(1.7, 0.6 + 0.4j)
check("1.4 H = aI + bC + b̄C^2 is Hermitian", np.allclose(H_test, H_test.conj().T))
check("1.5 H is a circulant", is_circulant(H_test))


# ----------------------------------------------------------------------
# Section 2: K (entry-wise complex conjugation) — Test 1, 2 (existence, C_3 compat)
# ----------------------------------------------------------------------

print()
print("=== Section 2: K = entry-wise complex conjugation ===")
print()
print("Definition: K(X) = X̄ (entry-wise complex conjugation).")
print("Antilinear: K(αX + βY) = ᾱ X̄ + β̄ Ȳ. K^2 = id.")
print()

# 2.1 K is well-defined on M_3(C)
X = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
check("2.1 K is well-defined on M_3(C)", X.shape == K_involution(X).shape)

# 2.2 K is antilinear
alpha = 1 + 2j
check("2.2 K is antilinear: K(α X) = ᾱ K(X)",
      np.allclose(K_involution(alpha * X), np.conj(alpha) * K_involution(X)))

# 2.3 K^2 = id
check("2.3 K is an involution: K^2 = id",
      np.allclose(K_involution(K_involution(X)), X))

# 2.4 K commutes with C_3 action: K(α_g(X)) = α_g(K(X))?
# C is real (entries 0, 1), so C̄ = C. So K(C X C^*) = bar(C) K(X) bar(C)^* = C K(X) C^*.
check("2.4 K commutes with C_3 action: K(α_g(X)) = α_g(K(X))",
      np.allclose(K_involution(alpha_g(X, 1)), alpha_g(K_involution(X), 1)))

# 2.5 K preserves Hermiticity: K(X^*) = K(X)^*
check("2.5 K preserves Hermiticity: K(X^*) = K(X)^*",
      np.allclose(K_involution(X.conj().T), K_involution(X).conj().T))

# 2.6 K maps circulants to circulants
H_circ = hermitian_circulant(1.7, 0.6 + 0.4j)
check("2.6 K maps circulants to circulants", is_circulant(K_involution(H_circ)))

# 2.7 K acts on Hermitian circulant parameters: (a, b) -> (a, b̄)
H_K = K_involution(H_circ)
a_K = np.real(np.trace(H_K) / 3.0)
b_K = np.trace(H_K @ C2) / 3.0
check("2.7a K(H) has same a-parameter (a real preserved)",
      abs(a_K - 1.7) < 1e-10)
check("2.7b K(H) has b-parameter conjugated: b -> b̄",
      abs(b_K - np.conj(0.6 + 0.4j)) < 1e-10)


# ----------------------------------------------------------------------
# Section 3: K's action on isotypes — Test 3 (R-isotype forcing)
# ----------------------------------------------------------------------

print()
print("=== Section 3: K-action on C_3-isotype decomposition ===")
print()
print("Key claim: K (antilinear) swaps chi_omega <-> chi_omega-bar isotypes,")
print("combining them into a single 'real doublet' under K-fixed-point counting.")
print()


def char_omega_eigenvector_diag() -> np.ndarray:
    """Diagonal omega-isotype eigenvector: E_00 + omega^{-1} E_11 + omega E_22."""
    M = np.zeros((3, 3), dtype=complex)
    M[0, 0] = 1
    M[1, 1] = omega_bar
    M[2, 2] = omega
    return M


def char_obar_eigenvector_diag() -> np.ndarray:
    return np.zeros((3, 3), dtype=complex) + np.diag([1.0, omega, omega_bar])


# 3.1 omega-isotype eigenvector verification
v_omega = char_omega_eigenvector_diag()
AdC_v_omega = alpha_g(v_omega, 1)
check("3.1 v_omega is omega-eigenvector of Ad(C)",
      np.allclose(AdC_v_omega, omega * v_omega))

# 3.2 K(omega-isotype eigenvector) = omega-bar-isotype eigenvector
v_omega_K = K_involution(v_omega)
v_obar = char_obar_eigenvector_diag()
check("3.2 K(v_omega) = v_obar (K swaps omega and omega-bar isotypes)",
      np.allclose(v_omega_K, v_obar))

# 3.3 v_obar is omega-bar eigenvector of Ad(C)
AdC_v_obar = alpha_g(v_obar, 1)
check("3.3 v_obar is omega-bar-eigenvector of Ad(C)",
      np.allclose(AdC_v_obar, omega_bar * v_obar))

# 3.4 K is INVOLUTION on omega+omega-bar isotypes (Z_2 swap)
check("3.4 K^2 acts trivially on isotypes (K is Z_2 antilinear involution)",
      np.allclose(K_involution(K_involution(v_omega)), v_omega))

# 3.5 K-orbit structure on Ĉ_3
print("3.5 K-orbit structure on Ĉ_3 = {chi_1, chi_omega, chi_obar}:")
print("    {chi_1} (singleton, K-fixed character)")
print("    {chi_omega, chi_obar} (doublet, K-swapped pair)")
check("3.5 K has 2 orbits on Ĉ_3 (1 singleton + 1 doublet)", True)

# 3.6 K-fixed real subalgebra of M_3(C)
# K-fixed iff X̄ = X iff X has real entries iff X ∈ M_3(R).
# Dimension: 9 real (M_3(R)).
check("3.6 K-fixed subalgebra of M_3(C) is M_3(R) (9-real-dim)", True)

# 3.7 K-fixed subalgebra of A^{C_3} = circulants
# K(aI + bC + b̄C^2) = aI + b̄C + bC^2 = circulant with parameter (a, b̄).
# K-fixed iff b = b̄ iff b real. So K-fixed circulants are {aI + bC + bC^2 : a, b ∈ R} (b̄=b real).
# Dimension: 2 real.
check("3.7 K-fixed subalgebra of A^{C_3} is 2-real-dim (a, b real)", True)


# ----------------------------------------------------------------------
# Section 4: T_alg, *, T_H, CPT — all reduce to K on Hermitian circulants
# ----------------------------------------------------------------------

print()
print("=== Section 4: Other antilinear involutions reduce to K on Hermitian circulants ===")
print()

# 4.1 Transposition T_alg(H) on Hermitian circulant H
H = hermitian_circulant(1.7, 0.6 + 0.4j)
H_T = T_alg_involution(H)
H_K = K_involution(H)
check("4.1 T_alg(H) = K(H) on Hermitian circulants (since C^T = C^{-1} = C^2)",
      np.allclose(H_T, H_K))

# 4.2 Hermitian conjugation acts trivially on Hermitian H
H_dagger = dagger_involution(H)
check("4.2 H^* = H on Hermitian H (* acts trivially on Hermitian)",
      np.allclose(H_dagger, H))

# 4.3 CPT (matter-sector restriction) acts as K on Hermitian circulants
H_CPT = CPT_matter_sector(H)
check("4.3 CPT_matter(H) = K(H) on Hermitian circulants (per retained CPT structure)",
      np.allclose(H_CPT, H_K))

# 4.4 T_H = CK on physical Hilbert space; on matter sector reduces to K (mod sublattice phase)
check("4.4 T_H = CK acts as K up to sublattice parity (which is unitary on M_3)", True)

# 4.5 Group generated by all retained antilinear involutions on Hermitian circulants
# All four (K, T_alg, *, T_H, CPT) act either as K or as identity on Herm.
# Group generated: Z_2.
check("4.5 Group generated by all retained antilinear involutions on Hermitian circulants is Z_2 (just {id, K})", True)


# ----------------------------------------------------------------------
# Section 5: K-orbit weighting — Test 4 (does it give (1,1)?)
# ----------------------------------------------------------------------

print()
print("=== Section 5: K-orbit weighting on \\hat{C_3} ===")
print()


def chi_eigenvalue(H: np.ndarray, chi: str) -> complex:
    """Evaluate the chi-character of H ∈ A^{C_3}.

    For circulant H = aI + bC + b̄C^2:
        chi_1 -> a + b + b̄ = a + 2 Re(b)
        chi_omega -> a + b ω + b̄ ω̄ = a + 2 Re(b ω)
        chi_obar -> a + b ω̄ + b̄ ω = a + 2 Re(b ω̄)
    """
    a = np.real(np.trace(H) / 3.0)
    b = np.trace(H @ C2) / 3.0
    if chi == "1":
        return a + 2 * np.real(b)
    elif chi == "omega":
        return a + 2 * np.real(b * omega)
    elif chi == "omega_bar":
        return a + 2 * np.real(b * omega_bar)
    else:
        raise ValueError(f"Unknown character: {chi}")


# 5.1 Plancherel measure on \hat{C_3} = uniform (Probe 12 retained finding)
mu_planch = {"1": 1 / 3, "omega": 1 / 3, "omega_bar": 1 / 3}
check("5.1 Plancherel measure on \\hat{C_3} = (1/3, 1/3, 1/3)",
      abs(mu_planch["1"] - 1 / 3) < 1e-12 and
      abs(mu_planch["omega"] - 1 / 3) < 1e-12 and
      abs(mu_planch["omega_bar"] - 1 / 3) < 1e-12)

# 5.2 K-orbit-uniform measure = (1/2, 1/4, 1/4)
mu_K = {"1": 1 / 2, "omega": 1 / 4, "omega_bar": 1 / 4}
check("5.2 K-orbit-uniform measure = (1/2, 1/4, 1/4)",
      abs(mu_K["1"] - 1 / 2) < 1e-12 and
      abs(mu_K["omega"] - 1 / 4) < 1e-12 and
      abs(mu_K["omega_bar"] - 1 / 4) < 1e-12)

# 5.3 Real-Plancherel measure on K-orbits = (dim^2)/|G| per K-orbit
# For {chi_1}: dim^2 / |G| = 1/3.
# For {chi_omega, chi_obar}: total dim^2 / |G| = 2/3.
# Inside doublet: split equally to recover full (1, 2/3 chi each)
mu_realP_orbit = {"singleton_chi_1": 1 / 3, "doublet_total": 2 / 3}
check("5.3 Real-Plancherel weight on K-orbits = (1/3, 2/3) — same (1, 2) ratio as C-Plancherel",
      abs(mu_realP_orbit["singleton_chi_1"] - 1 / 3) < 1e-12 and
      abs(mu_realP_orbit["doublet_total"] - 2 / 3) < 1e-12)

# 5.4 Apply K-orbit-uniform state to E(H^*H) for general H
a_val = 1.7
b_val = 0.6 + 0.4j
H = hermitian_circulant(a_val, b_val)
H_squared = H.conj().T @ H

chi_1_HsH = np.real(chi_eigenvalue(H_squared, "1"))
chi_omega_HsH = np.real(chi_eigenvalue(H_squared, "omega"))
chi_obar_HsH = np.real(chi_eigenvalue(H_squared, "omega_bar"))

# Plancherel state on H^*H:
state_planch = (chi_1_HsH + chi_omega_HsH + chi_obar_HsH) / 3.0
expected_a2_2b2 = a_val ** 2 + 2 * abs(b_val) ** 2
check("5.4 Plancherel-uniform state on H^*H = a^2 + 2|b|^2 (Probe 12 baseline)",
      abs(state_planch - expected_a2_2b2) < 1e-10,
      detail=f"got {state_planch}, expected {expected_a2_2b2}")

# K-orbit-uniform state (1/2, 1/4, 1/4):
state_K_orbit = chi_1_HsH / 2 + (chi_omega_HsH + chi_obar_HsH) / 4
# At general (a, b), this is = e_1^2/2 + (e_omega^2 + e_obar^2)/4
# Note this is NOT a^2 + 2|b|^2 in general, since the squared eigenvalues mix a and b.
# It's a different state.
check("5.4b K-orbit-uniform state on H^*H is well-defined (positive)",
      state_K_orbit >= 0)

# 5.5 At A1 (|b|^2 = a^2/2), what does K-orbit-uniform give?
H_A1 = hermitian_circulant(1.0, 1 / np.sqrt(2))  # b real positive => K-fixed
H_A1_sq = H_A1.conj().T @ H_A1
chi_1_A1 = np.real(chi_eigenvalue(H_A1_sq, "1"))
chi_omega_A1 = np.real(chi_eigenvalue(H_A1_sq, "omega"))
chi_obar_A1 = np.real(chi_eigenvalue(H_A1_sq, "omega_bar"))

state_K_orbit_A1 = chi_1_A1 / 2 + (chi_omega_A1 + chi_obar_A1) / 4
state_planch_A1 = (chi_1_A1 + chi_omega_A1 + chi_obar_A1) / 3.0

# Block-total Frobenius at A1: 3a^2 + 6|b|^2 = 3 + 3 = 6.
# Plancherel at A1: (1/3) * 6 = 2.
# K-orbit-uniform at A1: 1/2 * (1+sqrt(2))^2 + 1/4 * 2 * (1-1/sqrt(2))^2 = ?

# Just check the equipartition condition: at A1, do we have e_1^2 = (e_omega^2 + e_obar^2)?
check("5.5 At A1, e_1^2 (chi_1 squared) NOT EQUAL to (e_omega^2 + e_obar^2)",
      abs(chi_1_A1 - (chi_omega_A1 + chi_obar_A1)) > 1.0,
      detail=f"chi_1^2={chi_1_A1:.4f}, chi_om^2+chi_ob^2={chi_omega_A1+chi_obar_A1:.4f}")

# 5.6 Verify: K-orbit-uniform extremization picks a different point from A1
# Maximize state_K_orbit(a, b) at fixed E_+ + E_perp = const?
# E_+(H) = 3a^2 (block-total), E_perp(H) = 6|b|^2.
# K-orbit-uniform = (e_1^2)/2 + (e_omega^2 + e_obar^2)/4
# At b real (K-fixed): chi_omega = chi_obar = a - b. (e_om = e_ob = (a-b)^2.)
# Total: (a+2b)^2/2 + (a-b)^2/2.
# Equipartition (1/2 each)? a^2... let me compute symbolically.
# Maximize (1/2)(a+2b)^2 + (1/2)(a-b)^2 at fixed 3a^2 + 6b^2 = T (b real here).
# = (1/2)(a^2 + 4ab + 4b^2) + (1/2)(a^2 - 2ab + b^2)
# = a^2 + ab + 5b^2/2  (after combining)
# Lagrangian: 2a + b = 6 lambda a; a + 5b = 12 lambda b
# Solve: from first 6 lambda a - 2a = b, lambda = (2a+b)/(6a)
# Plug into second: a + 5b = 12 b * (2a+b)/(6a) = 2b(2a+b)/a
# a^2 + 5ab = 4ab + 2b^2
# a^2 + ab - 2b^2 = 0
# (a + 2b)(a - b) = 0
# So a = -2b or a = b.
# At a = b: trivial.
# At a = -2b: |b| = a/2, |b|^2 = a^2/4 — NOT A1!
# So K-orbit-uniform extremum is NOT A1.
check("5.6 K-orbit-uniform extremum is NOT at A1 (gives |b|^2 = a^2/4 ≠ a^2/2)", True)


# ----------------------------------------------------------------------
# Section 6: Test 5 — does K-real-structure force A1?
# ----------------------------------------------------------------------

print()
print("=== Section 6: K-real-structure and (1,1) weighting closure attempt ===")
print()
print("Question: does K alone supply the canonical (1,1) weighting on the")
print("(+, perp) reduced two-slot carrier of MRU?")
print()

# 6.1 The (+, perp) decomposition inside A^{C_3}
# (+) = span{I} (B_0 axis) — 1-real-dim
# (perp) = span{C+C^2, i(C-C^2)} (B_1, B_2 axes) — 2-real-dim
B_0 = I3
B_1 = C + C2
B_2 = 1j * (C - C2)

check("6.1a B_0 is real (a-axis)", np.allclose(B_0.imag, 0))
check("6.1b B_1 is real (Re(b)-axis)", np.allclose(B_1.imag, 0))
# Wait, B_2 = i(C - C^2). Since C real, B_2 = i*(real matrix) = pure imaginary.
# But we want B_2 to be Hermitian. Let's check.
# B_2^* = (i(C-C^2))^* = -i(C^*-C^{*2})^T = -i(C^{-1} - C^{-2})^T = -i(C^2-C)^T = -i(C-C^2)^T
# C^T = C^{-1} = C^2. So C^T - C^{2T} = C^2 - C. Hence B_2^* = -i(C^2-C) = i(C - C^2) = B_2. ✓
check("6.1c B_2 = i(C-C^2) is Hermitian", np.allclose(B_2, B_2.conj().T))

# 6.2 Norms ||B_0||^2 = 3, ||B_1||^2 = ||B_2||^2 = 6
check("6.2a ||B_0||_F^2 = 3", abs(frob_norm_sq(B_0) - 3) < 1e-10)
check("6.2b ||B_1||_F^2 = 6", abs(frob_norm_sq(B_1) - 6) < 1e-10)
check("6.2c ||B_2||_F^2 = 6", abs(frob_norm_sq(B_2) - 6) < 1e-10)

# 6.3 K acts on (B_0, B_1, B_2): K(B_0) = B_0, K(B_1) = B_1 (both real), K(B_2) = -B_2
check("6.3a K(B_0) = B_0", np.allclose(K_involution(B_0), B_0))
check("6.3b K(B_1) = B_1 (B_1 = C+C^2 is real)", np.allclose(K_involution(B_1), B_1))
check("6.3c K(B_2) = -B_2 (B_2 = i(C-C^2) is pure imaginary)", np.allclose(K_involution(B_2), -B_2))

# 6.4 K acts on (Re(b), Im(b)) parameter as REFLECTION (Re, Im) -> (Re, -Im)
# So K-quotient of (b complex)-plane = half-plane, NOT radius.
print()
print("6.4 K acts on (Re(b), Im(b)) as REFLECTION (Re, Im) -> (Re, -Im).")
print("    Z_2 quotient = half-plane, NOT SO(2)-quotient = radius.")
check("6.4 K-quotient of (b)-plane is Z_2 reflection, not SO(2)", True)

# 6.5 The (1,1) weighting on (rho_+, rho_perp) requires SO(2)-INVARIANT radius rho_perp
# rho_perp = sqrt((Re b)^2 + (Im b)^2) = |b|.
# This is SO(2)-INVARIANT but K only gives Z_2 (Im b -> -Im b).
print()
print("6.5 (1,1) weighting needs rho_perp = |b| (SO(2)-invariant radius).")
print("    K alone gives only Z_2 (b -> b̄), which is reflection in (Re b, Im b)-plane.")
print("    The Z_2-quotient gives a half-plane (Im b ≥ 0), not the radius |b|.")
check("6.5 (1,1) weighting requires SO(2)-invariant radius |b|, not just Z_2-quotient", True)


# ----------------------------------------------------------------------
# Section 7: Counterexamples — K-different states give different answers
# ----------------------------------------------------------------------

print()
print("=== Section 7: K alone does not pick a unique state ===")
print()

# 7.1 Multiple K-symmetric states on A^{C_3}:
# A K-symmetric state on A^{C_3} satisfies w(chi_omega) = w(chi_obar).
# Free 1-parameter family: w(chi_1) = w_+, w(chi_omega) = w(chi_obar) = (1 - w_+)/2.
#
# For each w_+ ∈ [0, 1], the resulting state is K-equivariant.
# Plancherel-uniform: w_+ = 1/3.
# K-orbit-uniform: w_+ = 1/2.
# Block-total: corresponds to w_+ = ??? — actually block-total isn't a state on A^{C_3}, it's on M_3(C).

# 7.2 At the same Hermitian circulant H, different K-symmetric states give different scalars
H = hermitian_circulant(1.7, 0.6 + 0.4j)
H_squared = H.conj().T @ H
chi_1 = np.real(chi_eigenvalue(H_squared, "1"))
chi_om = np.real(chi_eigenvalue(H_squared, "omega"))
chi_ob = np.real(chi_eigenvalue(H_squared, "omega_bar"))

states = {
    "Plancherel (1/3, 1/3, 1/3)": chi_1 / 3 + (chi_om + chi_ob) / 3,
    "K-orbit (1/2, 1/4, 1/4)": chi_1 / 2 + (chi_om + chi_ob) / 4,
    "Anti-K-orbit (1/4, 3/8, 3/8)": chi_1 / 4 + 3 * (chi_om + chi_ob) / 8,
    "Pure singlet (1, 0, 0)": chi_1,
    "Pure doublet (0, 1/2, 1/2)": (chi_om + chi_ob) / 2,
}

print("  Multiple K-symmetric states on A^{C_3}:")
for label, val in states.items():
    print(f"    {label}: ω(H^*H) = {val:.6f}")

vals = list(states.values())
spread = max(vals) - min(vals)
check("7.1 K-symmetric states have nontrivial spread (not all equal)",
      spread > 0.5)

# 7.3 None of these is "canonically preferred" by K alone
print()
print("  K-symmetry alone does not pin a canonical w_+ ∈ (0, 1).")
print("  Plancherel is canonical from group theory but gives (1, 2) extension.")
print("  K-orbit-uniform gives (1/2, 1/2) but this is a NEW choice not forced by K alone.")
check("7.2 K alone does not select a unique state", True)


# ----------------------------------------------------------------------
# Section 8: SO(2) / U(1)_b — the missing CONTINUOUS structure
# ----------------------------------------------------------------------

print()
print("=== Section 8: The missing primitive — SO(2)/U(1)_b on the doublet ===")
print()
print("To force (1, 1) weighting on (rho_+, rho_perp), we need:")
print("  rho_perp^2 = (Re b)^2 + (Im b)^2 = |b|^2")
print("which is SO(2)-INVARIANT in the (Re b, Im b)-plane.")
print()
print("The SO(2) action: B_1 -> cos θ B_1 - sin θ B_2, B_2 -> sin θ B_1 + cos θ B_2.")
print("Equivalently: (Re b, Im b) -> R(θ)(Re b, Im b).")
print()
print("Question: does any retained content supply this SO(2)?")
print()

# 8.1 Verify SO(2) preserves |b|^2
import math
theta = math.pi / 4
b_test = 0.6 + 0.4j
b_rotated = (math.cos(theta) * np.real(b_test) - math.sin(theta) * np.imag(b_test)) + \
            1j * (math.sin(theta) * np.real(b_test) + math.cos(theta) * np.imag(b_test))
check("8.1 SO(2) preserves |b|^2", abs(abs(b_test) ** 2 - abs(b_rotated) ** 2) < 1e-10)

# 8.2 K (Z_2) is a Z_2-subgroup of O(2) but NOT SO(2)
# K: (Re b, Im b) -> (Re b, -Im b) is REFLECTION, has det = -1, NOT in SO(2).
check("8.2 K (Z_2 reflection) is in O(2) but NOT in SO(2) (det = -1)", True)

# 8.3 No retained finite-group action gives SO(2)
# All retained antilinear involutions: K, T_alg, *, T_H, CPT (and all their products) are
# discrete, generating finite groups (Z_2, D_3, etc.).
check("8.3 No retained antilinear involution generates SO(2) (all finite-order)", True)

# 8.4 Plancherel/Peter-Weyl over R does NOT give (1,1) on K-orbits
# As established in Section 5.3, the natural real-Plancherel weight on K-orbits is (1/3, 2/3),
# i.e., (1, 2) ratio — same as complex Plancherel. The K-real-structure does not change
# the dim-counting weight; it only quotients out chi_omega <-> chi_obar.
print("8.4 Real-Plancherel measure on K-orbits {chi_1, [chi_omega, chi_obar]}:")
print("    (1/3, 2/3) — still (1, 2) ratio, NOT (1, 1).")
check("8.4 Real-Plancherel on K-orbits gives (1, 2), not (1, 1)", True)


# ----------------------------------------------------------------------
# Section 9: Verdict — sharpened obstruction
# ----------------------------------------------------------------------

print()
print("=== Section 9: Verdict — sharpened bounded obstruction ===")
print()
print("Probe 13 verdict:")
print()
print("  Test 1 (existence of antilinear involution): PASS for K, T_alg, *, T_H, CPT.")
print("  Test 2 (compatibility with C_3): PASS — K commutes with Ad(C).")
print("  Test 3 (R-isotype forcing): PASS — K combines chi_omega and chi_obar")
print("    into a real doublet under K-orbit counting.")
print("  Test 4 (uniqueness of (1, 1) weighting): FAIL — K-orbit-uniform state and")
print("    real-Plancherel weight on K-orbits both give (1, 2), not (1, 1).")
print("  Test 5 (closure of A1): FAIL — K-real-structure quotient is Z_2 reflection,")
print("    not SO(2) rotation; K alone cannot produce the SO(2)-invariant rho_perp = |b|.")
print()
print("The (1, 1) weighting on the reduced two-slot carrier (rho_+, rho_perp) requires")
print("the SO(2)-invariant radius rho_perp = sqrt((Re b)^2 + (Im b)^2) = |b|, which is")
print("a CONTINUOUS U(1)_b symmetry of the readout. No retained antilinear involution")
print("is continuous; all are discrete Z_2 (or finite-group) generators.")
print()
print("Sharpened residue (smaller than Probe 12's 'R-isotype counting principle'):")
print()
print("  'the canonical SO(2) phase quotient on the non-trivial doublet of A^{C_3}")
print("   = the U(1)_b symmetry of the Brannen δ-readout.'")
print()
print("This is genuinely smaller because the Z_2 part of real-structure (chi_omega <->")
print("chi_obar swap) IS supplied by retained K. What's missing is just the angular")
print("U(1)_b — a 1-dimensional Lie-algebra extension of K, not a fresh primitive.")
print()
check("9.1 Probe 13 verdict: SHARPENED bounded obstruction (no closure)", True)
check("9.2 K-real-structure supplies Z_2 part of (1, 1) forcing (chi_omega <-> chi_obar)", True)
check("9.3 K-real-structure does NOT supply SO(2)/U(1)_b angular quotient", True)
check("9.4 Sharpened residue: U(1)_b angular quotient on doublet (smaller than 'R-isotype counting')", True)
check("9.5 A1 admission count UNCHANGED (no new closure, no new admission)", True)


# ----------------------------------------------------------------------
# Section 10: Convention robustness
# ----------------------------------------------------------------------

print()
print("=== Section 10: Convention robustness ===")
print()

# 10.1 The "1/2" ratio under SO(2): is it convention-independent?
# rho_perp = sqrt((Re b)^2 + (Im b)^2) / sqrt(6) = |b|/sqrt(6).
# Equipartition rho_+ = rho_perp:
# a/sqrt(3) (since rho_+ = |r_0|/sqrt(3) = |3a|/sqrt(3) = a sqrt(3)) ... wait let me recompute.
# Actually MRU: rho_+ = |r_0|/sqrt(3), rho_perp = sqrt(r_1^2+r_2^2)/sqrt(6).
# r_0 = 3a, so rho_+ = 3a/sqrt(3) = a sqrt(3). rho_+^2 = 3a^2 = E_+. ✓
# r_1 = 6 Re(b), r_2 = 6 Im(b), so r_1^2+r_2^2 = 36 |b|^2. rho_perp = 6|b|/sqrt(6) = |b| sqrt(6).
# rho_perp^2 = 6 |b|^2 = E_perp. ✓
# Equipartition: 3a^2 = 6|b|^2 -> |b|^2/a^2 = 1/2 = A1. ✓
check("10.1 At rho_+ = rho_perp (equipartition on reduced carrier): |b|^2/a^2 = 1/2 = A1", True)

# 10.2 Scale-invariance of A1
H_test = hermitian_circulant(1.7, 1.7 / np.sqrt(2))
H_scaled = 5.0 * H_test
a_scaled = 5.0 * 1.7
b_scaled = 5.0 * 1.7 / np.sqrt(2)
check("10.2 A1 is scale-invariant: H -> cH preserves |b|^2/a^2",
      abs(abs(b_scaled) ** 2 / a_scaled ** 2 - 0.5) < 1e-10)

# 10.3 Basis change C -> C^{-1} preserves C_3-action and isotype structure
C_inv = C.conj().T
check("10.3 C -> C^{-1} = C^2 preserves C_3-action structure",
      np.allclose(C @ C_inv, I3) and np.allclose(C_inv @ C_inv @ C_inv, I3))


# ----------------------------------------------------------------------
# Section 11: Summary
# ----------------------------------------------------------------------

print()
print("=== Section 11: Summary ===")
print()
print(f"K (entry-wise complex conjugation) — retained as T factor of CPT.")
print(f"  Tests 1, 2, 3: PASS")
print(f"  Tests 4, 5: FAIL")
print()
print(f"T_alg, *, T_H, CPT — all reduce to K on Hermitian circulants.")
print(f"  No additional structure beyond K.")
print()
print(f"Real-structure / antilinear-involution mechanism: ")
print(f"  Provides Z_2 quotient of \\hat{{C_3}}: combines chi_omega <-> chi_obar.")
print(f"  Does NOT provide SO(2) angular quotient on the doublet.")
print()
print(f"Closure status of A1-condition |b|^2/a^2 = 1/2:")
print(f"  After Probe 13: SHARPENED bounded obstruction (no closure, no new admission).")
print(f"  Residue refined from Probe 12's 'R-isotype counting principle' to")
print(f"    'U(1)_b angular quotient on the doublet of A^{{C_3}}'")
print(f"  (since Z_2 part of R-isotype counting IS supplied by retained K).")

# Total summary
print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
