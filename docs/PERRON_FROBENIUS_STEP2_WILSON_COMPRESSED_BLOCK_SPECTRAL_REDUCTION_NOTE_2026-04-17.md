# Perron-Frobenius Step-2 Wilson Compressed-Block Spectral Reduction

**Date:** 2026-04-17  
**Status:** exact science-only theorem reducing the invariant Wilson
compressed-resolvent block law to three scalar spectral identities once the
rank-`3` Wilson support is realized, while carrying the matching current-bank
boundary that the bank still lacks even that support  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_compressed_block_spectral_reduction_2026_04_17.py`

## Question

After the Wilson compressed route has already been sharpened to the single
invariant block law

`P_e S_W P_e |_(Ran(P_e)) ~= H_e`,

with

`S_W := (D^(-1) + (D^(-1))^*) / 2`,

is a future positive theorem still required to prove a full operator identity
on the rank-`3` Wilson block?

Or, once the Wilson support projector `P_e` exists, can the remaining
verification be reduced to a finite scalar spectral packet?

## Bottom line

It reduces to a finite scalar spectral packet.

Once a theorem-grade rank-`3` Wilson support `P_e` is realized and one chooses
an isometry `I_e : C^3 -> H_W` with `P_e = I_e I_e^*`, define the compressed
Hermitian block

`B_e := I_e^* S_W I_e`.

Then because both `B_e` and `H_e` are Hermitian `3 x 3` matrices, the
following are equivalent:

1. `B_e ~= H_e`;
2. `B_e` and `H_e` have the same characteristic polynomial;
3. `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the strongest honest verification target **after** Wilson support
realization is no longer a full matrix comparison. It is the three scalar
spectral identities

`Tr(B_e) = Tr(H_e)`,

`Tr(B_e^2) = Tr(H_e^2)`,

`Tr(B_e^3) = Tr(H_e^3)`.

This does **not** solve the current bank’s main Wilson obstruction, because the
current bank still does not realize theorem-grade `P_e / I_e / Phi_e / Psi_e`.
But it does sharpen what remains once that support lands.

## What is already exact

### 1. The Wilson compressed theorem is already one invariant block law

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_RESOLVENT_BLOCK_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_RESOLVENT_BLOCK_TARGET_NOTE_2026-04-17.md):

- theorem-grade `Phi_e` plus `H_e^(cand) = H_e` is exactly equivalent to
  one invariant Wilson compressed-resolvent block law

  `P_e S_W P_e |_(Ran(P_e)) ~= H_e`.

So the Wilson front is already posed as one Hermitian rank-`3` block problem.

### 2. The current bank still lacks even the Wilson support itself

From
[PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md),
[PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md),
and
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the current exact bank still does **not** realize theorem-grade
  `I_e / P_e / Phi_e / Psi_e`.

So the present theorem is a **verification reduction** after support
realization, not a hidden positive construction.

## Theorem 1: Hermitian rank-`3` unitary equivalence is exactly three trace-power identities

Let `A, B in Herm(3)`. Then the following are equivalent:

1. `A ~= B`;
2. `chi_A(lambda) = chi_B(lambda)`;
3. `Tr(A^k) = Tr(B^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)` and `(1) => (3)` are immediate because unitary equivalence
preserves characteristic polynomial and all trace powers.

`(2) => (1)` because Hermitian matrices are unitarily diagonalizable, and equal
characteristic polynomial means equal multisets of real eigenvalues.

`(3) => (2)` because for a `3 x 3` matrix the first three power sums determine
the three elementary symmetric polynomials by Newton identities, hence
determine the characteristic polynomial. Therefore `(3)` implies `(2)`, and so
implies `(1)`.

## Corollary 1: the invariant Wilson block law reduces to three scalar spectral identities

Assume a theorem-grade rank-`3` Wilson support projector `P_e` and choose an
isometry `I_e : C^3 -> H_W` with `P_e = I_e I_e^*`. Define

`B_e := I_e^* S_W I_e`.

Then the invariant Wilson compressed-resolvent block law

`P_e S_W P_e |_(Ran(P_e)) ~= H_e`

is equivalent to

`Tr(B_e^k) = Tr(H_e^k)`, `k = 1, 2, 3`.

So once `P_e` exists, the remaining Wilson-side verification target is exactly
three scalar spectral identities.

## Corollary 2: the post-support Wilson verification target is smaller than full matrix equality

After a future positive realization of `P_e`, the branch no longer needs to
prove a coordinate-level `3 x 3` matrix identity entry by entry. It is enough
to prove:

- one support realization theorem for `P_e`, and
- three scalar block invariants.

That is the cleanest reviewer-facing verification target now available on the
Wilson front.

## Theorem 2: the current bank still does not realize even the support needed to use this reduction

Assume the exact Wilson matrix-source embedding target theorem, the exact
Hermitian source-embedding target theorem, and the exact charged-embedding
boundary theorem. Then the current exact bank still does **not** realize:

1. theorem-grade `P_e`,
2. theorem-grade `I_e`,
3. theorem-grade `Phi_e`,
4. theorem-grade `Psi_e`.

Therefore the current bank still does **not** instantiate the compressed block
`B_e = I_e^* S_W I_e` at theorem grade, and so does **not** yet reach the
three-scalar verification stage.

## What this closes

- exact reduction of the invariant Wilson rank-`3` block law to three scalar
  spectral identities once support is realized
- exact statement that the future verification target is smaller than full
  matrix equality
- exact boundary that the present bank still does not reach even that stage
  because support realization is still missing

## What this does not close

- a positive Wilson support theorem for `P_e / I_e / Phi_e / Psi_e`
- a positive Wilson-to-`dW_e^H` theorem
- a positive Wilson-to-`D_-` theorem
- a positive global PF selector

## Why this matters

This is the right next sharpening on the Wilson front.

The branch now knows two different kinds of missing work:

1. **construction**: realize the rank-`3` Wilson support;
2. **verification after construction**: match only three scalar spectral
   invariants of the compressed Hermitian Wilson block.

That is cleaner and smaller than treating the whole post-support theorem as an
opaque block-matrix identity.
