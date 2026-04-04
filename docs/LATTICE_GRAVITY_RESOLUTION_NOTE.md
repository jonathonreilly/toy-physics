# Lattice Gravity Resolution: Ultra-Weak Field Gives Both Attraction AND 1/b

**Date:** 2026-04-04
**Status:** 2D RESOLVED. 3D open.

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

3D NN lattice (9 edges/node): STILL AWAY at strength=0.0005 with
spent-delay. The 9-edge NN lattice doesn't have enough path diversity
for the linear response to dominate.

Dense 3D lattice (25 or 49 edges): ALSO AWAY at strength=0.0005.
The 3D beam depletion is stronger because the beam spreads in two
transverse dimensions.

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

Why does the transition work on the 2D dense lattice but not
on the 3D NN lattice? The 2D lattice has 11 edges/node while
the 3D has 9. But the dense 3D (49 edges) also fails. The
dimensionality itself might be the issue — the 3D beam spreads
faster, requiring even weaker field for the linear regime.

## Scripts

- `action_power_canonical_harness.py` — 2D/3D comparison
- Various inline tests documented in commit messages
