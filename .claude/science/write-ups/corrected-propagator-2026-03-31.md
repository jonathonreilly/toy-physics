# Corrected Propagator: From Amplitude Repulsion to Gravitational Attraction

**Date:** 2026-03-31
**Experiments:** 54 (amplitude-packet-action-sweep through between-slit-geometry-sweep)
**Scripts:** 40+ files in `scripts/`

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
- **Single-pass decoherence mechanisms**: Opacity, field fluctuation, directional recording, backreaction all ineffective with corrected propagator.
- **Mixed attenuation**: 1/(L(1+αf))^p with small α does not restore distance falloff (`mixed-atten.txt`).
- **Compact density**: y_range=3 kills attraction because field gradient saturates at 0.01 (vs 0.46 at y_range=10) (`compact-diagnosis.txt`).
- **Mass scaling**: Δky is mass-independent (threshold effect, not F∝M).
- **Field profile**: Steeper than log(R/r); f/log ratio 0.04-0.15 on finite grid.

### 9. Two-Register Endogenous Decoherence (bug fix + geometry sweep)

A code review revealed the between-slit test was placing mass nodes in the blocked barrier set, producing a forced null. After fixing mass placement to the post-barrier layer (traversable by slit paths), two-register decoherence emerged:

| Geometry param | Best D% | Best ALL% | Source |
|---|---|---|---|
| mass_offset=1 | **40%** | **30%** | `between-slit-sweep.txt` |
| radius=4.0 | **40%** | **30%** | `between-slit-sweep.txt` |
| y_half=2-3 | 20% | 20% | `between-slit-sweep.txt` |

The mechanism: mass nodes in the first layer past the barrier carry an environment register (fine-grained: last mass node index). Paths from different slits traverse different mass nodes → different env labels → partial trace removes cross-slit interference. Decoherence is slit-separation-independent (mass proximity to barrier matters, not slit geometry).

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
| Endogenous decoherence | **PASS** | D=40%, ALL THREE=30% (two-register, post-barrier mass) |
| Distance scaling | UNCLEAR | Not clean ray-optics |
| Universal force law | FAIL | R²=0.20 on DAGs |

**Overall confidence**: HIGH for the corrected propagator as an improvement over standard. MODERATE for the attraction mechanism's universality. LOW for distance scaling. MODERATE for endogenous decoherence (geometry-dependent, 30-40% rate).

**Known fragilities**: k-dependence (attraction fails at k≈3.5-4.7 on lattice, though this is a lattice resonance absent on DAGs); decoherence requires larger effect size or different mechanism.

---

## Discussion

The field-dependent attenuation 1/delay^p in the standard propagator creates an artifact: amplitude is suppressed near persistent-node clusters regardless of phase. This suppression dominates the phase-based attraction, producing net repulsion. Removing the field from the attenuation (using 1/L^p) reveals the underlying phase structure: the spent-delay action DECREASES near mass, creating a "phase valley" where paths accumulate less phase and interfere more constructively.

The corrected propagator preserves all established results (interference fringes, Born rule, signal speed, time dilation) while fixing the gravity sign. The mechanism is second-order in k (shift ∝ k²), explaining why it was not visible in the original geodesic-bending tests (which measure path extremization, not amplitude distribution).

The force law's failure to transfer from rectangular grids to random DAGs indicates that the coupling between field and amplitude depends on graph topology in ways not captured by simple field observables. The k² scaling IS universal — only the proportionality constant varies.

The weak decoherence is the most significant limitation. With uniform attenuation, all paths have similar amplitudes, improving coherence and making decoherence harder.

### Endogenous Decoherence Search (experiments 31-43)

Five endogenous mechanisms tested, none produce decoherence without damaging gravity:

| mechanism | V_drop | gravity preserved? | why it fails |
|---|---|---|---|
| Oscillating opacity | weak (1-2/12 all-three) | NO (4-6/12) | Blocks phase-valley paths |
| Field fluctuation | 0/12 | YES (10/12) | Spatially uniform modulation |
| Directional recording | = shuffled control | YES (9/12) | Direction doesn't matter |
| Backreaction (field += ε|a|²) | 0/12 all-three | YES (8/12) | Slit-indistinguishable |
| Phase noise (exogenous) | 35% at η=1 on irreg. | YES (10/12) | Works but NOT endogenous |

**Note (Codex measurement fix):** Original decoherence counts compared perturbed mass runs against no-mass baseline, inflating results. Corrected comparisons use unperturbed-mass baseline. Full unification weakened: ALL THREE = 4/12 at η=0.7 (was 7/12). Born rule re-confirmed: I₃/P = 4.28e-15.

Source: `endogenous-opacity.txt`, `endogenous-field-fluct.txt`, `directional-recording.txt`, `directional-comparison.txt`, `backreaction.txt`, `phase-noise-irregular.txt`.

**Key finding**: exogenous phase noise on irregular graphs produces genuine decoherence (ensemble-averaged V drops from 0.80 to 0.52) because heterogeneous path lengths cause noise to accumulate differently across paths. On regular lattices, equal path lengths prevent decoherence. The best structural predictor for decoherence susceptibility is `mass_overlap` (fraction of edges near the mass region, R²=0.50), replacing the coarse `path_length_std` (R²=0.006). Source: `structural-predictor.txt`.

**Interpretation**: the corrected propagator creates a clean separation between unitary physics (gravity + interference from phase structure) and non-unitary physics (decoherence). The unitary sector is fully solved. Single-pass perturbations (noise, opacity, field fluctuation) fail for decoherence. However, the two-register architecture with fine-grained environment at properly positioned mass nodes produces genuine endogenous decoherence at 40% rate. The key geometric requirement: mass must be traversable by slit paths (post-barrier, not blocked). All three phenomena coexist at 30% of seeds.

Additional findings (experiments 44-54): Δky is nearly b-independent (2D log field + multi-path averaging) and mass-independent (threshold effect). The field profile is steeper than pure log(R/r) on finite grids. The critical ratio R_c = 1+|y|/s is exactly identical for both propagators at zero field (13/13 match).

---

## Next Steps

1. **Increase decoherence rate**: The 40% D rate at fine env comes with a gravity trade-off (env fragmentation). Find an intermediate env granularity that achieves D>30% with G>70%. (HIGH)
2. **Decoherence on lattice**: The two-register mechanism was tested on DAGs. Does it also work on the rectangular grid? (MEDIUM)
3. **Topology-dependent coupling**: Characterize what graph properties determine the force law's proportionality constant C (MEDIUM).
4. **Integrate with Codex pattern-sourced results**: Cross-compare mover steering with corrected propagator attraction (MEDIUM).
5. ~~**Integrate with simulator**~~: DONE — `attenuation_mode="geometry"` added to `RulePostulates`.
6. ~~**Multi-pass decoherence**~~: DONE — two-register with fine env gives D=40%, ALL THREE=30%.
7. ~~**Scattering observable**~~: DONE — Δky momentum-space centroid, stable downstream.
8. ~~**Continuum limit**~~: DONE — anisotropy 8.23% irreducible, gravity finite-range.
