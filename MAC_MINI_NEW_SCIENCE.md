# Mac Mini — New Science Lanes

These are fresh experiments that push the framework further. Run after pulling latest.

```bash
cd Physics-compute
git pull origin claude/youthful-neumann
```

## Lane 1: Geodesic Equation (HIGH PRIORITY)

Shows that propagator trajectories match the emergent metric's geodesics.
This connects the propagator to GR at the trajectory level.

```bash
python3 scripts/frontier_geodesic_equation.py 2>&1 | tee ~/Desktop/geodesic.txt
```

**What to look for:** Does the propagator centroid trajectory match the Christoffel-symbol geodesic prediction? Deviation should be <5% in weak field.

## Lane 2: Strong-Field Regime

What happens when f→1 (near a "horizon")? Characterizes the breakdown.

```bash
python3 scripts/frontier_strong_field_regime.py 2>&1 | tee ~/Desktop/strong_field.txt
```

**What to look for:** At what f does weak-field GR break down? Is there a natural "horizon" at f=1? What happens to wavepackets that enter f>1?

## Lane 3: 3D Bogoliubov Quench (Paper 2)

Extends the 1D Hawking analog to a proper 3D spherical horizon.
This is the heaviest computation — 14³=2744 site eigendecomposition.

```bash
python3 scripts/frontier_hawking_3d_quench.py 2>&1 | tee ~/Desktop/hawking_3d.txt
```

**What to look for:** Does T∝κ (temperature proportional to surface gravity) hold in 3D? Does T∝1/R_h (larger horizon = colder)?

## Lane 4: Conformal Boundary

Tests whether the d=3 propagator's boundary has special CFT properties.

```bash
python3 scripts/frontier_conformal_boundary.py 2>&1 | tee ~/Desktop/conformal_boundary.txt
```

**What to look for:** Central charge c≈1 at d=3? CFT scaling of correlators?

## Lane 5: Self-Energy Critical Dimension

Already partially run — confirms d=3 as UV/IR transition. Rerun for clean output.

```bash
python3 scripts/frontier_self_energy_critical_dimension.py 2>&1 | tee ~/Desktop/self_energy.txt
```

## Lane 6: Bound State Selection (CONFIRM d=3 on bigger lattices)

The headline d=3 result. Run on Mini for bigger 4D/5D lattices.

```bash
python3 scripts/frontier_bound_state_selection.py 2>&1 | tee ~/Desktop/bound_states.txt
```

## Lane 7: Deep Experimental Literature Search

The earlier literature search found no anomaly match. But we should look deeper at:
- Precision tests of the equivalence principle (MICROSCOPE satellite, Eot-Wash)
- Gravitational Aharonov-Bohm experiments
- Atom interferometry gravity measurements (Stanford tower, MAGIS)
- Any experiment measuring gravitational phases at quantum level

```bash
python3 scripts/frontier_deep_literature_search.py 2>&1 | tee logs/2026-04-12-deep-literature.txt
```

**What to look for:** Any experimental result where gravitational phase effects were measured at quantum level. Even null results are useful -- they constrain the parameter space.

## Lane 8: Single Axiom Scripts

Three scripts testing whether the two axioms (path-sum + Poisson field) reduce to one:

```bash
python3 scripts/frontier_single_axiom_information.py 2>&1 | tee logs/2026-04-12-single-axiom-information.txt
python3 scripts/frontier_single_axiom_hilbert.py 2>&1 | tee logs/2026-04-12-single-axiom-hilbert.txt
python3 scripts/frontier_single_axiom_computation.py 2>&1 | tee logs/2026-04-12-single-axiom-computation.txt
```

**What to look for:** Does any single axiom (information-theoretic, Hilbert-space, or computational) recover both the path-sum propagator and the Poisson field equation?

## Lane 9: Hawking Sign Diagnosis

The 3D Hawking quench found a T-kappa sign issue. This script runs 5 hypothesis tests for the T-kappa sign reversal.

```bash
python3 scripts/frontier_hawking_sign_diagnosis.py 2>&1 | tee logs/2026-04-12-hawking-sign-diagnosis.txt
```

**What to look for:** Which of the 5 hypotheses explains the sign reversal? Is it a lattice artifact, a boundary condition issue, or a real physical effect?

## Priority Order

1. **Geodesic equation** (connects propagator to GR trajectories)
2. **3D Bogoliubov quench** (Paper 2 headline, needs compute)
3. **Strong-field regime** (understanding limitations)
4. **Conformal boundary** (strengthens d=3 argument)
5. **Self-energy** (supporting evidence)
6. **Bound states** (confirmation on bigger lattice)
7. **Deep literature search** (experimental constraints)
8. **Single axiom scripts** (axiom reduction, when ready)
9. **Hawking sign diagnosis** (resolve T-kappa sign issue)
