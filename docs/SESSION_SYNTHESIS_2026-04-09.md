# Session Synthesis — 2026-04-09

## What happened

A single session attacked all 20 proposed moonshot frontiers, went through
10+ review rounds, and ended by discovering that the model's "gravity"
mechanism was not gravity — leading to a fundamental modification (the
Lorentzian split-delay action) that produces genuine geometric gravity.

~70 scripts delivered. ~15 PRs merged. Every claim was narrowed by review
at least once.

## The three discoveries (in order of importance)

### 1. The original model's gravity is a dispersive wave force, not geometry

The geodesic test (frontier_geodesic_gravity_test.py) showed that shortest
paths on the delay landscape bend AWAY from mass, not toward it. The delay
formula delay = L×(1+f) makes all delays longer near mass, so geodesics
avoid the slow region. The TOWARD deflection at k=5 is a wave-interference
resonance that OVERRIDES the repulsive geometric baseline.

Evidence:
- 2D geodesics: mass-side delayed +4.31 vs far-side +1.91 (AWAY)
- 3D geodesics: mass-side delayed +0.000471 vs far-side +0.000122 (AWAY)
- k-sweep: gravity oscillates TOWARD/AWAY with period ~π in k
- Spectral averaging: universally AWAY on the retained lattice
- First-principles derivation: Axiom 8 predicts AWAY from the delay landscape

### 2. The Lorentzian split-delay action fixes this

Replacing the uniform delay with a causal/spatial split:

  S = L × (1 - f × cos(2θ))

where θ is the edge angle from the causal direction, gives:
- θ=0 (causal): S = L(1-f) — action decreases near mass (time dilation)
- θ=π/2 (spatial): S = L(1+f) — action increases near mass (spatial stretch)

This matches the Schwarzschild metric structure (g₀₀ shrinks, g_rr grows)
and makes geodesics bend TOWARD mass.

The Lorentzian model at k=7 passes all core tests:
- Born: 1.50e-15 (machine precision)
- Gravity: +0.001079 TOWARD (2.5× stronger than Euclidean k=5)
- F∝M: 1.00 (R²=1.0000)
- Distance: 5/6 TOWARD, b^(-1.23) (R²=0.96)
- Decoherence: 31.1%

### 3. F∝M = 1.00 is structural to the action, not to gravity

The linearity of deflection with field strength holds at ALL k values
(1.0 through 10.0), in both TOWARD and AWAY windows, with R²=1.0000
everywhere. This comes from the valley-linear action's linearity in f,
not from a gravitational mechanism. It survives any reinterpretation.

## What survived all reviews (no asterisks)

### Structural (mechanism-independent)
- Born rule: kernel-independent, machine precision on static and grown DAGs
- Gauge connections: U(1), AB modulation (cos²(φ/2), depth=1.0)
- F∝M = 1.00: structural to valley-linear action, all k values
- Dynamic growth: self-regulating, Born at 4.3e-17 (2D) and 8.3e-17 (3D)
- Causal set: valid poset, metric from chains at r=0.997
- Parity charge: Z₂ conserved quantum number

### Euclidean model (S = L(1-f)) — now understood as dispersive
- Attractive window k=1.5-6.0 on 3D lattice (phase diagram mapped)
- Repulsive geometric baseline (geodesics AWAY)
- 3D Laplacian solver confirms analytic field is not misleading
- 3+1D feasibility at h=0.5 (TOWARD at k=5, but this is wave resonance)
- Superposition 0.01% on additive fields in 3D (propagator linearity)
- Action constrained from axioms (valley-linear at leading order)

### Lorentzian model (S = L(1-f·cos(2θ))) — bounded, not yet broadband-safe
- Geometric gravity: geodesics TOWARD mass at strong field (5e-2).
  At weak field (5e-5, the closure-card regime), lattice cannot resolve
  geodesic deflection (both models show NONE). The geometric mechanism
  is demonstrated at strong field only.
- All core tests pass at k=7 on 3D lattice (h=0.5, W=6, L=12):
  Born 1.50e-15, gravity +0.001 TOWARD, F∝M=1.00, 5/6 TOWARD b^(-1.23)
- Born, F∝M, d_TV, decoherence identical to Euclidean (flat-space same)
- Attractive window shifted: k=6.5-7.5 and k=10-12
- 3+1D feasibility at k=7 passes: Born 3.14e-15, gravity +0.000453 TOWARD,
  F∝M=0.99
- Multi-L at k=7 passes: gravity grows monotonically with L, purity stable
- Raw broadband spectral sums are AWAY, just as in the Euclidean lane
- Source-side weighting controls do NOT rescue broadband attraction; only
  detector-equalized counterfactual weighting flips many cases
- STILL OPEN: weak-field geometric baseline resolution and self-consistent
  Laplacian-field closure on the Lorentzian lane

## Honest negatives

- Energy levels don't converge to n² (lattice-dominated spectrum)
- Rotational isotropy doesn't improve with h (angular kernel intrinsic)
- Continuum dispersion: cone and parabola indistinguishable at h=0.25
- Hawking T~1/M: falsified (thermal shape is lattice geometry)
- Lorentz invariance: not emergent (τ invariance is assumed, not derived)
- Dimensional preference: falsified (all dimensions 1+1D-4+1D pass)
- Spectral averaging: AWAY on both Euclidean and Lorentzian retained lattices
- Source-side spectral weighting does not rescue broadband attraction on the
  retained Lorentzian lane
- Propagator is diffusive, not causal (no light cone from amplitude alone)
- Angular kernel: not derived (heuristic phase-coherence story only)

## The resonance mechanism

Gravity in both models is a resonance phenomenon:
- The deflection oscillates between TOWARD and AWAY as k varies
- The period is ~π in k on the 3D lattice
- The mechanism is complex multi-path interference, not simple two-path
- The resonance structure is geometry-dependent (changes with lattice size)
- Spectral averaging washes out the resonance (no universal attraction)
- F∝M = 1.00 holds at ALL k values (structural to the action)

The Euclidean model has the resonance fighting a repulsive baseline.
The Lorentzian model shifts the resonance window, but broadband/source-side
averaging still does not produce generic attraction.

## Open questions for the next session

### Validation of the Lorentzian model
1. Weak-field geodesic refinement: does geometric TOWARD appear at higher
   resolution in the actual closure-card regime?
2. Self-consistent Laplacian field on the Lorentzian model
3. The attractive window k=6.5-7.5 is narrow — is this stable under box/h
   changes and source perturbations?
4. Does any physically motivated source spectrum produce broadband TOWARD
   without using detector-defined reweighting?

### Theoretical
6. Can cos(2θ) be derived from the axioms? (The split distinguishes causal
   from spatial edges — this might follow from Axiom 3 or 4)
7. Does the Lorentzian action change the effective Hamiltonian/dispersion?
8. Is k=7 "natural" or does the model need a k-selection mechanism?
9. Does the Lorentzian model produce geometric gravity that survives
   spectral averaging? (This would be THE decisive test)

### The paper
10. Frame as: "A linear path-sum on a discrete causal graph with Lorentzian
    split-delay action produces a narrowband gravity-like attraction window,
    Born rule, gauge connections, and dynamic graph growth."
11. The Euclidean→Lorentzian transition is a discovery worth documenting
12. The resonance mechanism is novel physics worth describing

## File inventory

### Derivations
- distance-law-analytic-theorem-2026-04-09.md
- action-uniqueness-theorem-2026-04-09.md (renamed to constraint theorem)
- geometric-vs-dispersive-gravity-2026-04-09.md

### Key scripts (in rough importance order)
- frontier_lorentzian_closure_card.py — Lorentzian head-to-head
- frontier_lorentzian_k7_card.py — k=7 full card (ALL PASS)
- frontier_lorentzian_delay_geodesic.py — geodesics TOWARD with split delay
- frontier_lorentzian_multi_l_and_3plus1d.py — multi-L and 3+1D feasibility
- frontier_lorentzian_spectral.py — raw Lorentzian spectral AWAY
- frontier_lorentzian_source_weight_spectral.py — retained-lane source-side vs detector-side spectral weighting
- frontier_geodesic_gravity_test.py — geodesics AWAY on Euclidean
- frontier_fm_vs_k.py — F∝M=1.00 at all k
- frontier_wave_geodesic_decomposition.py — wave vs geometric separation
- frontier_resonance_phase_diagram.py — broad attractive plateau
- frontier_spectral_on_lattice.py — spectral averaging AWAY
- frontier_3d_laplacian_closure.py — self-consistent field confirmed
- frontier_retained_field_growth.py — Laplacian gravity on grown DAG
- frontier_dynamic_growth.py — Born on grown DAG
- frontier_3d_dynamic_growth.py — Born on grown 3D DAG
- frontier_angular_kernel_investigation.py — 7 kernels tested
- frontier_cos2_closure_card.py — cos²(θ) comparison
- frontier_3plus1d_same_geometry_refinement.py — resolution confirmed
- frontier_2d_gravity_sign_diagnosis.py — field strength + attenuation
- frontier_pn_suppression_math.py — weak-field enhances, strong oscillates
- frontier_born_from_information.py — composability → linearity → p=2
- frontier_causal_set_bridge.py — valid poset, r=0.997
- frontier_gauge_invariance.py — U(1) + AB + SU(2)
- frontier_spin_from_symmetry.py — Z₂ parity charge
- frontier_why_3plus1.py — all dimensions pass
- frontier_cosmological_expansion.py — 14% separation growth
- frontier_geometry_superposition.py — phase differences real
- frontier_experimental_prediction.py — Planck-suppressed
- frontier_decoherence_local_entangle.py — exponential scaling
- frontier_wave_particle_transition.py — imposed complementarity
- frontier_hawking_analog.py — thermal shape = lattice geometry
- frontier_causal_propagator.py — diffusive, no light cone
