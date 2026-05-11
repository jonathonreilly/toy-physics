# Wave Static Boundary Sensitivity

**Date:** 2026-04-08
**Status:** bounded computational boundary probe
**Claim type:** bounded_theorem

This probe asks a narrow question:

> If we enlarge the field box `PW` at one shared `H`, do the direct
> static comparator `dS` and the retarded/static mismatch `rel_MS`
> stay within 5% of their smaller-box values?

The bounded result here is the off-center frozen-source case at
shared `H = 0.5` and frozen source `z_phys = 3.0`.

## Results

| quantity | `PW = 6.0` | `PW = 9.0` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.009857` | `+0.007991` | `18.93%` |
| `dS` | `+0.009507` | `+0.011529` | `17.54%` |
| `rel_MS` | `3.56%` | `30.69%` | `88.41%` |
| static residual | `1.998e-10` | `1.996e-10` | stable |

## Honest read

The boundary sensitivity is material. Enlarging `PW` from `6.0` to
`9.0` at the same `H = 0.5` does not preserve the direct static
comparator or the retarded/static mismatch within 5%.

That means this probe does **not** promote the current direct static
comparator as a boundary-stable baseline. It is still a useful diagnostic,
but the current `dS`/`rel_MS` values are box-dependent at this shared
resolution.

## Artifact chain

- [`scripts/wave_static_boundary_sensitivity.py`](../scripts/wave_static_boundary_sensitivity.py)
