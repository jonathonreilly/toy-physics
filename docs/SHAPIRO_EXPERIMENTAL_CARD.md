# Shapiro Phase Lag: Experimental Card

**Date:** 2026-04-06
**Status:** support - structural or confirmatory support note

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

## Experiment card requirement: ideal detector first

Before adding any NV, interferometer, or lab-specific noise model, the
card must include an **ideal-detector forward model**:

- same source trajectory used in all comparators
- perfect timing / phase reference
- no noise floor, bandwidth limit, or spectral artefacts
- direct prediction of the measured channels: `X`, `Y`, `R`, `phi`

This is required for two reasons:

1. It checks whether the source modulation itself is being simulated
   faithfully before detector assumptions enter.
2. It cleanly separates the physics prediction (retarded vs
   instantaneous / quasi-static) from instrument transfer functions.

Only after the ideal-detector prediction is fixed should the card add:

- finite bandwidth
- integration time
- lock-in windowing / spectral leakage
- technical noise and calibration systematics

## Experimental discriminator

The strongest discriminator is the **c-dependence**:
- Quasi-static gravity (Newtonian) predicts NO phase delay
- A causal field predicts a phase delay that depends on frequency
  (through k) and on source modulation speed (through c)

**Important caveat** (from `SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`):
a static field shaped like a cone (matching the dynamic cone's spatial
envelope) reproduces the same phase curve. The discriminator is the
field's spatial SHAPE, not causality per se. A lock-in experiment
would need to distinguish causal propagation from a shaped static field.

The static-scheduling proxy (uniform field applied at all layers) does
NOT reproduce the phase. So the discriminant is spatial structure,
and the causal cone naturally produces that structure.

A lock-in experiment modulating the source at frequency f would see:
- In-phase (X): the quasi-static gravitational response
- Quadrature (Y): the shaped-field delay contribution
- Phase lag (phi): atan2(Y, X) → nonzero if the field has cone-like structure

## What would count as a discriminating measurement

A measurement would discriminate the model's prediction from Newtonian
gravity if it shows:

1. **A phase lag that scales as s^1** when source mass is varied, AND
2. **That phase lag is frequency-dependent** (scales with k or drive frequency), AND
3. **The phase vanishes for a static (unmodulated) source**

The static-cone caveat means this is necessary but not sufficient: a shaped
static field could also produce items 1-2. The additional discriminator
would be:

4. **The phase depends on source modulation frequency** in a way consistent
   with finite field propagation speed (not just field shape)

Specifically: if the source is modulated at frequency f, the quadrature
signal Y should depend on f in a way that tracks c (the field propagation
speed), not just the spatial envelope. A static shaped field would produce
a frequency-independent Y; a causal field would produce Y(f) that changes
with f at rates comparable to the light-travel time across the apparatus.

**Update (retardation discriminator)**: This prediction is now confirmed
in the model. An oscillating source with retarded vs instantaneous field
response produces a frequency-dependent difference curve that:
- Has exact nulls at f=0 and d=0
- Is portable across 3 families (0.3-6%)
- Shows a sign split at f=0.15 (inst negative, retarded positive)
- Grows monotonically with retardation delay

The measurable is NOT a universal phase sign. It is the **phase-locked
response amplitude and phase** at the source modulation frequency:
- Lock-in at frequency f
- Measure amplitude R and phase phi of the response
- The retardation produces a phi(f) curve that differs from instantaneous
- The difference is phase-sensitive: phi_0 reversal flips the sign
  (this IS the built-in null control, not a weakness)

See `RETARDATION_DISCRIMINATOR_NOTE.md` for the full retained result.

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
| RETARDATION_DISCRIMINATOR_NOTE.md | Oscillating-source retardation result |
