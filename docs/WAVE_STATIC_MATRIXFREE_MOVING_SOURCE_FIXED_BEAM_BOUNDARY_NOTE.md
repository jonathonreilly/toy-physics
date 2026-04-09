# Wave Static Matrix-Free Moving-Source Fixed-Beam Boundary Probe

**Date:** 2026-04-08
**Status:** retained boundary probe — mixed, with a bounded rescue signal

This probe is the moving-source analogue of the frozen-source
fixed-beam boundary test.

It asks:

> At shared `H`, fixed beam geometry, and the Lane 6 source trajectory,
> does the exact discrete static comparator still depend materially on
> the field/static-solve box size?

## Setup

- shared `H = 0.35`
- fixed beam `PW_phys = 6.0`
- moving source on the standard Lane 6 trajectory
- matrix-free exact discrete static solve
- two field/static-solve boxes:
  - `PW_phys = 6.0`
  - `PW_phys = 9.0`
- same beam DAG for both runs

## Result

| quantity | field `PW = 5.95` | field `PW = 9.10` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.007942` | `+0.007973` | `0.39%` |
| `dS` | `+0.006111` | `+0.007720` | `20.84%` |
| `rel_MS` | `23.05%` | `3.18%` | `86.21%` |
| matrix-free residual | `2.292e-10` | `1.984e-10` | stable |
| matrix-free iterations | `87` | `128` | converged |

The realized motion parameters were the same in both runs:

- `NL = 43`
- `src_layer = 14`
- `iz_start = 9`
- `iz_end = 0`
- realized `v/layer = -0.3103`

## Honest read

This is a mixed result.

What stays negative:

- the exact moving-source static comparator is still materially
  field-box sensitive at `H = 0.35`
- `dS` moves by `20.84%`
- `rel_MS` moves by `86.21%`
- so there is still no boundary-stable quantitative comparator claim

What is genuinely encouraging:

- `dM` is almost unchanged (`0.39%`)
- on the larger field box, the exact static comparator gets close to
  the retarded response:
  - `rel_MS = 3.18%`
  - `dS = +0.007720` versus `dM = +0.007973`

So this lane does **not** rescue the exact-comparator story yet, but it
does sharpen the target:

- the problem is not that exact static and retarded responses are
  generically far apart
- the problem is that the exact static comparator is still boundary
  dependent on the smaller field box

## Follow-on test: does the large-box branch start to stabilize?

The initial `6.0 -> 9.0` field-box move leaves open a narrower question:

> Once the exact static comparator is already on a large field box,
> does the *next* box enlargement become small?

At the same shared `H = 0.35`, fixed beam `PW_phys = 6.0`, the probe was
extended from `field PW_phys = 9.0` to `12.0`.

| quantity | field `PW = 9.10` | field `PW = 11.90` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.007973` | `+0.007973` | `0.00%` |
| `dS` | `+0.007720` | `+0.008171` | `5.52%` |
| `rel_MS` | `3.18%` | `2.42%` | `23.94%` |
| matrix-free residual | `1.984e-10` | `1.865e-10` | stable |
| matrix-free iterations | `128` | `166` | converged |

This keeps the branch in the same honest box, but with a sharper read:

- the exact comparator is still **not** promoted:
  - `dS` is still just above a strict `5%` stability bar
  - `rel_MS` still moves materially
- but the large-box branch is no longer behaving like the small-box
  branch:
  - `dM` is unchanged at the shown precision
  - `dS` now moves only `5.52%`, not `20.84%`
  - `rel_MS` stays low at `3.18% -> 2.42%`

So the best current read is:

> the exact comparator is still not retained as a continuum-quality
> moving-source baseline, but the medium-`H` large-box branch looks like
> a plausible stabilization candidate rather than a dead end.

The next decisive run on this branch is now:

- `H = 0.25`
- fixed beam `PW_phys = 6.0`
- compare large field boxes directly (`9.0 -> 12.0`), not
  `6.0 -> 9.0`

## Artifact chain

- [`scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary.py`](../scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary.py)
- [`scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary_freeze.py`](../scripts/wave_static_matrixfree_moving_source_fixed_beam_boundary_freeze.py)
- [`logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035.txt`](../logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035.txt)
- [`logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035-wide.txt`](../logs/2026-04-08-wave-static-matrixfree-moving-source-fixed-beam-boundary-h035-wide.txt)
