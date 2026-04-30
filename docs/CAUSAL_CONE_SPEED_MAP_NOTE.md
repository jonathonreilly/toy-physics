# Causal Cone Speed Map Note

**Date:** 2026-04-06  
**Status:** bounded cone-speed probe on the center grown family

## Artifact Chain

- [`scripts/causal_cone_speed_map.py`](/Users/jonreilly/Projects/Physics/scripts/causal_cone_speed_map.py)
- [`logs/2026-04-06-causal-cone-speed-map.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-causal-cone-speed-map.txt)
- causal propagating-field context:
  - [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
  - [`docs/CAUSAL_FIELD_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_PORTABILITY_NOTE.md)
  - [`docs/CAUSAL_DISTANCE_TAIL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_DISTANCE_TAIL_NOTE.md)

## Question

On the retained center grown family, does the causal-field observable change
smoothly with cone speed `c`, fall into a few discrete proxy regimes, or act
like a noisy/non-monotone knob?

## Setup

- family: center grown family
- drift / restore: `0.2 / 0.7`
- seeds: `0..5`
- exact zero-source control included first
- `c` values: `0.10, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50`
- proxy source strength: `5.0e-05`

## Result

The exact zero-source control stays exact:

- max `|delta_y| = 0.000e+00`
- max `|field| = 0.000e+00`

The c-sweep is structured, but not monotone across the whole range:

| c | mean delta | ratio / delta | toward |
| --- | ---: | ---: | ---: |
| `0.10` | `-3.444e-08` | `-0.118` | `3/6` |
| `0.25` | `+2.781e-08` | `0.095` | `3/6` |
| `0.50` | `+2.741e-07` | `0.938` | `3/6` |
| `0.75` | `+3.011e-07` | `1.031` | `4/6` |
| `1.00` | `+4.253e-07` | `1.456` | `5/6` |
| `1.25` | `+2.128e-07` | `0.728` | `4/6` |
| `1.50` | `+1.291e-07` | `0.442` | `4/6` |

## Safe Read

What survives:

- the exact-null control is exact
- the finite-cone observable is not random; it varies in a structured way with
  `c`
- the biggest response in this scan sits near `c = 1.0`

What does not survive:

- the full sweep does not behave like a smooth monotone control parameter
- it does not reduce cleanly to just a few stable plateaus either

## Classification

**noisy / non-monotone knob**

## Narrow Conclusion

On the center retained family, cone speed `c` is a real proxy control, but
this scan does not support a clean smooth monotone law. The exact-null control
is robust, yet the response turns over after `c ≈ 1.0`, so the cleanest honest
read is that `c` is a structured but noisy/non-monotone proxy knob on this
family.

Do not read this as a physical wave-speed claim.
