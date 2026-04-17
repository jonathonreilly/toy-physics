# S_3 Mass-Matrix No-Go on the Hw=1 Triplet

**Status:** airtight
**Runner:** `scripts/frontier_s3_mass_matrix_no_go.py` (13/13 PASS)

## Classical results applied

- **Schur's lemma** (Schur 1905) for V ≅ A_1 ⊕ E: any G-invariant
  operator is a scalar on each isotypic component.
- **Hermitian matrix spectral theorem** (standard linear algebra):
  eigenvalues of a Hermitian matrix are real, with multiplicities
  summing to the dimension.
- **Dimension of End(V)^G for Z_2-representations** via Schur:
  dim End(V)^{Z_2} = n_+² + n_−² where n_± are the multiplicities
  of trivial and sign irreps.

## Framework-specific step

- Identification of the hw=1 triplet V = span(X_1, X_2, X_3) of the
  taste cube with the S_3 standard permutation-rep carrier A_1 ⊕ E
  (via the `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md` S_3 Axis-Permutation Decomposition).

## Framework object

Let V ⊂ C^8 be the hw=1 subspace (the three states with exactly one
axis excited; equivalently the standard 3-dim permutation carrier
spanned by {X_1, X_2, X_3}). By the S_3 Axis-Permutation Decomposition
(`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`),

    V  ≅  A_1 ⊕ E

as an S_3 representation.

## Theorem

1. The space of S_3-invariant Hermitian operators on V is a real
   2-dim vector space:

        End(V)^{S_3}_{Hermitian}  =  span_R { I_3, P_{A_1} },

   where P_{A_1} = (1/3) J_3 is the orthogonal projector onto the
   S_3-invariant line spanned by (X_1 + X_2 + X_3) / √3.

2. Every such operator M = α · I_3 + β · P_{A_1} has spectrum

        { α (multiplicity 2 on E),  α + β (multiplicity 1 on A_1) },

   i.e. at most 2 distinct eigenvalues.

3. **No-go corollary.** No S_3-invariant Hermitian operator on V can
   have three distinct eigenvalues. In particular, if V is identified
   with three physical generations, an unbroken S_3 symmetry at the
   mass-matrix level is incompatible with any three-way-distinct
   generation mass hierarchy (m_1 ≠ m_2 ≠ m_3).

4. **Size of the SSB relief.** Under spontaneous symmetry breaking
   S_3 → Z_2 (the residual subgroup fixing a single axis, as in the
   framework's V_sel axis-selection vacuum), the space of allowed
   Hermitian mass operators on V expands from 2-dim (S_3-invariant)
   to 5-dim (Z_2-invariant), with V ≅ 2·(trivial Z_2) ⊕ (sign Z_2)
   giving dim End(V)^{Z_2} = 2² + 1² = 5. This space contains
   operators with three distinct eigenvalues.

## Proof sketch

(1)–(2) by Schur's lemma applied to V ≅ A_1 ⊕ E: any linear operator
commuting with S_3 acts as a scalar on each isotypic component.
On the 1-dim A_1 component the scalar is (α + β); on the 2-dim E
component the scalar is α. Equivalently M = α·I_3 + β·P_{A_1}, and
the eigenvalues follow. (3) is immediate: the 2-fold degeneracy on
E forces at most two distinct eigenvalues. (4) by Schur on V as a
Z_2-representation (Z_2 fixes one axis and swaps the other two):
V decomposes as 2·(trivial) ⊕ (sign), so
dim End(V)^{Z_2} = 2² + 1² = 5.

## Verification

The runner rank-tests End(C^3)^{S_3} and confirms dim = 2; constructs
I_3 and J_3 and verifies both are S_3-invariant; checks P_{A_1} is
rank-1 idempotent; computes spectra for several (α, β) to confirm
the (α, α, α+β) structure; randomly samples 100 S_3-invariant
Hermitian operators and verifies none exceed 2 distinct eigenvalues;
and independently computes dim End(C^3)^{Z_2} = 5 to certify the SSB
dimension jump.

## Physical implication

The observed SM generation masses are three-way distinct in each of
the up, down, and charged-lepton sectors. Therefore, any framework
that places the three generations on the hw=1 triplet and invokes
S_3 symmetry MUST break S_3 spontaneously in order to lift the E-irrep
degeneracy. This no-go theorem provides a rigorous lower bound on
the symmetry-breaking content required for realistic flavor structure.

## Reusability

- Rigorous constraint on any framework claim invoking unbroken S_3
  at the mass-matrix level on the hw=1 triplet.
- Supports the necessity of SSB (in particular S_3 → Z_2) in
  frameworks using the hw=1 triplet as the three-generation carrier.
- Quantifies the dimensional relief from SSB: 2 → 5 real parameters
  on V after breaking to Z_2.
- Companion to the framework's V_sel mechanism, which is the natural
  S_3 → Z_2 breaking dynamics on the taste cube.
