# Perron-Frobenius Step-2 Wilson Two-Edge Chain Reduction

**Date:** 2026-04-18  
**Status:** exact science-only theorem repackaging the sharpest Wilson support
target as one adjacent directed two-edge chain on the physical lattice, while
preserving the current-bank support-first obstruction  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_two_edge_chain_reduction_2026_04_18.py`

## Question

After the Wilson support theorem has been sharpened to one Hermitian
off-diagonal nearest-neighbor `4`-packet, what is the right physical reading of
that target once the lattice is taken seriously as physical?

Is the frontier still best stated as four Hermitian channels, or can it be
stated more physically as local edge data on the nearest-neighbor lattice?

## Bottom line

It can be stated more physically.

The sharpest Wilson support theorem is already equivalent to one adjacent
directed two-edge chain:

- one complex nearest-neighbor edge source `G_12`,
- one complex nearest-neighbor edge source `G_23`,

together with the finite chain identities

- `G_12^2 = G_23^2 = 0`,
- `G_12 G_12^* G_12 = G_12`,
- `G_23 G_23^* G_23 = G_23`,
- `G_12^* G_12 = G_23 G_23^*`,
- `G_23 G_12 = 0`,
- `G_12 G_23^* = 0`,
- `rank(G_12 G_12^* + G_12^* G_12 + G_23^* G_23) = 3`.

From these two directed nearest-neighbor edges, everything else is downstream:

- reverse edges are adjoints:
  `F_21 = G_12^*`, `F_32 = G_23^*`,
- diagonal support data are products:
  `F_11 = G_12 G_12^*`, `F_22 = G_12^* G_12 = G_23 G_23^*`,
  `F_33 = G_23^* G_23`,
- the long corner is the chain product:
  `F_13 = G_12 G_23`, `F_31 = G_23^* G_12^*`.

So once the lattice is treated as physical, the sharpest Wilson support target
is no longer best read as a 4-channel abstract packet. It is one local
adjacent two-edge chain on the physical nearest-neighbor lattice.

The current bank still does **not** realize even that sharper physical two-edge
chain.

## What is already exact

### 1. The sharpest Hermitian support theorem is already the off-diagonal `4`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  Hermitian off-diagonal nearest-neighbor `4`-packet plus finite chain
  identities.

### 2. That `4`-packet is already minimal on the Hermitian support lane

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic Hermitian shortcut below four real channels can determine
  arbitrary sharpest-route support data.

So the only remaining sharpening is not lower real dimension. It is better
physical interpretation.

## Theorem 1: theorem-grade Wilson support realization is exactly equivalent to one adjacent directed two-edge chain

The following are equivalent:

1. theorem-grade Wilson support realization, equivalently theorem-grade
   `Phi_e / Psi_e / P_e / I_e`;
2. a pair of complex operators `(G_12, G_23)` satisfying the displayed
   two-edge chain identities and rank-`3` condition.

### Proof

`(1) => (2)`.

Given theorem-grade Wilson support realization, define

- `G_12 := F_12`,
- `G_23 := F_23`.

Then:

- `G_12^2 = F_12^2 = 0`,
- `G_23^2 = F_23^2 = 0`,
- `G_12 G_12^* G_12 = F_12 F_21 F_12 = F_12`,
- `G_23 G_23^* G_23 = F_23 F_32 F_23 = F_23`,
- `G_12^* G_12 = F_21 F_12 = F_22 = F_23 F_32 = G_23 G_23^*`,
- `G_23 G_12 = F_23 F_12 = 0`,
- `G_12 G_23^* = F_12 F_32 = 0`,

and the displayed rank condition becomes the usual rank-`3` support condition.

So theorem-grade support realization implies the two-edge chain certificate.

`(2) => (1)`.

Assume the displayed two-edge chain identities. Define

- `F_12 := G_12`, `F_21 := G_12^*`,
- `F_23 := G_23`, `F_32 := G_23^*`,
- `F_11 := G_12 G_12^*`,
- `F_22 := G_12^* G_12 = G_23 G_23^*`,
- `F_33 := G_23^* G_23`,
- `F_13 := G_12 G_23`,
- `F_31 := G_23^* G_12^*`.

Then:

- `F_11^2 = G_12 G_12^* G_12 G_12^* = G_12 G_12^* = F_11`,
- `F_22^2 = G_12^* G_12 G_12^* G_12 = G_12^* G_12 = F_22`,
- `F_33^2 = G_23^* G_23 G_23^* G_23 = G_23^* G_23 = F_33`,
- `F_13 F_31 = G_12 G_23 G_23^* G_12^* = G_12 F_22 G_12^* = F_11`,
- `F_31 F_13 = G_23^* G_12^* G_12 G_23 = G_23^* F_22 G_23 = F_33`,
- `F_13 F_32 = G_12 G_23 G_23^* = G_12 F_22 = G_12 = F_12`,
- `F_21 F_13 = G_12^* G_12 G_23 = F_22 G_23 = G_23 = F_23`,

and all wrong products vanish by the two-edge wrong-order identities. So the
full matrix-unit system is reconstructed. Therefore theorem-grade Wilson
support realization follows.

## Corollary 1: the physical Wilson support target is one adjacent two-edge chain

Once the lattice is treated as physical, the sharpest Wilson support theorem
should be read as:

- realize one adjacent directed nearest-neighbor two-edge chain,
- verify the finite edge-chain identities,
- verify rank `3`.

Reverse edges, diagonal support, and the long corner are all downstream.

## Corollary 2: the current bank still does not realize even that physical two-edge chain

If the current bank realized this physical two-edge chain certificate, then by
Theorem 1 it would realize theorem-grade Wilson support realization, hence the
off-diagonal Hermitian `4`-packet. But the exact `4`-packet nonrealization
theorem already rules that out.

So the current bank still does **not** realize even this physical adjacent
two-edge chain.

## What this closes

- exact physical re-reading of the sharpest Wilson support target as one local
  adjacent two-edge chain on the nearest-neighbor lattice
- exact statement that reversals, diagonals, and the long corner are all
  downstream of that chain
- exact statement that the current bank still fails even this sharper physical
  target

## What this does not close

- a positive realization of the two-edge chain
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the right physical reading of the Wilson front once the lattice is
taken seriously as physical.

The live Wilson target is now not just finite and minimal. It is local:

- one adjacent directed two-edge chain,
- then only the `3` scalar spectral identities.
