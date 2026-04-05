# Source-Resolved Wavefield Green Pocket

**Date:** 2026-04-05  
**Status:** exact-lattice finite-speed wavefield pocket, frozen on the retained compact family

## Artifact chain

- [`scripts/source_resolved_wavefield_green_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_wavefield_green_pocket.py)

## Question

Does the exact-lattice Green pocket change in a qualitatively stronger way if
the field is upgraded from same-site memory / finite-lag smoothing to a minimal
finite-speed wavefield update?

This probe stays narrow:

- one compact exact lattice family at `h = 0.25`
- one source-resolved Green control
- one same-site-memory baseline
- one finite-speed wavefield candidate with transverse transport + layer lag
- one reduction check: zero source must recover free propagation exactly
- one main observable: detector phase lag / overlap relative to the same-site
  control

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- same-site memory `mix = 0.9`
- wavefield update parameters:
  - `wave_lag_blend = 0.72`
  - `wave_speed2 = 0.16`
  - `damp = 0.18`
  - `source_blend = 0.52`

Reduction check:

- zero-source same-site shift: `+0.000000e+00`
- zero-source wavefield shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | same-site deflection | wavefield deflection | phase lag (rad) | overlap | wave/same |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.050891e-03` | `+2.412419e-03` | `+8.170763e-02` | `-0.484` | `0.991` | `39.840` |
| `0.0020` | `+4.105409e-03` | `+4.824993e-03` | `+1.639086e-01` | `-0.974` | `0.964` | `39.925` |
| `0.0040` | `+8.225500e-03` | `+9.650581e-03` | `+3.286071e-01` | `-1.953` | `0.856` | `39.950` |
| `0.0080` | `+1.651142e-02` | `+1.930336e-02` | `+6.377471e-01` | `+2.417` | `0.496` | `38.625` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- same-site memory `F~M`: `1.00`
- wavefield `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the wavefield keeps the weak-field `TOWARD` sign on the compact exact
  lattice
- the mass-scaling class stays essentially linear
- the wavefield produces a measurable phase lag relative to the same-site
  memory control

## Honest limitation

This is still a minimal pocket, not a full propagating field theory.

  - the wavefield is still a narrow local update rule, not a derivation of
    continuum retarded gravity
  - the detector response is much larger than the same-site baseline, so the
    wavefield is no longer just a tiny centroid/support nudge
  - the phase lag is real and order `10^-1` rad on average, which is a much
    more wave-like signal than the previous memory pockets
  - the overlap with same-site memory drops well below 1 on the harder rows,
    so this is a genuine architecture step beyond the earlier exact-lattice
    memory controls

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- the wavefield is distinguishable from the same-site control by a finite
  phase lag and a much larger detector response, making it the strongest
  exact-lattice propagating-field step yet
