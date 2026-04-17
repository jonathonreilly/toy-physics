# Write-Up: Interference Regime of the Discrete Event-Network Toy Model

## Abstract

We present the first systematic characterization of interference in the discrete event-network toy model's two-slit setup. Six experiments swept grid geometry, slit placement, source position, and record probability across >25,000 path-sum evaluations. The central finding is that interference visibility is governed by a topological threshold: off-center fringe visibility is exactly zero when the causal DAG admits paths through only one slit, and jumps discontinuously to a finite value when paths through both slits first become available. The threshold ratio R_c(y) ≈ 0.25|y| + 1.0 is y-dependent and intrinsically discrete — it has no continuum analogue. Breaking the setup's reflection symmetry confirms that interference is a genuine dynamical property of the path-sum, not a symmetry artifact. Partial record formation produces exactly linear decoherence V(y,p) = V_0(1-p), confirming gradual suppression but with the trivial amplitude-splitting law.

## Background

The model's two-slit interference was previously demonstrated only as a binary comparison: records OFF (interference pattern) vs records ON (no interference). No parameter sweeps existed. The `two_slit_distribution()` function had hardcoded geometry (width=16, height=10, slits at y=±4). This work parameterized the setup and swept geometry, symmetry, and record probability.

## Method

| Experiment | Parameters | Evaluations | Script |
|------------|-----------|-------------|--------|
| Geometry sweep | 6 widths × 4 slit_seps × 24 phases × 2 record modes | 1,152 | `interference_geometry_sweep.py` |
| Off-center visibility | 5 widths × 4 slit_seps × 21 screen_ys × 24 phases × 2 modes | 20,160 | `interference_offcenter_fringe_sweep.py` |
| Critical ratio | 19 widths × 12 slit_halves × 4 test_ys × 24 phases | ~44,000 | `interference_critical_ratio_sweep.py` |
| Slit reachability | 10 test cases, per-slit amplitude decomposition | 10 | `interference_slit_reachability_audit.py` |
| Asymmetric | 5 configs × 21 screen_ys × 24 phases × 2 modes | ~5,040 | `interference_asymmetric_sweep.py` |
| Partial records | 21 p-values × 3 geometries × 21 screen_ys × 24 phases | ~31,752 | `interference_partial_record_sweep.py` |

All experiments use the model's standard path-sum over the causal DAG with `phase_per_action=4.0`, `attenuation_power=1.0`, no persistent nodes.

## Results

### 1. Visibility threshold is topological

Off-center fringe visibility V(y) is exactly zero when the causal DAG admits paths through only ONE slit to screen position y. The per-slit amplitude decomposition confirms this with zero exceptions (6/6 zero-V cases: single slit; 4/4 nonzero-V cases: both slits).

The mechanism is purely topological: on a rectangular grid of width w with slits at y=±s, paths from source (1,0) to detector (w,y) must traverse the barrier at x=w/2. If |y| is too large relative to the post-barrier grid, paths through the far slit cannot reach detector position y within the grid bounds.

### 2. Threshold ratio R_c(y) is y-dependent and discontinuous

The critical ratio R_c = width/(2×slit_half) below which V(y)=0:

| y | R_c (slit_half=4) |
|---|-------------------|
| 1 | 1.25 |
| 2 | 1.50 |
| 3 | 1.75 |
| 5 | 2.25 |

Approximately: R_c(y) ≈ 0.25|y| + 1.0

The transition is discontinuous: V jumps from exactly 0 to 0.004–0.875 (larger jumps for positions closer to center). No gradual onset.

### 3. Post-threshold growth is monotonic and saturating

Above the threshold, V(y) increases monotonically with grid width toward an asymptote. V(y=1) reaches 0.996 at width=40; V(y=5) reaches only 0.304. Wider grids enable more paths through both slits, increasing the amplitude balance and thus fringe contrast.

### 4. Mean visibility grows monotonically with width, decreases with slit separation

At every tested geometry point, mean screen visibility increases with width (more positions participate in interference) and decreases with slit separation (paths diverge more, reducing overlap). Both trends are exception-free.

### 5. Asymmetric setups confirm genuine dynamical interference

Breaking the reflection symmetry (asymmetric slits or off-center source) destroys the V(y=0)=1.0 artifact and produces asymmetric visibility profiles. V(y=0) drops from 1.0 to as low as 0.000 with strong asymmetry. Interference persists — it is not an artifact of the symmetric setup.

### 6. Record suppression is exact and universal

Record mode gives V=0.0000000000 at every screen position, every geometry, every symmetry configuration. No leakage at 10-digit precision. The record mechanism is absolute.

### 7. Partial records produce linear decoherence

V(y, p) = V(y, 0) × (1-p) exactly, at every position, every geometry tested. This is the trivial amplitude-splitting law: the coherent sector's amplitude is √(1-p) of total, giving (1-p) in the visibility ratio. No threshold behavior, no phase transition, no model-specific dynamics in the decoherence curve.

## Validation Summary

| Experiment | Sanity | Key concern | Resolution |
|------------|--------|-------------|------------|
| Geometry sweep | SUSPICIOUS | Center V=1 is symmetry artifact | Resolved by off-center + asymmetric experiments |
| Off-center visibility | CLEAN | Could be grid-regularity artifact | Valid concern for follow-up; monotonicity robust |
| Critical ratio | CLEAN | R_c fit from 4 points | Monotonicity robust; linear fit suggestive |
| Slit reachability | CLEAN | Only 10 cases | Mathematical argument covers all cases |
| Asymmetric | CLEAN | Phase-shift labeling arbitrary | Invariant under label swap |
| Partial records | CLEAN | Result is mathematically trivial | Correct; mechanism works but law is expected |

## Discussion

The interference regime reveals three distinctly discrete-network features:

1. **Topological visibility threshold** — paths either exist or don't on the discrete grid. No continuum analogue.
2. **Discontinuous onset** — V jumps from 0 to finite at the threshold. In continuum optics, visibility varies continuously with geometry.
3. **Y-dependent threshold** — R_c(y) increases with off-center distance, reflecting the grid's finite connectivity.

The record mechanism is clean: binary records give total suppression, partial records give exactly linear decoherence. The linear law V=V_0(1-p) is mathematically guaranteed by the amplitude-splitting rule and does not test the model's specific dynamics. Non-trivial decoherence would require records that modify the continuation landscape, not just sector labels.

## Next Steps

1. **Derive R_c(y) from axioms** — the threshold should follow from the rectangular grid's DAG structure. A first-principles derivation would confirm the approximate linear relationship.
2. **Test on irregular networks** — the monotonic trends may be specific to rectangular grids. Random or scale-free networks would test generality.
3. **Non-trivial record mechanisms** — records that distort the delay field or continuation weights could produce non-linear decoherence, testing the model's dynamics rather than just amplitude splitting.
4. **Three-slit setup** — would the topological threshold show richer structure with more slits?

## Status
COMPLETE — promoted to canonical main.
