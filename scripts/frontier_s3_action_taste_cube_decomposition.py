#!/usr/bin/env python3
"""
S₃ Axis-Permutation Action on the Taste Cube: Orbit and Irrep Decomposition

Framework objects:
  - Taste cube C^8 = (C²)⊗³ with computational basis |α⟩
  - The symmetric group S_3 acting by permutations of tensor positions
    (equivalently, permutations of the three axes x, y, z).

  For each π ∈ S_3, the unitary U(π) on C^8 is defined by
    U(π) |α_1 α_2 α_3⟩ = |α_{π⁻¹(1)} α_{π⁻¹(2)} α_{π⁻¹(3)}⟩.

Theorem:
  (i)   π ↦ U(π) is a unitary representation of S_3 on C^8.
  (ii)  S_3 preserves Hamming weight: the orbit decomposition on the
        computational basis is 1 + 3 + 3 + 1 (the four Hamming-weight
        sectors).
  (iii) Under S_3, the 1-dim sectors (hw=0, hw=3) carry the trivial
        representation A_1. The two 3-dim sectors (hw=1, hw=2) carry
        the standard permutation representation of S_3 on {1,2,3},
        which decomposes as A_1 ⊕ E (trivial + 2-dim "standard" irrep).
  (iv)  Therefore as an S_3 representation,
           C^8 ≅ 4·A_1 + 2·E
        (4 trivial copies, 2 copies of the 2-dim standard irrep).
  (v)   In particular, C^8 contains NO copy of the sign representation A_2.

Proof method:
  Direct computation of characters on the 3 conjugacy classes of S_3
  (identity, 2-cycles, 3-cycles) + Peter-Weyl orthogonality.

Reusability:
  - Characterizes which operators on C^8 can be S_3-invariant
  - Provides the irrep projector algebra for block-decomposing
    S_3-symmetric operators
  - Generalizes the "axis symmetry" arguments referenced throughout
    the main repo to an explicit representation-theoretic statement
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
# Constructing S_3 unitaries on C^8
# ============================================================================

def basis_index(alpha: tuple) -> int:
    return alpha[0] * 4 + alpha[1] * 2 + alpha[2]


# S_3 elements as permutations of {0,1,2} (0-indexed axes)
# Conjugacy classes:
#   identity: (0,1,2)
#   2-cycles: (1,0,2), (0,2,1), (2,1,0)
#   3-cycles: (1,2,0), (2,0,1)

S3_elements = {
    "e":       (0, 1, 2),
    "(12)":    (1, 0, 2),   # swap axes 1 and 2
    "(23)":    (0, 2, 1),   # swap axes 2 and 3
    "(13)":    (2, 1, 0),   # swap axes 1 and 3
    "(123)":   (1, 2, 0),   # cycle 1→2→3→1
    "(132)":   (2, 0, 1),   # cycle 1→3→2→1
}


def build_S3_unitary(perm: tuple) -> np.ndarray:
    """
    For π ∈ S_3, build U(π) on C^8 such that
    U(π) |α_1 α_2 α_3⟩ = |α_{π⁻¹(1)} α_{π⁻¹(2)} α_{π⁻¹(3)}⟩.

    Equivalently, U(π) permutes the tensor positions.
    """
    # Inverse permutation for labels
    perm_inv = [0, 0, 0]
    for i, pi_i in enumerate(perm):
        perm_inv[pi_i] = i

    U = np.zeros((8, 8), dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        new_alpha = tuple(alpha[perm_inv[i]] for i in range(3))
        U[basis_index(new_alpha), basis_index(alpha)] = 1
    return U


# ============================================================================
# Part 1: S_3 group structure
# ============================================================================

def part1_group_structure() -> dict:
    print("\n" + "=" * 72)
    print("PART 1: S_3 unitary representation on C^8")
    print("=" * 72)

    Us = {name: build_S3_unitary(perm) for name, perm in S3_elements.items()}

    # Verify unitarity
    for name, U in Us.items():
        check(f"U({name}) is unitary",
              np.allclose(U @ U.conj().T, np.eye(8)))

    # Verify identity
    check("U(e) = I",
          np.allclose(Us["e"], np.eye(8)))

    # Verify order: 2-cycles have order 2
    for name in ["(12)", "(23)", "(13)"]:
        check(f"U({name})² = I (order 2)",
              np.allclose(Us[name] @ Us[name], np.eye(8)))

    # 3-cycles have order 3
    for name in ["(123)", "(132)"]:
        check(f"U({name})³ = I (order 3)",
              np.allclose(np.linalg.matrix_power(Us[name], 3), np.eye(8)))

    # Verify (123)·(12) = ... (well, any S_3 group relation)
    # (12)(23)(12) = (13) is a characteristic relation in S_3
    lhs = Us["(12)"] @ Us["(23)"] @ Us["(12)"]
    check("(12)(23)(12) = (13)",
          np.allclose(lhs, Us["(13)"]))

    return Us


# ============================================================================
# Part 2: Hamming-weight preservation and orbits
# ============================================================================

def part2_hw_orbits(Us: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 2: S_3 preserves Hamming weight; orbits = 1 + 3 + 3 + 1")
    print("=" * 72)

    # Each U(π) commutes with each hw-projector
    hw_projectors = [np.zeros((8, 8), dtype=complex) for _ in range(4)]
    for alpha in itertools.product([0, 1], repeat=3):
        hw = sum(alpha)
        idx = basis_index(alpha)
        hw_projectors[hw][idx, idx] = 1.0

    for name, U in Us.items():
        for hw in range(4):
            comm = U @ hw_projectors[hw] - hw_projectors[hw] @ U
            check(f"[U({name}), P_hw={hw}] = 0",
                  np.allclose(comm, 0))

    # Compute orbits of S_3 on {0,1}³
    all_alphas = list(itertools.product([0, 1], repeat=3))
    orbits = []
    visited = set()
    for alpha in all_alphas:
        if alpha in visited:
            continue
        orbit = set()
        for name, perm in S3_elements.items():
            perm_inv = [0, 0, 0]
            for i, pi_i in enumerate(perm):
                perm_inv[pi_i] = i
            permuted = tuple(alpha[perm_inv[i]] for i in range(3))
            orbit.add(permuted)
        orbits.append(sorted(orbit))
        visited.update(orbit)

    print("\n  S_3 orbits on {0,1}³:")
    for o in orbits:
        hw = sum(o[0])
        print(f"    hw={hw}, size={len(o)}: {o}")

    orbit_sizes = sorted([len(o) for o in orbits])
    check("Orbit sizes are {1, 1, 3, 3}",
          orbit_sizes == [1, 1, 3, 3],
          f"got {orbit_sizes}")


# ============================================================================
# Part 3: Character computation
# ============================================================================

def part3_characters(Us: dict) -> dict:
    print("\n" + "=" * 72)
    print("PART 3: Characters of the C^8 representation")
    print("=" * 72)

    # Character: χ(g) = Tr(U(g))
    chars = {name: np.real(np.trace(U)) for name, U in Us.items()}

    print("\n  Character χ(g) = Tr U(g) for each S_3 element:")
    for name, chi in chars.items():
        print(f"    χ({name}) = {chi:+.0f}")

    # Group by conjugacy class
    # Identity: {e}
    # 2-cycles: {(12), (23), (13)}
    # 3-cycles: {(123), (132)}
    chi_e = chars["e"]
    chi_2cycle = chars["(12)"]
    chi_3cycle = chars["(123)"]

    check("χ(e) = 8 (= dim C^8)",
          abs(chi_e - 8) < 1e-10)
    check("χ(2-cycles) are all equal",
          all(abs(chars[n] - chi_2cycle) < 1e-10 for n in ["(12)", "(23)", "(13)"]))
    check("χ(3-cycles) are all equal",
          all(abs(chars[n] - chi_3cycle) < 1e-10 for n in ["(123)", "(132)"]))

    print(f"\n  Class sums:")
    print(f"    χ(identity class) = {chi_e:+.0f}")
    print(f"    χ(2-cycle class)  = {chi_2cycle:+.0f}  (3 elements)")
    print(f"    χ(3-cycle class)  = {chi_3cycle:+.0f}  (2 elements)")

    return {"e": chi_e, "2c": chi_2cycle, "3c": chi_3cycle}


# ============================================================================
# Part 4: Irrep decomposition via Peter-Weyl
# ============================================================================

def part4_irrep_decomposition(chars: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Irrep decomposition of C^8 as S_3 representation")
    print("=" * 72)

    # S_3 character table:
    # class:     e    2-cycle  3-cycle
    # class size 1    3        2
    # A_1:       1    1        1
    # A_2:       1    -1       1
    # E:         2    0        -1

    char_table = {
        "A_1": {"e": 1, "2c": 1, "3c": 1},
        "A_2": {"e": 1, "2c": -1, "3c": 1},
        "E":   {"e": 2, "2c": 0, "3c": -1},
    }

    class_sizes = {"e": 1, "2c": 3, "3c": 2}
    group_order = 6

    print("\n  Multiplicities via ⟨χ, χ_irrep⟩:")
    multiplicities = {}
    for irrep, irrep_chars in char_table.items():
        # (1/|G|) Σ_class |class| · χ(class) · χ_irrep(class)*
        m = (1.0 / group_order) * sum(
            class_sizes[c] * chars[c] * irrep_chars[c]
            for c in ["e", "2c", "3c"]
        )
        multiplicities[irrep] = m
        print(f"    m({irrep}) = {m:.4f}")

    check("Multiplicity of A_1 is 4",
          abs(multiplicities["A_1"] - 4) < 1e-10,
          f"m(A_1) = {multiplicities['A_1']}")
    check("Multiplicity of A_2 is 0",
          abs(multiplicities["A_2"] - 0) < 1e-10,
          f"m(A_2) = {multiplicities['A_2']}")
    check("Multiplicity of E is 2",
          abs(multiplicities["E"] - 2) < 1e-10,
          f"m(E) = {multiplicities['E']}")

    total_dim = (multiplicities["A_1"] * 1 +
                 multiplicities["A_2"] * 1 +
                 multiplicities["E"] * 2)
    check(f"Total dimension 4·1 + 0·1 + 2·2 = {total_dim:.0f} = 8",
          abs(total_dim - 8) < 1e-10)

    print("\n  DECOMPOSITION: C^8 ≅ 4·A_1 ⊕ 2·E")
    print("  (The sign representation A_2 does NOT appear in C^8.)")


# ============================================================================
# Part 5: Explicit block decomposition per hw-sector
# ============================================================================

def part5_hw_sector_structure(Us: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 5: hw-sector decompositions under S_3")
    print("=" * 72)

    # Restrict Us to each hw-sector and decompose

    # hw=0: 1-dim, |000⟩
    # hw=3: 1-dim, |111⟩
    # Both trivially A_1

    # hw=1: 3-dim, {|100⟩, |010⟩, |001⟩}
    # hw=2: 3-dim, {|110⟩, |011⟩, |101⟩}

    # For each 3-dim sector, compute the character and verify
    # it's the standard permutation rep = A_1 + E

    print("\n  hw=1 sector: {|100⟩, |010⟩, |001⟩}")
    hw1_basis_alphas = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    hw1_indices = [basis_index(a) for a in hw1_basis_alphas]

    for name, U in Us.items():
        # Restrict U to hw=1 basis
        U_hw1 = np.zeros((3, 3), dtype=complex)
        for i in range(3):
            for j in range(3):
                U_hw1[i, j] = U[hw1_indices[i], hw1_indices[j]]
        chi_hw1 = np.real(np.trace(U_hw1))

        # Compare to standard perm rep character
        # For perm on 3 objects: χ(identity) = 3, χ(2-cycle) = 1, χ(3-cycle) = 0
        if name == "e":
            expected = 3
        elif name in ["(12)", "(23)", "(13)"]:
            expected = 1
        else:
            expected = 0
        check(f"    hw=1 character χ({name}) = {expected}",
              abs(chi_hw1 - expected) < 1e-10,
              f"got {chi_hw1}")

    print("\n  hw=2 sector: {|110⟩, |011⟩, |101⟩}")
    hw2_basis_alphas = [(1, 1, 0), (0, 1, 1), (1, 0, 1)]
    hw2_indices = [basis_index(a) for a in hw2_basis_alphas]

    for name, U in Us.items():
        U_hw2 = np.zeros((3, 3), dtype=complex)
        for i in range(3):
            for j in range(3):
                U_hw2[i, j] = U[hw2_indices[i], hw2_indices[j]]
        chi_hw2 = np.real(np.trace(U_hw2))
        if name == "e":
            expected = 3
        elif name in ["(12)", "(23)", "(13)"]:
            expected = 1
        else:
            expected = 0
        check(f"    hw=2 character χ({name}) = {expected}",
              abs(chi_hw2 - expected) < 1e-10,
              f"got {chi_hw2}")

    print("\n  Each 3-dim sector carries the standard permutation rep:")
    print("    3-dim perm rep of S_3 = A_1 ⊕ E")
    print("  Total hw contribution:")
    print("    hw=0 (1-dim): A_1")
    print("    hw=1 (3-dim): A_1 + E")
    print("    hw=2 (3-dim): A_1 + E")
    print("    hw=3 (1-dim): A_1")
    print("  Sum: 4·A_1 + 2·E  ✓ (consistent with Part 4)")


# ============================================================================
# Part 6: Theorem statement
# ============================================================================

def part6_theorem_statement() -> None:
    print("\n" + "=" * 72)
    print("PART 6: S₃ Decomposition Theorem")
    print("=" * 72)

    print("""
  THEOREM. Let C^8 = (C²)⊗³ carry the natural S_3 action by tensor-
  position permutations. Then:

  (1) The S_3 representation decomposes by Hamming weight as
         C^8 = C^8_{hw=0} ⊕ C^8_{hw=1} ⊕ C^8_{hw=2} ⊕ C^8_{hw=3}
      with dimensions 1 + 3 + 3 + 1.

  (2) On the 1-dim hw=0 and hw=3 sectors, S_3 acts trivially (A_1).

  (3) On each 3-dim sector (hw=1 and hw=2), S_3 acts as the standard
      permutation representation on 3 objects, which decomposes as
         3 = A_1 ⊕ E
      where A_1 is the trivial irrep and E is the 2-dim standard irrep.

  (4) As an S_3 representation:
         C^8 ≅ 4·A_1 ⊕ 2·E
      (4 trivial copies, 2 copies of E; the sign representation A_2
      does NOT appear).

  PROOF. (1) Hamming weight is S_3-invariant (permuting bit positions
  preserves the number of 1's). (2) A 1-dim rep of S_3 is either A_1
  or A_2; the sign is positive on Hamming-weight-preserving permutations
  of a single fixed label, so it's A_1. (3) The 3-element hw=1 and hw=2
  sectors are each a single S_3 orbit (acted on transitively), so S_3
  acts as the permutation rep on 3 points, which equals A_1 ⊕ E (standard
  result in finite-group representation theory). (4) Sum the irrep
  contributions across sectors, and verify via Peter-Weyl ⟨χ, χ_irrep⟩:
  m(A_1) = 4, m(A_2) = 0, m(E) = 2.

  QED.

  REUSABILITY. Cited wherever:
  - a framework statement invokes "S_3 axis-permutation symmetry" on
    the taste cube
  - operators are analyzed for S_3 invariance (e.g., V_sel = 4·A_1-valued
    invariant operators)
  - irrep projectors are needed to block-decompose S_3-symmetric
    computations
""")


def main() -> int:
    print("=" * 72)
    print("  S_3 Axis-Permutation Decomposition of the Taste Cube C^8")
    print("=" * 72)

    Us = part1_group_structure()
    part2_hw_orbits(Us)
    chars = part3_characters(Us)
    part4_irrep_decomposition(chars)
    part5_hw_sector_structure(Us)
    part6_theorem_statement()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
