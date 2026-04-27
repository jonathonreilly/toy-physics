# Impact-Parameter Lensing Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow positive on the strongest portable grown row

## Artifact Chain

- [`scripts/impact_parameter_lensing_probe.py`](/Users/jonreilly/Projects/Physics/scripts/impact_parameter_lensing_probe.py)
- [`logs/2026-04-06-impact-parameter-lensing-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-impact-parameter-lensing-probe.txt)
- retained portability context:
  - [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md)
  - [`docs/DISTANCE_LAW_BREAKPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_BREAKPOINT_NOTE.md)
  - [`logs/2026-04-06-distance-law-grown-geometry.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-distance-law-grown-geometry.txt)

## Question

Does the zero-field control stay exact, and does the strongest portable grown
row support a stable deflection-vs-impact-parameter law?

This note is intentionally bounded:

- exact/null control first
- one retained grown row only
- same impact-parameter sweep as the frozen distance-law replay

## Result

The control is clean, and the strongest portable grown row retains the law.

Exact/null control:

- zero-field replay at `b=8`: `delta = +0.000000e+00`

Retained grown row:

| b | delta | direction | `delta*b` | `delta*b²` |
| ---: | ---: | --- | ---: | ---: |
| `5` | `+1.551991e-02` | TOWARD | `0.0776` | `0.3880` |
| `6` | `+1.634038e-02` | TOWARD | `0.0980` | `0.5883` |
| `7` | `+1.387414e-02` | TOWARD | `0.0971` | `0.6798` |
| `8` | `+1.117876e-02` | TOWARD | `0.0894` | `0.7154` |
| `10` | `+8.389433e-03` | TOWARD | `0.0839` | `0.8389` |

Frozen fit:

- `delta ~= C * b^(-0.962)`
- `R^2 = 0.870`

## Safe Read

The centroid readout supports a stable impact-parameter law on the strongest
portable grown row.

What is retained:

- exact zero-field control
- positive TOWARD deflection on every sampled `b`
- a near-Newtonian tail exponent close to `-1`

What is not claimed:

- no geometry-generic theorem
- no universality across the breakpoint families
- no stronger strong-field claim than the frozen row supports

## Final Verdict

**retained narrow positive: the strongest portable grown row carries a stable
deflection-vs-impact-parameter law**
