# Staggered Graph Observables Note

**Status:** retained observables probe

This note freezes the graph-native observable split for the staggered /
Kahler-Dirac lane.

## Goal

Tighten the observables used on non-cubic graph families so the retained rows
match the transport law and the graph topology.

## Families

- bipartite random geometric graph
- bipartite growing graph
- layered bipartite DAG-compatible graph

## First Probe

Script: [`frontier_staggered_graph_observables.py`](../scripts/frontier_staggered_graph_observables.py)

### Exact Results

| Family | n | Retained | Centroid shift | Shell bias | Gauge/current |
|---|---:|---:|---:|---:|---:|
| bipartite random geometric | 36 | `8/8` | `-1.110e-16` | `-4.345e-01` | `5.142e-03` PASS |
| bipartite growing | 48 | `8/8` | `+1.110e-16` | `-4.398e-01` | `9.054e-03` PASS |
| layered bipartite DAG-compatible | 36 | `8/8` | `+1.388e-17` | `-4.826e-01` | `N/A` |

## Retained Observables

- Born / linearity
- norm preservation
- force sign
- `F∝M`
- achromatic force
- equivalence
- robustness
- gauge / current only when the graph has cycles

## Secondary Diagnostics

- centroid shift
- shell bias
- depth response

These are useful for understanding recurrence and finite-size effects, but they
should not replace the retained force/current rows on graph families.

## Working Rule

- If the graph has cycles, gauge/current is a retained row.
- If the graph is DAG-compatible, gauge/current is `N/A`.
- Centroid-based gravity diagnostics remain secondary on non-cubic graphs.
