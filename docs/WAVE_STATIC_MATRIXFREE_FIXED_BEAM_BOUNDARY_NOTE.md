# Wave Static Matrix-Free Fixed-Beam Boundary Probe

**Date:** 2026-04-08
**Status:** bounded computational side probe
**Claim type:** bounded_theorem

This probe is the next narrow rescue attempt for the exact discrete
static comparator lane.

It keeps the beam DAG fixed at the baseline beam box, enlarges only the
field/static solve box, and uses the matrix-free exact discrete static
solver.

The question is:

> At a finer shared `H`, does the exact discrete static comparator still
> show material field-box sensitivity when the beam geometry is held
> fixed?

## What it compares

- frozen source at a single fixed `z_phys`
- fixed beam box at `PW = 6.0`
- field/static solve box widened from `PW = 6.0` to `PW = 9.0`
- matrix-free exact discrete static solve, cropped back to the beam box
- retarded-wave response `dM` through the same beam DAG
- direct static response `dS` through the same beam DAG

## Why this is the right rescue test

The earlier boundary test changed both the field box and the beam DAG.
This probe removes that confound by holding the beam geometry fixed.
If the boundary sensitivity survives here, the comparator lane is still
box-dependent in a physically meaningful way.

## Result

The current bounded run uses shared `H = 0.35`, fixed beam
`PW_phys = 6.0`, frozen source `z_phys = 3.0`, and compares
`field PW_phys = 6.0` vs `9.0`.

| quantity | `field PW = 5.95` | `field PW = 9.10` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.008380` | `+0.008428` | `0.57%` |
| `dS` | `+0.010863` | `+0.014721` | `26.21%` |
| `rel_MS` | `22.86%` | `42.75%` | `46.52%` |
| matrix-free residual | `2.292e-10` | `1.585e-10` | stable |
| matrix-free iterations | `86` | `126` | converged |

## Honest read

At medium `H`, the matrix-free fixed-beam boundary probe reproduces the
same scientific conclusion as the direct-solve branch:

- enlarging only the field/static solve box still moves `dS` by
  `26.21%`
- `rel_MS` still moves materially, by `46.52%`
- `dM` is comparatively stable, moving only `0.57%`

So the matrix-free engine changes the engineering envelope, but not the
science read. The fixed-beam field-box dependence survives.

This is useful because it removes one possible escape hatch:

> the comparator lane is not weak because of the direct static solver;
> it is weak because the static baseline itself remains materially
> field-box dependent.

The `H = 0.25` matrix-free fixed-beam run is still not established here.
The current side-thread only shows that at shared `H = 0.35`, the
matrix-free engine agrees with the existing negative rather than
rescuing it.

## Artifact chain

- [`scripts/wave_static_matrixfree_fixed_beam_boundary.py`](../scripts/wave_static_matrixfree_fixed_beam_boundary.py)
