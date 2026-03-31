# Frontier Map: 2026-03-31 (Session Close)

## Session Summary
- **63 experiments** over one extended session
- **4 code review bugs fixed** (two_register env, mass_scaling label, between_slit geometry, constant_deflection field)
- **Key breakthrough**: corrected propagator (1/L^p) + two-register decoherence at proper geometry

## Established Results (HIGH confidence)

| # | Result | Evidence |
|---|--------|---------|
| 1 | 1/L^p corrected propagator fixes gravity sign | 90% attract on DAGs, k=0→zero |
| 2 | Gravity = pure phase effect (phase valley) | ΔS ≈ -L√(2f), shift ∝ k² |
| 3 | Born rule preserved | I₃ = 4.28e-15 |
| 4 | Interference preserved | V = 0.995, R_c unchanged (13/13 exact) |
| 5 | Growth emergence | Interference at 6 layers, gravity at 3-8 |
| 6 | Δky b-independent | 2D log field + multi-path averaging |
| 7 | Δky mass-independent | Threshold effect, not F∝M |
| 8 | Endogenous decoherence (two-register) | D=40%, ALL THREE=30% at optimal geometry |
| 9 | Decoherence is geometry-tuned | Requires mass_offset=1, fine env |
| 10 | ALL THREE not structurally predictable | Best predictor r=0.24 (slit_mass_asym) |
| 11 | Attraction corridor | deg ∈ [2,14] × gradient ∈ [0.09, 0.67] |
| 12 | mass_overlap predicts decoherence susceptibility | R²=0.50 |
| 13 | Regular lattice: D=0% (symmetry blocks env selectivity) | V_coh=0.997 but V_2reg=0.997 |
| 14 | Fringes survive mass on lattice | V_mass=1.0 across k=0.5..8.0 |
| 15 | Dual mass clusters worse than single | D=1/15 vs D=5/15 |
| 16 | Δky mass-independent | Threshold effect, not F∝M |
| 17 | Decoherence universal (purity < 0.99 for all seeds) | Mean purity=0.80, density matrix |
| 18 | Purity INCREASES with graph size | 0.57→0.89 from 6→25 layers |
| 19 | Cumulative env also wrong-scaling | Same trend as node-label |

## Dead Ends (do not revisit)

| # | Dead end | Why |
|---|----------|-----|
| 1 | 1/delay^p attenuation | Produces repulsion |
| 2 | (1+field)^p boost | Unstable, blow-up, Born rule violated |
| 3 | 2D gravitational lensing | Outgoing angle doesn't stabilize |
| 4 | Universal force law on DAGs | R²=0.20, topology-dependent |
| 5 | F∝M mass scaling | Δky is mass-independent |
| 6 | Single-pass decoherence (5 mechanisms) | All ineffective with corrected propagator |
| 7 | Structural predictor for ALL THREE | r < 0.25 for all observables tested |
| 8 | Field profile = log(R/r) | Steeper on finite grid (f/log ratio 0.04-0.15) |

## Open Frontiers (ranked by expected value)

### 1. Decoherence scaling problem (THE open frontier)
Two-register decoherence is universal (0/20 pure) but purity INCREASES with graph size (0.57→0.89 from 6→25 layers). Both node-label and cumulative-action env architectures have wrong scaling. Path multiplicity makes both slits equivalent through mass on large graphs. Need: continuous (infinite-dim) environment or qualitatively different architecture. **This is the model's sharpest remaining problem.** Effort: theoretical work + new implementation.

### 2. Density matrix as diagnostic (DONE)
Purity Tr(ρ²) is the best predictor (r=-0.40) of decoherence outcome. Mean purity=0.80 at 12 layers. Most seeds decohere sub-threshold. V_drop threshold (0.02) misses widespread weak decoherence.

### 3. Integrate with Codex pattern-sourced mover results
Codex's mover/steering experiments test whether persistent patterns steer amplitude at the CA level. Our corrected propagator tests the same question at the path-sum level. Cross-comparison could unify the two investigation threads. **Effort: 1-2 experiments.**

### 4. Decoherence on rectangular lattice
All two-register tests were on generated DAGs. Does the mechanism work on the regular lattice? The lattice has perfect symmetry which might prevent slit-selective env coupling. **Effort: 1 experiment, quick.**

### 5. Higher-dimensional graphs
All tests used 2D-like graphs. A 3D graph would have 1/r field (not log) and different path diversity. Would the corrected propagator give 1/r distance scaling and F∝M in 3D? **Effort: moderate, needs new graph generator.**

## Model Architecture (final)

```
UNITARY SECTOR (solved)
  Propagator: exp(i*k*S_spent) / L^p
  S = delay - sqrt(delay² - L²)  [spent-delay action]
  delay = L * (1 + field)         [field from Laplacian relaxation]
  → Gravity (phase valley) + Interference (path-sum coherence)

NON-UNITARY SECTOR (partially solved)
  Two-register: system × environment
  env = last mass node index (fine-grained)
  Partial trace: P(det) = Σ_env |ψ(det,env)|²
  → Decoherence (40% at optimal geometry)
  Requires: mass in post-barrier layer, traversable by slit paths
```
