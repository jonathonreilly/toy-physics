# Perron-Frobenius Step-2 Wilson Physical Sharpest Certificate Target

**Date:** 2026-04-18  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route in the right physical language as one local `2-edge + 3` certificate  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_physical_sharpest_certificate_target_2026_04_18.py`

## Question

After the Wilson support target has been repackaged as one adjacent directed
two-edge chain on the physical nearest-neighbor lattice, can the whole Wilson
compressed route be packaged at that same physical level too?

## Bottom line

Yes.

The whole Wilson compressed route is now equivalent to one local physical
certificate with two layers:

1. **local support layer**:
   one adjacent directed nearest-neighbor two-edge chain satisfying the finite
   edge-chain identities and rank-`3` condition;
2. **post-support spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the best reviewer-facing Wilson target is now not merely the abstract
`4 + 3` certificate. It is the physical local `2-edge + 3` certificate.

The current bank still does **not** realize even the first local two-edge
layer.

## What is already exact

### 1. The physical support theorem is already the adjacent two-edge chain

From
[PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md):

- theorem-grade Wilson support realization is exactly equivalent to one local
  adjacent directed nearest-neighbor two-edge chain.

### 2. That physical local support theorem is already minimal

From
[PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic one-edge shortcut can determine arbitrary sharpest-route
  physical chain data.

### 3. Post-support verification is already equivalent to three scalar identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the support exists, the compressed Wilson block law is exactly
  equivalent to the three scalar spectral identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: exact local `2-edge + 3` finite-certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization:
   - theorem-grade `Phi_e / Psi_e / P_e / I_e`,
   - together with the invariant compressed-resolvent block law
     `P_e S_W P_e |_(Ran(P_e)) ~= H_e`;
2. one local physical Wilson certificate consisting of:
   - one adjacent directed nearest-neighbor two-edge chain satisfying the
     finite edge-chain identities and rank-`3` condition,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the exact two-edge chain-reduction theorem, theorem-grade Wilson support
realization is exactly equivalent to the local two-edge support layer.

By the compressed-block spectral-reduction theorem, once that support exists
the invariant block law is exactly equivalent to the `3` scalar spectral
identities.

So `(1)` implies the stated local `2-edge + 3` certificate.

`(2) => (1)`.

By the exact two-edge chain-reduction theorem, the local two-edge support layer
reconstructs theorem-grade `Phi_e / Psi_e / P_e / I_e`.

Then by the compressed-block spectral-reduction theorem, the `3` scalar
spectral identities imply the invariant compressed Wilson block law.

So `(2)` implies `(1)`.

Therefore the whole Wilson compressed route is exactly equivalent to one local
physical `2-edge + 3` certificate.

## Corollary 1: the Wilson reviewer target is now physical, local, and sharp

A future positive Wilson theorem may now be judged by the finite checklist:

- realize the adjacent directed nearest-neighbor two-edge chain,
- verify the finite edge-chain identities,
- verify rank `3`,
- verify the `3` scalar spectral identities.

So the correct hard-review-safe Wilson target is now one local physical
`2-edge + 3` certificate.

## Corollary 2: the current bank still fails at the first local layer

Because the current bank still does **not** realize the local two-edge support
layer, it still does **not** realize the full physical `2-edge + 3`
certificate.

So the obstruction remains local support-side first.

## What this closes

- exact replacement of the abstract `4 + 3` certificate by the physically read
  local `2-edge + 3` certificate
- exact statement that the current bank still fails at the first local
  support layer
- exact reviewer-facing Wilson checklist at the sharpest physical level

## What this does not close

- a positive realization of the physical `2-edge + 3` certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the cleanest Wilson theorem package once the lattice is treated as
physical.

The live positive Wilson route is now:

- one local adjacent two-edge chain,
- then only the `3` scalar spectral identities.
