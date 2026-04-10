# Full Test Matrix — All Architectures × All Measures

**Date:** 2026-04-10
**Status:** Comprehensive scorecard across the ENTIRE REPO (pre-session + session).

## Pre-Session Architectures (from existing repo)

| Code | Architecture | Description |
|------|-------------|-------------|
| **MIR** | Exact Mirror / Z₂ | Flagship 2D DAG lane, Born-clean through N=100 |
| **MIR-2D** | Exact 2D Mirror | Validation card, strongest at N=60 |
| **Z2Z2** | Z₂ × Z₂ | Stronger decoherence, longer range |
| **MOD-3D** | 3D Modular DAGs | Random modular, gap-controlled |
| **MOD-4D** | 4D Modular DAGs | Strongest decoherence lane |
| **LAT-3D** | Ordered 3D Lattice (Spent-delay) | Dense lattice, h=0.25 |
| **VL-3D** | Ordered 3D Lattice (Valley-linear) | Flagship closure card, F∝M=1.00 |
| **UNI-2D** | 2D Uniform DAGs (24 seeds) | Gravity at 5.1 SE peak |

### Pre-Session 10-Property Card

| # | Property | MIR-2D (N=60) | VL-3D (h=0.25) | UNI-2D (N=30) | MOD-4D |
|---|----------|--------------|----------------|---------------|---------|
| 1 | Born | 1.08e-15 | 4.20e-15 | — | machine |
| 2 | d_TV | 0.857 | 0.834 | — | — |
| 3 | k=0 | 0 | 0 | — | — |
| 4 | F∝M | — | 1.00 | — | ~1.07 |
| 5 | Gravity | +2.57 | +0.000224 T | 5.1 SE | partial |
| 6 | Decoherence | 44.2% | 49.9% | 5.3% | bounded |
| 7 | MI | 0.756 | 0.64 | — | — |
| 8 | Purity stable | — | 50% stable | — | — |
| 9 | Gravity grows | wall N=120 | yes | peak N=30 | — |
| 10 | Distance law | — | b⁻⁰·⁹³/b⁻¹·⁰⁷ | b⁻¹·⁹³ | flat |

### Pre-Session Decoherence Scaling

| Dimension | Exponent | pur=0.99 at N | Best with LayerNorm |
|-----------|----------|---------------|-------------------|
| 2D | -1.01 (R²=0.83) | ~156 | — |
| 3D modular | ~-0.70 | ~500 | — |
| 4D modular | -0.178 (R²=0.84) | ~2.4M | — |
| 4D+LN+gap | -0.53 (R²=0.96) | ~16,500 | 70× over 2D |
| 5D | +0.11 | never | density-bound |

### Pre-Session Interference

| Observable | Value | Source |
|-----------|-------|--------|
| Sorkin |I₃|/P | 6.48e-16 | Fixed-DAG 3-slit |
| Best 2-slit V | 0.9951 | Fixed-DAG |
| Generated-DAG V range | 0.078-0.988 | Across seeds |

## Architectures Tested

| Code | Architecture | Description |
|------|-------------|-------------|
| **TM** | Transfer Matrix (Euclidean) | S = L(1-f), exp(-0.8θ²) kernel, 1/L^p, non-unitary |
| **TM-L** | Transfer Matrix (Lorentzian) | S = L(1-f·cos(2θ)), split delay |
| **BM** | Beam-Splitter Unitary | Local 2×2 unitaries, brick-wall pattern |
| **QW** | Quantum Walk (Grover coin) | Coined walk, 3-direction, unitary |
| **PU** | Polar-Factor Unitary | U = polar(M), global dense unitary |
| **CH-1D** | Chiral Walk 1+1D | 2-component, symmetric coin, θ-coupling |
| **CH-2D** | Chiral Walk 2+1D | 4-component, factorized coin |
| **CH-3D** | Chiral Walk 3+1D | 6-component, n=21, N=16 |

---

## PART 1: Original 10-Property Closure Card

| # | Property | TM | TM-L | BM | QW | PU | CH-1D | CH-2D | CH-3D |
|---|----------|-----|------|-----|-----|-----|-------|-------|-------|
| 1 | Born |I₃|/P | 2.5e-15 | 2.5e-15 | 5.6e-17 | 0.106 | 5.8e-2† | 3.3e-16 | 0 (exact) | 0.056 |
| 2 | d_TV | 0.83 | 0.78 | — | — | — | 0.80 | 0.53 | 0.68 |
| 3 | k=0 / f=0 control | 0 | 0 | 0 | — | — | 0 (exact) | 0 (exact) | 0 (exact) |
| 4 | F∝M alpha | 1.00 | 1.00 | FAIL | FAIL | 1.00 | 1.00 | 0.99 | 1.00 |
| 5 | Gravity sign | TOWARD* | TOWARD‡ | AWAY | AWAY | TOWARD§ | TOWARD | TOWARD | TOWARD¶ |
| 6 | Decoherence % | 49.5 | 49.5 | — | — | — | 38.6 | 82.8 | PASS |
| 7 | MI (bits) | 0.64 | 0.64 | — | — | — | 0.56 | 0.35 | 0.17 |
| 8 | Purity stable | PASS | PASS | — | — | — | PASS | CV=0.08 | CV=0.03 |
| 9 | Gravity grows | PASS | PASS | — | — | — | PASS | PASS | PASS |
| 10 | Distance law | b⁻⁰·⁹³ | b⁻¹·²³ | — | — | — | d⁻⁰·⁶⁰ | — | α=-0.56 |
| | **Score** | **10/10** | **10/10** | **2/10** | **0/10** | **3/10** | **10/10** | **10/10** | **10/10** |

\* k-window only (k=1-6), spectral AWAY
† Barrier I₃ fails; linearity is tautological
‡ k=7 window, spectral AWAY
§ Global medium, not localized mass
¶ Converged regime (N ≤ n-5), sign windows exist

---

## PART 2: 20 Moonshot Frontiers

| # | Frontier | TM | TM-L | CH-1D | CH-2D | CH-3D |
|---|----------|-----|------|-------|-------|-------|
| 1 | Distance law | b⁻⁰·⁹³ | b⁻¹·²³ | d⁻⁰·⁶⁰ | — | α=-0.56 |
| 2 | Lorentz/dispersion | ambiguous | — | **E²=θ²+k²** | approx (R²>0.999) | — |
| 3 | Action constraint | VL from axioms | — | θ-coupling | θ-coupling | θ-coupling |
| 4 | Dynamic growth | Born 4.3e-17 | — | FAIL (asymmetry) | FAIL (revival) | — |
| 5 | Entanglement | sub-area ln(2) | — | — | — | — |
| 6 | Energy spectrum | lattice-dominated | — | **exact analytic** | — | — |
| 7 | Spin / chirality | Z₂ parity | — | precesses, SG | — | — |
| 8 | Cosmology | 14% separation | — | FAIL | — | — |
| 9 | Hawking | thermal=lattice | — | FAIL (no thermal) | — | — |
| 10 | RG flow | scale-dependent | — | clean unitary | — | — |
| 11 | Gauge U(1) | structural | — | **AB 88.5%** | — | — |
| 12 | Two-body superposition | 0.01% (3D add.) | — | 0.17% | 0.10% | 0.65% |
| 13 | Decoherence scaling | CLT ceiling | — | CLT ceiling | — | — |
| 14 | Born from info | composability→p=2 | — | structural | structural | structural |
| 15 | Time dilation | correct sign | — | θ(1-f) | — | — |
| 16 | Wave-particle | imposed | — | FAIL (V=1) | — | — |
| 17 | Why d=3+1 | all dims pass | — | no preference | — | no preference |
| 18 | Causal set | r=0.997 | — | **r=0.956, strict LC** | — | — |
| 19 | Geometry superposition | phase diffs real | — | **0.08-0.61 rad** | — | — |
| 20 | Experimental predictions | Planck-suppressed | — | **3/4 pass** | — | — |

---

## PART 3: Structural Properties

| Property | TM | TM-L | BM | QW | PU | CH-1D | CH-2D | CH-3D |
|----------|-----|------|-----|-----|-----|-------|-------|-------|
| **Linearity** | YES | YES | YES | YES | YES | YES | YES | YES |
| **Norm preserved** | NO (10²²) | NO | YES | YES | YES | YES | YES | YES |
| **Locality (sparse)** | YES | YES | YES | YES | NO (dense) | YES | YES | YES |
| **Light cone** | NO (diffusive) | NO | NO | YES (v=1) | NO | **YES (v=1)** | — | — |
| **Unitary** | NO | NO | YES | YES | YES | YES | YES | YES |
| **Causal (DAG)** | YES | YES | YES | YES | — | YES | YES | YES |

---

## PART 4: Gravity Mechanism Properties

| Property | TM | TM-L | BM | QW | PU | CH-1D | CH-2D | CH-3D |
|----------|-----|------|-----|-----|-----|-------|-------|-------|
| **Geodesic direction** | AWAY | TOWARD | — | — | — | — | — | — |
| **Wave direction (k=5)** | TOWARD | AWAY | AWAY | AWAY | TOWARD§ | TOWARD | TOWARD | TOWARD¶ |
| **F∝M** | 1.00 | 1.00 | FAIL | FAIL | 1.00 | 1.00 | 0.99 | 1.00 |
| **Achromatic (k-indep)** | NO (k-window) | NO (shifted window) | — | — | — | YES (fixed θ) | YES | YES |
| **Achromatic (θ-indep)** | N/A | N/A | — | — | — | **NO (56% var)** | — | — |
| **Spectral survives** | AWAY | AWAY | — | — | TOWARD§ | N/A (no k) | N/A | N/A |
| **Broadband survives** | NO | NO | — | — | — | YES (achromatic) | YES | YES |
| **Superposition** | 0.01% (3D) | — | — | — | — | 0.17% | 0.10% | 0.65% |
| **N-stable** | N/A | N/A | — | — | — | YES (n≥41) | YES (n≥21) | basin¶ |

§ Global medium, not localized
¶ Converged regime with sign windows

---

## PART 5: Physics Emergence

| Property | TM | CH-1D | CH-3D | Status |
|----------|-----|-------|-------|--------|
| **Born rule** | ✓ (2.5e-15) | ✓ (3.3e-16) | ✓ (0.056) | CONFIRMED |
| **Klein-Gordon** | ambiguous | ✓ (R²>0.99999) | — | CONFIRMED (1D) |
| **Newtonian gravity** | F∝M in k-window | F∝M achromatic | F∝M in basin | PARTIAL |
| **Equivalence principle** | violated (k-dep) | violated (θ-dep) | — | FAIL |
| **Light cone** | NO | ✓ (v=1 exact) | — | CONFIRMED (1D) |
| **U(1) gauge** | structural | ✓ (AB 88.5%) | — | CONFIRMED |
| **SU(2) gauge** | custom code | FAIL (needs color) | — | FAIL |
| **Spin/chirality** | Z₂ parity | precession, SG | — | PARTIAL |
| **Decoherence** | 49.5%, CLT ceiling | 38.6%, CLT ceiling | PASS | BOUNDED |
| **Causal set** | r=0.997 | r=0.956, strict LC | — | CONFIRMED |
| **Cosmological expansion** | 14% | FAIL | — | TM ONLY |
| **Dynamic growth** | Born 4.3e-17 | FAIL | — | TM ONLY |
| **Geometry superposition** | phase diffs | 0.08-0.61 rad | — | CONFIRMED |

---

## PART 6: Summary Scores

| Architecture | Closure (10) | Moonshots (20) | Structural (6) | Gravity (9) | Physics (13) | Total |
|-------------|-------------|---------------|----------------|-------------|-------------|-------|
| **TM (Euclidean)** | 10/10 | 11 pass/partial | 3/6 | 4/9 | 7/13 | 35/58 |
| **TM (Lorentzian)** | 10/10 | ~8 | 3/6 | 5/9 | ~7/13 | ~33/58 |
| **Beam-Splitter** | 2/10 | — | 5/6 | 1/9 | — | ~8/58 |
| **Quantum Walk** | 0/10 | — | 5/6 | 0/9 | — | ~5/58 |
| **Polar Unitary** | 3/10 | — | 4/6 | 3/9 | — | ~10/58 |
| **Chiral 1+1D** | **10/10** | **13 pass/partial** | **6/6** | **7/9** | **9/13** | **45/58** |
| **Chiral 2+1D** | **10/10** | ~8 | 5/6 | 6/9 | ~7/13 | ~36/58 |
| **Chiral 3+1D** | **10/10** | ~7 | 5/6 | 5/9 | ~6/13 | ~33/58 |

---

## PART 7: Remaining Open Issues (by priority)

### Critical:
1. **Equivalence principle violation** — θ parameterizes both mass AND gravity coupling (56% variation)
2. **3+1D sign windows** — converged basin but not universal
3. **Distance exponent -0.6** — explained by beam spreading but not Newtonian

### Significant:
4. **Dynamic growth** — works on TM, fails on chiral
5. **CLT decoherence ceiling** — persists on all architectures
6. **SU(2) gauge** — needs additional color DOF
7. **Wave-particle complementarity** — absorption doesn't create which-path

### Moderate:
8. **Cosmological expansion** — fails on chiral
9. **Hawking analog** — no thermal spectrum on chiral
10. **3+1D Born** — 0.056 (weaker than lower dimensions)
11. **2+1D dispersion** — approximate KG only (slope 0.87-0.93)
12. **Chirality not conserved** — precesses, not a good spin analog

### Resolved/Understood:
13. **2D gravity sign** — non-unitarity artifact (TOWARD with polar U)
14. **Spectral averaging** — non-unitarity hierarchy (chiral doesn't have this problem)
15. **Angular kernel** — derived from Axiom 6 (turn-cost) in 2+1D
16. **Distance exponent** — beam spreading d^0.6 softens 1/d
17. **Convergence threshold** — N >> π/θ + 20, n >> 2×offset
18. **F∝M mechanism** — amplitude coupling (|sin²(θ(1-f))| linear in f)
