# Complex Selectivity Predictor Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow predictor card for complex-action survival on structured families

## Artifact Chain

- [`scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py`](/Users/jonreilly/Projects/Physics/scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py)
- [`logs/2026-04-06-complex-selectivity-predictor.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-complex-selectivity-predictor.txt)
- retained family cards:
  - [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md)
  - [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md)
  - [`docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md)
  - [`docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md)
  - [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md)
  - [`docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md)

## Question

What is the smallest review-safe discriminator for when a complex-action
companion survives on a structured family?

## Comparison

| family | retained complex | exact gamma=0 | anchor crossover | basin shape | discriminator note |
| --- | --- | --- | --- | --- | --- |
| Original grown basin | yes | yes | yes on nearby rows | narrow and selective | anchor-local crossover survives on a nearby row neighborhood |
| Second-family complex | yes | yes | yes on the anchor row | tiny basin | exact gamma=0 + Born proxy + crossover survive narrowly |
| Alt connectivity family | no | yes | no | bounded sign-law basin only | sign-law survives, complex branch does not |
| Third grown family | no | yes | not stable across drift window | bounded drift basin | crossover is seed-selective and drift-sensitive; not retained |
| Fourth family quadrant | no | yes | no | narrow seed-selective sign basin | complex response stays boundary-like despite clean controls |
| Fifth family radial | yes | yes | yes on the anchor row | narrow anchor-row basin | anchor-local crossover survives, but only at the center row |

## Safe Read

- exact gamma=0 baseline is necessary, but not sufficient
- signed-source portability and weak-field linearity do not predict complex survival by themselves
- support width and seed selectivity are useful context, but they do not separate the positive families from the diagnosed boundaries cleanly
- the smallest stable discriminator we found is the anchor-local crossover: exact gamma=0 baseline plus `TOWARD -> AWAY` on the retained anchor row

## Exact Mismatch

- the original grown basin and the fifth-family radial slice retain the crossover only in a narrow local neighborhood
- the second-family complex slice retains it on the anchor row but loses it in the tighter boundary window
- the alt, third, and fourth families all fail the same crossover test in structurally different ways

## Final Verdict

**retained narrow predictor: complex-action survival requires an anchor-local crossover; coarser basin geometry does not predict it**
