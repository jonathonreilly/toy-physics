# Wave Retarded Gravity: Beam Sees Source at Retarded Position

**Date:** 2026-04-07
**Status:** retained positive — moving source on wave-equation field gives retarded deflection on 3 families; Newton falsified

## Artifact chain

- [`scripts/wave_retarded_gravity.py`](../scripts/wave_retarded_gravity.py)
- [`logs/2026-04-07-wave-retarded-gravity.txt`](../logs/2026-04-07-wave-retarded-gravity.txt)

## Question

The wave-equation self-field has a finite-c lightcone. Does that
finite-c carry through to gravity in the way GR demands — does the
beam respond to where the source WAS at light-travel time ago
(retarded), not where it IS at the moment of crossing (Newton)?

## Decisive test

Source moves from `z_start=3.0` to `z_end=0.0` over 20 layers
(`v/c = 0.30`). Measure beam deflection on the moving-source field
and compare against three frozen references:

- **A**: frozen at z_start (retarded prediction at high v/c)
- **B**: frozen at z_end (Newton/instantaneous prediction)
- **C**: frozen at z_mid (midpoint average)

Define mixing parameter `alpha = (delta_M - delta_A) / (delta_B - delta_A)`:
- alpha = 0 → matches z_start (retarded)
- alpha = 1 → matches z_end (Newton)
- alpha = 0.5 → midpoint

| Reference | delta_z (Fam1) |
| --- | ---: |
| A: frozen at z_start | +0.008158 |
| B: frozen at z_end (Newton) | +0.001846 |
| C: frozen at z_mid | +0.006543 |
| **M: moving source** | **+0.008457** |
| **alpha** | **−0.05** |

The moving-source result is **+0.0085**, essentially identical to
the z_start reference. Newton predicts +0.0018 — falsified by 4.6×.

## Family portability

| Family | alpha | delta_A | delta_B | delta_M |
| --- | ---: | ---: | ---: | ---: |
| Fam1 | −0.05 | +0.0082 | +0.0018 | +0.0085 |
| Fam2 | −0.04 | +0.0080 | +0.0021 | +0.0082 |
| Fam3 | −0.03 | +0.0081 | +0.0011 | +0.0083 |

All three families give alpha < 0.05. The retarded behaviour is
geometry-portable, not a Fam1 artifact.

## Other observables on the moving-source field

| Property | Value |
| --- | ---: |
| F~M (Fam1) | 0.9965 |
| F~M (Fam2) | 0.9955 |
| F~M (Fam3) | 0.9963 |
| Born |I3|/P | 2.22e-15 |
| Null (s=0) | exact |
| v-symmetry (+v vs −v) | +0.0072 vs +0.0085 |

F~M holds, Born stays at machine precision, exact null. The full
weak-field package survives the dynamical, time-translating source.

## What this means

The model now has a genuinely retarded gravitational interaction.
The field equation:

  (1/c²) ∂²f/∂t² − ∇²f = source(t, y, z)

generates a field that propagates at `c = 1` lattice cell per layer
(certified separately by the wave-equation lightcone test), AND when
the source moves, the beam responds to the source position at the
retarded time, not the instantaneous time.

This is the GR-style local-causal-influence statement. Newton's
instantaneous-action prediction is falsified on 3/3 families on this
single harness.

## Claim boundary

- v/c = 0.30 (single velocity tested; full v-sweep not yet done)
- Linear translation only; orbital / accelerated source not yet tested
  (vector_sector lane covers orbital with imposed field, not wave eqn)
- alpha < 0 slightly: the moving source produces deflection slightly
  larger than frozen-A. Likely from the wave field building up
  along the source's prior trajectory. Sign unaffected.
- Single source; multi-source superposition not tested
- Backreaction not tested
