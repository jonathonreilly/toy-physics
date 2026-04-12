# Work Backlog

**Scope:** next steps for the retained staggered / graph-Dirac program.

This backlog is ordered by value to the main project, not by ease.

## P0 - Sign Selection / Direction Observable

- The two-sign comparison is now retained in
  [`frontier_two_sign_comparison.py`](../scripts/frontier_two_sign_comparison.py)
  and
  [`TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](../docs/TWO_SIGN_COMPARISON_NOTE_2026-04-10.md):
  on irregular graph families, the current shell-radial and edge-radial sign
  measures are not sign-selective. Both attractive and repulsive coupling can
  remain inward on those observables, even after the corrected parity
  coupling is applied.
- The exact cubic card now retains its directional result under the corrected
  parity coupling, so the remaining directional blocker is specifically the
  endogenous same-surface irregular probe.
- The next real fork is:
  - derive the attractive sign from the staggered / Dirac structure, or
  - freeze the irregular graph program as explicitly sign-agnostic
- A new exploratory weak-coupling regime now exists in
  [`WEAK_COUPLING_SIGN_SENSITIVITY_NOTE_2026-04-11.md`](../docs/WEAK_COUPLING_SIGN_SENSITIVITY_NOTE_2026-04-11.md):
  at `G=5,10`, width asymmetry and shell-force separation are much stronger
  than on the retained structural operating points. This is promising, but it
  is not yet a retained closure because the effect is `14/15`, not `15/15`,
  and repulsive shell-force counts are still mixed on some random-geometric
  seeds.
- Acceptance gate:
  either produce one graph-native irregular observable that distinguishes
  coupling sign, or rewrite the program around structural interacting-field
  results without directional gravity claims. Do not conflate this with the
  exact-cubic external-potential sign test.

## P1 - Endogenous Field Closure

- Frozen narrow positive:
  [`frontier_staggered_backreaction_green_closure.py`](../scripts/frontier_staggered_backreaction_green_closure.py)
  and
  [`STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md`](../docs/STAGGERED_BACKREACTION_GREEN_CLOSURE_NOTE.md)
  now give a graph-native direct Green map (`resistance_yukawa`) that cuts the
  retained cycle-bearing mean gap from `8.899e-01` to `9.889e-02` and the
  layered holdout gap from `8.759e-01` to `1.680e-02`, while preserving the
  retained force battery.
- Portability is established enough for the retained force battery:
  baseline portability, stress portability, and the failure map are frozen.
- Native gauge/current closure is retained on the cycle-bearing stress
  families, and explicit layered cycle geometry also closes the current probe.
- True self-gravity is now retained on the three cycle-bearing graph families
  in [`frontier_staggered_self_gravity.py`](../scripts/frontier_staggered_self_gravity.py).
- A retained scaling readout now exists in
  [`frontier_staggered_self_gravity_scaling.py`](../scripts/frontier_staggered_self_gravity_scaling.py):
  inward force is stable, but contraction is topology-sensitive.
- A retained larger-graph sibling now exists in
  [`frontier_staggered_cycle_battery_scaled.py`](../scripts/frontier_staggered_cycle_battery_scaled.py):
  the force-first battery stays closed on random geometric, growing, and
  layered cycle at side `8`, `10`, and `12`.
- A retained causal-DAG compatibility probe now exists in
  [`frontier_staggered_dag.py`](../scripts/frontier_staggered_dag.py): `6/6`
  on three layered DAG configurations.
- A first two-field endogenous coupling is now retained as a prototype in
  [`frontier_two_field_coupling.py`](../scripts/frontier_two_field_coupling.py),
  but it still uses relaxation dynamics for `Phi`.
- A wave-law two-field hardening is now retained in
  [`frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py): hard
  `5/5` on the retained cycle-bearing families, with width kept as a
  diagnostic rather than a hard gate. The corrected parity coupling leaves the
  hard score intact but changes the width diagnostic.
- A retarded / hybrid field-law probe is now retained in
  [`frontier_two_field_retarded_probe.py`](../scripts/frontier_two_field_retarded_probe.py):
  the main coupled-force battery survives, but family robustness still drops to
  `2/3` on random geometric and layered-cycle families.
- A sibling family-closure attempt now exists in
  [`frontier_two_field_retarded_family_closure.py`](../scripts/frontier_two_field_retarded_family_closure.py):
  it closes `9/9` on all three admissible cycle-bearing families and retains
  the causal DAG at `8/9` (`R8` gauge structurally N/A).
- The first larger-graph break frontier is now frozen in
  [`frontier_staggered_cycle_break_frontier.py`](../scripts/frontier_staggered_cycle_break_frontier.py):
  the earliest clean failure is a gauge/current collapse on the random
  geometric family under dense shortcuts, not a force-sign collapse.
- The matched frontier slice is now frozen in
  [`frontier_staggered_cycle_break_slice.py`](../scripts/frontier_staggered_cycle_break_slice.py):
  a quality-matched local control stays retained through `extra=6`, while the
  frontier branch fails native gauge at `extra=5/6`.
- The gravity-sign audit is now frozen in
  [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](../docs/GRAVITY_SIGN_AUDIT_2026-04-10.md):
  exact lattice force remains the standard on the canonical card, while the
  irregular-graph batteries are now explicitly treated as audited radial
  proxies that do not by themselves distinguish attractive from repulsive
  coupling. The failed same-surface probe is the current blocker.
- The sparse layered DAG-like family remains a useful negative control; it
  still fails the gauge/current threshold.
- The main blocker is now the endogenous same-surface directional observable
  on irregular graphs. The source-sector pieces are characterized, but the
  irregular graph batteries still need one frozen sign-selective observable
  before any directional claim off-lattice is defensible.
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
  cycle-bearing families. Also keep the parity-coupling rewrite frozen and do
  not reopen the old identity-coupling convention.
- After that, either justify the new retarded family-closure sibling as a real
  retained canonical harness or leave it explicitly as a tuned positive
  sibling. Do not blur that distinction.
- Acceptance gate:
  preserve the retained `resistance_yukawa` closure level while reducing the
  one-step self-refresh gap, while preserving source linearity, exact
  additivity, norm stability, and the current structural interaction battery.

## P2 - Native Gauge Holdout on Layered Graphs

- [`frontier_staggered_graph_gauge_closure.py`](../scripts/frontier_staggered_graph_gauge_closure.py)
  closes native gauge/current on the cycle-bearing stress families.
- The engineered layered cycle geometry now closes native gauge/current.
- The sparse layered DAG-like holdout still fails and should be kept as a
  negative control rather than a target for the same loop geometry.
- Next step: preserve the explicit layered-loop closure while pushing the
  source sector toward endogenous scale closure.
- Stay on the same graph-native staggered transport law. No 1D helpers or proxy
  substitutions.

## P3 - Shell / Spectral Diagnostics for the Source Sector

- Compare `phi_solved(depth)` against `phi_ext(depth)` directly on one
  cycle-bearing family and one layered family.
- Frozen in [`STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md`](../docs/STAGGERED_BACKREACTION_SHELL_SPECTRAL_NOTE.md): the solved graph field is much flatter in depth than the external-kernel control, and its spectrum is more concentrated in the lowest modes on both families. Treat this as source-sector characterization, not as an open blocker.
- Use that result to decide whether the next closure attempt should be:
  - a different Green's-function map
  - a genuinely nonlinear iterative source sector
  - or a graph-family-specific normalization rule

## P4 - Graph-Dirac Design

- Write down the graph invariants the staggered lane actually needs.
- Separate "bipartite", "layered", "cycle-bearing", and "DAG-compatible" as
  explicit architectural constraints.
- Identify which graph families are structurally incompatible before coding.

## P4.5 - Staggered Open-Cubic Two-Body Closure

- Freeze the late 2026-04-11 open-cubic staggered notes as follows:
  - bounded positives:
    - [STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md](../docs/STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
    - [STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md](../docs/STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md)
    - [STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md](../docs/STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md)
  - bounded negative / next-step memo:
    - [STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md](../docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md)
    - [STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md](../docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md)
- Current honest state:
  - the primary staggered architecture has a bounded open-cubic external-source
    trajectory `d^-2` law
  - it also has a bounded self-consistent two-body **force** channel
  - it does **not** have a retained blocked-centroid both-masses or
    trajectory-level two-body closure
- Do not reopen another blocked-centroid packet-split mass sweep.
- The observed failure mode is now explicit:
  - blocking is good enough for single-packet envelope drift
  - it is not good enough to decompose a pair-relative closing signal into two
    packet-level mutual forces
  - the `shared - self-only` trajectory residual is too small and too aliased
    by parity-scale density reshuffling inside the coarse windows
- Next observables to try, in order:
  - local momentum flux around each packet
  - mid-plane current between the packets
  - a relative-coordinate density observable built directly from the blocked
    density
- Acceptance gate:
  do not promote a staggered two-body lane until one of those observables gives
  same-row inward sign on both packets, stable partner-mass normalization, and
  materially better force-balance than the current blocked-centroid split.

## P5 - Documentation Hygiene

- Keep the force-based staggered card separate from the repo-wide centroid card.
- Keep the exact lattice-force card separate from the irregular-graph
  shell-radial proxy batteries, and do not describe the latter as exact
  coordinate-force expectations or as sign-selection evidence. Treat
  [`IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`](../docs/IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md)
  as the blocker note.
- Keep the portability probe separate from the canonical card.
- Preserve the full-suite baseline as `29/38` in 1D and `28/38` in 3D.
- Tighten the staggered card doc so the semantic differences table fully matches
  the force-based script and the tested family sets.

## Acceptance Criteria

- A portability result is promotable only if it stays honest across graph
  family changes, not just on one retained graph.
- Backreaction is promotable only if the force rows survive with an endogenous
  `Phi`, and any directional claim on irregular graphs must use a
  sign-selective observable rather than the current shell/edge proxies or the
  failed same-surface probe.
- A design memo is promotable only if it lists the required graph invariants
  and failure modes concretely enough to guide implementation.
