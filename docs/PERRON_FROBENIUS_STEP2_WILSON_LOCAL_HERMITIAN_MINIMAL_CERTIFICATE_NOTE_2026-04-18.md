# Perron-Frobenius Step-2 Wilson Local Hermitian Minimal Certificate

**Date:** 2026-04-18  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one minimal local Hermitian `4 + 3` certificate on the physical
nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_minimal_certificate_2026_04_18.py`

## Question

Once the Wilson constructive primitive is reduced to one local Hermitian
nearest-neighbor `4`-source packet and that packet is proved minimal, can the
whole compressed Wilson route be packaged at that exact minimal local Hermitian
level?

## Bottom line

Yes.

The whole Wilson compressed route is now exactly one minimal local Hermitian
certificate with two layers:

1. **minimal local constructive layer**:
   one local Hermitian nearest-neighbor `4`-source packet;
2. **post-source spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the sharpest reviewer-facing Wilson target is now not only finite and local.
It is minimal too.

The current bank still does **not** realize even the first local Hermitian
`4`-source layer.

## What is already exact

### 1. The remaining constructive primitive is exactly the local Hermitian `4`-source packet

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md):

- the remaining constructive Wilson primitive is exactly one local Hermitian
  nearest-neighbor `4`-source packet.

### 2. That local Hermitian packet is already minimal

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic local Hermitian `3`-source shortcut can determine
  arbitrary Wilson constructive packet data.

### 3. Post-source verification is still only `3` scalar spectral identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the support exists, the compressed Wilson block law is exactly
  equivalent to
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: exact minimal local Hermitian `4 + 3` certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one minimal local Hermitian Wilson certificate consisting of:
   - one local Hermitian nearest-neighbor `4`-source packet,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the local Hermitian `4`-source reduction theorem, theorem-grade Wilson
realization implies the local Hermitian `4`-source packet.

By the local Hermitian `4`-source minimality theorem, that packet is already
dimensionally sharp on the local Wilson lane.

By the compressed-block spectral-reduction theorem, once that support exists
the remaining verification is exactly the `3` scalar spectral identities.

So `(1)` implies the minimal local Hermitian `4 + 3` certificate.

`(2) => (1)`.

By the local Hermitian `4`-source reduction theorem, the local Hermitian
packet reconstructs the sharpest local constructive Wilson layer.

Then by the compressed-block spectral-reduction theorem, the `3` scalar
spectral identities imply the compressed Wilson block law.

So `(2)` implies theorem-grade Wilson compressed-route realization.

Therefore the whole Wilson compressed route is exactly equivalent to one
minimal local Hermitian `4 + 3` certificate.

## Corollary 1: the sharpest Wilson checklist is now finite, local, and minimal

A future positive Wilson theorem may now be judged by the checklist:

- realize the local Hermitian nearest-neighbor `4`-source packet,
- verify the downstream chain identities,
- verify rank `3`,
- verify `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

And the first layer is already known to be minimal.

## Corollary 2: the current bank still fails at the first minimal local Hermitian layer

Because the current bank still does **not** realize the local Hermitian
`4`-source packet, it still does **not** realize the full minimal local
Hermitian `4 + 3` certificate.

So the obstruction remains local constructive-side first.

## What this closes

- exact replacement of the local Hermitian `4 + 3` certificate by its minimal
  local Hermitian form
- exact reviewer-facing Wilson checklist in finite, local, and minimal packet
  language
- exact statement that the current bank still fails at the first minimal local
  Hermitian layer

## What this does not close

- a positive realization of the minimal local Hermitian `4 + 3` certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest Wilson theorem package now available on the branch.

The live positive Wilson route is now:

- one minimal local Hermitian nearest-neighbor `4`-source packet,
- then only the `3` scalar spectral identities.
