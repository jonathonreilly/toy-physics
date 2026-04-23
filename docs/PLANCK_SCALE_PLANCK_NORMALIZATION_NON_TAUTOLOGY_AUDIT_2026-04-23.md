# Planck-Scale Planck-Normalization Non-Tautology Audit

**Date:** 2026-04-23
**Status:** branch-local audit for issue #5, the tautology objection
**Audit runner:** `scripts/frontier_planck_planck_normalization_non_tautology_audit.py`

## Question

Does matching the primitive boundary count to the gravitational area/action law
trivially assume

`a = l_P`?

## Short answer

No. The match imports the gravitational area/action normalization and the
standard dimensional constants. It does not import the microscopic lattice
spacing.

The matching equation leaves the spacing as

`a^2 = 4 c_cell l_P^2`,

or

`a = 2 sqrt(c_cell) l_P`.

Therefore matching to gravity alone would give an arbitrary multiple of the
Planck length if the primitive coefficient were arbitrary. Writing

`c_cell = lambda / 4`,

the same match gives

`a = sqrt(lambda) l_P`.

The nontrivial result is the prior microscopic derivation

`c_cell = Tr((I_16 / 16) P_A) = rank(P_A) / 16 = 4/16 = 1/4`.

Only after that dimensionless coefficient has been derived does the matched
spacing become exactly

`a = l_P`

instead of

`a = sqrt(lambda) l_P`.

## What is imported

The Planck-normalization step imports the semiclassical gravitational
area/action law

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`,

with the conventional Planck-area definition

`l_P^2 := hbar G / c_light^3`.

It also imports the meanings of the physical constants `G`, `hbar`,
`c_light`, and `k_B`.

## What is not imported

The step does not import:

1. the value of `a`;
2. the equality `a = l_P`;
3. a fitted dimensionless lattice coefficient;
4. a convention that one primitive cell has Planck area.

The microscopic input is instead the dimensionless coefficient already derived
on the native packet:

`dim(H_cell) = 16`,

`rank(P_A) = 4`,

`rho_cell = I_16 / 16`,

so

`c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`.

## Algebraic audit

The cell law is

`S_cell / k_B = c_cell A / a^2`.

The gravitational law is

`S_grav / k_B = A / (4 l_P^2)`.

Identifying the primitive boundary count as the gravitational
area/action carrier means equating the leading dimensionless densities:

`c_cell / a^2 = 1 / (4 l_P^2)`.

Solving for the unknown spacing gives

`a^2 = 4 c_cell l_P^2`.

This equation is not the statement `a^2 = l_P^2`. It becomes that statement
only if

`4 c_cell = 1`.

The native packet supplies exactly that:

`4 c_cell = 4 (1/4) = 1`.

Hence

`a^2 = l_P^2`,

and because both lengths are positive,

`a = l_P`.

## Counterfactual check

The tautology objection would be correct if every value of `c_cell` produced
`a = l_P` after matching to gravity. It does not.

For example:

| primitive coefficient | matched result |
| --- | --- |
| `c_cell = 1/8` | `a^2 = (1/2) l_P^2` |
| `c_cell = 1/4` | `a^2 = l_P^2` |
| `c_cell = 1` | `a^2 = 4 l_P^2` |

Equivalently, if an undetermined coefficient were written

`c_cell = lambda / 4`,

then matching would give

`a^2 = lambda l_P^2`

and

`a = sqrt(lambda) l_P`.

So the exact Planck spacing is not produced by dimensional matching alone. It
is produced by the separately derived, dimensionless, microscopic value

`lambda = 1`,

equivalently

`c_cell = 1/4`.

## Relation to existing notes

This audit does not replace the existing carrier-identification or
normalization theorems. It records the anti-tautology logic connecting them.

Load-bearing references:

1. [PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md)
2. [PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md)
3. [PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md](./PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md)

Those notes establish, respectively:

1. the algebraic normalization `a^2 = 4 c_cell l_P^2`;
2. the physical carrier-identification condition for using the gravitational
   area/action law;
3. the native microscopic derivation `c_cell = 1/4`.

## Hostile-review conclusion

The remaining valid objection is not:

> The proof secretly assumed `a = l_P`.

The sharper remaining objection is:

> Reject the physical matching of the primitive boundary count to the
> gravitational area/action law.

If that matching is rejected, the branch keeps the exact dimensionless result

`c_cell = 1/4`,

but it no longer claims a Planck-length normalization. If the matching is
accepted, the exact coefficient forces the conventional result

`a = l_P`

without importing the lattice spacing.
