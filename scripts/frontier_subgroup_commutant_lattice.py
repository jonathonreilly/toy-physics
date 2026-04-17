#!/usr/bin/env python3
"""
Subgroup-Commutant Dimension Lattice on C^8

Classical math applied:
  - Subgroup lattice of S_3 (standard group theory; S_3 has five
    subgroups: {e}, three Z_2 transpositions, Z_3, and S_3 itself —
    see e.g. Dummit–Foote, "Abstract Algebra", §3.2).
  - Schur's lemma (Schur 1905) for the commutant dimension
    dim End(V)^H = Σ_i m_i² where m_i are the isotypic
    multiplicities of V as an H-representation.
  - Inclusion-reversing nature of subgroup-to-commutant map:
    H ⊆ K  ⟹  End(V)^K ⊆ End(V)^H, hence dim non-decreasing as H
    shrinks.
  - Character theory of finite groups for isotypic-multiplicity
    counting (Frobenius 1896; Serre, "Linear Representations of
    Finite Groups", ch. 2).

Framework object:
  The taste cube C^8 = (C²)^⊗³ with the S_3 axis-permutation action,
  together with each subgroup H ⊆ S_3 and the induced action on C^8.

Theorem (subgroup-commutant dimension lattice):
  For each subgroup H ⊆ S_3, the complex dimension of the H-invariant
  operator commutant dim End(C^8)^H is:

         H                         dim End(C^8)^H
       ─────────────────────────────────────────
         S_3          (order 6)          20     (Batch 3)
         Z_3 = ⟨(123)⟩  (order 3)         24     (Batch 6 T1)
         Z_2^{(ij)}    (order 2, × 3)     40     (Batch 5, T1 for one)
         {e}          (order 1)           64     (trivially End(C^8))

  The lattice is order-reversing with respect to subgroup inclusion:
  H ⊆ K  ⟹  End(V)^K ⊆ End(V)^H, with equality exactly when V
  carries a trivial H-action on its K-irrep content relative to
  H-irrep content.  The gaps in the chain

     20  ⊂  24  ⊂  40  ⊂  64

  are 4, 16, 24 — non-trivial jumps that reflect which H-irreps
  become reducible when restricting from a larger subgroup to a
  smaller one.

Proof method: direct commutator-kernel computation at each subgroup
level, together with the isotypic-multiplicity formula cross-check.

Applied rather than invented:
  The subgroup lattice of S_3, Schur's lemma, and character theory
  are all textbook.  We compile the specific dimension table for
  C^8 with the S_3 axis-permutation action — an instance of the
  standard "subgroup restriction + commutant dimension" calculation.

Reusability:
  - Single citable table for any framework argument that invokes a
    specific subgroup of S_3 (e.g. Z_2 residual after SSB, Z_3 for
    phase analysis, or the full S_3 for unbroken-symmetric analysis).
  - Establishes the monotonicity "as we break more symmetry, we gain
    more invariant-operator freedom" in quantitative form.
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


# ---------------------------------------------------------------------------
# Axis permutation on C^8
# ---------------------------------------------------------------------------

def axis_permutation(perm: tuple) -> np.ndarray:
    U = np.zeros((8, 8), dtype=complex)
    for a in itertools.product([0, 1], repeat=3):
        src = a[0] * 4 + a[1] * 2 + a[2]
        new_a = [0, 0, 0]
        for i in range(3):
            new_a[perm[i]] = a[i]
        dst = new_a[0] * 4 + new_a[1] * 2 + new_a[2]
        U[dst, src] = 1.0
    return U


# ---------------------------------------------------------------------------
# Subgroup enumeration
# ---------------------------------------------------------------------------

# Identify permutation perms for all S_3 elements:
ALL_PERMS = [
    ((0, 1, 2), "e"),
    ((1, 0, 2), "(12)"),   # axis swap 1 <-> 2
    ((0, 2, 1), "(23)"),   # axis swap 2 <-> 3
    ((2, 1, 0), "(13)"),   # axis swap 1 <-> 3
    ((1, 2, 0), "(123)"),
    ((2, 0, 1), "(132)"),
]

SUBGROUPS = {
    "S_3": [p for p, _ in ALL_PERMS],                             # order 6
    "Z_3 = <(123)>": [(0, 1, 2), (1, 2, 0), (2, 0, 1)],           # order 3
    "Z_2 = <(12)>": [(0, 1, 2), (1, 0, 2)],                       # order 2
    "Z_2 = <(23)>": [(0, 1, 2), (0, 2, 1)],                       # order 2
    "Z_2 = <(13)>": [(0, 1, 2), (2, 1, 0)],                       # order 2
    "{e}": [(0, 1, 2)],                                            # order 1
}


# ---------------------------------------------------------------------------
# Commutant dim via kernel of commutator map
# ---------------------------------------------------------------------------

def commutant_dim(generators: list) -> int:
    """dim_C End(C^8)^H given generator unitaries of H."""
    if len(generators) == 0:
        return 64
    n = 8
    bases = []
    for j in range(n):
        for k in range(n):
            M = np.zeros((n, n), dtype=complex)
            M[j, k] = 1.0
            bases.append(M)
    C_mats = []
    for g in generators:
        Cg = np.stack([(g @ M - M @ g).reshape(n * n) for M in bases], axis=1)
        C_mats.append(Cg)
    C = np.vstack(C_mats)
    rank = np.linalg.matrix_rank(C, tol=1e-10)
    return n * n - rank


# ---------------------------------------------------------------------------
# Part 1: Dimension table for each subgroup
# ---------------------------------------------------------------------------

def part1_dim_table() -> dict:
    print("\n" + "=" * 72)
    print("PART 1: dim End(C^8)^H for each subgroup H ⊆ S_3")
    print("        (applies Schur's lemma + commutator-kernel computation)")
    print("=" * 72)

    dims = {}

    expectations = {
        "S_3": 20,
        "Z_3 = <(123)>": 24,
        "Z_2 = <(12)>": 40,
        "Z_2 = <(23)>": 40,
        "Z_2 = <(13)>": 40,
        "{e}": 64,
    }

    for name, perms in SUBGROUPS.items():
        gens = [axis_permutation(p) for p in perms]
        # For the subgroup of order n, use one or two generators (enough to
        # generate H).  For S_3, need (12) and (123).  For Z_n cyclic, one.
        if name == "S_3":
            # τ = (12) and σ = (123) generate S_3
            gens = [axis_permutation((1, 0, 2)), axis_permutation((1, 2, 0))]
        elif name.startswith("Z_3"):
            gens = [axis_permutation((1, 2, 0))]
        elif name.startswith("Z_2"):
            # Single transposition generator
            non_id_perms = [p for p in perms if p != (0, 1, 2)]
            gens = [axis_permutation(non_id_perms[0])]
        elif name == "{e}":
            gens = []
        d = commutant_dim(gens)
        dims[name] = d
        expected = expectations[name]
        print(f"  {name:20s}  dim End(C^8)^H = {d:3d}   (expected {expected})")
        check(f"{name} commutant dim matches expected {expected}",
              d == expected)

    return dims


# ---------------------------------------------------------------------------
# Part 2: Monotonicity — H ⊆ K gives dim End(V)^K ≤ dim End(V)^H
# ---------------------------------------------------------------------------

def part2_monotonicity(dims: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Subgroup-inclusion reversed by commutant-dimension")
    print("=" * 72)

    # Subgroup chain: {e} ⊂ Z_2 ⊂ S_3,  {e} ⊂ Z_3 ⊂ S_3.
    # Check: monotone decreasing dim as subgroup grows.
    chains = [
        ("{e} ⊂ Z_2 = <(12)> ⊂ S_3", ["{e}", "Z_2 = <(12)>", "S_3"]),
        ("{e} ⊂ Z_3 = <(123)> ⊂ S_3", ["{e}", "Z_3 = <(123)>", "S_3"]),
    ]
    for label, chain in chains:
        vals = [dims[h] for h in chain]
        print(f"  {label}: dims = {vals}")
        monotone = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
        check(f"Monotone decreasing along {label}", monotone)

    # Sanity: three Z_2's are all conjugate in S_3, so same dim
    z2_dims = {n: dims[n] for n in dims if n.startswith("Z_2")}
    all_equal = len(set(z2_dims.values())) == 1
    check("All three Z_2 subgroups give dim = 40  (conjugate in S_3)",
          all_equal)


# ---------------------------------------------------------------------------
# Part 3: Isotypic cross-check via character tables
# ---------------------------------------------------------------------------

def part3_isotypic_crosscheck(dims: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Isotypic-multiplicity cross-check (Schur's lemma)")
    print("=" * 72)

    # Known decompositions:
    #   S_3: C^8 = 4·A_1 ⊕ 0·A_2 ⊕ 2·E       → 4² + 0² + 2² = 20
    #   Z_3: C^8 = 4·1 ⊕ 2·χ_ω ⊕ 2·χ_{ω²}     → 4² + 2² + 2² = 24
    #   Z_2: C^8 = 6·1 ⊕ 2·sgn                → 6² + 2² = 40
    #   {e}: C^8 = 8·1                         → 8² = 64

    predictions = {
        "S_3": (4**2 + 0**2 + 2**2, "4·A_1 + 0·A_2 + 2·E"),
        "Z_3 = <(123)>": (4**2 + 2**2 + 2**2, "4·1 + 2·χ_ω + 2·χ_{ω²}"),
        "Z_2 = <(12)>": (6**2 + 2**2, "6·1 + 2·sgn"),
        "{e}": (8**2, "8·1"),
    }

    for name, (pred, decomp) in predictions.items():
        print(f"  {name:20s}  decomp = {decomp}")
        print(f"    {'':20s}  Schur sum Σ m_i² = {pred}")
        check(f"Schur prediction {pred} matches computed {dims[name]} for {name}",
              dims[name] == pred)


# ---------------------------------------------------------------------------
# Part 4: Theorem statement
# ---------------------------------------------------------------------------

def part4_theorem(dims: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Subgroup-Commutant Dimension Lattice (statement)")
    print("=" * 72)

    print("""
  THEOREM (Subgroup-Commutant Dimension Lattice on C^8).  Let
  C^8 = (C²)^⊗³ carry the S_3 axis-permutation action.  For each
  subgroup H ⊆ S_3, the complex dimension of the H-invariant
  operator commutant is given by

         H                    |H|    dim End(C^8)^H    Decomposition
       ─────────────────────────────────────────────────────────────
         S_3                   6          20            4·A_1 + 2·E
         Z_3 = ⟨(123)⟩          3          24            4·1 + 2·χ_ω + 2·χ_{ω²}
         Z_2 = ⟨(ij)⟩  (×3)     2          40            6·1 + 2·sgn
         {e}                    1          64            8·1

  The three Z_2 subgroups (generated by the three transpositions) are
  conjugate in S_3 and give the same commutant dimension.

  The lattice is inclusion-reversing: for H ⊆ K,
     End(C^8)^K  ⊆  End(C^8)^H  ⟹  dim End(C^8)^K  ≤  dim End(C^8)^H.
  Along the two maximal chains {e} ⊂ Z_2 ⊂ S_3 and {e} ⊂ Z_3 ⊂ S_3,
  the dimensions are

     64  >  40  >  20    and    64  >  24  >  20,

  with gaps 24, 20 and 40, 4 respectively reflecting which H-irreps
  become reducible upon restriction.

  CLASSICAL RESULTS USED.
  - Subgroup lattice of S_3 (standard finite-group theory; Dummit–
    Foote, *Abstract Algebra*, §3.2).  S_3 has exactly five
    subgroups: the trivial {e}, three conjugate Z_2's (the
    transpositions), the unique Z_3, and S_3 itself.
  - Schur's lemma (Schur 1905): dim End(V)^H = Σ m_i².
  - Character theory of finite groups (Frobenius 1896; Serre ch. 2)
    for the isotypic-multiplicity counts.
  - Inclusion-reversing property of the subgroup → commutant map
    (standard).

  FRAMEWORK-SPECIFIC STEP.
  - Compiling the specific commutant dimensions for C^8 = (C²)^⊗³
    under each S_3 subgroup, using the Batch 2 S_3 decomposition
    (4·A_1 + 2·E) and the Batch 5/6 Z_2/Z_3 decompositions.

  PROOF.  For each subgroup H, compute dim End(C^8)^H via either
  (a) Schur's lemma using the known isotypic decomposition under H,
  or (b) direct kernel of the commutator map [g, ·] for a generating
  set of H.  Both methods agree on all four subgroups (inclusive of
  the three conjugate Z_2's giving the same dim 40).  The monotone
  decreasing behavior along chains is a direct consequence of
  End(V)^K ⊆ End(V)^H for H ⊆ K.  QED.

  REUSABILITY.
  - Single reference table for any framework argument that invokes
    a specific subgroup of S_3 acting on the taste cube.
  - Quantifies the "invariant-operator relief" gained by breaking
    symmetry: 20 (full S_3) → 24 (keep Z_3 only) → 40 (keep one
    Z_2) → 64 (no symmetry).  Guides which subgroup corresponds to
    which physical SSB scenario.
""")


def main() -> int:
    print("=" * 72)
    print("  Subgroup-Commutant Dimension Lattice on C^8")
    print("=" * 72)

    dims = part1_dim_table()
    part2_monotonicity(dims)
    part3_isotypic_crosscheck(dims)
    part4_theorem(dims)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
