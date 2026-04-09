# Moving Source Retarded Portability Note

**Date:** 2026-04-06  
**Status:** bounded moving-source / retarded-source proxy on a portable grown row

## Artifact chain

- [`scripts/moving_source_retarded_portability_probe.py`](/Users/jonreilly/Projects/Physics/scripts/moving_source_retarded_portability_probe.py)
- [`logs/2026-04-06-moving-source-retarded-portability-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-moving-source-retarded-portability-probe.txt)

## Question

Does a moving-source proxy leave a real directional observable on a portable
grown family, or does it collapse to static-field replay once the exact
zero baseline is enforced?

This note is intentionally narrow:

- one portable retained grown row: `drift = 0.2`, `restore = 0.7`
- exact zero-source baseline check
- matched static-field control at `v = 0`
- one moving-source sweep with signed `v`
- one main observable: final-layer detector centroid `y` shift relative to the static control

## Frozen Result

Frozen run settings:

- `seeds = 6`
- `source_layer = 8`
- `h = 0.5`
- source anchor target: `(y, z) = (0.0, 3.0)`
- motion law: `y_src(layer) = y0 + v * (layer - source_layer) * h`

Exact baseline:

- zero-source static max `|delta_y| = 0.000e+00`
- zero-source moving max `|delta_y| = 0.000e+00`

Matched static control:

- `v = 0.00`
- `delta_y vs free = +2.921491e-07 ± 6.816e-07`
- `delta_y vs static = +0.000000e+00 ± 0.000e+00`
- `phase lag = +0.000000e+00 ± 0.000e+00`

Moving-source rows:

| `v` | `delta_y vs free` | `delta_y vs static` | `phase lag (rad)` |
| --- | ---: | ---: | ---: |
| `+0.50` | `+1.158721e-06 ± 8.048e-07` | `+8.665715e-07 ± 1.380e-07` | `+1.401315e-05 ± 2.744e-07` |
| `+1.00` | `+1.764349e-06 ± 8.125e-07` | `+1.472200e-06 ± 1.571e-07` | `+4.334258e-05 ± 1.396e-07` |
| `-0.50` | `-6.311548e-07 ± 5.243e-07` | `-9.233039e-07 ± 1.986e-07` | `+1.309075e-05 ± 5.927e-07` |
| `-1.00` | `-1.349256e-06 ± 4.309e-07` | `-1.641405e-06 ± 3.484e-07` | `+4.852935e-05 ± 1.170e-06` |

## Safe Read

The strongest bounded statement is:

- the exact zero baseline survives unchanged
- the moving-source rows do not collapse into static replay, because the
  centroid `y` bias flips sign with `v`
- the phase lag is small but nonzero, so there is a secondary delay-like
  residue, but the clean survivor is the direction observable
- the effect is modest, not a wave claim, and should be read as a moving-source
  proxy on a portable grown geometry row

## Branch Verdict

This is a small positive on the portable grown row, not a universal theorem.
It shows one signed moving-source observable that survives the exact zero
baseline and the matched static-field control.
