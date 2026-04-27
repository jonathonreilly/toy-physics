# Distance Law Preserving Third Family Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow positive on the high-drift/high-restore third family

## Artifact Chain

- [`scripts/DISTANCE_LAW_PRESERVING_THIRD_FAMILY.py`](/Users/jonreilly/Projects/Physics/scripts/DISTANCE_LAW_PRESERVING_THIRD_FAMILY.py)
- [`logs/2026-04-06-distance-law-preserving-third-family.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-distance-law-preserving-third-family.txt)
- three-family context: [`docs/THREE_FAMILY_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THREE_FAMILY_CARD_NOTE.md)
- distance-law portability context: [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md)

## Question

Does the high-drift/high-restore third grown family from the three-family card
preserve both the signed-source package and the near-Newtonian distance tail?

The probe is intentionally narrow:

- family: `drift = 0.50`, `restore = 0.90`
- controls: exact zero-source baseline and exact neutral `+1/-1` cancellation
- sign gate: positive `+1` versus negative `-1`
- weak charge scaling: `+2` versus `+1`
- distance gate: `b = 5, 6, 7, 8, 10`

## Result

The family passes both gates on the direct test:

- zero control: exact `0.000e+00`
- neutral control: exact `0.000e+00`
- sign orientation: `+1.764e-04` versus `-1.764e-04`
- weak charge scaling exponent: `1.000`
- distance tail: `alpha = -1.150`
- tail fit quality: `R^2 = 0.971`
- direction count: `5/5 TOWARD`

## Safe Read

This is a real third-family preservation result:

- the signed-source package survives unchanged on the high-drift/high-restore family
- the direct distance tail remains near-Newtonian on the same family
- the tail is slightly steeper than `-1.0`, but still within the retained near-Newtonian band

## Claim Boundary

This does **not** imply a universal theorem across all grown families.
It only says that the third family from the three-family card preserves both:

- signed-source / weak-field controls
- near-Newtonian distance-tail viability

## Conclusion

**retained narrow positive: the high-drift/high-restore third family preserves both the signed-source package and the near-Newtonian distance tail on the direct test**
