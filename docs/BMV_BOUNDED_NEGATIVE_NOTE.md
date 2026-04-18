# BMV Gravitational Entanglement: Bounded Negative

**Date:** 2026-04-05
**Status:** s² coupling confirmed; no discrete spacetime correction found

## What was tested

Simulated BMV comparison protocol: beam propagates through field of a mass
in superposition of two z-positions (z=+sep and z=-sep). Measured the
entanglement (1 - overlap) between beam states conditioned on the
two mass positions.

## Results

### Coupling dependence

Entanglement ∝ s^2.00 (exact). Matches the continuum BMV prediction
from gravitational phase squaring. Verified across 5 orders of s
(1e-4 to 5e-2).

### Separation dependence

| h | ent ∝ sep^α |
|---|-------------|
| 1.0 | +0.19 (wrong sign) |
| 0.5 | -1.11 |
| 0.25 | -1.21 |

The separation exponent converges toward the continuum prediction
(sep^(-2.0)) as h decreases. The correction scales as h^0.17 —
very slow convergence. At h=0.25 the exponent is -1.21, still far
from -2.0.

## Bounded interpretation

The s² coupling is an exact lattice reproduction of the continuum BMV
prediction. This is non-trivial as a verification (10^5 paths contribute),
but it is NOT a discrete spacetime prediction — it converges to the
continuum.

The separation exponent has a finite-h correction that vanishes in the
continuum limit. This is a lattice artifact, not a prediction about
discrete spacetime.

## No-go statement

The model does not produce a distinguishable discrete correction to the
BMV entanglement signal. The lattice gives the same s² coupling as the
continuum, and the separation dependence converges to the continuum
value at finer h. There is no discrete spacetime signature in the BMV
observable on this model.

## Missing artifact chain

This note is based on inline tests (not a frozen script+log). A frozen
harness exists only for the coupling-dependence check. The separation
convergence was tested inline across h=0.5, 0.25 but not frozen.
