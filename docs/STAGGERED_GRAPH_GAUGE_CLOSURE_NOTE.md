# Staggered Graph Gauge Closure Note

**Status:** proposed_retained gauge/current closure probe

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

## Expected Readout

- Cycle-bearing layered or stress families: score current span and periodicity
  residual on the native cycle edge
- Acyclic layered family: `gauge = N/A`
- No 1D helpers, no slit-phase proxy rows

## What Counts as Closure

The gauge/current lane is considered closed only if a cycle-bearing family shows
both:

- nontrivial current span under threaded flux
- periodic closure at `phi = 0` and `phi = 2pi`

The best geometry/operator/observable combination should be stated explicitly
from the frozen run, not inferred from the portability probes.

## Working Rule

- Keep force as the primary gravity observable.
- Treat gauge/current as a separate native observable on cycle-bearing graphs.
- Treat DAG-compatible graphs as `N/A` for gauge/current.
- Do not promote proxy gauge rows into this lane.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_graph_gauge_closure_results_2026-04-10](STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md)
- [staggered_graph_portability_note](STAGGERED_GRAPH_PORTABILITY_NOTE.md)
