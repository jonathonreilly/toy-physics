# Planck-Scale Hbar Non-Homogeneous Real Action-Unit Reduction Theorem

**Date:** 2026-04-24
**Status:** conditional closure plus no-go/reduction for `Phi(I_16)=1`
**Verifier:** `scripts/frontier_planck_hbar_nonhomogeneous_real_action_unit_reduction_2026_04_24.py`

## Question

After the primitive phase trace reduction

`Phi(P) = gamma Tr(P) / 16`,

can the remaining hbar/action-unit scalar

`gamma = Phi(I_16)`

be closed by a genuinely non-homogeneous primitive real action-unit theorem,
without reusing homogeneous trace/naturality, without invoking bare `U(1)`
periodicity, and without treating finite roots alone as real action units?

## Verdict

The clean theorem-grade result is a necessary-and-sufficient reduction.

If the following non-homogeneous primitive real action-unit law is derived,
then the hbar lane closes at the reduced-action level:

> the complete source-free primitive `C^16` event cell `A_cell = I_16` is the
> indecomposable generator of the real primitive action monoid, and the reduced
> real action coordinate is the generator-count coordinate.

Equivalently,

`Phi(A_cell) = Phi(I_16) = 1`.

Under that law,

`gamma = 1`,

so

`q_atom = 1/16`,

`kappa_info = 1/32 per bit`,

and on the minimal cubical defect

`a^2 / l_P^2 = 1`.

But this document does **not** derive the non-homogeneous action-unit law from
the current bare event algebra. It proves that every currently viable strong
route must supply exactly that law, or an equivalent real-action generator
normalization. Therefore the hbar/action-unit status is **conditional**, not
unconditionally closed.

## Definition: Primitive Real Action-Unit Law

Let `A_cell := I_16` denote one complete source-free primitive `C^16` event
cell.

A primitive real action-unit theorem must provide three objects before
exponentiation:

1. an ordered additive primitive action monoid `M_action`;
2. an identification of the one-cell history with an indecomposable generator
   `[A_cell] in M_action`;
3. a reduced real action coordinate
   `Phi_action: M_action -> R_{\ge 0}` satisfying

`Phi_action(n [A_cell]) = n`

for every nonnegative integer `n`.

The one-cell case is the missing hbar lock:

`Phi_action([A_cell]) = 1`.

This is non-homogeneous. If `Phi_action` is replaced by

`lambda Phi_action`

with `lambda != 1`, the trace shape and additivity survive, but the
generator-count coordinate condition fails:

`(lambda Phi_action)([A_cell]) = lambda`.

So this law is exactly the scale-breaking input that the previous
homogeneous no-go demanded.

## Theorem 1: Conditional Gamma-One Closure

Assume the already established trace-reduced shape on the primitive event
projectors:

`Phi(P) = gamma Tr(P) / 16`.

Do not use trace/naturality to set `gamma`; use only the non-homogeneous
primitive real action-unit law above.

Since `A_cell = I_16` is the action-monoid generator and the reduced action
coordinate is generator count,

`gamma = Phi(I_16) = Phi_action([A_cell]) = 1`.

Therefore

`Phi(P_eta) = 1/16`

for each primitive event atom `P_eta`.

On the time-locked elementary information carrier,

`I_* = log 4 = 2 bits`,

so

`kappa_info = (1/16) / 2 = 1/32 per bit`.

On the minimal cubical defect with

`eps_* = pi/2`,

the action-phase reduction gives

`a^2 / l_P^2 = 8 pi (1/16) / (pi/2) = 1`.

This is a reduced-action-unit closure, not a prediction of the SI decimal
value of `hbar`.

## Theorem 2: Equivalence With The Missing Gamma Statement

Given the trace-reduced primitive phase law, the following are equivalent:

1. `gamma = 1`;
2. `Phi(I_16) = 1`;
3. the complete primitive `C^16` event cell carries one reduced real action
   unit;
4. the primitive action monoid coordinate agrees with generator count on the
   one-cell generator.

The equivalence is immediate because `gamma` is defined by

`gamma := Phi(I_16)`.

Thus the remaining problem is not another shape theorem. It is exactly the
existence and derivation of the generator-count real action coordinate.

## No-Go Lemma: Omitting The Unit Law Leaves A Scale Model

Let `Phi_1(P) = Tr(P)/16`.

For any positive `lambda`, define

`Phi_lambda(P) = lambda Tr(P)/16`.

Then `Phi_lambda` is still finitely additive, positive, source-free on atoms,
and supported on the same primitive event algebra. It also preserves any
homogeneous Ward balance of the form `delta Phi = 0`.

But

`Phi_lambda(I_16) = lambda`.

So all homogeneous conditions admit both `lambda = 1` and `lambda = 2`, while
only the non-homogeneous action-unit law rejects `lambda = 2`.

This is the minimal countermodel to any proof that claims `gamma = 1` from the
current homogeneous premises alone.

## Route Audit

### 1. Noncompact Central Action Generator

A noncompact central lift

`0 -> R_action -> G_hat -> G -> 1`

is the right kind of move because it replaces periodic phase classes with a
real pre-exponential action coordinate.

It still does not fix the unit by itself. The central line has automorphisms

`t -> lambda t`, with `lambda > 0`.

Thus a real central generator closes `gamma = 1` only if the lift also derives
a primitive integral action lattice or monoid

`Z_{\ge 0} [A_cell] subset R_action`

and proves that one complete primitive cell lifts by exactly one generator.

That added statement is precisely the primitive real action-unit law. Without
it, the route only moves the ambiguity from periodic phase to real central
scale.

### 2. Spectral-Flow / Index-One Primitive Pair

An index route can close the target if it constructs a canonical primitive
Dirac/Fredholm pair `D_cell` and proves

`Index(D_cell) = SF(D_cell) = 1`

for one complete primitive event cell.

Index one alone is not yet enough. If the reduced action is only known to be

`Phi = c Index`

with an unconstrained positive constant `c`, then

`Phi(I_16) = c`.

The index route closes hbar only after it also proves the unit identification

`Phi = Index`

on the primitive cell. That is the same non-homogeneous generator-count law in
index language. The current branch has not constructed the canonical
`D_cell`, the invariant one-cell spectral-flow path, or the action-index unit
map.

### 3. Primitive Action Monoid

This is the sharpest viable route.

If the microscopic ontology proves that primitive source-free action histories
form the free ordered monoid

`M_action = N [A_cell]`

and that the reduced real action coordinate is the unique generator-count
coordinate on that monoid, then `gamma = 1` follows immediately.

What remains open is not algebraic manipulation. It is the physical theorem
that the real action coordinate is the primitive count coordinate rather than

`lambda` times that coordinate.

### 4. Microscopic Action Ward Normalization

A Ward identity can close the target only if its source parameter is already
the reduced real action coordinate and the complete primitive cell has Ward
charge one:

`d/ds log Z_cell(s) |_{s=0} = 1`.

If the source parameter can be rescaled,

`s -> lambda s`,

or if the Ward equation only states a homogeneous balance, then the same
scale model survives.

Therefore the Ward route must derive a unit-calibrated microscopic action
source, not merely a conserved current or a stationary variation.

## What Is Closed

This document closes the form of the missing hbar theorem:

> `gamma = 1` is equivalent to a non-homogeneous primitive real action-unit
> theorem selecting `I_16` as one generator of reduced real action.

It also proves that the following do not close the target by themselves:

- homogeneous trace/naturality;
- homogeneous Ward balances;
- bare `U(1)` periodicity;
- finite roots of unity alone;
- a noncompact real central line without an integral primitive generator;
- an index-one count without the action-index unit map.

## What Remains Open

The current branch has not derived the primitive real action-unit law from the
bare lattice/event stack.

So the hbar/action-unit closure is:

**conditional** on deriving or accepting the non-homogeneous primitive real
action-unit theorem.

The viable next targets are exactly:

1. derive the primitive action monoid `M_action = N [I_16]` and its generator
   count as reduced real action;
2. derive a noncompact central action lift with a primitive integral generator
   and one-cell lift equal to one;
3. construct a canonical primitive Dirac/Fredholm pair with spectral flow one
   and a unit action-index identification;
4. derive a microscopic Ward source whose identity derivative is the reduced
   action coordinate with one-cell charge one.

## Safe Claim

Use:

> The hbar lane is now reduced to a necessary-and-sufficient non-homogeneous
> theorem: the complete primitive `C^16` event cell must be the generator of
> reduced real action, so `Phi(I_16)=1`. If that primitive action-unit law is
> derived, then `q_atom=1/16`, `kappa_info=1/32` per bit, and the minimal
> cubical defect gives `a^2/l_P^2=1`.

Do not use:

> The branch derives `gamma = 1` from the current bare trace/naturality stack.

Do not use:

> Bare `U(1)` periodicity or finite roots alone derive the real action value
> `gamma = 1`.

Do not use:

> The SI decimal value of `hbar` is predicted.
