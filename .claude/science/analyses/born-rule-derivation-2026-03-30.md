# Analysis: Born Rule Derivation Test

## Date
2026-03-30

## Key Finding: Born rule IS derived, but from three assumptions that ARE put in

### What the model assumes:
1. Complex amplitudes (e^(i*k*action) phase accumulation)
2. Linear propagation (amplitudes add at each node)
3. Reversibility (unitary mixing at beam-splitter-like junctions)

### What follows:
- The 2-norm |ψ|² is the UNIQUE p-norm preserved by ALL unitary transformations
- Verified: p=2 preserved by 6/6 test transforms (Hadamard, rotations, phase shifts, beam splitters)
- Every other p (0.5, 1, 1.5, 2.5, 3, 4, 5, 6) breaks under at least one transform
- Therefore |ψ|² probability is a CONSEQUENCE, not an additional assumption

### What's still put in:
- WHY complex? Real amplitudes preserve the 2-norm too, but can't produce continuous phase → no smooth interference fringes
- WHY linear? Nonlinear propagation could preserve different norms
- WHY reversible? Dissipative propagation doesn't preserve any norm

### The honest accounting:

| Feature | Status |
|---------|--------|
| Born rule (|ψ|²) | DERIVED from linearity + reversibility |
| Interference fringes | DERIVED from complex amplitudes + path-sum |
| Complex amplitudes | ASSUMED (enables continuous phase) |
| Linear propagation | ASSUMED (amplitude superposition) |
| Reversibility | ASSUMED (unitary edge weights) |
| Gravity = Laplacian | ASSUMED (field relaxation rule) |
| Action = spent delay | ASSUMED (proper-time deficit formula) |

## Significance
The external reviewer was partly right and partly wrong. The Born rule IS derivable from the model's structure — it's not a separate assumption. But the INPUTS to that derivation (complex linear reversible amplitudes) are themselves assumptions that the model doesn't derive from anything deeper. The model reduces the assumption count by one (no separate Born rule needed) but doesn't reach rock bottom.

The deepest remaining question: can complex amplitudes + linearity be derived from the network structure? This would require showing that the discrete causal DAG naturally selects complex-linear propagation over alternatives — a much harder problem.
