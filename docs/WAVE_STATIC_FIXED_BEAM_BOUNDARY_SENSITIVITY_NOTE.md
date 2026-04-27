# Wave Static Fixed-Beam Boundary Sensitivity

**Date:** 2026-04-08
**Status:** proposed_retained boundary probe

This probe isolates the boundary question more carefully than the
previous field-box test:

> Keep the beam DAG fixed at the baseline beam box, enlarge only the
> field/static solve box, then crop the enlarged field back to the
> baseline beam box before propagation.

That removes the most obvious confound in the earlier boundary test:
changing `PW` changed both the field solve and the beam geometry.

## Results

The retained probe used a fixed beam `PW_phys = 6.0`, frozen source
`z_phys = 3.0`, and compared `field PW_phys = 6.0` vs `9.0`.

### Shared `H = 0.5`

| quantity | `field PW = 6.0` | `field PW = 9.0` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.009857` | `+0.010629` | `7.26%` |
| `dS` | `+0.009507` | `+0.013637` | `30.29%` |
| `rel_MS` | `3.56%` | `22.06%` | `83.88%` |
| static residual | `1.998e-10` | `1.996e-10` | stable |

### Shared `H = 0.35`

| quantity | `field PW = 5.95` | `field PW = 9.10` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.008380` | `+0.008428` | `0.57%` |
| `dS` | `+0.010863` | `+0.014721` | `26.21%` |
| `rel_MS` | `22.86%` | `42.75%` | `46.52%` |
| static residual | `1.997e-10` | `1.998e-10` | stable |

## Honest read

The fixed-beam probe still shows material boundary sensitivity, and the
effect persists at medium `H`.

- at shared `H = 0.5`, enlarging only the field/static solve box from
  `6.0` to `9.0` moves `dS` by `30.29%` and `rel_MS` by `83.88%`
- at shared `H = 0.35`, the same test still moves `dS` by `26.21%`
  and `rel_MS` by `46.52%`
- `dM` is much less sensitive than the comparator:
  `7.26%` move at `H = 0.5`, and only `0.57%` at `H = 0.35`

So the earlier boundary negative was not just a beam-geometry confound.
Fixing the beam DAG helps isolate the problem, but it does not remove it.
The exact discrete static comparator is still box-dependent at this shared
resolution, and the field-box dependence is now visible at both coarse
and medium `H`.

## Artifact chain

- [`scripts/wave_static_fixed_beam_boundary_sensitivity.py`](../scripts/wave_static_fixed_beam_boundary_sensitivity.py)
