# Quick Third Vs Sixth Distance Law Note

**Date:** 2026-04-06  
**Status:** targeted contrast on one retained row per family

## Artifact chain

- [`scripts/SIXTH_FAMILY_DISTANCE_LAW_THIRD_VS_SIXTH_QUICK.py`](/Users/jonreilly/Projects/Physics/scripts/SIXTH_FAMILY_DISTANCE_LAW_THIRD_VS_SIXTH_QUICK.py)
- [`logs/2026-04-06-sixth-family-distance-law-third-vs-sixth-quick.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-sixth-family-distance-law-third-vs-sixth-quick.txt)

## Question

Does the third retained grown family preserve the near-Newtonian distance tail
on a retained interior row, and how does that compare to the retained sixth
sheared basin?

This quick spot check is intentionally narrow:

- third family row: `drift=0.20, seed=2` from the retained signed-source basin
- sixth family row: `drift=0.20, seed=2` from the retained sheared basin
- distance samples: `b = [5, 6, 7, 8, 10]`
- exact zero / neutral gate language stays inside the parent family notes

## Result

The sixth family preserves the near-Newtonian tail on the sampled retained row.
The third family does not.

Measured rows:

| family | drift | seed | alpha | R^2 | toward | tail read |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| third | 0.20 | 2 | -2.158 | 0.909 | 5/5 | miss |
| sixth | 0.20 | 2 | -1.077 | 0.911 | 5/5 | preserve |

Gate replay:

- third gate replay is exact on the narrow controls:
  - zero = `0.000e+00`
  - neutral = `0.000e+00`
  - plus = `+6.711e-06`
  - minus = `-6.711e-06`
- sixth gate replay is exact on the narrow controls:
  - zero = `0.000e+00`
  - neutral = `0.000e+00`
  - plus = `+3.871e-06`
  - minus = `-3.871e-06`

## Safe Read

- the sixth-family sheared basin keeps the near-Newtonian tail on the sampled
  retained row
- the third-family interior retained row misses the tail, even though its
  sign gate is clean
- that miss should be read through the existing distance-law breakpoint
  classifier, not promoted as a generic family failure

## Conclusion

**targeted positive for sixth-family tail survival; third-family miss remains
consistent with the breakpoint classifier**
