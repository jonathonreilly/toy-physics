# Persistent Object Readout Localization Probe

**Date:** 2026-04-05  
**Status:** bounded negative for detector/readout localization on the compact repeated-update source object

## Artifact chain

- [`scripts/persistent_object_readout_localization_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_readout_localization_probe.py)
- [`logs/2026-04-05-persistent-object-readout-localization.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-readout-localization.txt)

## Question

Starting from the retained compact repeated-update source object, can a
peak-centered detector readout shrink the detector/readout support without
losing the weak-field sign and near-linear mass-scaling class?

This probe stays narrow:

- one exact 3D lattice family at `h = 0.25`
- one compact repeated-update source object from the retained top-3 update
- one broad detector readout
- one peak-centered `3x3` detector window
- one reduction check: zero source recovers free propagation exactly
- one observable pair:
  - detector effective support `N_eff`
  - weak-field sign / `F~M` exponent

## Frozen result

The frozen probe uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- compact source object with `top_keep = 3`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- readout window radius `1` around the detector peak
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- fixed field calibration gain `1.800031e+00`
- three repeated source-object updates

Reduction check:

- zero-source shift: `+0.000000e+00`

Frozen readout:

| mode | step `F~M` | `TOWARD` | mean detector `N_eff` | mean support fraction | mean capture | mean window bins | mean centroid delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| broad | `1.00, 1.00, 1.00` | `12/12` | `497.319` | `1.000` | `1.000` | `625.00` | `+8.56e-03` |
| localized | `-0.00, -0.00, -0.00` | `12/12` | `8.992` | `1.000` | `0.038` | `9.00` | `+4.996e-01` |

## Safe read

The strongest bounded statement is:

- the peak-centered detector window does shrink the detector effective support
  sharply, from `N_eff = 497.319` to `N_eff = 8.992`
- the weak-field sign survives in the localized readout
- but the localized readout only captures about `3.8%` of the detector mass
- and the weak-field mass-scaling class collapses, with the step-wise
  localized `F~M` fit going to `~0`

So this is not a successful detector/readout localization route.

## Honest limitation

This is a useful negative, not a closure.

- the compact source object is real
- the detector window is genuinely smaller
- but the localized readout does not preserve the weak-field mass law
- so the readout sector remains too broad / too lossy to count as a retained
  inertial-response localization

## Branch verdict

Treat this as a bounded negative for the detector/readout localization lane:

- exact zero-source reduction survives
- the localized detector readout is much smaller than the broad one
- the weak-field sign survives
- but the localized mass law does not survive, and the captured detector
  fraction is too small to promote the idea

The next readout-side question, if we keep pushing this lane, is whether a
much less aggressive window or a different response-localization rule can keep
`F~M ≈ 1` while still reducing detector support.
