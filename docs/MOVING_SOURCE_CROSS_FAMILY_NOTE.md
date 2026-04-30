# Moving Source Cross-Family Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow extension positive across two portable grown families

## Artifact Chain

- [`scripts/moving_source_cross_family_probe.py`](/Users/jonreilly/Projects/Physics/scripts/moving_source_cross_family_probe.py)
- [`logs/2026-04-06-moving-source-cross-family-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-moving-source-cross-family-probe.txt)
- first portable moving-source lane:
  - [`docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md)
- second portable family context:
  - [`archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_CARD_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_CARD_EXTENSION_NOTE.md)
  - [`archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_PACKAGE_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_PACKAGE_EXTENSION_NOTE.md)

## Question

Does the bounded moving-source directional observable survive a second
portable grown family under the same exact zero and static controls, or is the
effect local to the first portable family?

This replay stays narrow:

- two portable grown families
- exact zero-source baseline on both families
- matched static-field control at `v = 0`
- one moving-source sweep with signed `v`
- one main observable: final-layer detector centroid `y` shift relative to the
  static control

## Frozen Result

Frozen family rows:

- family 1: `drift = 0.20`, `restore = 0.70`
- family 2: `drift = 0.05`, `restore = 0.30`

Exact baseline:

- zero-source static max `|delta_y| = 0.000e+00` on both families
- zero-source moving max `|delta_y| = 0.000e+00` on both families

Matched static control:

- family 1 at `v = 0.00`: `delta_y vs static = +0.000000e+00`
- family 2 at `v = 0.00`: `delta_y vs static = +0.000000e+00`

Moving-source rows:

| family | `v` | `delta_y vs static` | phase lag |
| --- | ---: | ---: | ---: |
| family 1 | `+0.50` | `+8.665715e-07 ± 1.380e-07` | `+1.401315e-05 ± 2.744e-07` |
| family 1 | `+1.00` | `+1.472200e-06 ± 1.571e-07` | `+4.334258e-05 ± 1.396e-07` |
| family 1 | `-0.50` | `-9.233039e-07 ± 1.986e-07` | `+1.309075e-05 ± 5.927e-07` |
| family 1 | `-1.00` | `-1.641405e-06 ± 3.484e-07` | `+4.852935e-05 ± 1.170e-06` |
| family 2 | `+0.50` | `+9.628235e-07 ± 7.508e-08` | `+1.401789e-05 ± 2.577e-07` |
| family 2 | `+1.00` | `+1.606752e-06 ± 7.161e-08` | `+4.355026e-05 ± 2.640e-07` |
| family 2 | `-0.50` | `-1.030247e-06 ± 1.313e-07` | `+1.334915e-05 ± 4.680e-07` |
| family 2 | `-1.00` | `-1.822671e-06 ± 2.373e-07` | `+4.919546e-05 ± 9.070e-07` |

## Safe Read

The strongest bounded statement is:

- the exact zero baseline survives unchanged on both portable grown families
- the matched static control is still flat at `v = 0`
- the moving-source centroid bias keeps the same signed response pattern on
  the second family, so the effect is not just a one-family artifact
- the phase lag is present but secondary to the directional centroid bias

## Branch Verdict

This is a retained narrow extension positive: the bounded moving-source
directional observable survives on two portable grown families under the same
exact zero and static controls.
