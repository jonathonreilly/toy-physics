# Hamming-Weight Projector Algebra on C^8

**Status:** airtight (Grind Program, Batch 7)
**Runner:** `scripts/frontier_hw_projector_algebra.py` (54/54 PASS)

## Classical results applied

- **Spectral theorem for self-adjoint operators** and the resulting
  orthogonal-projector algebra (Reed–Simon, *Methods of Modern
  Mathematical Physics* vol. I, §VII.2).
- **Commuting-idempotents algebra**: for pairwise orthogonal
  projectors Π_0, …, Π_n summing to I, the span is an abelian
  unital *-algebra isomorphic to C^{n+1} under componentwise
  operations (Blackadar, *Operator Algebras*, §I.1).
- **S_3-equivariance of the Hamming-weight function** sum(α) on
  α ∈ {0,1}³ (combinatorial: hw is invariant under any permutation
  of the bits).

## Framework-specific step

Identification of the Hamming-weight operator H = Σ_μ (I − S_μ)/2
on C^8 = (C²)^⊗³. H is self-adjoint with eigenvalues 0, 1, 2, 3
and 1/3/3/1-dim eigenspaces, giving the four spectral projectors
Π_k onto the hw = k subspaces of the taste cube.

## Framework object

The four orthogonal projectors Π_0, Π_1, Π_2, Π_3 : C^8 → C^8,
projecting onto the Hamming-weight k subspaces V_k of the taste cube.

## Theorem

1. The four projectors satisfy

        Π_j · Π_k  =  δ_{jk} · Π_j,   Σ_k Π_k  =  I.

   They span a 4-dim commutative unital *-algebra

        P := span_C {Π_0, Π_1, Π_2, Π_3}  ⊂  End(C^8),

   isomorphic to C^4 as a *-algebra (one factor per hw level).

2. Each Π_k is S_3-invariant (U(π) Π_k = Π_k U(π) for all π ∈ S_3),
   so P is a 4-dim abelian subalgebra of the 20-dim S_3-invariant
   commutant End(C^8)^{S_3} (Batch 3).

3. P is the spectral-projector algebra of the Hamming-weight
   operator H = Σ_μ (I − S_μ)/2 on C^8.

4. Compared with the Batch 4 cube-shift elementary-symmetric
   subalgebra A_S^{S_3} = span{e_0, e_1, e_2, e_3} (also 4-dim,
   abelian, S_3-invariant):
   - A_S^{S_3} is Hadamard-diagonal (not hw-diagonal except for e_0).
   - P is hw-diagonal (not Hadamard-diagonal except for the total-
     parity projector Π_0 + Π_2).
   These are two distinct 4-dim abelian S_3-invariant subalgebras
   of End(C^8)^{S_3} sharing only the identity line (Batch 7 T2).

## Proof sketch

(1) Direct check on the computational basis: Π_k has 1's on basis
vectors with hw = k and 0's elsewhere, so Π_j Π_k is non-zero only
when j = k. The sum Σ Π_k is the identity because every basis
vector has some hw. (2) Since hw is invariant under axis permutation,
each V_k is S_3-invariant, so U(π) Π_k U(π)^{-1} = Π_k. (3) The
Hamming-weight operator H has eigenvalues {0, 1, 2, 3}, each with
eigenspace V_k; the spectral theorem identifies Π_k with the
spectral projector for eigenvalue k. (4) Part 5 of the runner shows
e_1 = S_1 + S_2 + S_3 sends hw = 0 to hw = 1, so e_1 is hw-off-
diagonal and cannot lie in P.

## Verification

The runner (a) verifies Π_k² = Π_k, Π_j Π_k = 0 for j ≠ k, and
Σ Π_k = I, (b) confirms rank(Π_k) = 1, 3, 3, 1 for k = 0, 1, 2, 3,
(c) confirms dim P = 4 via matrix rank, (d) checks Π_k commutes with
all 6 S_3 axis permutations, (e) recomputes dim End(C^8)^{S_3} = 20
to confirm P ⊂ End(C^8)^{S_3} strictly, (f) checks each Π_k is
diagonal in the hw basis, (g) exhibits e_1 mapping hw = 0 to hw = 1
to certify A_S^{S_3} ≠ P.

## Reusability

- Canonical abelian subalgebra for any framework argument that
  respects the Hamming-weight grading on the taste cube.
- Companion to the cube-shift polynomial algebra A_S (Batch 4,
  Hadamard-diagonal 8-dim) and its S_3-invariant subalgebra
  A_S^{S_3} (Batch 4, Hadamard-diagonal 4-dim). P is the
  hw-diagonal S_3-invariant 4-dim analogue.
- Direct input to the Batch 7 Intersection Theorem
  (A_S^{S_3} ∩ P = span{I}).
