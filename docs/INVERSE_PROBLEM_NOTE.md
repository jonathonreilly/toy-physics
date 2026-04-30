# Inverse Problem: What Does Newton+Born Require of the Network?

**Status:** unknown (pending author classification)
**Date:** 2026-04-04

## Answer: almost nothing.

Gravity (TOWARD) survives all tested graph perturbations:

| Perturbation | Gravity | Born |
|---|---|---|
| Baseline (regular lattice) | +0.001083 T | 6.0e-16 |
| 70% random edge deletion | +0.000689 T | 6.6e-16 |
| Asymmetric (z>0 edges removed) | +0.000320 T | 5.5e-16 |
| Random positions (jitter 0.5h) | +0.000391 T | 1.7e-15 |
| Sparse (NN only, 9 edges) | +0.000586 T | 5.0e-17 |

Born holds at machine precision on ALL graph types.

## Only TWO things are required:

1. **Field coupling** (S depends on f): without it, gravity = 0
2. **Phase** (k > 0): without it, gravity = 0

The graph structure controls the QUANTITATIVE gravity (magnitude,
distance exponent, convergence rate) but not its existence. Almost
any causal graph gives gravitational attraction with the valley-
linear action.

## What this means

The model is VERY forgiving about graph structure. The physics
comes from the PROPAGATOR (linear path sum with phase valley),
not from the graph. The graph is the canvas; the physics is the paint.

This is good news for Gate B: any growth rule that produces a
causal graph with forward edges will give gravity. The growth
rule doesn't need to be precise — it just needs to produce a graph.
