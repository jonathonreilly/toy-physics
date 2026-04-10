# Chiral Walk Architecture — Complete Synthesis

**Date:** 2026-04-09
**Status:** Overnight synthesis. See `CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md` for the narrowed 3+1D status.

> Update 2026-04-10: the overnight 1+1D and 2+1D results still stand, and the
> 3+1D closure card at its tested operating point still stands, but the later
> like-for-like 3+1D periodic sweep shows a TOWARD basin with genuine sign
> windows, not a universal sign-stable 3+1D gravity law.

## The Architecture

A discrete chiral quantum walk where each lattice site has 2d
chirality components (d = spatial dimensions). Per layer:

1. **Coin:** Independent 2×2 symmetric unitaries on each chirality pair
   C = [[cos θ, i·sin θ], [i·sin θ, cos θ]]
   Lorentzian gravity: θ(r) = θ₀(1 - f(r))

2. **Shift:** Each chirality moves one step in its direction (permutation)

## What This Produces

### Overnight operating-point positives:

| Property | 1+1D | 2+1D | 3+1D |
|----------|------|------|------|
| Closure card | 10/10 | 10/10 | 10/10 |
| Born |I₃|/P | 3.3e-16 | 0 (exact) | 0.056 |
| F∝M | 1.000 | 0.992 | 1.000 (R²=1.0) |
| Gravity | TOWARD | TOWARD | TOWARD basin* |
| Norm | exact | exact | exact |
| Light cone | v=1.0 | — | — |
| Decoherence | 38.6% | 82.8% | PASS |

\* The 3+1D closure card operating point remained positive, but the later
  addendum narrows the global 3+1D claim to a TOWARD basin with genuine
  periodic sign windows.

### Klein-Gordon dispersion (1+1D):
  cos(E) = cos(θ)·cos(k)
  → E² = θ² + k² for small θ, k
  → Mass = θ (coin angle), speed of light = 1
  → R² > 0.99999 (Klein-Gordon vs Schrödinger)

### 2+1D approximate Klein-Gordon:
  R² > 0.999 for factorized and SO(4) coins
  Isotropic along axes, anisotropic on diagonal (lattice effect)

### Gauge connections:
  U(1): pure gauge invariance (2.8e-16)
  Aharonov-Bohm: V=88.5%, cos(2A) modulation
  Wilson loop: cos(Φ), R²=1.0
  SU(2): fails on chirality index (needs color DOF)

### Spin-like chirality:
  Not conserved (oscillates, [H,C]≠0)
  Stern-Gerlach separation detected (gradient enhances ψ₊/ψ₋ split)
  Chirality-dependent gravity (ψ₊ deflects 2× more than ψ₋)
  Precession under uniform field

### Causal set:
  Valid partial order, metric recovery r=0.956
  Strict light-cone propagation (max spread within v=1 cone)

### Distance law:
  1+1D: α=-0.60, 15/15 TOWARD on wide lattice
  3+1D: α=-0.56, 6/7 TOWARD (R²=0.90)
  Not Newtonian (-1.0). Softened by beam spreading (~d^0.5)

### Convergence (overnight view; narrowed later):
  The overnight sweep suggested a substantial TOWARD basin in 3+1D periodic
  chiral transport.
  The later addendum shows genuine AWAY windows that survive in coherent,
  classical, and phase-kill runs on the same periodic architecture.
  So 3+1D should be read as a retained basin and operating-point success,
  not as a universal sign-stable regime.

### Superposition:
  1+1D: 0.17% on adequate lattice
  2+1D: 0.10%
  (3+1D not yet tested on chiral)

## What Doesn't Work Yet

### Dynamic growth:
  Transfer matrix growth works (Born 4.3e-17, self-regulating)
  Chiral walk growth is unstable (threshold pruning + chiral
  asymmetry creates collapse regardless of coin design)
  Needs a fundamentally different growth approach

### Cosmological expansion:
  Expanding lattice doesn't stretch separation (walk too localized)

### Distance law exponent:
  α ≈ -0.6, not -1.0 (Newtonian). Beam spreading softens the falloff.
  May improve with better coupling or continuum limit.

### Dimensional preference:
  No clean preferred dimension. Gravity magnitude decreases with d.
  2+1D can flip AWAY at some parameters (lattice-size effect).

## The F∝M Mechanism (explained)

Phase coupling: |e^{ikf}|² = 1 → zero first-order probability shift → F∝M²
Theta coupling: sin²(θ(1-f)) has linear f-dependence → F∝M=1.0

The coin angle θ directly modulates transition probability. The field
enters through the AMPLITUDE of mixing, not just the phase. This is
why F∝M=1.0 is exact: the centroid shift is proportional to the
first-order probability perturbation, which is linear in f.

## The Gravity Mechanism (from first principles)

Axiom 8: "Gravity is natural continuation in a distorted continuation structure."

The Lorentzian θ-coupling: θ(r) = θ₀(1-f(r))
  Near mass: θ decreases → less chirality mixing → walk is more forward-directed
  Far from mass: θ = θ₀ → normal mixing

This creates a "refractive index" gradient: the walk is faster/straighter
near mass (less scattering), pulling the probability centroid TOWARD mass.

At fixed θ, the coupling is k-independent. That resolves the transfer matrix's
k-dependent resonance problem in 1+1D, but it does not by itself guarantee a
universal sign-stable 3+1D periodic regime.

## Connection to Known Physics

The 1+1D chiral walk is equivalent to the Feynman checkerboard / Dirac
quantum walk. What's NEW:

1. Gravitational coupling via θ-modulation (not in the literature)
2. F∝M=1.0 from amplitude coupling (new mechanism)
3. 10/10 closure card across 3 spacetime dimensions (new validation)
4. The connection to the axiom chain (Axiom 6 → kernel, Axiom 8 → gravity)
5. Klein-Gordon + gravity + Born + gauge in one framework
