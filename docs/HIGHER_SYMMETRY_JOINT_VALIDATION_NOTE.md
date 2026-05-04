# Higher-Symmetry Joint Validation Note

**Date:** 2026-04-03  
**Status:** bounded positive for `Z2 x Z2`, proposed_retained through `N = 120` on a
denser narrow probe
**Primary runner:** [`scripts/higher_symmetry_joint_validation.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_joint_validation.py) (joint Born + gravity + decoherence validator)

This note records the first joint Born + gravity + decoherence validation for
the higher-symmetry families introduced in:

[`scripts/higher_symmetry_dag.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_dag.py)

The joint validator is:

[`scripts/higher_symmetry_joint_validation.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_joint_validation.py)

Logs:

[`logs/2026-04-03-higher-symmetry-joint-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-joint-validation.txt)
[`logs/2026-04-03-higher-symmetry-joint-validation-z2z2-dense-n80-n120.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-joint-validation-z2z2-dense-n80-n120.txt)

## Question

The earlier higher-symmetry pass only checked decoherence. The next real
question was whether the strongest new family, `Z2 x Z2`, still survives the
joint standards used on the retained mirror lane:

- corrected Born `|I3|/P`
- gravity centroid shift
- `k=0` gravity control
- CL-bath purity `pur_cl`

## Setup

- families: random, `Z2 x Z2`, ring
- `32` seeds
- `N = 25, 40, 60, 80`
- same geometry as the higher-symmetry discovery script:
  - random: `50` nodes per layer
  - `Z2 x Z2`: `12` quarter-seeds per layer (`48` total nodes)
  - ring: `48` nodes per layer
- single-`k` joint metric at `k = 5.0`
- small band-averaged gravity read over `k = 3, 5, 7`

The band-averaged gravity read is included because the higher-symmetry families
show stronger single-`k` phase oscillation than the mirror chokepoint lane.

### Dense extension

A narrower density bump was then tested to see whether `Z2 x Z2` could stay
alive at larger `N`:

- `N = 80, 100, 120`
- `16` seeds
- `z2z2-quarter = 16` (`64` total nodes per layer)
- `connect_radius = 5.2`

This extension is the one that reaches `N = 120` while staying Born-clean and
gravity-positive.

## Results

### `Z2 x Z2`

| N | `pur_cl` | decoh `1-pur_cl` | gravity@`k=5` | gravity band | band positive | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 25 | `0.660±0.025` | `0.340` | `+0.059±0.632` | `+0.690±0.323` | `21/30` | `9.02e-16±1.44e-16` | `0.00e+00` |
| 40 | `0.667±0.023` | `0.333` | `+1.196±0.574` | `+0.916±0.403` | `20/30` | `1.24e-15±4.76e-16` | `0.00e+00` |
| 60 | `0.685±0.028` | `0.315` | `+0.823±0.640` | `+1.493±0.454` | `23/30` | `9.86e-16±1.25e-16` | `0.00e+00` |
| 80 | `0.783±0.019` | `0.217` | `+2.771±0.567` | `+1.736±0.337` | `24/30` | `1.48e-15±2.72e-16` | `0.00e+00` |

### Dense `Z2 x Z2` Extension

| N | `pur_cl` | decoh `1-pur_cl` | gravity@`k=5` | gravity band | band positive | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 80 | `0.785±0.035` | `0.215` | `+2.677±0.806` | `+2.713±0.372` | `16/16` | `1.55e-15±3.37e-16` | `0.00e+00` |
| 100 | `0.742±0.040` | `0.258` | `+0.763±0.616` | `+1.431±0.443` | `13/16` | `1.94e-15±3.18e-16` | `0.00e+00` |
| 120 | `0.764±0.036` | `0.236` | `+0.245±0.750` | `+1.356±0.382` | `14/16` | `3.04e-15±1.31e-15` | `0.00e+00` |

### Comparison Families

| family | `pur_cl(N=25)` | `pur_cl(N=80)` | bounded alpha | gravity-band read |
|---|---:|---:|---:|---|
| random | `0.787±0.034` | `0.905±0.018` | `-0.760` | weak / noisy |
| `Z2 x Z2` | `0.660±0.025` | `0.783±0.019` | `-0.335` | positive at all tested `N` |
| ring | `0.716±0.019` | `0.927±0.021` | `-1.088` | positive but weaker as a decoherence lane |

## Exponent Fit

Using the family-mean decoherence depth

`1 - pur_cl ~= C * N^alpha`

the retained bounded fit for `Z2 x Z2` is:

- direct fit: `alpha = -0.335`, `R^2 = 0.643`
- bootstrap: `alpha = -0.335`, `95% CI [-0.509, -0.139]`

For the dense extension:

- direct fit: `alpha = +0.255`, `R^2 = 0.322`
- bootstrap: `alpha = +0.265`, `95% CI [-0.719, +1.303]`

For reference on the same bounded window:

- random: `alpha = -0.760`, bootstrap `[-1.148, -0.379]`
- ring: `alpha = -1.088`, bootstrap `[-1.619, -0.711]`

So the `Z2 x Z2` family really does retain a much slower decoherence decay
than the random baseline on this joint rerun, while the ring family does not.
The dense extension remains Born-clean and gravity-positive through `N = 120`,
but its exponent fit is too noisy to promote as a clean asymptotic law.

## Narrow Read

- `Z2 x Z2` is **Born-clean** at machine precision through the full tested
  window.
- `Z2 x Z2` keeps the **`k=0` control exactly zero**.
- `Z2 x Z2` also keeps a **positive gravity signal** on the band-averaged
  read at all tested `N`, with the strongest support at `N = 60, 80` on the
  discovery geometry and at `N = 80, 100, 120` on the dense extension.
- The `Z2 x Z2` decoherence exponent remains **slow**: about `-0.33` on the
  discovery geometry, with the dense extension too noisy to lock a cleaner
  asymptotic law.
- The ring family is **not** the next winner once the joint tests are imposed:
  it is Born-clean and mildly gravity-positive, but its decoherence scaling is
  closer to the random ceiling than to the `Z2 x Z2` lane.

## Important Scope Note

This note does **not** replace the earlier exact-`Z2` story. The canonical
exact mirror result remains the mirror/chokepoint lane in:

[`docs/MIRROR_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md)

The `Z2` branch inside [`scripts/higher_symmetry_dag.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_dag.py)
is only a node-placement symmetry check, not the exact edge-mirrored
construction used in the retained mirror result.

## Conclusion

The project now has a new bounded higher-symmetry coexistence lane:

- **exact `Z2` mirror** remains the canonical parity-protected story
- **`Z2 x Z2`** extends that symmetry idea into a stronger bounded
  decoherence lane that is still Born-clean and gravity-positive, and now
  remains retained through `N = 120` on a denser narrow probe
- **ring / approximate rotational symmetry** does not survive the joint test
  as cleanly

The most productive next move is now quantitative rather than qualitative:
test whether the `Z2 x Z2` family also inherits a usable distance or mass law
on the dense extension, not just a positive joint gravity signal. Until that
probe lands, the review-safe read is: **decoherence lead yes, gravity-law
contender unproven**.
