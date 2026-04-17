# Claude Backlog Brief

Use this brief for the next pass on the staggered / graph-Dirac program.

## Primary Objective

Portability is no longer the main question. The next objective is:

1. materially reduce or close the endogenous-field force-scale gap on the
   cycle-bearing graph families
2. preserve the explicit layered-cycle gauge/current closure while treating
   the sparse layered DAG-like graph as a negative control

## Working Order

1. Port the staggered transport law to bipartite random geometric graphs,
   bipartite growing graphs, and a layered bipartite DAG-compatible graph.
2. Stress-test the portability result on larger, more irregular bipartite
   families before promoting it: seed-swept or larger-size runs are fine if the
   retained battery stays the same.
3. Keep the battery narrow and retained: Born/linearity, norm, force sign,
   `F∝M`, achromatic force, equivalence, robustness, and gauge only when the
   graph family actually has cycles.
4. Attack endogenous-field scale closure on the cycle-bearing families:
   the solved/source-generated `Phi` has the right sign, linearity, additivity,
   and norm behavior, but it is still too weak relative to the external-kernel
   control.
5. Use the explicit layered brickwall / plaquette geometry as the retained
   layered gauge/current closure. Keep the sparse layered DAG-like family as a
   negative control. Do not fall back to 1D helpers or proxy rows.
6. Add shell-profile / spectral diagnostics for `phi_solved` vs `phi_ext` so
   the source-sector miss is explained structurally.
7. Keep the graph invariants and failure map current before trying any larger
   redesign.

## Constraints

- Do not modify existing retained card scripts unless a fix is required for
  the new portability harness.
- Keep the force-based staggered card separate from the repo-wide centroid card.
- Treat gauge as conditional: score it only when the graph family actually has
  cycles.
- Treat DAG-compatible graphs as a portability test, not as evidence that the
  transport law is already causal-set complete.
- Treat native gauge closure as a separate blocker from portability: the next
  retained win should be the layered cycle-bearing holdout, not more stress
  passes on families that already close.
- Treat portability as established enough for now: do not spend more time on
  first-pass graph families unless a new source/gauge result forces it.

## Deliverables

- One endogenous-field closure harness under `scripts/` with exact force-scale
  comparisons on the cycle-bearing families.
- One layered gauge-closure harness under `scripts/` that stays on the
  graph-native staggered transport law and targets explicit layered loop
  geometry.
- One diagnostic note under `docs/` comparing `phi_solved` vs `phi_ext` by
  shell/depth or low-mode content.
- One backlog note under `docs/` kept aligned to the current blockers.

## Recommended Reporting

- State exact graph family, size, seed, and metric values.
- Separate pass/fail from "N/A" rows.
- If a row changes semantics relative to the repo-wide card, say so directly.
