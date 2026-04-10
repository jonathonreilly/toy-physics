# Staggered Layered Loop Threshold Note

**Status:** threshold map for native gauge/current closure on sparse layered graphs

This note freezes the minimal nearby layered loop geometry that closes native
gauge/current on the retained staggered graph transport law without losing the
retained force battery.

## Question

Should the sparse layered DAG-like family be frozen as a negative control, or
can a nearby layered cycle geometry close gauge/current natively while keeping
the retained force rows?

## Harness

- Script: [`frontier_staggered_layered_loop_threshold.py`](../scripts/frontier_staggered_layered_loop_threshold.py)
- Inputs anchored to:
  [`frontier_staggered_graph_gauge_closure.py`](../scripts/frontier_staggered_graph_gauge_closure.py),
  [`frontier_staggered_layered_gauge_engineering.py`](../scripts/frontier_staggered_layered_gauge_engineering.py),
  [`frontier_staggered_graph_failure_map.py`](../scripts/frontier_staggered_graph_failure_map.py),
  [`GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md`](./GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md)
- Geometry:
  keep the `seed=13`, `layers=8`, `width=5` layered node cloud, open a
  source-connected two-rail corridor, then insert exactly one local `K2,2`
  plaquette on a selected adjacent-layer window
- Rows:
  retained force battery plus strict native gauge closure
  `J_span > 1e-4` and `|J(0) - J(2pi)| < 1e-8`
- Constraints:
  no 1D helpers, no proxy rows, bipartite/local only

## Threshold Map

| Case | `n/reach` | cycle len | retained | force | `J_span` | `J_resid` | gauge |
|---|---:|---:|---:|---:|---:|---:|---|
| `control_dag` | `36 / 8` | `N/A` | `8/8` | `+3.787e-03` | `N/A` | `N/A` | `N/A` |
| `control_sparse_cycle` | `55 / 28` | `4` | `7/8` | `+3.851e-03` | `4.769e-06` | `6.748e-20` | `FAIL` |
| `two_rail_no_loop` | `36 / 15` | `N/A` | `8/8` | `+3.965e-03` | `N/A` | `N/A` | `N/A` |
| `single_loop_l1` | `36 / 15` | `4` | `8/8` | `+3.965e-03` | `4.944e-02` | `8.028e-18` | `PASS` |
| `single_loop_l2` | `36 / 15` | `6` | `8/8` | `+3.965e-03` | `1.406e-02` | `5.031e-18` | `PASS` |
| `single_loop_l3` | `36 / 15` | `8` | `8/8` | `+3.965e-03` | `4.367e-03` | `2.035e-19` | `PASS` |
| `single_loop_l4` | `36 / 15` | `10` | `8/8` | `+3.965e-03` | `1.617e-03` | `1.808e-19` | `PASS` |
| `single_loop_l5` | `36 / 15` | `12` | `8/8` | `+3.965e-03` | `7.669e-04` | `5.457e-19` | `PASS` |
| `single_loop_l6` | `36 / 15` | `14` | `8/8` | `+3.965e-03` | `1.311e-03` | `8.052e-19` | `PASS` |

## Readout

- The sparse DAG holdout stays machine-clean on the retained force battery, but
  it has no cycle and therefore remains the correct negative control for
  gauge/current.
- The irregular `fanout=2` sparse-cycle holdout proves that cycle existence
  alone is not enough: it keeps a cycle, but its native current span is only
  `4.769e-06`, about `21x` below the retained `1e-4` closure threshold.
- Opening a two-rail corridor without a plaquette still gives `gauge = N/A`, so
  the win is not caused by source fanout alone.
- Inserting exactly one local `K2,2` plaquette is already sufficient. Every
  tested one-plaquette case keeps `8/8` retained rows and `gauge = PASS`.
- The weakest passing one-plaquette case is `single_loop_l5`, and it still
  clears the gauge threshold comfortably with `J_span = 7.669e-04`.

## Structural Guardrails

All passing threshold families stay inside the requirements and failure-map
guardrails:

- same-color edges: `0`
- long-edge fraction: `0.00`
- max degree: `3`

So the promoted loop geometry is still bipartite, local, and layered. The win
comes from one controlled even plaquette, not from dense shortcuts or parity
defects.

## Decision

Freeze [`layered_bipartite_dag_s13_n36`](../scripts/frontier_staggered_layered_backreaction.py)
as the negative control for gauge/current. The minimal nearby positive geometry
is a source-connected two-rail layered corridor with one local `K2,2`
plaquette. That is enough to close gauge/current natively on the retained
staggered transport law without losing the retained force battery.
