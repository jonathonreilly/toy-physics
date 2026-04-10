# Full Test Matrix — All Architectures × All Measures

**Date:** 2026-04-10 (updated with spot checks, bottleneck probes, and axiom pass)
**Status:** Comprehensive scorecard across the ENTIRE REPO (pre-session + session + spot checks + bottleneck probes).

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
| **DIR-3D** | Dirac Walk 3+1D | 4-component spinor, Hamiltonian/shift hybrid, reversed mass coupling |

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
† Part 1: Barrier I₃ fails (linearity is tautological). Part 2/5: Factorized coin gives 1D-per-pair dispersion, not isotropic 3D KG. Generic coupled `6×6` families help but do not close; `DIR-3D` is the stronger current route.
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

`DIR-3D` is not yet scored as a full architecture in Part 6 because the branch
still mixes an integrated `16`-row core card with supporting stability scans
rather than one all-sections repo-wide score surface. But the current Dirac
evidence is no longer just scattered probes: the integrated core card now gives
a single canonical `12/16` read on the retained harness.

---

## PART 7: Remaining Open Issues (by priority)

### Critical:
1. **Factorized 3+1D chiral coin** — confirmed blocker for the current CH-3D lane. Coupled-coin scan lifts gauge visibility from `0.0000` to `0.9142` and KG fit from `R²=0.0627` to `0.4787`, but isotropic 3D KG still does not retain there.
2. **Dirac 3+1D gravity stability** — the 4-component Dirac walk closes proper Born, exact KG (`R²=1.000000`), nonzero AB (`V=0.5056`), split susceptibility, and boundary robustness on the integrated card, but the larger-lattice lane still keeps non-monotone `N`-growth plus mixed-sign distance law even under open boundaries.
3. **Equivalence / parameter overload** — splitting `theta_m` from gravity susceptibility reduces theta-envelope sensitivity (`3.802 -> 2.803`, `CV 1.0825 -> 0.9013`) but leaves strong k-chromaticity intact (`CV_k = 2.6580`).
4. **3+1D periodic sign windows** — mostly recurrence / boundary artifacts in CH-3D. Reflecting is `25/25` TOWARD across all scanned cells; open classical and phase-kill are also `25/25` TOWARD, while periodic retains AWAY corners.
5. **Distance exponent -0.6** — explained by beam spreading but not Newtonian

### Significant:
6. **Dynamic growth** — works on TM, fails on chiral
7. **CLT decoherence ceiling** — persists on all architectures
8. **SU(2) gauge** — needs additional color DOF
9. **Chromaticity on chiral gravity** — corrected k-sweep at fixed θ shows strong k-dependence (CV=2.66)

### Moderate:
10. **Cosmological expansion** — fails on chiral
11. **Hawking analog** — no thermal spectrum on chiral
12. **3+1D Born** — 0.056 (weaker than lower dimensions)
13. **2+1D dispersion** — approximate KG only (slope 0.87-0.93)
14. **Chirality not conserved** — precesses, not a good spin analog
15. **VL-3D spectrum growth-contaminated** — CV=0.334, spectral radius=1.72 (non-unitary)
16. **Dirac decoherence rows need redesign** — explicit record purity behaves correctly while the current detector proxy barely moves, so the retained negative is harness-level for now.
17. **Dirac strict isotropy gate still misses** — the integrated core card gets exact low-k KG fit but still lands isotropy ratio `1.1034` at the current retained mass point, so `C11` stays stricter than a scalar `R²` gate.
18. **Dirac fixed-`theta` k-achromaticity still fails** — the literal `C13` row on the integrated card gives `CV = 0.3606` on a matched-travel packet sweep, with residual wavelength-sensitive deflection.

### Design Bottleneck (from spot checks):
0. **Separable continuation channels are the central 3D transport blocker** — In CH-3D, the independent `2×2` blocks on each chirality pair produce 1D-per-pair dispersion (`R²=0.16`) and zero 3D AB visibility. Generic coupled `6×6` families help but do not close. The first architecture that actually closes both gates materially is the irreducible 4-component Dirac Hamiltonian lane (`R²=1.000000`, `AB V=0.519`). The highest-priority design task is therefore no longer “arbitrary larger coupled coin,” but a symmetry-matched irreducible 3+1D transport law.

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
23. **Periodic sign windows are mostly recurrence artifacts** — reflecting is `25/25` TOWARD and open classical / phase-kill are `25/25` TOWARD on the boundary phase diagram; the worst sign windows are tied to periodic wrap.
24. **Theta overload is real but not sole** — split mass/gravity coupling reduces theta-envelope sensitivity but does not cure k-chromaticity, so overloading matters without being the whole story.
25. **Cross-axis coupling helps but does not finish 3D** — a coupled `6×6` family lifts 3D gauge response strongly and improves KG fit, but the best low-k isotropic fit remains only moderate (`R²=0.4787`).
26. **Dirac Hamiltonian closes KG and AB but not yet gravity stability** — the 4-component `DIR-3D` lane recovers exact isotropic KG and nonzero AB, but larger-lattice `v4` keeps non-monotone `N` response and mixed-sign offset law even with open boundaries.
27. **Dirac field broadening helps offset law but not `N`-growth** — a broad Gaussian source field reaches `5/5` TOWARD offsets with `alpha = 3.053`, `R² = 0.8098`, but monotonicity over `N` still fails.
28. **Dirac source smoothing is not the missing fix** — a Gaussian initial packet can improve the sign count on one narrow `N` sweep (`4/5` TOWARD at `sigma=1.25`) but does not repair monotonicity and does not beat the point source on the offset law.
29. **Weak coupling does not rescue Dirac gravity stability** — sign-stability totals are unchanged across a 10× strength sweep; the cleaner trend is at larger `lambda`, which points to geometry/recurrence rather than coupling magnitude.

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

The stronger next step is now an **irreducible 3+1D transport law**. The branch already has one concrete example: the 4-component `DIR-3D` Hamiltonian lane closes exact KG and restores nonzero AB, even though its gravity stability is still incomplete.

---

## PART 9: Bottleneck Probes (2026-04-10)

These are not new score-card rows for the existing architectures. They are targeted design probes meant to identify why the same failures keep reappearing.

| Probe | Harness | Key result | Interpretation |
|---|---|---|---|
| Coupled 3+1D coin scan | `frontier_chiral_3plus1d_coupled_coin_scan.py` | Baseline `mix=0`: KG `R²=0.0627`, gauge `V=0.0000`. Best gauge at `mix=0.88`: `V=0.9142`. Best KG at `mix=1.00`: `R²=0.4787`. | Separability is a confirmed 3D blocker, but arbitrary coupling alone does not yet recover a clean isotropic 3D KG law. |
| Dirac 3+1D v3 | `frontier_dirac_walk_3plus1d_v3.py` | Exact Hamiltonian KG `R²=1.000000`, AB flux-tube `V=0.519`, `F∝M=1.000`, closure `7/10`. | An irreducible 4-component spinor transport law can recover the two hardest 3D gates that the factorized chiral lane misses. This weakens any generic 3D no-go reading. |
| Dirac 3+1D v4 convergence | `frontier_dirac_walk_3plus1d_v4_convergence.py` | Best at `m0=0.10`: periodic closure plateaus at `7/10` for `n=17..29`; open boundaries do not fix `N`-monotonicity or offset-law failure. | Larger lattices do not rescue the remaining Dirac gravity issues. In the current 4-component implementation, the residual failures look structural rather than purely boundary-driven. |
| Dirac decoherence / record probe | `frontier_dirac_walk_3plus1d_decoherence_probe.py` | Clean vs record residual `0.91-0.94`, record-mixture purity `~0.500`, detector proxy barely moves. | The current closure-card purity/decoherence proxy is a harness mismatch for `DIR-3D`. Dirac should be judged with explicit which-path record purity plus an interference-residual metric. |
| Dirac observable panel | `frontier_dirac_walk_3plus1d_observable_panel.py` | Centroid and shell agree `5/6`, current `3/6`, peak `0/6`, first-arrival fixed at layer `6`. | `C16` is now concrete: centroid/shell are the best current sign proxies, peak is too wave-sensitive, and multi-observable agreement must become an explicit promotion gate. |
| Dirac integrated core card | `frontier_dirac_walk_3plus1d_core_card.py` | `12/16`: Born `3.98e-16`, `F∝M` pass, AB `0.5056`, record-purity pass, split susceptibility pass, boundary robustness pass; fails on `N`-growth, distance law, strict isotropy gate, and fixed-`theta` `k`-achromaticity. | The `DIR-3D` lane is now one retained harness rather than four scattered probes. Its remaining failures are narrowly localized and explicitly named. |
| Dirac source smoothing | `frontier_dirac_walk_3plus1d_source_smoothing_scan.py` | Best Gaussian source (`sigma=1.25`) gives `4/5` TOWARD on the short `N` sweep, but monotonicity still fails and the point source remains best on the offset law. | Source smoothing is not the missing fix. |
| Dirac field smoothing | `frontier_dirac_walk_3plus1d_field_smoothing_scan.py` | Broad Gaussian field reaches `5/5` TOWARD offsets with `alpha = 3.053`, `R² = 0.8098`, but `N` monotonicity still fails. | Mass-field shape matters for the offset law, but it does not solve the deeper gravity-stability problem by itself. |
| Dirac weak coupling / larger `lambda` | `frontier_dirac_walk_3plus1d_weak_coupling_scan.py` | Cross-strength sign-stability is unchanged; magnitude-law fit improves mainly with larger `lambda` (`R² = 0.8537` at `lambda = 0.70`). | The remaining Dirac failures are more geometry/recurrence-driven than coupling-driven. |
| Graph Laplacian KG core card (audited) | `frontier_graph_kg_16card.py` | Audited score `13/16`: local KG operator closes `C4/C5/C9/C10/C11/C15/C16`, but Born fails (`|I3|/P = 1.9943`), carrier-`k` achromaticity fails (`CV = 1.0786`), and the split mass/gravity row flips sign at `m = 0.8`. | The no-coin local graph lane is real and promising, but the inflated `16/16` story does not survive audit. Treat it as a live probe, not a retained replacement architecture. |
| Graph true KG vs CN comparison | `frontier_graph_true_kg_vs_cn.py` | On cubic, CN free-mode fit lands at `R² = 0.9634`, slope `0.7055`, intercept `-0.0263`, isotropy `1.1728`, while true local KG lands at `R² = 0.9998`, slope `0.9520`, intercept `0.0932`, isotropy `1.0309`. On the tested operating point both still give TOWARD gravity and `F∝M`. | The current CN scalar graph lane is a strong low-energy scalar control, not a faithful stand-in for a true local graph KG theory. Free theory and weak-field gravity rows must now be treated as separate claims. |
| Staggered fermion probe | `frontier_staggered_fermion.py` | Genuine staggered Dirac dispersion closes exactly: `E² = m² + sin²(k)` in 1D and `R² = 1.000000` for the 3D low-`k` KG fit. Gravity is `18/18` TOWARD and monotone in 1D, `F∝M` is `R² = 0.999975`, Born is `1.20e-15`, norm drift is `4.44e-16`. | This is the strongest current no-coin genuine Dirac lane. Its main unresolved issue is transport realism: the current CN evolution blows through a strict light-cone gate, so it is promising but not yet a retained replacement architecture. |
| Staggered fermion force-based card | `frontier_staggered_17card.py` | **Force-based canonical card**: gravity rows use F=-⟨dV/dz⟩ instead of centroid shift. 1D n=61: `17/17` (6/6 families, no qualifiers). 3D n=9: `17/17` (6/6 families). 3D n=11,13: `17/17` (4/6 families, energy projections skipped). Full suite baseline: 1D `29/38`, 3D `28/38`. The centroid oscillates in a permanent period-4 pattern on the staggered periodic lattice; force converges at all tested sizes. | The retained staggered result. Rows C5/C9/C10/C15/C16 use force semantics (different from the repo-wide centroid card). C12 is a native persistent-current test (1D ring or 3D torus on the actual card lattice). C17 tests all 7 families including anti/Nyquist at n=9; anti is TOWARD under force measurement. See `STAGGERED_FERMION_CARD_2026-04-10.md` for the full semantic-differences table. |
| Staggered graph portability probe | `frontier_staggered_graph_portable.py` | Bipartite random geometric, bipartite growing, and cubic lattice all pass `7/7` retained rows. | Portability established; superceded by the cycle battery for gauge and backreaction testing. |
| Staggered cycle-bearing battery | `frontier_staggered_cycle_battery.py` | **9/9 on 3 cycle-bearing families**: random geometric (36), growing (48), layered cycle (24). Includes native gauge (B8: sin(A) persistent current on graph cycle, R²=0.95-0.9999), iterative backreaction (B5: 15/15 TOWARD), shell/spectral diagnostics (B9: G_eff=12-178, spectral ratio 8-19%). | Retained cycle battery. See `CYCLE_BATTERY_NOTE_2026-04-10.md`. The force-scale gap (G_eff) is structural (Poisson Green function smoother than 1/r on small graphs), not a sign/linearity failure. Layered gauge holdout is closed (layered cycle family has cycles + gauge PASS). |
| Staggered graph portability stress probe | `frontier_staggered_graph_portability_stress.py` | Larger, more irregular bipartite families still retain the staggered force battery. Current run: random geometric stress `8/8` on `n=81`, growing stress `8/8` on `n=82`, chorded grid stress `8/8` on `n=144`, layered DAG stress `8/8` on `n=66`. Gauge passes on the cycle-bearing families and is N/A on the acyclic layered family. | Stress checkpoint for portability beyond the baseline probe. This is the first larger-size / more irregular confirmation that the retained battery survives on the same force semantics. |
| Staggered graph failure map | `frontier_staggered_graph_failure_map.py` | Odd-cycle defect and parity-wrap inconsistency are structural breaks: each injects a same-color edge and preserves `8/8` only in the retained battery, not in the staggered assumptions. Dense shortcuts and high-degree contamination are graceful degradations: retained battery still passes `8/8`, with gauge current still present on cycle-bearing families. | Adversarial boundary map for the retained staggered lane. It operationalizes `GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md` by separating bipartite/parity violations from shortcut/high-degree contamination. |
| Graph scalar + spinor prototype | `frontier_graph_scalar_plus_spinor.py` | Matter norm stays at machine precision, the matter centroid shifts TOWARD the scalar source across the tested strength scan, and a nontrivial upper/lower spinor imbalance survives. | A two-field graph architecture is plausibly cleaner than forcing gravity and spin into one field. The immediate blocker is that the scalar background is still external and one-way; there is no self-consistent backreaction yet. |
| Staggered self-gravity probe | `frontier_staggered_self_gravity.py` | **5/5 on 3 cycle-bearing families**: random geometric (6% contraction), growing (1%), layered cycle (36%). No external source — |ψ|² generates its own Φ. Force 20/20 TOWARD, norm <7e-16, 0 sign flips, 3/3 state families. | First genuine endogenous gravity result. The wavepacket contracts under self-gravity (Schrödinger-Newton on graph). Layered cycle shows strongest contraction due to channeling. See `CYCLE_BATTERY_NOTE_2026-04-10.md`. |
| Two-field coupling prototype | `frontier_two_field_coupling.py` | Separate Φ field (relaxation+source) and staggered ψ (CN). Φ grows from zero sourced by |ψ|². Force 30/30 TOWARD, norm 9e-16, width contracts to 0.9992 (binding). | First two-field endogenous gravity. Separates gravitational DOF from matter DOF. Next: wave-equation Φ dynamics, larger graphs, full battery. |
| Staggered layered backreaction bridge | `frontier_staggered_layered_backreaction.py` | Layered DAG-compatible family: zero-source reduction exact, source-on force `+3.064e-01` TOWARD, source-response `R²=1.0000`, `Phi` residual `3.84e-16`, norm drift `3.33e-16`, gauge `N/A`. Layered stress family: source-on force `+1.849e-01` TOWARD, `R²=1.0000`, `Phi` residual `1.69e-16`, norm drift `2.22e-16`, gauge `FAIL`. | First layered / DAG-compatible backreaction bridge. It strengthens the source-generated `Phi` story on the admissible layered family, but the cycle-bearing stress family still fails native gauge closure, so this is a bridge result, not self-gravity closure. |
| Staggered cycle-bearing battery | `frontier_staggered_cycle_battery.py` | Integrated retained cycle-bearing harness: random geometric `9/9`, growing `9/9`, layered cycle `9/9`. Rows include zero-source control, source linearity, two-body additivity, force sign, iterative stability, norm, family robustness, native gauge closure, and force-gap plus shell/spectral characterization. | Current retained cycle-bearing staggered result. It unifies iterative endogenous closure and native graph-loop gauge closure in one force-based harness while keeping the source-scale miss as a characterization row rather than a failure gate. See `CYCLE_BATTERY_NOTE_2026-04-10.md`. |
| Weak-coin chiral + potential probe | `frontier_weakcoin_16card.py` | Default right-polarized packet scores `16/16` with strict light cone, exact norm, Born `2.66e-16`, force-achromaticity and force-level equivalence. But the new state-family sweep shows `R` TOWARD, `L` AWAY, symmetric AWAY, and antisymmetric TOWARD. | This is a real sector-conditioned success, not a universal gravity architecture. It motivates a formal state-family robustness gate in the core card. |
| Split mass vs gravity coupling | `frontier_chiral_split_mass_gravity.py` | KG and `F∝M` survive unchanged. Theta-envelope sensitivity drops from exponent `3.802` to `2.803` and `CV 1.0825` to `0.9013`. `k`-chromaticity stays `CV_k = 2.6580`. | `theta` overload is real, but it is not the only bottleneck; wavelength sensitivity survives the split. |
| Boundary-condition phase diagram | `frontier_chiral_3plus1d_boundary_phase_diagram.py` | Periodic coherent has `4/25` AWAY consensus cells, periodic classical/phase-kill `10/25`; reflecting is `25/25` TOWARD in all modes; open classical/phase-kill are `25/25` TOWARD. | The 3+1D sign problem is dominated by periodic recurrence / boundary effects, not by a torus-observable bug. |

## PART 10: Expanded Core Card (N = 17)

The old 10-row closure card is still useful, but it is no longer the best
front-door card by itself. The best current core card is:

- `C1-C10`: operating-point health
- `C11-C17`: structural bottleneck checks

Optional:
- `C18`: growth / backreaction separation

| Row | Test | Description | Current branch read |
|---|---|---|---|
| C1 | Born barrier / slit `|I3|/P` | Pairwise/Born interference under blocking. | retained operating-point gate |
| C2 | `d_TV` / slit distinguishability | Whether the slit harness actually separates alternatives. | retained |
| C3 | null control (`k=0` or `f=0`) | No-field baseline. | retained |
| C4 | `F∝M` scaling | Weak-field linearity in source strength or mass. | retained |
| C5 | gravity sign at retained point | Minimal TOWARD/AWAY operating-point check. | retained but insufficient alone |
| C6 | decoherence / record proxy | Weak environment / record sensitivity. | retained but bounded; `DIR-3D` needs explicit record purity instead of detector concentration proxy |
| C7 | mutual information | Branch correlation strength. | retained |
| C8 | purity stability | Whether the record proxy is stable across the scan. | retained, but proxy choice is architecture-sensitive |
| C9 | gravity growth with propagation | Whether the signal is a trend instead of one lucky depth. | retained |
| C10 | distance law | Offset falloff and fit quality. | retained with caveats |
| C11 | 3D KG isotropy / coupled-coin dispersion | `E^2` vs `k^2` along axes/diagonals and isotropy ratio. | factorized CH-3D fails; generic coupled family improves but only `DIR-3D` closes KG cleanly |
| C12 | 3D gauge-loop / AB visibility | Genuine 3D loop/flux response on the same transport law. | factorized CH-3D fails; generic coupled family helps, and `DIR-3D` flux-tube gives retained nonzero AB |
| C13 | fixed-`theta` `k`-achromaticity | Deflection CV across carrier `k` at matched travel distance. | current CH-1D fails (`CV_k ≈ 2.66`) |
| C14 | split mass vs gravity susceptibility | Separate free gap from gravity coupling. | split helps but does not solve chromaticity |
| C15 | boundary-condition robustness | Same `delta = d/n`, `lambda = L/n` point under periodic/reflecting/open boundaries. | current 3+1D periodic windows are mostly boundary-sensitive |
| C16 | multi-observable gravity consistency | First-arrival, peak, current, centroid, torus-aware centroid on one run. | concrete in `DIR-3D`: centroid/shell agree `5/6`, current `3/6`, peak `0/6`; now wired into the integrated Dirac core card |
| C17 | state-family robustness | Same transport/gravity claim under packet-family / polarization / chirality / sublattice preparations. | Force-based staggered card: all 7 families (incl. anti/Nyquist) TOWARD under force measurement in 1D and 3D n=9; 3D n=11,13 omit energy-projected families because eigensolve is skipped. Weak-coin chiral: R-only TOWARD, L/sym AWAY (sector-conditioned). Centroid-based staggered: anti oscillates with lattice size (period-4 artifact). |

### Optional Core-Adjacent Row

| Row | Test | Description |
|---|---|---|
| C18 | growth / backreaction separation | Apply growth or record deposition after transport/readout rather than while the state is still coherent. |

### Recommended Order

1. `C1-C5`: prove the operating point is not nonsense
2. `C11-C17`: prove the architecture is not structurally broken
3. `C6-C10`: add measurement and scaling context
4. `C18` if growth or endogenous backreaction is in scope

This is the best current N-card for core tests. If a branch cannot clear these
rows, the moonshots are likely to mislead.
