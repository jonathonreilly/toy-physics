# Perron-Frobenius Step-2 Wilson Four-Packet Minimality

**Date:** 2026-04-18  
**Status:** exact science-only lower-bound theorem showing the Hermitian
off-diagonal Wilson support route is already dimensionally minimal at `4`
real channels  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_four_packet_minimality_2026_04_18.py`

## Question

After the Wilson support theorem has been sharpened to one Hermitian
off-diagonal nearest-neighbor `4`-packet, is that only a convenient packet?

Or is `4` the exact minimal number of real Hermitian source channels on the
sharpest Wilson support route?

## Bottom line

It is minimal.

The sharpest Wilson support route now lives on the real vector space

`V_off := span_R{ E_12 + E_21, -i E_12 + i E_21, E_23 + E_32, -i E_23 + i E_32 }`.

This is the Hermitian nearest-neighbor off-diagonal source space. It has real
dimension `4`.

So any real-linear Hermitian source family

`L : V_off -> R^m`

that determines arbitrary off-diagonal chain data must be injective. But if
`m < 4`, no such map can be injective.

Therefore:

- fewer than `4` real Hermitian Wilson source channels cannot determine
  arbitrary sharpest-route support data;
- the existing off-diagonal `4`-packet is not just sufficient;
- it is the exact minimal finite Hermitian support packet on the present
  Wilson route.

So the branch now knows the Wilson support target sharply:

- one off-diagonal Hermitian `4`-packet,
- no honest Hermitian shortcut below `4`,
- then only the `3` spectral identities.

## What is already exact

### 1. The support theorem is already reduced to an off-diagonal `4`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md):

- theorem-grade Wilson support realization is exactly equivalent to one
  Hermitian off-diagonal nearest-neighbor `4`-packet plus finite chain
  identities.

So the sharpest current support theorem already lives on the real off-diagonal
source space `V_off`.

### 2. The whole compressed route is already packaged as one `4 + 3` certificate

From
[PERRON_FROBENIUS_STEP2_WILSON_SHARPEST_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_SHARPEST_FINITE_CERTIFICATE_TARGET_NOTE_2026-04-17.md):

- the whole Wilson compressed route is exactly one sharpest `4 + 3`
  certificate.

So the minimality question is now only whether the first `4` support channels
can still be reduced further.

## Theorem 1: fewer than four real Hermitian off-diagonal channels cannot determine arbitrary sharpest-route support data

Let

`V_off := span_R{ E_12 + E_21, -i E_12 + i E_21, E_23 + E_32, -i E_23 + i E_32 }`.

Then `dim_R V_off = 4`.

Let `ell_1, ..., ell_m : V_off -> R` be any real-linear Hermitian source
channels, and form

`L(X) := (ell_1(X), ..., ell_m(X)) in R^m`.

If `m < 4`, then `L` cannot be injective. Hence such a channel family cannot
determine arbitrary sharpest-route off-diagonal chain data.

### Proof

The four displayed Hermitian off-diagonal basis elements are real-linearly
independent, so `dim_R V_off = 4`.

If `m < 4`, then every linear map `L : V_off -> R^m` has

`rank(L) <= m < 4`.

By rank-nullity,

`dim ker(L) = 4 - rank(L) > 0`.

So there exists nonzero `K in V_off` with `L(K) = 0`. Then for every
`X in V_off`,

`L(X + K) = L(X)`.

Therefore the channel data do not distinguish `X` from `X + K`, so they do
not determine arbitrary off-diagonal chain data.

On the other hand, the exact off-diagonal `4`-packet reduction theorem already
provides a `4`-channel Hermitian packet that does determine the sharpest-route
support data.

Therefore the exact minimal finite number of real Hermitian Wilson source
channels on the sharpest support route is `4`.

## Corollary 1: the existing off-diagonal `4`-packet is dimensionally sharp

The Wilson support theorem may now be stated as:

- derive `4` real Hermitian off-diagonal Wilson sources,
- reconstruct the chain data,
- verify the finite chain identities,
- verify rank `3`.

But this is no longer only a convenient packet choice. It saturates the exact
finite lower bound.

## Corollary 2: no honest Hermitian sharpest-route closure can use three or fewer generic channels

Any claimed Wilson support theorem that purports to determine arbitrary
sharpest-route off-diagonal chain data from three or fewer real Hermitian
channels must be using extra structure beyond the current theorem class.

Without such extra structure, three or fewer channels cannot separate all of
`V_off`.

So review should reject any generic Hermitian support-closure claim below the
four-channel threshold.

## What this closes

- one exact lower bound on the sharpest Wilson Hermitian support channel count
- one exact statement that the off-diagonal `4`-packet is minimal, not just
  sufficient
- one review-safe exclusion of generic `3`-channel-or-smaller Wilson support
  shortcuts

## What this does not close

- existence of the off-diagonal `4`-packet on the current bank
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This removes one more ambiguity from the Wilson side.

The branch no longer has to say only:

- the sharpest support target is finite.

It can now say:

- the sharpest support target saturates the exact finite lower bound.

That is a much cleaner theorem surface under hard review because it blocks
underspecified “smaller packet” shortcut claims.
