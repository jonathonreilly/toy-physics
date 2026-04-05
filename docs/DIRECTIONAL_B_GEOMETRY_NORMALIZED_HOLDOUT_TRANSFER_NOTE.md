# Directional-B Geometry-Normalized Holdout Transfer Note

**Date:** 2026-04-04  
**Status:** bounded family-transfer replay for geometry-normalized response density

## Artifact chain

- Script: [`scripts/directional_b_geometry_normalized_holdout_transfer.py`](/Users/jonreilly/Projects/Physics/scripts/directional_b_geometry_normalized_holdout_transfer.py)
- Log: [`logs/2026-04-04-directional-b-geometry-normalized-holdout-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-directional-b-geometry-normalized-holdout-transfer.txt)

This follow-on keeps the retained directional propagator and the same
mass-side action observables fixed:

```text
exp(i k S_spent) / L^p × exp(-β θ²),  β = 0.8
```

It asks one narrow transfer question:

- do the retained geometry-normalized response densities survive on the older
  second dense-family holdout, or were they only a feature of the original
  dense random-DAG generator?

The replay uses:

- original dense family: `25` nodes/layer, `y_range = 12`, `radius = 3`
- second dense-family holdout: `28` nodes/layer, `y_range = 13`, `radius = 3`
- same `mass_nodes = 3`, `N = 12, 25`, `b = 1.5 .. 7.5`, `5` seeds

## Frozen result

The baseline replay reproduces the earlier pass, and the holdout family keeps
the same directional hierarchy.

### Shared family-local passes

For both `N = 12` and `N = 25`, all four retained normalized metrics still
decrease with actual `b` on both families:

- `action_channel / b`
- `action_channel / edge_b`
- `packet_flow_action / b`
- `packet_flow_action / edge_b`

### Holdout endpoints

On the second dense-family holdout:

- `N = 12`
  - `A/b`: `0.1746 -> 0.0349`
  - `A/edge`: `0.1655 -> 0.0399`
  - `F/b`: `0.2208 -> 0.0389`
  - `F/edge`: `0.2359 -> 0.0449`
- `N = 25`
  - `A/b`: `0.1862 -> 0.0406`
  - `A/edge`: `0.1168 -> 0.0460`
  - `F/b`: `0.1304 -> 0.0352`
  - `F/edge`: `0.0592 -> 0.0395`

The raw action-style strengths still rise with `b`, so this does **not** repair
the raw distance-law caveat. The retained statement is only about the
geometry-normalized density trend.

## Safe read

This strengthens the current directional-`b` hierarchy in one bounded way:

- center-offset density is not just a one-generator accident
- nearest-edge density is still the safer finite-source correction
- the corrected read now transfers across the original dense family and the
  existing second dense-family holdout without changing transport or observables

So the current hierarchy remains:

- asymptotic leading term: `response / b`
- safer finite-source correction: `response / (b - h_mass)`
- discrete packet-support correction: secondary, family-sensitive, and not the
  promoted main law

## Relation to the existing lane

This note should be read with:

- [`docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`](/Users/jonreilly/Projects/Physics/docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md)
- [`logs/2026-04-01-directional-b-geometry-normalized-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-geometry-normalized-compare.txt)
- [`logs/2026-04-01-directional-b-mass-window-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-mass-window-transfer.txt)
- [`logs/2026-04-01-directional-b-asymptotic-bridge-card.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-01-directional-b-asymptotic-bridge-card.txt)
- [`docs/DIRECTIONAL_B_DENSITY_STENCIL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIRECTIONAL_B_DENSITY_STENCIL_NOTE.md)

Together they now say:

- the geometry-normalized response-density hierarchy transfers across the two
  dense-family generators already on disk
- the remaining open gravity-side question is not another wide denominator
  search; it is how far that hierarchy survives once low-`b` overlap and
  widened-source effects become dominant
- the overlap-onset seam still stays occupancy-first, with the current smooth
  law limited by stencil-local residuals rather than a new global denominator

## Best next move

The next bounded follow-on should stay on the same lane:

- test whether the same holdout transfer survives the widened `mass_nodes = 5`
  family, where the finite-source correction should matter most

If that fails, the honest read is still useful:

- `b` remains the clean asymptotic leading term
- `b - h_mass` remains the practical finite-source correction
- the limit is family overlap geometry, not absence of a geometry-normalized
  trend
