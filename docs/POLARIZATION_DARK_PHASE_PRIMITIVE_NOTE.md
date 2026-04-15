# Dark-Phase Primitive on the Residual `SO(2)` Bundle

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** minimal angle-sensitive primitive after the common obstruction has collapsed to one dark-plane angle

## Verdict

The last connected gauge is not structureless.

The smallest angle-sensitive primitive already latent on the support side is
the exact dark pair on the residual dark `T1` plane:

`D_R(q) := (d_y, d_z)`.

Equivalently, in polar form:

- `rho_R(q) := ||D_R(q)||`
- `vartheta_R(q) := atan2(d_z, d_y)`

Under the residual connected `SO(2)` action:

- `rho_R` is invariant;
- `vartheta_R` shifts by the gauge angle.

So wherever `rho_R != 0`, the support side already carries a canonical local
phase coordinate that trivializes the connected residual gauge.

## Why this matters

The dark-angle no-go established that the current exact common objects

- `Pi_A1`
- `K_R`
- `I_TB`
- `Xi_TB`

are all blind to the residual `SO(2)` dark angle.

That does **not** mean an angle-sensitive primitive does not exist anywhere in
the atlas. It means the current common bridge does not yet carry one.

The exact support dark coordinates provide the missing kind of object:

> an exact angle-sensitive primitive.

## Exact covariance

The exact support-side dark coordinates transform covariantly under the
residual `SO(2)` rotation of the dark `T1` plane.

If the residual rotation angle is `phi`, then:

`D_R(q_phi) = R(phi) D_R(q)`

with `R(phi)` the standard `2x2` rotation matrix.

Therefore:

- `rho_R(q_phi) = rho_R(q)`
- `vartheta_R(q_phi) = vartheta_R(q) + phi`

modulo the usual angular branch choice.

## Sharpened frontier

This changes the gravity frontier again.

Before:

> we need an angle-sensitive primitive.

Now:

> we already have an exact support-side angle-sensitive primitive
> `vartheta_R`, but it is not yet carried by the current common bridge /
> curvature-localization side.

So the remaining theorem is no longer “invent an angle-sensitive object from
nothing.” It is:

> lift the exact support-side dark phase `vartheta_R` canonically into the
> common bundle / curvature-localization side.

## Remaining issue

The current exact common bridge triple

`B_R = (K_R, I_TB, Xi_TB)`

does not depend on `D_R` or `vartheta_R`, so it does not yet transport the
dark phase.

That is why the dark-angle no-go and the dark-phase primitive can both be
true:

- the primitive exists on the support side;
- the current common candidate does not yet carry it.

## Bottom line

The last connected residual gauge is `SO(2)`, and the exact support side
already carries a canonical local phase coordinate for it:

`vartheta_R = atan2(d_z, d_y)`.

So the honest remaining task is now:

> extend the common bridge from `(Pi_A1, K_R, I_TB, Xi_TB)` to an exact
> angle-carrying object that transports `vartheta_R` into the universal
> curvature-localization side.
