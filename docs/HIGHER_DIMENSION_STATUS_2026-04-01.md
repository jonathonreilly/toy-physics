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
  - Densifying the graph improves validity, but the current bounded sweep still does not recover a robust positive exponent.

## Strong branch-local results that still need careful wording

- **Optimized 4D gravity can reach near-Newtonian mass scaling.**
  - In the shared Claude worktree, the verified 4D gravity harness reaches `alpha ≈ 1.07` on modular `gap=5`.
  - This is best read as: **`F ~ M` is achievable in the current 4D architecture under optimized graph parameters.**
  - It should not yet be promoted as a universal 4D law across families/settings.

- **3D density scaling suggests a convergent mass exponent near `0.58`.**
  - The shared branch-side continuum sweep points to a stable 3D mass-scaling exponent slightly above the naive `sqrt(M)` value.
  - That supports the broader claim that **mass-scaling strength increases with spatial dimension**.

## Metric cautions to keep explicit

- **4D true visibility is not yet a settled positive.**
  - [four_d_true_visibility.py](/Users/jonreilly/Projects/Physics/scripts/four_d_true_visibility.py)
  - [2026-04-01-four-d-true-visibility.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-true-visibility.txt)
  - The current script reports `V_gain ~ 0`, but the detector profile is built by grouping on exact floating-point `y` values, so the metric itself should be treated as provisional until detector binning/envelope handling is improved.

- **The branch-local 3D joint script still uses an interference proxy, not the strict visibility-gain metric.**
  - That means the strongest “all four pass” language is safe for the branch-local 3D joint run only if the interference clause is read as a proxy.

- **The branch-local 3D continuum `b` test does not yet isolate impact parameter cleanly.**
  - Its distance sweep varies the mid-layer mass-node set with `b` instead of holding the source mass configuration fixed.
  - So the specific “continuum-limit `b`-independence is confirmed” wording should stay provisional until rerun with fixed mass count / geometry across `b`.

## Current best claim

The current higher-dimensional story is:

- gravity survives in the higher-dimensional extensions,
- mass-scaling strength increases with spatial dimension,
- modular 3D and especially modular 4D dramatically improve the decoherence story,
- Born-rule compliance survives with chokepoint barriers,
- but the distance law remains effectively topological/flat, and the strict higher-dimensional visibility story still needs cleaner metrics.

## Next frontiers

1. **Locality-constrained graph architecture**
   - test whether explicit spatial-locality shells or locality-preserving graph families can produce a real distance falloff.

2. **Strict 4D visibility metric**
   - replace the current exact-`y` detector-profile handling with a binned/envelope-aware visibility computation.

3. **4D continuum / density limit**
   - determine whether the 4D mass exponent converges toward `1`.

4. **5D density rescue**
   - determine whether a denser 5D regime yields a stable positive exponent or whether a new limitation appears.
