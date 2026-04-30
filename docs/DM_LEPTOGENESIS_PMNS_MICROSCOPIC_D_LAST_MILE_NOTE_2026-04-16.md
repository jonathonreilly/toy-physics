# DM Leptogenesis PMNS Microscopic `D` Last-Mile Reduction

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_leptogenesis_pmns_microscopic_d_last_mile.py`

## Question

After the PMNS-assisted flavored-DM route has already been reduced to the
microscopic operator `D`, what exact `D`-level object is still missing on the
charged-lepton-active `N_e` route?

## Bottom line

Not the full microscopic operator again.

The exact remaining object is only the active off-seed `5`-real
corner-breaking source beyond the already-derived aligned seed pair:

`(xi_1, xi_2, eta_1, eta_2, delta)`.

Equivalently, on the DM branch the remaining projected-source target is the
charge-`-1` off-seed source law `dW_e^H` beyond the aligned weak-axis seed
patch.

## What closes

### 1. The aligned seed patch is exact but insufficient

Reusing the PMNS microscopic seed law, the aligned weak-axis seed patch is
already positively closed at the `D` level.

But the canonical near-closing `N_e` sample used on the DM branch is genuinely
off-seed:

- `x = (0.24, 0.38, 1.07)`
- `y = (0.09, 0.22, 0.61)`
- `delta = 1.10`

while its derived seed pair is only

- `xbar = 0.5633333333333334`
- `ybar = 0.30666666666666664`.

If one collapses back to the exact aligned seed patch with the same seed pair,
the best flavored lift is only

`eta / eta_obs = 0.7190825360613422`,

whereas the canonical off-seed `N_e` packet gives

`eta / eta_obs = 0.9895125971972334`.

So the exact seed law helps, but it does not close the PMNS-assisted DM repair
route by itself.

### 2. The seed pair is not the remaining value law

Two off-seed active samples can share the same exact seed pair `(xbar,ybar)`
while carrying different breaking-source data and producing different flavored
packets and different selected transport columns.

So the unresolved microscopic object is not the seed pair.

### 3. The remaining `D`-level object is only the active `5`-real breaking source

Once the seed pair and the `5`-real breaking source

`(xi_1, xi_2, eta_1, eta_2, delta)`

are supplied, the rest is exact and algorithmic:

`(xbar,ybar,xi_1,xi_2,eta_1,eta_2,delta)`
`-> D_act`
`-> H_e`
`-> |U_e|^2^T`
`-> selected flavor column`
`-> eta`.

On the canonical `N_e` sample this reproduces the same near-closing PMNS lift
exactly.

## Quantitative consequence for the old `5.3x` miss

The old exact one-flavor theorem-native miss factor was

`eta_obs / eta = 5.297004933778`.

On the PMNS-assisted charged-lepton route:

- aligned seed patch miss factor:
  `1 / 0.7190825360613422 = 1.3906609462070065`
- canonical off-seed `N_e` miss factor:
  `1 / 0.9895125971972334 = 1.010598554108833`

So the old `5.3x` problem is basically gone on this route. The remaining gap is
no longer transport and no longer projector selection. It is the off-seed
microscopic charged-sector value law.

## Exact consequence

The PMNS-assisted DM target has now been reduced to the smallest exact
microscopic object I can honestly defend on this branch:

- not the full PMNS pair
- not the full microscopic operator again
- not the aligned seed patch
- not transport
- not flavored-column selection

but only

`(xi_1, xi_2, eta_1, eta_2, delta)`

on the active charged-lepton branch, equivalently the off-seed microscopic
charge-`-1` projected source law.

## Boundary

This note does **not** derive those `5` real values from `Cl(3)` on `Z^3`.

It proves only that:

1. the aligned seed patch is already exact,
2. the near-closing DM repair is off-seed,
3. and the remaining `D`-level object is only the active `5`-real
   corner-breaking source beyond the seed pair.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_microscopic_d_last_mile.py
```
