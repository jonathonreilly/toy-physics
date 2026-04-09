# Symmetry Head-To-Head Note

**Date:** 2026-04-03  
**Status:** review-safe apples-to-apples comparison between the retained exact
mirror chokepoint lane and the retained dense `Z2 x Z2` lane

This note freezes the comparison requested after the exact mirror and
`Z2 x Z2` lanes were both independently validated on `main`.

Script:
[`scripts/symmetry_head_to_head.py`](/Users/jonreilly/Projects/Physics/scripts/symmetry_head_to_head.py)

Canonical sources:
- [`docs/MIRROR_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md)
- [`docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md)
- [`docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md)
- [`docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md)

## Shared-Row Comparison

The two lanes are compared on the same retained metrics at the shared
`N = 80` and `N = 100` rows.

| N | lane | d_TV | pur | gravity | Born | k=0 |
|---|---|---:|---:|---:|---:|---:|
| 80 | exact mirror chokepoint | `0.4291` | `0.8182` | `+3.0551` | `2.43e-15` | `0.00e+00` |
| 80 | `Z2 x Z2` | `0.5250` | `0.7850` | `+2.6770` | `1.55e-15` | `0.00e+00` |
| 100 | exact mirror chokepoint | `0.2308` | `0.9043` | `+1.3089` | `1.13e-15` | `0.00e+00` |
| 100 | `Z2 x Z2` | `0.5670` | `0.7420` | `+0.7630` | `1.94e-15` | `0.00e+00` |

## Retained Ranges

- Exact mirror chokepoint: retained through `N = 100`; `N = 120` loses
  gravity.
- `Z2 x Z2`: retained through `N = 120` on the dense extension; gravity stays
  positive but the gravity-side law is not clean.

## Mirror MI Supplement

The exact mirror family has a separate canonical MI artifact chain on the
retained dense chokepoint family. That result is bounded and mid-`N`
positive over the matched random baseline, but it is not a clean asymptotic
law and is not directly paired with a `Z2 x Z2` MI artifact.

## Retained Read

- Exact mirror is the stronger gravity-weighted joint lane on the shared
  `N = 80/100` rows.
- `Z2 x Z2` is the stronger decoherence-side lane and has the longer retained
  range.
- Both lanes remain Born-clean at machine precision on their retained
  harnesses.

## Bottom Line

Use exact mirror when the priority is joint coexistence with stronger gravity.
Use `Z2 x Z2` when the priority is decoherence depth and retained range.
