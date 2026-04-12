# Reviewer-Facing Summary

**Date:** 2026-04-02
**Purpose:** One-page framing of what the project currently is and is not.

## What the project is

A **discrete event-network toy model** that explores whether path-sum
amplitude propagation on causal directed acyclic graphs can produce
gravity-like deflection, quantum-like interference, Born rule compliance,
and environment-mediated decoherence from a single propagator.

The model is best described as **toy mechanism science** — it does not
claim to derive real physics, but it systematically tests which toy-level
phenomena emerge from which architectural ingredients.

## What works (retained results)

| Phenomenon | Evidence | Confidence |
|---|---|---|
| Gravity (phase valley) | Deflection toward mass, k=0→zero, correct sign | HIGH |
| Born rule | I_3/P = 3e-16 on chokepoint DAGs | HIGH (mathematical) |
| CL bath decoherence | pur_cl stable ~0.85-0.95 on modular 3D/4D | HIGH on modular |
| Cross-family gravity | 4 of 5 3D graph families | HIGH |
| 3D mass scaling | Alpha converges to ~0.58 with density | HIGH |
| Dimensional progression | Alpha increases: 2D→3D→4D | MEDIUM (4D parameter-sensitive) |

## What doesn't work (structural limitations)

| Limitation | Status | What was tested |
|---|---|---|
| Distance scaling (1/b) | Structural — no rescue | 9+ avenues including propagator power, locality shells, lattice, causal field, nonlinear phase, edge reweighting |
| Asymptotic emergence | Bounded to N=80 | Pruning, adaptive quantile, birth/death, connectivity guard |
| 4D mass exponent | Parameter-sensitive | Gap × density sweep, doesn't converge |
| Strict visibility gain | Vanishes at large N | Single-vs-double-slit metric |

## Key diagnostic tools developed

- **k=0 control**: Separates phase-mediated gravity from trivial amplitude bias. Any future mechanism must pass this.
- **Fixed-mass-position control**: Prevents mass-selection confounds in b-sweep and alpha measurements. Three confounds caught and retracted.
- **Chokepoint barrier**: Required for Born rule tests on random DAGs (skip-layer bypass discovered and fixed).

## What distinguishes this from simpler models

1. Gravity requires k > 0 (phase, not amplitude routing)
2. Decoherence requires bin-resolved bath contrast (not random dephasing)
3. Hub concentration kills gravity (path diversity required)
4. Mass scaling depends on spatial dimension (not trivially flat)

## What the project does NOT claim

- It does not derive gravity or quantum mechanics from first principles
- It does not produce distance-dependent gravitational force
- It does not have a fully satisfying evolving-network dynamics
- It does not transfer all results beyond the modular DAG family
- The 4D "F~M" mass scaling is parameter-specific, not a universal exponent

## Current priority frontier

1. **Evolving-network dynamics** — the deepest remaining gap between axioms and implementation. All tested local rules (9+ variants including pruning, birth/death, connectivity-aware) are bounded. The next serious approach requires qualitatively different dynamics.

2. **Continuum bridge** — 3D alpha converges (0.58), 4D doesn't. Separating finite-size artifacts from retained structure is documented but incomplete.

3. **Cross-family transfer** — gravity and decoherence work on 4 of 5 3D families. 4D gravity doesn't transfer beyond modular.

## Repository integrity

- 3 claims retracted during this investigation (causal field 1/b, alpha=(d-1)/2, pruning alpha boost)
- All retractions documented with root cause analysis
- Fixed-mass and k=0 controls are now permanent requirements
- PREDICTION_CARD.md lists 5 explicit falsification criteria

## Known remaining confounds (flagged by review workers)

- Hierarchical alpha=0.71 is exploratory (mass-position confounded)
- Smart-prune vs adaptive-quantile comparison is trivial (same function)
- Mass scaling on pruned graphs is not fixed-position clean
- Modular-special predictor scan uses positive-only truncated fits

These are documented here rather than promoted as retained results.
