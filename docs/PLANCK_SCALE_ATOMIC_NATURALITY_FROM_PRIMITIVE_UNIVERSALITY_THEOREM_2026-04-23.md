# Planck-Scale Atomic Naturality from Primitive Universality Theorem

**Date:** 2026-04-23
**Status:** branch-local theorem/scoping note for remaining issue #1
**Audit runner:** `scripts/frontier_planck_atomic_naturality_from_primitive_universality_theorem.py`

## Question

Can the atomic-naturality clause used in the primitive counting-trace theorem be
earned from primitive universality and object-class locality, rather than being
silently equivalent to choosing the uniform state?

The clause at issue is U5 in:

- [PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md)

This note attacks only that clause. It does not edit the existing packet.

## Bottom line

Atomic naturality is a theorem if the elementary Planck coefficient is a
**bare primitive event-frame coefficient rule**:

`C_E(P)`,

where the primitive object is the finite event frame

`E = {P_eta : eta in {0,1}^4}`

and atom names are presentation labels, not physical preparation data.

Under that object-class reading, primitive universality says that isomorphic
presentations of the same primitive event frame receive the same coefficient
rule. Object-class locality says that the rule has no access to embedding,
state-preparation, boundary, Hamiltonian, or hidden atom-label data. Therefore
every relabeling of the sixteen primitive atoms is a presentation isomorphism,
and the coefficient must satisfy

`C_E(U_pi P U_pi^dagger) = C_E(P)`.

That is atomic naturality.

This proof does **not** assume `rho = I_16/16`. It does not even introduce a
density matrix. The uniform counting trace appears only later, after finite
additivity and normalization are added, exactly as in the existing universal
primitive counting-trace theorem.

However, if a reviewer insists that the coefficient object is richer, for
example

`(E, N_evt, P_A)`

or

`(E, P_A)`,

then full atomic naturality is not proved by object-class locality alone. One
gets only orbit-wise naturality under automorphisms preserving the extra
structure, and that weaker statement does not fix `C(P_A) = 1/4`. In that
enriched-object reading, no-preferred-primitive-event remains an additional
principle.

So the remaining fork is now sharp:

1. **Bare primitive coefficient rule accepted:** atomic naturality follows from
   primitive universality/object-class locality.
2. **Readout-enriched coefficient object imposed:** atomic naturality remains a
   source-free no-preferred-event principle, not a theorem of object locality
   alone.

## Inputs

This note links, but does not modify, the existing Planck packet:

- [PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md](./PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md)
- [PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_P1_DECOMPOSITION_AND_COUNTING_TRACE_REDUCTION_2026-04-23.md](./PLANCK_SCALE_P1_DECOMPOSITION_AND_COUNTING_TRACE_REDUCTION_2026-04-23.md)
- [PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md](./PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_EVENT_FRAME_NO_INFORMATION_STATE_THEOREM_2026-04-23.md](./PLANCK_SCALE_EVENT_FRAME_NO_INFORMATION_STATE_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md)

## Primitive setup

The exact primitive event frame is

`E = {P_eta : eta in {0,1}^4}`,

with sixteen rank-one atomic projectors on the time-locked primitive cell

`H_cell ~= C^16`.

An event-frame projector is a finite sum

`P_S = sum_(eta in S) P_eta`.

For a permutation `pi` of the sixteen atoms, let `U_pi` be the induced
permutation unitary, so

`U_pi P_eta U_pi^dagger = P_(pi eta)`.

The worldtube packet used later is

`P_A = sum_(|eta| = 1) P_eta`,

with `rank(P_A) = 4`.

## Definitions

### Bare primitive coefficient rule

A bare primitive coefficient rule is an assignment

`C_E(P_S) in R`

whose arguments are only:

1. the primitive event-frame object `E`;
2. the event-frame projector `P_S` being counted.

It is not a density-matrix expectation, and it does not contain a hidden
weight vector `(p_eta)`.

### Primitive universality

Primitive universality means that the same coefficient rule applies to every
isomorphic presentation of the primitive event frame. If

`phi : E -> E'`

is an isomorphism of primitive event frames, then

`C_(E')(phi(P)) = C_E(P)`.

For the same cell in two atom-label presentations, `phi` is just a relabeling
of the primitive atoms.

### Object-class locality

Object-class locality means that `C_E(P)` has access only to the primitive
object class just named. It does not depend on:

- a global embedding;
- a chosen reduced vacuum;
- a Hamiltonian;
- a boundary condition;
- a preparation datum;
- a hidden distinguished atom label;
- a chosen atom-name convention.

This is the coefficient-object version of the object-class separation already
isolated in:

- [PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md](./PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md)

### Atomic naturality

Atomic naturality is the statement

`C_E(U_pi P U_pi^dagger) = C_E(P)`

for every relabeling `pi` of the sixteen primitive atoms.

Equivalently, the coefficient rule is invariant under automorphisms of the
bare primitive event frame.

## Theorem 1: primitive universality plus object-class locality implies atomic naturality

Assume the coefficient is a bare primitive coefficient rule in the sense above.
Then primitive universality and object-class locality imply atomic naturality.

### Proof

Let `pi` be any permutation of the sixteen primitive atoms.

Because the bare primitive object is the event frame `E` itself, with atom
names treated as presentation labels, `pi` is an automorphism of the primitive
object. It gives an isomorphic presentation of the same event frame:

`P_eta -> P_(pi eta)`.

Primitive universality says that the coefficient rule is unchanged under such
an isomorphism:

`C_E(U_pi P U_pi^dagger) = C_E(P)`.

If this equality failed for some `pi` and `P`, the coefficient would depend on
which atom-name presentation was used. That would introduce hidden atom-label
data into the primitive coefficient object, contradicting object-class
locality.

Therefore the coefficient rule is invariant under every primitive atom
relabeling. This is atomic naturality.

No positivity, normalization, additivity, entropy maximization, or density
matrix has been used.

## Corollary: the existing counting-trace theorem may use U5 as earned on the bare object class

Once Theorem 1 supplies atomic naturality, the rest is the already-recorded
finite counting argument:

1. finite additivity gives `C(P_S) = sum_(eta in S) C(P_eta)`;
2. atomic naturality gives `C(P_eta) = C(P_xi)` for all atoms;
3. normalization gives `C(I) = 1`, hence `C(P_eta) = 1/16`;
4. therefore `C(P_S) = |S|/16`.

For the worldtube packet,

`|S_A| = rank(P_A) = 4`,

so

`C(P_A) = 4/16 = 1/4`.

This is exactly the normalized primitive counting trace proved in:

- [PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md)

## Why this does not smuggle in the uniform state

The proof of Theorem 1 is a coherence proof for a coefficient rule. It does
not start from

`rho_cell = I_16/16`,

does not maximize entropy, and does not assert that every physical state on
the cell is tracial.

The logical order is:

`primitive universality + object-class locality`

`-> atomic naturality of the coefficient rule`

`-> with additivity and normalization, normalized counting trace`.

The uniform trace is a conclusion of the last step. It is not a premise of the
first step.

## Sharp scoping: what weaker object classes actually prove

The theorem above depends on the coefficient object being the bare primitive
event-frame rule. If additional structure is treated as part of the object
whose automorphisms must be preserved, the automorphism group shrinks.

### Packet-preserving object

If the object is

`(E, P_A)`,

then relabelings are required to preserve `P_A`. There are at least two atom
orbits:

1. the four atoms inside `P_A`;
2. the twelve atoms outside `P_A`.

Finite additivity and normalization then allow

`C(P_eta) = alpha` for `eta in P_A`,

`C(P_eta) = beta` for `eta notin P_A`,

with

`4 alpha + 12 beta = 1`.

The packet coefficient is

`C(P_A) = 4 alpha`,

which is not fixed. For example,

`alpha = 1/32`,

`beta = 7/96`

is positive and normalized, packet-preserving, and gives

`C(P_A) = 1/8`.

So packet-preserving naturality alone does not prove quarter.

### Event-count-preserving object

If the object is

`(E, N_evt)`,

where

`N_evt = sum_eta |eta| P_eta`,

then automorphisms preserve Hamming weight. There are five atom orbits, with
sizes

`1, 4, 6, 4, 1`.

Finite additivity and normalization allow five orbit weights

`a_0, a_1, a_2, a_3, a_4`,

constrained only by

`a_0 + 4 a_1 + 6 a_2 + 4 a_3 + a_4 = 1`.

The packet coefficient is

`C(P_A) = 4 a_1`,

again not fixed by object-class locality alone.

### Retained residual spatial symmetry

If only the retained residual spatial `S_3` action is used, the primitive
atoms split into eight orbits labelled by temporal bit and spatial Hamming
weight. This is even weaker, matching the historical event-frame obstruction
recorded in:

- [PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_EVENT_FRAME_ROUTE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_TRACIALITY_EVENT_FRAME_ROUTE_2026-04-23.md)

## What is proved

This note proves:

- atomic naturality is not the same as selecting `rho = I_16/16`;
- for a bare primitive event-frame coefficient rule, atomic naturality follows
  from primitive universality and object-class locality;
- full atom relabeling is a coherence requirement on the primitive coefficient
  object class, not a dynamical vacuum-state assertion;
- weaker packet-preserving or readout-preserving naturality does not fix the
  Planck coefficient.

## What remains a principle

This note does not prove that every reviewer must accept the bare primitive
coefficient object class.

If the reviewer makes the Planck coefficient a readout-enriched coefficient object,
or a state-enriched object, then full atomic naturality remains an additional
source-free no-preferred-primitive-event principle. In the current branch that
principle is supplied by Axiom Extension P1 and its default-datum/no-information
state notes, not by packet-preserving symmetry alone.

This note also does not prove:

- every reduced local vacuum state is tracial;
- every prepared cell state is tracial;
- `P_A` is unphysical or erased;
- the gravitational area/action carrier identification.

The packet `P_A` remains the physical worldtube readout. The theorem concerns
the universal primitive coefficient rule used to evaluate event-frame
projectors, not the deletion of the readout.

## Hostile-review status

The reviewer-safe statement is:

> Atomic naturality is earned from primitive universality/object-class locality
> exactly when the Planck coefficient is treated as a bare primitive
> event-frame coefficient rule. If the coefficient object is enriched by
> readout-preserving or state-selecting data, object-class locality gives only
> orbit-wise invariance and the no-preferred-primitive-event law remains a
> separate principle.

Thus issue #1 is reduced to a precise object-class question, not a hidden
choice of the uniform state.
