# Emergent Geometry from Matter-Coupled Growth

**Date:** 2026-04-10  
**Status:** bounded - bounded or caveated result note
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

Initial single-seed growth result (frozen 2026-04-10 numbers; current
runner produces values in the same qualitative direction but slightly
different specific numbers — see live runner output for the current pass):

| Metric | Matter-coupled growth | Uniform-growth control |
| --- | ---: | ---: |
| Effective dimension `d_eff` | ~`1.6-2.0` (`R²>0.97`) | ~`1.5-1.6` (`R²>0.95`) |
| Peak shell-bin density | order `10^2 / unit²` | order `10^1 / unit²` |
| Parent-node clustering | several-x above uniform | N/A |

The qualitative finding survives: the matter-coupled grown graph has a higher
effective dimension and a denser peak shell than the uniform control. The
exact numerics drift across runs because the growth rule has stochastic seed
dependence (see the multi-seed audit below).

Follow-up audit on the stronger `v2` probe, before hardening the growth rule:

- node density vs `Φ`: `R²≈0.1353` on the seed-42 `G=100` run
- `d_eff` vs coupling: fluctuates `~1.5-2.2`, not monotone in `G`
- grown-graph gravity sign: **seed- and `G`-dependent**
  - `G=50`: mixed/AWAY on the seed-42 single run
  - `G=100`: `ROBUST_TOWARD` on the seed-42 single run, but not seed-robust
  - `G=150`: mixed/AWAY on the seed-42 single run
- 3D seeds do **not** preserve `d_eff≈3`

Hardened audit on the retained `k=4` growth rule:

- this is the only minimal growth-rule change that clearly expanded the
  robust-TOWARD region without changing the coupling semantics
- compared with `matter_k3`, `matter_k4` improved the `G=100` robust-TOWARD
  count from `3/10` to `8/10`
- `degree_penalty_k4` ties the `8/10` robust-TOWARD count at `G=100`, but its
  density-`Φ` correlation is much weaker (`mean R²≈0.098`), so it does not beat
  `matter_k4` as the retained rule
- `uniform_k4` does not match the retained rule on either sign stability or
  density-`Φ` quality
- the density-`Φ` correlation also strengthened:
  - `G=50`: `mean R²=0.411`, `8/10` ROBUST_TOWARD
  - `G=100`: `mean R²=0.454`, `8/10` ROBUST_TOWARD
  - `G=150`: `mean R²=0.283`, `6/10` ROBUST_TOWARD
- the single-seed `G=100` density-`Φ` check is now clearly positive:
  - `R²=0.5788`, positive slope
- `G=100` is the best retained operating point, but it is **not** universal
  across seeds

## Honest reading

- This remains a **real exploratory geometry result**: the growth rule changes
  the coarse graph geometry in a matter-correlated way.
- The new `G` sweep partially reopens the lane at strong coupling:
  - `G=100` is the narrow retained high-`G` window where the grown graph is
    robust TOWARD on the audited measures
  - lower and higher `G` remain mixed or AWAY
- It is **still not fully retained** because:
  - the density-to-`Φ` correlation is positive but seed-dependent
  - `d_eff(G)` is not monotone and does not encode a clean curvature law
  - the gravity diagnostics are mixed away from the high-`G` operating point
  - 3D seeds do not preserve `d_eff≈3`

## Why it matters

This is still the first growth result in the current staggered program that
looks like a plausible bridge from “physics on a fixed graph” toward “matter
shapes geometry,” but the bridge is only geometric so far, not gravitationally
closed. Treat the strong-coupling window as a partial reopen, not retained
closure.

## Next acceptance gates

1. multi-seed robustness at `G=100` and a nearby lower/higher `G`
2. compare the retained `k=4` rule against at least one alternative minimal
   attachment rule
3. agreement between a probability-weighted shell force and an edge-radial
   force on the grown graph at the retained operating point
4. a curvature / metric comparison, not just shell-volume scaling
