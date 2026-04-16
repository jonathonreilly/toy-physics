# `beta = 6` Provenance for the Quotient-Surface Plaquette Package

**Date:** 2026-04-16  
**Status:** provenance / imported fixed input for the current pure-gauge package

## Purpose

This note fixes the physical input surface for the quotient-surface plaquette
program and makes explicit what is being imported rather than re-derived here.

## Fixed input

The current package does **not** reopen the bare-coupling choice.

It imports the already-established CI3 normalization chain:

`g_bare^2 = 1  ->  beta = 2 N_c = 6`

for `SU(3)`.

So every theorem in the quotient-surface package is stated on the fixed
physical gauge point

`beta = 6`.

## Local anchor

The exact local `SU(3)` one-plaquette block remains the local anchor:

`P_1plaq(beta) = d/d beta log Z_1plaq(beta)`.

At the fixed physical point,

`P_1plaq(6) = 0.422531739649983`.

That value is imported from the exact local block theorem package, not
recomputed as a new physical assumption here.

## Why this package freezes `beta`

The present job is narrower:

1. quotient rooted fillings by exact `4`-cube boundary moves
2. count quotient-distinct same-boundary anchored surfaces
3. rebuild the plaquette route on those physical surfaces

So `beta = 6` is a fixed input surface throughout this package.

## Imported references

- `docs/ALPHA_S_DERIVED_NOTE.md`
- `docs/CI3_Z3_PUBLICATION_STATE_2026-04-15.md`
- `docs/publication/ci3_z3/DERIVATION_ATLAS.md`
- `docs/GAUGE_PLAQUETTE_SOURCE_NO_GO_NOTE.md`

## Honest scope

This note does **not** add a new theorem.

It only freezes the physical gauge point so the quotient-surface closure work
stays on one exact target:

`P(6)`.
