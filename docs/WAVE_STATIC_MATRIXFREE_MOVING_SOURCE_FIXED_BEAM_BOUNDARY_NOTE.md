# Wave Static Matrix-Free Moving-Source Fixed-Beam Boundary Probe

**Date:** 2026-04-08
**Status:** retained negative side probe

This is the moving-source analogue of the frozen-source fixed-beam
boundary probes.

It asks the directly relevant comparator question:

> At a shared `H` and fixed beam geometry, does the exact discrete static
> comparator remain materially field-box sensitive when the source moves
> through the Lane 6 trajectory?

## What it compares

- moving source on the standard Lane 6 history
- fixed beam box at `PW = 6.0`
- field/static solve box widened from `PW = 6.0` to `9.0`
- matrix-free exact discrete static solve, cached by visited source `z`
- retarded-wave response `dM` through the same fixed beam DAG
- exact static response `dS` through the same fixed beam DAG

## Why this is the right rescue test

This is the cleanest medium-`H` check of the exact-comparator rescue story:

- the source motion is the real moving-source Lane 6 history
- the beam geometry is fixed
- only the field/static solve box changes

If the exact static baseline still moves materially here, the comparator
problem is not a direct-solver artifact and not just a frozen-source quirk.

## Result

The retained run uses shared `H = 0.35`, fixed beam `PW_phys = 6.0`,
and compares `field PW_phys = 6.0` vs `9.0`.

| quantity | `field PW = 5.95` | `field PW = 9.10` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.007942` | `+0.007973` | `0.39%` |
| `dS` | `+0.006111` | `+0.007720` | `20.84%` |
| `rel_MS` | `23.05%` | `3.18%` | `86.21%` |
| matrix-free residual | `2.292e-10` | `1.984e-10` | stable |
| matrix-free iterations | `87` | `128` | converged |
| cached static solves | `10` | `10` | same history |

## Honest read

This is a useful negative.

The exact static comparator does move **toward** the retarded response when
the field box is enlarged:

- `rel_MS` drops from `23.05%` to `3.18%`

But the key quantity is not the improved large-box fit by itself. The key
quantity is the sensitivity:

- widening only the field box moves `dS` by `20.84%`
- the corresponding `rel_MS` changes by `86.21%`
- `dM` itself moves only `0.39%`

So at medium `H`, the moving-source exact static comparator is still not
boundary-stable enough to promote as the quantitative `c = infinity`
baseline.

What this does show is narrower and still useful:

- the matrix-free engine is not the problem
- the exact-static baseline can be pulled much closer to `dM`
- but the current finite-box exact-static baseline is still dominated by
  box choice

That means the exact-comparator lane is still alive in principle, but not
yet promotable on the current field-box setup.

## Boundary

This note does **not** show:

- a converged exact static baseline
- a restored continuum-stable retardation magnitude
- a reason to replace the direct-`dM` lane as the current clean flagship

The current honest ranking is:

- direct `dM`: still the clean retained moving-source observable
- exact static comparator: still a live rescue attempt, but boundary-limited

## Artifact chain

- [`scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary.py`](../scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary.py)
- [`logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035.txt`](../logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035.txt)
