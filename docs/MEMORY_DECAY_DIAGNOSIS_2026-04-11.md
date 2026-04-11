# Memory Signal Decay — Protocol Fragility and Screening

**Date:** 2026-04-11

## The Data
  N=41:  memory = +0.47 (strong — lattice within screening range)
  N=61:  memory = +0.013 (original result)
  N=81:  memory ~ 1e-5 (vanishing)
  N=101: memory ~ 1e-7 (gone)

## What the first sweep suggested

The original ring protocol used a screened field with `mu^2 = 0.22`. In the
original size-scaled setup, the marker/source geometry moved outward with `N`,
and the memory signal collapsed with size.

Screening length in the operator convention is `ell_screen = 1/sqrt(mu^2)`.
For the original scanned values:

| N | source-marker distance | `ell_screen` | memory trend |
|---|----------------|-----------|------------|
| 41 | ~10 | 2.13 | strong |
| 61 | ~15 | 2.13 | positive but small |
| 81 | ~20 | 2.13 | vanishing |
| 101 | ~25 | 2.13 | gone |

That first pass was consistent with a screening-limited protocol, but it did
not isolate whether Yukawa range was the only cause.

## Follow-up sweep

The later `mu^2` / geometry sweep changed the interpretation:

- when the source/marker geometry was scaled with `N`, the memory still
  decreased strongly with size even as `mu^2` was lowered to `0`
- when the geometry was held fixed, the memory survived and actually grew
  with `N`, with only weak dependence on `mu^2`

That means the original collapse was **not primarily a Yukawa-range artifact**.
Screening contributes, but geometry scaling and boundary placement are the
dominant confounds.

## Assessment

The narrow `N=61` ring signal is real, but the original protocol is too
geometry-sensitive to support a publication-grade memory claim.

## Fix

Future reruns should:

- keep the marker/source geometry fixed while increasing `N`
- use a more direct arrival-time / displacement observable
- treat `mu^2 = 0` as one control, not the sole explanation

The memory result remains exploratory, but the failure mode is now better
understood and less singular than the original Yukawa diagnosis suggested.
