# Perron-Frobenius Step-2 Wilson Local Hermitian Four-Source Reduction

**Date:** 2026-04-18  
**Status:** exact science-only theorem reducing the remaining Wilson local
two-edge source primitive to one local Hermitian `4`-source packet on the
physical nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_four_source_reduction_2026_04_18.py`

## Question

After the remaining Wilson constructive primitive has been reduced to one local
adjacent two-edge source law on the physical lattice, is that still the
sharpest finite source-side formulation?

Or is there already an exact local Hermitian packet form of the same object?

## Bottom line

There is already an exact local Hermitian packet form.

Let

- `X_12 := E_12 + E_21`,
- `Y_12 := -i E_12 + i E_21`,
- `X_23 := E_23 + E_32`,
- `Y_23 := -i E_23 + i E_32`.

Then

- `E_12 = (X_12 + i Y_12)/2`,
- `E_21 = (X_12 - i Y_12)/2`,
- `E_23 = (X_23 + i Y_23)/2`,
- `E_32 = (X_23 - i Y_23)/2`.

So one local adjacent two-edge source law is exactly equivalent to one local
Hermitian nearest-neighbor `4`-source packet.

Therefore the remaining Wilson constructive primitive is now not best read as
an abstract source family and not even as an unspecified complex two-edge law.
It may already be posed as:

- one local Hermitian `4`-source packet on the adjacent nearest-neighbor
  two-edge chain.

The current bank still does **not** realize even that sharper local Hermitian
packet.

## What is already exact

### 1. The remaining primitive is already one local adjacent two-edge source law

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md):

- the remaining compressed-route constructive primitive is one local adjacent
  two-edge Wilson source law on the physical nearest-neighbor lattice.

### 2. The support theorem is already the Hermitian nearest-neighbor `4`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  off-diagonal Hermitian nearest-neighbor `4`-packet.

So the source-side constructive primitive and the support-side finite packet are
already written in the same local nearest-neighbor language.

## Theorem 1: exact reduction of the local two-edge source primitive to one local Hermitian `4`-source packet

The following are equivalent on the physical nearest-neighbor lattice:

1. one local adjacent two-edge Wilson source law carrying the complex edge data
   `E_12, E_23` and their adjoints;
2. one local Hermitian nearest-neighbor `4`-source packet
   `X_12, Y_12, X_23, Y_23`.

### Proof

`(1) => (2)`.

Given the local two-edge source law, form the Hermitian linear combinations

- `X_12 := E_12 + E_21`,
- `Y_12 := -i E_12 + i E_21`,
- `X_23 := E_23 + E_32`,
- `Y_23 := -i E_23 + i E_32`.

These are local Hermitian nearest-neighbor sources, so they define one local
Hermitian `4`-source packet.

`(2) => (1)`.

Given the local Hermitian `4`-source packet, recover the complex edge data by

- `E_12 = (X_12 + i Y_12)/2`,
- `E_21 = (X_12 - i Y_12)/2`,
- `E_23 = (X_23 + i Y_23)/2`,
- `E_32 = (X_23 - i Y_23)/2`.

So the adjacent directed two-edge data are reconstructed exactly.

Therefore the local adjacent two-edge source law is exactly equivalent to one
local Hermitian nearest-neighbor `4`-source packet.

## Corollary 1: the next positive Wilson source attempt should target the local Hermitian `4`-packet directly

The next positive compressed-route theorem may now be framed as:

- derive the local Hermitian nearest-neighbor `4`-source packet.

That is sharper than:

- an abstract charged source family,
- or an unspecified complex local two-edge law.

## Corollary 2: the current bank still does not realize even that sharper local Hermitian packet

If the current bank realized the local Hermitian `4`-source packet at theorem
grade, then by Theorem 1 it would realize the local adjacent two-edge source
law, and therefore the local Wilson source primitive already isolated on the
compressed route.

But the current bank still does **not** realize even that local adjacent
two-edge source law.

So the current bank still does **not** realize even this sharper local
Hermitian `4`-source packet.

## What this closes

- exact reduction of the Wilson local source primitive from a local complex
  two-edge law to one local Hermitian nearest-neighbor `4`-source packet
- exact source-side alignment between the local constructive primitive and the
  already exact off-diagonal Hermitian `4`-packet support theorem
- exact statement that the current bank still fails even this sharper local
  Hermitian packet

## What this does not close

- a positive realization of the local Hermitian `4`-source packet
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This removes one more layer of vagueness from the Wilson front.

The live Wilson constructive problem is no longer:

- build some source family,
- or even build some local two-edge law.

It is now:

- build one local Hermitian nearest-neighbor `4`-source packet.
