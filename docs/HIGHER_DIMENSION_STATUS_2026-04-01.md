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

- **The stricter 4D unification pass is positive but still partial.**
  - [four_d_joint_strict.py](/Users/jonreilly/Projects/Physics/scripts/four_d_joint_strict.py)
  - [2026-04-01-four-d-joint-strict.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-joint-strict.txt)
  - The strongest current row is `gap=3, N=40`, where gravity, `pur_cl`, binned visibility, and the companion Born/chokepoint check all pass.
  - The safe wording is still partial coexistence overall, because the Born check is on a companion graph and the later rows do not all survive.

- **Born rule is clean in higher dimensions when the barrier is a true chokepoint.**
  - [four_d_born_rule_chokepoint.py](/Users/jonreilly/Projects/Physics/scripts/four_d_born_rule_chokepoint.py)
  - [2026-04-01-four-d-born-rule.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-born-rule.txt)
  - The same chokepoint logic also checks out in the verified 3D branch-side script.
  - A stricter same-family follow-up is now narrower but more internal:
    - [four_d_same_family_born.py](/Users/jonreilly/Projects/Physics/scripts/four_d_same_family_born.py)
    - [2026-04-01-four-d-same-family-born.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-same-family-born.txt)
  - Safe wording: the same-family chokepoint-pruned view reaches machine-precision
    Sorkin `I_3` only on a restricted low-`N` modular subfamily, while the raw
    modular family still fails and the pass does not survive broadly at large `N`.

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
  - Under the corrected control pool, the rerun narrows further: the positive region stays inside a very tight dense modular corner, and the stability-aware follow-up shows that this corner spans multiple nearby rows rather than a single isolated point.
  - Best current read: 5D is not dead, but its positive mass-law signal is a meaningful narrow dense-corner regime, not a broad stable window and not a one-row artifact.
  - A source-aware follow-up in that same dense neighborhood is negative:
    - [five_d_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/five_d_source_projected_pilot.py)
  - Safe wording: the narrow positive 5D corner is a Laplacian/modular mass-scaling story, not a broader source-aware rescue.

- **The first causal-field alternative is not yet a retained distance-law rescue.**
  - [causal_field_fixed_mass_verify.py](/Users/jonreilly/Projects/Physics/scripts/causal_field_fixed_mass_verify.py)
  - [2026-04-01-causal-field-fixed-mass-verify.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-causal-field-fixed-mass-verify.txt)
  - [causal_field_mass_scaling.py](/Users/jonreilly/Projects/Physics/scripts/causal_field_mass_scaling.py)
  - [2026-04-01-causal-field-mass-scaling.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-causal-field-mass-scaling.txt)
  - [causal_field_unification.py](/Users/jonreilly/Projects/Physics/scripts/causal_field_unification.py)
  - [2026-04-01-causal-field-unification.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-causal-field-unification.txt)
  - Once the impact-parameter sweep is rerun with fixed mass count and fixed source geometry, the earlier apparent causal-field falloff does not survive as a clean `1/b` law, and the same forward-only field weakens mass scaling relative to the retained Laplacian lane.
  - A bounded hybrid interpolation check also stays negative:
  - [hybrid_field_fixed_mass_pilot.py](/Users/jonreilly/Projects/Physics/scripts/hybrid_field_fixed_mass_pilot.py)
  - [2026-04-01-hybrid-field-fixed-mass-pilot.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-hybrid-field-fixed-mass-pilot.txt)
  - No tested hybrid mix beats the retained Laplacian endpoint on both distance trend
    and mass scaling at once; the interpolation only slides between the two endpoints.

- **Geometry-clean source templates are only available in a tiny corner.**
  - [source_template_availability_scan.py](/Users/jonreilly/Projects/Physics/scripts/source_template_availability_scan.py)
  - [2026-04-01-source-template-availability-scan.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-source-template-availability-scan.txt)
  - The retained and denser fixed-layer scans both have zero clean maps at the default template choice.
  - A later geometry search does find a narrow clean corner, and the best combo in both families is layer `6`, mass count `4`, but the clean acceptance rate is still sparse.
  - The geometry-clean pilot therefore keeps the source-aware seam narrow rather than opening a broad rescue lane.

- **Explicit fixed-template source-aware coupling is now a conditional rather than broad result.**
  - [fixed_template_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/fixed_template_source_projected_pilot.py)
  - [2026-04-01-fixed-template-source-projected-pilot.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-fixed-template-source-projected-pilot.txt)
  - On the retained 3D modular family, the explicit non-overlapping template bank still improves the distance exponent relative to the Laplacian baseline and strengthens the mass exponent.
  - On the denser 3D modular control family, the same template discipline flips back against the projected lane: the distance trend does not improve and the mass trend weakens.
  - Safe wording: **the source-projected seam is real but family-sensitive; it is not a retained rescue across both 3D control families.**
  - The newer detector-side purity ablation / rescue pair is also negative for the simplest mechanism story:
    - [detector_purity_ablation.py](/Users/jonreilly/Projects/Physics/scripts/detector_purity_ablation.py)
    - [detector_purity_rescue.py](/Users/jonreilly/Projects/Physics/scripts/detector_purity_rescue.py)
  - Lowering purity in the retained family does not collapse the seam, and nudging purity upward in the denser family does not restore a balanced rescue. So detector purity is currently best read as a correlate, not the main causal lever.

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
  - [2026-04-01-four-d-visibility-envelope.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-visibility-envelope.txt)
  - The older exact-`y` profile metric was too brittle. The newer fixed-bin / envelope-smoothed checks are better, and they now support a slightly stronger but still narrow claim: strict 4D visibility is **weak and intermittent**, not strongly retained across the family. The visibility caveat therefore survives even after the metric cleanup.

- **The original branch-local 3D joint script still uses an interference proxy, and the stricter reruns narrow the 3D joint claim further.**
  - [three_d_joint_visibility_strict.py](/Users/jonreilly/Projects/Physics/scripts/three_d_joint_visibility_strict.py)
  - [2026-04-01-three-d-joint-visibility-strict.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-three-d-joint-visibility-strict.txt)
  - On the retained 3D modular `gap=3` lane, the strict same-family visibility gain is effectively flat at large `N` (`V_gain ≈ +0.0049` for `N>=40`), so the stronger 3D “all four pass” language remains unsafe under strict controls.
  - The corrected chokepoint + fixed-mass rerun of [three_d_joint_test.py](/Users/jonreilly/Projects/Physics/scripts/three_d_joint_test.py) keeps decoherence but not a strong retained gravity clause, so the safe 3D statement is now: **3D decoherence clearly survives; the earlier broad four-way coexistence wording does not.**

- **The strict 4D pass is not literally same-graph on all four columns.**
  - Gravity, decoherence, and binned visibility run on the retained modular DAGs.
  - The Born-rule column comes from a companion chokepoint graph.
  - That makes the current 4D result a strong companion-control coexistence check, not a literal same-instance four-way proof.

- **The branch-local 3D continuum `b` test does not yet isolate impact parameter cleanly.**
  - Its distance sweep varies the mid-layer mass-node set with `b` instead of holding the source mass configuration fixed.
  - So the specific “continuum-limit `b`-independence is confirmed” wording should stay provisional until rerun with fixed mass count / geometry across `b`.
- **The current distance-law closure is much stronger than the earlier 4D sweep alone.**
  - [four_d_distance_scaling.py](/Users/jonreilly/Projects/Physics/scripts/four_d_distance_scaling.py)
  - [propagator_power_sweep.py](/Users/jonreilly/Projects/Physics/scripts/propagator_power_sweep.py)
  - [locality_shell_distance_law_fixed_mass.py](/Users/jonreilly/Projects/Physics/scripts/locality_shell_distance_law_fixed_mass.py)
  - [nonlinear_propagation_distance_law.py](/Users/jonreilly/Projects/Physics/scripts/nonlinear_propagation_distance_law.py)
  - [effective_metric_distance_law.py](/Users/jonreilly/Projects/Physics/scripts/effective_metric_distance_law.py)
  - [causal_field_fixed_mass_verify.py](/Users/jonreilly/Projects/Physics/scripts/causal_field_fixed_mass_verify.py)
  - [causal_field_unification.py](/Users/jonreilly/Projects/Physics/scripts/causal_field_unification.py)
  - Across those fixed-mass and rescue-variant tests, the same flat/topological distance law survives.
  - The only remaining live seam is source-aware coupling:
    - [source_resolved_green_pilot.py](/Users/jonreilly/Projects/Physics/scripts/source_resolved_green_pilot.py)
    - [source_projected_field_pilot.py](/Users/jonreilly/Projects/Physics/scripts/source_projected_field_pilot.py)
  - [source_projected_parameter_map.py](/Users/jonreilly/Projects/Physics/scripts/source_projected_parameter_map.py)
  - [2026-04-01-source-projected-parameter-map-rerun.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-source-projected-parameter-map-rerun.txt)
  - [fixed_source_geometry_sanity.py](/Users/jonreilly/Projects/Physics/scripts/fixed_source_geometry_sanity.py)
  - [2026-04-01-fixed-source-geometry-sanity-rerun.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-fixed-source-geometry-sanity-rerun.txt)
  - Current safe wording: **source-projected coupling is family-sensitive: the explicit non-overlapping template pilot improves the distance trend and mass scaling on the retained family, but it flips back against the denser control family, so it is not a retained rescue.**

- **The 4D source-aware seam is narrow and family-sensitive.**
  - [four_d_source_projected_pilot.py](/Users/jonreilly/Projects/Physics/scripts/four_d_source_projected_pilot.py)
  - [2026-04-01-four-d-source-projected-pilot.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-source-projected-pilot.txt)
  - On the retained 4D modular family, the source-projected lane flips to a positive `b` exponent and loses the mass trend.
  - [four_d_source_template_availability_scan.py](/Users/jonreilly/Projects/Physics/scripts/four_d_source_template_availability_scan.py)
  - [2026-04-01-four-d-source-template-availability-scan.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-four-d-source-template-availability-scan.txt)
  - The retained 4D family still has no clean template maps, but the denser 4D holdout does admit a clean corner at layer=5, `M=4`.
  - The corresponding clean-corner pilot on that denser family still does not produce a stable source-aware rescue: the projected lane has accepted maps, but its shifts stay mixed and the mass fit is not robust.
  - Safe wording: the explicit source-aware seam is not a broad 4D rescue, but it remains a narrow geometry-sensitive corner in the denser family.

## Current best claim

The current higher-dimensional story is:

- gravity survives in the higher-dimensional extensions in narrower form than the early branch story,
- mass-scaling strength increases with spatial dimension,
- modular 3D and especially modular 4D dramatically improve the decoherence story,
- Born-rule compliance survives with chokepoint barriers,
- but the distance law remains effectively topological/flat, the strict higher-dimensional visibility story still needs cleaner metrics, and the corrected 3D joint rerun now retains decoherence more clearly than gravity. The explicit non-overlapping source-template pilots now sharpen the last source-aware seam: the retained family improves, the denser family flips back, and the result is family-sensitive rather than a stable rescue.
- the dense 5D source-aware follow-up and the detector-purity ablation / rescue pair both keep that last seam narrow: the higher-dimensional transfer stays negative, and purity alone does not explain the surviving retained-family effect.

## Next frontiers

1. **Source-aware mechanism frontier**
   - explain why the retained 3D family improves while the denser 3D control, the retained 4D family, and the dense 5D corner all flip back or fail.

2. **Analytic / architectural distance-law frontier**
   - derive why the current linear path-sum force stays flat/topological, or test genuinely deeper alternatives such as metric emergence or stronger nonlinearity.

3. **4D continuum / density limit**
   - determine whether the 4D mass exponent converges toward `1`.

4. **5D dense robustness**
   - the corrected-control reruns now suggest a meaningful narrow dense-corner regime rather than a one-row artifact; the remaining question is whether that corner can widen into a more stable family.
