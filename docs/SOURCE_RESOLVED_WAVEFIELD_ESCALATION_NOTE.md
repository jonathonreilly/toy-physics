# Source-Resolved Wavefield Escalation

**Date:** 2026-04-05  
**Status:** larger exact-lattice wavefield escalation, frozen on the retained family

## Artifact chain

- [`scripts/source_resolved_wavefield_escalation.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_wavefield_escalation.py)
- [`logs/2026-04-05-source-resolved-wavefield-escalation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-wavefield-escalation.txt)

## Question

Can the exact-lattice wavefield lane be pushed beyond the compact pocket by
moving to a larger exact family and using a cleaner wave-like observable than a
single phase lag?

This probe stays narrow:

- one larger exact lattice family at `h = 0.25`
- one exact zero-source reduction check
- one instantaneous `1/r` control
- one same-site-memory control
- one finite-speed wavefield candidate
- one weak-field sign / `F~M` gate
- one wave-like observable: detector-line phase-ramp slope and span relative
  to the same-site control

## Frozen result

The frozen larger exact family uses:

- `h = 0.25`
- `W = 4`
- `L = 8`
- source cluster with `5` in-bounds nodes
- `source_z = 2.5`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`, `eps = 0.5`
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

| `s` | instantaneous deflection | same-site deflection | wavefield deflection | phase lag (rad) | ramp slope (rad / z) | ramp R² | wave/same |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.931018e-03` | `+3.658426e-03` | `+1.759245e-01` | `-0.740` | `-0.1215` | `0.959` | `60.022` |
| `0.0020` | `+5.873223e-03` | `+7.321503e-03` | `+3.559416e-01` | `-1.473` | `-0.2444` | `0.959` | `60.604` |
| `0.0040` | `+1.179000e-02` | `+1.466136e-02` | `+7.157359e-01` | `-2.880` | `-0.4925` | `0.960` | `60.707` |
| `0.0080` | `+2.374397e-02` | `+2.939408e-02` | `+1.326988e+00` | `+0.337` | `-1.0274` | `0.966` | `55.887` |

Fitted exponents:

- instantaneous `F~M`: `1.01`
- same-site-memory `F~M`: `1.00`
- wavefield `F~M`: `0.98`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the weak-field sign stays `TOWARD` on the larger exact family
- the mass-scaling class stays essentially linear
- the wavefield is now much more clearly wave-like than the compact pocket:
  - detector-line phase ramp is coherent
  - phase-ramp `R²` stays near `0.96`
  - the ramp span is several radians
  - the detector response is far above the same-site control

## Honest limitation

This is still a minimal exact-lattice wavefield probe, not a full causal-field
theory.

- the wavefield is a narrow local update rule, not a continuum derivation
- the detector line is a stronger observable than a single phase lag, but it is
  still a proxy
- the result is an exact-lattice escalation, not yet a generated-geometry
  transfer

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` remains near `1.00`
- the detector-line phase-ramp observable is a cleaner and stronger wave
  signature than the previous compact pocket
- this is the strongest exact-lattice wavefield step yet
