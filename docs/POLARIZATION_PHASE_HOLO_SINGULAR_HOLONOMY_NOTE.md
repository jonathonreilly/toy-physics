# Polarization Phase Holonomy and the `rho_R = 0` Locus

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** exact analysis of the dark-phase section on the punctured dark complement and the obstruction to a distinguished global connection

## Verdict

The dark-phase section does separate the `rho_R > 0` region from the singular
set `rho_R = 0`, but that singular-set structure does **not** force a unique
distinguished global connection on the current common bundle.

The exact obstruction is:

> the current atlas fixes the puncture and the local phase coordinate, but it
> does not fix the normalization of the flat `SO(2)` connection on the
> punctured complement, nor does it canonically extend that connection across
> the `rho_R = 0` defect set.

## Exact support-side dark phase

The exact support-side dark pair is

`D_R(q) = (d_y, d_z)`.

Its radius-phase form is

`rho_R(q) := sqrt(d_y^2 + d_z^2)`,

`vartheta_R(q) := atan2(d_z, d_y)`.

The `rho_R = 0` locus is exactly the dark-plane singular set:

`Sigma_R = { q : d_y = 0 and d_z = 0 }`.

On `X_R := { rho_R > 0 }`, the normalized direction

`D_R / rho_R`

is a canonical local phase section.

So the support side already has a genuine angle-sensitive primitive, but it
is only defined on the punctured complement `X_R`.

## Holonomy on the punctured complement

On `X_R`, the canonical phase 1-form is

`A_phase = d vartheta_R`.

This is flat on `X_R`, but it is not a global gauge-fixing principle by
itself. On a loop `gamma` in `X_R`, the holonomy angle is

`Hol(gamma) = ∮_gamma A_phase = Delta vartheta_R(gamma)`.

For a loop of winding number `w` about `Sigma_R`,

`Hol(gamma) = 2 pi w`.

So the corresponding `SO(2)` group element is trivial after one full turn,
but the connection lives on the punctured complement and is singular at
`Sigma_R`.

That is the key point: the singular set gives a defect locus, not a canonical
extension rule.

## Why singular-set structure does not force a unique connection

The current exact common bridge data are blind to the dark angle:

- `Pi_A1`
- `K_R`
- `I_TB`
- `Xi_TB`

All of those factor through the same `SO(2)`-invariant support data.

Therefore the common bridge can detect the puncture, but it cannot select a
unique normalization of the dark-plane connection. On the punctured
complement there is a compatible flat family

`A_lambda = lambda d vartheta_R`.

All members of this family have:

- the same singular set `Sigma_R`;
- the same local flatness on `X_R`;
- different holonomy characters around loops that wind around `Sigma_R`.

So flatness alone does not distinguish a canonical global connection.

## Exact obstruction

The exact obstruction is not “missing topology.” The topology is already
identified:

- the singular set is codimension two in the dark-plane sector;
- the punctured complement has nontrivial loop classes;
- the phase section has winding data.

What is missing is a canonical normalization principle that fixes the
`lambda` in

`A_lambda = lambda d vartheta_R`.

Without such a principle, the connection is only canonical up to the residual
`SO(2)` gauge on the punctured complement.

## Consequence for the common bundle

The current common bundle candidate still does not gain a distinguished
global connection from holonomy or singular-set structure alone.

What it does gain is the precise obstruction:

> a one-parameter family of flat dark-plane connections on `X_R`, all
> compatible with the same singular locus, with no axiom-native rule in the
> current atlas that selects the normalization.

So the remaining theorem target is narrower than before:

> derive an angle-normalization principle for `A_lambda`, or prove that the
> current atlas cannot fix `lambda`.

## Bottom line

The `rho_R = 0` locus is the branch singular set of the dark phase.
The punctured complement admits a flat `SO(2)` phase connection.
But singular-set structure and flatness do **not** force a distinguished
global connection on the current common bundle.

The exact obstruction is the missing normalization of the dark-phase
connection on `X_R`.
