# Staggered Backreaction Capture-Closure Note

**Date:** 2026-04-10  
**Status:** retained positive closure on the cycle-bearing battery, with one layered holdout check

## Objective

Move the source-generated staggered field materially closer to the
external-kernel force scale without relying on another fitted global gain, and
without losing the retained force battery on the cycle-bearing graphs.

## Harness

- Script: [`frontier_staggered_backreaction_capture_closure_harness.py`](../scripts/frontier_staggered_backreaction_capture_closure_harness.py)
- Cycle-bearing retained battery:
  - `random_geometric`, `n=36`
  - `growing`, `n=48`
- Layered holdout:
  - `layered_bipartite_dag_s29_n55`
- Observable:
  - force `F = < -dPhi/dd >`

## Closure Rule

The source sector is closed iteratively on the same graph:

1. start from the local Gaussian seed source
2. evolve the staggered probe in the solved graph field
3. refresh the source shape with a 50/50 blend of
   - the original seed source
   - one normalized-Laplacian sharpen step applied to the returned density
4. update the source gain from the source-pocket capture deficit:

`gain <- capture^(-3/2)`

with relaxed fixed-point iteration.

The external kernel is **not** used to fit the closure. It remains a control
only.

## Exact Cycle-Battery Results

| Graph | Score | Closed force | External force | Baseline gap | Closed gap | `R^2` | Gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_geometric` | `9/9` | `+4.842e-01` | `+5.200e-01` | `9.690e-01` | `6.880e-02` | `0.999265` | `44.504` |
| `growing` | `9/9` | `+3.222e-01` | `+5.534e-01` | `9.944e-01` | `4.178e-01` | `0.998906` | `100.726` |

Retained rows stayed intact:

- zero-source control exact on both graphs
- source-response linearity stayed above `0.9989`
- two-body additivity stayed at machine precision
- iterative stability stayed `15/15` TOWARD
- norm drift stayed at machine precision
- state-family robustness stayed `3/3`
- native gauge row still passed

Cycle-bearing mean force gap:

- baseline: `9.817e-01`
- closed: `2.433e-01`
- improvement: `4.03x`

## Layered Holdout

On `layered_bipartite_dag_s29_n55`:

- closed force: `+1.655e+00`
- external force: `+2.010e+00`
- baseline gap: `9.080e-01`
- closed gap: `1.764e-01`
- improvement: `5.15x`
- source-response `R^2 = 0.999777`

So the closure is not just rescuing the cycle-bearing rows by a graph-specific
fit. One larger layered holdout also moves substantially toward the external
control.

## Readout

- The earlier linear-map lane was right that the missing piece was the source
  sector itself, not the force observable.
- A self-consistent capture closure can preserve the retained cycle battery
  while moving the solved field much closer to the external-kernel scale.
- The growing graph remains the harder cycle-bearing row, so this is not yet a
  universal closure theorem.
- But the blocker is no longer "the endogenous field always stays an order of
  magnitude too weak." That statement is now false on the retained harness.
