# Claude Backlog Brief

Use this brief for the next pass on the staggered / graph-Dirac program.

## Primary Objective

Test whether staggered / Kahler-Dirac style transport plus potential gravity
survives on non-cubic graph families, then move toward backreaction.

## Working Order

1. Port the staggered transport law to bipartite random geometric graphs,
   bipartite growing graphs, and a layered bipartite DAG-compatible graph.
2. Stress-test the portability result on larger, more irregular bipartite
   families before promoting it: seed-swept or larger-size runs are fine if the
   retained battery stays the same.
3. Build an adversarial failure map for odd-cycle defects, parity ambiguity,
   dense shortcuts, wrap/parity inconsistencies, and high-degree contamination.
4. Keep the battery narrow and retained: Born/linearity, norm, force sign,
   `F∝M`, achromatic force, equivalence, robustness, and gauge if cycles exist.
5. If the portable force battery survives, build a layered backreaction bridge
   where the source field is solved from the graph rather than imposed
   externally.
6. Write down the graph invariants required by the staggered lane before trying
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
- One layered backreaction bridge under `scripts/` with a note under `docs/`
  that freezes exact results and caveats.
- One backlog note under `docs/` that lists the next work items in priority
  order.

## Recommended Reporting

- State exact graph family, size, seed, and metric values.
- Separate pass/fail from "N/A" rows.
- If a row changes semantics relative to the repo-wide card, say so directly.
