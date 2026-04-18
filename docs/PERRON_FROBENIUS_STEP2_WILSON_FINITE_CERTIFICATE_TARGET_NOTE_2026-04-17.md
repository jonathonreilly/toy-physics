# Perron-Frobenius Step-2 Wilson Finite Certificate Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem packaging the whole Wilson compressed
route as one finite certificate: a `9`-element Hermitian support packet plus
`3` scalar spectral identities  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_finite_certificate_target_2026_04_17.py`

## Question

After the Wilson front has already been sharpened to:

- one finite `9`-element Hermitian source packet realizing support,
- and one `3`-scalar spectral packet verifying the compressed block after
  support,

can the whole Wilson compressed route now be stated as one explicit finite
certificate theorem?

## Bottom line

Yes.

The whole Wilson compressed route is now equivalent to one finite certificate
with two layers:

1. **support packet**:
   `9` Hermitian Wilson operators `S_1, ..., S_9` whose reconstructed
   matrix units satisfy the exact matrix-unit table and whose diagonal sum has
   rank `3`;
2. **post-support spectral packet**:
   for the induced compressed Hermitian Wilson block
   `B_e := I_e^* S_W I_e`,
   the three scalar identities

   `Tr(B_e^k) = Tr(H_e^k)`, `k = 1, 2, 3`.

So the Wilson compressed front is no longer an open-ended operator theorem in
practice. It is one finite certificate problem:

- `9` support-side packet conditions,
- then `3` spectral identities.

The current bank still does **not** realize that certificate, because it still
does not realize even the first packet.

## What is already exact

### 1. Wilson support realization is already reduced to one finite `9`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one finite
  `9`-element Hermitian packet with explicit matrix-unit reconstruction
  identities.

### 2. Post-support Wilson verification is already reduced to `3` scalar invariants

From
[PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md):

- once the rank-`3` Wilson support exists, unitary equivalence of the
  compressed Hermitian Wilson block to `H_e` is exactly equivalent to the
  three trace-power identities
  `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### 3. So the whole Wilson route is now finite

There is no additional infinite verification layer after support realization.

The only remaining infinite-dimensional rhetoric is historical packaging. The
actual theorem content has already collapsed to one finite support packet plus
one finite spectral packet.

## Theorem 1: exact finite-certificate form of the Wilson compressed route

The following are equivalent:

1. theorem-grade Wilson compressed-route realization:
   - theorem-grade `Phi_e / Psi_e / P_e / I_e`,
   - together with the invariant compressed-resolvent block law
     `P_e S_W P_e |_(Ran(P_e)) ~= H_e`;
2. one finite Wilson certificate consisting of:
   - a `9`-element Hermitian Wilson packet `S_1, ..., S_9` satisfying the
     matrix-unit reconstruction identities and rank-`3` support condition,
   - and the three scalar spectral identities
     `Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`.

### Proof

`(1) => (2)`.

By the Hermitian source-packet realization theorem, theorem-grade support
realization is exactly equivalent to the `9`-packet with the explicit
matrix-unit table.

By the compressed-block spectral-reduction theorem, once that support exists
the invariant block law is exactly equivalent to the three scalar spectral
identities.

So `(1)` implies the stated finite certificate.

`(2) => (1)`.

By the Hermitian source-packet realization theorem, the first layer of the
certificate reconstructs theorem-grade `Phi_e / Psi_e / P_e / I_e`.

Then by the compressed-block spectral-reduction theorem, the second layer of
the certificate implies the invariant Wilson compressed block law.

So `(2)` implies `(1)`.

Therefore the whole Wilson compressed route is exactly equivalent to one finite
certificate.

## Corollary 1: Wilson step-2A now has a finite reviewer-facing target

A future positive Wilson theorem may now be judged by a finite checklist:

- realize the `9` support packet,
- verify the matrix-unit table,
- verify rank `3`,
- verify `3` scalar spectral identities.

That is the sharpest hard-review-safe target yet on this lane.

## Corollary 2: the current bank still fails at the first certificate layer

Because the current bank still does **not** realize the support packet, it
still does **not** realize the full finite certificate. So the present
obstruction remains support-side first, not spectral-side.

## What this closes

- exact packaging of the whole Wilson compressed route as one finite
  certificate
- exact separation between support-side finite conditions and post-support
  spectral finite conditions
- exact statement that the current bank still fails at the first layer

## What this does not close

- a positive realization of the finite certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the cleanest Wilson summary theorem on the branch.

The live constructive route is no longer:

- “find a cross-sector bridge somehow.”

It is now:

- satisfy a finite `9 + 3` certificate.
