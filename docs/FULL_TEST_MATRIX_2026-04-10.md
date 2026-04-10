# Full Test Matrix — All Architectures × All Measures

**Date:** 2026-04-10 (updated with spot checks)
**Status:** Comprehensive scorecard across the ENTIRE REPO (pre-session + session + spot checks).

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
| 10 | Distance law | b⁻⁰·⁹³ | b⁻¹·²³ | — | — | — | d⁻⁰·⁶⁰ | d⁻²·⁵⁵ | α=-0.56 |
| | **Score** | **10/10** | **10/10** | **2/10** | **0/10** | **3/10** | **10/10** | **10/10** | **10/10** |

\* k-window only (k=1-6), spectral AWAY
† Part 1: Barrier I₃ fails (linearity is tautological). Part 2/5: Factorized coin gives 1D-per-pair dispersion, not isotropic 3D KG — needs coupled 6×6 Dirac coin
‡ k=7 window, spectral AWAY
§ Global medium, not localized mass
¶ Converged regime (N ≤ n-5), sign windows exist

---

## PART 2: 20 Moonshot Frontiers

| # | Frontier | TM | TM-L | CH-1D | CH-2D | CH-3D |
|---|----------|-----|------|-------|-------|-------|
| 1 | Distance law | b⁻⁰·⁹³ | b⁻¹·²³ | d⁻⁰·⁶⁰ | — | α=-0.56 |
| 2 | Lorentz/dispersion | ambiguous | — | **E²=θ²+k²** | approx (R²>0.999) | FAIL (R²=0.16)† |
| 3 | Action constraint | VL from axioms | — | θ-coupling | θ-coupling | θ-coupling |
| 4 | Dynamic growth | Born 4.3e-17 | — | FAIL (asymmetry) | FAIL (revival) | — |
| 5 | Entanglement | sub-area ln(2) | — | — | — | — |
| 6 | Energy spectrum | lattice-dominated | — | **exact analytic** | — | — |
| 7 | Spin / chirality | Z₂ parity | — | precesses, SG | — | SG 6.75, 117% asym |
| 8 | Cosmology | 14% separation | — | FAIL | — | — |
| 9 | Hawking | thermal=lattice | — | FAIL (no thermal) | — | — |
| 10 | RG flow | scale-dependent | — | clean unitary | — | — |
| 11 | Gauge U(1) | structural | — | **AB 88.5%** | **AB V=0.88** | FAIL (geometry) |
| 12 | Two-body superposition | 0.01% (3D add.) | — | 0.17% | 0.10% | 0.65% |
| | | VL-3D: 0.00% | | | | |
| 13 | Decoherence scaling | CLT ceiling | — | CLT ceiling | — | — |
| 14 | Born from info | composability→p=2 | — | structural | structural | structural |
| 15 | Time dilation | correct sign | — | θ(1-f) | — | — |
| 16 | Wave-particle | imposed | — | PASS (local V²+D²) | — | — |
| 17 | Why d=3+1 | all dims pass | — | no preference | — | no preference |
| 18 | Causal set | r=0.997 | — | **r=0.956, strict LC** | — | — |
| 19 | Geometry superposition | phase diffs real | — | **TV=0.039, dphi=0.25-0.66 rad** | — | — |
| 20 | Experimental predictions | Planck-suppressed | — | **3/4 pass (k-achromatic FAIL)** | — | — |

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
| **Achromatic (k-indep)** | NO (k-window) | NO (shifted window) | — | — | — | NO (k-sweep CV=2.66) | YES | YES |
| **Achromatic (θ-indep)** | N/A | N/A | — | — | — | **NO (56% var)** | — | NO (117% asym)‖ |
| **Spectral survives** | AWAY | AWAY | — | — | TOWARD§ | N/A (no k) | N/A | N/A |
| **Broadband survives** | NO | NO | — | — | — | NO (k-dependent deflection) | YES | YES |
| **Superposition** | 0.01% (3D) | — | — | — | — | 0.17% | 0.10% | 0.65% |
| | VL-3D: 0.00% | | | | | | | |
| **N-stable** | N/A | N/A | — | — | — | YES (n≥41) | YES (n≥21) | basin¶ |

§ Global medium, not localized
¶ Converged regime with sign windows
‖ Chirality-dependent: ψ₊ deflects 3.8× more than ψ₋

---

## PART 5: Physics Emergence

| Property | TM | CH-1D | CH-2D | CH-3D | Status |
|----------|-----|-------|-------|-------|--------|
| **Born rule** | ✓ (2.5e-15) | ✓ (3.3e-16) | ✓ (exact 0) | ✓ (0.056) | CONFIRMED |
| **Klein-Gordon** | ambiguous | ✓ (R²>0.99999) | approx (R²>0.999) | FAIL (R²=0.16)† | CONFIRMED (1D,2D) |
| **Newtonian gravity** | F∝M in k-window | F∝M but k-dependent | F∝M=0.99 | F∝M in basin | PARTIAL |
| **Equivalence principle** | violated (k-dep) | violated (θ-dep) | — | violated (117% asym) | FAIL |
| **Light cone** | NO | ✓ (v=1 exact) | — | — | CONFIRMED (1D) |
| **U(1) gauge** | structural | ✓ (AB 88.5%) | ✓ (AB V=0.88) | FAIL (geometry) | CONFIRMED (1D,2D) |
| **SU(2) gauge** | custom code | FAIL (needs color) | — | — | FAIL |
| **Spin/chirality** | Z₂ parity | precession, SG | — | SG 6.75, 117% grav asym | PARTIAL |
| **Decoherence** | 49.5%, CLT ceiling | 38.6%, CLT ceiling | 82.8% | PASS | BOUNDED |
| **Causal set** | r=0.997 | r=0.956, strict LC | — | — | CONFIRMED |
| **Cosmological expansion** | 14% | FAIL | — | — | TM ONLY |
| **Dynamic growth** | Born 4.3e-17 | FAIL | — | — | TM ONLY |
| **Geometry superposition** | phase diffs | TV=0.039, dphi=0.25-0.66 rad | — | — | CONFIRMED |

---

## PART 6: Summary Scores

| Architecture | Closure (10) | Moonshots (20) | Structural (6) | Gravity (9) | Physics (13) | Total |
|-------------|-------------|---------------|----------------|-------------|-------------|-------|
| **TM (Euclidean)** | 10/10 | 11 pass/partial | 3/6 | 4/9 | 7/13 | 35/58 |
| **TM (Lorentzian)** | 10/10 | ~8 | 3/6 | 5/9 | ~7/13 | ~33/58 |
| **Beam-Splitter** | 2/10 | — | 5/6 | 1/9 | — | ~8/58 |
| **Quantum Walk** | 0/10 | — | 5/6 | 0/9 | — | ~5/58 |
| **Polar Unitary** | 3/10 | — | 4/6 | 3/9 | — | ~10/58 |
| **Chiral 1+1D** | **10/10** | **14 pass/partial** | **6/6** | **5/9** | **9/13** | **44/58** |
| **Chiral 2+1D** | **10/10** | ~10 | 5/6 | 6/9 | ~8/13 | ~39/58 |
| **Chiral 3+1D** | **10/10** | ~9 | 5/6 | 5/9 | ~7/13 | ~36/58 |

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
7. **Chromaticity on chiral gravity** — corrected k-sweep at fixed θ shows strong k-dependence (CV=2.66)

### Moderate:
8. **Cosmological expansion** — fails on chiral
9. **Hawking analog** — no thermal spectrum on chiral
10. **3+1D Born** — 0.056 (weaker than lower dimensions)
11. **2+1D dispersion** — approximate KG only (slope 0.87-0.93)
12. **Chirality not conserved** — precesses, not a good spin analog
13. **VL-3D spectrum growth-contaminated** — CV=0.334, spectral radius=1.72 (non-unitary)

### Design Bottleneck (from spot checks):
0. **Factorized coin cannot produce 3D Klein-Gordon** — The independent 2×2 blocks on each chirality pair produce 1D-per-pair dispersion (R²=0.16 for isotropic 3D KG). This also prevents 3D Aharonov-Bohm (V=0.0). A coupled 6×6 or 8×8 Dirac-like coin is needed. This is the single biggest open design challenge.

### Resolved/Understood:
14. **2D gravity sign** — non-unitarity artifact (TOWARD with polar U)
15. **Spectral averaging** — non-unitarity hierarchy (chiral doesn't have this problem)
16. **Angular kernel** — derived from Axiom 6 (turn-cost) in 2+1D
17. **Distance exponent** — beam spreading d^0.6 softens 1/d (1D); d^-2.55 in 2D (steeper)
18. **Convergence threshold** — N >> π/θ + 20, n >> 2×offset
19. **F∝M mechanism** — amplitude coupling (|sin²(θ(1-f))| linear in f)
20. **Wave-particle complementarity** — passes under an explicit local path-tag model; absorption-only harness was invalid
21. **2D gauge works** — Node-phase U(1) exact (6.7e-16), AB V=0.884 in 2+1D chiral
22. **3D chirality conserved within pairs** — factorized coin preserves chirality per spatial pair (100%)

---

## PART 8: Spot Check Results (2026-04-10)

10 spot checks run to fill blank cells in the matrix. Scripts committed on `frontier/spot-checks`.

| # | Check | Architecture | Result | Verdict |
|---|-------|-------------|--------|---------|
| 1 | 3D Klein-Gordon dispersion | CH-3D | R²=0.156 | **FAIL** — factorized coin gives 1D-per-pair |
| 2 | 3D Aharonov-Bohm gauge | CH-3D | V=0.000 | **FAIL** — geometry prevents AB in 3D |
| 3 | 2D distance law | CH-2D | α=-2.55 (R²=0.87) | Steeper than 1D (d⁻⁰·⁶⁰), not Newtonian |
| 4 | VL-3D two-body superposition | VL-3D | 0.00% error | **PASS** |
| 5 | 3D chirality conservation | CH-3D | 100% within pair | **PASS** — coin preserves per-pair chirality |
| 6 | 3D Stern-Gerlach | CH-3D | 6.75 separation | **PASS** — gradient separates +z/−z |
| 7 | 3D chirality-dependent gravity | CH-3D | 117% asymmetry | **PASS** — ψ₊ deflects 3.8× more than ψ₋ |
| 8 | 2D node-phase U(1) gauge | CH-2D | max dev=6.7e-16 | **PASS** — exact invariance |
| 9 | 2D Aharonov-Bohm | CH-2D | V=0.884 | **PASS** — strong modulation |
| 10 | VL-3D energy spectrum | VL-3D | CV=0.334, ρ=1.72 | Growth-contaminated (non-unitary) |

### Key Insight

The **factorized coin** (independent 2×2 blocks per chirality pair) is the central design bottleneck. It explains:
- Why 3D KG fails (each pair disperses in 1D only)
- Why 3D gauge fails (AB requires coupled spatial dimensions)
- Why the 2D results are strong (2D has only one spatial pair)

A **coupled Dirac-like coin** (6×6 for 3+1D, mixing all chirality components) would be the natural next step. This is the highest-priority experiment remaining.
