# Persistent Object Compact Update Probe

**Date:** 2026-04-05  
**Status:** bounded positive on a compact repeated-update object, not an inertial-mass closure

## Artifact chain

- [`scripts/persistent_object_compact_update_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_compact_update_probe.py)
- [`logs/2026-04-05-persistent-object-compact-update.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-compact-update.txt)

## Question

Starting from the retained broad quasi-persistent exact-lattice control, can a
tighter localization update produce a smaller repeated-update source object
while still preserving the weak-field sign and near-linear mass scaling?

This probe stays narrow:

- one exact 3D lattice family at `h = 0.25`
- one fixed cross-shaped source cluster
- one broad repeated-update control
- one compact `top-3` update rule
- one exact zero-source reduction check
- one observable pair:
  - source-object effective support from the update weights
  - detector response / weak-field sign / `F~M`

## Frozen result

The frozen probe uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- fixed field calibration gain `1.800031e+00`
- three repeated source-object updates
- compact update rule: keep only the `top-3` source weights after each update

Reduction check:

- zero-source shift: `+0.000000e+00`

Frozen readout:

| mode | step | `F~M` | `TOWARD` | object `N_eff` | object support | response `N_eff` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| broad | `0` | `1.00` | `4/4` | `4.859` | `5.000` | `497.34` |
| broad | `1` | `1.00` | `4/4` | `4.859` | `5.000` | `497.34` |
| broad | `2` | `1.00` | `4/4` | `4.859` | `5.000` | `497.34` |
| compact | `0` | `1.00` | `4/4` | `3.593` | `3.667` | `497.32` |
| compact | `1` | `1.00` | `4/4` | `3.593` | `3.667` | `497.32` |
| compact | `2` | `1.00` | `4/4` | `3.593` | `3.667` | `497.32` |

Summary:

- broad object `N_eff = 4.859`, support `= 5.000`, response `N_eff = 4.789`
- compact object `N_eff = 3.593`, support `= 3.667`, response `N_eff = 4.788`
- both modes keep `4/4` `TOWARD`
- both modes keep `F~M = 1.00` at every repeated-update step

## Safe read

The strongest bounded statement is:

- the tighter top-3 update does produce a smaller repeated-update source
  object on this exact-lattice family
- the weak-field sign survives the repeated updates
- the mass-scaling class stays linear

## Honest limitation

This is still a quasi-persistent source-object control, not a persistent-mass
theorem.

- the detector response stays broad
- the compact update shrinks the source object, but it does not yet produce a
  sharply localized inertial response
- the repeated-update loop is still minimal and exact-lattice only

## Branch verdict

Treat this as a bounded positive for the persistent-object lane:

- exact zero-source reduction survives
- the compact update makes the source object smaller than the broad control
- the weak-field sign and `F~M = 1.00` survive
- but the detector/readout sector remains broad, so this does **not** close the
  persistent-pattern / inertial-response gap

## Fastest Falsifier

If a future version of this probe shows either:

- compact update loses `TOWARD`
- or the step-wise `F~M` drifts away from `1`
- or the object support rises back to the broad control

then the broad quasi-persistent object should remain the smallest retained
object on this family.
