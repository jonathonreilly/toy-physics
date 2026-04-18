# Perron-Frobenius Step-2 Wilson Local Nilpotent-Charpoly Certificate

**Date:** 2026-04-18  
**Status:** exact science-only sharpening of the Wilson compressed route from a
local nilpotent-chain `1 + 3` certificate to a local nilpotent-chain `1 + 1`
certificate  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py`

## Question

After the Wilson front has been reduced to:

- one local nilpotent chain generator `N_chain`,
- plus the three scalar spectral identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`,

can the post-support spectral layer be compressed one step further?

## Answer

Yes.

Because `B_e` and `H_e` are Hermitian `3 x 3` blocks, the three scalar
identities are exactly equivalent to equality of characteristic polynomials.

So the whole Wilson compressed route is now exactly one local nilpotent-chain
`1 + 1` certificate:

1. **local constructive layer**:
   one local nilpotent chain generator `N_chain` on the physical adjacent
   two-edge chain;
2. **post-support spectral layer**:
   one cubic spectral identity
   `chi_(B_e)(lambda) = chi_(H_e)(lambda)`.

The current bank still does **not** realize even the first generator layer.

## Setup

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md):

- the whole Wilson compressed route is one local nilpotent-chain `1 + 3`
  certificate.

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- for Hermitian `3 x 3` blocks, unitary equivalence is exactly equivalent to:
  - equality of characteristic polynomials,
  - equivalently equality of the first three trace powers.

So the only remaining issue is whether the three-scalar post-support layer
should still be treated as three separate constraints or as one exact cubic
spectral packet.

## Theorem 1: the whole Wilson compressed route is exactly one local nilpotent-chain `1 + 1` certificate

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one local nilpotent chain generator `N_chain`,
   together with one cubic spectral identity
   `chi_(B_e)(lambda) = chi_(H_e)(lambda)`.

### Proof

From the local nilpotent-chain minimal-certificate theorem, theorem-grade
Wilson compressed-route realization is already equivalent to:

- one local nilpotent generator `N_chain`,
- and the three scalar identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

From the compressed-block spectral-reduction theorem, for Hermitian `3 x 3`
blocks those three identities are exactly equivalent to equality of
characteristic polynomials.

Therefore the Wilson compressed route is exactly equivalent to:

- one local nilpotent generator `N_chain`,
- and one cubic spectral identity
  `chi_(B_e)(lambda) = chi_(H_e)(lambda)`.

## Corollary 1: the sharpest Wilson reviewer-facing certificate is now `1 + 1`

The live Wilson route is now sharper than:

- a local path algebra + three traces,
- a local nilpotent generator + three traces.

It is exactly:

- one local nilpotent generator,
- one cubic characteristic-polynomial identity.

## Corollary 2: the current bank still fails already at the generator layer

Because the current bank still does **not** realize `N_chain`, it still does
**not** realize the full local nilpotent-chain `1 + 1` certificate.

So the current-bank Wilson obstruction remains constructive-side first.

## What this closes

- exact compression of the Wilson route from a `1 + 3` certificate to a `1 + 1`
  certificate
- exact statement that the whole post-support spectral layer is one cubic
  characteristic-polynomial identity

## What this does not close

- a positive realization of the local nilpotent chain generator
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest compact Wilson theorem package now available.

The Wilson reopening lever is no longer a packet of scalar checks. It is one
local constructive generator plus one cubic spectral identity.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_wilson_local_nilpotent_charpoly_certificate_2026_04_18.py
```
