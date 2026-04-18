# Perron-Frobenius Step-2 Wilson Sharp Finite Certificate Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one sharp finite `7 + 3` certificate: a nearest-neighbor Hermitian
`7`-packet support layer plus `3` scalar spectral identities  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_sharp_finite_certificate_target_2026_04_17.py`

## Question

After the Wilson support theorem has been sharpened from a `9`-packet to a
nearest-neighbor `7`-packet chain certificate, can the whole Wilson compressed
route be re-packaged at that sharper level too?

## Bottom line

Yes.

The whole Wilson compressed route is now equivalent to one sharp finite
certificate with two layers:

1. **support layer**:
   one nearest-neighbor Hermitian `7`-packet satisfying the exact chain
   matrix-unit identities and rank-`3` condition;
2. **post-support spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the best reviewer-facing Wilson target is no longer `9 + 3`. It is now
`7 + 3`.

The current bank still does **not** realize even the first `7`-packet layer.

## What is already exact

### 1. Support is already equivalent to a nearest-neighbor `7`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one finite
  nearest-neighbor Hermitian `7`-packet plus finite chain identities.

### 2. Post-support verification is already equivalent to `3` scalar identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the support exists, the compressed Wilson block law is exactly
  equivalent to the three scalar spectral identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: exact `7 + 3` finite-certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization:
   - theorem-grade `Phi_e / Psi_e / P_e / I_e`,
   - together with the invariant compressed-resolvent block law
     `P_e S_W P_e |_(Ran(P_e)) ~= H_e`;
2. one sharp finite Wilson certificate consisting of:
   - one nearest-neighbor Hermitian `7`-packet satisfying the chain
     matrix-unit identities and rank-`3` condition,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the seven-packet chain-reduction theorem, theorem-grade Wilson support
realization is exactly equivalent to the `7`-packet support layer.

By the compressed-block spectral-reduction theorem, once that support exists
the invariant block law is exactly equivalent to the `3` scalar spectral
identities.

So `(1)` implies the stated `7 + 3` certificate.

`(2) => (1)`.

By the seven-packet chain-reduction theorem, the `7`-packet support layer
reconstructs theorem-grade `Phi_e / Psi_e / P_e / I_e`.

Then by the compressed-block spectral-reduction theorem, the `3` spectral
identities imply the invariant compressed Wilson block law.

So `(2)` implies `(1)`.

Therefore the whole Wilson compressed route is exactly equivalent to one sharp
finite `7 + 3` certificate.

## Corollary 1: the Wilson reviewer target is now strictly smaller

A future positive Wilson theorem may now be judged by the finite checklist:

- realize the nearest-neighbor `7`-packet,
- verify the chain matrix-unit identities,
- verify rank `3`,
- verify the `3` scalar spectral identities.

So the correct hard-review-safe Wilson target is now one `7 + 3` certificate.

## Corollary 2: the current bank still fails at the first layer

Because the current bank still does **not** realize the `7`-packet support
layer, it still does **not** realize the full sharp `7 + 3` certificate.

So the obstruction remains support-side first.

## What this closes

- exact replacement of the older Wilson `9 + 3` certificate by the sharper
  `7 + 3` certificate
- exact statement that the current bank still fails at the first `7`-packet
  layer
- exact reviewer-facing Wilson checklist at the sharpest current level

## What this does not close

- a positive realization of the `7 + 3` certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is now the cleanest Wilson theorem package on the branch.

The live positive Wilson route is no longer:

- an abstract embedding theorem,
- or even a `9 + 3` finite package.

It is now:

- one sharp `7 + 3` certificate.
