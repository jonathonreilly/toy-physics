# Perron-Frobenius Step-2 Wilson Seven-Packet Chain Reduction

**Date:** 2026-04-17  
**Status:** exact science-only theorem reducing theorem-grade Wilson support
realization from a finite `9`-element Hermitian packet to a finite `7`-element
nearest-neighbor Hermitian chain packet, while preserving the current-bank
support-first obstruction  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_seven_packet_chain_reduction_2026_04_17.py`

## Question

After Wilson support realization has already been reduced to one finite
`9`-element Hermitian source packet, can the support theorem be sharpened
further by deriving the `(1,3)` corner from nearest-neighbor chain data rather
than treating it as primitive?

## Bottom line

Yes.

Theorem-grade Wilson support realization is already equivalent to one finite
nearest-neighbor Hermitian chain packet:

- `S_1 = Psi_e(E_11)`,
- `S_2 = Psi_e(E_22)`,
- `S_3 = Psi_e(E_33)`,
- `S_4 = Psi_e(E_12 + E_21)`,
- `S_5 = Psi_e(-i E_12 + i E_21)`,
- `S_8 = Psi_e(E_23 + E_32)`,
- `S_9 = Psi_e(-i E_23 + i E_32)`.

From these `7` Hermitian operators define

- `F_11 = S_1`,
- `F_22 = S_2`,
- `F_33 = S_3`,
- `F_12 = (S_4 + i S_5)/2`,
- `F_21 = (S_4 - i S_5)/2`,
- `F_23 = (S_8 + i S_9)/2`,
- `F_32 = (S_8 - i S_9)/2`,
- `F_13 := F_12 F_23`,
- `F_31 := F_32 F_21`.

Then theorem-grade Wilson support realization is exactly equivalent to the
statement that the reconstructed nearest-neighbor operators satisfy the chain
matrix-unit identities and that `F_11 + F_22 + F_33` has rank `3`.

So the `(1,3)` corner is already downstream. The Wilson support problem is
sharper than a `9`-packet: it is one finite `7`-packet plus finite chain
identities.

The current exact bank still does **not** realize even that sharper chain
packet.

## What is already exact

### 1. The `9`-packet theorem is already exact

From
[PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one finite
  `9`-element Hermitian Wilson source packet whose reconstructed matrix units
  satisfy the exact matrix-unit table.

### 2. The `(1,3)` corner is algebraically downstream of the chain

Inside `Mat_3(C)` one has

- `E_13 = E_12 E_23`,
- `E_31 = E_32 E_21`.

So if theorem-grade matrix units are already realized on the nearest-neighbor
chain, the long corner is forced.

## Theorem 1: theorem-grade Wilson support realization is exactly equivalent to one finite `7`-packet chain certificate

The following are equivalent:

1. theorem-grade Wilson support realization, equivalently theorem-grade
   `Phi_e / Psi_e / P_e / I_e`;
2. a `7`-tuple of Hermitian Wilson operators `S_1, S_2, S_3, S_4, S_5, S_8,
   S_9` such that the reconstructed nearest-neighbor operators satisfy:
   - `F_aa F_bb = delta_ab F_aa` for `a, b in {1,2,3}`,
   - `F_12 = F_11 F_12 F_22`,
   - `F_21 = F_22 F_21 F_11`,
   - `F_23 = F_22 F_23 F_33`,
   - `F_32 = F_33 F_32 F_22`,
   - `F_12 F_21 = F_11`,
   - `F_21 F_12 = F_22`,
   - `F_23 F_32 = F_22`,
   - `F_32 F_23 = F_33`,
   - `rank(F_11 + F_22 + F_33) = 3`.

### Proof

`(1) => (2)`.

Given theorem-grade `Phi_e`, take the `7` listed Hermitian sources from the
standard Hermitian basis. The reconstructed nearest-neighbor operators are
exactly the embedded matrix units `Phi_e(E_11), Phi_e(E_22), Phi_e(E_33),
Phi_e(E_12), Phi_e(E_21), Phi_e(E_23), Phi_e(E_32)`. So all displayed chain
matrix-unit identities hold, and `F_11 + F_22 + F_33 = Phi_e(1_3)` has rank
`3`.

`(2) => (1)`.

Assume the stated `7`-packet chain certificate and define the long corner by

- `F_13 := F_12 F_23`,
- `F_31 := F_32 F_21`.

Then the displayed chain identities imply the missing matrix-unit relations.
For example:

- `F_13 F_31 = F_12 F_23 F_32 F_21 = F_12 F_22 F_21 = F_12 F_21 = F_11`,
- `F_31 F_13 = F_32 F_21 F_12 F_23 = F_32 F_22 F_23 = F_32 F_23 = F_33`,
- `F_13 F_32 = F_12 F_23 F_32 = F_12 F_22 = F_12`,
- `F_21 F_13 = F_21 F_12 F_23 = F_22 F_23 = F_23`,

and all wrong-corner products vanish by the displayed corner-support identities
and orthogonality of `F_11, F_22, F_33`.

So the full `3 x 3` matrix-unit table is recovered. Now set

- `S_6 := F_13 + F_31`,
- `S_7 := -i F_13 + i F_31`.

This reconstructs the full Hermitian `9`-packet. By the exact `9`-packet
realization theorem, theorem-grade Wilson support realization follows.

Therefore the theorem-grade Wilson support problem is exactly equivalent to the
finite `7`-packet chain certificate.

## Corollary 1: the Wilson support frontier is sharper than a `9`-packet

The long corner does not need to be realized independently.

A future positive Wilson support theorem may now be judged by the smaller
reviewer-facing target:

- realize the `7` nearest-neighbor Hermitian Wilson sources,
- verify the finite chain matrix-unit identities,
- verify rank `3`.

Then the `(1,3)` corner and hence the full `9`-packet follow automatically.

## Corollary 2: the current bank still does not realize even that sharper `7`-packet

If the current bank realized the `7`-packet chain certificate, then by Theorem
1 it would realize theorem-grade Wilson support realization, hence the full
Hermitian `9`-packet. But the exact `9`-packet nonrealization theorem already
rules that out.

So the current bank still does **not** realize even this sharper
nearest-neighbor `7`-packet.

## What this closes

- exact reduction of the Wilson support theorem from a `9`-element Hermitian
  packet to a `7`-element nearest-neighbor Hermitian chain packet
- exact statement that the `(1,3)` corner is already downstream of the chain
- exact statement that the current bank still fails even this sharper support
  target

## What this does not close

- a positive realization of the `7`-packet chain certificate
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

The Wilson front is now finite in a stronger sense than before.

The live support target is no longer:

- one abstract embedding theorem,
- or even one `9`-element packet.

It is now:

- one nearest-neighbor `7`-packet plus finite chain identities.
