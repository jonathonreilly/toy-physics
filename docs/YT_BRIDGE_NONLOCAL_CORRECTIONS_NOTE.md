# `y_t` Bridge Nonlocal Corrections Note

**Date:** 2026-04-15 (revised 2026-05-16)
**Status:** bounded support note — Cauchy-Schwarz family-agnostic bound
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
> nonlocal correction on the forced UV window?

## Scope

The 2026-05-16 revision narrows the claim scope explicitly so the runner
matches the bounded-support framing the note has carried since its first
draft. The numerical results below are reported as a Cauchy-Schwarz
family-agnostic upper bound on the integrated nonlocal effect — not as a
target-conditioned best-family search.

In particular this note does **not** claim:

- a structural derivation of the residual operator norm bound from the
  exact interacting bridge action (still missing — that is the
  upstream review target);
- a target-`y_t`-conditioned best-fit selection from a chosen family
  grid (the prior runner included a viability filter that has been
  removed; only the family-agnostic Cauchy-Schwarz bound is now
  load-bearing).

It does claim:

- a bounded operator-norm distance between the exact endpoint-response
  kernel and its affine local-Hessian model on the forced UV window,
  given the standard SM inputs at `M_Z` and the derived `V` scale;
- a Cauchy-Schwarz upper bound on the integrated nonlocal effect for
  every profile `phi` in the UV-localized class, namely

  `|<K_nonloc, phi>| <= ||K_nonloc||_2 * ||phi||_2`.

Both numbers are intrinsic to the kernel pair `(K, K_loc)` on the
forced UV window and do not depend on any target-`y_t` filter or
best-family selection.

## Result

On the forced UV window `x >= 0.95`, the exact endpoint-response kernel is
still nearly affine. If we write

`K(x) = K_loc(x) + K_nonloc(x)`

with `K_loc` the affine local-Hessian model fit on the same window, then
the residual correction is small:

- `||K_nonloc||_2 / ||K||_2 = 5.024e-3`
- `||K_nonloc||_2 = 2.799e-5` on the runner's normalized window measure
- pointwise affine-fit max relative error `= 1.188e-2`

By Cauchy-Schwarz on the forced UV window, the integrated nonlocal
effect against any normalized profile `phi` (with `||phi||_2 = 1`) is
therefore bounded by

`|<K_nonloc, phi>| <= ||K_nonloc||_2 = 2.799e-5`

independent of family, family grid, or target-`y_t` viability filter.

The runner additionally reports the three reference family numbers
(logistic, erf, smoothstep) at a fixed reference parameter pair, but
only as a non-load-bearing sanity comparison against the
family-agnostic Cauchy-Schwarz bound.

## Meaning

This is a bounded statement at the kernel level:

> once the bridge is forced into the UV-localized class, the
> integrated nonlocal correction beyond the local Hessian selector is
> at most the absolute residual operator norm `2.799e-5` times the
> profile L2 norm, for every profile in that class, given the standard
> SM inputs at `M_Z`. Equivalently, the residual is `5.024e-3` of the
> full kernel L2 norm on the same window.

That is a real Cauchy-Schwarz control statement on the residual
operator norm. It is still not a full unbounded proof. It says the
residual operator norm is small at the chosen SM inputs; it does not
prove that the microscopic lattice bridge is exactly the local-Hessian
model, and it does not derive the operator-norm bound from the exact
interacting bridge action.

## Honest boundary

This note does **not** remove the remaining YT bound by itself.

It does show that the nonlocal correction on the forced UV window is
bounded and numerically small in operator norm for the standard SM
inputs at `M_Z`. By Cauchy-Schwarz that bound carries to every profile
in the UV-localized class without needing a target-`y_t` viability
filter. The remaining theorem gap is the structural derivation of the
operator-norm bound from the exact interacting bridge action, which is
the upstream review target carried by the dependency links below.

## Honest auditor read

The 2026-05-05 audit recorded an earlier version of this row as
`audited_numerical_match` because the previous runner ran a
target-`y_t` viability filter over a chosen profile grid and reported
the best rows. The 2026-05-16 revision removes that filter and grid
search. The load-bearing step is now the Cauchy-Schwarz
family-agnostic upper bound `2.799e-5 * ||phi||_2`, with relative
kernel norm `||K_nonloc||_2 / ||K||_2 = 5.024e-3`. Both numbers are
intrinsic to the kernel pair on the forced UV window.

The structural derivation of the operator-norm bound from the exact
interacting bridge action remains open and is the upstream review
target, not a claim made by this note.

## Audit dependency repair links

This graph-bookkeeping section records the upstream authorities the
nonlocal residual analysis reuses. It does not promote this note or
change the audited claim scope.

- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  for the constructive UV-localized family the Cauchy-Schwarz bound
  applies to.
- [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
  for the affine local-Hessian model `K_loc` whose residual is
  measured.
- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV window definition.
- [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
  for the response-kernel structure used in the affine fit.
