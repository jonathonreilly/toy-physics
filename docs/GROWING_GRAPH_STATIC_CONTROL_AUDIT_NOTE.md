# Growing Graph Static Control Audit Note

**Date:** 2026-04-06  
**Status:** retained graph-distance proxy; dynamic-propagation no-go

## Artifact chain

- [`scripts/growing_graph_dynamic_limit_diag.py`](/Users/jonreilly/Projects/Physics/scripts/growing_graph_dynamic_limit_diag.py)
- [`logs/2026-04-06-growing-graph-static-control-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-growing-graph-static-control-audit.txt)

## What was tested

This audit reran the existing growing-graph diagnostic against a frozen static
control and checked whether the dynamic-propagation signal can be promoted to a
stable growth observable.

The diagnostic compares:

- frontier-delay growth on the expanding-graph proxy
- dynamic-propagation visibility drop against a static graph control

## Frozen readout

The rerun is stable and matches the existing shape:

- frontier delay: `3.000 -> 22.000`
- frontier-delay slope: `+0.9325` hops/step
- RMS-delay slope: `+0.5981` hops/step
- width slope: `+0.2129` hops/step
- static-control frontier delay: `3.000`
- dynamic visibility drop at `n_layers = 10`: `+0.0492` with `4/10` positive seeds
- dynamic visibility drop at `n_layers = 15`: `+0.0366` with `4/10` positive seeds
- dynamic visibility drop at `n_layers = 20`: `+0.0224` with `2/10` positive seeds

## Safe read

The review-safe conclusion is:

- frontier delay is the retained expansion observable
- the dynamic-propagation visibility signal is noisy, seed-dependent, and not monotone
- the graph-growth story is better framed as distance expansion against a
  static control than as a repaired propagation law
- the dynamic-propagation repair lane remains a bounded no-go unless a future
  replay can beat the static-control comparison and recover monotonicity

The tightened claim boundary is:

- promote the frontier-delay proxy only
- keep dynamic-propagation repair as a static-control failure
- do not widen the result to a transport or cosmology statement

## What this does not claim

- no cosmology derivation
- no transport theorem
- no unitarity or field-theory claim

## Final verdict

**retain graph-distance expansion; freeze dynamic-propagation repair as no-go**
