# Gauge-Vacuum Plaquette Finite Sample Packet Nonclosure

**Date:** 2026-04-17  
**Status:** exact PF-only nonclosure theorem on the plaquette beta-side lane;
no finite packet of marked-holonomy samples can by itself determine the full
beta-side vector `v_6`  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_finite_sample_packet_nonclosure_2026_04_17.py`

## Question

Could the plaquette PF lane be closed by evaluating a sufficiently large but
still finite packet of marked-holonomy samples?

For example, if one added more and more exact values of

`Z_hat_6(W_1), ..., Z_hat_6(W_n)`,

would some finite `n` eventually determine the full beta-side environment
vector `v_6`?

## Answer

No.

The obstruction is structural.

Any finite sample packet supplies only finitely many linear functionals of the
beta-side coefficient bank. But the higher-orbit conjugation-symmetric
coefficient space is infinite-dimensional.

Already on any higher-orbit slice of dimension one larger than the packet
size, the finite sample map has nontrivial kernel by dimension alone.

Because the identity functional carries strictly positive orbit weights, that
kernel contains sign-changing directions, and those directions can be added to
or subtracted from a strictly positive baseline while keeping all coefficients
nonnegative for sufficiently small amplitude.

So no finite sample packet, no matter how large, can by itself determine the
full beta-side coefficient stack or the full beta-side vector `v_6`.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md):

- every marked-holonomy sample is a linear functional of the common beta-side
  vector `v_6`.

From
[GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_IDENTITY_PLUS_THREE_SAMPLE_HIGHER_ORBIT_UNDERDETERMINATION_NOTE_2026-04-17.md):

- this higher-orbit nonuniqueness already occurs for the concrete finite
  packet `{e, W_A, W_B, W_C}`.

The new theorem abstracts that mechanism.

## Theorem 1: any finite sample packet leaves higher-orbit kernel freedom

Let

`P = {W_1, ..., W_n}`

be any finite packet of marked holonomies, and include the identity sample
`e`.

Let `L_P` be the map from the conjugation-symmetric beta-side coefficient bank
to the finite summary vector

`(Z_hat_6(e), Z_hat_6(W_1), ..., Z_hat_6(W_n))`.

Then `L_P` is a linear map from an infinite-dimensional real vector space to
`R^(n+1)`.

Choose any `(n+2)` independent higher-orbit basis vectors. Restrict `L_P` to
their span. Then the restricted map has the form

`R^(n+2) -> R^(n+1)`.

Therefore its kernel is nontrivial.

So every finite sample packet leaves a nonzero higher-orbit direction that is
invisible to that packet.

## Theorem 2: the invisible higher-orbit directions support positive ambiguity

The identity component of `L_P` assigns strictly positive orbit weights

`m_(p,q) d_(p,q)^2`

to every higher orbit.

So if a nonzero kernel vector had all entries nonnegative or all entries
nonpositive, its identity component could not vanish.

Therefore every nonzero kernel vector must contain both positive and negative
entries.

Let `b` be any strictly positive baseline vector on the chosen higher-orbit
slice. Then for sufficiently small `epsilon > 0`,

`b + epsilon k`

and

`b - epsilon k`

remain distinct and entrywise nonnegative.

Because `k in ker(L_P)`, those two nonnegative higher-orbit coefficient stacks
produce exactly the same finite sample packet.

So finite packet ambiguity persists even inside the nonnegative
conjugation-symmetric coefficient class.

## Corollary 1: no finite marked-holonomy sampling program can by itself close `v_6`

The full beta-side vector `v_6` contains infinitely many higher-orbit
coefficients.

Since every finite sample packet leaves nontrivial higher-orbit kernel freedom,
no finite marked-holonomy sample program can by itself determine `v_6`.

At best, finite packets can constrain or reconstruct finite retained
truncations.

## What this closes

- exact proof that no finite sample packet can by itself determine the full
  beta-side coefficient bank
- exact proof that no finite sample packet can by itself determine the full
  beta-side vector `v_6`
- exact clarification that the finite-sample program is structurally a
  truncation/constraint program, not a full closure program

## What this does not close

- the true explicit beta-side vector `v_6`
- the true explicit operator data `K_6^env / B_6(W)`
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Why this matters

This closes the sample-based strategy at the right level.

The branch can still use finite sample packets to:

- reconstruct retained truncations,
- test candidate beta-side solves,
- and prove partial obstructions or bounds.

But it can no longer honestly pretend that evaluating finitely many sample
values will ever determine the full beta-side environment vector.

That means the only scientifically honest closure route is now the operator
route:

- explicit beta-side environment operator/vector data,
- not merely more sample values.
