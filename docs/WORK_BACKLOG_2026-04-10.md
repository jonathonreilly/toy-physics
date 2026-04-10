# Work Backlog

**Scope:** next steps for the retained staggered / graph-Dirac program.

This backlog is ordered by value to the main project, not by ease.

## P0 - Endogenous Field Closure

- Frozen narrow positive:
  [`frontier_staggered_backreaction_green_closure.py`](../scripts/frontier_staggered_backreaction_green_closure.py)
  and
  [`STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md`](../docs/STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md)
  now give a graph-native direct Green map (`resistance_yukawa`) that cuts the
  retained cycle-bearing mean gap from `8.899e-01` to `9.889e-02` and the
  layered holdout gap from `8.759e-01` to `1.680e-02`, while preserving the
  retained force battery.
- Portability is now established enough for the retained force battery:
  baseline portability, stress portability, and the failure map are all frozen.
- Native gauge/current closure is now retained on the cycle-bearing stress
  families, and explicit layered brickwall / plaquette geometries also close
  the current probe.
- True self-gravity is now retained on the three cycle-bearing graph families
  in [`frontier_staggered_self_gravity.py`](../scripts/frontier_staggered_self_gravity.py).
- A retained scaling readout now exists in
  [`frontier_staggered_self_gravity_scaling.py`](../scripts/frontier_staggered_self_gravity_scaling.py):
  inward force is stable, but contraction is topology-sensitive.
- A retained larger-graph sibling now exists in
  [`frontier_staggered_cycle_battery_scaled.py`](../scripts/frontier_staggered_cycle_battery_scaled.py):
  the force-first `9/9` battery stays closed on side `8`, `10`, and `12`.
- A first two-field endogenous coupling is now retained as a prototype in
  [`frontier_two_field_coupling.py`](../scripts/frontier_two_field_coupling.py),
  but it still uses relaxation dynamics for `Phi`.
- A wave-law two-field hardening is now retained in
  [`frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py): hard
  `5/5` on the retained cycle-bearing families, with width kept as a
  diagnostic rather than a hard gate.
- A retarded / hybrid field-law probe is now retained in
  [`frontier_two_field_retarded_probe.py`](../scripts/frontier_two_field_retarded_probe.py):
  the main coupled-force battery survives, but family robustness still drops to
  `2/3` on random geometric and layered-cycle families.
- The sparse layered DAG-like family remains a useful negative control; it
  still fails the gauge/current threshold.
- The main blocker is no longer transport portability. It is self-consistent
  endogenous refresh on top of the now-retained nonlocal source-to-field
  closure.
- Push beyond
  [`frontier_staggered_backreaction_prototype.py`](../scripts/frontier_staggered_backreaction_prototype.py)
  and
  [`frontier_staggered_backreaction_iterative.py`](../scripts/frontier_staggered_backreaction_iterative.py):
  the local screened-Poisson field is too weak, but the direct nonlocal
  `resistance_yukawa` Green map now closes the raw source-to-field scale on the
  retained graph set.
- Do not reopen small linear source preconditioner sweeps.
- Next seam: iterative endogenous closure on top of the retained nonlocal Green
  map, because the one-step self-refresh gap is still `O(1)` on the
  cycle-bearing families.
- After that, push beyond the current wave-law hardening toward a retarded or
  hybrid field law that actually closes family robustness, rather than
  multiplying more one-way background-field probes.
- Acceptance gate:
  preserve the retained `resistance_yukawa` closure level while reducing the
  one-step self-refresh gap, without losing TOWARD sign, source linearity,
  exact additivity, or norm stability.

## P1 - Native Gauge Holdout on Layered Graphs

- [`frontier_staggered_graph_gauge_closure.py`](../scripts/frontier_staggered_graph_gauge_closure.py)
  closes native gauge/current on the cycle-bearing stress families.
- The engineered layered cycle geometry now closes native gauge/current.
- The sparse layered DAG-like holdout still fails and should be kept as a
  negative control rather than a target for the same loop geometry.
- Next step: preserve the explicit layered-loop closure while pushing the
  source sector toward endogenous scale closure.
- Stay on the same graph-native staggered transport law. No 1D helpers or proxy
  substitutions.

## P2 - Shell / Spectral Diagnostics for the Source Sector

- Compare `phi_solved(depth)` against `phi_ext(depth)` directly on one
  cycle-bearing family and one layered family.
- Frozen in [`STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md`](../docs/STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md): the solved graph field is much flatter in depth than the external-kernel control, and its spectrum is more concentrated in the lowest modes on both families.
- Use that result to decide whether the next closure attempt should be:
  - a different Green's-function map
  - a genuinely nonlinear iterative source sector
  - or a graph-family-specific normalization rule

## P3 - Graph-Dirac Design

- Write down the graph invariants the staggered lane actually needs.
- Separate "bipartite", "layered", "cycle-bearing", and "DAG-compatible" as
  explicit architectural constraints.
- Identify which graph families are structurally incompatible before coding.

## P4 - Documentation Hygiene

- Keep the force-based staggered card separate from the repo-wide centroid card.
- Keep the portability probe separate from the canonical card.
- Preserve the full-suite baseline as `29/38` in 1D and `28/38` in 3D.
- Tighten the staggered card doc so the semantic differences table fully matches
  the force-based script and the tested family sets.

## Acceptance Criteria

- A portability result is promotable only if it stays honest across graph
  family changes, not just on one retained graph.
- Backreaction is promotable only if the force rows survive with an endogenous
  `Phi`.
- A design memo is promotable only if it lists the required graph invariants
  and failure modes concretely enough to guide implementation.
