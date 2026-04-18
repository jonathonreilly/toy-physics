# Perron-Frobenius Step-2 Wilson Local Chain-Plane Minimal Certificate

**Date:** 2026-04-18  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one minimal invariant local chain-plane certificate on the physical
nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_chain_plane_minimal_certificate_2026_04_18.py`

## Question

Once the Wilson local Hermitian `4 + 3` certificate is known, can the whole
route be stated in a cleaner invariant local form than a basis-dependent source
packet?

## Bottom line

Yes.

Define the real Hermitian nearest-neighbor chain plane

`V_chain^H := span_R{ X_12, Y_12, X_23, Y_23 } subset Herm(3)`.

Then the whole Wilson compressed route is exactly equivalent to one minimal
local chain-plane certificate with two layers:

1. **local constructive layer**:
   one real-linear injective Hermitian embedding
   `Psi_chain : V_chain^H -> Herm(H_W)`;
2. **post-source spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the sharpest Wilson theorem package is now not merely:

- a basis-dependent local Hermitian `4 + 3` certificate.

It is:

- one minimal invariant local chain-plane `4 + 3` certificate.

The current bank still does **not** realize even the first chain-plane layer.

## What is already exact

### 1. The local Hermitian `4`-packet is exactly one chain-plane embedding

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md):

- theorem-grade realization of the local Hermitian nearest-neighbor `4`-source
  packet is exactly equivalent to theorem-grade realization of one real-linear
  injective Hermitian chain-plane embedding
  `Psi_chain : V_chain^H -> Herm(H_W)`.

### 2. The local Hermitian lane is already minimal at `4`

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md):

- the sharpest local Hermitian Wilson source space has real dimension `4`,
- and no honest generic local Hermitian `3`-source shortcut exists.

So the chain-plane layer is already minimal.

### 3. Post-source verification is still only the same three scalar spectral identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the Wilson support exists, the compressed Wilson block law is exactly
  equivalent to
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: the whole Wilson compressed route is exactly one minimal local chain-plane `4 + 3` certificate

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one minimal local Wilson certificate consisting of:
   - one real-linear injective Hermitian chain-plane embedding
     `Psi_chain : V_chain^H -> Herm(H_W)`,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the local Hermitian chain-plane target theorem, theorem-grade Wilson
compressed-route realization implies theorem-grade realization of the local
chain-plane embedding `Psi_chain`.

By the local Hermitian `4`-source minimality theorem, that local layer is
already minimal at real dimension `4`.

By the compressed-block spectral-reduction theorem, once support exists the
remaining verification is exactly the three scalar spectral identities.

So `(1)` implies the minimal local chain-plane `4 + 3` certificate.

`(2) => (1)`.

By the local Hermitian chain-plane target theorem, `Psi_chain` is exactly
equivalent to realization of the local Hermitian nearest-neighbor `4`-source
packet, hence to the sharpest local constructive Wilson layer.

Then by the compressed-block spectral-reduction theorem, the three scalar
spectral identities imply the compressed Wilson block law.

So `(2)` implies theorem-grade Wilson compressed-route realization.

Therefore the whole Wilson compressed route is exactly equivalent to one
minimal local chain-plane `4 + 3` certificate.

## Corollary 1: the sharpest reviewer-facing Wilson target is now invariant, local, and minimal

A future positive Wilson theorem may now be judged by the checklist:

- realize the local chain-plane embedding `Psi_chain`,
- verify the downstream chain identities,
- verify rank `3`,
- verify `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

And the first layer is already known to be minimal.

## Corollary 2: the current bank still fails at the first invariant local layer

Because the current bank still does **not** realize the local chain-plane
embedding `Psi_chain`, it still does **not** realize the full minimal local
chain-plane `4 + 3` certificate.

So the obstruction remains local constructive-side first.

## What this closes

- exact replacement of the basis-dependent local Hermitian `4 + 3` certificate
  by its invariant local chain-plane form
- exact statement that the sharpest Wilson theorem package is now invariant,
  local, and minimal
- exact statement that the current bank still fails already at the first local
  chain-plane layer

## What this does not close

- a positive realization of the minimal local chain-plane `4 + 3` certificate
- a positive realization of `Psi_e`
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest invariant local Wilson theorem package now available on
the branch.

The live positive Wilson route is now:

- one minimal invariant Hermitian embedding of the physical nearest-neighbor
  chain plane `V_chain^H`,
- then only the three scalar spectral identities.
