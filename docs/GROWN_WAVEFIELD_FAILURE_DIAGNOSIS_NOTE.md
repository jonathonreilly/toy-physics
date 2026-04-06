# Grown Wavefield Failure Diagnosis Note

**Date:** 2026-04-06  
**Status:** diagnosed closure for detector-line phase-ramp transfer on the retained grown row

## Artifact Chain

- [`scripts/gate_b_grown_wavefield_companion.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_wavefield_companion.py)
- [`docs/GATE_B_GROWN_WAVEFIELD_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_WAVEFIELD_COMPANION_NOTE.md)
- exact-lattice controls:
  - [`docs/SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_GREEN_POCKET_NOTE.md)
  - [`docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_WAVEFIELD_ESCALATION_NOTE.md)

## Question

Why does the exact-lattice wavefield mechanism fail to transfer cleanly onto the
retained grown row?

This diagnosis keeps the comparison narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- fixed field, no graph feedback
- exact zero-source reduction check
- same promoted observable as the exact wavefield lane when possible:
  detector-line phase-ramp slope/span relative to the same-site control

## What The Grown Row Still Gets Right

The grown-row companion is not failing at the baseline:

- zero-source same-site shift span: `+0.000000e+00 .. +0.000000e+00`
- zero-source wavefield shift span: `+0.000000e+00 .. +0.000000e+00`

So the exact zero-source reduction survives.

The grown row also still produces a real detector response:

- `wave/same = 12.485` at layer `2`
- `wave/same = 6.938` at layer `4`

So the detector is not empty and the failure is not a trivial support collapse.

## What The Grown Row Loses

The observable that made the exact-lattice wavefield compelling does **not**
survive cleanly:

- phase-lag values are small and inconsistent in sign
- ramp slopes are small
- `R²` is low

Frozen row values:

| `layer` | `depth` | `inst F~M` | `same F~M` | `wave F~M` | `phase_lag` | `ramp_slope` | `ramp_R2` | `wave/same` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `2` | `22.0` | `0.978` | `1.052` | `1.056` | `+0.017` | `+0.0193` | `0.294` | `12.485` |
| `4` | `20.0` | `0.938` | `1.030` | `0.904` | `-0.221` | `+0.0227` | `0.298` | `6.938` |

The exact-lattice control by contrast has a coherent detector-line phase ramp
with high `R²`:

- `ramp R² ≈ 0.96`
- phase ramp slope is coherent and source-strength dependent

## Diagnosis

The failure is **not** best explained by any of the following:

- not a zero-source reduction bug
- not a detector-support collapse
- not a pure same-site-vs-wavefield amplitude issue

The strongest retained diagnosis is:

**geometry-induced phase dephasing on the detector line**

More concretely:

- the grown geometry preserves the broad amplitude response
- but it does not preserve the linear phase accumulation needed for a coherent
  detector-line ramp
- the retained grown row is therefore phase-poor, not support-poor

That points to a structural mismatch between the exact-lattice wavefield
observable and the grown-row geometry:

- the exact lane benefits from enough regularity for phase to align across the
  detector line
- the grown row keeps the signal but scrambles the phase relationship that the
  ramp fit is trying to measure

## Final Verdict

**diagnosed closure: coherent detector-line phase-ramp transfer fails on the
retained grown row because the grown geometry dephases the ramp observable even
though the amplitude response and zero-source reduction survive**

## Reopen Condition

Only a genuinely new grown geometry family, or a different wave observable that
does not rely on coherent detector-line phase accumulation, should be treated as
an actual reopen.

