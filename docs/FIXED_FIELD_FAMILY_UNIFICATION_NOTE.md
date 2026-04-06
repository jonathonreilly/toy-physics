# Fixed-Field Family Unification Note

**Date:** 2026-04-06  
**Status:** compact retained same-row comparison, not a geometry-generic theorem

## Artifact chain

- [`scripts/FIXED_FIELD_FAMILY_UNIFICATION.py`](/Users/jonreilly/Projects/Physics/scripts/FIXED_FIELD_FAMILY_UNIFICATION.py)
- [`logs/FIXED_FIELD_FAMILY_UNIFICATION_2026-04-06.txt`](/Users/jonreilly/Projects/Physics/logs/FIXED_FIELD_FAMILY_UNIFICATION_2026-04-06.txt)
- companion retained notes:
  - [`docs/GATE_B_NONLABEL_SIGN_GROWN_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_SIGN_GROWN_TRANSFER_NOTE.md)
  - [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)

## Question

Can the same retained grown row support both of the narrow fixed-field
couplings that have already been retained separately:

- the signed-source companion
- the exact `gamma = 0` complex-action companion

The comparison stays intentionally narrow:

- same retained grown row only: `drift = 0.2`, `restore = 0.7`
- exact zero / neutral controls on the sign-law branch
- exact `gamma = 0` baseline on the complex-action branch
- no geometry-generic or continuum claim

## Frozen Result

Seed `0` on the retained grown row:

### Signed-source branch

| metric | value |
|---|---:|
| zero source | `+0.000000e+00` |
| single `+1` | `-1.594422e-04` |
| single `-1` | `+1.594790e-04` |
| neutral `+1/-1` | `+0.000000e+00` |
| double `+2` | `-3.188474e-04` |
| charge exponent | `0.999833` |

### Complex-action branch

| metric | value |
|---|---:|
| `gamma = 0` baseline deflection | `+2.460475e-01` |
| `gamma = 0.2` delta vs free | `-7.003685e-02` |
| `gamma = 0.5` delta vs free | `-4.993079e-01` |
| escape at `gamma = 0.2` | `1.053490e+00` |
| escape at `gamma = 0.5` | `4.120507e-01` |

## Safe Read

The same retained grown row supports both narrow fixed-field companions:

- the signed-source family keeps exact zero-source and neutral same-point
  cancellation
- the complex-action family keeps the retained `gamma = 0` baseline on the
  same row, and moves into the absorptive side at stronger `gamma`

This is a compact family-unification positive at the same retained grown row
level. It is not yet a geometry-generic theorem and it does not by itself
reopen the wider transfer or continuum claims.

## Final Verdict

**retained compact fixed-field family-unification positive**
