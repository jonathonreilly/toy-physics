# Intersection of A_S^{S_3} and the Hw-Projector Algebra

**Status:** airtight (Grind Program, Batch 7)
**Runner:** `scripts/frontier_cube_shift_vs_hw_projector_intersection.py` (10/10 PASS)

## Classical results applied

- **Grassmann's formula** for linear subspace dimensions:
  dim(U ∩ V) = dim U + dim V − dim(U + V) (textbook linear algebra).
- **Z_2^3 Hadamard character theory** (Frobenius 1896) for the
  Hadamard-diagonal structure of A_S^{S_3}.
- **Spectral-projector framework** for the hw-diagonal structure of P.
- **Standard fact** that an operator diagonal in two orthonormal
  bases whose spans overlap only trivially must be a scalar multiple
  of I (consequence of the spectral theorem).

## Framework-specific step

Identification of A_S^{S_3} (Batch 4, Hadamard-diagonal 4-dim
S_3-invariant subalgebra of End(C^8)) and P (Batch 7 T1,
hw-diagonal 4-dim S_3-invariant subalgebra) as two structurally
distinct 4-dim abelian subalgebras of the 20-dim End(C^8)^{S_3}.

## Framework object

The pair of subalgebras
  A_S^{S_3} = span{e_0, e_1, e_2, e_3} ⊂ End(C^8)^{S_3},
  P = span{Π_0, Π_1, Π_2, Π_3} ⊂ End(C^8)^{S_3},
and their intersection A_S^{S_3} ∩ P.

## Theorem

1. A_S^{S_3} ∩ P = span_C{I} (1-dimensional), with the identity
   realized simultaneously as e_0 = I (from A_S^{S_3}) and as
   Σ_k Π_k = I (from P).

2. dim (A_S^{S_3} + P) = 4 + 4 − 1 = 7 (Grassmann's formula).

3. A_S^{S_3} + P is NOT a subalgebra of End(C^8)^{S_3}: the product
   e_1 · Π_0 is S_3-invariant (since both factors are) but does not
   lie in A_S^{S_3} + P.

## Proof sketch

(1) A_S^{S_3} is Hadamard-diagonal (Batch 4 Part 2) and P is
hw-diagonal (Batch 7 T1 Part 5). Suppose M ∈ A_S^{S_3} ∩ P. Then
M is simultaneously Hadamard-diagonal and hw-diagonal. Every
Hadamard vector |ψ_s⟩ is a uniform superposition of all 8
computational basis vectors |α⟩ (up to ±1 signs), so for M to have a
single eigenvalue on |ψ_s⟩ while being diagonal in |α⟩, all its
hw-diagonal eigenvalues must be equal. Hence M = λ · I for some
λ ∈ C, and A_S^{S_3} ∩ P = span{I}. (2) is Grassmann. (3) is
verified explicitly: the product e_1 · Π_0 has support on the
hw = 0 → hw = 1 block only; adding it to a basis of A_S^{S_3} + P
strictly increases the rank.

## Verification

The runner (a) confirms dim A_S^{S_3} = 4 and dim P = 4, (b) computes
the rank of the combined span and finds 7, thereby certifying the
intersection is 1-dim via Grassmann, (c) exhibits I = e_0 and
I = Σ Π_k as explicit generators of the intersection, (d) checks
that Π_1 is NOT Hadamard-diagonal (ruling out Π_1 ∈ A_S^{S_3}) and
e_1 is NOT hw-diagonal (ruling out e_1 ∈ P), (e) computes
e_1 · Π_0 and confirms it raises the rank of (basis ∪ {M}) from 7
to 8, proving it is not in the sum.

## Reusability

- Makes precise the complementary nature of "cube-shift-symmetric"
  (via A_S^{S_3}) and "hw-graded" (via P) as structural viewpoints
  on the S_3-invariant commutant.
- Decomposes End(C^8)^{S_3} (dim 20) into a 4-dim A_S^{S_3} piece,
  a 4-dim P piece, and a 13-dim "mixing" remainder (modulo the
  1-dim overlap at I).
- Useful for any framework construction that needs to organize
  S_3-invariant operators by simultaneous "cube-shift symmetry"
  and "hw-preservation" properties.
