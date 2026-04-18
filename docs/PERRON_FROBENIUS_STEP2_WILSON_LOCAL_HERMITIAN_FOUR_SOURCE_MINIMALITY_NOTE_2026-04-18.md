# Perron-Frobenius Step-2 Wilson Local Hermitian Four-Source Minimality

**Date:** 2026-04-18  
**Status:** exact science-only lower-bound theorem showing the local Hermitian
Wilson source route is already minimal at one nearest-neighbor `4`-source
packet on the physical lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_four_source_minimality_2026_04_18.py`

## Question

After the remaining Wilson constructive primitive has been reduced to one local
Hermitian nearest-neighbor `4`-source packet, is that packet only a convenient
finite presentation?

Or is four the exact minimal local Hermitian source count on this Wilson lane?

## Bottom line

It is minimal.

Let

`V_loc^H := span_R{ X_12, Y_12, X_23, Y_23 }`.

This is the real local Hermitian nearest-neighbor source space on the adjacent
two-edge chain. It has real dimension `4`.

So any real-linear local Hermitian source-channel map

`L : V_loc^H -> R^m`

that determines arbitrary local Hermitian packet data must be injective. But if
`m < 4`, no such map can be injective.

Therefore:

- fewer than `4` real local Hermitian source channels cannot determine
  arbitrary sharpest Wilson constructive data;
- the local Hermitian `4`-source packet is not only sufficient;
- it is the exact minimal local Hermitian source target on the current Wilson
  route.

So the branch now knows the Wilson constructive primitive sharply:

- one local Hermitian nearest-neighbor `4`-source packet,
- no honest generic `3`-source shortcut,
- then only the `3` scalar spectral identities.

## What is already exact

### 1. The remaining primitive is already the local Hermitian `4`-source packet

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md):

- the remaining constructive Wilson primitive is exactly one local Hermitian
  nearest-neighbor `4`-source packet.

### 2. The support lane is already minimal at `4`

From
[PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic Hermitian shortcut below four real channels can determine
  arbitrary sharpest-route support data.

So the local source-side target and the support-side target already agree on
the same finite lower bound.

## Theorem 1: fewer than four real local Hermitian source channels cannot determine arbitrary local Hermitian packet data

Let

`V_loc^H := span_R{ X_12, Y_12, X_23, Y_23 }`.

Then `dim_R V_loc^H = 4`.

Let `ell_1, ..., ell_m : V_loc^H -> R` be any real-linear local Hermitian
source channels, and form

`L(S) := (ell_1(S), ..., ell_m(S)) in R^m`.

If `m < 4`, then `L` cannot be injective. Hence such a channel family cannot
determine arbitrary local Hermitian packet data.

### Proof

The four displayed Hermitian generators `X_12, Y_12, X_23, Y_23` are real-
linearly independent, so `dim_R V_loc^H = 4`.

If `m < 4`, then every real-linear map `L : V_loc^H -> R^m` has

`rank(L) <= m < 4`.

By real rank-nullity,

`dim_R ker(L) = 4 - rank(L) > 0`.

So there exists nonzero `K in V_loc^H` with `L(K) = 0`. Then for every
`S in V_loc^H`,

`L(S + K) = L(S)`.

Therefore the channel data do not distinguish `S` from `S + K`, so they do not
determine arbitrary local Hermitian packet data.

On the other hand, the exact local Hermitian `4`-source reduction theorem
already provides a `4`-source local target that does determine the current
Wilson constructive primitive.

Therefore the exact minimal finite number of real local Hermitian source
channels on the current Wilson lane is `4`.

## Corollary 1: the local Hermitian `4`-source packet is dimensionally sharp

The Wilson constructive theorem may now be stated locally as:

- derive the `4` local Hermitian nearest-neighbor sources,
- verify the downstream chain identities,
- verify rank `3`.

But this is no longer just a convenient local packet form. It saturates the
exact finite lower bound on the local Hermitian lane.

## Corollary 2: no honest generic local Hermitian `3`-source shortcut exists

Any claimed Wilson constructive theorem that purports to determine arbitrary
local Hermitian packet data from only three generic local Hermitian sources
must be using extra structure beyond the current theorem class.

Without such extra structure, three real local Hermitian source channels cannot
separate all of `V_loc^H`.

So review should reject any generic `3`-source shortcut claim on this lane.

## What this closes

- one exact lower bound on the local Hermitian Wilson source-channel count
- one exact statement that the nearest-neighbor `4`-source packet is minimal,
  not just sufficient
- one review-safe exclusion of generic local Hermitian `3`-source shortcuts

## What this does not close

- existence of the local Hermitian `4`-source packet on the current bank
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This removes the last obvious finite shortcut question on the local Hermitian
Wilson source lane.

The branch no longer has to say only:

- the constructive Wilson target is finite and local.

It can now say:

- the constructive Wilson target is finite, local, and minimal.
