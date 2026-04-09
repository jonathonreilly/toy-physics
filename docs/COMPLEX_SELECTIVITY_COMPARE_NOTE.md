# Complex Selectivity Compare Note

**Date:** 2026-04-06  
**Status:** narrow comparison card for signed-source portability vs complex-action selectivity

## Artifact Chain

- [`scripts/COMPLEX_SELECTIVITY_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/COMPLEX_SELECTIVITY_COMPARE.py)
- [`logs/2026-04-06-complex-selectivity-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-complex-selectivity-compare.txt)
- retained family cards:
  - [`docs/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWN_TRANSFER_BASIN_NOTE.md)
  - [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
  - [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md)
  - [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_QUADRANT_NOTE.md)

## Question

Why does signed-source transfer survive on multiple independent families while complex-action companions stay much more selective?

## Comparison

| family | signed-source result | weak-field response | complex-action result | mismatch |
| --- | --- | --- | --- | --- |
| Original grown basin | retained narrow basin positive | `F~M = 1.000` | retained narrow `gamma=0 -> AWAY` crossover on nearby rows | selective basin, not family-wide closure |
| Second-family complex | not the shared surface | `F~M = 1.000` | retained narrow anchor-row positive | tiny basin, then a tighter `AWAY`-at-`gamma=0` boundary |
| Alternative connectivity family | retained bounded positive | `F~M = 0.999994` | clean boundary failure; no `TOWARD -> AWAY` crossover | sign-law survives, complex branch does not |
| Third grown family | retained bounded basin positive | charge exponent `0.999842` | not retained on this slice | signed-source basin survives in the interior only |
| Fourth family quadrant | retained narrow basin | near-linear charge scaling | not retained on this slice | fresh family exists, but remains sign-law only |

## Safe Read

- signed-source transfer is the portable feature: exact zero / neutral controls survive on several distinct structured families
- weak-field linearity survives with the signed-source package across the retained grown, alt, third, and fourth family slices
- complex action is more selective: it needs the exact `gamma=0` anchor / crossover structure and fails cleanly on the alt family and the tightened second-family window

## Exact Mismatch

- the signed-source families share a common control surface
- the complex-action branch does not share that same surface; it lives on a more constrained `gamma` baseline plus crossover test
- the result is not a universal family theorem; it is a selectivity split between portable sign-law and basin-local complex action

## Final Verdict

**retained selectivity split: signed-source is family-portable, while complex-action is anchor-local and boundary-sensitive**
