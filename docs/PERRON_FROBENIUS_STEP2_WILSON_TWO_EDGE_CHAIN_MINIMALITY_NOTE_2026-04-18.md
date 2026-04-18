# Perron-Frobenius Step-2 Wilson Two-Edge Chain Minimality

**Date:** 2026-04-18  
**Status:** exact science-only lower-bound theorem showing the physical-lattice
Wilson support route is already minimal at one adjacent directed two-edge chain  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_two_edge_chain_minimality_2026_04_18.py`

## Question

After the Wilson support theorem has been repackaged as one adjacent directed
two-edge chain on the physical nearest-neighbor lattice, is that chain only a
convenient local presentation?

Or is two directed edges the exact minimal local lattice support target on this
Wilson route?

## Bottom line

It is minimal.

The sharpest physical Wilson support route now lives on the complex edge-source
space

`V_edge := span_C{ E_12, E_23 }`.

That space has complex dimension `2`, equivalently real dimension `4`.

So any complex-linear local edge-response map

`L : V_edge -> C^m`

that determines arbitrary physical two-edge chain data must be injective. But
if `m < 2`, no such map can be injective.

Therefore:

- fewer than two complex directed edge channels cannot determine arbitrary
  sharpest physical-lattice support data;
- the existing adjacent two-edge chain is not only sufficient;
- it is the exact minimal local lattice support target on the current Wilson
  route.

So once the lattice is treated as physical, the branch now knows the Wilson
support target sharply:

- one adjacent directed two-edge chain,
- no honest one-edge shortcut,
- then only the `3` scalar spectral identities.

## What is already exact

### 1. The physical Wilson support theorem is already the adjacent two-edge chain

From
[PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  adjacent directed nearest-neighbor two-edge chain.

### 2. The Hermitian support lane is already minimal at four real channels

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic Hermitian shortcut below four real channels can determine
  arbitrary sharpest-route support data.

Since one complex directed edge carries exactly two real source coordinates,
this already suggests the same lower bound in physical edge language.

## Theorem 1: fewer than two complex directed edge channels cannot determine arbitrary sharpest-route local chain data

Let

`V_edge := span_C{ E_12, E_23 }`.

Then `dim_C V_edge = 2`.

Let `ell_1, ..., ell_m : V_edge -> C` be any complex-linear local edge
channels, and form

`L(X) := (ell_1(X), ..., ell_m(X)) in C^m`.

If `m < 2`, then `L` cannot be injective. Hence such a channel family cannot
determine arbitrary physical two-edge chain data.

### Proof

The two displayed directed edge generators `E_12` and `E_23` are
complex-linearly independent, so `dim_C V_edge = 2`.

If `m < 2`, then every complex-linear map `L : V_edge -> C^m` has

`rank(L) <= m < 2`.

By complex rank-nullity,

`dim_C ker(L) = 2 - rank(L) > 0`.

So there exists nonzero `K in V_edge` with `L(K) = 0`. Then for every
`X in V_edge`,

`L(X + K) = L(X)`.

Therefore the channel data do not distinguish `X` from `X + K`, so they do
not determine arbitrary physical two-edge chain data.

On the other hand, the exact two-edge chain theorem already provides a
two-edge local support target that does determine the sharpest Wilson support
data.

Therefore the exact minimal finite number of complex directed edge channels on
the sharpest physical Wilson support route is `2`.

## Corollary 1: the adjacent two-edge chain is dimensionally sharp

The Wilson support theorem may now be stated physically as:

- derive the two complex adjacent directed edge sources,
- verify the finite edge-chain identities,
- verify rank `3`.

But this is no longer just a convenient local presentation. It saturates the
exact finite lower bound on the physical-lattice lane.

## Corollary 2: no honest physical-lattice sharpest-route closure can use one generic directed edge channel

Any claimed Wilson support theorem that purports to determine arbitrary
sharpest-route physical chain data from a single generic directed edge channel
must be using extra structure beyond the current theorem class.

Without such extra structure, one directed edge cannot separate all of
`V_edge`.

So review should reject any generic one-edge shortcut claim on this lane.

## What this closes

- one exact lower bound on the physical-lattice Wilson support channel count
- one exact statement that the adjacent two-edge chain is minimal, not just
  sufficient
- one review-safe exclusion of generic one-edge Wilson support shortcuts

## What this does not close

- existence of the adjacent two-edge chain on the current bank
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This removes the last obvious local-lattice shortcut question on the Wilson
front.

The branch no longer has to say only:

- the physical Wilson target is local.

It can now say:

- the physical Wilson target is locally minimal too.
