# Emergent Geometry from Matter-Coupled Growth

**Date:** 2026-04-10  
**Status:** exploratory mixed, not yet retained  
**Scripts:** `frontier_emergent_geometry.py`, `frontier_emergent_geometry_v2.py`

## Question

Can a local growth rule biased by quantum matter density `|psi|^2` produce a
graph whose coarse geometry differs measurably from a matter-blind growth
control?

## Probe

- Start from a small bipartite seed graph.
- Evolve a staggered matter field with self-gravity.
- Add new nodes preferentially near high-`|psi|^2` regions.
- Compare against a uniform-growth control.
- Measure shell-volume scaling, central density, and clustering.

## Current outputs

Initial single-seed growth result:

| Metric | Matter-coupled growth | Uniform-growth control |
| --- | ---: | ---: |
| Effective dimension `d_eff` | `2.03` (`R²=0.9839`) | `1.54` (`R²=0.9440`) |
| Central node density | `108 / unit²` | `11 / unit²` |
| Parent-node clustering | `5.43x` above uniform | N/A |

Follow-up audit on the stronger `v2` probe:

- node density vs `Φ`: `R²≈0.0005` (no useful correlation)
- `d_eff` vs coupling: fluctuates `~1.5-2.0`, not monotone in `G`
- grown-graph gravity sign: **mixed**
  - shell-radial proxies can be AWAY
  - edge-radial force can remain TOWARD on the same graph
- 3D seeds do **not** preserve `d_eff≈3`

## Honest reading

- This remains a **real exploratory geometry result**: the growth rule changes
  the coarse graph geometry in a matter-correlated way.
- It is **not yet retained** because the stronger follow-up audit found:
  - no clean density-to-`Φ` correlation
  - no systematic `d_eff(G)` curvature story
  - mixed gravity-sign diagnostics on the grown graph
  - no preservation of seed dimensionality

## Why it matters

This is still the first growth result in the current staggered program that
looks like a plausible bridge from “physics on a fixed graph” toward “matter
shapes geometry,” but the bridge is only geometric so far, not gravitationally
closed.

## Next acceptance gates

1. multi-seed robustness
2. at least one alternative growth rule
3. agreement between a probability-weighted shell force and an edge-radial
   force on the grown graph
4. a curvature / metric comparison, not just shell-volume scaling
