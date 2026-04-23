# Planck-Scale Source-Free Local Traciality Event-Frame Route

**Date:** 2026-04-23  
**Status:** science-only direct event-frame route to the last Planck blocker; exact reduction plus sharp obstruction  
**Audit runner:** `scripts/frontier_planck_source_free_local_traciality_event_frame_route.py`

## Question

After closing the direct counting law

`c_cell(rho) = Tr(rho P_A)`,

can source-free local traciality be derived from a direct **event-frame / no
preferred projector** principle on the primitive time-locked `C^16` cell?

This route deliberately avoids the older scalar "boundary pressure" packaging.
It asks only:

> what exact symmetry of the primitive 16-event frame would force the
> source-free local state to be tracial?

## Bottom line

Yes, the event-frame route isolates the problem exactly.

The result is:

1. on the current retained direct stack, the exact primitive-cell event-frame
   symmetry is still only the residual spatial permutation group `S_3`;
2. on the primitive 16-event frame, that `S_3` action has exactly eight
   orbits, classified by

   `(t,w) in {0,1} x {0,1,2,3}`,

   where `t` is the temporal bit and `w` is the spatial Hamming weight;
3. therefore the current retained direct stack still allows an exact
   8-weight diagonal source-free family, hence a 7-parameter normalized state
   family;
4. so the event-frame route does **not** close retained Planck on current
   accepted structure alone;
5. however, if one strengthens the source-free local law to:

   > **primitive event-frame transitivity / no preferred primitive projector,**

   meaning invariance under any transitive relabeling group on the 16 atomic
   projectors, then the source-free state is forced to be

   `rho_cell = I_16 / 16`;

6. together with the already-closed counting law, that gives

   `c_cell = Tr((I_16 / 16) P_A) = 1/4`,

   hence the direct Planck route closes.

So the sharp exact obstruction is now:

> the current retained direct stack does not yet provide a transitive symmetry
> theorem on the full primitive 16-event frame.

That is the genuinely missing statement.

## Why this is the right direct route

The counting law is already closed. The only remaining issue is state
selection on the primitive cell.

The direct physical question is therefore not:

- "what scalar free-energy object should be called pressure?"

It is:

- "why should the source-free local state on the primitive physical cell have
  no preferred primitive event?"

That is exactly an event-frame / no-preferred-projector question.

## Inputs

This route uses only current branch-local direct Planck surfaces plus accepted
support semantics:

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)

What these already fix:

1. the primitive local carrier is the exact finite one-cell Hilbert carrier
   `H_cell = C^16`;
2. the physical one-step worldtube packet is the exact projector `P_A`;
3. the direct coefficient law is already closed:
   `c_cell(rho) = Tr(rho P_A)`;
4. primitive cell events live on the physical lattice surface and are not to be
   discarded by proper exact quotienting;
5. the current retained direct stack still leaves the source-free state
   underdetermined.

This note attacks only the exact symmetry content of that last underdetermined
state problem.

## Setup

Work on the exact time-locked primitive cell basis

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`,

with atomic projectors

`P_eta = |eta><eta|`.

Call the set `{P_eta}` the **primitive event frame**.

Define the residual exact symmetry already present on the retained direct
stack:

`G_ret = S_3`,

acting by permutation of the spatial bits `(eta_x, eta_y, eta_z)` and fixing
the temporal bit `eta_t`.

Let

`w(eta) = eta_x + eta_y + eta_z`.

Then the exact `G_ret` orbit label is the pair

`(eta_t, w(eta)) in {0,1} x {0,1,2,3}`.

## Definition: event-frame source-free candidate state

Call `rho` an **event-frame source-free candidate** if:

1. `rho` is diagonal on the primitive event frame `{P_eta}`;
2. `rho` is positive and normalized;
3. `rho` is invariant under the currently retained direct event-frame symmetry.

On current accepted structure, item 3 means only:

`U_sigma rho U_sigma^dagger = rho` for every `sigma in S_3`.

This is exactly the symmetry content already earned on the direct route.

## Theorem 1: current retained event-frame symmetry is not transitive

On the primitive 16-event frame, the currently retained direct event-frame
symmetry `G_ret = S_3` has exactly eight orbits, classified by the pair

`(t,w) in {0,1} x {0,1,2,3}`.

### Proof

The temporal bit is fixed by `S_3`, so `t = eta_t` is invariant.

The spatial Hamming weight

`w = eta_x + eta_y + eta_z`

is also invariant under spatial permutation.

Conversely, if two bit strings have the same pair `(t,w)`, then one can
permute the spatial axes to map one support set to the other. So the pair
`(t,w)` classifies the exact `S_3` orbit.

There are eight such pairs, so there are eight orbits.

Therefore the current retained exact event-frame symmetry is not transitive on
the full primitive 16-event frame.

## Corollary 1: current retained event-frame symmetry leaves a 7-parameter family

An event-frame source-free candidate state invariant only under `G_ret = S_3`
has the exact form

`rho = sum_(t=0)^1 sum_(w=0)^3 a_(t,w) Pi_(t,w)`,

with

- `a_(t,w) >= 0`,
- `sum_(t,w) binom(3,w) a_(t,w) = 1`.

So the source-free family has eight orbit weights and one normalization
equation, hence exact affine dimension `7`.

This reproduces the retained underdetermination exactly.

## Theorem 2: transitive event-frame invariance implies traciality

Assume:

1. `rho` is diagonal on the primitive event frame `{P_eta}`;
2. `rho` is normalized;
3. `rho` is invariant under a transitive relabeling group `G_evt` acting on the
   sixteen primitive projectors.

Then

`rho_cell = I_16 / 16`.

### Proof

Write

`rho = sum_eta p_eta P_eta`.

If `G_evt` is transitive on the primitive event frame, then for any two
primitive projectors `P_eta`, `P_xi`, there exists `g in G_evt` with

`g(P_eta) = P_xi`.

Invariance of `rho` under `G_evt` therefore implies

`p_eta = p_xi`

for all `eta, xi`.

So every atomic weight equals one common value `c`.

Normalization gives

`16 c = 1`,

hence

`c = 1/16`.

Therefore

`rho_cell = sum_eta (1/16) P_eta = I_16 / 16`.

So source-free local traciality follows immediately from transitive
event-frame invariance.

## Corollary 2: direct Planck closure under primitive event-frame transitivity

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

If Theorem 2 holds, then

`rho_cell = I_16 / 16`.

Because `P_A` has rank `4`,

`c_cell = Tr((I_16 / 16) P_A) = 4/16 = 1/4`.

Then the direct coefficient chain closes:

`a^2 = l_P^2`,

hence

`a = l_P`.

## What current direct worldtube and physical-lattice semantics do support

They support three important pieces:

1. **primitive events are physical**: the cell basis is not a disposable
   regulator fiction;
2. **proper quotienting is disallowed on retained physical sectors**: one may
   not simply throw away exact event content and still claim to be on the same
   physical surface;
3. **the full packet `P_A` is the right minimal one-step boundary object**:
   the direct counting law closes on that packet already.

So the event-frame route is not philosophically random. It is pointed at the
right physical object: source-free local occupancy on the exact physical cell.

## What current direct worldtube and physical-lattice semantics do not support

They do **not** yet provide an exact theorem identifying all sixteen primitive
projectors in one source-free orbit.

Concretely, current retained exact structure does not yet supply:

- an exact symmetry exchanging the vacuum with a one-hot event;
- an exact symmetry exchanging Hamming-weight-one and Hamming-weight-two
  events;
- an exact symmetry exchanging the temporal one-hot event with a spatial
  one-hot event on the full primitive source-free event frame.

Those are precisely the moves needed to collapse the eight retained `S_3`
orbit classes to one orbit.

So the exact missing content is now sharp:

> a theorem of primitive event-frame transitivity, or equivalently a theorem
> that the source-free local state has no preferred primitive projector on the
> full `C^16` cell.

## Why the older full-flip witness is still useful but not canonical

The older full local bit-flip witness is still a sufficient route because the
full translation/flip action on `{0,1}^4` is transitive.

But that is stronger than the real missing content.

The exact theorem target is not:

- "the full bit-flip group is exact."

It is:

- "the source-free local primitive event frame is transitive."

Any transitive event-frame relabeling law would do.

So the clean conceptual object is event-frame transitivity / no preferred
primitive projector, not the specific full-flip witness.

## Honest status

This route does **not** close retained Planck on the current accepted stack.

What it does achieve exactly is:

- it shows the current retained event-frame symmetry is only `S_3`, not
  transitive;
- it identifies the exact obstruction as missing transitivity on the primitive
  event frame;
- it proves that any transitive event-frame law would force traciality and
  close the direct Planck route immediately.

So the strongest honest status is:

- **not retained closure**
- **not yet an axiom-native retained Planck derivation**
- **sharpest exact remaining need:** primitive event-frame transitivity / no
  preferred primitive projector on the full source-free `C^16` cell

## Safe wording

**Can claim**

- the direct Planck route is now reduced to a primitive event-frame state law;
- current retained direct symmetry is only `S_3`, leaving eight event-frame
  orbits and a 7-parameter source-free family;
- transitive primitive event-frame invariance would force the tracial state
  and close Planck immediately.

**Cannot claim**

- that the current accepted retained stack already provides transitivity on the
  primitive event frame;
- that the event-frame route is already retained closure;
- that `a = l_P` has already been derived axiom-natively on this branch.
