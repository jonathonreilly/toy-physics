# Perron-Frobenius Step-2 Wilson Local Hermitian Sharpest Certificate

**Date:** 2026-04-18  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one local Hermitian `4 + 3` certificate on the physical
nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_sharpest_certificate_2026_04_18.py`

## Question

Once the Wilson constructive primitive is reduced to one local Hermitian
nearest-neighbor `4`-source packet, can the whole compressed Wilson route be
packaged in that same local source-side language?

## Bottom line

Yes.

The whole Wilson compressed route is now exactly one local Hermitian finite
certificate with two layers:

1. **local constructive layer**:
   one local Hermitian nearest-neighbor `4`-source packet on the adjacent
   two-edge chain;
2. **post-source spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the sharpest constructive Wilson target is now not merely the abstract
`4 + 3` certificate and not merely the physical `2-edge + 3` certificate.
It is the local Hermitian `4 + 3` certificate.

The current bank still does **not** realize even the first local Hermitian
`4`-source layer.

## What is already exact

### 1. The local constructive primitive is already the Hermitian `4`-source packet

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md):

- the remaining local Wilson source primitive is exactly one local Hermitian
  nearest-neighbor `4`-source packet.

### 2. Post-support verification is still only `3` scalar spectral identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the support exists, the compressed Wilson block law is exactly
  equivalent to
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: exact local Hermitian `4 + 3` certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one local Hermitian Wilson certificate consisting of:
   - one local Hermitian nearest-neighbor `4`-source packet,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the local Hermitian `4`-source reduction theorem, theorem-grade Wilson
realization implies the local Hermitian `4`-source packet.

By the compressed-block spectral-reduction theorem, once that support exists
the remaining verification is exactly the `3` scalar spectral identities.

So `(1)` implies the local Hermitian `4 + 3` certificate.

`(2) => (1)`.

By the local Hermitian `4`-source reduction theorem, the local Hermitian
`4`-source packet reconstructs the local adjacent two-edge source law and
hence the sharpest Wilson support layer.

Then by the compressed-block spectral-reduction theorem, the `3` scalar
spectral identities imply the compressed Wilson block law.

So `(2)` implies theorem-grade Wilson compressed-route realization.

Therefore the whole Wilson compressed route is exactly equivalent to one local
Hermitian `4 + 3` certificate.

## Corollary 1: the sharpest constructive Wilson checklist is now finite and local

A future positive Wilson theorem may now be judged by the checklist:

- realize the local Hermitian nearest-neighbor `4`-source packet,
- verify the finite chain identities downstream,
- verify rank `3`,
- verify `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Corollary 2: the current bank still fails at the first local Hermitian layer

Because the current bank still does **not** realize the local Hermitian
`4`-source packet, it still does **not** realize the full local Hermitian
`4 + 3` certificate.

So the obstruction remains source-side first.

## What this closes

- exact replacement of the local two-edge constructive target by one local
  Hermitian `4 + 3` certificate
- exact reviewer-facing Wilson checklist in local Hermitian packet language
- exact statement that the current bank still fails at the first local
  Hermitian source layer

## What this does not close

- a positive realization of the local Hermitian `4 + 3` certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest constructive Wilson theorem package now available.

The live positive Wilson route is now:

- one local Hermitian nearest-neighbor `4`-source packet,
- then only the `3` scalar spectral identities.
