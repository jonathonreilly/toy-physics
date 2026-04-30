# DM Neutrino Exact H-Side Source-Surface Preimage-Bundle Theorem

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_exact_h_source_surface_preimage_bundle_theorem.py`

## Question

Once the exact source-oriented triplet package is fixed, how small is the
remaining mainline `H`-side inverse-image problem?

## Bottom line

It is already an explicit two-sheet codimension-three preimage bundle on the
active Hermitian grammar.

Let the free real data be

- `(d1, d2, d3, r31)`

with `r31 >= 1/2`. Define

- `phi_+(r31) = asin(1 / (2 r31))`
- `phi_-(r31) = pi - phi_+(r31)`

and for either sheet `phi in {phi_+, phi_-}` set

- `r12 = 2 sqrt(8/3) - d2 + d3 + r31 cos(phi)`
- `r23 = d1 - d2 + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi)`

Then every such point lands exactly on the mainline source surface:

- `r31 sin(phi) = 1/2`
- `d2 - d3 + r12 - r31 cos(phi) = 2 sqrt(8/3)`
- `2 d1 - d2 - d3 + r12 - 2 r23 + r31 cos(phi) = 2 sqrt(8)/3`

So the remaining mainline object is no longer a generic `H`-law. It is the
post-canonical mixed-bridge law that selects a point on this exact preimage
bundle.

## Why this is sharper

The earlier exact source-surface theorem only said that the source-oriented
triplet package pulls back to a nonempty `H`-side surface.

This theorem solves that surface explicitly.

So the live mainline blocker is now smaller:

- not “derive the triplet values”
- not even “find some point on the source surface”
- but only “derive the post-canonical mixed-bridge law that lands on this exact
  two-sheet positive bundle”

## Positive region

Both sheets already contain explicit positive witnesses.

One `+`-sheet witness is:

- `(d1, d2, d3, r31) = (5, 5, 5, 1)`
- `phi = pi / 6`

One `-`-sheet witness is:

- `(d1, d2, d3, r31) = (10, 10, 10, 2)`
- `phi = pi - asin(1/4)`

On both, the direct intrinsic CP pair equals the exact source-oriented package

- `(-0.544331053952, +0.314269680527)`

and each witness sits inside a whole local positive box that stays on the exact
bundle.

## Exact consequence

The honest mainline blocker is now:

- derive the post-canonical mixed-bridge / `H`-side law whose image selects a
  point on this exact positive preimage bundle

That is smaller than the old “triplet-side value law” wording.

## Command

```bash
python3 scripts/frontier_dm_neutrino_exact_h_source_surface_preimage_bundle_theorem.py
```
