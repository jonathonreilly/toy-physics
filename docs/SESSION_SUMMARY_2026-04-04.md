# Session Summary: 2026-04-04

**Duration:** Full day session (208 commits)
**Focus:** Continuum limit, dimension-dependent kernel, valley-linear action, Newton derivation, tier-2 search

## Headline Results

### 1. Dimension-dependent kernel: 1/L^(d-1)
The propagation kernel must match the spatial dimension:
- 2D: 1/L, 3D: 1/L², 4D: 1/L³
- Selected by gravity PERSISTENCE: only p=d-1 gives TOWARD gravity
  that strengthens with lattice length
- Transfer norm: p=d-1 is logarithmically marginal (boundary between
  "beam too spread" and "amplitude overflows")
- Confirmed across 2D, 3D, 4D with h^(d-1) measure factor

### 2. Valley-linear action: S = L(1-f) → Newtonian gravity
- F∝M = 1.00 (exact, verified across all parameters)
- Distance tail ≈ b^(-1.0) (near-Newtonian, confirmed at W=12)
- Born: machine precision for ALL actions
- Decoherence: 50%, action-independent (exact identity proven)
- Robust: all W (4-12), max_d (1-3), L (8-18), h (0.5-0.25)

### 3. F∝M = p universality class
For action S = L(1-f^p): F∝M = p exactly.
| p | F∝M | Distance tail |
|---|-----|---------------|
| 0.5 | 0.50 | -0.82 |
| 1.0 | 1.00 | -1.08 |
| 1.5 | 1.50 | -2.06 |
| 2.0 | 2.00 | -3.00 |

### 4. Momentum conservation selects p=1
Two-body test: valley-linear (p=1) conserves momentum to 0.0%.
Spent-delay (p≈0.5) violates by 42-55%. Verified on 10 configurations.

### 5. Newton derivation (bounded)
Chain: linear propagator → Born → additive mass → m=s → p=1 → Newton.
Still open: persistent-pattern inertial mass (the weakest link).

### 6. Gravity is universal across graph structures
Gravity survives: 70% edge deletion, asymmetric connectivity, random
positions, sparse NN connectivity. Only REQUIRED: field coupling + phase.
Newton (p=1) is the MOST ROBUST universality class under graph damage.

### 7. Action crossover
Spent-delay wins on random graphs, valley-linear wins on regular.
Crossover at regularity ~0.3. NOT renormalization — signal-to-noise +
saturation difference.

### 8. Gravitational diffraction at Nyquist
Gravity reverses at k = π/h (exact to 0.5%), field-independent.
A lattice property (moves with h), not a continuum prediction.

### 9. BMV gravitational entanglement
First lattice computation: entanglement ∝ s² (exact, matches BMV).
Separation dependence converges toward continuum (not a discrete prediction).

### 10. Same-family 3D closure
All 10 properties at h=0.25, W=10, valley-linear, 1/L². No companions needed.

## Honest Corrections Made During Session

- 3D 1/L gravity: RETRACTED (lattice artifact at h=0.5)
- Distance tail steepening: CORRECTED (shallows at matched width)
- Near-field z_peak: NOT gravitational radius (z_peak ∝ L, beam optics)
- EP derivation: CIRCULAR without additivity argument
- Self-gravity Born: GENERIC nonlinearity (saturates at all g)
- Topological gravity: CONDUCTANCE BIAS (already known)
- Gravity-EM interference: ZERO (0.2%, as in standard physics)
- d=3 special: NO (2D is better by most metrics)
- BMV separation exponent: CONVERGES to continuum (not discrete prediction)

## Tier Assessment

**Tier 3 (solid computational paper):** universality classes, momentum
conservation, dimensional kernel selection, same-family closure.

**Tier 2 boundary:** the combined universality statement (gravity is
generic on causal networks, Newton is the most robust force law) is
novel but requires external physicist validation to assess impact.

**Not tier 2:** no single result is individually surprising enough for
the "I didn't know that was possible" reaction.

## Scripts on Main

20+ new scripts including:
- `dimensional_gravity_card.py` — canonical d-dimensional card
- `lattice_3d_valley_linear_card.py` — same-family 10-property card
- `valley_linear_robustness_sweep.py` — parameter sweeps
- `action_crossover_sweep.py` — regularity crossover
- `two_body_momentum_harness.py` — momentum conservation test
- `transfer_norm_and_born.py` — kernel selection theory

## Open Problems

1. **Gate B (dynamics):** grown geometry gives 67-92% TOWARD on v6 replay.
   Near-field parameter sensitivity, not growth-rule failure.
2. **Persistent-pattern inertial mass:** the weakest link in the Newton
   derivation. Codex is exploring mesoscopic surrogate sources.
3. **4D distance law:** needs wider lattice (W≥10 in 4D, ~3M nodes).
4. **The tier-2 breakthrough:** 12 candidates tested, none individually
   sufficient. The universality statement is the strongest candidate.
