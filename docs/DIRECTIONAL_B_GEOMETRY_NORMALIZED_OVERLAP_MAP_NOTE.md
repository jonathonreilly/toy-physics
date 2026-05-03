# Directional-B Geometry-Normalized Overlap Map Note

**Date:** 2026-04-05
**Status:** bounded overlap/occupancy map for the widened-source holdout
center-offset failure

## Artifact chain

- Script:
  [`scripts/directional_b_geometry_normalized_overlap_map.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_geometry_normalized_overlap_map.py)
- Log:
  [`logs/2026-04-05-directional-b-geometry-normalized-overlap-map.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-directional-b-geometry-normalized-overlap-map.txt)
- Prior widened-source baseline:
  [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md)
- Prior overlap bridge:
  [`scripts/directional_b_overlap_occupancy_bridge_card.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_overlap_occupancy_bridge_card.py)

## Question

The widened-source holdout replay already showed a clean split:

- on the second dense-family holdout at `mass_nodes = 5`, `N = 25`,
  `response / b` fails
- `response / (b - h_mass)` still passes

This follow-on asks one narrower question:

- do those `A/b` and `F/b` failures mean the center-offset density law breaks
  generically on the holdout family?
- or do they live only on the low-`b` overlap corners already isolated by the
  retained overlap / occupancy cards?

## Frozen setup

- same transport:

```text
exp(i k S_spent) / L^p × exp(-β θ²),  β = 0.8
```

- same holdout family:
  - `28` nodes/layer
  - `y_range = 13`
  - `radius = 3`
- widened source: `mass_nodes = 5`
- frozen slice: `N = 25`
- same target ladder: `b = 1.5 .. 7.5`
- same `5` seeds
- each geometry-normalized transfer row is joined directly to the existing
  overlap observables:
  - signed overlap coordinate `mu = edge_b / h_mass`
  - occupancy bridge variable `target_fill = local_target_count / mass_nodes`

## Frozen result

On the full widened-source holdout sample:

- `A/b`: FAIL (`-0.3518 -> +0.0416`)
- `F/b`: FAIL (`-0.4761 -> +0.0294`)
- `A/edge`: PASS (`+0.1651 -> +0.0524`)
- `F/edge`: PASS (`+0.1070 -> +0.0382`)

The direct overlap map shows why:

- exactly `4/25` rows are true overlap rows (`mu <= 0`)
- all `4` overlap rows live in the first two target buckets: `b = 1.5` or
  `b = 3.0`
- all `4` overlap rows also satisfy the promoted occupancy-floor side of the
  old bridge: `target_fill <= 0.4`

Once only those overlap rows are removed, the center-offset trend comes back:

- non-overlap `A/b`: PASS (`+0.1017 -> +0.0416`, slope `-0.0116`)
- non-overlap `F/b`: PASS (`+0.0833 -> +0.0294`, slope `-0.0107`)

So the widened-source holdout failure is not spread across the whole sample.
It is concentrated in the same low-`b` overlap sector the older bridge cards
already isolated.

## Safe read

The honest bounded conclusion is now sharper:

- the widened-source `N = 25` holdout does **not** show that `response / b`
  fails generically on the second dense-family holdout
- it shows that the center-offset law breaks exactly where low occupancy has
  already become real source overlap
- nearest-edge density `response / (b - h_mass)` remains the portable
  finite-source correction on the full sample
- occupancy shortage is still the promoted coarse bridge variable, but on this
  joined diagnostic the actual trend failure is the smaller subset where that
  shortage has already crossed into `mu <= 0`

In plain language:

- `b` remains the asymptotic coordinate
- `edge_b = b - h_mass` remains the review-safe low-`b` correction
- the widened-source failure is an overlap-seam effect, not a new reason to
  reopen denominator search

## Relation To The Existing Lane

Read this with:

- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_MASS5_NOTE.md)
- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md)
- `docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_SUBCRITICAL_N12_NOTE.md` (sibling artifact in same lane; cross-reference only — not a one-hop dep of this note)
- [`docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`](/Users/jonreilly/Projects/Physics/docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md)
- [`scripts/directional_b_overlap_occupancy_bridge_card.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_overlap_occupancy_bridge_card.py)

Together they now say:

- the old `mass_nodes = 3` transfer was real
- widening to `mass_nodes = 5` does not kill the geometry-normalized lane
- the same low-`b` overlap seam is already visible on the shallower `N = 12`
  slice, but remains subcritical there
- the `N = 25` holdout failure of `response / b` is not a fresh global
  breakdown
- it is the overlap-sector effect already anticipated by the `mu` and
  occupancy cards
- `response / (b - h_mass)` remains the portable finite-source correction on
  the tested dense families

## Best next move

Do not reopen a wider denominator search from this result.

This direct overlap map closes the cleanest remaining support diagnostic on the
current geometry-normalized lane.

If the lane is revisited again, keep it equally narrow:

- either test whether the same overlap-conditioned recovery survives on one
  other retained dense-family card
- or leave this lane parked and move to the next non-overlapping program lane
