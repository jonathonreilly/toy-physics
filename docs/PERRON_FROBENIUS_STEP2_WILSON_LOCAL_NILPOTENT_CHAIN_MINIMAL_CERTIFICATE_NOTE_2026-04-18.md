# Perron-Frobenius Step-2 Wilson Local Nilpotent-Chain Minimal Certificate

**Date:** 2026-04-18  
**Status:** exact science-only packaging of the whole Wilson compressed route
as one minimal local nilpotent-chain `1 + 3` certificate on the physical
lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_nilpotent_chain_minimal_certificate_2026_04_18.py`

## Question

Once the local Wilson constructive primitive has been reduced all the way to
one nilpotent chain generator, what is the sharpest complete Wilson
reviewer-facing certificate?

## Answer

The whole Wilson compressed route is now exactly one minimal local
nilpotent-chain `1 + 3` certificate:

1. **local constructive layer**:
   one local nilpotent chain generator `N_chain` on the physical adjacent
   two-edge chain;
2. **post-support spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the Wilson front is now sharper than:

- one local path-algebra `2-edge + 3` certificate,
- one local Hermitian `4 + 3` certificate,
- or one local adjacent two-edge source law.

It is exactly:

- one local nilpotent-chain `1 + 3` certificate.

The current bank still does **not** realize even the first generator layer.

## Setup

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_GENERATOR_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_GENERATOR_REDUCTION_NOTE_2026-04-18.md):

- the local path-algebra constructive layer is exactly one local nilpotent
  chain generator `N_chain`.

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once support exists, the remaining Wilson verification is exactly the three
  scalar identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: the whole Wilson compressed route is exactly one local nilpotent-chain `1 + 3` certificate

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one local nilpotent-chain `1 + 3` certificate consisting of:
   - one local nilpotent chain generator `N_chain`,
   - and the three scalar identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the nilpotent chain-generator reduction theorem, theorem-grade Wilson
realization implies theorem-grade realization of one local nilpotent chain
generator `N_chain`.

By the compressed-block spectral-reduction theorem, the remaining Wilson
verification is exactly the three scalar identities.

So `(1)` implies the local nilpotent-chain `1 + 3` certificate.

`(2) => (1)`.

By the same reduction theorem, the local generator `N_chain` reconstructs the
entire local path-algebra/source layer.

Then by the spectral-reduction theorem, the three scalar identities imply the
compressed Wilson block law.

So `(2)` implies theorem-grade Wilson compressed-route realization.

Therefore the whole Wilson compressed route is exactly one local
nilpotent-chain `1 + 3` certificate.

## Corollary 1: the Wilson positive reopening route is now a single-generator problem

The live positive Wilson question is no longer:

- “find a Wilson bridge somehow,”
- or “construct a large packet.”

It is:

- construct one local nilpotent chain generator `N_chain`,
- then verify three scalar spectral identities.

## Corollary 2: the current bank still fails at the first local generator layer

Because the current bank still does **not** realize the local nilpotent chain
generator `N_chain`, it still does **not** realize the whole local
nilpotent-chain `1 + 3` certificate.

So the Wilson obstruction remains constructive-side first.

## What this closes

- exact packaging of the whole Wilson compressed route as one local
  single-generator certificate
- exact statement that the Wilson reopening route is now a `1 + 3` certificate
- exact statement that the current bank still fails already at the generator
  layer

## What this does not close

- a positive realization of the local nilpotent chain generator
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest Wilson theorem package yet on the branch.

The positive reopening lever is now brutally explicit:

- one local nilpotent chain generator,
- then 3 scalar spectral identities.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_wilson_local_nilpotent_chain_minimal_certificate_2026_04_18.py
```
