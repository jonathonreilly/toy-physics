# Staggered Graph Gauge Closure Results

**Status:** proposed_retained gauge/current closure result

This note freezes the first dedicated native gauge/current closure run for the
staggered graph lane.

## Question

Can the retained staggered transport law produce a native gauge/current win on
cycle-bearing layered or stress graphs without falling back to 1D helpers or
proxy rows?

## Harness

- Script: [`frontier_staggered_graph_gauge_closure.py`](../scripts/frontier_staggered_graph_gauge_closure.py)
- Operator: native staggered Hamiltonian with flux threaded through the
  detected cycle edge
- Observable: ground-state persistent-current span over `phi in [0, 2pi]`
- Retained side battery: Born/linearity, norm, force sign, `F∝M`, achromatic
  force, equivalence, robustness

## Exact Results

| Family | n | cycle | Retained | Force | F∝M | Achrom | Equiv | Robust | J span | J resid | Gauge |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| bipartite random geometric stress `s17` | 81 | yes | `8/8` | TOWARD | `1.000` | `1.271e-16` | `1.078e-16` | `3/3` | `6.922e-04` | `4.478e-19` | PASS |
| bipartite growing stress `s23` | 82 | yes | `8/8` | TOWARD | `1.000` | `2.369e-16` | `1.589e-16` | `3/3` | `2.050e-03` | `3.679e-18` | PASS |
| bipartite chorded grid stress `s31` | 144 | yes | `8/8` | TOWARD | `1.000` | `0.000e+00` | `1.719e-16` | `3/3` | `1.342e-04` | `3.405e-19` | PASS |
| layered bipartite DAG `s13` | 36 | no | `8/8` | TOWARD | `1.000` | `1.699e-16` | `1.683e-16` | `3/3` | `N/A` | `N/A` | N/A |
| layered bipartite DAG `s29` | 55 | yes | `7/8` | TOWARD | `1.000` | `1.126e-16` | `0.000e+00` | `3/3` | `4.769e-06` | `6.748e-20` | FAIL |

## Closure Readout

- Native gauge/current closes on the cycle-bearing stress families.
- The best geometry in this run is the bipartite growing stress family
  `s23` at `n=82`.
- The operator that closes it is the native staggered Hamiltonian with flux
  threaded through the graph's detected cycle edge.
- The observable that closes it is the ground-state persistent-current span
  over `phi in [0, 2pi]`.

## Readout

- The retained force battery survives on all cycle-bearing stress families.
- Gauge/current is correctly `N/A` on the acyclic layered DAG family.
- The layered bipartite DAG `s29` is the narrow negative: it has a cycle but
  still fails the gauge closure threshold in this probe.

## Caveat

This is a retained native-gauge result, not a new canonical card.
Force remains the primary gravity observable; current is the gauge observable.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `staggered_graph_gauge_closure_note` (UPSTREAM framing note; this
  results note is the data appendix that the framing note describes —
  citation graph direction is *framing_note → results*; backticked here
  to avoid the length-2 cycle that a reverse-direction markdown link
  would create)
- [staggered_graph_portability_note](STAGGERED_GRAPH_PORTABILITY_NOTE.md)
