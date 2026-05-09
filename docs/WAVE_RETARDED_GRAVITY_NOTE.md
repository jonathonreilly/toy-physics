# Wave Retarded Gravity: Retarded ≠ Instantaneous on the Wave Field

**Date:** 2026-04-07 (revised)
**Status:** proposed_retained positive — retarded moving-source field differs from instantaneous (c=∞) comparator by 23–26% on 3 families; F~M and Born preserved

## Artifact chain

- [`scripts/wave_retarded_gravity.py`](../scripts/wave_retarded_gravity.py)
- [`logs/2026-04-07-wave-retarded-gravity.txt`](../logs/2026-04-07-wave-retarded-gravity.txt)

## Question

The wave-equation field carries a finite-c lightcone (certified
separately). When the source moves, does the resulting beam deflection
actually differ from what an instantaneous (c=∞) field would produce?
The earlier draft compared against frozen-position fields, which is not
a clean instantaneous comparator. This revision uses one.

## Decisive comparator

The **instantaneous comparator** I is built layer-by-layer: at each
layer t, the field everywhere is set to the LATE-TIME stationary slice
of a static wave-equation solve with the source frozen at `iz_of_t(t)`.
This is the c=∞ limit — the field everywhere always tracks the current
source position with no propagation delay. Stationary slices are
cached per source position.

The retarded field M is the standard wave-equation evolution with the
same `iz_of_t` source motion.

Beam runs through both fields. The decisive metric is `delta_M − delta_I`.

## Result (Fam1, v/c = 0.30)

| Reference | delta_z |
| --- | ---: |
| A: frozen at z_start (intuition only) | +0.008158 |
| B: frozen at z_end (intuition only) | +0.001846 |
| C: frozen at z_mid (intuition only) | +0.006543 |
| **M: moving source, RETARDED** | **+0.008457** |
| **I: moving source, INSTANTANEOUS (c=∞)** | **+0.011242** |
| **M − I** | **−0.002785** |
| relative |M−I| / max(|M|,|I|) | **24.77%** |

The retarded and instantaneous fields produce **different** beam
deflections by 25%. The frozen references are kept in the table as
intuition only; they are not the test.

## Family portability

| Family | dM | dI | M − I | relative |
| --- | ---: | ---: | ---: | ---: |
| Fam1 | +0.008457 | +0.011242 | −0.002785 | 24.77% |
| Fam2 | +0.008234 | +0.011134 | −0.002901 | 26.05% |
| Fam3 | +0.008267 | +0.010671 | −0.002404 | 22.53% |

Three independent grown geometries: M and I differ by 22–26%.
Same sign (M < I), same order of magnitude. The retardation effect
is geometry-portable.

## Other observables on the moving-source field

| Property | Value |
| --- | ---: |
| F~M (Fam1) | 0.9965 |
| F~M (Fam2) | 0.9955 |
| F~M (Fam3) | 0.9963 |
| Born |I3|/P | 6.21e-16 |
| Null (s=0) | exact |
| v-symmetry (+v vs −v) | +0.0072 vs +0.0085 |

F~M holds, Born stays at machine precision, exact null. The full
weak-field package survives the dynamical, time-translating source.

## What this means

On the wave-equation field, a moving source produces a beam deflection
that does NOT match the field that would be produced if the field
everywhere instantaneously tracked the current source position. The
two are 25% apart in magnitude on this v/c=0.30 geometry, and the
retarded version is consistently the smaller one — consistent with
finite-c information transport.

This is the dynamical retardation signature, certified against the
proper c=∞ comparator instead of frozen-position references.

## What this DOES NOT yet show

- A specific `r/c` light-travel-time match (just that M ≠ I)
- The detailed angular profile of the retardation
- Multiple v/c values; only 0.30 is tested
- Strong-field or non-perturbative regime
- Backreaction (source feeling its own field)
- Orbital / accelerated source (translation only)

## Claim boundary

- v/c = 0.30 single value
- Linear translation, not orbit
- Single source, no backreaction
- Stationary slices used for the instantaneous comparator are
  cached per visited iz; with the chosen v that's 7 unique positions
- The retarded effect is +25% scale, not order-of-magnitude — small v/c

## Inputs (cited authorities)

The runner's load-bearing observable is `delta_M − delta_I`, the
difference between retarded moving-source field and a layer-by-layer
stitched late-time stationary slice (the c=∞ comparator). The
primitives the runner imports are each one-hop authorities on the
current main retained surface:

- standard parallel perturbation propagator and beam-deflection readout
  for the linear gravitational response:
  [`LINEAR_RESPONSE_TRUE_KUBO_NOTE.md`](LINEAR_RESPONSE_TRUE_KUBO_NOTE.md);
- continuum-stable static-slice construction for the stitched
  instantaneous comparator and the wave-equation field's finite-c
  lightcone certification:
  [`WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md`](WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md)
  and
  [`WAVE_RETARDATION_LAB_PREDICTION_NOTE.md`](WAVE_RETARDATION_LAB_PREDICTION_NOTE.md);
- grown-DAG geometry families Fam1/Fam2/Fam3 used for the portability
  check:
  [`KUBO_CONTINUUM_LIMIT_NOTE.md`](KUBO_CONTINUUM_LIMIT_NOTE.md).

The note's contribution is the bounded numerical M − I gap on three
families. The c=∞ asymptotic identification of the stitched stationary
slices is taken as the audit-flagged conditional input, not derived
inside this note.
