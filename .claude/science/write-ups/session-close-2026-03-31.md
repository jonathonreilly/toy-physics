# Session Close: 2026-03-31

**66 experiments, 50+ scripts, one extended session**

## What the model does (confirmed across 2D and 3D)

1. **Gravitational attraction** from phase structure (90%, corrected propagator 1/L^p)
2. **Interference fringes** from path-sum coherence (100%, V=0.995)
3. **Born rule** preserved (I₃ = 4.28e-15)
4. **Both emerge during growth** at 6-8 layers
5. **Gravity is pure phase** (k=0 → exactly zero shift)
6. **Phase valley mechanism** analytically derived (ΔS ≈ -L√(2f), shift ∝ k²)
7. **Endogenous decoherence** via two-register env (universal on irregular DAGs, mean purity 0.80)

## What the model doesn't do (confirmed across architectures)

1. **1/r distance scaling**: deflection is b-independent in both 2D and 3D
2. **F∝M mass scaling**: deflection is mass-independent (threshold effect)
3. **Decoherence that scales with graph size**: purity increases from 0.57 to 0.89 as graphs grow (5 architectures tested, all wrong-scaling)
4. **Decoherence on regular lattices**: purity=1.0 (symmetry blocks slit selectivity)

## Root cause of both scaling failures

The path-sum on growing/dense graphs averages over exponentially many paths. This averaging:
- **Helps** gravity sign and interference (constructive/destructive interference is robust to path averaging)
- **Hurts** gravity scaling (b-dependent action asymmetry averages out)
- **Hurts** decoherence scaling (slit-selective env labels get shared across paths)

The model's physics is **qualitatively correct** (right phenomena, right signs, right emergence pattern) but **quantitatively threshold-like** (doesn't scale with mass, distance, or graph size the way real gravity and decoherence do).

## Model architecture (final)

```
PROPAGATOR: exp(i*k*S_spent) / L^p
  S = delay - sqrt(delay² - L²)
  delay = L × (1 + field)
  field from Laplacian relaxation at persistent nodes

  → Gravity (phase valley, threshold deflection)
  → Interference (path-sum coherence)
  → Born rule (linear propagation)

TWO-REGISTER ENVIRONMENT (optional, on irregular DAGs):
  env = last mass node index
  P(det) = Σ_env |ψ(det,env)|²
  → Decoherence (universal but wrong-scaling)

GRAPH REQUIREMENTS:
  - Irregular (for decoherence)
  - Connected (deg ≥ 3, for interference + gravity)
  - Grown from simple rules (Axiom 1)
```

## For the next session

The model is at a **theoretical junction**, not an experimental one. More experiments will confirm the same patterns. The next advance needs:

1. **A propagator that gives 1/r scaling**: the current `1/L^p` gives threshold deflection because the phase valley depth saturates. A propagator where the phase effect grows with distance through the field could fix this.

2. **An environment that grows exponentially**: the current node-label env grows linearly with graph size while path multiplicity grows exponentially. Tensor-product env structure (each mass interaction multiplies env dimension by 2) could fix the decoherence scaling.

3. **Theoretical analysis**: derive why the phase valley produces threshold deflection analytically, and identify what modification would give power-law scaling.

These are theory questions, not parameter sweeps.
