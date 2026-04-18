# Perron-Frobenius Step-2 Wilson Local Path-Algebra Minimal Certificate

**Date:** 2026-04-18  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one minimal local path-algebra `2-edge + 3` certificate on the
physical nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_path_algebra_minimal_certificate_2026_04_18.py`

## Question

Once the Wilson front is stated as one local path-algebra embedding on the
physical adjacent two-edge chain, can the whole compressed route be packaged in
that same local algebraic language?

## Bottom line

Yes.

The whole Wilson compressed route is now exactly one minimal local
path-algebra certificate with two layers:

1. **local constructive layer**:
   one local unital `*`-monomorphism
   `Phi_chain : A_chain -> End(H_W)` of the physical adjacent two-edge chain
   path algebra;
2. **post-support spectral layer**:
   the three scalar identities
   `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

So the sharpest Wilson theorem package is now not merely:

- one local Hermitian `4 + 3` certificate,
- or one local chain-plane `4 + 3` certificate.

It is:

- one minimal local path-algebra `2-edge + 3` certificate.

The current bank still does **not** realize even the first local path-algebra
layer.

## What is already exact

### 1. The sharpest local constructive object is already `Phi_chain`

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md):

- the sharpest Wilson local constructive primitive is exactly one local unital
  `*`-monomorphism `Phi_chain : A_chain -> End(H_W)`.

### 2. That local algebra object is already minimal in physical support size

From
[PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md):

- the adjacent directed two-edge chain is already the exact minimal physical
  local support target.

So the local algebra layer is already minimal in the physical-lattice sense.

### 3. Post-support verification is still only the same three scalar spectral identities

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the Wilson support exists, the compressed Wilson block law is exactly
  equivalent to
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

## Theorem 1: the whole Wilson compressed route is exactly one minimal local path-algebra `2-edge + 3` certificate

The following are equivalent:

1. theorem-grade Wilson compressed-route realization;
2. one minimal local Wilson certificate consisting of:
   - one local unital `*`-monomorphism
     `Phi_chain : A_chain -> End(H_W)`,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the local chain path-algebra target theorem, theorem-grade Wilson
compressed-route realization implies theorem-grade realization of the local
path-algebra embedding `Phi_chain`.

By the two-edge chain minimality theorem, the underlying physical support is
already minimal at one adjacent two-edge chain.

By the compressed-block spectral-reduction theorem, once support exists the
remaining verification is exactly the three scalar spectral identities.

So `(1)` implies the minimal local path-algebra `2-edge + 3` certificate.

`(2) => (1)`.

By the local chain path-algebra target theorem, `Phi_chain` is exactly
equivalent to theorem-grade realization of the local adjacent two-edge chain
and its downstream local Hermitian source layers.

Then by the compressed-block spectral-reduction theorem, the three scalar
spectral identities imply the compressed Wilson block law.

So `(2)` implies theorem-grade Wilson compressed-route realization.

Therefore the whole Wilson compressed route is exactly equivalent to one
minimal local path-algebra `2-edge + 3` certificate.

## Corollary 1: the sharpest reviewer-facing Wilson target is now local, algebraic, and minimal

A future positive Wilson theorem may now be judged by the checklist:

- realize the local path-algebra embedding `Phi_chain`,
- verify the downstream chain identities,
- verify rank `3`,
- verify `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

And the first layer is already known to be physically minimal.

## Corollary 2: the current bank still fails at the first local algebraic layer

Because the current bank still does **not** realize the local path-algebra
embedding `Phi_chain`, it still does **not** realize the full minimal local
path-algebra `2-edge + 3` certificate.

So the obstruction remains local constructive-side first.

## What this closes

- exact packaging of the whole Wilson compressed route in local path-algebra
  language
- exact statement that the sharpest Wilson theorem package is now local,
  algebraic, and minimal
- exact statement that the current bank still fails already at the first local
  algebraic layer

## What this does not close

- a positive realization of the minimal local path-algebra `2-edge + 3`
  certificate
- a positive realization of the full global source embedding `Phi_e`
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest local algebraic Wilson theorem package now available on
the branch.

The live positive Wilson route is now:

- one minimal local path-algebra embedding of the physical adjacent two-edge
  chain,
- then only the three scalar spectral identities.
