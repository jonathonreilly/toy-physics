# Derivation: Newton's law from three axioms

## Date
2026-04-04

## Target
Derive p=1 (Newtonian gravity) from the model's axioms, rather
than selecting it as a free parameter.

## Axioms Used
1. Linear propagator (amplitude at node = linear sum of contributions)
2. Phase valley (action decreases near mass → TOWARD gravity)
3. Action-reaction symmetry (force of A on B = force of B on A)

## Derivation

### Step 1: Linear propagator gives Born rule
The propagator ψ_j = Σ K(i→j) ψ_i is linear. This gives the
Sorkin test I_3 = 0 (Born rule) for ANY action formula. Born does
not constrain p.

### Step 2: Phase valley gives TOWARD gravity
The action S = L × g(f) with g'(0) < 0 creates a phase deficit
near mass. This produces constructive interference on the mass
side → centroid shifts TOWARD mass. The sign of gravity is
determined by g'(0) < 0, not by the specific form of g.

### Step 3: Action S = L(1-f^p) gives F ∝ M^p
The deflection of a test particle in the field of mass M_A is
proportional to M_A^p (from the phase integral of f^p ∝ (M_A/r)^p).
This was verified numerically: p=0.5 gives F∝M^0.5, p=1 gives
F∝M^1, p=2 gives F∝M^2.

### Step 4: Action-reaction forces p = 1
Consider two masses M_A and M_B separated by distance r.

The FORCE on B from A (= B's inertial mass × deflection from A's field):
  F_{A→B} = M_B × M_A^p × g(r)

The FORCE on A from B (= A's inertial mass × deflection from B's field):
  F_{B→A} = M_A × M_B^p × g(r)

Action-reaction symmetry: F_{A→B} = F_{B→A} for all M_A, M_B.
  M_B × M_A^p = M_A × M_B^p
  (M_A / M_B)^{p-1} = 1

This holds for ALL mass ratios only if p-1 = 0, i.e., **p = 1**.

### Step 5: p = 1 gives Newtonian gravity
With p = 1: F ∝ M_A × M_B / r (on 3D lattice with 1/r field).
The distance law deflection ∝ 1/b follows from the phase integral
(derived separately). Combined:

  **F = G × M_A × M_B / r²** (in 3+1D)

where G is determined by the field coupling constant s and the
wave number k.

## Novel Prediction
The model predicts that ANY system with:
  (a) linear amplitude propagation
  (b) phase-mediated interaction (action depends on a field)
  (c) action-reaction symmetry between interacting particles

MUST produce Newtonian gravity. There is no other option.

Conversely: a non-Newtonian force law (p ≠ 1) requires either
violating Born rule, or violating action-reaction, or having
the interaction NOT be phase-mediated.

## Weakest Link
Step 4 assumes that the "inertial mass" (resistance to deflection)
is the same quantity as the "gravitational mass" (source of field).
This is the equivalence principle. In the model, both are determined
by the field coupling constant s: the same s that creates the field
also determines how much the particle deflects in another field.

If gravitational and inertial mass could differ, p ≠ 1 would be
possible even with action-reaction. The derivation assumes
equivalence principle, which is itself an axiom (not derived).

A more honest statement: action-reaction + equivalence principle
→ p = 1. The equivalence principle is assumed, not derived.

## Status
PROPOSED — the argument is clean but the equivalence principle
assumption needs to be explicitly stated as an axiom.
