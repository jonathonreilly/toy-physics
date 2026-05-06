# Higher-Symmetry Gravity Probe Note

**Date:** 2026-04-03 (originally); 2026-05-03 (review-loop scope-narrow)
**Claim type:** bounded_theorem
**Status:** bounded support theorem: positive-row bump fit inside `M ∈ {2,3,5,8}`; not rowwise-positive and not a clean gravity-law contender

This note records the gravity-side follow-up to the higher-symmetry joint
validation.

Script:
[`scripts/higher_symmetry_gravity_probe.py`](../scripts/higher_symmetry_gravity_probe.py)

Audit cache:
[`logs/runner-cache/higher_symmetry_gravity_probe.txt`](../logs/runner-cache/higher_symmetry_gravity_probe.txt)

Log:
[`logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt`](../logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt)

## Runner/cache closure (2026-05-06)

The audit-facing runner defaults now match this note's dense surface:
`N = 80, 100, 120`, `16` seeds, `z2z2-quarter = 16`,
`connect_radius = 5.2`, `anchor_b = 5.0`, and `mass_count = 4`.
The SHA-pinned audit cache linked above is the completed runner record for
that surface.

The mass power-law fit is a **positive-row subfit inside** the declared
window `M ∈ {2,3,5,8}`. The runner source filters the fit inputs to rows
with `delta > 0`; therefore the claim is not rowwise positivity throughout
`{2,3,5,8}`. The excluded in-window negative rows are visible in the table
below: `N=80, M=2` and `N=100, M=3`.

## Review-loop scope-narrow (2026-05-03)

The 2026-05-03 audit identified two over-broad statements in the original
note:

1. **"Gravity-positive" was asserted globally**, but the fixed-anchor data
   contains negative-delta rows, including `N=80 M∈{1,2}`;
   `N=100 M∈{1,3}`; `N=120 M=16`. The honest claim is restricted to the
   **positive-row subfit inside `M ∈ {2,3,5,8}`** where the power-law fit is
   computed.
2. **"Does not lose Born safety at N=120"** is asserted from external
   context, but the runner [`scripts/higher_symmetry_gravity_probe.py`](../scripts/higher_symmetry_gravity_probe.py)
   does not check Born safety on this surface. The Born-safety claim is
   removed from this note; if a Born-safety statement is needed for the
   coexistence-lane reading, it must come from a separate registered runner.

## Question

Does the dense `Z2 x Z2` extension inherit a usable gravity-side mass window
or distance tail, or does gravity flatten out as the symmetry lane is widened?

The probe uses the same slit/detector geometry as the joint validator and
checks:

- fixed-anchor mass windows
- fixed-mass distance sweeps
- the same phase-mediated `k`-band readout used in the joint note

## Dense Extension Setup

- `N = 80, 100, 120`
- `16` seeds
- `z2z2-quarter = 16` (`64` total nodes per layer)
- `connect_radius = 5.2`
- `anchor_b = 5.0`
- `mass_count = 4`

## Fixed-Anchor Mass Window — full row data (added 2026-05-03)

Honest row-by-row data including negative-delta rows outside the fit window:

| N | M | delta | SE | t | sign |
|---:|---:|---:|---:|---:|:---|
| 80 | 1 | -0.1881 | 0.4222 | -0.45 | **negative** |
| 80 | 2 | -0.2732 | 0.4081 | -0.67 | **negative** |
| 80 | 3 | +0.8074 | 0.4132 | +1.95 | positive |
| 80 | 5 | +1.1941 | 0.4622 | +2.58 | positive |
| 80 | 8 | +1.6421 | 0.5366 | +3.06 | positive |
| 80 | 12 | +1.2832 | 0.4871 | +2.63 | positive |
| 80 | 16 | +0.9455 | 0.5560 | +1.70 | positive |
| 100 | 1 | -0.1708 | 0.3845 | -0.44 | **negative** |
| 100 | 2 | +0.1708 | 0.4558 | +0.37 | positive |
| 100 | 3 | -0.0479 | 0.3739 | -0.13 | **negative** |
| 100 | 5 | +0.9033 | 0.4346 | +2.08 | positive |
| 100 | 8 | +0.9971 | 0.4381 | +2.28 | positive |
| 100 | 12 | +0.3419 | 0.3970 | +0.86 | positive |
| 100 | 16 | +0.7421 | 0.4317 | +1.72 | positive |
| 120 | 1 | +0.3716 | 0.2805 | +1.32 | positive |
| 120 | 2 | +0.0814 | 0.3571 | +0.23 | positive |
| 120 | 3 | +0.2745 | 0.4006 | +0.69 | positive |
| 120 | 5 | +0.8950 | 0.4853 | +1.84 | positive |
| 120 | 8 | +0.4396 | 0.3147 | +1.40 | positive |
| 120 | 12 | +0.4172 | 0.3927 | +1.06 | positive |
| 120 | 16 | -0.1194 | 0.3448 | -0.35 | **negative** |

The power-law fit is computed from positive rows inside the window
`M ∈ {2,3,5,8}` (chosen upstream by the joint-validator setup). Row signs
are not hidden: the in-window negative rows are excluded from the fit by
the runner's `delta > 0` guard, and the fitted positive rows are listed
explicitly:

| N | fit rows inside `M ∈ {2,3,5,8}` | positive-row fit |
|---:|:---|:---|
| 80 | `{3,5,8}` | `delta ~= 0.3668 * M^0.724`, `R^2 = 0.999` |
| 100 | `{2,5,8}` | `delta ~= 0.0748 * M^1.348`, `R^2 = 0.918` |
| 120 | `{2,3,5,8}` | `delta ~= 0.0504 * M^1.318`, `R^2 = 0.622` |

## Fixed-Distance Sweep

The distance response remains positive within the audited `b ∈ [2,12]`
range, but the tail is not a clean retained gravity law:

| N | peak | tail fit |
|---|---|---|
| 80 | `b = 6.0` | `delta ~= C * b^-2.132`, `R^2 = 0.562` |
| 100 | `b = 6.0` | `delta ~= C * b^0.751`, `R^2 = 0.014` |
| 120 | `b = 4.0` | `delta ~= C * b^-0.563`, `R^2 = 0.151` |

## Narrow Read (scope-narrowed 2026-05-03)

- **Inside the declared fit window `M ∈ {2,3,5,8}`** the dense `Z2 x Z2`
  extension shows a positive-row mass-bump fit with high `R^2` at
  `N = 80` and degrading but still positive-row bump-fits at
  `N = 100, 120`.
- The in-window negative rows `N=80, M=2` and `N=100, M=3` are not fit
  inputs, so the note does **not** claim rowwise positivity throughout the
  whole set `{2,3,5,8}`.
- **Outside the fit window** there are explicit negative-delta rows at low
  `M` (and at `M = 16` for `N = 120`). The note no longer claims global
  gravity-positivity.
- The distance response is a broad bump / plateau across `b ∈ [2,12]`
  rather than a clean retained law.
- So this lane is a real bounded fit-window positive-row bump, but it is
  **not** the cleanest gravity law in the project.

## Conclusion (scope-narrowed 2026-05-03)

The dense `Z2 x Z2` extension survives as a review-safe coexistence-lane
*candidate* on the fit-window-restricted bump. The Born-safety reading
this note previously asserted is removed; that claim must come from a
separate registered runner if needed.

The honest current interpretation is:

- **decoherence lead:** yes (from upstream joint-validator notes, not
  re-derived here)
- **positive-row gravity bump fit inside `M ∈ {2,3,5,8}`:** yes
- **rowwise gravity-positive on all of `M ∈ {2,3,5,8}`:** **no**
- **gravity-positive globally:** **no** (negative rows at `M = 1, 2, 16`
  for various `N`)
- **Born safety at `N = 120`:** **not checked here** (this note does not
  carry that claim)
- **gravity-law contender:** not yet
