#!/usr/bin/env python3
"""
SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM (composition): Site-Phase / Cube-Shift Intertwiner

Framework objects:
  - C^8 taste cube with cube-shift operators S_μ (see CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM)
  - C^{L³} periodic lattice with BZ corners |X_α⟩ (see TRANSLATION-EIGENVALUE THEOREM)
  - Site-phase operator P_μ on C^{L³}: (P_μ ψ)(x) = (−1)^{x_μ} ψ(x)

Theorem (SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM):
  The site-phase operator P_μ, when acting on the BZ-corner basis of
  C^{L³}, implements the same α-label permutation as the cube-shift
  S_μ on C^8:

     P_μ |X_α⟩ = |X_{α ⊕ e_μ}⟩

  Equivalently, under the isomorphism C^{L³}_{BZ-corners} ≅ C^8 via
  |X_α⟩ ↔ |α⟩, the site-phase P_μ corresponds exactly to the cube-shift
  S_μ on C^8.

Composition of:
  - CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM: S_μ as bit-flip on computational basis of C^8
  - TRANSLATION-EIGENVALUE THEOREM: |X_α⟩ as plane-wave state with label α ∈ {0,1}³ on Z_L³
  - HAMMING-DISTANCE SELECTION RULE: single-axis momentum transfer P_μ has specific matrix elements

Proof method:
  Direct plane-wave algebra.

Reusability:
  SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM provides the canonical bridge between abstract taste-cube
  results (C^8 arguments) and concrete lattice-level statements
  (C^{L³} arguments). Any downstream derivation that mixes the two
  pictures can cite SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM as the explicit isomorphism.

  In particular, the repo's THREE_GENERATION_OBSERVABLE_THEOREM_NOTE
  uses the restriction of this isomorphism to the hw=1 subspace.
  SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM is the full 8-dim statement.

No structural identifications. No imports. Pure math.
"""

from __future__ import annotations

import itertools
import math
import numpy as np

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


# ============================================================================
# Setup
# ============================================================================

def site_index(x: tuple, L: int) -> int:
    return ((x[0] % L) * L + (x[1] % L)) * L + (x[2] % L)


def bz_corner_state(alpha: tuple, L: int) -> np.ndarray:
    N = L ** 3
    psi = np.zeros(N, dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                phase = (-1) ** (alpha[0] * x1 + alpha[1] * x2 + alpha[2] * x3)
                psi[site_index((x1, x2, x3), L)] = phase
    return psi / math.sqrt(N)


def site_phase_operator(mu: int, L: int) -> np.ndarray:
    """Diagonal operator P_μ: (P_μ ψ)(x) = (−1)^{x_μ} ψ(x)."""
    N = L ** 3
    P = np.zeros((N, N), dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                x = (x1, x2, x3)
                P[site_index(x, L), site_index(x, L)] = (-1) ** x[mu]
    return P


def cube_shift(mu: int) -> np.ndarray:
    """Cube-shift S_μ on C^8 = σ_x in position μ, I elsewhere."""
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    factors = [I2, I2, I2]
    factors[mu] = sigma_x
    return np.kron(np.kron(factors[0], factors[1]), factors[2])


def cube_basis_vector(alpha: tuple) -> np.ndarray:
    """Computational basis vector |α⟩ in C^8."""
    idx = alpha[0] * 4 + alpha[1] * 2 + alpha[2]
    v = np.zeros(8, dtype=complex)
    v[idx] = 1
    return v


# ============================================================================
# Part 1: P_μ on BZ corners = cube-shift on α-labels
# ============================================================================

def part1_site_phase_on_bz_corners(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print(f"PART 1: P_μ |X_α⟩ = |X_{{α ⊕ e_μ}}⟩ on Z_{L}³")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))

    for mu in range(3):
        P_mu = site_phase_operator(mu, L)
        for alpha in alphas:
            psi_alpha = bz_corner_state(alpha, L)
            result = P_mu @ psi_alpha

            # Expected: |X_{α ⊕ e_μ}⟩
            alpha_flipped = list(alpha)
            alpha_flipped[mu] = 1 - alpha_flipped[mu]
            expected = bz_corner_state(tuple(alpha_flipped), L)

            check(f"  P_{mu+1} |X_{alpha}⟩ = |X_{tuple(alpha_flipped)}⟩",
                  np.allclose(result, expected, atol=1e-12),
                  f"|result - expected| max = {np.max(np.abs(result - expected)):.2e}")

    print("\n  Proof:")
    print("  (P_μ |X_α⟩)(x) = (−1)^{x_μ} · (1/√L³) (−1)^{α·x}")
    print("                 = (1/√L³) (−1)^{(α + e_μ)·x}")
    print("                 = |X_{α ⊕ e_μ}⟩(x)  (for α_μ ∈ {0,1})")


# ============================================================================
# Part 2: The isomorphism BZ-corners ≅ C^8 intertwines P_μ and S_μ
# ============================================================================

def part2_intertwiner(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print("PART 2: The map Φ: |X_α⟩ ↦ |α⟩ (C^8) intertwines P_μ and S_μ")
    print("=" * 72)

    # Build the map Φ as an 8 × L^3 matrix
    # Columns of Φ are the BZ corner states (in C^{L^3})
    # We can then check Φ^† P_μ Φ = S_μ on C^8

    alphas = list(itertools.product([0, 1], repeat=3))

    # Construct a matrix whose columns are |X_α⟩ for α in canonical order
    N = L ** 3
    Phi = np.zeros((N, 8), dtype=complex)  # columns are |X_α⟩ in C^{L³}
    for i, alpha in enumerate(alphas):
        Phi[:, i] = bz_corner_state(alpha, L)

    # Check that Φ is an isometry: Φ^† Φ = I_8
    check("Φ† Φ = I_8 (BZ corners are orthonormal in C^{L³})",
          np.allclose(Phi.conj().T @ Phi, np.eye(8), atol=1e-12),
          f"max|Φ†Φ - I| = {np.max(np.abs(Phi.conj().T @ Phi - np.eye(8))):.2e}")

    # For each μ, check that Φ^† P_μ Φ on C^8 = S_μ
    for mu in range(3):
        P_mu_lattice = site_phase_operator(mu, L)
        S_mu_cube = cube_shift(mu)

        # Pull P_μ back to C^8 via Φ
        P_mu_pulled = Phi.conj().T @ P_mu_lattice @ Phi

        check(f"  Φ† P_{mu+1} Φ = S_{mu+1} on C^8",
              np.allclose(P_mu_pulled, S_mu_cube, atol=1e-12),
              f"max|diff| = {np.max(np.abs(P_mu_pulled - S_mu_cube)):.2e}")

    print("\n  Proof:")
    print("  Part 1 gives P_μ |X_α⟩ = |X_{α⊕e_μ}⟩.")
    print("  Under the isomorphism Φ: |X_α⟩ ↦ |α⟩ (computational basis of C^8),")
    print("  this becomes Φ P_μ Φ^(-1) |α⟩ = |α⊕e_μ⟩,")
    print("  which is exactly S_μ |α⟩ (see CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM).")
    print("  So Φ^† P_μ Φ = S_μ on the 8-dim BZ-corner subspace.")


# ============================================================================
# Part 3: Consequence — eigenvalue structure transfers
# ============================================================================

def part3_eigenvalue_transfer(L: int = 4) -> None:
    """
    Because P_μ and S_μ are intertwined by Φ, all spectral properties of
    S_μ (CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM) transfer to P_μ on the BZ-corner subspace. In particular:
    - P_μ has eigenvalues ±1 on BZ-corner subspace
    - Joint eigenstates of {P_1, P_2, P_3} on the BZ-corner subspace
      correspond to the CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM Hadamard basis.

    Explicit construction: the joint P_μ eigenstate with eigenvalue triple
    (s_1, s_2, s_3) ∈ {±1}³ on the BZ-corner subspace is
       |ψ_s^lattice⟩ = (1/√8) Σ_α (∏_μ s_μ^{α_μ}) |X_α⟩
    """
    print("\n" + "=" * 72)
    print("PART 3: Spectral transfer — joint P_μ eigenstates on BZ-corner subspace")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))

    for s in itertools.product([+1, -1], repeat=3):
        # Build the joint eigenstate as specified
        psi_s = np.zeros(L**3, dtype=complex)
        for alpha in alphas:
            chi = np.prod([s[μ] ** alpha[μ] for μ in range(3)])
            psi_s += chi * bz_corner_state(alpha, L)
        psi_s /= math.sqrt(8)

        # Verify normalization
        norm_sq = np.real(np.vdot(psi_s, psi_s))
        check(f"  ψ_{s}^lattice has norm 1",
              abs(norm_sq - 1.0) < 1e-12,
              f"|ψ|² = {norm_sq:.6f}")

        # Verify eigenvalue condition
        for mu in range(3):
            P_mu = site_phase_operator(mu, L)
            P_psi = P_mu @ psi_s
            expected = s[mu] * psi_s
            check(f"    P_{mu+1} ψ_{s}^lattice = {s[mu]:+d} ψ_{s}^lattice",
                  np.allclose(P_psi, expected, atol=1e-12))

    print("\n  Proof (via SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM intertwiner):")
    print("  The isomorphism Φ intertwines P_μ and S_μ.")
    print("  So joint P_μ eigenstates on BZ-corner subspace of C^{L³}")
    print("  are images under Φ^(-1) of joint S_μ eigenstates on C^8.")
    print("  CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM gives the S_μ eigenstates as Hadamard/Z_2³-character vectors.")


# ============================================================================
# Part 4: Theorem statement
# ============================================================================

def part4_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 4: SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM formal statement")
    print("=" * 72)

    print("""
  THEOREM (SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM, Site-Phase / Cube-Shift Intertwiner).
  Let Z_L³ (L even) be the periodic lattice, |X_α⟩ (α ∈ {0,1}³) the BZ
  corner states from TRANSLATION-EIGENVALUE THEOREM, and C^8 = (C²)⊗³ the taste cube with
  cube-shifts S_μ from CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM. Define the site-phase operator P_μ on
  C^{L³} by (P_μ ψ)(x) = (−1)^{x_μ} ψ(x).

  Let Φ: C^8 → C^{L³} be the linear isometry defined by Φ|α⟩ = |X_α⟩
  for α ∈ {0,1}³ (and arbitrarily extended, or viewed as an embedding
  of C^8 into C^{L³} onto the 8-dim BZ-corner subspace).

  Then:

  (1) P_μ |X_α⟩ = |X_{α ⊕ e_μ}⟩ (single bit flip in direction μ).

  (2) Φ intertwines P_μ and S_μ: on C^8, Φ^† P_μ Φ = S_μ.

  (3) Consequently, all spectral structure of S_μ on C^8 (CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM)
      transfers to P_μ on the BZ-corner subspace of C^{L³}.
      Explicitly, the joint eigenstate of {P_1, P_2, P_3} with
      eigenvalue triple (s_1, s_2, s_3) ∈ {±1}³ is:

         |ψ_s^lattice⟩ = (1/√8) Σ_α (∏_μ s_μ^{α_μ}) |X_α⟩

  PROOF. (1) by direct plane-wave computation: (−1)^{x_μ}·(−1)^{α·x} =
  (−1)^{(α+e_μ)·x}. (2) follows because CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM shows S_μ |α⟩ = |α ⊕ e_μ⟩
  in the computational basis, and Φ carries |α⟩ to |X_α⟩.
  (3) by intertwining: spectral properties preserved under unitary
  conjugation.

  QED.

  REUSABILITY. This is the CANONICAL BRIDGE between:
  - abstract taste-cube results stated on C^8 (e.g., V_sel selector
    derivation on the cube, S_3 symmetry of axes, cube-shift algebra)
  - concrete lattice-level statements on C^{L³} (e.g., BZ corner
    transitions, gauge-mediated taste changing, hw-sector dynamics)

  Any downstream derivation that bridges the two pictures can cite
  SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM to move freely between them.

  The repo's THREE_GENERATION_OBSERVABLE_THEOREM_NOTE restricts this
  bridge to the hw=1 triplet. SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM gives the full 8-dim version.
""")


def main() -> int:
    print("=" * 72)
    print("  SITE-PHASE / CUBE-SHIFT INTERTWINER THEOREM: Site-Phase / Cube-Shift Intertwiner")
    print("  (composition of CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM, B, C)")
    print("=" * 72)

    L = 4
    part1_site_phase_on_bz_corners(L)
    part2_intertwiner(L)
    part3_eigenvalue_transfer(L)
    part4_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
