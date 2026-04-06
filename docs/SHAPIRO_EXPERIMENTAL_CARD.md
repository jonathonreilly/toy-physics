# Shapiro Phase Lag: Experimental Card

**Date:** 2026-04-06
**Status:** lab-facing prediction card — what the model predicts, what it doesn't

## The observable

A beam passing a mass source acquires a **phase shift that depends on
the propagation speed of the gravitational field**. This is the discrete
analog of the Shapiro time delay in GR.

In a matter-wave interferometer: two paths with different gravitational
exposure produce a relative phase. The model predicts this phase depends
on how quickly the gravitational field establishes itself.

## Model predictions (retained, portable)

### 1. Phase scales linearly with mass
phase = k × s × G(b, c, L)

where s is the source strength (mass proxy), k is the wavenumber,
and G is a geometric factor that depends on impact parameter b,
field speed c, and path length L.

Verified: phase ~ s^1.000 over a 16× range of s (0.001 to 0.016).

### 2. Phase depends on field propagation speed
| c (field speed) | Phase (rad) |
| ---: | ---: |
| instantaneous | 0.000 |
| 2.0 | +0.040 |
| 1.0 | +0.050 |
| 0.5 | +0.062 |
| 0.25 | +0.068 |

Approaches a saturation value (~0.070 rad) as c → 0.

### 3. Phase decreases with impact parameter
| b (source distance) | Phase (rad) |
| ---: | ---: |
| 3.0 | +0.062 |
| 5.0 | +0.049 |
| 7.0 | +0.040 |

### 4. Phase is chromatic (proportional to k)
| k | Phase (rad) |
| ---: | ---: |
| 2.0 | +0.030 |
| 5.0 | +0.062 |
| 10.0 | +0.200 |

## Null controls

| Control | Expected | Verified |
| --- | ---: | --- |
| No source (s=0) | phase = 0 | YES (exact) |
| Instantaneous field | phase = 0 | YES (by construction) |
| Source at large b | phase → 0 | YES (monotone decrease) |
| Zero trapping (eta=0) | escape = 1.000 | YES (exact) |

## What the model does NOT predict

1. **The value of c**: the field propagation speed is a free parameter.
   The model says the phase DEPENDS on c but doesn't say what c IS.

2. **Absolute phase in lab units**: the model works in dimensionless
   proxy units. Converting to radians in a real interferometer requires
   a transfer coefficient that depends on the specific experimental setup.

3. **Signal-to-noise**: whether the predicted phase exceeds the detector
   sensitivity is a lab-specific question requiring signal budget analysis.

4. **Systematic contamination**: heating, strain, magnetic cross-talk,
   and instrument lag could produce similar-looking phase shifts. The
   model's prediction is a SCALING LAW (phase ∝ GM, phase ∝ k,
   phase(c) monotone), not a single number.

## Experimental discriminator

The strongest discriminator is the **c-dependence**:
- Quasi-static gravity (Newtonian) predicts NO phase delay
- A causal field predicts a phase delay that depends on frequency
  (through k) and on source modulation speed (through c)

A lock-in experiment modulating the source at frequency f would see:
- In-phase (X): the quasi-static gravitational response
- Quadrature (Y): the causal delay contribution
- Phase lag (phi): atan2(Y, X) → should be nonzero if gravity is causal

## Existing bridge notes

| Note | What it covers |
| --- | --- |
| SHAPIRO_DELAY_NOTE.md | Core retained result + portability |
| SHAPIRO_SCALING_NOTE.md | s, b, k scaling laws |
| SHAPIRO_DIAMOND_BRIDGE_NOTE.md | NV/diamond proxy language |
| DIAMOND_ABSOLUTE_UNIT_BRIDGE_NOTE.md | Absolute vs relative calibration |
| DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md | Signal budget analysis |
| DIAMOND_SENSOR_PROTOCOL_NOTE.md | Measurement protocol |
| GRAVITOMAGNETIC_NOTE.md | Velocity-dependent correction |
| CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md | Full chain hierarchy |
