# Planck-Scale Boundary Same-Source Covariance Theorem

**Date:** 2026-04-23
**Status:** derivation of same-source covariance for the Schur and event boundary generators
**Verifier:** `scripts/frontier_planck_boundary_same_source_covariance_theorem.py`

## Question

The finite-source event Ward theorem derives

`d/ds log Tr(rho_cell exp(s P_A))|_(s=0) = Tr(rho_cell P_A)`.

The Schur boundary action has normal-ordered pressure

`p_Schur = nu - lambda_min(L_Sigma)`.

Why must these two generators be equal?

## Result

They are equal if both are retained as representations of the same primitive
gravitational boundary-action source on the same physical cell.

The proof is a uniqueness theorem for a source-free local boundary action
generator:

> a source-free primitive boundary cell cannot carry two inequivalent
> infinitesimal generators for the same boundary action source.

If the Schur generator and the event generator differed by

`Delta := p_Schur - p_event`,

then the quotient of the two one-parameter source groups would be

`exp(s Delta)`.

That is a source-free local boundary-action scalar. It is not attached to a
retained primitive incidence charge, not a Schur floor term, and not a prepared
source. Therefore it is hidden boundary-action data.

The source-free primitive boundary-action surface forbids such data, so

`Delta = 0`.

Thus

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

## Inputs

This theorem uses:

1. the exact Schur boundary generator after floor subtraction,

   `p_Schur = nu - lambda_min(L_Sigma)`;

2. the finite primitive event source,

   `U_A(s) = exp(s P_A)`;

3. its Ward generator,

   `p_event = d/ds log Tr(rho_cell U_A(s))|_(s=0)`;

4. the single-source requirement:
   both are claimed to represent the same source-free one-cell gravitational
   boundary action;
5. no hidden local boundary-action scalar:
   a mismatch between two same-source generators would be extra local action
   data with no retained carrier.

The theorem does not assume the value of `p_event`. That value is derived by
the finite event Ward theorem. This theorem proves that the Schur generator
must equal it if both descriptions are descriptions of the same physical
boundary action source.

## Theorem 1: same-source one-parameter groups have equal infinitesimal generators

Let two scalar one-parameter source groups be

`U_1(s) = exp(s p_1)`,

`U_2(s) = exp(s p_2)`.

If both represent the same physical source parameter `s`, then their quotient

`Q(s) := U_1(s) U_2(s)^(-1)`

must be the identity group.

Since

`Q(s) = exp(s (p_1 - p_2))`,

this is equivalent to

`p_1 = p_2`.

If `p_1 != p_2`, then `Q(s)` is a new source-free scalar action group. That is
a second boundary-action source hidden inside the same physical parameter.

## Theorem 2: Schur/event mismatch is hidden boundary-action data

Set

`p_1 = p_Schur = nu - lambda_min(L_Sigma)`,

and

`p_2 = p_event = d/ds log Tr(rho_cell exp(s P_A))|_(s=0)`.

If

`p_Schur != p_event`,

then

`Delta = p_Schur - p_event`

generates the quotient group

`exp(s Delta)`.

This group has no support on a retained primitive event charge. The retained
event charge has already been exhausted by `P_A`. It is also not the Schur
floor, because the floor was removed by normal-ordering. It is not a prepared
source, because the cell is source-free.

Therefore `Delta` is precisely hidden local boundary-action data.

No-hidden source-free boundary-action semantics force

`Delta = 0`.

Thus

`p_Schur = p_event`.

## Theorem 3: same-source covariance gives the Planck density

The finite event Ward theorem gives

`p_event = Tr(rho_cell P_A)`.

Same-source covariance gives

`p_Schur = p_event`.

Since

`p_Schur = nu - lambda_min(L_Sigma)`,

we obtain

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

On the source-free primitive cell,

`rho_cell = I_16 / 16`,

and

`rank(P_A) = 4`,

so

`Tr(rho_cell P_A) = 1/4`.

On the exact rational witness,

`lambda_min(L_Sigma) = 1`,

so

`nu = 5/4`.

## What This Closes

This closes the specific objection:

> the finite event Ward derivative is real, but why should it equal the Schur
> normal-ordered pressure?

Answer:

> if the Schur boundary action and primitive event source are the same
> gravitational boundary-action source, unequal generators create a hidden
> source-free local boundary-action scalar.

## Remaining Rejection

The remaining rejection is no longer a coefficient objection, a Ward-derivative
objection, or a same-source covariance objection.

It is:

> deny that the Schur boundary action and the primitive event insertion source
> are two representations of the same physical gravitational boundary action.

That denial changes the target. It says one of the two retained descriptions is
not the gravitational boundary-action source.
