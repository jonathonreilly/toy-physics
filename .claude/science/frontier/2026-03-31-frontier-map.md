# Frontier Map: 2026-03-31

## Coverage Summary
- Total scripts: 305
- Total log files: 156 (63 from 2026-03-30, 51 from 2026-03-31)
- Active mechanism families: 8
- Confirmed results: 12 (6 pre-session + 6 from corrected propagator)
- Unvalidated observations: 4
- Dead ends: 7

## Family Census

| Family | Scripts | Logs (3/31) | Focus | Status |
|--------|---------|-------------|-------|--------|
| suppressor (pocket_wrap) | 166 | 0 | Low-overlap order parameters | DORMANT (Codex lane) |
| generated-DAG core | 24 | 15 | Interference/gravity on random graphs | ACTIVE |
| propagator-correction | 16 | 14 | 1/L^p attenuation, phase valley | MATURE — core result established |
| decoherence-search | 17 | 10 | Endogenous decoherence mechanisms | EXHAUSTED for single-pass |
| interference (lattice) | 14 | 8 | Two-slit, Sorkin, Born rule | MATURE |
| gravity-core (lattice) | 11 | 5 | Delay field, geodesics, Lorentz | MATURE |
| gravity-characterize | 8 | 6 | Distance scaling, force law, corridor | PARTIAL — lensing retracted |
| pattern-dynamics | 4 | 4 | Gliders, field-coupled CA, movers | PARTIAL |
| growth-emergence | 1 | 1 | Phenomena during graph growth | CONFIRMED but thin |
| Codex pattern-sourced | 6 | 6 | Mover steering, footprint, support geometry | ACTIVE (Codex) |
| validation | 3 | 2 | Regression, sanity | CURRENT |
| infrastructure | 3 | 0 | Automation, locks | INFRASTRUCTURE |

## Confirmed Results (post-session)

1. **Corrected propagator**: 1/L^p attenuation fixes gravity sign (11/12 on DAGs)
2. **Gravity = pure phase**: k=0 → zero shift (exact)
3. **Phase valley**: spent-delay action decreases near mass (ΔS ≈ -L√(2f))
4. **k² scaling**: shift ∝ k² (CV=0.10, universal)
5. **Born rule**: I₃ = 4.28e-15 with corrected propagator
6. **Growth emergence**: interference at 6 layers, gravity at 3-8
7. **Attraction corridor**: degree ∈ [2,14] × gradient ∈ [0.09, 0.67]
8. **Force law on grid**: shift = C × k² × Q3, R²=0.91
9. **mass_overlap predictor**: R²=0.50 for decoherence susceptibility
10. **Phase noise on irregular graphs**: V drops 35% (exogenous)
11. **Directional recording = shuffled**: direction doesn't matter
12. **Full unification (post-fix)**: 4/12 all-three at η=0.7

## Unvalidated Observations

1. Force law coupling constant C — lattice-specific, not characterized on DAGs
2. Centroid trajectory oscillation downstream of mass — wave-optics interpretation
3. Codex mover-steering: late-support flip mechanism (43 toward vs 26 flip-away)
4. Codex footprint ranking: last6_union vs last3 — not yet hardened

## Dead Ends (do not revisit)

1. **1/delay^p attenuation** — produces repulsion, not attraction
2. **(1+field)^p boost** — unstable (blow-up ×7B), wrong scaling, Born rule violated
3. **2D gravitational lensing** — outgoing angle doesn't stabilize, retracted
4. **Universal force law on DAGs** — R²=0.20, topology-dependent
5. **Endogenous opacity decoherence** — hurts gravity (blocks phase-valley paths)
6. **Field fluctuation decoherence** — spatially uniform, no effect
7. **Backreaction decoherence** — slit-indistinguishable, 0/12

## Top 5 Highest-Value Gaps

### 1. Multi-pass decoherence with environment register
**Why:** All 5 single-pass endogenous mechanisms failed. The corrected propagator is too coherent for perturbative decoherence. The next step requires a fundamentally different architecture: amplitude propagates forward, creating an "environment state" at mass nodes, then the environment is traced out. This is the standard quantum decoherence mechanism (system + environment + partial trace) and the only remaining avenue.
**Feasibility:** Needs new code — a two-register path-sum where the "system" register propagates to the detector and the "environment" register stays at the mass. Moderate complexity.
**Effort:** Interactive, 1-2 experiments.
**Information gain:** VERY HIGH — could either solve endogenous decoherence or definitively show the model needs a new axiom.

### 2. Continuum limit with corrected propagator
**Why:** The earlier continuum limit test (anisotropy ~ 1/n_directions) used the standard propagator. Does 1/L^p change the scaling? If the corrected propagator has a cleaner continuum limit, it strengthens the "bridge to known physics." The script `continuum_limit_test.py` already exists but hasn't been run with `attenuation_mode="geometry"`.
**Feasibility:** Existing script, minor modification (add attenuation_mode parameter).
**Effort:** Quick — 1 experiment.
**Information gain:** HIGH — directly tests whether the propagator correction improves or worsens the continuum behavior.

### 3. Momentum-space scattering observable
**Why:** The centroid-shift observable saturates (flat distance scaling) and the ray-slope oscillates. A momentum-space observable (Fourier transform of the detector distribution, or angular decomposition) would give a cleaner characterization of gravitational deflection without the centroid's sensitivity to boundary effects.
**Feasibility:** Needs new analysis code but uses existing propagation.
**Effort:** Interactive, 1 experiment.
**Information gain:** HIGH — could rehabilitate the gravity characterization story.

### 4. Integration with Codex pattern-sourced mover results
**Why:** Codex has been developing the pattern-sourced mover/steering story on the same generated-DAG substrate. Their `generated_dag_pattern_sourced_mover_probe.py` measures whether persistent patterns steer amplitude packets — this is the "mass creates gravity" story from the other direction. Combining: does a pattern that steers amplitude also produce the phase-valley attraction we found?
**Feasibility:** Existing Codex scripts + existing corrected propagator. Cross-comparison.
**Effort:** Interactive, 1-2 experiments.
**Information gain:** MEDIUM-HIGH — unifies two independent investigation threads.

### 5. Decoherence on growing (not static) graphs
**Why:** All decoherence tests used static graphs. The model's Axiom 1 says "reality is an evolving network." If the graph GROWS during propagation (new nodes appearing mid-transit), the path-sum genuinely changes — this is topology change that CAN'T be reduced to a single-pass perturbation. It's the one topology-change mechanism not yet tested.
**Feasibility:** Needs new propagation code that adds nodes mid-transit.
**Effort:** Interactive, moderate complexity.
**Information gain:** MEDIUM — could work, but the topology-change test on static graphs already showed V unchanged, so expectations are modest.
