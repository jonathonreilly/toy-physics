# Derivation: Newton's Law from Two Principles + One Separation

## Date
2026-04-04

## Claim
Newton's law is the unique gravity in the model, given:
1. Linear propagator (Born rule)
2. Phase-valley interaction (gravitational attraction)
Plus the SEPARATION PRINCIPLE: mass is a property of the particle,
not the propagator.

## The argument

### Step 1: Linear propagator → Born + EP
The propagator ψ_out = M ψ_in is linear. This gives:
- Born rule (I₃ = 0 for any action)
- Equivalence principle (centroid shift is amplitude-independent)

### Step 2: Phase valley → TOWARD gravity
Action S = L × g(f) with g'(0) < 0 gives constructive interference
on the mass side → centroid shifts TOWARD mass.

### Step 3: The universality law
With S = L(1-f^p), the deflection scales as s^p where s is the
field coupling. Therefore F ∝ M^p (verified for p = 0.5 to 2.0).

### Step 4: Two-body momentum
Particle A (coupling s_A) deflects B by ∝ s_A^p.
Particle B (coupling s_B) deflects A by ∝ s_B^p.

Define momentum: p = m × centroid_shift, where m = s^α.
Conservation requires: s_A^α × s_B^p = s_B^α × s_A^p → α = p.

### Step 5: The separation principle
m = s^p makes mass depend on the action power p. But mass is a
property of the PARTICLE (determined by its field coupling s),
not a property of the PROPAGATOR (which determines p).

Requiring mass to be action-independent: m = f(s) where f does
not reference p. The simplest: m = s (i.e., α = 1).

With α = 1: conservation gives p = 1.

### Step 6: Conclusion
p = 1 → F ∝ M₁M₂/r^(d-2) → Newton's law.

## The two principles + one separation

1. **Linear propagator**: gives Born rule + equivalence principle
2. **Phase valley**: gives gravitational attraction + F ∝ M^p
3. **Separation**: mass is action-independent → m = s → p = 1

Newton = linear propagator + phase valley + mass-action separation.

## Honest assessment

The separation principle is the weakest link. It says: "the mass
of a particle shouldn't depend on how we compute its trajectory."
This is physically compelling but not mathematically forced.

If we accept it: Newton is derived from two physical principles
(linearity + attraction) and one ontological principle (particle
properties are independent of propagator properties).

If we don't accept it: p is a free parameter and Newton is a
choice, not a derivation.

## Numerical verification

| Test | Result |
|------|--------|
| F∝M = p (exact) | p = 0.50, 0.75, 1.00, 1.50, 2.00 |
| Momentum (valley, m=s) | conserved 0.0% |
| Momentum (spent, m=s) | violated 38.9% |
| Momentum (p=2, m=s²) | conserved |
| Born (all actions) | < 5e-15 |
| EP (point particles) | exact |
| EP (extended states) | position-dependent (expected) |

## Status
PROPOSED — the separation principle is physically motivated but
not logically forced. The numerical evidence is clean.
