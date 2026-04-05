# Directional-B Geometry-Normalized Holdout Transfer Mass5 Note

**Date:** 2026-04-05  
**Status:** bounded widened-source holdout replay for geometry-normalized response density

## Artifact chain

- Script: [`scripts/directional_b_geometry_normalized_holdout_transfer.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_geometry_normalized_holdout_transfer.py)
- Log: [`logs/2026-04-05-directional-b-geometry-normalized-holdout-transfer-mass5.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-directional-b-geometry-normalized-holdout-transfer-mass5.txt)
- Prior bounded baseline: [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md)

This follow-on keeps the fixed directional-measure propagator and the same
mass-side action observables, but widens the source window from `3` to `5`
mid-layer nodes on both dense random-DAG families.

The question is intentionally narrow:

- does the original holdout transfer story survive once the source is wide
  enough that low-`b` overlap should matter?

## Frozen setup

- same transport:

```text
exp(i k S_spent) / L^p × exp(-β θ²),  β = 0.8
```

- same observables:
  - `action_channel`
  - `packet_flow_action`
- same families:
  - baseline dense family: `25` nodes/layer, `y_range = 12`, `radius = 3`
  - second dense-family holdout: `28` nodes/layer, `y_range = 13`, `radius = 3`
- widened source: `mass_nodes = 5`
- same slices: `N = 12, 25`, target `b = 1.5 .. 7.5`, `5` seeds

## Frozen result

The widened replay is still not a raw distance-law repair. Raw action-style
strengths continue to grow with `b`. The retained question is only the
geometry-normalized density trend.

### Baseline family

On the original dense family, all four normalized metrics still pass at both
`N = 12` and `N = 25` under the widened source.

### Holdout family

On the second dense-family holdout:

- `N = 12`
  - `A/b`: PASS (`+0.1061 -> +0.0364`)
  - `A/edge`: PASS (`+0.2161 -> +0.0497`)
  - `F/b`: PASS (`+0.1479 -> +0.0428`)
  - `F/edge`: PASS (`+0.2613 -> +0.0583`)
- `N = 25`
  - `A/b`: FAIL (`-0.3518 -> +0.0416`)
  - `A/edge`: PASS (`+0.1651 -> +0.0524`)
  - `F/b`: FAIL (`-0.4761 -> +0.0294`)
  - `F/edge`: PASS (`+0.1070 -> +0.0382`)

So the widened source does **not** erase the normalized hierarchy, but it does
change which part of that hierarchy transfers cleanly.

## Safe read

The honest bounded conclusion is now sharper:

- center-offset density `response / b` is still the asymptotic leading term on
  the bounded family
- but once the source is widened enough that low-`b` overlap becomes real on
  the holdout family, pure `response / b` is no longer the portable
  finite-source correction
- nearest-edge density `response / (b - h_mass)` still transfers at both
  `N = 12` and `N = 25`, so it is now the promoted finite-source correction

In other words:

- `b` remains the clean asymptotic coordinate
- `edge_b = b - h_mass` is the review-safe low-`b` correction on the tested
  dense families

## Relation to the existing lane

Read this with:

- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_HOLDOUT_TRANSFER_NOTE.md)
- [`logs/2026-04-01-directional-b-mass-window-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-mass-window-transfer.txt)
- [`logs/2026-04-01-directional-b-overlap-margin-card.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-overlap-margin-card.txt)
- [`docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`](/Users/jonreilly/Projects/Physics/docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md)

Together they now say:

- the old `mass_nodes = 3` holdout replay was a real transfer result
- widening the source does not kill the geometry-normalized lane
- it does reveal the portable split more cleanly:
  - `response / b` is asymptotic
  - `response / edge_b` is the finite-source correction that still transfers

## Best next move

Do not reopen a wider denominator search from this result.

That direct overlap map has now landed as:

- [`docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_GEOMETRY_NORMALIZED_OVERLAP_MAP_NOTE.md)

The sharpened read is:

- the failed `N = 25` center-offset rows are concentrated in the existing
  low-`b` overlap / occupancy seam
- they are not a new reason to widen the denominator search

So if this lane is revisited again, keep it equally narrow:

- either test whether the same overlap-conditioned recovery survives on one
  other retained dense-family card
- or move on to the next non-overlapping program lane
