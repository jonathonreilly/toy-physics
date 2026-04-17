#!/usr/bin/env python3
"""
CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM: Cube-Shift Joint Eigenvalue Structure on C^8

Framework object:
  The three cube-shift operators on the taste cube C^8 = (C^2)^⊗3:
    S_1 = sigma_x ⊗ I ⊗ I
    S_2 = I ⊗ sigma_x ⊗ I
    S_3 = I ⊗ I ⊗ sigma_x

Theorem (CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM):
  (i)   S_1, S_2, S_3 are Hermitian and involutive (S_i² = I).
  (ii)  They pairwise commute: [S_i, S_j] = 0.
  (iii) They admit a simultaneous eigenbasis on C^8 consisting of 8
        one-dimensional joint eigenspaces, each labeled by
        s = (s_1, s_2, s_3) ∈ {+1, -1}³.
  (iv)  The joint eigenstate with signs (s_1, s_2, s_3) is explicitly
        |ψ_s⟩ = (1/√8) Σ_{a ∈ {0,1}³} (∏_μ s_μ^{a_μ}) |a⟩
        i.e. a specific superposition of the 8 computational-basis
        states |a_1 a_2 a_3⟩.

Proof method:
  Pure linear algebra. Each step is a direct computation on explicit
  8x8 matrices and 8-dim vectors.

Reusability:
  (i) and (ii) are standing properties used in V_sel derivation and
  elsewhere. (iii) and (iv) provide the canonical basis translation
  between the "computational" basis |a⟩ (staggered cube sites) and
  the "momentum" basis |X_s⟩ (BZ corners). This basis translation is
  cited anywhere a hw=k sector is mentioned.

No structural identifications. No imports. Pure math.
"""

from __future__ import annotations

import itertools
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
# Setup: the three cube-shift operators
# ============================================================================

def build_cube_shifts() -> tuple:
    """Construct S_1, S_2, S_3 as 8x8 real matrices."""
    sigma_x = np.array([[0, 1], [1, 0]], dtype=float)
    I2 = np.eye(2, dtype=float)

    S_1 = np.kron(np.kron(sigma_x, I2), I2)
    S_2 = np.kron(np.kron(I2, sigma_x), I2)
    S_3 = np.kron(np.kron(I2, I2), sigma_x)

    return S_1, S_2, S_3


# ============================================================================
# Part 1: S_i are Hermitian and involutive
# ============================================================================

def part1_hermitian_involutive() -> None:
    print("\n" + "=" * 72)
    print("PART 1: S_i are Hermitian and involutive")
    print("=" * 72)

    S_1, S_2, S_3 = build_cube_shifts()
    ops = {"S_1": S_1, "S_2": S_2, "S_3": S_3}

    for name, S in ops.items():
        check(f"{name} is Hermitian (S = S†)",
              np.allclose(S, S.T))
        check(f"{name}² = I (involutive)",
              np.allclose(S @ S, np.eye(8)))

    print("\n  Proof:")
    print("  Each S_i is a tensor product of two I's and one sigma_x.")
    print("  sigma_x is Hermitian (sigma_x = sigma_x^T) and sigma_x² = I.")
    print("  Tensor products preserve both properties.")


# ============================================================================
# Part 2: Pairwise commutativity
# ============================================================================

def part2_commutativity() -> None:
    print("\n" + "=" * 72)
    print("PART 2: [S_i, S_j] = 0 for all i, j")
    print("=" * 72)

    S_1, S_2, S_3 = build_cube_shifts()
    ops = [(1, S_1), (2, S_2), (3, S_3)]

    for (i, A), (j, B) in itertools.combinations(ops, 2):
        comm = A @ B - B @ A
        check(f"[S_{i}, S_{j}] = 0",
              np.allclose(comm, 0),
              f"max|comm| = {np.max(np.abs(comm)):.2e}")

    print("\n  Proof:")
    print("  [S_1, S_2] = [sigma_x⊗I⊗I, I⊗sigma_x⊗I]")
    print("             = (sigma_x·I) ⊗ (I·sigma_x) ⊗ (I·I)")
    print("             − (I·sigma_x) ⊗ (sigma_x·I) ⊗ (I·I)")
    print("             = 0")
    print("  (sigma_x and I commute trivially in each tensor factor)")


# ============================================================================
# Part 3: Joint eigenspaces — 8 one-dimensional eigenspaces
# ============================================================================

def joint_eigenstate(s: tuple) -> np.ndarray:
    """
    Construct the joint eigenstate of S_1, S_2, S_3 with joint eigenvalue
    (s_1, s_2, s_3). The explicit formula:
      |ψ_s⟩ = (1/√8) Σ_{a ∈ {0,1}³} (∏_μ s_μ^{a_μ}) |a⟩
    where |a⟩ = |a_1 a_2 a_3⟩ is the computational basis.
    """
    psi = np.zeros(8, dtype=float)
    for a1, a2, a3 in itertools.product([0, 1], repeat=3):
        idx = a1 * 4 + a2 * 2 + a3
        phase = (s[0] ** a1) * (s[1] ** a2) * (s[2] ** a3)
        psi[idx] = phase
    return psi / np.sqrt(8)


def part3_joint_eigenspaces() -> None:
    print("\n" + "=" * 72)
    print("PART 3: Joint eigenspace structure — 8 one-dim eigenspaces")
    print("=" * 72)

    S_1, S_2, S_3 = build_cube_shifts()

    # Enumerate all 8 sign triples
    all_signs = list(itertools.product([+1, -1], repeat=3))

    # Build all 8 joint eigenstates
    eigenstates = [joint_eigenstate(s) for s in all_signs]

    # Verify each is a unit vector
    for s, psi in zip(all_signs, eigenstates):
        norm_sq = psi @ psi
        check(f"|ψ_{s}| = 1",
              abs(norm_sq - 1.0) < 1e-14,
              f"|ψ|² = {norm_sq}")

    # Verify joint eigenvalues
    print("\n  Joint eigenvalue verification:")
    for s, psi in zip(all_signs, eigenstates):
        S_psi = (S_1 @ psi, S_2 @ psi, S_3 @ psi)
        eigs = []
        for i, Spsi in enumerate(S_psi):
            # Eigenvalue = <psi | S | psi> / <psi | psi>
            eig = psi @ Spsi
            eigs.append(eig)
            check(f"  S_{i+1} |ψ_{s}⟩ = {s[i]} |ψ_{s}⟩",
                  np.allclose(Spsi, s[i] * psi),
                  f"eig = {eig:+.1f}")

    # Verify mutual orthonormality
    print("\n  Orthonormality of the 8 joint eigenstates:")
    gram = np.array([[psi_i @ psi_j for psi_j in eigenstates]
                     for psi_i in eigenstates])
    check("Gram matrix is identity (orthonormal basis)",
          np.allclose(gram, np.eye(8), atol=1e-12),
          f"max off-diag = {np.max(np.abs(gram - np.eye(8))):.2e}")

    # Verify each eigenspace is one-dimensional
    # (The 8 distinct sign triples partition C^8 into 8 one-dim eigenspaces)
    print("\n  The 8 sign triples s ∈ {±1}³ give distinct joint eigenstates,")
    print("  each one-dimensional, collectively spanning C^8.")

    # Completeness: the eigenstates form a basis
    E = np.stack(eigenstates, axis=1)  # columns are eigenstates
    check("Eigenstate matrix E is unitary (orthonormal basis of C^8)",
          np.allclose(E @ E.T, np.eye(8)),
          f"E E^T − I max = {np.max(np.abs(E @ E.T - np.eye(8))):.2e}")


# ============================================================================
# Part 4: Explicit basis translation formula
# ============================================================================

def part4_basis_translation() -> None:
    """
    Verify the explicit basis translation formula:
      |ψ_s⟩ = (1/√8) Σ_a (∏_μ s_μ^{a_μ}) |a⟩

    This is the discrete Fourier transform on Z_2³ (the Hadamard transform),
    with characters χ_s(a) = ∏_μ s_μ^{a_μ}.
    """
    print("\n" + "=" * 72)
    print("PART 4: Basis translation via Z_2³ characters (Hadamard transform)")
    print("=" * 72)

    S_1, S_2, S_3 = build_cube_shifts()
    all_signs = list(itertools.product([+1, -1], repeat=3))
    all_a = list(itertools.product([0, 1], repeat=3))

    # Inverse transform: express |a⟩ in terms of |ψ_s⟩
    # |a⟩ = (1/√8) Σ_s (∏_μ s_μ^{a_μ}) |ψ_s⟩
    # This follows by orthonormality of characters

    print("\n  Forward transform: |ψ_s⟩ = (1/√8) Σ_a χ_s(a) |a⟩")
    print("  where χ_s(a) = ∏_μ s_μ^{a_μ} are Z_2³ characters.")

    for s in all_signs:
        psi = joint_eigenstate(s)
        for μ in range(3):
            S_op = [S_1, S_2, S_3][μ]
            check(f"  S_{μ+1} |ψ_{s}⟩ = {s[μ]} |ψ_{s}⟩",
                  np.allclose(S_op @ psi, s[μ] * psi))

    # Character orthogonality: Σ_a χ_s(a) χ_{s'}(a) = 8 δ_{s,s'}
    print("\n  Character orthogonality (Z_2³ Peter-Weyl):")
    for s in all_signs:
        for sp in all_signs:
            total = 0
            for a in all_a:
                chi_s = np.prod([s[μ]**a[μ] for μ in range(3)])
                chi_sp = np.prod([sp[μ]**a[μ] for μ in range(3)])
                total += chi_s * chi_sp
            expected = 8 if s == sp else 0
            assert total == expected, f"Character orthogonality fails for s={s}, s'={sp}: got {total}"

    check("Z_2³ character orthogonality Σ_a χ_s(a) χ_{s'}(a) = 8 δ_{s,s'}",
          True,
          "verified over all 8x8 pairs")

    # Completeness: Σ_s χ_s(a) χ_s(b) = 8 δ_{a,b}
    for a in all_a:
        for b in all_a:
            total = 0
            for s in all_signs:
                chi_sa = np.prod([s[μ]**a[μ] for μ in range(3)])
                chi_sb = np.prod([s[μ]**b[μ] for μ in range(3)])
                total += chi_sa * chi_sb
            expected = 8 if a == b else 0
            assert total == expected

    check("Z_2³ character completeness Σ_s χ_s(a) χ_s(b) = 8 δ_{a,b}",
          True,
          "verified over all 8x8 pairs")

    print("\n  Both relations hold identically. Proof: discrete Fourier on Z_2³.")
    print("  Each character χ_s(a) = ∏_μ s_μ^{a_μ} factors as a product of")
    print("  Z_2 characters, each orthonormal in Z_2.")


# ============================================================================
# Part 5: Theorem statement (for reuse in downstream notes)
# ============================================================================

def part5_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 5: CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM formal statement")
    print("=" * 72)

    print("""
  THEOREM (CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM, Cube-Shift Joint Eigenvalue Structure).
  Let S_1, S_2, S_3 be the three cube-shift operators on C^8 = (C^2)^⊗3
  defined by S_μ = tensor product of three factors, with σ_x in position
  μ and I in the other two positions.

  Then:

  (1) Each S_μ is Hermitian and S_μ² = I. Eigenvalues are ±1.

  (2) [S_i, S_j] = 0 for all i, j.

  (3) The three operators admit a simultaneous eigenbasis on C^8
      consisting of 8 one-dimensional joint eigenspaces. The joint
      eigenstate with eigenvalue triple (s_1, s_2, s_3) ∈ {±1}³ is:

         |ψ_s⟩ = (1/√8) Σ_{a ∈ {0,1}³} (∏_μ s_μ^{a_μ}) |a_1 a_2 a_3⟩

  (4) The 8 joint eigenstates {|ψ_s⟩ : s ∈ {±1}³} form an orthonormal
      basis of C^8 (the Z_2³ character / Hadamard transform of the
      computational basis).

  PROOF. (1) from tensor structure: each S_μ = I ⊗ σ_x ⊗ I (up to
  positioning), σ_x is Hermitian and idempotent squared to I.
  (2) from commutativity of tensor factors acting on disjoint subsystems.
  (3) from joint diagonalization of commuting Hermitian operators +
  explicit construction via Z_2³ characters.
  (4) from character orthogonality for the abelian group Z_2³.

  QED.

  REUSABILITY. This lemma is cited whenever the following appears
  in a downstream derivation:
  - joint-eigenbasis parameterization of C^8 (taste cube)
  - translation between computational basis |a⟩ and momentum basis |ψ_s⟩
  - explicit formulas for BZ corner states on Z_L³ (L even) via the
    restriction of |ψ_s⟩ to a lattice of L^3 sites
  - character theory on Z_2³ = taste-cube symmetry group
""")


def main() -> int:
    print("=" * 72)
    print("  CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM: Cube-Shift Joint Eigenvalue Structure on C^8")
    print("=" * 72)

    part1_hermitian_involutive()
    part2_commutativity()
    part3_joint_eigenspaces()
    part4_basis_translation()
    part5_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
