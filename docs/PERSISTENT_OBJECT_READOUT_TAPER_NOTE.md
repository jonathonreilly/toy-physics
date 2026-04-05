# Persistent Object Readout Taper Audit

**Date:** 2026-04-05  
**Status:** robust no-go for detector/readout localization on the compact repeated-update source object

## Artifact chain

- [`scripts/persistent_object_readout_taper_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_readout_taper_probe.py)
- [`logs/2026-04-05-persistent-object-readout-taper-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-readout-taper-probe.txt)

## Question

Was the earlier hard `3x3` readout-localization failure just too harsh?

This audit stays narrow:

- one exact 3D lattice family at `h = 0.25`
- one compact repeated-update source object from the retained top-3 update
- one broad detector readout
- one hard `3x3` reference
- one small Gaussian taper family
- one reduction check: zero source recovers free propagation exactly

## Frozen result

The frozen probe uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- compact source object with `top_keep = 3`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- hard window radius `1`
- Gaussian taper widths `sigma = 1.5, 2.5, 4.0` cells
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- fixed field calibration gain `1.800031e+00`
- three repeated source-object updates

Reduction check:

- zero-source shift: `+0.000000e+00`

Frozen readout:

| mode | step `F~M` | `TOWARD` | mean detector `N_eff` | mean support fraction | mean capture | mean readout `N_eff` | mean centroid delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| broad | `1.00, 1.00, 1.00` | `12/12` | `497.319` | `1.000` | `1.000` | `625.000` | `+8.56e-03` |
| hard | `-0.00, -0.00, -0.00` | `12/12` | `8.992` | `1.000` | `0.038` | `9.000` | `+4.996e-01` |
| Gaussian `sigma=1.5` | `-0.00, -0.00, -0.00` | `12/12` | `34.370` | `0.099` | `0.054` | `38.429` | `+4.924e-01` |
| Gaussian `sigma=2.5` | `0.00, 0.00, 0.00` | `12/12` | `90.244` | `0.243` | `0.135` | `106.720` | `+4.652e-01` |
| Gaussian `sigma=4.0` | `0.01, 0.01, 0.01` | `12/12` | `189.501` | `0.518` | `0.286` | `261.514` | `+4.144e-01` |

## Safe read

The strongest bounded statement is:

- the hard `3x3` window was not the only problem
- softer Gaussian tapers do shrink the detector/readout support compared with
  the broad readout
- but every tapered readout still destroys the weak-field mass law
- even the softest tested taper (`sigma = 4.0`) only gets `F~M` to about
  `0.01`, far from the retained `1.00`
- so the readout-localization idea is not rescued by a gentler window shape

## Honest limitation

This is a useful negative, not a closure.

- the compact source object is real
- the detector support can be reduced
- but the readout sector is still too lossy to keep the weak-field mass law
- so the detector/readout localization lane is robustly blocked on this family

## Branch verdict

Treat this as a robust no-go for detector/readout localization on the compact
repeated-update source object:

- exact zero-source reduction survives
- readout support can be shrunk with either a hard or soft window
- the weak-field sign survives
- but the mass law does not survive any of the tested localization rules

The next readout-side question, if this lane is ever reopened, is not whether a
slightly softer window helps.
It is whether a different readout architecture entirely can localize support
without collapsing `F~M`.
