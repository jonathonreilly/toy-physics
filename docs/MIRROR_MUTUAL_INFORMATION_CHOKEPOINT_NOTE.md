# Mirror Mutual Information Chokepoint Note

**Date:** 2026-04-03  
**Status:** canonical exact-mirror MI artifact chain on the retained dense chokepoint family

This note freezes the mirror-specific mutual-information question on the
retained exact mirror chokepoint family, using the same linear propagator and
same slit/detector geometry as the review-safe mirror chokepoint pocket.

Script:
[`scripts/mirror_mutual_information_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_chokepoint.py)

Log:
[`logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt)

## Question

Does the exact mirror chokepoint family retain which-slit information more
strongly than a matched random chokepoint baseline, and if so, does that hold
cleanly enough to support an asymptotic law?

## Setup

- families: exact mirror chokepoint, matched random chokepoint baseline
- `16` seeds
- `N = 40, 60, 80, 100`
- `npl_half = 60` (`120` total nodes per layer for the mirror family)
- `connect_radius = 5.0`
- `layer2_prob = 0.0`
- MI evaluated on the same exact linear propagator as the retained mirror pocket
- `k = 5.0`

## Retained Rows

The exact mirror family keeps a clear mid-N MI advantage over the matched
random baseline, but the comparison is not monotone and does not support a
clean slower-decay theorem:

| N | random MI | mirror MI | random pur_cl | mirror pur_cl |
|---|---:|---:|---:|---:|
| 40 | `0.1774±0.034` | `0.4295±0.068` | `0.8368±0.04` | `0.8608±0.03` |
| 60 | `0.0846±0.032` | `0.1973±0.041` | `0.8928±0.03` | `0.8440±0.03` |
| 80 | `0.0564±0.018` | `0.1385±0.021` | `0.9509±0.02` | `0.8182±0.03` |
| 100 | `0.0574±0.021` | `0.0408±0.011` | `0.9188±0.03` | `0.9043±0.02` |

## Descriptive Fits

These fits summarize the retained window, but they are not a clean asymptotic
law:

```text
mirror MI      ~= 2973.2137 × N^(-2.363)   R²=0.909
random MI      ~= 19.3325 × N^(-1.299)     R²=0.918
mirror 1-pur   ~= 0.3906 × N^(-0.246)      R²=0.126
random 1-pur   ~= 6.3099 × N^(-1.010)      R²=0.629
```

Interpretation:

- The exact mirror family clearly beats the matched random baseline in MI at
  `N = 40, 60, 80`.
- The advantage is not monotone, because the `N = 100` row falls below the
  random baseline in MI.
- The CL-bath purity tells a slightly different story: mirror is more
  decohering than random at `N = 60, 80, 100`, but slightly less decohering at
  `N = 40`.
- The MI and CL-bath metrics are therefore related but not identical on this
  family.

## Retained Conclusion

- The exact mirror chokepoint family has a real, review-safe, bounded MI
  advantage over the matched random baseline.
- The strongest supported statement is **mid-N advantage**, not a clean
  asymptotic law.
- If you need one canonical line, it is:
  - **mirror preserves which-slit information better than random in the
    retained dense window, but the exponent fit is too noisy to claim a
    global slower-decay theorem.**
