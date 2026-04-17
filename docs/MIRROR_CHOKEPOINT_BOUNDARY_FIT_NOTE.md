# Mirror Chokepoint Boundary Fit Note

**Date:** 2026-04-03  
**Status:** canonical fit for the retained dense boundary mirror pocket

This note freezes the strongest retained mirror boundary family on `main`.
The fit is intentionally cautious: it summarizes the retained window, but it
does not claim a clean asymptotic law.

[`scripts/mirror_chokepoint_joint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_chokepoint_joint.py)

Canonical log:
[`logs/2026-04-03-mirror-chokepoint-boundary-canonical-n60-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-chokepoint-boundary-canonical-n60-r5p0.txt)

## Setup

- strict layer-1 chokepoint connectivity
- `NPL_HALF = 60` (`120` total nodes per layer)
- `connect_radius = 5.0`
- `layer2_prob = 0.0`
- `k = 5.0`
- `16` seeds
- retained `N = 40, 60, 80, 100`
- gravity wall at `N = 120`

## Retained Rows

The retained boundary pocket is Born-clean and gravity-positive through
`N = 100`:

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|
| 40 | `0.6884` | `0.8608±0.03` | `0.9850` | `+4.7499±0.666` | `1.05e-15` | `0.00e+00` |
| 60 | `0.4791` | `0.8440±0.03` | `0.9953` | `+3.9733±0.473` | `1.54e-15` | `0.00e+00` |
| 80 | `0.4291` | `0.8182±0.03` | `1.0029` | `+3.0551±0.672` | `2.43e-15` | `0.00e+00` |
| 100 | `0.2308` | `0.9043±0.02` | `1.0058` | `+1.3089±0.570` | `1.13e-15` | `0.00e+00` |

`N = 120` is still Born-clean, but gravity collapses to zero and the row is
not retained.

## Canonical Decoherence Fit

Fit on the retained rows only, using `1 - pur_cl`:

```text
(1 - pur_cl) = 0.3901 × N^(-0.245)
R² = 0.126
```

Interpretation:

- This is the canonical fit for the retained dense boundary mirror family.
- It is intentionally weak: the retained values are not monotone, so the fit
  should be read as a descriptive summary of the window, not a robust
  asymptotic law.
- If taken literally, the fit gives:
  - `pur_cl = 0.95` at `N ≈ 4.32e3`
  - `pur_cl = 0.99` at `N ≈ 3.05e6`
- Those extrapolations are only illustrative because the fit quality is poor.

## Retained Conclusion

- The boundary mirror family is a real Born-clean, gravity-positive, decohering
  pocket through `N = 100`.
- The canonical decoherence fit is weak and non-monotone.
- `N = 120` is the gravity wall for this fixed family/config.

So the safe statement is:

- **mirror boundary pocket:** yes
- **canonical exponent fit:** `alpha = -0.245`, weak
- **bounded asymptotic claim:** no, not yet
