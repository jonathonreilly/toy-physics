# Planck-Scale Bare Boundary Representative After Gravity Theorem

**Date:** 2026-04-23
**Status:** B4 conditional closure theorem
**Verifier:** `scripts/frontier_planck_bare_boundary_representative_after_gravity_theorem.py`

## Question

If B3 derives the gravitational boundary/action sector from the bare
`Cl(3)` / `Z^3` observable algebra, does any further physical identification
remain before the Planck representative is `P_A`?

## Result

No.

Once B3 is closed, B4 follows from the already-proven same-surface uniqueness
argument:

`N_grav = P_A`.

The reason is simple. A derived gravitational boundary/action sector must have a
source-free local primitive representative on the same one-cell boundary surface.
On the retained `Cl(3)` / `Z^3` primitive boundary cell, the unique
time-complete, spatially isotropic, unit-valued one-step incidence source is

`P_A = 1_(|eta| = 1)`.

Thus B4 has no independent coefficient freedom. It is conditional only on B3.

## Proof

Assume B3:

> the gravitational boundary/action sector is derived from the retained
> `Cl(3)` / `Z^3` observable algebra.

Then the sector is not imported. It is part of the same algebraic physical
surface as the primitive cell.

The microscopic source-free local representative must be:

1. local on one primitive boundary cell;
2. supported on primitive one-step incidences;
3. additive over disjoint primitive incidences;
4. time-complete;
5. spatially isotropic;
6. unit-valued on admitted primitive incidences;
7. free of quotienting of retained physical multiplicity.

The existing carrier theorem proves the unique operator satisfying these
conditions is

`P_A`.

Therefore

`N_grav = P_A`.

## Consequence

With the bare finite-cell canonical state,

`rho_cell = I_16 / 16`,

we get

`c_cell = Tr(rho_cell N_grav) = Tr((I_16/16) P_A) = 1/4`.

The standard gravitational area/action normalization then gives

`a = l_P`.

So the remaining bare-cell-alone gap is exactly B3, not B4.

## Safe Claim

Use:

> B4 is conditionally closed: once the gravity/action sector is derived from the
> same algebra, its primitive source-free one-cell representative is forced to be
> `P_A`.

Do not use:

> B4 alone derives the gravity/action sector.
