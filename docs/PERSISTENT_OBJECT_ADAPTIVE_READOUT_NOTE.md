# Persistent Object Adaptive Readout Note

**Date:** 2026-04-05  
**Status:** bounded positive for a genuinely different detector/readout architecture on the compact repeated-update source object

## Artifact chain

- [`scripts/persistent_object_adaptive_readout_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_adaptive_readout_probe.py)
- [`logs/2026-04-05-persistent-object-adaptive-readout-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-adaptive-readout-probe.txt)

## Question

Can a softer, more dynamical readout architecture do better than the fixed
windows / Gaussian tapers already shown to be a no-go on the compact
repeated-update source object?

This probe stays narrow:

- one exact 3D lattice family at `h = 0.25`
- one compact repeated-update source object from the retained top-3 update
- one broad readout reference
- one adaptive readout candidate based on an entropy-guided diffusion contour
- one exact zero-source reduction check

## Architecture

The adaptive readout is not a fixed crop.

It does three things:

1. diffuses the detector profile locally on the final layer
2. blends the diffused profile with the raw detector mass
3. turns that blended profile into a soft contour mask by choosing a target
   mass threshold adaptively from the profile entropy

That makes it softer and more dynamical than the fixed hard window or Gaussian
taper tests.

## Frozen result

The frozen probe uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- compact source object with `top_keep = 3`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- fixed field calibration gain `1.800031e+00`
- three repeated source-object updates
- adaptive contour parameters:
  - `diffuse_steps = 2`
  - `diffuse_lambda = 0.35`
  - `target_mass_base = 0.32`
  - `target_mass_gain = 0.26`
  - `mask_slope_floor = 0.10`
  - `blend_with_raw = 0.50`

Reduction check:

- zero-source broad shift: `+0.000000e+00`
- zero-source adaptive shift: `-3.155826e-16`

Frozen readout:

| mode | step `F~M` | `TOWARD` | det `N_eff` | support frac | capture | readout `N_eff` | mean centroid delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| broad | `1.00, 1.00, 1.00` | `12/12` | `497.319` | `1.000` | `1.000` | `625.000` | `+8.561e-03` |
| adaptive contour | `1.04, 1.04, 1.04` | `12/12` | `120.414` | `0.264` | `0.351` | `132.034` | `+1.972e-02` |

## Safe read

The strongest bounded statement is:

- the adaptive contour is a real alternative to the fixed windows / tapers
- it preserves the weak-field sign on all tested source strengths
- it keeps the step-wise mass-scaling class close to linear
- it reduces detector support substantially compared with the broad readout
- it captures a meaningful fraction of the detector mass without collapsing
  the readout to a near-zero mask

## Honest limitation

This is still not an inertial-mass closure.

- the centroid shift is larger than the broad reference
- the readout remains a detector-side proxy, not a persistent localized object
- the adaptive contour is better than the fixed tapers, but it still does not
  solve the full detector/readout localization problem

## Branch verdict

Treat this as a bounded positive for the persistent-object lane:

- exact zero-source reduction survives
- the adaptive contour is materially different from the fixed window / taper
  family
- weak-field sign survives
- `F~M` stays close to `1`
- detector support is reduced
- but this does **not** close the persistent-pattern / inertial-response gap

## Fastest Falsifier

If a future adaptive contour version shows either:

- `TOWARD` fails
- or `F~M` drifts far from `1`
- or detector support stops improving over the broad readout

then the adaptive contour should be treated as a readout refinement, not a
route to inertial-object closure.
