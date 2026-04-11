# Born Rule Negative — What It Teaches

**Date:** 2026-04-11

## The Result
Self-consistent gravity does NOT select α=2 (Born rule). Lower α is
more stable. The test measured Banach fixed-point convergence of the
Hartree iteration, not anything about quantum measurement.

## Why It Failed (Complete Diagnosis)

The Hartree loop maps ψ → V(|ψ|^α) → H(V) → ψ'. The contraction rate
depends on the Lipschitz constant of |ψ|^α as a source term:
- α < 2: sublinear → smoother source → faster convergence (trivially)
- α = 2: Born rule → standard density
- α > 2: superlinear → rougher source → slower convergence

This is a theorem about elliptic PDE fixed-point iteration. The
Lyapunov ranking α=1.0 < 1.5 < 2.0 < 3.0 < 4.0 is the textbook
Banach contraction mapping answer.

## The Deep Reason

The Born rule is a MEASUREMENT postulate (interface between quantum
state and classical observables). Gravitational self-consistency is a
DYNAMICS statement (how ψ and Φ co-evolve). These are different levels
of the theoretical stack:
- Dynamics: deterministic, unitary
- Measurement: probabilistic, non-unitary

Unitary dynamics cannot distinguish α values because it preserves the
entire function |ψ(x)| up to phases. The loop never performs a
measurement — it never asks "what is the probability of finding the
particle at x?"

## What This Means for the Model

The model is a theory of QUANTUM GEOMETRY, not QUANTUM MEASUREMENT.
Spectral results (area law, CDT flow, sign selectivity) depend on the
spectrum of H, which exists regardless of the probability measure.
Trajectory results (Penrose, DP, BH) depend on the Born rule through
the density matrix formalism — they need additional structure.

## Implications

- Gravity and quantum probability are LOGICALLY INDEPENDENT at the
  axiomatic level (confirming the standard physics intuition)
- Spectral results are ROBUST: they hold for any α
- To get measurement-level physics, need: many-body + environment +
  decoherence → ask if the resulting mixed-state dynamics is α-sensitive
- The spectral-trajectory hierarchy is not a failure — it correctly
  identifies what gravitational self-consistency can explain
