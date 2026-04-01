# Claim Audit Note

**Date:** 2026-04-01  
**Purpose:** compact claim ledger for syncing future README / docs updates after the topology, decoherence, and gravity fixes.

## Safe current claims

1. The corrected propagator still supports positive gravity-like deflection on the retained modular graph family.
2. The IF / CL reduced-description route still supports decoherence on the retained modular family.
3. The modular family is the current gravity + decoherence lane, but the strict 3D joint wording is now narrower after the corrected reruns.
4. The emergence story is still open: local feedback and soft-pruning rules do not generate a stable hard-gap topology asymptotically, even though adaptive quantile pruning now gives a bounded 3D improvement through `N=60`.
5. The higher-dimensional lane is now real, but its metric discipline still matters: dense modular 4D strongly improves large-`N` decoherence and higher-dimensional chokepoint Born-rule tests are clean, while strict visibility and universal mass-law wording still need tighter handling.

## Metric caveats to keep explicit

### `gap=0` baseline

- In the modular generator, `gap=0` now behaves as the true uniform-style baseline.
- Do not describe `gap=0` as a channelized modular special case.
- Broad-window claims should be phrased as properties of the modular sweep itself, not as a continuous “uniform to modular” dial.

### `pur_cl` vs `pur_min`

- `pur_cl` is the actual traced CL-bath detector purity.
- `pur_min` is the fully decohered lower-bound / floor metric.
- Phase-diagram pass/fail should be read using the metric the script actually tests.
- Do not swap `pur_min` and `pur_cl` in prose.

### Paired gravity SE

- Gravity significance should be reported from paired per-seed deltas, not from pooled `(seed, k)` samples.
- The old error bars were too optimistic when `k` samples were treated as independent.
- Use the paired-SE wording unless the script explicitly changes again.

### Large-N visibility

- The current large-`N` script now does compute a true single-vs-double-slit visibility gain.
- The old both-slits-open detector-profile contrast still stays high.
- The true visibility gain is only `+0.023` at `N=12`, drops to `+0.002` at `N=18`, and is near zero or negative by `N>=25`.
- So do not describe the asymptotic modular bath lane as preserving strong interference gain.

### Higher-dimensional visibility

- The older exact-`y` 4D visibility script reported `V_gain ~ 0` on the retained modular lane.
- The newer fixed-bin / envelope-smoothed 4D visibility script is a better check, and it still says the retained 4D lane has mostly weak or near-zero strict visibility gain.
- Do not yet describe 4D as having a strong strict visibility gain under the true metric.

### Higher-dimensional distance law

- The current 4D distance sweep is effectively flat/topological, not `1/b`.
- Fixed-mass locality-shell sweeps, propagator-power sweeps, a minimal local saturation nonlinearity, and an induced/effective-distance readout also fail to recover a clean `1/b` law.
- A first causal-field alternative also fails the stricter control: once the impact-parameter sweep is rerun with fixed mass count and fixed source geometry, the earlier apparent falloff does not survive as a retained `1/b` law, and the same forward-only field weakens mass scaling relative to the retained Laplacian lane.
- A source-aware follow-up now defines the only live seam:
  - source-resolved Green coupling improves the distance trend only weakly and loses a stable mass-law fit under corrected controls
  - source-projected coupling is still the strongest partial mover, but it remains only a partial move
  - the stricter geometry-clean control now finds a tiny clean corner only in a narrow dense family, and the explicit fixed-template pilots show that the effect is family-sensitive rather than broad
- The template-availability scan now sharpens that picture: the retained and denser fixed-layer scans admit no clean fixed-count source templates at the default construction, while a later geometry search finds only a tiny clean corner at very small layer/count combinations.
- The explicit fixed-template 3D pilot now splits the result by family: the retained family improves under source-projected coupling, but the denser control family flips back and the Green lane stays weak.
- The new 4D transfer pilot is a negative follow-up: the source-projected lane flips to a positive distance exponent and loses the mass trend on the retained 4D modular family.
- The new 4D geometry-template availability scan reopens only a narrow seam: the retained 4D family still has no clean maps, but the denser 4D holdout does admit a clean corner at layer=5, `M=4`.
- The follow-on 4D clean-corner pilot keeps that seam narrow: the denser family admits clean maps, but the source-projected lane still does not produce a stable mass trend there.
- The shell-contribution audit shows that broad shells are present in the retained 3D family, but the source-resolved Green lane improves the distance trend more than the shell picture alone; shell support is therefore not the full mechanism.
- The newer detector-purity ablation / rescue pair is narrowly negative for the simplest causal story:
  - late detector-side mixing lowers purity in the retained 3D family without collapsing the source-projected seam
  - late detector-side purification in the denser 3D family nudges purity only slightly and does not restore a balanced rescue
  - so detector purity currently looks more like a correlate than the main causal lever.
- A branch-side 3D density sweep points the same way, but that specific continuum-distance script still needs a stricter fixed-mass comparison before the strongest “confirmed continuum `b`-independence” wording is safe.
- So the safe current claim is: **distance-law failure remains a structural architecture issue, not something repaired by the current higher-dimensional, shell-based, or minimal nonlinear rescue sweeps.**

### 4D strict unification wording

- The new 4D strict pass is useful and positive, but it is narrower than its filename suggests.
- Gravity, `pur_cl`, and binned visibility are measured on the retained modular DAGs, while the Born-rule column comes from a companion chokepoint graph.
- So the safe wording is: **one retained 4D companion-control coexistence row exists, but the broader strict 4D story is still partial.**

### Node-removal asymptotics

- Node removal helps at intermediate `N`.
- In 3D, fixed-threshold self-regulation helps through `N=50`, and adaptive-quantile pruning extends the useful window through `N=60` with all seeds still valid.
- By `N = 80`, the deletion-only rules still fail: the ceiling returns or the valid-seed fraction collapses.
- Adaptive/aggressive pruning still pushes the graph toward disconnection if the rule is not scaled carefully.
- Treat these as bounded partial positives for Gate B, not a solved local emergence law.

## Recommended wording discipline

- Use “retained modular family” for the joint gravity + decoherence result.
- Use “actual traced purity `pur_cl`” only where the script measures it.
- Use “decoherence floor `pur_min`” only where the lower-bound metric is intended.
- Distinguish clearly between the old detector-profile contrast proxy and the new true visibility gain.
- Use “intermediate-`N` pruning surrogate” for node removal.
- Keep the 3D/4D dimensional-scaling language framed as: **mass-scaling strength increases with spatial dimension**, while the exact `alpha(d)` law and the strict continuum limit remain open.
- Keep 4D visibility language narrower than 4D decoherence/Born-rule language until the detector-profile metric is improved.
- Keep 3D joint language narrower than the old branch summary: **3D decoherence survives clearly; the stronger four-way coexistence claim does not survive the corrected chokepoint + fixed-mass rerun.**
- Keep 5D language narrow: **a meaningful dense-corner regime remains positive, but it is still not a broad stable window.**
- Keep Gate B language narrow: **adaptive quantile pruning is the best bounded dynamics result so far, but it is not yet an asymptotic hard-gap generation law.**

## One-line summary

The code now supports a stronger modular-family higher-dimensional story, but the repo should keep its metric language precise: `gap=0` is the true baseline, `pur_cl` and `pur_min` are distinct, gravity SE is paired, 2D large-`N` visibility gain is weak/gone on the retained modular bath lane, dense modular 4D strongly improves decoherence, chokepoint Born-rule checks are clean, Gate B now has a bounded adaptive-quantile positive through `N=60` but not an asymptotic law, the 4D strict visibility metric remains weak even after binning cleanup, the corrected 3D joint rerun keeps decoherence more clearly than gravity, the 5D signal is a meaningful narrow dense-corner effect rather than a one-row artifact, and the distance law stays flat/topological across the current rescue variants with source-projected coupling remaining only a family-sensitive partial mover.
