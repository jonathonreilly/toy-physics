# Perron-Frobenius Step-2 Wilson Sharpest Finite Certificate Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one sharpest finite `4 + 3` certificate: an off-diagonal Hermitian
`4`-packet support layer plus `3` scalar spectral identities  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_sharpest_finite_certificate_target_2026_04_17.py`

## Question

After the Wilson support theorem has been sharpened to the off-diagonal
Hermitian `4`-packet, can the whole compressed Wilson route be packaged at that
same sharpest level?

## Bottom line

Yes.

The whole Wilson compressed route is now equivalent to one sharpest finite
certificate with two layers:

1. **support layer**:
   one off-diagonal Hermitian nearest-neighbor `4`-packet satisfying the exact
   finite chain identities and rank-`3` condition;
2. **post-support spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the best reviewer-facing Wilson target is now no longer `9 + 3` or `7 + 3`.
It is `4 + 3`.

The current bank still does **not** realize even the first `4`-packet layer.

## What is already exact

### 1. Support is already equivalent to an off-diagonal Hermitian `4`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  off-diagonal Hermitian nearest-neighbor `4`-packet plus finite chain
  identities.

### 2. Post-support verification is already equivalent to `3` scalar identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the support exists, the compressed Wilson block law is exactly
  equivalent to the three scalar spectral identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: exact `4 + 3` finite-certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization:
   - theorem-grade `Phi_e / Psi_e / P_e / I_e`,
   - together with the invariant compressed-resolvent block law
     `P_e S_W P_e |_(Ran(P_e)) ~= H_e`;
2. one sharpest finite Wilson certificate consisting of:
   - one off-diagonal Hermitian nearest-neighbor `4`-packet satisfying the
     finite chain identities and rank-`3` condition,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the off-diagonal `4`-packet reduction theorem, theorem-grade Wilson support
realization is exactly equivalent to the `4`-packet support layer.

By the compressed-block spectral-reduction theorem, once that support exists
the invariant block law is exactly equivalent to the `3` scalar spectral
identities.

So `(1)` implies the stated `4 + 3` certificate.

`(2) => (1)`.

By the off-diagonal `4`-packet reduction theorem, the `4`-packet support layer
reconstructs theorem-grade `Phi_e / Psi_e / P_e / I_e`.

Then by the compressed-block spectral-reduction theorem, the `3` spectral
identities imply the invariant compressed Wilson block law.

So `(2)` implies `(1)`.

Therefore the whole Wilson compressed route is exactly equivalent to one
sharpest finite `4 + 3` certificate.

## Corollary 1: the Wilson reviewer target is now smallest at the current theorem surface

A future positive Wilson theorem may now be judged by the finite checklist:

- realize the off-diagonal Hermitian nearest-neighbor `4`-packet,
- verify the finite chain identities,
- verify rank `3`,
- verify the `3` scalar spectral identities.

So the correct hard-review-safe Wilson target is now one `4 + 3` certificate.

## Corollary 2: the current bank still fails at the first layer

Because the current bank still does **not** realize the `4`-packet support
layer, it still does **not** realize the full sharpest `4 + 3` certificate.

So the obstruction remains support-side first.

## What this closes

- exact replacement of the older Wilson `7 + 3` package by the sharper
  `4 + 3` package
- exact statement that the current bank still fails at the first `4`-packet
  layer
- exact reviewer-facing Wilson checklist at the sharpest current level

## What this does not close

- a positive realization of the `4 + 3` certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is now the cleanest Wilson theorem package on the branch.

The live positive Wilson route is now:

- one sharpest `4 + 3` certificate.
