# Newton's Law Derived from Four Principles

**Date:** 2026-04-04
**Status:** bounded derivation candidate. Additivity now strengthens Principle 3, but persistent-pattern inertia remains open.

## The Claim

The strongest bounded claim currently supported is:

on the retained ordered-lattice family, Newtonian mass scaling is selected when
all of the following hold together:

1. Linear amplitude propagation (Born rule)
2. Phase valley (gravitational attraction)
3. Additive one-parameter mass (`m ∝ s` under the same composition law)
4. Momentum conservation (action-reaction symmetry)

The open step is still whether Principle 3 can be made real for persistent
patterns rather than only for the current test-particle/composition harnesses.

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

### Principle 3: Additivity / one-parameter mass

The weakest step is still the identification of the field-source parameter
with the inertial quantity that weights momentum.

What is now frozen:

- the dedicated equivalence harness shows that global amplitude scaling cancels
  exactly in the centroid ratio on the linear test-particle family
- but localized packet shape still changes the response strongly
- the dedicated composite-source harness shows that, on the same weak-field
  test-particle family, valley-linear source composition is additive while
  spent-delay is not

Artifact chains:

- [`scripts/equivalence_principle_harness.py`](/Users/jonreilly/Projects/Physics/scripts/equivalence_principle_harness.py)
- [`logs/2026-04-04-equivalence-principle-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-equivalence-principle-harness.txt)
- [`docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md)
- [`scripts/composite_source_additivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_harness.py)
- [`logs/2026-04-04-composite-source-additivity-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-composite-source-additivity-harness.txt)
- [`docs/COMPOSITE_SOURCE_ADDITIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPOSITE_SOURCE_ADDITIVITY_NOTE.md)

This is enough for a stronger bounded statement:

- if the inertial quantity of a persistent pattern is an extensive quantity
  attached to the same composition law as the field-source parameter `s`,
  then `m ∝ s`

What is still missing is a persistent-pattern or quasi-persistent localized
state whose inertial response can actually be measured on the lattice.

So Principle 3 is **stronger than a bare assumption**, but it is still **not
closed** by the current code.

### Principle 4: Momentum conservation → p = 1

With action S = L(1-f^p), the deflection of a test particle in
field f ∝ s/r scales as s^p (the F∝M = p universality law).

Two particles A (coupling s_A) and B (coupling s_B) at separation r:
- Deflection of A by B's field: ∝ s_B^p
- Deflection of B by A's field: ∝ s_A^p

Define momentum: p = m × v_centroid, with `m ∝ s` under Principle 3.
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
| Two-body momentum (`m ∝ s`) | Valley-linear conserved to `0.0-0.1%`; spent-delay violated by `42-55%` at unequal masses |
| Distance tail (p=1) | b^(-1.07), near Newtonian |
| Amplitude-level equivalence | Exact under global amplitude rescaling |
| Packet-shape independence | Fails on the bounded localized-packet probe |
| Valley same-site / disjoint additivity | Exact to printed precision on the weak-field test-particle family |
| Spent-delay same-site / disjoint additivity | Violated by 24-29% on the same family |

## What This Does NOT Prove

1. It does not derive the dimension d of spacetime
2. It does not derive the lattice geometry (still imposed)
3. It does not derive the specific form of g(f) — only that g must
   be linear in f at weak field
4. Principle 3 is stronger than before because additivity now supports
   `m ∝ s` on the weak-field test-particle family, but it is still not a
   derived persistent-pattern theorem
5. The current equivalence and additivity harnesses only close the
   test-particle response statement; they do not yet produce a
   persistent-pattern inertial mass

## The Strongest Safe Statement

"On the retained ordered-lattice family, if the propagator is linear, the
action creates a phase valley, the inertial quantity is extensive under the
same composition law as the field-source parameter, and momentum is conserved,
then `p = 1` is selected and the Newtonian mass-scaling law follows. The open
step in the current project is still the persistent-pattern version of that
extensive one-parameter mass principle."
