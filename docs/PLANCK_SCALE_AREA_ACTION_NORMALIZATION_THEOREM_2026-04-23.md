# Planck-Scale Area/Action Normalization Theorem

**Date:** 2026-04-23
**Status:** branch-local standalone normalization theorem for the final `c_cell = 1/4 -> a = l_P` step
**Audit runner:** `scripts/frontier_planck_area_action_normalization_theorem.py`

## Scope

The carrier-selection part of this step is separated in:

- [PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md)

This file handles the algebraic normalization after the primitive count has
been identified as the microscopic gravitational boundary/action carrier.

## Question

Given the dimensionless primitive-cell coefficient

`c_cell = 1/4`,

does the gravitational area/action normalization really imply

`a^2 = l_P^2`

with all dimensional constants accounted for?

## Definitions

Let:

- `a` be the physical lattice spacing;
- `A` be a macroscopic boundary area;
- `c_light` be the speed of light;
- `G` be Newton's gravitational constant;
- `hbar` be the reduced Planck constant;
- `k_B` be Boltzmann's constant;
- `l_P^2 := hbar G / c_light^3` be the conventional Planck area.

The gravitational area/action law is the dimensionless Bekenstein-Hawking /
Euclidean-boundary normalization

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`.

The primitive-cell counting law assigns the same dimensionless boundary
coefficient as

`S_cell / k_B = c_cell A / a^2`.

Here `c_cell` is dimensionless. All dimensions live in `A / a^2` on the cell
side and in `A / l_P^2` on the gravitational side.

## Theorem

If the primitive-cell boundary count is the microscopic realization of the
gravitational area/action density, then

`a^2 = 4 c_cell l_P^2`.

For the derived value

`c_cell = 1/4`,

this gives

`a^2 = l_P^2`,

and since both lengths are positive,

`a = l_P`.

## Proof

Equate the two dimensionless boundary densities:

`c_cell / a^2 = 1 / (4 l_P^2)`.

Solving for `a^2` gives

`a^2 = 4 c_cell l_P^2`.

Substituting

`c_cell = 1/4`

gives

`a^2 = 4 (1/4) l_P^2 = l_P^2`.

Using the definition

`l_P^2 = hbar G / c_light^3`,

the result is equivalently

`a^2 = hbar G / c_light^3`.

No independent observed lattice spacing is inserted.

## What is imported and what is not

Imported physical normalization:

1. the gravitational boundary/action law
   `S_grav / k_B = A c_light^3 / (4 G hbar)`;
2. the standard definitions of `G`, `hbar`, `c_light`, and `k_B`;
3. the convention `l_P^2 = hbar G / c_light^3`.

Not imported:

1. the value of `a`;
2. the equality `a = l_P`;
3. any tunable dimensionless coefficient.

The theorem derives the lattice spacing from the dimensionless microscopic
coefficient once the cell count is identified with the gravitational
area/action density.

## Failure mode

If a reviewer rejects the identification of the primitive-cell count with the
gravitational area/action density, then this theorem does not apply.

That would not refute the exact `c_cell = 1/4` result. It would reject the
physical normalization that maps that coefficient to Newton/Planck units.
