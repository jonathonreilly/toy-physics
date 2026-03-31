# Frontier Map: 2026-03-31 (Session Close)

## Session Summary
- **56 experiments** over one extended session
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

### 1. Increase decoherence rate beyond 40%
The two-register mechanism works but is geometry-sensitive. Can we find a configuration with D > 50% and G > 80%? Candidates: vary n_layers, y_range, mass size, try multiple mass clusters. **Effort: 1-2 experiments.**

### 2. Why is decoherence phase-emergent?
The ALL THREE outcome isn't predicted by structure (r < 0.25). Understanding WHY specific graph realizations decohere while others don't would be a theoretical advance. Candidate: compute the full density matrix at the detector and identify which matrix elements determine the outcome. **Effort: 1 experiment, moderate complexity.**

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
