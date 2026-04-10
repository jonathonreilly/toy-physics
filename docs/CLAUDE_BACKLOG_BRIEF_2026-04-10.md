# Claude Backlog Brief

Use this brief for the next pass on the staggered / graph-Dirac program.

## Primary Objective

Test whether staggered / Kahler-Dirac style transport plus potential gravity
survives on non-cubic graph families, then move toward backreaction.

## Working Order

1. Port the staggered transport law to bipartite random geometric graphs,
   bipartite growing graphs, and a layered bipartite DAG-compatible graph.
2. Keep the battery narrow and retained: Born/linearity, norm, force sign,
   `F∝M`, achromatic force, equivalence, robustness, and gauge if cycles exist.
3. If the portable force battery survives, build a backreaction prototype where
   the source field is solved from the graph rather than imposed externally.
4. Write down the graph invariants required by the staggered lane before trying
   any larger redesign.

## Constraints

- Do not modify existing retained card scripts unless a fix is required for
  the new portability harness.
- Keep the force-based staggered card separate from the repo-wide centroid card.
- Treat gauge as conditional: score it only when the graph family actually has
  cycles.
- Treat DAG-compatible graphs as a portability test, not as evidence that the
  transport law is already causal-set complete.

## Deliverables

- One retained portability harness under `scripts/` with a clear task prefix.
- One note under `docs/` with exact results and caveats.
- One backlog note under `docs/` that lists the next work items in priority
  order.

## Recommended Reporting

- State exact graph family, size, seed, and metric values.
- Separate pass/fail from "N/A" rows.
- If a row changes semantics relative to the repo-wide card, say so directly.
