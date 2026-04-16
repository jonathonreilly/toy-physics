# `y_t` Bridge Nonlocal Corrections Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_nonlocal_corrections.py`

## Role

This note quantifies the first correction beyond the local-Hessian selector on
the forced UV window.

The earlier branch steps already established:

- a constructive UV-localized bridge class
- a positive local quadratic selector on the forced UV window
- a nearly affine endpoint-response kernel on that same window

The remaining question is therefore narrower:

> after extracting the local affine Hessian model, how large is the
> nonlocal correction on the viable bridge families?

## Result

On the forced UV window `x >= 0.95`, the exact endpoint-response kernel is
still nearly affine. If we write

`K(x) = K_loc(x) + K_nonloc(x)`

with `K_loc` the affine local-Hessian model from the branch selector note,
then the residual correction is small:

- `||K_nonloc||_2 / ||K||_2 = 5.024e-3`
- pointwise affine-fit max relative error `= 1.188e-2`

When that residual is tested against the best viable bridge families from the
constructive UV-localized class, the integrated effect remains small:

- logistic family: `3.428e-5` of the total kernel response
- erf family: `2.053e-4` of the total kernel response
- smoothstep family: `1.028e-3` of the total kernel response

So the nonlocal tail is not the dominant effect on the viable class. The local
Hessian selector still captures the leading structure, and the remaining
nonlocal correction is at the half-percent level in operator norm on the
forced UV window, while the integrated effect on the viable families stays at
or below the per-mille level.

## Meaning

This is the cleanest bounded statement available at this stage:

> once the bridge is forced into the UV-localized class, the nonlocal
> correction beyond the local Hessian selector is small on the viable
> families, even though it is not negligible at the operator-norm level.

That is a real control statement, but it is still not a full unbounded proof.
It says the residual is tiny; it does not prove that the microscopic lattice
bridge is exactly the local-Hessian model.

## Honest boundary

This note does **not** remove the remaining YT bound by itself.

It does show that the nonlocal correction on the forced UV window is bounded
and numerically small on the viable families, so the remaining theorem gap is
now microscopic rather than structural.
