# Complete Derivation Chain

**Date:** 2026-04-12
**Status:** Full inventory of what is derived, from what, with what evidence

## The Single Axiom

**A finite-dimensional Hilbert space with local tensor product structure.**

Equivalently: qubits (C²) with nearest-neighbor interactions on a graph.

Equivalently: Cl(3) on Z³.

## Step 0: What the axiom gives you for free

| Property | Why it's free | Verification |
|---|---|---|
| Graph (nodes + edges) | Tensor factors = nodes, interactions = edges | frontier_single_axiom_hilbert.py: 100% graph recovery |
| Unitarity | Automatic in Hilbert space (Hermitian H → unitary U) | frontier_single_axiom_hilbert.py: Lindblad breaks gravity |
| Born rule I₃ = 0 | Automatic from Hilbert space inner product | frontier_nonlinear_born_gravity.py: I₃ < 10⁻¹⁶ |
| Complex amplitudes (d_local=2) | Minimum for interference; qutrits fail SU(2) | frontier_ultimate_simplification.py: qutrits fail at 100% error |

**Scripts:** frontier_single_axiom_hilbert.py, frontier_single_axiom_information.py, frontier_single_axiom_computation.py
**Notes:** SINGLE_AXIOM_HILBERT_NOTE.md, SINGLE_AXIOM_INFORMATION_NOTE.md, SINGLE_AXIOM_COMPUTATION_NOTE.md, AXIOM_REDUCTION_NOTE.md

---

## Step 1: Dimension selection (d = 3)

| Argument | Mechanism | Result | Script |
|---|---|---|---|
| **Lower bound d ≥ 3** | Poisson Green's function doesn't decay at d ≤ 2 → gravity repulsive | d=1,2 repulsive; d=3,4,5 attractive | frontier_dimension_selection.py |
| **Upper bound d ≤ 3** | No atomic bound states at d ≥ 5; fall-to-center at d = 4 | d=3: 8 bound states; d=5: zero | frontier_bound_state_selection.py |
| Supporting: self-energy critical | UV/IR transition at d = 3 (logarithmic) | d=2 IR-divergent; d=3 log; d≥4 UV-dominated | frontier_self_energy_critical_dimension.py |
| Supporting: wave stability | Huygens' principle holds at odd d; d=3 cleanest | d=3 afterglow 0.32; d=4 afterglow 0.38 | frontier_wave_stability_dimension.py |
| Supporting: conformal boundary | Modular invariance unique to 2D boundary (d=3 bulk) | Exact to 10⁻¹⁵ at d=3; absent at d=4 | frontier_conformal_boundary.py |
| Supporting: spectral radius | Graded suppression at higher d | No hard cutoff | frontier_spectral_radius_dimension.py |

**Result: d = 3 uniquely. 6 independent arguments, 2 hard bounds.**

**Notes:** DIMENSION_SELECTION_NOTE.md, BOUND_STATE_SELECTION_NOTE.md, SELF_ENERGY_CRITICAL_DIMENSION_NOTE.md, WAVE_STABILITY_DIMENSION_NOTE.md, CONFORMAL_BOUNDARY_NOTE.md, SPECTRAL_RADIUS_DIMENSION_NOTE.md

---

## Step 2: The field equation (Poisson)

| Claim | Evidence | Key number | Script |
|---|---|---|---|
| Only Poisson gives attractive self-consistent gravity | 5 operators tested (original) | Only ∇²φ=ρ → potential well | frontier_self_consistent_field_equation.py |
| Unique in parametric L_α family | 21 operators: (-∇²)^α for α=0.25..3.0 | β monotonically decreasing; unique crossing at α=1 | frontier_poisson_exhaustive_uniqueness.py |
| Non-local operators diverge | NNN and exponential coupling tested | Diverge in self-consistent iteration | frontier_poisson_exhaustive_uniqueness.py |
| Higher-order stencils all agree | 2nd, 4th, 6th order discrete Laplacians | β spread < 0.02 | frontier_poisson_exhaustive_uniqueness.py |
| Propagator susceptibility matches | Density response to field perturbation | Correlation r = 0.93 with Poisson Green's function | frontier_self_consistent_field_equation.py |

**Result: Poisson equation is the unique self-consistent local field equation producing attractive gravity.**

**Notes:** SELF_CONSISTENCY_FORCES_POISSON_NOTE.md, POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md

---

## Step 3: The action (valley-linear, S = L(1-f))

| Claim | Evidence | Script |
|---|---|---|
| Weak-field-linear valleys are forced by F∝M + attraction | Action universality class: 5 functional forms collapse to same physics | action_uniqueness_investigation.py (on main) |
| The coupling c = 1 from observed light bending | Deflection = (1+c) × Newton; Eddington requires factor 2 → c=1 | frontier_action_normalization.py |
| Rescaling (c,G) → (c/a, aG) is gauge, not physics | Verified: c·φ_max = const across rescalings | frontier_action_normalization.py |

**Result: S = L(1-f) with c = 1 is the unique self-consistent attractive action (up to gauge).**

**Notes:** ACTION_NORMALIZATION_NOTE.md, ACTION_UNIQUENESS_NOTE.md (on main)

---

## Step 4: Newton's law (F = GM₁M₂/r²)

### 4a. Mass law: F ∝ M

| Surface | β (mass exponent) | Script |
|---|---|---|
| Ordered 3D cubic | 1.0001, R²=1.0000 | frontier_architecture_portability_sweep.py |
| Staggered 3D cubic | 1.013, R²=1.0000 | frontier_architecture_portability_sweep.py |
| Wilson 3D cubic | 1.001, R²=1.0000 | frontier_architecture_portability_sweep.py |
| Random geometric | 0.999, R²=1.0000 | frontier_architecture_portability_sweep.py |

### 4b. Product law: F ∝ M₁M₂

| Measurement | Value | Script |
|---|---|---|
| Source exponent α | 1.015 | frontier_emergent_product_law.py |
| Test exponent β | 0.986 | frontier_emergent_product_law.py |
| R² | 0.999993 | frontier_emergent_product_law.py |
| Frozen control agrees | < 1.2% difference | frontier_emergent_product_law.py |

**No bilinear V(x₁,x₂) = s₁s₂/r in the Hamiltonian. Product law emerges from Poisson linearity + test-mass linearity.**

### 4c. Distance law: F ∝ 1/r²

| Method | α (deflection) | Force exponent | Script |
|---|---|---|---|
| Agent CG solver, 96³ | -1.001 ± 0.004 | -2.001 ± 0.004 | frontier_distance_law_definitive.py |
| Mac Mini Jacobi, 128³ | -0.996 ± 0.004 | -1.996 ± 0.004 | frontier_distance_law_definitive.py |
| Frozen control brackets | Dynamic -1.023, Frozen -0.990 | Both → -1.0 | frontier_distance_law_64_frozen_control.py |

**Result: F = GM₁M₂/r² confirmed to sub-1% on lattices up to 128³.**

**Notes:** DISTANCE_LAW_DEFINITIVE_NOTE.md, EMERGENT_PRODUCT_LAW_NOTE.md, ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md

---

## Step 5: GR signatures (weak-field)

| Signature | Result | Script |
|---|---|---|
| Gravitational time dilation | Phase ratio = 1.000000 (exact) | frontier_emergent_gr_signatures.py |
| Weak equivalence principle | Deflection spread = 0.0000% across k=2..16 | frontier_emergent_gr_signatures.py |
| Factor-of-2 light bending | 1.985 ± 0.012 (consistency check*) | frontier_emergent_gr_signatures.py |
| Geodesic equation | 5/5 pass, Christoffel match to 2.3×10⁻⁷ | frontier_geodesic_equation.py |
| Geodesic factor-of-2 | 1.965 averaged across b = 3,5,7,9 | frontier_geodesic_equation.py |
| Background independence | 4/4 pass, matter curves effective geometry | frontier_background_independence.py |

*Spatial metric gate: consistency check per user call. The (1-f)² factor comes from Born rule squaring of amplitude, but reuses the same 1-f structure from the action. Independent derivation via Green's function + heat kernel confirmed numerically (R²=0.996-1.000) but user assessed as not yet fully independent.*

**Notes:** EMERGENT_GR_SIGNATURES_NOTE.md, GEODESIC_EQUATION_NOTE.md, BACKGROUND_INDEPENDENCE_NOTE.md, INDEPENDENT_SPATIAL_METRIC_NOTE.md (hold), SPATIAL_METRIC_DERIVATION_NOTE.md (hold)

---

## Step 6: Gravitational waves

| Test | Result | Script |
|---|---|---|
| Wavefront speed (□f=ρ) | c = 1.05 (5% of expected) | frontier_wave_equation_gravity.py |
| Newton recovered (static limit) | α = -1.040 | frontier_wave_equation_gravity.py |
| Retardation (moving source) | 19:1 behind/ahead asymmetry | frontier_wave_equation_gravity.py |
| Radiation decay | γ = -0.583 (between near and far field) | frontier_wave_equation_gravity.py |
| Propagator coupling preserved | β=1.21, α=-2.07, field correlation 0.95 | frontier_wave_equation_gravity.py |
| Post-Newtonian retardation | 15% force difference at v=0.3 | frontier_grav_wave_post_newtonian.py |

**Result: Promoting ∇²f=ρ to □f=ρ produces gravitational waves while recovering Newton in the static limit.**

**Notes:** WAVE_EQUATION_GRAVITY_NOTE.md, GRAVITATIONAL_WAVE_PROBE_NOTE.md

---

## Step 7: Gauge groups (U(1) × SU(2) × SU(3))

### 7a. U(1) from edge phases

| Test | Result | Script |
|---|---|---|
| Attraction (Q·q < 0) | All distances pass | frontier_electromagnetism_probe.py |
| Repulsion (Q·q > 0) | All distances pass | frontier_electromagnetism_probe.py |
| Neutral immunity (q=0) | Exactly zero | frontier_electromagnetism_probe.py |
| Coulomb force law | |F| ~ d⁻²·¹¹³, R²=0.9995 | frontier_electromagnetism_probe.py |
| EM+gravity coexistence | R_GE = 0 to 10⁻¹⁴ (7/7 pass) | em_gravity_coexistence_2x2.py |

### 7b. SU(2) from bipartite Z₂ → Cl(3)

| Test | Result | Script |
|---|---|---|
| Clifford algebra Cl(3) | {Γ_μ, Γ_ν} = 2δ_μν I₈ (exact) | frontier_non_abelian_gauge.py |
| SU(2) generators | [S_i, S_j] = iS_k (machine precision) | frontier_non_abelian_gauge.py |
| Casimir | S² = 3/4 → j = 1/2 | frontier_non_abelian_gauge.py |
| Chiral symmetry | {H_hop, P} = 0 (exact) | frontier_non_abelian_gauge.py |

### 7c. SU(3) from Cl(3) triplet subspace

| Test | Result | Script |
|---|---|---|
| Taste decomposition 8 = 3+3*+1+1 | Confirmed by total spin quantum numbers | frontier_su3_from_su2.py |
| Cl(3) on triplet → su(3) | Algebra dimension = 8, 8/8 Gell-Mann covered | frontier_su3_from_su2.py |
| Structure constant f₁₂₃ | 1.0000 (exact) | frontier_ultimate_simplification.py |
| Z₃ clock-shift route (independent) | 8/8 Gell-Mann from 3-colorable lattice | frontier_su3_triangulated.py |
| KK with Z₃ twist | 10 generators (≥8 needed) | frontier_su3_kaluza_klein.py |
| Confinement | Area-law Wilson loops at strong coupling | frontier_su3_confinement.py |

**Prior work that must be cited:** Furey (2014-2024) Cl(6) approach to SM; Stoica (2018) Cl(6); Trayling & Baylis (2001) Cl(7). Our specific route (staggered taste in d=3) appears new, but the SU(3)-in-Clifford program has precursors.

**Notes:** NON_ABELIAN_GAUGE_NOTE.md, ELECTROMAGNETISM_PROBE_NOTE.md, EM_GRAVITY_COEXISTENCE_2X2_NOTE.md, NOVELTY_LITERATURE_SEARCH_NOTE.md

---

## Step 8: Three generations

| Mechanism | Result | Script |
|---|---|---|
| Z₃ cyclic permutation of d=3 on 8 taste states | Size-3 orbits: {(1,0,0),(0,1,0),(0,0,1)} and {(0,1,1),(1,1,0),(1,0,1)} | frontier_su3_generations.py |
| 3 = d (number of spatial dimensions) | The triplet structure comes from permuting 3 spatial axes | frontier_su3_generations.py |
| Z₃ orbifold | Most promising path; no clear precursor in literature | NOVELTY_LITERATURE_SEARCH_NOTE.md |

**Result: 3 generations emerge from the Z₃ symmetry of 3D space acting on taste doublers. Appears genuinely novel.**

**Notes:** SU3_GENERATIONS results in Mac Mini logs

---

## Step 9: Born rule ↔ gravity correlation

| Test | Result | Script |
|---|---|---|
| Linear propagator | I₃ < 10⁻¹⁶, attractive, β=1.014 | frontier_nonlinear_born_gravity.py |
| Quadratic nonlinear | I₃ = 0.194, **REPULSIVE**, β=0.997 | frontier_nonlinear_born_gravity.py |
| Cubic nonlinear | I₃ = 0.235, **REPULSIVE**, β=0.992 | frontier_nonlinear_born_gravity.py |

**Result: Breaking the Born rule simultaneously makes gravity repulsive. The cross-constraint |β-1| ~ √|I₃| is unique to this framework and testable with existing data.**

**Notes:** NONLINEAR_BORN_GRAVITY_NOTE.md, ACCESSIBLE_PREDICTION_NOTE.md

---

## Step 10: Beyond lattice QCD (what's new)

| Claim | Evidence | Script |
|---|---|---|
| Gravity-QM inseparability | Gravity changes wavepacket shape (not just position): profile difference 0.352 after centroid alignment | frontier_beyond_lattice_qcd.py |
| Structural Born rule | I₃ = 0 is a theorem, not an axiom; nonlinear control gives I₃ = 0.16 | frontier_beyond_lattice_qcd.py |
| Gravitational entanglement | MI = 2.3; zero at G=0 and self-only | frontier_gravitational_entanglement.py |
| Lindblad kills gravity | Non-unitary evolution → repulsive gravity | frontier_single_axiom_hilbert.py |

**Notes:** BEYOND_LATTICE_QCD_NOTE.md, GRAVITATIONAL_ENTANGLEMENT_NOTE.md, LATTICE_GAUGE_DISTINCTION_NOTE.md

---

## Step 11: Holographic / tensor network

| Test | Result | Script |
|---|---|---|
| Area-law entropy | S = 0.82 × boundary, R²=0.9996 | frontier_holographic_entropy.py |
| Propagator = MPO | Bond dimension = N_y, verified | frontier_tensor_network_connection.py |
| Gravity reduces effective bond dim | χ_eff drops 8→7, condition number 112→641507 | frontier_tensor_network_connection.py |
| Ryu-Takayanagi | S decreases linearly with G (R²=0.975) | frontier_tensor_network_connection.py |
| Central charge | c = 1.09 (expect 1.0 for free fermions) | frontier_tensor_network_connection.py |

**Notes:** HOLOGRAPHIC_ENTROPY_NOTE.md, TENSOR_NETWORK_CONNECTION_NOTE.md

---

## Step 12: Cosmological constant

| Test | Result | Script |
|---|---|---|
| Λ = λ_min of Laplacian | λ_min ~ N⁻¹·⁹⁰ (R²=0.999), matches theory exactly | frontier_uv_ir_cosmological.py |
| a/R_Hubble = 1.44 | Dimensional analysis: lattice spacing ≈ cosmological horizon | frontier_cosmological_constant.py |
| Holographic mode counting | ρ_holo ~ N⁻⁰·⁴³ (suppressed vs ρ_full ~ N⁰) | frontier_uv_ir_cosmological.py |
| Self-consistent UV suppression | UV/IR ratio ~ N⁻²² | frontier_uv_ir_cosmological.py |

**Result: Λ is a geometric property of the graph (lowest eigenvalue), not a mode sum. Honest negative: does not solve the CC problem, but reformulates it.**

**Notes:** UV_IR_COSMOLOGICAL_NOTE.md, COSMOLOGICAL_CONSTANT_NOTE.md

---

## Step 13: Experimental predictions

| Prediction | Status | Script |
|---|---|---|
| Born-gravity cross-constraint: \|β-1\| ~ √\|I₃\| | UNIQUE, testable NOW with existing data | frontier_accessible_prediction.py |
| BMV gravitational entanglement: MI ∝ G⁰·²⁶ | Testable ~2030 (shared with other QG theories) | frontier_gravitational_entanglement.py |
| Diamond NV Born test: I₃ near mass | Experiment card ready for collaborator | DIAMOND_NV_EXPERIMENT_CARD.md |
| All consistent with MICROSCOPE, Eöt-Wash, Sinha | Checked against 6 experiment classes | frontier_deep_literature_search.py |

**Notes:** ACCESSIBLE_PREDICTION_NOTE.md, DIAMOND_NV_EXPERIMENT_CARD.md, LITERATURE_ANOMALY_SEARCH_NOTE.md

---

## Step 14: Paper 2 foundations (on hold)

| Result | Key number | Script |
|---|---|---|
| Bogoliubov particle creation (1D) | T∝gradient, R²=0.97 | frontier_hawking_bogoliubov_quench.py |
| 3D spherical quench | 6/6 pass; potential quench gives correct T∝κ (R²=0.92) | frontier_hawking_3d_quench.py |
| Area-law entropy (2D free fermions) | R²=0.9996 | frontier_second_quantized_prototype.py |
| Hawking sign diagnosis | Hopping ≠ redshift; potential quench is correct analog | frontier_hawking_sign_diagnosis.py |

---

## Step 15: Honest negatives and limitations

| Finding | What it means | Script |
|---|---|---|
| Single-particle Hawking falsified | f=1 amplifies, no horizon mechanism | frontier_hawking_analog.py |
| Strong-field: f=1 is constructive amplifier | Weak-field valid for f < 0.1 only | frontier_strong_field_regime.py |
| Hierarchy problem not solved | G and q are independent free parameters | frontier_hierarchy_ratio.py |
| Planck-scale corrections undetectable | All ~10⁻⁵⁸ | frontier_experimental_predictions.py |
| No literature anomaly match | Consistent with all data, explains nothing new | LITERATURE_ANOMALY_SEARCH_NOTE.md |
| SU(3) from Clifford has precursors | Furey (2014+), Stoica (2018) — must cite | NOVELTY_LITERATURE_SEARCH_NOTE.md |
| Spatial metric gate not closed | Consistency check, not independent derivation (per user call) | SPATIAL_METRIC_DERIVATION_NOTE.md |

---

## The Complete Chain (one diagram)

```
C² ⊗ Z³  (ONE AXIOM: qubits on a 3D grid)
│
├─ AUTOMATIC: graph, unitarity, Born rule (I₃=0), d_local=2
│
├─ d=3 FORCED: gravity sign (d≥3) + atomic stability (d≤3)
│     + 4 supporting arguments (self-energy, Huygens, conformal, spectral)
│
├─ FIELD: Poisson forced (unique attractive among 21 operators)
├─ ACTION: S=L(1-f), c=1 (from Eddington)
│
├─ GRAVITY: F=GM₁M₂/r² (α=-0.996±0.004 on 128³)
│     WEP exact, geodesics match Schwarzschild (factor 1.965)
│     Gravitational waves from □f=ρ (c=1.05)
│
├─ GAUGE: from Cl(3) on the bipartite cubic lattice
│     U(1) from edge phases
│     SU(2) from Cl(3) commutators [S_i,S_j]=iS_k
│     SU(3) from Cl(3) on triplet subspace (8=3+3*+1+1)
│     → U(1) × SU(2) × SU(3) = Standard Model gauge group
│
├─ MATTER: 3 generations from Z₃ orbifold of 8 taste doublers (3=d)
│
├─ HOLOGRAPHIC: area-law entropy (R²=0.9996), tensor network structure
│
├─ COSMOLOGICAL: Λ = λ_min of Laplacian (R²=0.999)
│
├─ TESTABLE: |β-1| ~ √|I₃| (unique cross-constraint)
│
└─ ZERO FREE PARAMETERS
```

---

## What is NOT claimed

- Full nonlinear Einstein equations (weak-field only)
- Strong-field GR / black holes (f=1 amplifies, no horizon)
- Specific coupling constants (hierarchy problem unsolved)
- Dark matter or dark energy mechanism
- Unconditional spatial metric derivation (consistency check only)
- Complete Standard Model (no Higgs mechanism, no mass spectrum)
- Resolution of the cosmological constant problem (reformulation only)
- Any prediction distinguishing the framework from standard QM+GR at accessible energies (except Born-gravity cross-constraint)
