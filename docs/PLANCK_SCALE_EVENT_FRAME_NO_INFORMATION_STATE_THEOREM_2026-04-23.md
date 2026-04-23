# Planck-Scale Event-Frame No-Information State Theorem

**Date:** 2026-04-23
**Status:** branch-local hardening theorem replacing the older `U(2)^4` default-state argument
**Audit runner:** `scripts/frontier_planck_event_frame_no_information_state_theorem.py`

## Question

Can the source-free state law be stated without treating arbitrary factor-local
`U(2)^4` rotations as presentation changes, given that the physical packet
`P_A` is defined on a particular primitive event frame?

## Bottom line

Yes.

The hardened proof separates two structures that the older wording mixed:

1. the **source-free bare cell state law**, which says the bare primitive event
   frame has no preferred primitive event;
2. the **worldtube readout law**, which defines the physical packet projector
   `P_A` invariantly on that event frame.

The source-free state does not have to be derived from a symmetry group that
preserves `P_A`. The state is fixed before any prepared or boundary readout bias
is supplied. The packet `P_A` is then a fixed invariant readout operator
evaluated against that already-fixed state.

## Primitive event frame

The exact primitive cell is the time-locked event frame

`E = {P_eta : eta in {0,1}^4}`,

where

`P_eta = |eta><eta|`.

This event frame is physical on the accepted physical-lattice package surface.
It is not an arbitrary Hilbert basis that can be rotated away by `U(2)^4`.

## Invariant definition of the packet

Define the primitive Hamming count operator

`N_evt = sum_eta |eta| P_eta`,

where

`|eta| = eta_t + eta_x + eta_y + eta_z`.

The one-step worldtube packet is the spectral projector

`P_A = 1_{N_evt = 1}`.

Equivalently,

`P_A = sum_(|eta|=1) P_eta`.

Thus `P_A` is not chosen by an arbitrary basis convention. It is the invariant
rank-four spectral projector of the retained event-count readout `N_evt`.

Any automorphism of the readout structure `(E, N_evt)` preserves `P_A`.
This is enough to make `P_A` a well-defined physical observable.

## Why packet-preserving symmetry alone is not enough

The automorphism group that preserves `P_A` has at least two event classes:

1. events inside `P_A`;
2. events outside `P_A`.

Therefore packet-preserving invariance alone can at most force a block state

`rho = alpha P_A + beta (I - P_A)`,

with

`4 alpha + 12 beta = 1`.

That does **not** force `alpha = beta = 1/16`. So the hardened proof does not
pretend that the packet stabilizer derives traciality.

## Source-free no-information law

Axiom Extension P1 supplies the missing state-law statement:

> a source-free bare primitive cell has no preferred primitive event.

In event-frame terms, this means the source-free state is invariant under the
transitive relabeling action of the bare primitive event frame.

This is not a claim that the physical readout `P_A` is erased. It is a claim
that the **state of the bare source-free cell** carries no hidden event
preference before a source, preparation, boundary condition, or dynamical
embedding is added.

## Theorem: no preferred primitive event forces traciality

Let

`rho = sum_eta p_eta P_eta`

be the source-free bare-cell state on the primitive event frame. Assume:

1. `rho` is positive and normalized;
2. `rho` is diagonal on the primitive event frame;
3. the bare source-free cell has no preferred primitive event.

Then

`rho = I_16 / 16`.

### Proof

No preferred primitive event means that for any two primitive projectors
`P_eta` and `P_xi`, the source-free law cannot distinguish them. Therefore

`p_eta = p_xi`

for all `eta, xi`.

Let the common value be `p`. Normalization gives

`16 p = 1`,

so

`p = 1/16`.

Hence

`rho = sum_eta (1/16) P_eta = I_16 / 16`.

## Corollary: exact quarter

Because `P_A` is the rank-four spectral projector of `N_evt` at eigenvalue
`1`,

`rank(P_A) = 4`.

Therefore

`Tr((I_16 / 16) P_A) = rank(P_A) / 16 = 4/16 = 1/4`.

## Hostile-review closure

This theorem removes the older `U(2)^4` vulnerability.

The proof does not say:

> arbitrary local basis rotations are gauge while `P_A` is also physical.

It says instead:

1. the physical event frame is retained;
2. `P_A` is invariantly defined inside that event frame as a spectral
   projector of the event-count readout;
3. the source-free bare-cell state has no preferred primitive event by Axiom
   Extension P1;
4. the tracial state follows from that no-information state law.

The remaining denial is therefore explicit and narrow:

> reject Axiom Extension P1's no-preferred-primitive-event state law.

That is a package-governance denial, not a hidden `U(2)^4` inconsistency.
