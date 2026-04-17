# S_3-Invariant Subalgebra of the Cube-Shift Polynomial Algebra

**Status:** airtight (Grind Program, Batch 4)
**Runner:** `scripts/frontier_s3_invariant_polynomial_subalgebra.py` (21/21 PASS)

## Framework object

Let A_S ⊂ End(C^8) be the cube-shift polynomial algebra (Batch 4,
dim 8). Let S_3 act on C^8 by axis permutation (Batch 2 decomposition
C^8 ≅ 4·A_1 ⊕ 2·E). The S_3-fixed subalgebra is

    A_S^{S_3}  :=  { M ∈ A_S  :  U(π) M U(π)^{-1} = M for all π ∈ S_3 }.

## Theorem

1. dim_C A_S^{S_3} = 4, with a canonical basis given by the elementary
   symmetric polynomials in the cube-shifts:

        e_0 = I
        e_1 = S_1 + S_2 + S_3
        e_2 = S_1 S_2 + S_1 S_3 + S_2 S_3
        e_3 = S_1 S_2 S_3.

2. A_S^{S_3} is a commutative subalgebra of A_S. Every element is
   simultaneously diagonal in the Hadamard basis, with the eigenvalue
   on |ψ_s⟩ given by the corresponding symmetric polynomial in the
   three signs s_1, s_2, s_3.

3. dim A_S^{S_3} = 4 = number of S_3 orbits on {±1}^3 (two singletons
   at s = (+,+,+), s = (−,−,−) and two orbits of size 3 at hw = 1
   and hw = 2 mod sign).

4. A_S^{S_3} is a strict subalgebra of End(C^8)^{S_3} (dim 20 by the
   S_3-Invariant Operator Dimension theorem, Batch 3). The remaining
   16 dimensions come from non-Hadamard-diagonal S_3-invariants;
   their decomposition into hw-parity-preserving (10) and
   hw-parity-swapping (10) blocks is the content of the S_3 Hw-Parity
   Block Decomposition (Batch 3).

## Proof sketch

(1) Elementary symmetric polynomials in the generators of an abelian
algebra are S_3-invariant by construction. Linear independence over
C^8 follows by evaluating on the eight Hadamard vectors: the 8×4
matrix of eigenvalues e_k(s) has rank 4. (2) Abelianness is inherited
from A_S. Diagonality in the Hadamard basis is inherited from the
fact that each M_T is Hadamard-diagonal. (3) By Peter–Weyl restricted
to a maximal-abelian subalgebra, the dimension of the S_3-fixed part
of the diagonal algebra on 8 vectors equals the number of orbits of
S_3 on the 8 labels. The 8 sign triples split as orbit sizes 1+3+3+1,
giving 4. (4) An explicit hw=1-block cross operator X is constructed,
is S_3-invariant, but is not Hadamard-diagonal; hence it lies in
End(C^8)^{S_3} \ A_S^{S_3}.

## Verification

The runner verifies each e_k commutes with U(π) for three generating
π ∈ S_3 (12 commutativity checks), rank-4 linear independence both
as operators and via their Hadamard-eigenvalue profiles, matches
dim = 4 against the 4 S_3-orbits on {±1}^3, and constructs an
explicit non-Hadamard-diagonal S_3-invariant to certify strict
inclusion in the 20-dim S_3-invariant commutant.

## Reusability

- Canonical description of any S_3-invariant operator built from the
  cube-shifts alone: such an operator lives in the 4-dim subalgebra
  spanned by {e_0, e_1, e_2, e_3}.
- Sharpens the 20-dim S_3-invariant commutant into its diagonal part
  (4 dim, this theorem) plus off-diagonal hw-parity structure
  (16 dim, Batch 3 S_3 Hw-Parity Block Decomposition).
- Used whenever a framework claim invokes "symmetric function of the
  cube-shifts" as a constraint — this theorem pins down the exact
  4-parameter freedom.
