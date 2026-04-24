# Planck-Scale Parent-Source Discharge After Realification Theorem

**Date:** 2026-04-24
**Status:** closes the parent-source object-class objection after B3 realification
**Verifier:** `scripts/frontier_planck_parent_source_discharge_after_realification_theorem_2026_04_24.py`

## Question

After B3 realification derives the metric/coframe Ward response, is the
gravitational boundary parent-source object class still an independent
physical assumption?

## Result

No, once canonical realified B3 is accepted.

The previous parent-source naturality obstruction was correct before B3 was
closed: the Schur carrier diagram commuted, but an affine hidden character

`chi_delta(s) = exp(s delta)`

could still be attached to the scalar Schur normalization unless the
Schur-normal-ordered boundary action was accepted as the functorial
representation of the same parent source.

After B3 realification, the gravity sector is no longer an imported object
class. It is the realified edge-Clifford coframe response on the same primitive
one-cell boundary surface. On that surface, the local source-free boundary
representative must be:

1. local on one primitive boundary cell;
2. supported on primitive one-step incidences;
3. additive over disjoint primitive incidences;
4. time-complete;
5. spatially isotropic;
6. unit-valued on retained primitive incidences;
7. free of quotienting of retained multiplicity;
8. free of source-free one-dimensional scalar characters.

The unique representative satisfying these conditions is

`P_A = 1_(|eta| = 1)`.

Therefore the parent source is not an extra postulate after realified B3:

`B_parent = (H_A, P_A)`

is forced by the derived gravity response surface and the primitive boundary
cell.

## Theorem 1: B3 realification puts gravity on the primitive boundary surface

The B3 Clifford realification theorem derives the coframe response as

`Hom_R(Z^3 tensor_Z R, Cl_1(3))`.

The boundary source conjugate to this response is local on the same primitive
cell and is additive over one-step boundary incidences. No independent scalar
Schur object is introduced at this stage.

Thus the gravitational boundary representative must be a primitive incidence
operator on the same cell, not an unrelated scalar free-energy readout.

## Theorem 2: the primitive incidence representative is unique

On the one-cell event frame, the primitive one-step incidence shell has four
axis events: one time event and three spatial events.

Time-completeness includes the time incidence. Spatial isotropy treats the
three spatial incidences equally. Unit valuation assigns charge one to each
retained primitive incidence. Additivity forbids replacing the shell by a
nonlinear scalar function of the shell.

Therefore the unique operator is

`P_A = P_t + P_x + P_y + P_z`.

Any alternative fails one of the conditions:

- `P_t` is not spatially complete;
- `P_x + P_y + P_z` is not time-complete;
- `alpha P_A` with `alpha != 1` violates unit valuation;
- a quotient projector loses retained spatial-doublet multiplicity;
- `P_A + delta I` adds a source-free scalar character not supported on
  primitive incidence.

## Theorem 3: the hidden character is excluded

The parent-source naturality obstruction left the family

`p_Schur(delta) = Tr(rho_cell P_A) + delta`.

After B3 realification, `delta I` is not a boundary incidence source. It is not
a coframe response source, not the Schur floor, not a primitive event
insertion, and not retained multiplicity.

It is exactly a source-free one-dimensional scalar character. The derived
realified gravity response has no slot for such a character. Hence

`delta = 0`.

So

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`.

## Consequence

The parent-source objection is discharged:

> Before B3, parent-source functoriality was a retained physical object-class
> statement. After realified B3, the same source is forced as the unique
> primitive incidence representative of the derived gravitational coframe
> response.

The only remaining way to reopen the objection is to reject B3 realification
itself. If realification is accepted, the parent-source object class is no
longer a separate primitive.

## Safe Claim

Use:

> Realified B3 derives the gravitational response on the primitive boundary
> surface; locality, one-step support, time-completeness, spatial isotropy,
> unit valuation, multiplicity retention, and no hidden scalar character force
> `B_parent = (H_A, P_A)`.

Do not use:

> The scalar Schur free-energy observable alone derives the parent source.

Do not use:

> The hidden affine character is excluded before the gravity response surface is
> derived or accepted.
