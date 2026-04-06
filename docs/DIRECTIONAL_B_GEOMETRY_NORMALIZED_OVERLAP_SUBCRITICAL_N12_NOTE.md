# Directional-B Geometry-Normalized Overlap Subcritical `N=12` Note

**Date:** 2026-04-05
**Status:** bounded shallow-slice follow-on for the widened-source overlap seam

## Artifact chain

- Script:
  [`scripts/directional_b_geometry_normalized_overlap_map.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_geometry_normalized_overlap_map.py)
- Log:
  [`logs/2026-04-05-directional-b-geometry-normalized-overlap-map-n12.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-directional-b-geometry-normalized-overlap-map-n12.txt)
- Prior deeper-slice baseline:
  [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md)

## Question

The widened-source holdout story is already sharp at the deeper slice:

- on the second dense-family holdout at `mass_nodes = 5`, `N = 25`,
  `response / b` fails only because the low-`b` overlap rows drag the trend
- `response / (b - h_mass)` still passes on the full sample

This follow-on asks one narrower question:

- does the same overlap / occupancy seam already appear at the shallower
  `N = 12` slice?
- or is the deeper `N = 25` failure the first place the seam becomes visible
  at all?

## Frozen setup

- same transport:

```text
exp(i k S_spent) / L^p × exp(-β θ²),  β = 0.8
```

- same widened-source holdout family:
  - `28` nodes/layer
  - `y_range = 13`
  - `radius = 3`
- widened source: `mass_nodes = 5`
- frozen slice: `N = 12`
- same target ladder: `b = 1.5 .. 7.5`
- same `5` seeds
- same joined overlap observables:
  - signed overlap coordinate `mu = edge_b / h_mass`
  - occupancy bridge variable `target_fill = local_target_count / mass_nodes`

## Frozen result

The seam is already present at `N = 12`, but it is still weaker than on the
deeper slice.

- exactly `3/25` rows are true overlap rows (`mu <= 0`)
- all `3` overlap rows live in the first two target buckets (`b = 1.5`, `3.0`)
- all `3` also satisfy the retained occupancy-floor side
  `target_fill <= 0.4`

Unlike the `N = 25` slice, the full center-offset trends still pass:

- full-sample `A/b`: PASS (`+0.1061 -> +0.0364`, slope `-0.0123`)
- full-sample `F/b`: PASS (`+0.1479 -> +0.0428`, slope `-0.0184`)
- full-sample `A/edge`: PASS (`+0.2161 -> +0.0497`)
- full-sample `F/edge`: PASS (`+0.2613 -> +0.0583`)

But removing only the overlap rows still sharpens the center-offset law:

- non-overlap `A/b`: PASS (`+0.1362 -> +0.0364`, slope `-0.0179`)
- non-overlap `F/b`: PASS (`+0.1892 -> +0.0428`, slope `-0.0264`)

So the same overlap/occupancy seam already exists on the shallower slice. It
just is not strong enough yet to flip the full-sample center-offset trend.

## Safe read

The honest bounded conclusion is now cross-slice rather than single-slice:

- the widened-source holdout seam is not unique to the deeper `N = 25` replay
- the same low-`b` overlap rows already distort the shallower `N = 12` slice
- on `N = 12` that distortion is subcritical: `response / b` still passes on
  the full sample and only steepens after the overlap rows are removed
- on `N = 25` the same seam is strong enough to flip the full-sample
  `response / b` trend into failure
- nearest-edge density `response / (b - h_mass)` remains the portable
  finite-source correction on both slices

In plain language:

- `b` remains the asymptotic coordinate
- `edge_b = b - h_mass` remains the review-safe low-`b` correction
- the low-`b` overlap / occupancy seam is now visible as a shallow-to-deep
  progression, not a one-off failure

## Relation To The Existing Lane

Read this with:

- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md)
- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md)
- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md)

Together they now say:

- the old `mass_nodes = 3` holdout transfer was real
- widening to `mass_nodes = 5` does not kill the geometry-normalized lane
- the same overlap-sector distortion is already visible on `N = 12`
- that seam only becomes trend-flipping on the deeper `N = 25` slice
- there is still no reason to reopen denominator search

## Best next move

This closes the cleanest remaining same-lane support check on the current
geometry-normalized branch.

If this lane is revisited again, keep it equally narrow:

- either test the same subcritical-to-critical seam on one genuinely new dense
  family
- or leave the directional-`b` lane parked and move to the next
  non-overlapping program lane
