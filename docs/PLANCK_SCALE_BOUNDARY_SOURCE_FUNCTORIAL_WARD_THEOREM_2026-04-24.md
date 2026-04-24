# Planck-Scale Boundary Source Functorial Ward Theorem

**Date:** 2026-04-24
**Status:** hostile-review hardening of the Schur/event Ward bridge
**Verifier:** `scripts/frontier_planck_boundary_source_functorial_ward_theorem.py`

## Question

Is the equality

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`

really a derived Ward identity, or is it still an imported physical readout
law?

## Result

The finite event derivative is purely algebraic:

`d/ds log Tr(rho_cell exp(s P_A))|_(s=0) = Tr(rho_cell P_A)`.

The equality to the Schur normal-ordered pressure is not derived from the
scalar Schur observable grammar alone. It is derived only after one additional
retained object-class statement:

> the Schur normal-ordered boundary action and the faithful event insertion are
> two functorial representations of the same parent one-cell boundary source
> `B_parent = (H_A, P_A)`.

With that parent-source representation statement, unequal generators would
define an extra one-dimensional source-free boundary-action character

`chi_Delta(s) = exp(s Delta)`,

where

`Delta = (nu - lambda_min(L_Sigma)) - Tr(rho_cell P_A)`.

That character has no support on a retained primitive incidence, is not the
Schur floor, and is not a prepared source. On the source-free primitive
boundary-action object class it is inadmissible. Therefore `Delta = 0`.

This is the precise Ward bridge. It is not a conventional continuum
path-integral Ward identity with an invariant measure. It is the finite
source-functoriality identity of the retained primitive boundary-action source.

## Definitions

The parent boundary source is

`B_parent := (H_A, P_A)`,

with

`H_A = span{|t>, |x>, |y>, |z>}`

and

`P_A = P_t + P_x + P_y + P_z`.

An admissible source representation of `B_parent` must:

1. preserve the same source parameter `s`;
2. preserve unit charge on retained primitive incidences;
3. not add a source-free scalar character;
4. not quotient away retained physical multiplicity.

The faithful event representation is

`R_event(B_parent): U_A(s) = exp(s P_A)`.

The Schur representation is the quotient-shape representation plus retained
doublet multiplicity:

`R_Schur(B_parent): H_A = H_q (+) E`,

where `H_q = span{|t>, |s>}` is the permutation-blind quotient and `E` is the
retained spatial doublet complement.

The Schur floor `lambda_min(L_Sigma)` is not source charge. It is the exact
normal-ordering floor of the reduced Schur operator. The Schur source
generator after floor subtraction is

`p_Schur = nu - lambda_min(L_Sigma)`.

## Theorem 1: event Ward derivative

Because `P_A` is a projector,

`exp(s P_A) = I + (e^s - 1) P_A`.

Thus

`Z_A(s) = Tr(rho_cell exp(s P_A))`

has identity-source derivative

`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A)`.

This theorem alone does not mention `nu`.

## Theorem 2: source-functoriality forces equal generators

Let

`p_event = Tr(rho_cell P_A)`

and

`p_Schur = nu - lambda_min(L_Sigma)`.

If event and Schur are functorial representations of the same parent source,
then the quotient of their one-parameter source groups is

`chi_Delta(s) = exp(s (p_Schur - p_event))`.

If `Delta != 0`, this is a new one-dimensional boundary-action character. It
is invisible to the parent incidence support `P_A`, invisible to the Schur
floor after normal-ordering, and not carried by any retained boundary event.

Therefore it is hidden source-free boundary-action data.

The retained source-free primitive boundary-action object class forbids such a
character, hence

`Delta = 0`.

So

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

## What This Does And Does Not Prove

This closes the reviewer objection only **inside** the retained parent-source
boundary-action object class.

It does prove:

1. the finite event derivative is exact;
2. the Schur/event equality follows from parent-source functoriality plus no
   hidden one-dimensional source-free character;
3. the equality does not come from the scalar Schur vacuum observable
   `p_vac = (1/(2n)) log det(L_Sigma)`;
4. the value `1/4` is not inserted into the Schur side.

It does not prove:

1. that a reviewer must accept the primitive boundary-action object class;
2. that ordinary scalar Schur pressure equals `1/4`;
3. a conventional path-integral Ward identity with a continuum invariant
   measure;
4. bare `Cl(3)` / `Z^3` gravity without the parent-source boundary-action
   interpretation.

## What Would Stop This

The exact remaining rejection is:

> the Schur normal-ordered boundary action is not a functorial representation
> of the same parent source `B_parent = (H_A, P_A)` as the event insertion.

If that rejection is accepted, the finite event Ward derivative remains true
but does not determine `nu`. The Planck branch then falls back to a retained
primitive counting theorem plus a conditional gravity-carrier identification,
not an unqualified bare-axiom Planck closure.

## Safe Claim

Use:

> The boundary Ward bridge is a finite parent-source functoriality theorem. It
> closes the Schur/event equality inside the retained primitive boundary-action
> object class by forbidding an extra source-free one-dimensional character.

Do not use:

> The scalar Schur observable principle alone derives the quarter.

Do not use:

> The branch derives a conventional continuum path-integral Ward identity.
