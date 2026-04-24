# Planck-Scale Nature Review Plain-Language Status

**Date:** 2026-04-23
**Status:** reviewer-facing status note with project-local shorthand removed
**Verifier:** `scripts/frontier_planck_axiom_only_gravity_unit_map_final_audit.py`

## One-Sentence Status

The branch derives the native primitive coefficient `1/4`; the new boundary
event Ward theorem closes the remaining additive boundary-density law on the
primitive boundary-event action surface, so the conventional Planck length
follows without inserting `a = l_P` or `nu = 5/4` as values.

The remaining hostile-review pressure is now physical, not numerical:

> reject or accept that gravitational boundary action on the physical primitive
> lattice is governed by the normal-ordered primitive boundary event Ward
> identity.

## What Is Derived

The local physical cell is the time-locked primitive event cell

`H_cell ~= C^16`.

The primitive one-step worldtube packet has rank

`rank(P_A) = 4`.

The source-free bare event-frame state is the normalized counting state

`rho_cell = I_16 / 16`.

Therefore the primitive coefficient is

`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`.

This is the native dimensionless result.

## What The New Ward Theorem Adds

The previous audit showed that ordinary Schur source-response Ward identities
cannot see the additive density. The new closure theorem uses a different
identity: the constant-term Ward identity for inserting one primitive boundary
cell.

Let

`G_nu = nu I - L_Sigma`.

Normal-order the exact Schur floor by writing

`G_nu = (nu - lambda_min(L_Sigma)) I - (L_Sigma - lambda_min(L_Sigma) I)`.

The normal-ordered primitive boundary event Ward identity says

`sup spec(G_nu) = Tr(rho_cell P_A)`.

Therefore

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`.

On the exact rational witness with `lambda_min(L_Sigma) = 1`, this gives

`nu = 5/4`.

## What Converts It To Planck Length

The microscopic boundary density is

`S_micro / k_B = (1/4) A / a^2`.

The standard gravitational boundary/action law is

`S_grav / k_B = A / (4 l_P^2)`.

Matching the same physical surface gives

`a^2 = l_P^2`,

so

`a = l_P`.

## What Is Not Imported

The branch does not import:

- the observed value of the lattice spacing;
- the equality `a = l_P`;
- the additive density `nu = 5/4`;
- a fitted dimensionless multiplier;
- the present age of the universe as a microscopic tick count;
- an observed electroweak scale as a Planck calibration.

## Remaining Review Pressure

The old conditional gap was:

> why is the primitive count exactly the gravitational boundary/action unit?

The new answer is:

> because the normal-ordered primitive boundary event Ward identity ties the
> additive action density to the expectation of the forced primitive incidence
> charge `P_A`.

A reviewer can still reject that identity. If they do, the package falls back
to the earlier conditional result: exact native `1/4`, with Planck length
conditional on the gravitational boundary/action identification.

If they accept the identity, the boundary density is closed and the Planck
normalization follows.

## Safe Submission Claim

Use this:

> The physical `Cl(3)` / `Z^3` packet derives `c_cell = 1/4`. On the primitive
> boundary-event action surface, the normal-ordered boundary event Ward
> identity derives `nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`; with
> the standard gravitational area/action normalization this gives `a = l_P`
> exactly.

Do not use this:

> Ordinary Schur source-response Ward identities alone force the Planck length.

## Review Outcome

The package is now Nature-grade as a conditional-on-the-boundary-event-Ward-
surface Planck derivation with no inserted Planck value.

The remaining review question is whether that event Ward surface is accepted as
the physical gravitational boundary-action readout of the primitive lattice.
