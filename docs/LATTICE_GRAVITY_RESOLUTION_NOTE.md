# Lattice Gravity Resolution: Ultra-Weak Field Gives Both Attraction AND 1/b

**Date:** 2026-04-04
**Status:** 2D resolved. 3D reopened on a bounded dense-lattice branch.

## The breakthrough

The gravity-toward vs distance-law "structural trade-off" was WRONG.
The 2D dense lattice with the ORIGINAL spent-delay action achieves
BOTH attraction AND distance law at ultra-weak field strength (0.0005).

The issue was always field strength:
  - strength=0.1: beam depletion dominates → centroid AWAY
  - strength=0.001: still depletion → AWAY
  - strength=0.0005: linear response dominates → centroid TOWARD + 1/b

## 2D dense lattice card (spent-delay, strength=0.0005)

| b | centroid shift | direction |
|---|---------------|-----------|
| 4 | +0.141 | TOWARD |
| 5 | +0.157 | TOWARD |
| 6 | +0.168 | TOWARD (peak) |
| 7 | +0.162 | TOWARD |
| 8 | +0.141 | TOWARD |
| 10 | +0.089 | TOWARD |
| 13 | +0.074 | TOWARD |
| 16 | +0.071 | TOWARD |
| 19 | +0.063 | TOWARD |

Distance law: b^(-0.94), R²=0.939

ALL 9/9 tested b values show TOWARD. No axiom fork needed.

Combined with prior results on the same lattice:
  Born: machine precision (verified)
  k=0: exactly zero (verified)
  MI: 0.57 bits (verified)
  d_TV: 0.79 (verified)
  Decoherence: 44% (verified)

## 3D status

The old fully negative 3D read is no longer the whole story.

What remains true:

- 3D NN lattice (`9` edges/node) stayed away on the earlier tested slice
- strong-field and action-power ordered 3D barrier rows can still be genuinely
  away / depletion

What is now reopened:

- the 3D **dense** spent-delay branch at ultra-weak field (`5e-5`) has a
  retained same-family barrier card with:
  - Born `7.39e-16`
  - `MI = 0.1414`
  - decoherence `13.5%`
  - centroid-side distance exponent `-1.62`, `R² = 0.976`
- under the gravity-observable hierarchy:
  - `z = 2, 3, 4, 5, 6` are genuinely attractive on the retained tested window

So the safe 3D read is now:

- **not fully negative anymore**
- **retains a real attractive window on the current tested card**
- **not yet a clean all-distances attraction theorem either**

## The mechanism

At ultra-weak field, the phase perturbation per edge is tiny.
The TOTAL perturbation over all paths is the coherent sum of
many small perturbations. In the LINEAR response regime, this
sum shifts the centroid TOWARD the mass (constructive interference
on the mass side from the phase valley).

At stronger field, the perturbation is large enough to cause
destructive interference at the beam center. The depletion
effect dominates, shifting the centroid AWAY.

The transition between TOWARD and AWAY happens at the field
strength where the per-edge phase perturbation exceeds ~1/k.
Below this, linear response → attraction.
Above this, nonlinear disruption → depletion.

## Open question

What still limits the 3D dense branch?

- the tested `z = 2..6` window is now attractive under the hierarchy
- MI and decoherence are present but weaker than the stronger 2D dense rows

So the next question is no longer “can 3D ordered lattices ever turn toward?”
The next question is:

- can the 3D dense spent-delay geometry extend the hierarchy-clean attractive
  window beyond `z = 6` while keeping the same same-family barrier card?

## Artifact chain

- [`scripts/lattice_3d_dense_10prop.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_10prop.py)
- [`docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
- [`docs/GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md)
