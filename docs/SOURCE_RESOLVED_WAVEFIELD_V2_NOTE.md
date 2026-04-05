# Source-Resolved Wavefield V2 Note

**Date:** 2026-04-05  
**Status:** retained exact-lattice phase-ramp law on the larger exact family

## Artifact chain

- [`scripts/source_resolved_wavefield_v2.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_wavefield_v2.py)
- [`logs/2026-04-05-source-resolved-wavefield-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-wavefield-v2.txt)

## Question

Can the strongest retained exact-lattice wavefield lane be pushed one step
further by turning the detector-line phase-ramp itself into a clean
source-strength law, while keeping exact zero-source reduction and the
weak-field sign?

This v2 probe stays narrow:

- the same retained larger exact family
- the same exact zero-source reduction check
- the same instantaneous `1/r` control
- the same same-site-memory control
- the same finite-speed wavefield candidate
- a slightly denser source-strength ladder
- a promoted observable: detector-line phase-ramp slope and span

## Frozen Result

The frozen larger exact family uses:

- `h = 0.25`
- `W = 4`
- `L = 8`
- source cluster with `5` in-bounds nodes
- `source_z = 2.5`
- source strengths `s = 0.0005, 0.001, 0.002, 0.004, 0.008`
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
| `0.0005` | `+1.464093e-03` | `+1.828628e-03` | `+8.729054e-02` | `-0.369` | `-0.0606` | `0.959` | `59.621` |
| `0.0010` | `+2.931018e-03` | `+3.658426e-03` | `+1.759245e-01` | `-0.740` | `-0.1215` | `0.959` | `60.022` |
| `0.0020` | `+5.873223e-03` | `+7.321503e-03` | `+3.559416e-01` | `-1.473` | `-0.2444` | `0.959` | `60.604` |
| `0.0040` | `+1.179000e-02` | `+1.466136e-02` | `+7.157359e-01` | `-2.880` | `-0.4925` | `0.960` | `60.707` |
| `0.0080` | `+2.374397e-02` | `+2.939408e-02` | `+1.326988e+00` | `+0.337` | `-1.0274` | `0.966` | `55.887` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- same-site-memory `F~M`: `1.00`
- wavefield `F~M`: `0.99`
- phase-ramp slope exponent: `1.02`
- phase-ramp span exponent: `1.01`

Other retained summary numbers:

- `TOWARD` rows: `5/5`
- mean detector phase lag at same-site peak: `-1.025 rad`
- mean detector phase-ramp slope: `-0.3893 rad / z`
- mean detector phase-ramp `R²`: `0.961`
- mean detector phase-ramp span: `+2.751 rad`
- mean detector overlap with same-site baseline: `0.693`
- mean `|wave-same|` centroid delta: `+5.210034e-01`
- mean `|wave/same|` centroid ratio: `47.680`

## Safe Read

The strongest bounded statement is:

- exact zero-source reduction survives
- the weak-field sign stays `TOWARD` on the retained larger exact family
- the mass-scaling class stays essentially linear
- the detector-line phase-ramp is not just present, it now follows a clean
  source-strength law
- both the phase-ramp slope and phase-ramp span scale close to linearly with
  source strength
- the same-site control remains much weaker than the wavefield response

So this is a real next science step, not just a prettier replay:

- the exact-lattice wavefield lane now has a sharper structural discriminator
- the discriminator is the detector-line phase-ramp law itself
- that is a better bridge to later causal-field or self-gravity ideas than a
  single phase-lag number

## Honest Limitation

Do not overstate the next step.

- this is still an exact-lattice retained result, not a continuum theorem
- generated-geometry transfer remains exploratory
- absolute experimental amplitude remains outside the retained claim surface

## Branch Verdict

Treat this as a **retained exact-lattice phase-ramp law**:

- exact zero-source reduction survives
- `TOWARD` survives
- `F~M` stays near `1.00`
- phase-ramp slope and span both scale with source strength at roughly unit
  exponent

This is the strongest exact-lattice wavefield step yet because it turns the
wavefield from a single structural observable into a source-strength law.
