# Planck-Scale Gravitational Area/Action Carrier Identification Theorem

**Date:** 2026-04-23
**Status:** branch-local theorem attacking the primitive-count-to-gravity identification step
**Audit runner:** `scripts/frontier_planck_gravitational_area_action_carrier_identification_theorem.py`

## Question

Why should the primitive one-cell count density be identified with the
gravitational area/action density?

## Bottom line

On the physical lattice package, if the Planck lane is required to reproduce the
semiclassical gravitational boundary area/action law, then the primitive
worldtube count is the unique available local codimension-1 microscopic carrier
for that law.

The identification is therefore not a numerical fit:

`S_cell / k_B = c_cell A / a^2`

is the microscopic lattice expression of the same extensive boundary density as

`S_grav / k_B = A c_light^3 / (4 G hbar)`.

Equating them gives

`a^2 = 4 c_cell l_P^2`.

With the independently derived primitive coefficient

`c_cell = 1/4`,

one obtains

`a^2 = l_P^2`.

## Scope

This theorem does not derive the existence of semiclassical gravity from the
Planck packet alone. It is a carrier-identification theorem:

> given that the physical `Cl(3)` / `Z^3` package is being matched to the
> gravitational area/action sector with Newton constant `G`, the only local
> primitive boundary carrier available in the direct Planck lane is the
> worldtube count density.

So the theorem removes a hidden choice of carrier. It does not remove the
standard requirement that the framework reproduce the gravitational
area/action law.

## Inputs

1. The lattice is physical, so primitive cells are not regulator artifacts.
2. The direct worldtube theorem fixes the one-cell codimension-1 count operator:

   `N_cell = P_A`.

3. The universal primitive counting-trace theorem fixes:

   `c_cell = tau(P_A) = 1/4`.

4. The semiclassical gravitational boundary/action density is:

   `S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`.

5. The boundary law is local and extensive in area at leading order.

## Theorem 1: a local lattice boundary law must be cell-count extensive

Let `A` be a macroscopic boundary area tiled by primitive lattice boundary
cells of area `a^2`, up to lower-order edge/corner corrections.

Then the number of primitive boundary cells is

`N_boundary = A / a^2 + o(A/a^2)`.

If the microscopic boundary law is local and has the same primitive coefficient
on each source-free boundary cell, then

`S_cell / k_B = c_cell N_boundary + o(N_boundary)`.

Therefore, at leading area order,

`S_cell / k_B = c_cell A / a^2`.

## Theorem 2: the direct Planck lane has a unique primitive boundary carrier

On the direct Planck lane, the only retained primitive codimension-1 carrier is
the one-step worldtube packet

`P_A = 1_{N_evt = 1}`.

Alternative scalar/free-energy, reduced-vacuum, and local holonomy carriers
were audited separately and either:

1. do not land the exact quarter;
2. depend on extra state/source data;
3. belong to a different object class;
4. or fail exact conventional `a = l_P`.

Thus, within the direct Planck packet, a local extensive gravitational boundary
density has only one primitive microscopic carrier:

`c_cell = tau(P_A)`.

## Theorem 3: matching to gravitational area/action fixes the lattice area

If the physical lattice boundary count is the microscopic carrier of the
semiclassical gravitational area/action density, then equate the leading
dimensionless densities:

`c_cell / a^2 = 1 / (4 l_P^2)`.

Solving gives

`a^2 = 4 c_cell l_P^2`.

With

`c_cell = 1/4`,

this yields

`a^2 = l_P^2`.

## What is now forced versus still assumed

Forced inside the Planck packet:

1. the primitive `C^16` event cell;
2. the packet `P_A`;
3. the normalized counting-trace coefficient `c_cell = 1/4`;
4. the leading local lattice boundary density `c_cell A/a^2`;
5. the algebraic consequence `a^2 = 4 c_cell l_P^2` once matched to gravity.

Still a physical matching requirement:

> the framework's primitive boundary count is the microscopic carrier of the
> semiclassical gravitational area/action density.

That requirement is not a fitted numerical coefficient. It is the statement
that the Planck lane is the gravitational boundary/action lane.

## Hostile-review status

The remaining denial is now narrow:

> reject that the direct primitive boundary count is the microscopic carrier of
> gravitational area/action.

If that denial is made, the branch still has the exact primitive coefficient
`1/4`, but it no longer has a Planck-length normalization.

If that denial is rejected, no further scale is imported:

`a^2 = 4 (1/4) l_P^2 = l_P^2`.
