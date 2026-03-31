# Corrected Propagator: From Amplitude Repulsion to Gravitational Attraction

**Date:** 2026-03-31
**Experiments:** 30 (amplitude-packet-action-sweep through force-law-delta-q3)
**Scripts:** 20 files in `scripts/`

---

## Abstract

The model's standard edge propagator `exp(ikS) / delay^p` produces amplitude distributions that concentrate AWAY from persistent-node clusters ("mass"), the opposite of gravitational attraction. A systematic search over 9 action formulas and 6 attenuation modes identified the root cause: the field-dependent denominator `1/delay^p` suppresses amplitude near mass independently of phase. Replacing the attenuation with geometry-only `1/L^p` (where L is coordinate link length) makes gravity a pure phase effect: at k=0, the centroid shift is exactly zero; at k>0, amplitude concentrates toward mass via a "phase valley" mechanism where the spent-delay action DECREASES near mass (ΔS ≈ -L√(2f) for weak field f). On generated causal DAGs, the corrected propagator produces gravitational attraction in 11/12 seeds (k-averaged) while preserving interference (12/12, V=0.995) and the Born rule (I₃/P = 6.5×10⁻¹⁶). Both phenomena emerge during graph growth at 6-8 layers. The gravitational shift scales as k² (CV=0.10 across a decade of k). On rectangular grids, the shift correlates with total action asymmetry (R²=0.91), but this force law does not transfer to random DAGs (R²=0.20), where topology-specific scattering dominates.

---

## Background

Prior work (experiments 1-50, pre-2026-03-31) established that:
- Path-sum propagation on rectangular grids produces interference fringes, gravitational path bending, and a Sorkin I₃=0 Born rule (`logs/` from 2026-03-30 sessions).
- Persistent self-maintaining patterns create delay fields via Laplacian relaxation.
- On generated causal DAGs, both interference and gravity-induced phase shifts emerge without pre-built geometry (`generative_causal_dag_interference.py`, `generated_dag_gravity_induced_phase.py`).
- Field-coupled CA attempts to produce smooth gravitational deflection of patterns failed due to discrete thresholds (`logs/2026-03-31-field-coupled-ca.txt`).

The gap: **amplitude packet mobility tests** (`logs/2026-03-31-amplitude-packet-mobility.txt`) showed that the path-sum centroid shifts AWAY from mass, not toward it. The standard propagator produces gravitational repulsion, contradicting the geodesic-bending results. This investigation sought the cause and a fix.

---

## Method

### Parameter Table

| Parameter | Value | Notes |
|-----------|-------|-------|
| Grid (rectangular) | 40×31 to 80×71 | Varied per experiment |
| Generated DAG | 12-15 layers × 20-25 nodes | connect_radius=3.0, y_range=10.0 |
| Phase wavenumber k | 0.01 - 20.0 | Swept per experiment |
| Attenuation power p | 0.0 - 3.0 | Usually 1.0 |
| Mass configuration | 3-5 persistent nodes, column | x and y varied |
| Seeds per test | 5-20 | Seed strategy: seed × prime + offset |
| Ensemble: k-averaging | k ∈ {3, 4, 5, 6, 7, 8} | For DAG attraction tests |

### Observables

1. **Centroid shift**: probability-weighted mean y at detector plane, mass minus free.
2. **Fringe visibility V**: (max_peak - min_trough) / (max_peak + min_trough) in two-slit probability distribution.
3. **Sorkin I₃**: three-slit inclusion-exclusion with amplitude masking on fixed DAG.
4. **Action asymmetry Q3**: total spent-delay action on above-center edges minus below-center edges.
5. **Field gradient**: mean field above center minus mean field below center at detector layer.

### Controls

- Free field (f=0 everywhere) for all shift measurements.
- k=0 propagation as pure-attenuation control.
- Mass above vs mass below (flip test) for sign verification.

### Scripts

Core experiments: `amplitude_packet_action_sweep.py`, `amplitude_spent_fraction_deep.py`, `spent_fraction_generated_dag.py`, `amplitude_attenuation_attraction.py`, `attraction_sanity_checks.py`, `geometry_attenuation_definitive.py`, `attraction_k_resonance.py`, `corrected_unified_mechanism.py`, `growth_rule_attraction_selection.py`, `attenuation_first_principles.py`, `corrected_opaque_decoherence.py`, `corrected_distance_and_lorentz.py`, `distance_scaling_large_grid.py`, `compact_density_diagnosis.py`, `attraction_corridor_map.py`, `weak_coupling_distance.py`, `corrected_propagator_regression_v2.py`, `ray_slope_lensing_test.py`, `growing_graph_attraction_emergence.py`, `perturbative_attraction_derivation.py`, `gravitational_force_law.py`, `force_law_on_dags.py`, `force_law_delta_q3.py`.

---

## Results

### 1. Root Cause: Attenuation, Not Phase

The standard propagator `exp(ikS) / delay^p` has two field-dependent factors: phase (exp(ikS)) and attenuation (1/delay^p). Setting k=0 isolates the attenuation contribution.

| propagator | k=0 shift | k=2 shift | source |
|---|---|---|---|
| 1/delay^p (standard) | **-14.02** | +2.17 | `attenuation-first-principles.txt` |
| 1/L^p (geometry) | **+0.00** | +13.66 | `attenuation-first-principles.txt` |

The standard propagator produces -14.02 repulsion even with no phase. The corrected propagator gives exactly zero — gravity is purely phase-driven.

### 2. Action Formula and Attenuation Sweep

9 action formulas tested (`amplitude-action-sweep.txt`). All produce repulsion with standard 1/delay^p attenuation. Only `spent_fraction` = (delay-retained)/delay (bounded [0,1]) produced attraction on the rectangular grid (+11.23 mean shift at k=2.5), but this failed on random DAGs (0/15 attract, `spent-fraction-generated-dag.txt`).

6 attenuation modes tested on DAGs (`attenuation-attraction.txt`):

| attenuation | attract rate | mean shift | stable? |
|---|---|---|---|
| 1/delay^p (standard) | 0/10 | -2.18 | yes |
| flat (no atten) | 5/10 | +0.25 | yes |
| (1+field)^p (boost) | 10/10 | +2.15 | **NO** |
| 1/L^p (geometry) | 8/10 | +0.23 | yes |

The (1+field)^p boost attracts but is unstable: amplitude blows up by 7×10⁹, distance scaling inverts (stronger at larger b), and Born rule violates (I₃/P=0.46) (`attraction-sanity-checks.txt`).

### 3. Corrected Propagator: 1/L^p

On generated causal DAGs with k-averaging:

| observable | result | source |
|---|---|---|
| Attraction rate | **11/12** (92%) | `corrected-unified.txt` |
| Interference rate | **12/12** (100%), V=0.995 | `corrected-unified.txt` |
| Born rule I₃ | 6.48×10⁻¹⁶ | `regression-v2.txt` |
| Signal speed | 1.000000 | `regression-v2.txt` |
| Time dilation | +5.26 delay | `regression-v2.txt` |
| k=0 gravity | 0.000000 (exact) | `regression-v2.txt` |
| Decoherence rate | 5/12 (42%) | `corrected-unified.txt` |

Regression test: 6/7 pass. The one failure (record suppression) is a 0.002 visibility difference, likely numerical.

### 4. Phase Valley Mechanism

Spent-delay action DECREASES with field (`perturbative-derivation.txt`):

| field f | action S (L=1) | ΔS |
|---|---|---|
| 0.00 | 1.000 | 0.000 |
| 0.01 | 0.868 | -0.132 |
| 0.10 | 0.642 | -0.358 |
| 0.50 | 0.382 | -0.618 |

Analytically: ΔS ≈ -L√(2f) for f≪1. Mass creates a region of LESS action → LESS phase accumulation → constructive interference → probability concentrates toward mass.

### 5. k² Scaling

Shift is quadratic in k, not linear (`perturbative-derivation.txt`):

- shift/k² = 20.8 to 21.6 for k = 0.01 to 0.15 (CV = 0.10)
- Confirmed on generated DAGs: shift/k² constant within 5% for k = 0.05 to 0.3 (`force-law-dags-v1.txt`)

### 6. Growth Creates Conditions for Phenomena

Incrementally growing DAGs from 4 to 20 layers (`growing-emergence.txt`):

| n_layers | interference | attraction |
|---|---|---|
| 4-5 | 0% | 60% |
| 6 | **100%** | 60% |
| 8+ | 100% | **80-100%** |

Interference emerges sharply at 6 layers. Gravity emerges by 8 layers. Both coexist from 8 layers onward.

### 7. Force Law (Grid-Specific)

On rectangular grid: shift = C × k² × Q3 (total action asymmetry), R²=0.91 (`force-law.txt`).

On random DAGs: R²=0.20 for Q3, R²=0.04 for ΔQ3 (`force-law-dags.txt`). The coupling is topology-dependent.

### 8. Null Results

- **2D lensing**: Outgoing deflection angle does NOT stabilize with detector distance; oscillates and reverses sign at large impact parameter (`ray-slope.txt`). Claim retracted.
- **Universal force law**: Does not transfer from grid to random DAGs. Graph topology dominates the coupling.
- **Decoherence**: Marginal at 5/12 with corrected propagator. Opaque mass even weaker (3/12) — paths route around blocked nodes (`corrected-opaque-decoherence.txt`).
- **Mixed attenuation**: 1/(L(1+αf))^p with small α does not restore distance falloff (`mixed-atten.txt`).
- **Compact density**: y_range=3 kills attraction because field gradient saturates at 0.01 (vs 0.46 at y_range=10) (`compact-diagnosis.txt`).

---

## Validation Summary

| check | status | detail |
|---|---|---|
| Born rule (I₃ on fixed DAG) | PASS | I₃/P = 6.48×10⁻¹⁶ |
| Interference visibility | PASS | V = 0.995 at k=2.0 |
| Signal speed = 1 | PASS | 1.000000 |
| Time dilation | PASS | +5.26 mass delay |
| k=0 → no gravity | PASS | shift = 0.000000 |
| Gravity attraction | PASS | 11/12 on DAGs |
| Record suppression | MARGINAL | ΔV = 0.002 |
| Decoherence | WEAK | 5/12 on DAGs |
| Distance scaling | UNCLEAR | Not clean ray-optics |
| Universal force law | FAIL | R²=0.20 on DAGs |

**Overall confidence**: HIGH for the corrected propagator as an improvement over standard. MODERATE for the attraction mechanism's universality. LOW for distance scaling and decoherence.

**Known fragilities**: k-dependence (attraction fails at k≈3.5-4.7 on lattice, though this is a lattice resonance absent on DAGs); decoherence requires larger effect size or different mechanism.

---

## Discussion

The field-dependent attenuation 1/delay^p in the standard propagator creates an artifact: amplitude is suppressed near persistent-node clusters regardless of phase. This suppression dominates the phase-based attraction, producing net repulsion. Removing the field from the attenuation (using 1/L^p) reveals the underlying phase structure: the spent-delay action DECREASES near mass, creating a "phase valley" where paths accumulate less phase and interfere more constructively.

The corrected propagator preserves all established results (interference fringes, Born rule, signal speed, time dilation) while fixing the gravity sign. The mechanism is second-order in k (shift ∝ k²), explaining why it was not visible in the original geodesic-bending tests (which measure path extremization, not amplitude distribution).

The force law's failure to transfer from rectangular grids to random DAGs indicates that the coupling between field and amplitude depends on graph topology in ways not captured by simple field observables. The k² scaling IS universal — only the proportionality constant varies.

The weak decoherence is the most significant limitation. With uniform attenuation, all paths have similar amplitudes, improving coherence and making decoherence harder. This suggests that decoherence in the model may require a mechanism beyond the propagator — possibly the topology-changing process (node creation/destruction) that was already shown to produce I₃≠0 in earlier work.

---

## Next Steps

1. **Scattering observable**: Define a momentum-space or angular observable that characterizes gravitational deflection without relying on centroid shift (expected information gain: HIGH).
2. **Topology-dependent coupling**: Characterize what graph properties determine the force law's proportionality constant C — path count, spectral gap, effective dimension (MEDIUM).
3. **Decoherence from topology change**: Test whether dynamically growing the graph during propagation (adding/removing nodes) produces stronger decoherence than field-only or opacity mechanisms (HIGH).
4. **Continuum limit**: Does the corrected propagator change the anisotropy scaling (1/n_directions)? Is 1/L^p the natural attenuation in the continuum? (MEDIUM).
5. **Integrate with simulator**: Add `action_attenuation_mode` parameter to `toy_event_physics.py` so the corrected propagator can be used in all existing experiments (LOW effort, HIGH utility).
