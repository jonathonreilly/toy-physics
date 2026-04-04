# Directional-B Density Stencil Note

**Status:** bounded transfer diagnostic on the fixed directional-measure lane  
**Date:** 2026-04-04

## Scope

This note does not reopen the directional-measure denominator search. It asks a
smaller question forced by the new center-biased midlayer sentinel:

- is the recent continuous-density miss mode really a problem with the fourth-neighbor stencil?

The comparison reuses the existing artifact chain:

- original dense reference sample from the continuous-density bridge card
- branching-tree freeze control
- center-biased midlayer sentinel from the latest holdout

No new graph family or new threshold fit is introduced on the expanded sample.
The only frozen thresholds are the old dense-reference density-load rules:

- `knn3_density_load >= 1.9783`
- `knn4_density_load >= 2.7354`

## Result

On the original reference sample plus the tree control, the frozen 4-NN law is
still cleaner:

- 4-NN: `21/2/3/37`, accuracy `0.9206`
- 3-NN: `22/5/2/34`, accuracy `0.8889`

But the center-biased midlayer sentinel reverses that preference:

- 4-NN: `4/0/6/30`, accuracy `0.8500`
- 3-NN: `8/0/2/30`, accuracy `0.9500`

So once the midlayer sentinel is added to the existing reference+tree sample,
the frozen 3-NN stencil becomes the better smooth law on the current expanded
dataset:

- extended sample 3-NN: `30/5/4/64`, accuracy `0.9126`
- extended sample 4-NN: `25/2/9/67`, accuracy `0.8932`

## Miss mode

The 4-NN failures are not random. They are mostly one-sided, low-occupancy
target bands on the midlayer sentinel:

- `5/6` frozen 4-NN false negatives have in-band nodes on only one side of the target plane
- `4/6` are rescued immediately by the frozen 3-NN stencil
- the remaining two misses are the sharpest shallow-overlap corners:
  - one nearly singular `m3` row with only one in-band node
  - one `m5` row with three in-band nodes but still a shallow overlap geometry

The bounded interpretation is that the fourth neighbor is the unstable sample on
this sentinel. Under one-sided midlayer densification, the fourth neighbor is
often the first point that jumps across the target-plane gap, so `r4` inflates
the estimated same-side support and makes the frozen 4-NN load too
conservative. The 3-NN stencil stays closer to the counted occupancy picture.

## Consequence

This does **not** overturn the current portable overlap statement:

- occupancy shortage is still the robust coarse bridge

It does sharpen the continuous-law story:

- 4-NN remains the cleaner fit on the original dense reference sample
- 3-NN is now the better frozen smooth-density candidate on the current
  expanded sample that includes the midlayer sentinel

So the next bounded continuous-law step, if one is needed, should start from the
3-NN stencil or another equally local occupancy-aware correction, not from a
broader denominator search.
