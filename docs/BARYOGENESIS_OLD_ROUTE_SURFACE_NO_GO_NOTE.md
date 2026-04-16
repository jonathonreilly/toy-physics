# Baryogenesis Old-Route Current-Surface No-Go Note

**Date:** 2026-04-16
**Status:** bounded current-surface no-go on `main`
**Script:** `scripts/frontier_baryogenesis_old_route_surface_no_go.py`

## Safe statement

The old 2HDM-like taste-scalar electroweak-transition route is **not** a live
same-surface route on the current `main` package.

This is not an axiom-level impossibility theorem. It is a sharper and more
honest current-package statement:

- the present authority surface derives exactly one Higgs doublet
- the scalar-spectrum matching boundary already shows that this one-doublet
  package contributes only about `41%` of the old target before screening
- the current baryogenesis target note explicitly does **not** derive an extra
  taste-scalar doublet on the authority path

So the old route is dead **on the present surface**.

## Authority input used

The current package surface already fixes:

1. one Higgs doublet from the `G_5` condensate
2. one radial Higgs mode plus three Goldstones on the Higgs/CW surface
3. exact selector portal coefficient `kappa_sel = 6 lambda_H`
4. the scalar-spectrum matching boundary:

   - radial mode matches the selector coefficient
   - Goldstones do not
   - the matched one-doublet spectrum has selector-equivalent multiplicity
     `1 + 1/sqrt(3)`

Separately, the cubic-target note already says explicitly that it does **not**
claim an extra taste-scalar doublet is derived on the authority path.

That combination is enough for a current-surface no-go.

## Why the old route is not live on current `main`

The earlier route-history logic was:

- if one had an effective 2HDM-like taste-scalar sector
- and if that sector carried the right order-1 portal
- and if screening were mild
- then the old `v(T_c)/T_c ~ 0.52` target might be viable

The present package no longer supports that as a same-surface route.

Why:

1. the current authority surface derives only one Higgs doublet
2. the exact matching boundary shows the one-doublet scalar package reaches
   only about `41%` of the old target before screening
3. there is no currently derived extra doublet or same-surface bosonic family
   available to supply the missing factor

So the old route is no longer a live implementation candidate on current
`main`. It is only route history and a discriminator for what new finite-`T`
structure would need to look like if a future route is found.

## What this closes

This note closes the question:

> “Is the old 2HDM-like taste-scalar EWPT route still alive on the current
> framework surface?”

Answer:

- no, not on current `main`
- the current package does not derive the needed extra scalar sector
- the currently derived one-doublet scalar package is far too weak even before
  screening

## What remains open

This note does **not** prove baryogenesis impossible in the framework.

It leaves open:

- a genuinely new derived finite-`T` bosonic sector
- a non-minimal or nonperturbative finite-`T` potential that invalidates the
  old one-loop scalar-cubic bookkeeping
- a lattice-derived transition strength / sphaleron / transport computation

So the honest remaining baryogenesis question is no longer:

- “does the old taste-scalar route work if screening is mild?”

It is now:

- “what new derived finite-`T` structure, if any, replaces that old route?”

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md)
  reduced the old route to an `O(3x-4x)` enhancement problem
- [BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md](./BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md)
  turned that into an exact target relation
- [BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md)
  derived the order-1 portal scale
- [BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md)
  proved the one-doublet matching boundary

This note is the next logical step:

- on the current authority surface, the old route is no longer live

## Validation

- [frontier_baryogenesis_old_route_surface_no_go.py](./../scripts/frontier_baryogenesis_old_route_surface_no_go.py)
- [BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md)
- [BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md](./BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md)

Current runner state:

- `frontier_baryogenesis_old_route_surface_no_go.py`: expected `PASS>0`,
  `FAIL=0`
