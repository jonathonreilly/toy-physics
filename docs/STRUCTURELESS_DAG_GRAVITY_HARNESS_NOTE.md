# Structureless DAG Gravity Harness Note

**Date:** 2026-04-05
**Status:** bounded harness result

## Setup

This harness tests the note-only structureless-DAG claim with a narrow seed
sweep on random causal DAGs:

- 3D points sampled uniformly and then sorted by `x` to impose causality
- edges from `i -> j` when `x_j > x_i` and `dist(i, j) <= 0.35`
- source slab: `x <= 0.05`
- detector slab: `x >= 0.95`
- one weak source mass placed at the highest-`z` node in the mid-`x` slab
- valley-linear action `S = L(1-f)`
- `1/L^2` kernel
- phase `k = 1.0`

The sweep is intentionally bounded to the pocket that produced stable seed
statistics in trial runs:

- `n = 200` nodes, 8 seeds
- `n = 500` nodes, 8 seeds
- strengths: `1e-3, 2e-3, 5e-3, 1e-2`

## Results

### `n = 200`

- TOWARD: `28/32` = `87.5%`
- seed-local `F~M` median: `1.00`
- seed-local `F~M` mean: `1.00`
- median local `R^2`: `1.000`
- no-field control: `+0.0e+00`

### `n = 500`

- TOWARD: `21/32` = `65.6%`
- seed-local `F~M` median: `1.00`
- seed-local `F~M` mean: `1.00`
- median local `R^2`: `1.000`
- no-field control: `+0.0e+00`

### Combined read

- TOWARD rows: `49/64` = `76.6%`
- when the detector shift is TOWARD, the source-strength response stays
  close to linear in this pocket
- the sign is seed-sensitive, but the slope on positive rows is stable

## Interpretation

The safe claim is narrow:

> On this bounded random-causal-DAG pocket, valley-linear propagation
> produces TOWARD shifts in the majority of seeds, and the TOWARD rows
> retain approximately linear mass scaling (`F~M ≈ 1.0`).

What this does **not** show:

- it does not prove graph universality
- it does not show that every random DAG behaves the same way
- it does not extend the claim to the numerically unstable 1000-node raw
  pocket from the earlier note-only probe

The no-field control stays at zero by construction, so the retained signal is
in the sourced phase response, not in the baseline graph transport.
