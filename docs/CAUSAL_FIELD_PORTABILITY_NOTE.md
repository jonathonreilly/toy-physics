# Causal Field Portability Note

**Date:** 2026-04-06  
**Status:** support - structural or confirmatory support note

## Artifact Chain

- [`scripts/causal_field_portability_probe.py`](/Users/jonreilly/Projects/Physics/scripts/causal_field_portability_probe.py)
- [`logs/2026-04-06-causal-field-portability-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-causal-field-portability-probe.txt)
- causal propagating-field context:
  - [`docs/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_PROPAGATING_FIELD_NOTE.md)

## Question

Does the causal propagating-field observable from the center grown family stay
portable onto the second and third portable families under exact-null control,
or do the ratios diagnose a family boundary?

## Result

The exact-null control stays exact on all three families:

- max `|delta_y|` across families: `0.000e+00`
- max `|field|` across families: `0.000e+00`

The retained center family keeps the original forward-only scale, but the
other two families do not track it cleanly:

| family | inst delta | forward delta | forward / inst | dynamic(c=0.5) / inst |
| --- | ---: | ---: | ---: | ---: |
| center grown family | `2.921e-07` | `1.951e-07` | `0.668` | `0.938` |
| portable family 2 | `4.802e-07` | `1.758e-07` | `0.366` | `0.728` |
| portable family 3 | `1.927e-07` | `1.522e-07` | `0.790` | `1.080` |

## Safe Read

What survives:

- the exact-null control is stable and exact on the replay
- the center family keeps the retained forward-only causal-field behavior

What does not survive:

- the second and third portable families do not sit on the same forward-only
  ratio as the center family
- the finite-cone ratio also moves enough to break a clean cross-family
  portability claim

## Boundary Call

The spread is large enough to freeze the claim as a diagnosed family boundary:

- forward-only ratio spread across the three families: `0.423`
- dynamic(c=0.5)/instantaneous ratio spread: `0.352`

So the current causal-field observable is real on the center family, but it is
not yet a cross-family portability law on the second and third portable
families.

## Final Verdict

**diagnosed family boundary: the exact-null control survives, but the causal
field ratios split by family instead of extending cleanly across the portable
family chain**
