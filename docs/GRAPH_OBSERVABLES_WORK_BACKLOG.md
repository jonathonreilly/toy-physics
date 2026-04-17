# Graph Observables Work Backlog

This backlog is the active queue for graph-native observables on the staggered
lanes.

## P0

- Validate force/current as the retained observables on cycle-bearing graph
  families.
- Confirm centroid and shell diagnostics remain secondary on layered / DAG-
  compatible graphs.

## P1

- Extend the observables probe to a larger irregular bipartite family if the
  current families stay clean.
- Use the observables split to decide which rows belong in future graph-native
  cards and which should stay diagnostic only.

## P2

- Add a backreaction version only after the retained observables are stable on
  the current portability families.
- Keep the canonical staggered card untouched while this work is in progress.
