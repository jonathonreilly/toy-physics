# Diamond / NV Phase-Ramp Signal Budget Note

**Date:** 2026-04-05  
**Status:** narrow experiment-facing prediction note for the retained phase-sensitive lane

## One-line read

The best current diamond-facing prediction is not an absolute gravity
measurement.
It is a lock-in quadrature and spatial phase-ramp null test.

## What should be measured

Measure the standard lock-in channels:

- `X`: in-phase response
- `Y`: quadrature response
- `phi = atan2(Y, X)`: phase lag

If the setup is widefield, also measure the spatial phase profile across the
NV image.

## Standard null

After calibration and static-background subtraction, the quasi-static /
instantaneous baseline should give:

- `Y ≈ 0`
- `phi ≈ 0`
- no stable spatial phase ramp

That is the null the protocol is built around.

## Retained prediction

The retained phase-sensitive / retarded / wavefield lane predicts:

- a nonzero quadrature channel `Y`
- a nonzero phase lag `phi`
- in widefield readout, a coherent spatial phase ramp
- stronger phase-sensitive response as source-detector separation increases
  and as the drive moves away from the quasi-static limit

This is the narrowest defensible external prediction in the current repo.

## Minimal control stack

Use the smallest control set that distinguishes signal from instrument lag:

1. drive off
2. source retracted far enough that coupling should be negligible
3. same drive with a `pi` reference flip, to verify the quadrature sign
4. static source / no modulation, to remove DC or slow drift backgrounds

If the lab wants one extra validation step, run the same lock-in pipeline on a
known magnetic or strain source first.

## What retained science supports this

This note is supported by retained `main` evidence, not by lab-budgeted
amplitude estimates:

- [`docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_MECHANISM_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_CARRYOVER_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- [`docs/PROPAGATOR_FAMILY_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PROPAGATOR_FAMILY_UNIFICATION_NOTE.md)
- [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md)
- [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PREDICTION_NOTE.md)

The reason this is a plausible lab interface is simple:

- the wavefield lane gives the phase-ramp motivation
- the complex-action lanes show that a scalar coupling can deform the same
  propagator into a phase/absorption crossover
- the propagator-family note keeps the claim surface narrow: same transport
  skeleton, different scalar coupling
- the diamond protocol note already maps that structure onto an NV
  lock-in readout

## What remains unknown

Before contacting a lab, the repo still does **not** provide:

- a calibrated absolute signal budget
- a source geometry that is already tied to a specific lab setup
- a lab-specific noise-floor estimate
- a validated mapping from the retained wavefield proxy to a real NV sensor
  coupling strength

So the claim surface stays narrow:

- phase-quadrature discriminator: yes
- coherent spatial phase ramp: yes
- absolute gravity detectability: not yet budgeted here

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the reference `pi` control
- a widefield image shows a stable nonzero phase gradient
- the phase signal strengthens in the expected causal direction with
  separation / drive changes

## What would count as a miss

- the quadrature vanishes after calibration
- the phase is flat across the image
- the signal is explained entirely by instrument lag, heating, or a trivial
  amplitude rescaling

## Final verdict

**bounded but testable phase-sensitive diamond/NV signal-budget note**
