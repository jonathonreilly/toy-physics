# Portable Card Extension Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow extension positive with a distance-law measurement holdout

## Artifact Chain

- [`scripts/PORTABLE_CARD_EXTENSION_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/PORTABLE_CARD_EXTENSION_COMPARE.py)
- [`logs/PORTABLE_CARD_EXTENSION_COMPARE_2026-04-06.txt`](/Users/jonreilly/Projects/Physics/logs/PORTABLE_CARD_EXTENSION_COMPARE_2026-04-06.txt)
- retained three-family card:
  - [`docs/THREE_FAMILY_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THREE_FAMILY_CARD_NOTE.md)
- portability context:
  - [`docs/PORTABLE_PACKAGE_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PORTABLE_PACKAGE_EXTENSION_NOTE.md)
  - [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
- distance-law context:
  - [`docs/DISTANCE_LAW_BREAKPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_BREAKPOINT_NOTE.md)
  - [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md)

## Question

Does the new three-family card extend the portable package cleanly beyond the
first two grown families, and is the distance law the main holdout subset
rather than the card itself?

## Comparison

The retained three-family card stays clean on the portable core:

- the portable core remains retained on all three families
- family 3 (`drift = 0.50`, `restore = 0.90`) joins the same portable package
- the card is still narrow: this is not a universal geometry theorem

The distance-law probe is separated explicitly from that card:

- the family-3 distance lookup collapses to the same boundary node for all
  tested `b` values
- the fitted probe therefore reports `alpha = 0.000` with `r2 = 1.000`
- that collapse is a source-placement / harness issue, not a physics failure,
  because the probe never samples distinct distance rows on the family-3
  geometry

## Safe Read

The narrow read is now:

- the portable package extends cleanly onto the three-family card
- the distance law is still the stricter holdout subset
- on the current family-3 probe, the open question is measurement coverage,
  not a physics contradiction

## Exact Mismatch

- the distance-law window used by the current probe does not map to distinct
  interior source positions on family 3
- the observed flat `delta` is therefore not evidence against the portable
  package
- it is evidence that the current distance-law harness needs a family-relative
  source-placement fix before it can be treated as a physics test on that row

## Final Verdict

**retained narrow extension positive: the three-family card extends the
portable package cleanly, while the distance law remains the main holdout
subset on the current family-3 probe**
