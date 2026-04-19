# DM Leptogenesis PMNS `N_e` Effective-Block Gap Localization

**Date:** 2026-04-16  
**Status:** exact gap-localization theorem on the observation-free reduced
`N_e` lane  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_ne_effective_block_gap_localization.py`

## Question

After the lower-level PMNS response pack and microscopic completion have been
quotiented away, is the remaining observation-free `N_e` gap still a diffuse
active-Hermitian law, or does it localize to a much smaller exact object?

## Bottom line

It localizes much more tightly.

On the exact reduced `N_e` closure surface:

- there are only two live stationary branches
- both branches lie on the same exact native seed surface
- both branches share the same derived mean `xbar`
- both branches share the same native cycle mean `sigma`
- both branches are essentially real-phase
- they differ only in the centered four-real source
  `(xi_1, xi_2, rho_1, rho_2)`

So the live observation-free gap is no longer a vague active-Hermitian/source
law. It is an exact branch-selection law between two off-seed centered
four-real sources on one fixed native seed surface.

## Exact theorem

The reduced `N_e` selector stack already gives two stationary branches:

- low-action physical branch
- higher-action competing branch

For those two exact branches:

- `xbar = 0.5633333333333334` on both
- `sigma = 0.306666666666666...` on both
- `delta ≈ 0` on both

Each branch active block rebuilds exactly from the common pair `(xbar, sigma)`
plus its own centered four-real source. The two sources are distinct:

- low branch:
  `(-0.091658, -0.009523, -0.098604, 0.157716)`
- high branch:
  `(0.226855, -0.156570, 0.279519, -0.139100)`

Each source also carries its own exact first-order normalization coefficient:

- low branch:
  `a_low ≈ 0.51848`
- high branch:
  `a_high ≈ 0.18949`

So the branch ambiguity is not full active-block freedom. It is a discrete
choice between two exact off-seed centered four-real sources.

## What this closes

This removes another layer of vagueness from the observation-free normalization
lane.

What is no longer the right description:

- “some unknown active Hermitian law”
- “some unknown lower-level response profile”
- “some unknown microscopic completion”

What is now the right description:

- one observation-free branch-selection law choosing between two exact
  off-seed centered four-real sources on one fixed seed surface

## Consequence

The next exact theorem should not search for a broader carrier or a new
microscopic completion. It should target the native rule that selects the
low-action four-real source.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_ne_effective_block_gap_localization.py
```
