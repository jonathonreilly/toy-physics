# Impact-Parameter Portability Note

**Date:** 2026-04-06  
**Status:** proposed_retained positive across two portable grown families

## Artifact Chain

- [`scripts/impact_parameter_portability_probe.py`](/Users/jonreilly/Projects/Physics/scripts/impact_parameter_portability_probe.py)
- [`logs/2026-04-06-impact-parameter-portability-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-impact-parameter-portability-probe.txt)
- retained lensing context:
  - [`docs/IMPACT_PARAMETER_LENSING_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/IMPACT_PARAMETER_LENSING_NOTE.md)
  - [`logs/2026-04-06-impact-parameter-lensing-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-impact-parameter-lensing-probe.txt)
- broader portability context:
  - [`docs/PORTABLE_CARD_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PORTABLE_CARD_EXTENSION_NOTE.md)
  - [`docs/IMPACT_PARAMETER_PORTABILITY_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/IMPACT_PARAMETER_PORTABILITY_EXTENSION_NOTE.md)

## Question

Does the retained impact-parameter law survive beyond the center portable row
onto at least one additional grown family?

This probe stays narrow:

- exact/null control first
- same `b` sweep on each retained row
- no new geometry search
- no claim about the family-3 holdout from the extension note

## Result

The answer is yes on the tested pair of portable grown families.

Exact/null control:

- zero-field replay at `b = 8` is exact on both rows: `delta = +0.000000e+00`

Retained rows:

| family | `delta ~= C * b^alpha` | `R^2` | direction |
| --- | ---: | ---: | --- |
| grown family 1 | `alpha = -0.962` | `0.870` | `5/5 TOWARD` |
| grown family 2 | `alpha = -0.947` | `0.875` | `5/5 TOWARD` |

## Safe Read

The retained impact-parameter law ports cleanly onto the second grown family:

- the null control stays exact
- every sampled `b` stays TOWARD on both rows
- the fitted exponents stay close to `-1`
- the alpha span across the two rows is small, so the window looks stable

## Claim Boundary

This is still a bounded portability statement, not a universal theorem:

- it covers the two retained portable grown families tested here
- it does not override the separate family-3 holdout diagnosis in the
  extension note

## Final Verdict

**retained positive: the impact-parameter law survives onto the second grown
family with a stable TOWARD window and near-Newtonian fit**
