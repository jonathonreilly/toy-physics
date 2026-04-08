# Wave Static Fixed-Beam Boundary Sensitivity

**Date:** 2026-04-08
**Status:** retained boundary probe

This probe isolates the boundary question more carefully than the
previous field-box test:

> Keep the beam DAG fixed at the baseline beam box, enlarge only the
> field/static solve box, then crop the enlarged field back to the
> baseline beam box before propagation.

That removes the most obvious confound in the earlier boundary test:
changing `PW` changed both the field solve and the beam geometry.

## Results

The probe used shared `H = 0.5`, fixed beam `PW_phys = 6.0`, frozen
source `z_phys = 3.0`, and compared `field PW_phys = 6.0` vs `9.0`.

| quantity | `field PW = 6.0` | `field PW = 9.0` | move |
| --- | ---: | ---: | ---: |
| `dM` | `+0.009857` | `+0.010629` | `7.26%` |
| `dS` | `+0.013268` | `+0.017944` | `26.06%` |
| `rel_MS` | `25.71%` | `40.76%` | `36.94%` |
| static residual | `1.998e-10` | `1.996e-10` | stable |

## Honest read

The fixed-beam probe still shows material boundary sensitivity:

- enlarging only the field/static solve box from `6.0` to `9.0` moves
  `dS` by `26.06%`
- `rel_MS` also moves materially, by `36.94%`
- `dM` is less sensitive than the comparator, but it still moves by
  `7.26%`

So the earlier boundary negative was not just a beam-geometry confound.
Fixing the beam DAG helps isolate the problem, but it does not remove it.
The exact discrete static comparator is still box-dependent at this shared
resolution.

## Artifact chain

- [`scripts/wave_static_fixed_beam_boundary_sensitivity.py`](../scripts/wave_static_fixed_beam_boundary_sensitivity.py)
