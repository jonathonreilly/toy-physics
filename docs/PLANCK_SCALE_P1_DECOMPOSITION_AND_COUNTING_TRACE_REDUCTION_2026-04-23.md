# Planck-Scale P1 Decomposition and Counting-Trace Reduction

**Date:** 2026-04-23
**Status:** branch-local reduction of Axiom Extension P1 to its only load-bearing clause
**Audit runner:** `scripts/frontier_planck_p1_decomposition_and_counting_trace_reduction.py`

## Question

What exactly is Axiom Extension P1 doing in the Planck packet?

More sharply:

> Is P1 a large new axiom, or is it mostly bookkeeping around one remaining
> source-free counting-state rule?

## Bottom line

P1 is not a new numerical input. It is a local state-semantics extension.

After decomposition, only one part is genuinely load-bearing for the Planck
number:

> the bare source-free primitive event frame carries no preferred primitive
> event.

Everything else in P1 is either already upstream, definitional, or a guardrail
against confusing readout operators with hidden preparation data.

The best reduction target is therefore not "derive all of P1." It is:

> reduce the no-preferred-event state law to the normalized counting trace on
> the primitive finite event frame.

On that reduction, `rho_cell = I_16/16` is not a dynamical vacuum-state
assumption. It is the normalized counting functional on the 16 primitive event
atoms.

## P1 decomposed

P1 currently says:

1. a primitive physical cell has finite local Hilbert/event semantics;
2. primitive cell events are physical event projectors, not regulator artifacts;
3. local information cannot appear in a source-free cell as hidden preparation
   data;
4. a source-free bare cell carries no preferred primitive event unless such a
   preference is supplied by an explicit source, preparation, boundary condition,
   or dynamical embedding;
5. readout operators may be invariantly defined on the physical event frame, but
   they are not themselves hidden state-preparation data.

These clauses have different status.

## Clause status

### P1.1: finite local Hilbert/event semantics

This is not the Planck-lane novelty. It is supplied by the accepted
Hilbert/locality surface and the time-locked primitive-cell construction:

`H_cell = C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16`.

### P1.2: primitive events are physical

This is supplied by the physical-lattice reading. The event frame is not a
regulator artifact to be quotiented away after the fact.

### P1.3: no hidden preparation in a source-free cell

This is the source-free meaning of the one-axiom information surface. A
nonuniform local state carries local information. If no source, preparation,
boundary condition, or dynamical embedding is supplied, that information cannot
be smuggled in as an unnamed state parameter.

### P1.4: no preferred primitive event

This is the real load-bearing state law.

For the primitive event frame

`E = {P_eta : eta in {0,1}^4}`,

P1.4 says the bare source-free cell has no distinguished atom of `E`.

Equivalently, the source-free local functional on primitive events is the
normalized counting trace:

`tau(P_eta) = 1/16`

for every primitive atom.

This is the only clause that fixes the Planck coefficient.

### P1.5: readout is not preparation

This is a guardrail. The packet readout

`P_A = 1_{N_evt = 1}`

is a physical observable. Its existence does not mean the bare cell state is
prepared inside or outside `P_A`.

## Counting-trace reduction

If the elementary Planck coefficient is a kinematic primitive-cell counting
coefficient, then the relevant local functional is not an arbitrary density
matrix selected by a Hamiltonian or global vacuum.

It is the normalized finite counting functional on the primitive event frame:

`tau(X) = Tr(X) / dim(H_cell)`

on event-frame projectors.

For the exact cell,

`dim(H_cell) = 16`.

For the worldtube packet,

`rank(P_A) = 4`.

Therefore

`tau(P_A) = Tr(P_A) / 16 = rank(P_A) / 16 = 4/16 = 1/4`.

In density-matrix notation this same normalized trace is represented by

`rho_count = I_16 / 16`.

The important point is object-class:

> `I_16/16` is being used as the normalized counting trace of the primitive
> finite event algebra, not as a claim about every local reduced physical vacuum.

## Why this is stronger than "choose the maximally mixed state"

A nonuniform event weighting has the form

`omega(P_eta) = p_eta`,

with

`p_eta >= 0`,

`sum_eta p_eta = 1`.

That is a 15-parameter local datum. Unless supplied by a source, preparation,
boundary condition, or dynamical embedding, it is hidden state data.

The normalized counting trace has no such parameter:

`p_eta = 1/16`

for every primitive event.

So the source-free counting read is not:

> pick the maximally mixed vacuum.

It is:

> evaluate the kinematic count operator by normalized primitive-event counting.

## What remains if a reviewer rejects this reduction

If a reviewer says the coefficient must be a physical density-matrix expectation
rather than a normalized counting functional, then P1.4 remains an explicit
state-law axiom.

That is the exact remaining fork:

1. **counting-trace reading accepted:** P1.4 is reduced to normalized finite
   counting on the primitive event frame;
2. **state-expectation reading imposed:** P1.4 remains an explicit
   source-free state-selection axiom.

So the next axiom-native target is not vague. It is:

> prove that the elementary Planck coefficient belongs to the normalized
> primitive counting-trace object class, not to the dynamical state-expectation
> object class.

That target is already supported by the kinematic cell-coefficient and
primitive-coefficient object-class theorems. This note isolates it as the exact
place where P1 can be reduced rather than merely promoted.

## Follow-up close

The normalized counting-trace object class is now proved directly in:

- [PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md)

That theorem shows that object-class locality, positivity, normalization,
finite additivity, and atomic naturality uniquely force

`tau(P) = rank(P) / 16`

on the primitive `C^16` event frame.
