# Diamond Sensor Prediction Note

**Date:** 2026-04-05  
**Status:** experiment-facing discriminator note, intentionally bounded

## Purpose

This note turns the current retained phase-sensitive / retarded / wavefield
lanes into one lab-facing prediction for a diamond/NV sensor setup.

The goal is not a generic force claim.
The goal is one observable that a diamond lock-in microscope can actually
measure, one standard-physics null, and one minimal control set.

## Why this is the right interface

The NV literature already supports the relevant readout style:

- phase-sensitive lock-in readout of time-dependent fields in diamond NV
  magnetometry
- widefield / pixel-wise lock-in detection
- NV sensitivity to strain in diamond mechanical structures

That makes a lock-in quadrature or phase-ramp prediction a much better lab
interface than an absolute gravitational-force claim.

This repo can already support the phase-sensitive logic through the retained
retarded / wavefield lanes:

- [`docs/RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/RETARDED_FIELD_CAUSALITY_PROBE_NOTE.md)
- [`docs/RETARDED_FIELD_DELAY_PROXY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/RETARDED_FIELD_DELAY_PROXY_NOTE.md)
- [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)

## Concrete prediction

The smallest defensible experiment-facing prediction is:

- a driven-source NV lock-in readout should show a nonzero quadrature channel
  `Y` or a nonzero phase lag `phi = atan2(Y, X)` if the coupling is genuinely
  retarded / wave-like
- the same readout should remain phase-null after calibration in the
  standard instantaneous / quasi-static baseline
- in a widefield geometry, the phase should not just shift globally; it
  should form a coherent spatial phase ramp across the NV image if the
  wavefield lane is the right effective description

The direct null is:

- after phase calibration and static-background subtraction, standard
  Newtonian / quasi-static coupling predicts `Y ≈ 0` and no stable spatial
  phase ramp

The retained model-side prediction is:

- finite propagation or wave-scheduling should produce a measurable
  phase-lag / quadrature component
- that quadrature should strengthen as the drive frequency rises and as the
  source-detector separation increases
- in an imaging readout, the phase slope across the field of view should be
  the cleanest discriminator, not raw amplitude

## Requirement: ideal detector first

Before adding any NV-specific sensitivity, noise floor, spectral artefact,
or lock-in implementation detail, the card must include an
**ideal-detector forward model**:

- perfect phase reference
- no technical noise
- no bandwidth or integration limits
- direct predicted outputs for `X`, `Y`, `R`, and `phi`

The source-fidelity check comes before detector realism:

- verify that the simulated source trajectory is the intended one
- verify that retarded and instantaneous comparators use the same source history
- only then add instrument-specific filtering or noise

This keeps the experiment card honest: physics prediction first,
instrument model second.

## Minimal control set

The smallest useful control set is:

1. drive off
2. same drive with the source removed or retracted far enough that the
   coupling should be negligible
3. same drive with a `pi` phase flip in the reference channel, to check that
   the extracted quadrature really changes sign
4. static source / no modulation, to remove any DC or slow drift background

If the lab wants a stronger control, the same protocol can be run first on a
known magnetic or strain source to verify the lock-in pipeline before trying
the weaker gravity-facing interpretation.

## Honest limitation

This repo does **not** yet give a defensible absolute gravity amplitude for an
NV lab.

So the claim surface should stay narrow:

- phase-quadrature discriminator: yes
- coherent spatial phase ramp: yes
- absolute gravity detectability: not yet budgeted here
- ideal-detector forward model: required before any lab-specific noise claim

That is the smallest prediction still worth taking to a diamond lab.

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the reference `pi` control
- a widefield sensor image shows a stable nonzero phase gradient
- the effect strengthens with frequency / separation in the expected causal
  direction

## What would count as a miss

- quadrature vanishes after calibration
- the phase is flat across the image
- the signal moves only because of instrument lag, heating, or a trivial
  amplitude rescaling

## Experimental framing

If we send this to a diamond/NV lab, the cleanest phrasing is:

"Measure the lock-in quadrature and spatial phase ramp for a driven source
near an NV sensor. The standard quasi-static baseline predicts no stable
quadrature after calibration; the retained retarded/wavefield lane predicts a
nonzero phase-lag signature."

## References that motivate the readout choice

- NV dual-channel lock-in readout of time-dependent fields:
  [Phys. Rev. B 88, 220410](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.88.220410)
- widefield / per-pixel lock-in detection in diamond NV imaging:
  [Scientific Reports 2022](https://www.nature.com/articles/s41598-022-12609-3)
- NV strain sensitivity in diamond mechanical structures:
  [Scientific Reports 2020](https://www.nature.com/articles/s41598-020-65049-2)

## Final Verdict

**bounded but testable phase-sensitive discriminator**
