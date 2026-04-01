# Higher-Dimension Status

**Date:** 2026-04-01  
**Purpose:** compact, review-safe summary of the current 3D / 4D / 5D state.

## What is solid on `main`

- **3D modular decoherence is materially better than the 2D ceiling lane.**
  - [three_d_modular_asymptotic_decoherence.py](/Users/jonreilly/Projects/Physics/scripts/three_d_modular_asymptotic_decoherence.py)
  - [2026-04-01-three-d-modular-asymptotic-decoherence.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-three-d-modular-asymptotic-decoherence.txt)
  - The retained `gap=3` lane keeps `pur_cl` well below `1` through `N=100`.

- **4D modular decoherence is currently the strongest large-`N` non-unitary lane in the repo.**
  - [four_d_decoherence_large_n.py](/Users/jonreilly/Projects/Physics/scripts/four_d_decoherence_large_n.py)
  - [2026-04-01-four-d-decoherence-large-n.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-decoherence-large-n.txt)
  - Dense modular `gap=3` and `gap=5` both stay bounded away from `1` through `N=100`.

- **Born rule is clean in higher dimensions when the barrier is a true chokepoint.**
  - [four_d_born_rule_chokepoint.py](/Users/jonreilly/Projects/Physics/scripts/four_d_born_rule_chokepoint.py)
  - [2026-04-01-four-d-born-rule.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-born-rule.txt)
  - The same chokepoint logic also checks out in the verified 3D branch-side script.

- **4D distance scaling is still effectively flat/topological.**
  - [four_d_distance_scaling.py](/Users/jonreilly/Projects/Physics/scripts/four_d_distance_scaling.py)
  - [2026-04-01-four-d-distance-scaling.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-distance-scaling.txt)
  - The retained 4D modular lane does not show a convincing `1/b` falloff.

- **5D is currently connectivity-limited rather than decisively physics-limited.**
  - [five_d_connectivity_diagnostic.py](/Users/jonreilly/Projects/Physics/scripts/five_d_connectivity_diagnostic.py)
  - [2026-04-01-five-d-connectivity-diagnostic.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-five-d-connectivity-diagnostic.txt)
  - Densifying the graph improves validity, but the first broad bounded sweep still does not recover a robust positive exponent.
  - A later dense pilot does recover a narrow positive window:
    - [five_d_dense_pilot.py](/Users/jonreilly/Projects/Physics/scripts/five_d_dense_pilot.py)
    - [2026-04-01-five-d-dense-pilot.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-five-d-dense-pilot.txt)
  - A denser robustness map broadens that positive window around the pilot corner, but it still stays inside the dense modular neighborhood rather than becoming a stable generic regime:
    - [five_d_dense_robustness_map.py](/Users/jonreilly/Projects/Physics/scripts/five_d_dense_robustness_map.py)
    - [2026-04-01-five-d-dense-robustness-map.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-five-d-dense-robustness-map.txt)
  - Best current read: 5D is not dead, but its positive mass-law signal remains density-sensitive and tied to a dense modular corner of parameter space.

## Strong branch-local results that still need careful wording

- **Optimized 4D gravity can reach near-Newtonian mass scaling.**
  - In the shared Claude worktree, the verified 4D gravity harness reaches `alpha ≈ 1.07` on modular `gap=5`.
  - This is best read as: **`F ~ M` is achievable in the current 4D architecture under optimized graph parameters.**
  - It should not yet be promoted as a universal 4D law across families/settings.

- **3D density scaling suggests a convergent mass exponent near `0.58`.**
  - The shared branch-side continuum sweep points to a stable 3D mass-scaling exponent slightly above the naive `sqrt(M)` value.
  - That supports the broader claim that **mass-scaling strength increases with spatial dimension**.

## Metric cautions to keep explicit

- **4D true visibility is still not a settled positive.**
  - [four_d_true_visibility.py](/Users/jonreilly/Projects/Physics/scripts/four_d_true_visibility.py)
  - [2026-04-01-four-d-true-visibility.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-true-visibility.txt)
  - [four_d_true_visibility_binned.py](/Users/jonreilly/Projects/Physics/scripts/four_d_true_visibility_binned.py)
  - [2026-04-01-four-d-true-visibility-binned.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-true-visibility-binned.txt)
  - The older exact-`y` profile metric was too brittle. The newer fixed-bin / envelope-smoothed check is better, and it still says the retained 4D lane has mostly weak or near-zero strict visibility gain. So the visibility caveat survives even after the metric cleanup.

- **The branch-local 3D joint script still uses an interference proxy, not the strict visibility-gain metric.**
  - That means the strongest “all four pass” language is safe for the branch-local 3D joint run only if the interference clause is read as a proxy.

- **The branch-local 3D continuum `b` test does not yet isolate impact parameter cleanly.**
  - Its distance sweep varies the mid-layer mass-node set with `b` instead of holding the source mass configuration fixed.
  - So the specific “continuum-limit `b`-independence is confirmed” wording should stay provisional until rerun with fixed mass count / geometry across `b`.
- **The current distance-law closure is much stronger than the earlier 4D sweep alone.**
  - [four_d_distance_scaling.py](/Users/jonreilly/Projects/Physics/scripts/four_d_distance_scaling.py)
  - [propagator_power_sweep.py](/Users/jonreilly/Projects/Physics/scripts/propagator_power_sweep.py)
  - [locality_shell_distance_law_fixed_mass.py](/Users/jonreilly/Projects/Physics/scripts/locality_shell_distance_law_fixed_mass.py)
  - [nonlinear_propagation_distance_law.py](/Users/jonreilly/Projects/Physics/scripts/nonlinear_propagation_distance_law.py)
  - [effective_metric_distance_law.py](/Users/jonreilly/Projects/Physics/scripts/effective_metric_distance_law.py)
  - Across those fixed-mass and rescue-variant tests, the same flat/topological distance law survives. The remaining live question is no longer “which weight or shell fixes `1/b`?” but whether the flat force law can be derived analytically or only escaped by a deeper architecture change.

## Current best claim

The current higher-dimensional story is:

- gravity survives in the higher-dimensional extensions,
- mass-scaling strength increases with spatial dimension,
- modular 3D and especially modular 4D dramatically improve the decoherence story,
- Born-rule compliance survives with chokepoint barriers,
- but the distance law remains effectively topological/flat, and the strict higher-dimensional visibility story still needs cleaner metrics.

## Next frontiers

1. **Strict 4D same-graph unification pass**
   - run gravity, decoherence, binned true visibility, and Born checks on the same retained 4D graph instances.

2. **4D continuum / density limit**
   - determine whether the 4D mass exponent converges toward `1`.

3. **5D dense robustness map**
   - determine whether the positive dense 5D window widens beyond the pilot corner or stays density-sensitive inside the modular neighborhood.

4. **Analytic / architectural distance-law frontier**
   - derive why the current linear path-sum force stays flat/topological, or test genuinely deeper alternatives such as metric emergence or stronger nonlinearity.
