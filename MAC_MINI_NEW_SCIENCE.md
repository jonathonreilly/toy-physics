# Mac Mini — Current Run List

Pull first:
```bash
cd Physics-compute
git pull origin claude/youthful-neumann
```

Then run in this order:

## 1. Single Axiom Tests (HIGHEST PRIORITY — foundational question)

Can the two axioms be reduced to one? Three routes tested.

```bash
python3 scripts/frontier_single_axiom_information.py 2>&1 | tee ~/Desktop/single_axiom_info.txt
python3 scripts/frontier_single_axiom_hilbert.py 2>&1 | tee ~/Desktop/single_axiom_hilbert.txt
python3 scripts/frontier_single_axiom_computation.py 2>&1 | tee ~/Desktop/single_axiom_computation.txt
```

Route 2 (Hilbert) already passed on laptop — confirm here. Routes 1 and 3 still running on laptop.

## 2. Hawking Sign Diagnosis (Paper 2)

Why does T∝(-κ) for hopping quench? 5 hypothesis tests.

```bash
python3 scripts/frontier_hawking_sign_diagnosis.py 2>&1 | tee ~/Desktop/hawking_sign.txt
```

## 3. Conformal Boundary (d=3 selection)

Tests modular invariance of d=3 boundary CFT.

```bash
python3 scripts/frontier_conformal_boundary.py 2>&1 | tee ~/Desktop/conformal_boundary.txt
```

## 4. Geodesic Equation

Propagator trajectories match metric geodesics?

```bash
python3 scripts/frontier_geodesic_equation.py 2>&1 | tee ~/Desktop/geodesic.txt
```

## 5. Self-Energy Critical Dimension

d=3 as UV/IR transition.

```bash
python3 scripts/frontier_self_energy_critical_dimension.py 2>&1 | tee ~/Desktop/self_energy.txt
```

## 6. Bound State Selection (bigger lattices)

Confirm d=3 is highest dimension with stable atoms.

```bash
python3 scripts/frontier_bound_state_selection.py 2>&1 | tee ~/Desktop/bound_states.txt
```

## 7. Deep Experimental Literature Search

The earlier literature search found no anomaly match. Look deeper at:
- Precision tests of the equivalence principle (MICROSCOPE satellite, Eot-Wash)
- Gravitational Aharonov-Bohm experiments
- Atom interferometry gravity measurements (Stanford tower, MAGIS)
- Any experiment measuring gravitational phases at quantum level

```bash
python3 scripts/frontier_deep_literature_search.py 2>&1 | tee logs/2026-04-12-deep-literature.txt
```

Even null results are useful -- they constrain the parameter space.

## Run-all one-liner

```bash
for s in frontier_single_axiom_information frontier_single_axiom_hilbert frontier_single_axiom_computation frontier_hawking_sign_diagnosis frontier_conformal_boundary frontier_geodesic_equation frontier_self_energy_critical_dimension frontier_bound_state_selection; do echo "=== $s ===" && python3 scripts/${s}.py 2>&1 | tee ~/Desktop/${s}.txt && echo "DONE: $s"; done
```
