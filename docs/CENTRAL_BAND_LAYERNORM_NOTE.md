# Central-Band Removal + Layernorm Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_layernorm_combo.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

Date: 2026-04-02

## Purpose

This note records the direct comparison between the simplest hard-geometry
rule from the gap thread and the current best Born-clean regulated propagator:

- remove post-barrier nodes with `|y - center| < y_cut`
- propagate on the same graph with per-layer normalization

The goal was to answer:

1. what `|y|` threshold works best?
2. how does the joint gravity/decoherence card scale from `N=25` to `N=100`?
3. how does this compare to the modular-gap + layernorm lane?

## Script

- [central_band_layernorm_combo.py](/Users/jonreilly/Projects/Physics/scripts/central_band_layernorm_combo.py)

## Main table

Settings:
- `nodes_per_layer = 25`
- `y_range = 12`
- `connect_radius = 3.0`
- `16 seeds`
- `N = 25, 40, 60, 80, 100`
- `y_cut = 1, 2, 3`

### Layernorm `pur_min`

Base layernorm row:
- `N=25`: `0.811`
- `N=40`: `0.801`
- `N=60`: `0.875`
- `N=80`: `0.948`
- `N=100`: `0.961`

Best pruned rows:
- `N=25`: `y_cut=2 -> 0.668`
- `N=40`: `y_cut=1 or 2 -> 0.734/0.736`
- `N=60`: `y_cut=2 -> 0.816`
- `N=80`: `y_cut=3 -> 0.881`
- `N=100`: `y_cut=2 -> 0.876`

So the strongest overall threshold on the decoherence side is:
- **`|y-center| < 2`**

## Joint gravity read

The threshold tradeoff is not identical on the gravity side.

### Strongest gravity-retaining pockets

- `N=40`, `y_cut=2`
  - layernorm gravity: `+1.664 ± 0.821`
  - about `2.0 SE`
- `N=80`, `y_cut=1`
  - layernorm gravity: `+1.668 ± 0.637`
  - about `2.6 SE`
- `N=80`, `y_cut=2`
  - layernorm gravity: `+1.440 ± 0.644`
  - about `2.2 SE`
- `N=100`, `y_cut=1`
  - layernorm gravity: `+1.022 ± 0.890`
  - positive but weaker

So the strongest gravity-preserving threshold at large `N` is usually:
- **`|y-center| < 1`**

## Scaling fit for the best overall threshold

Using the decoherence-optimal `y_cut = 2` layernorm row:

- `N=25`: `pur_min = 0.668`
- `N=40`: `0.736`
- `N=60`: `0.816`
- `N=80`: `0.887`
- `N=100`: `0.876`

Fit:

- `(1 - pur_min) = 4.81 × N^(-0.813)`
- `R^2 = 0.932`

Derived range estimates:
- `pur_min = 0.90` at about `N ≈ 117`
- `pur_min = 0.99` at about `N ≈ 1993`

## Comparison to modular gap=2 + layernorm

The modular-gap row remains cleaner:

- `(1 - pur_min) = 6.94 × N^(-0.916)`
- `R^2 = 0.957`
- `pur_min = 0.90` at about `N ≈ 103`
- `pur_min = 0.99` at about `N ≈ 1269`

Comparison:

- central-band `|y|<2` is slightly worse at small `N=25`
- better around `N=40`, `N=60`, and `N=100`
- slightly worse at `N=80`
- has a shallower exponent but a longer extrapolated tail

Safe conclusion:
- the simple `|y|`-removal rule is **competitive** with the imposed modular
  gap once combined with layernorm
- but it does **not** clearly dominate modular gap=2 across the whole range

## Best supported wording

- `|y-center| < 2` is the best overall **decoherence** threshold
- `|y-center| < 1` is the best **gravity-preserving** threshold at larger `N`
- the lane is real and scales through `N=100`
- it is competitive with modular gap=2 + layernorm, but not an outright winner
