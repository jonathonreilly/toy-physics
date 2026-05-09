# 3D 1/L^2 Tail Statistics Note

**Date:** 2026-04-04  
**Status:** bounded - bounded or caveated result note

## Purpose

This note freezes a narrow follow-up on the exploratory 3D `1/L^2`
propagator fork. The question is not whether the branch is promoted; it is
whether widening the `h = 0.25` lattice improves the post-peak tail fit
without losing the same-family barrier sanity checks.

Artifact chain:

- [`scripts/lattice_3d_l2_tail_stats.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_tail_stats.py)
- [`scripts/lattice_3d_inverse_square_kernel.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_inverse_square_kernel.py)
- [`logs/2026-04-04-lattice-3d-l2-tail-stats.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-l2-tail-stats.txt)

## Result

The wider `h = 0.25` probe at `width = 8` stayed review-clean on the same
barrier geometry:

- Born: `3.75e-15`
- `k=0`: `0.000000`
- `dTV`: `0.358`
- barrier read: `ATTRACTIVE`

The no-barrier rows remained attractive across the post-peak sample:

| `z` | centroid | `P_near` | bias | read |
|---|---:|---:|---:|---|
| 4 | `+0.049373` | `+0.004422` | `+0.795766` | attractive |
| 5 | `+0.046445` | `+0.003459` | `+0.765371` | attractive |
| 6 | `+0.040248` | `+0.001309` | `+0.719169` | attractive |
| 7 | `+0.035067` | `+0.000651` | `+0.668926` | attractive |
| 8 | `+0.030697` | `+0.000357` | `+0.627323` | attractive |

Tail fit on the post-peak segment:

- `peak@z = 4`
- `n_tail = 5`
- exponent `b^(-0.70)`
- `R^2 = 0.955`

## Comparison

This is a real improvement over the earlier `h = 0.25`, width-6 readout that
had fewer post-peak points and a weaker tail fit (`b^(-0.53)` in the retained
summary). The wider lattice gives:

- more post-peak support points
- a steeper tail
- slightly better `R^2`

The right review-safe wording is still narrow:

- the wider lattice **improves the post-peak tail fit**
- it does **not** by itself prove an asymptotic `-2` law
- it remains a propagator-fork probe, not a promoted branch theorem

## Registered runner artifacts (audit lane)

The runner source backing the rows above is present in the worktree:

- `scripts/lattice_3d_l2_tail_stats.py` — primary runner for the tail-fit
  rows reported above.
- `scripts/lattice_3d_inverse_square_kernel.py` — companion kernel module
  imported by the primary runner.

The historical log file `logs/2026-04-04-lattice-3d-l2-tail-stats.txt` is the
recorded stdout from a prior run. The `logs/runner-cache/` artifact for this
runner is not yet present; the note's bounded read above does not promote a
result tier and remains a propagator-fork probe pending registered cache.

