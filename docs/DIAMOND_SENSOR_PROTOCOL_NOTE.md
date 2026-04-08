# Diamond Sensor Protocol Note

**Date:** 2026-04-05  
**Status:** lab-facing discriminator protocol, intentionally bounded

## Purpose

This note turns the current retained phase-sensitive / retarded / wavefield
lane into a concrete protocol a diamond/NV collaborator could evaluate.

The repo does **not** yet support a defensible absolute gravity amplitude for
an NV experiment. So the correct claim surface stays narrow:

- phase-quadrature discriminator: yes
- coherent spatial phase ramp: yes
- absolute gravity detectability: not yet budgeted here

## What the lab should measure

Measure the lock-in channels:

- `X`: in-phase response
- `Y`: quadrature response
- `phi = atan2(Y, X)`: phase lag

If the setup is widefield, also record the spatial phase profile across the NV
image.

## Requirement: ideal-detector forward model first

Before any lab-specific protocol is treated as complete, build the
ideal-detector version of the measurement:

- same driven source history in every comparator
- perfect phase reference
- no noise floor
- no finite-bandwidth or spectral-leakage model
- direct output for `X`, `Y`, `phi`, and spatial phase profile

This is a required precondition, not an optional refinement.
It checks source fidelity first and keeps the physics prediction
separate from detector artefacts.

## Standard null

After calibration and static-background subtraction, the quasi-static /
instantaneous Newtonian baseline should give:

- `Y ≈ 0`
- `phi ≈ 0`
- no stable spatial phase ramp

## Retained prediction

The retained retarded / wavefield lane predicts:

- a nonzero quadrature channel `Y`
- a nonzero phase lag `phi`
- a coherent spatial phase ramp in widefield readout
- strengthening of the quadrature / phase signal with increasing drive
  frequency and increasing source-detector separation

## Minimal control stack

Use the smallest control set that lets the collaborator tell signal from
instrument lag:

1. drive off
2. source retracted far enough that the coupling should be negligible
3. same drive with a `pi` reference flip, to verify the quadrature sign
4. static source / no modulation, to remove DC or slow drift backgrounds

If the lab wants an extra control, first run the same lock-in pipeline on a
known magnetic or strain source to validate the instrumentation.

## Suggested scan points

The repo cannot justify calibrated amplitude numbers yet, so the protocol is
expressed as an ordering table rather than a quantitative prediction table.

Suggested scan classes:

- drive frequency: low, mid, high
- source-detector separation: near, mid, far

| scan class | standard null expectation | retained wavefield expectation |
| --- | --- | --- |
| low drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | weakest retained signal; likely small or marginal |
| low drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | weak retained phase lag if any |
| mid drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | detectable `Y` is more plausible |
| mid drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | stronger phase lag or quadrature than near separation |
| high drive, near separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | stronger phase-sensitive response than low drive |
| high drive, far separation | `X` dominates, `Y ~ 0`, `phi ~ 0` | strongest candidate for a coherent `Y` and phase ramp |

The qualitative ordering is the key claim:

- retained lane: `Y` and `phi` should grow with drive frequency and
  separation
- standard null: `Y` stays near zero after calibration

## What would count as a hit

- `Y` survives calibration and is not consistent with zero
- the sign of `Y` flips under the `pi` reference control
- the phase is not flat across the image in widefield mode
- the effect strengthens in the high-drive / far-separation direction

## What would count as a miss

- quadrature vanishes after calibration
- the phase is flat across the field of view
- the signal moves only because of instrument lag, heating, or trivial
  amplitude rescaling

## Honest limitation

This repo does not yet provide a calibrated gravity amplitude for NV sensors.

So the strongest defensible lab-facing artifact is a discriminator protocol:

- ideal-detector forward model first
- phase-sensitive lock-in readout
- standard quasi-static null
- sign-flip control
- optional spatial phase-ramp imaging

## Experimental framing

The cleanest phrasing for a lab contact is:

"Measure the lock-in quadrature and spatial phase profile for a driven source
near an NV sensor. The standard quasi-static baseline predicts no stable
quadrature after calibration; the retained retarded/wavefield lane predicts a
nonzero phase-lag signature that strengthens with drive frequency and source-
detector separation."

## References

- NV dual-channel lock-in readout of time-dependent fields:
  [Phys. Rev. B 88, 220410](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.88.220410)
- widefield / per-pixel lock-in detection in diamond NV imaging:
  [Scientific Reports 2022](https://www.nature.com/articles/s41598-022-12609-3)
- NV strain sensitivity in diamond mechanical structures:
  [Scientific Reports 2020](https://www.nature.com/articles/s41598-020-65049-2)

## Final Verdict

**bounded but testable phase-sensitive protocol**
