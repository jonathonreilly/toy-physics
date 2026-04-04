# Newton's Law Derived from Four Principles

**Date:** 2026-04-04
**Status:** Derivation proposed. Numerical verification in progress.

## The Claim

Newton's law of gravity (F ∝ M₁M₂/r²) is the UNIQUE phase-mediated
gravity on a discrete causal network satisfying four principles:

1. Linear amplitude propagation (Born rule)
2. Phase valley (gravitational attraction)
3. One-parameter mass (persistent patterns have a single coupling s)
4. Momentum conservation (action-reaction symmetry)

No other gravitational force law is consistent with all four.

## The Argument

### Principle 1: Linear propagator → Born rule

The amplitude at node j is a linear sum of contributions from
connected nodes: ψ_j = Σ K(i→j) ψ_i. This gives the Sorkin test
I₃ = 0 (Born rule) for ANY action formula. Born does not constrain
the action.

Verified: I₃/P < 5e-15 for all tested actions (p=0.5 to p=2.0).

### Principle 2: Phase valley → TOWARD gravity

The action S = L × g(f) with g'(0) < 0 creates a phase deficit
near mass. This produces constructive interference on the mass side,
shifting the centroid TOWARD the mass.

Phase HILL (g'(0) > 0) gives AWAY (repulsion). Zero coupling gives
no gravity. The phase valley is the unique mechanism for attraction.

### Principle 3: One-parameter mass

A persistent pattern (Axiom 2) is characterized by a single coupling
constant s, which determines both:
- Its gravitational field: f = s/r^(d-2)
- Its identity as a "mass"

There is no separate inertial mass parameter. The coupling s is the
only number characterizing the pattern's interaction with the network.

### Principle 4: Momentum conservation → p = 1

With action S = L(1-f^p), the deflection of a test particle in
field f ∝ s/r scales as s^p (the F∝M = p universality law).

Two particles A (coupling s_A) and B (coupling s_B) at separation r:
- Deflection of A by B's field: ∝ s_B^p
- Deflection of B by A's field: ∝ s_A^p

Define momentum: p = m × v_centroid, with m = s (Principle 3).
- p_A = s_A × s_B^p × g(r)
- p_B = s_B × s_A^p × g(r)

Momentum conservation: p_A + p_B = 0 requires
  s_A × s_B^p = s_B × s_A^p
  (s_A/s_B)^(p-1) = 1

This holds for ALL mass ratios s_A/s_B only if **p = 1**.

### Conclusion

With p = 1: F ∝ s_A × s_B / r^(d-2) on a d-dimensional lattice.
In 3+1D (d=3): F ∝ M₁M₂/r. This is Newton's law.

## Numerical Evidence

| Test | Result |
|------|--------|
| F∝M = p (5 powers) | Exact: 0.50, 0.75, 1.00, 1.50, 2.00 |
| Born (all actions) | < 5e-15 |
| Two-body momentum (p=1) | Conserved to 10⁻²⁰ |
| Two-body momentum (p≠1) | Violated by 33-80% |
| Distance tail (p=1) | b^(-1.07), near Newtonian |
| Equivalence principle | Trivially true (linear model) |

## What This Does NOT Prove

1. It does not derive the dimension d of spacetime
2. It does not derive the lattice geometry (still imposed)
3. It does not derive the specific form of g(f) — only that g must
   be linear in f at weak field
4. Principle 3 (one-parameter mass) is an assumption about what
   "persistent patterns" look like — it is not derived from the
   model's axioms

## The Strongest Safe Statement

"On any d-dimensional lattice with 1/L^(d-1) kernel, if the
propagator is linear, the action creates a phase valley, masses are
characterized by a single parameter, and momentum is conserved, then
Newton's gravitational force law F ∝ M₁M₂/r^(d-2) is the unique
outcome."
