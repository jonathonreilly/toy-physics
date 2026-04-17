# Persistent Object Green Scout

**Date:** 2026-04-05  
**Status:** bounded quasi-persistent source-object control on the compact exact lattice

## Artifact chain

- [`scripts/persistent_object_green_scout.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_green_scout.py)
- [`logs/2026-04-05-persistent-object-green-scout.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-persistent-object-green-scout.txt)

## Question

Can the smallest self-consistent Green-like source object survive more than one
update on the compact exact lattice while still sourcing a field?

This probe stays deliberately narrow:

- one compact exact `h = 0.25` family
- one interior cross-shaped source object
- one source-resolved Green-like field
- one self-consistency loop repeated for three updates
- one observable pair:
  - source-object survival / localization
  - detector response / weak-field sign

## Frozen result

The frozen probe uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
- fixed field calibration gain `1.800031e+00`
- three repeated source-object updates

Reduction check:

- zero-source shift: `+0.000000e+00`

Frozen readout:

| `s` | step | source `N_eff` | source peak share | detector `N_eff` | detector `supp(>=1% peak)` | `delta` | field max | overlap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `0` | `4.788` | `0.318` | `497.28` | `1.000` | `+2.293350e-03` | `2.500000e-03` | `0.956` |
| `0.0010` | `1` | `4.788` | `0.318` | `497.28` | `1.000` | `+2.284438e-03` | `2.482322e-03` | `0.956` |
| `0.0010` | `2` | `4.788` | `0.318` | `497.28` | `1.000` | `+2.284434e-03` | `2.482305e-03` | `1.000` |
| `0.0020` | `0` | `4.789` | `0.318` | `497.31` | `1.000` | `+4.587808e-03` | `5.000000e-03` | `0.956` |
| `0.0020` | `1` | `4.788` | `0.318` | `497.30` | `1.000` | `+4.569582e-03` | `4.964883e-03` | `0.956` |
| `0.0020` | `2` | `4.788` | `0.318` | `497.30` | `1.000` | `+4.569565e-03` | `4.964815e-03` | `1.000` |
| `0.0040` | `0` | `4.789` | `0.318` | `497.37` | `1.000` | `+9.179951e-03` | `1.000000e-02` | `0.956` |
| `0.0040` | `1` | `4.788` | `0.318` | `497.34` | `1.000` | `+9.141876e-03` | `9.930719e-03` | `0.956` |
| `0.0040` | `2` | `4.788` | `0.318` | `497.34` | `1.000` | `+9.141805e-03` | `9.930446e-03` | `1.000` |
| `0.0080` | `0` | `4.790` | `0.318` | `497.47` | `1.000` | `+1.837657e-02` | `2.000000e-02` | `0.956` |
| `0.0080` | `1` | `4.788` | `0.318` | `497.42` | `1.000` | `+1.829381e-02` | `1.986525e-02` | `0.956` |
| `0.0080` | `2` | `4.788` | `0.318` | `497.42` | `1.000` | `+1.829350e-02` | `1.986416e-02` | `1.000` |

Step summary:

- step `0`: `F~M = 1.00`, mean source `N_eff = 4.789`, mean detector `N_eff = 497.36`, `4/4` TOWARD
- step `1`: `F~M = 1.00`, mean source `N_eff = 4.788`, mean detector `N_eff = 497.33`, `4/4` TOWARD
- step `2`: `F~M = 1.00`, mean source `N_eff = 4.788`, mean detector `N_eff = 497.33`, `4/4` TOWARD

## Safe read

The strongest bounded statement is:

- the source object survives more than one self-consistency update
- it keeps sourcing a field with the retained weak-field sign
- the weak-field mass-scaling class remains linear across the repeated updates
- the source object is stable, but it is still broad rather than sharply
  localized

## Honest limitation

This is a quasi-persistent source-object control, not a persistent-mass theorem.

- the source support stays broad: `N_eff` remains about `4.788/5`
- the detector remains broad as well, so this does not yet produce a compact
  localized inertial object
- the update loop is self-consistent but still minimal; it does not yet test a
  fully converged dynamical object sector

## Branch verdict

Treat this as a bounded positive for the persistent-object lane:

- exact zero-source reduction survives
- source-object survival survives multiple updates
- the field remains sourceable on each update
- the weak-field sign and `F~M = 1.00` class survive
- but the object is still broad, so this does **not** yet close the
  persistent-pattern / inertial-response gap

## Fastest Falsifier

If a future version of this probe shows either:

- source `N_eff` collapsing toward `1`
- or the repeated-update detector sign flipping AWAY

then the result should be treated as a bounded control, not an inertial-object
candidate.
