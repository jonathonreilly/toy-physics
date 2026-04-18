# Perron-Frobenius Step-2 Wilson Four-Packet Off-Diagonal Reduction

**Date:** 2026-04-17  
**Status:** exact science-only theorem reducing theorem-grade Wilson support
realization from the nearest-neighbor `7`-packet to an off-diagonal Hermitian
`4`-packet plus finite chain identities, while preserving the current-bank
support-first obstruction  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_four_packet_offdiagonal_reduction_2026_04_17.py`

## Question

After the Wilson support theorem has already been reduced to a nearest-neighbor
Hermitian `7`-packet, are the diagonal sources themselves still primitive, or
are they already downstream of the off-diagonal nearest-neighbor chain?

## Bottom line

They are already downstream.

Theorem-grade Wilson support realization is exactly equivalent to one
off-diagonal Hermitian nearest-neighbor `4`-packet:

- `S_4 = Psi_e(E_12 + E_21)`,
- `S_5 = Psi_e(-i E_12 + i E_21)`,
- `S_8 = Psi_e(E_23 + E_32)`,
- `S_9 = Psi_e(-i E_23 + i E_32)`.

From these define

- `F_12 = (S_4 + i S_5)/2`,
- `F_21 = (S_4 - i S_5)/2`,
- `F_23 = (S_8 + i S_9)/2`,
- `F_32 = (S_8 - i S_9)/2`,

and then set

- `F_11 := F_12 F_21`,
- `F_22 := F_21 F_12 = F_23 F_32`,
- `F_33 := F_32 F_23`,
- `F_13 := F_12 F_23`,
- `F_31 := F_32 F_21`.

Then theorem-grade Wilson support realization is exactly equivalent to the
statement that these reconstructed operators satisfy the finite off-diagonal
chain identities:

- `F_12^2 = F_21^2 = F_23^2 = F_32^2 = 0`,
- `F_12 F_21 F_12 = F_12`,
- `F_21 F_12 F_21 = F_21`,
- `F_23 F_32 F_23 = F_23`,
- `F_32 F_23 F_32 = F_32`,
- `F_21 F_12 = F_23 F_32`,
- `F_12 F_32 = F_23 F_21 = F_21 F_32 = F_23 F_12 = 0`,
- `rank(F_11 + F_22 + F_33) = 3`.

So the diagonal data are already downstream of the off-diagonal chain. The
Wilson support frontier is sharper than a `7`-packet: it is one Hermitian
off-diagonal `4`-packet plus finite chain identities.

The current bank still does **not** realize even that sharper `4`-packet.

## What is already exact

### 1. The `7`-packet chain theorem is already exact

From
[PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  nearest-neighbor Hermitian `7`-packet plus finite chain identities.

### 2. The diagonal matrix units are already products of the off-diagonal chain

Inside `Mat_3(C)` one has

- `E_11 = E_12 E_21`,
- `E_22 = E_21 E_12 = E_23 E_32`,
- `E_33 = E_32 E_23`.

So once the off-diagonal chain is realized with the exact chain identities,
the diagonal support data are already forced.

## Theorem 1: theorem-grade Wilson support realization is exactly equivalent to one off-diagonal Hermitian `4`-packet

The following are equivalent:

1. theorem-grade Wilson support realization, equivalently theorem-grade
   `Phi_e / Psi_e / P_e / I_e`;
2. a Hermitian `4`-packet `S_4, S_5, S_8, S_9` such that the reconstructed
   off-diagonal operators satisfy the displayed finite chain identities and
   `rank(F_11 + F_22 + F_33) = 3`.

### Proof

`(1) => (2)`.

Given theorem-grade `Phi_e`, take the four displayed Hermitian Wilson sources.
The reconstructed off-diagonal operators are exactly the embedded matrix units
`Phi_e(E_12), Phi_e(E_21), Phi_e(E_23), Phi_e(E_32)`. So the displayed
off-diagonal chain identities hold, and the derived `F_11, F_22, F_33` are the
embedded diagonal matrix units whose sum has rank `3`.

`(2) => (1)`.

Assume the displayed `4`-packet chain identities. Define

- `F_11 := F_12 F_21`,
- `F_22 := F_21 F_12 = F_23 F_32`,
- `F_33 := F_32 F_23`,
- `F_13 := F_12 F_23`,
- `F_31 := F_32 F_21`.

The nilpotency, partial-isometry, common-middle, and wrong-order vanishing
relations imply the full matrix-unit table. For example:

- `F_11^2 = F_12 (F_21 F_12) F_21 = F_12 F_22 F_21 = F_12 F_21 = F_11`,
- `F_11 F_22 = F_12 F_21 F_21 F_12 = 0`,
- `F_13 F_31 = F_12 F_23 F_32 F_21 = F_12 F_22 F_21 = F_11`,
- `F_31 F_13 = F_32 F_21 F_12 F_23 = F_32 F_22 F_23 = F_33`,
- `F_13 F_32 = F_12 F_23 F_32 = F_12 F_22 = F_12`,
- `F_21 F_13 = F_21 F_12 F_23 = F_22 F_23 = F_23`,

and all wrong products vanish by the wrong-order chain vanishings. So the full
matrix-unit system is reconstructed. Therefore theorem-grade Wilson support
realization follows.

## Corollary 1: the Wilson support frontier is now an off-diagonal `4`-packet problem

A future positive Wilson support theorem may now be judged by the smaller
reviewer-facing target:

- realize the Hermitian off-diagonal `4`-packet,
- verify the finite off-diagonal chain identities,
- verify rank `3`.

Then the diagonal data and long corner follow automatically.

## Corollary 2: the current bank still does not realize even that sharper `4`-packet

If the current bank realized the off-diagonal `4`-packet chain certificate,
then by Theorem 1 it would realize theorem-grade Wilson support realization,
hence the `7`-packet and the full `9`-packet. But the exact sharper
nonrealization theorems already rule that out.

So the current bank still does **not** realize even this sharper off-diagonal
`4`-packet.

## What this closes

- exact reduction of the Wilson support theorem from a `7`-packet to an
  off-diagonal Hermitian `4`-packet
- exact statement that the diagonal support data are already downstream of the
  off-diagonal chain
- exact statement that the current bank still fails even this sharper support
  target

## What this does not close

- a positive realization of the off-diagonal `4`-packet
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

The Wilson support frontier is now finite in the sharpest current sense.

The live support target is no longer:

- an abstract embedding theorem,
- a `9`-packet,
- or even a `7`-packet.

It is now:

- one Hermitian off-diagonal `4`-packet plus finite chain identities.
