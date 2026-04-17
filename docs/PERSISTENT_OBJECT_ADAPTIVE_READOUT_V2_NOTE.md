# Persistent Object Adaptive Readout V2 Note

**Date:** 2026-04-05  
**Status:** bounded no-go for a stronger frontier-shell readout on the compact repeated-update source object

## Artifact chain

- [`scripts/persistent_object_adaptive_readout_v2_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_adaptive_readout_v2_probe.py)
- [`logs/2026-04-05-persistent-object-adaptive-readout-v2-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-adaptive-readout-v2-probe.txt)

## Question

Can we push one step further toward detector/readout localization on the
compact repeated-update source object without losing the exact zero-source
reduction or the weak-field law?

This probe stays narrow:

- one exact 3D lattice family at `h = 0.25`
- one compact repeated-update source object from the retained top-3 update
- one broad detector reference
- one adaptive frontier-shell readout candidate
- one exact zero-source reduction check

## Architecture

This is not the same readout as the v1 adaptive contour.

The v2 readout:

1. diffuses the detector profile locally on the final layer
2. blends the diffused profile with the raw detector mass
3. converts that profile into a frontier shell, not a monotone crop

The intent is to localize harder by emphasizing the transition band of the
detector profile rather than just keeping the high-probability core.

## Frozen result

The frozen probe uses the same retained source object and a frontier-shell
readout on top of it.

Reduction check:

- zero-source broad shift: `+0.000000e+00`
- zero-source frontier shift: `+3.696951e-16`
- zero-source frontier target: `0.246575`
- zero-source frontier tau: `3.204892e-03`
- zero-source frontier bias: `0.000662`
- fixed dynamic field gain: `1.800031e+00`

Frozen readout:

| mode | step `F~M` | `TOWARD` | det `N_eff` | support frac | capture | readout `N_eff` | mean centroid delta | frontier |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| broad | `1.00, 1.00, 1.00` | `12/12` | `497.319` | `1.000` | `1.000` | `625.000` | `+8.561e-03` | `n/a` |
| frontier-shell | `0.74, 1.78, 1.78` | `2/12` | `54.118` | `0.241` | `0.003` | `73.763` | `-8.877e-04` | `0.001` |

## Safe read

The replay is now frozen and the claim surface is kept narrow on purpose:

- the frontier-shell readout localizes harder than v1
- but it does not preserve the weak-field law
- `TOWARD` survives on only `2/12` rows
- the step-wise `F~M` class breaks hard, reaching `0.74, 1.78, 1.78`
- detector support shrinks further, but capture collapses to `0.003`
- so this is a stronger localization attempt, not a successful closure route

## Honest limitation

This is still detector-side only.

- it is not an inertial-mass theorem
- it is not a persistent-pattern closure
- it is not a self-consistent field equation

## Branch verdict

Treat this as a bounded no-go for the stronger frontier-shell readout on the
compact repeated-update source object:

- exact zero-source reduction survives
- detector support shrinks more than v1
- but the weak-field sign and mass-scaling class do not survive
- so this is not a viable readout-localization route on the retained family

The useful outcome is that the readout lane is now cleaner:

- the adaptive contour from v1 remains the best retained detector-side bridge
- the frontier-shell v2 attempt is frozen as too selective
- the persistent-pattern / inertial-response gap remains open
