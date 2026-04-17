---
experiment: dimensional-scaling-law
date: 2026-04-01
status: PARTIALLY CONFIRMED
confidence: HIGH (alpha increases with d), LOW (exact formula)
---

# Dimensional Scaling Law: Revisited

## What is confirmed

**Alpha (mass scaling exponent) increases with spatial dimension.**

This is robust across both optimized and unified parameter sets:
- 2D: alpha near 0 (threshold/weak scaling)
- 3D: alpha ~ 0.35-0.52 (sub-linear, around sqrt(M))
- 4D: alpha ~ 0.64-1.07 (approaching linear)

The progression is real and reproducible.

## What is NOT confirmed

**The formula alpha = (d-1)/2 is premature.**

The initial claim was based on three individually-optimized experiments
that happened to give alpha ≈ 0, 0.5, 1.0. A unified test with
matched parameters gives:

| d | (d-1)/2 | Unified params | Optimized params |
|---|---|---|---|
| 1 | 0.0 | 0.13 | ~0 |
| 2 | 0.5 | 0.35 | 0.52 |
| 3 | 1.0 | 0.64 | 1.07 |
| 4 | 1.5 | 0.44 (unreliable) | — |

The optimized values (with connect_radius tuned per dimension) are
higher because larger connect_radius gives denser graphs with more
paths, amplifying the mass scaling effect.

## The 5D problem

5D (4 spatial + 1 causal) with 25-30 nodes per layer in a 16^4
volume is extremely sparse. Average node separations exceed the
connect_radius, leading to:
- Few edges per node
- Weak amplitude at detectors (shift ~ 1e-4)
- t-values < 1 for all mass counts

5D requires either:
- Many more nodes per layer (100+) to fill the volume
- Much larger connect_radius (defeats the locality structure)
- Smaller spatial_range

## The honest picture

The model shows a real dimensional dependence of mass scaling:
- More spatial dimensions → stronger mass dependence
- The effect is monotonic and consistent across parameter regimes
- At 3 spatial dimensions (4D), the effect CAN reach F~M with
  optimized parameters (connect_radius=4.5, gap=5)

But alpha is parameter-dependent, not a pure function of d.
The specific value depends on:
- connect_radius (larger → higher alpha)
- gap (larger → higher alpha, but too large → disconnection)
- nodes_per_layer (more → higher alpha via better statistics)

The (d-1)/2 pattern may emerge in a continuum limit where these
parameters are scaled appropriately, but we can't confirm it with
discrete finite graphs.

## Revised claim

**The model exhibits dimensionality-dependent mass scaling that
approaches Newtonian (F~M) at 3 spatial dimensions under
appropriate graph parameters.** The exact functional form alpha(d)
is sensitive to graph density and channel separation, and the
simple formula alpha = (d-1)/2 is not confirmed.

## Scripts

- `scripts/dimensional_scaling_law.py` — unified d=1-4 comparison
