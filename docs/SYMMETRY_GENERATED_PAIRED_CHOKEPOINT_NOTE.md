# Symmetry-Generated Paired Chokepoint Note

**Date:** 2026-04-03  
**Status:** bounded negative for the long-term vector; density-optimum scout stays exploratory

This note records the generated symmetry pilot that tries to recover part of
the mirror-chokepoint benefit without hard-coding mirrored edge copies.

Script:
[`scripts/symmetry_generated_paired_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/symmetry_generated_paired_chokepoint.py)

Log:
[`logs/2026-04-03-symmetry-generated-paired-chokepoint-n30.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-symmetry-generated-paired-chokepoint-n30.txt)

## Question

Can an axiom-friendlier, generated paired scaffold keep the mirror benefit
alive well enough to be a long-term vector?

The comparison set was:

- random chokepoint DAGs
- exact mirror chokepoint DAGs
- paired-generated chokepoint DAGs with small symmetry noise

## Small-N Result

The first pilot only had usable rows in the small-`N` window (`N = 15, 25`).
We then re-ran the generated scaffold at the grown-graph density optimum
(`npl_half = 30`) to see whether the approximate symmetry could survive a
more favorable geometry.

Density-optimum probe:

- `npl_half = 30`
- `connect_radius = 4.0`
- `N = 25, 40, 60`
- `8` seeds

Representative rows from the 8-seed pilot:

| family | N | d_TV | pur_cl | Born | gravity |
|---|---:|---:|---:|---:|---:|
| random chokepoint | 15 | `0.9198±0.0319` | `0.8965±0.0737` | `0.0000±0.0000` | `-0.2761±0.4994` |
| exact mirror chokepoint | 15 | `0.9619±0.0228` | `0.5585±0.0179` | `0.0000±0.0000` | `+0.6855±1.3012` |
| paired-generated noise=0.0 | 15 | `0.9155±0.0634` | `0.6211±0.0360` | `0.0000±0.0000` | `+2.1173±0.2519` |
| paired-generated noise=0.15 | 15 | `0.9584±0.0183` | `0.6741±0.0658` | `0.0000±0.0000` | `+2.3013±1.2805` |

At `N = 25`:

| family | N | d_TV | pur_cl | Born | gravity |
|---|---:|---:|---:|---:|---:|
| random chokepoint | 25 | `0.6759±0.0851` | `0.8223±0.0691` | `0.0000±0.0000` | `+0.6337±1.3701` |
| exact mirror chokepoint | 25 | `0.7684±0.1544` | `0.8126±0.0839` | `0.0000±0.0000` | `+1.9479±0.7397` |
| paired-generated noise=0.0 | 25 | `0.9272±0.0424` | `0.7215±0.0585` | `0.0000±0.0000` | `-0.3732±1.5978` |
| paired-generated noise=0.15 | 25 | `0.9575±0.0215` | `0.8805±0.0368` | `0.0000±0.0000` | `+2.7262±2.5270` |

## Density-Optimum Check

At the density optimum, the generated paired scaffold is still Born-clean
where it runs and does recover a modest subset of the mirror gap at `N = 25`
and `N = 40`. But it still loses retention by `N = 60`:

| family | N | d_TV | pur_cl | Born | gravity |
|---|---:|---:|---:|---:|---:|
| paired-generated noise=0.0 | 25 | `0.9558±0.0152` | `0.6891±0.0664` | `0.0000±0.0000` | `+1.5068±1.3860` |
| paired-generated noise=0.15 | 25 | `0.9491±0.0149` | `0.8193±0.0369` | `0.0000±0.0000` | `+1.5452±1.8265` |
| paired-generated noise=0.35 | 25 | `0.9172±0.0445` | `0.8218±0.0538` | `0.0000±0.0000` | `+2.1464±1.6825` |
| paired-generated noise=0.0 | 40 | `0.7680±0.1399` | `0.7352±0.0904` | `0.0000±0.0000` | `+1.0619±0.7770` |
| paired-generated noise=0.15 | 40 | `0.8273±0.0810` | `0.7219±0.0973` | `0.0000±0.0000` | `+1.8619±1.8833` |
| paired-generated noise=0.35 | 40 | `0.8150±0.0966` | `0.8406±0.0407` | `0.0000±0.0000` | `+3.3896±3.5779` |
| all noise values | 60 | FAIL | FAIL | FAIL | FAIL |

So the generated paired scaffold does improve over the purely random
chokepoint in a small bounded pocket, but it still does **not** survive to a
retained `N = 60` lane.

## Narrow Conclusion

- The generated paired scaffold is **Born-clean where it runs**.
- It does **not** consistently beat the exact mirror baseline.
- It does **not** survive to `N = 60` even at the density-optimum probe.

So the more generated / axiom-friendly symmetry construction is **not yet a
live long-term vector**.

The mirror effect appears to be real, but in this pilot it still looks tied to
the exact symmetry-protected chokepoint construction rather than to a robust
generated approximation.

## What This Means

- Keep the mirror chokepoint as the retained exact-symmetry baseline.
- Do not promote the generated paired scaffold as the new frontier.
- If the symmetry idea is to become a long-term vector, it needs a new
  generator that preserves the benefit beyond the small-`N` pocket.
