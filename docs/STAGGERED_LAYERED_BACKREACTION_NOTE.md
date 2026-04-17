# Staggered Layered Backreaction Note

**Status:** first layered/DAG-compatible backreaction bridge

This note freezes the first retained bridge between the staggered transport law
and a source-generated `Phi` on layered graph families.

## Question

Can the staggered force result survive when `Phi` is solved on the same graph
instead of being imposed externally?

## Harness

- Script: [`frontier_staggered_layered_backreaction.py`](../scripts/frontier_staggered_layered_backreaction.py)
- Observable: force `F = -<dPhi/dd>`
- Controls: zero-source, source-on, source-doubling / linearity sweep
- Stability: one DAG-compatible layered family plus one cycle-bearing layered
  stress family

## First Retained Run

| Family | n | zero-source `Phi` | zero-source force | source-on force | source `R^2` | `Phi` residual | norm drift | robustness | gauge |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `layered_bipartite_dag_s13_n36` | 36 | `0.00e+00` | `+0.000e+00` | `+3.064e-01` TOWARD | `1.0000` | `3.84e-16` | `3.33e-16` | `3/3` | `N/A` |
| `layered_bipartite_dag_s29_n55` | 55 | `0.00e+00` | `+0.000e+00` | `+1.849e-01` TOWARD | `1.0000` | `1.69e-16` | `2.22e-16` | `3/3` | `FAIL` |

## Readout

- Zero-source control is exact on both layered families.
- The source-on response stays TOWARD on both families.
- The source-response linearity is exact to machine precision (`R^2 = 1.0000`).
- Norm stays machine-clean.
- The DAG-compatible baseline has no gauge/current row, as expected.
- The cycle-bearing stress family still has a weak gauge failure, so native
  gauge closure is not yet part of the retained bridge.

## Blockers

1. The source field is still a point-source / screened-Poisson approximation, not
   a fully endogenous density-fed backreaction sector.
2. The layered stress family does not yet give a retained gauge/current win.
3. This is a bridge result, not a self-gravity closure.

## Next Step

Replace the point-source approximation with a graph-solved source sector fed by
the evolving matter density, then rerun the same zero-source / source-on /
stability battery on the layered family before expanding outward.
