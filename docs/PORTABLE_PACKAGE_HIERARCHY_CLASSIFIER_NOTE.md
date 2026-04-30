# Portable Package Hierarchy Classifier

**Date:** 2026-04-06  
**Status:** support - review-safe portable-package classifier

## Artifact Chain

- [`scripts/portable_package_hierarchy_classifier.py`](/Users/jonreilly/Projects/Physics/scripts/portable_package_hierarchy_classifier.py)
- [`logs/2026-04-06-portable-package-hierarchy-classifier.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-portable-package-hierarchy-classifier.txt)
- broad portable package cards: [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md), [`archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_PACKAGE_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_PACKAGE_EXTENSION_NOTE.md), [`archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_CARD_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/portability-stale-extension-wrappers-2026-04-30/PORTABLE_CARD_EXTENSION_NOTE.md)
- distance-tail cards: [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md), [`docs/DISTANCE_LAW_BREAKPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_BREAKPOINT_NOTE.md)
- complex-action cards: [`docs/COMPLEX_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_ACTION_NOTE.md), [`docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md)

## Classifier

The retained evidence supports one nested read:

1. The broad portable weak-field package is the signed-control fixed point.
2. The distance tail is a stricter open-transport subset of that package.
3. The complex-action branch is narrower still because it needs the exact `gamma = 0` anchor and crossover structure.

## Retained Cards / Closures

| layer | retained family cards | closure or boundary |
| --- | --- | --- |
| broad portable weak-field package | grown transfer basin, alt connectivity family, second grown-family sign, third grown-family sign, fourth family quadrant, fifth family radial holdout | exact zero-source cancellation, exact neutral same-point cancellation, plus/minus antisymmetry, weak-field response near unit slope |
| stricter distance tail | first two grown families as the preservation anchor; alt connectivity, third family, and fourth family as breakpoints; fifth family radial as a direction-only holdout | open directed transport that keeps direction and tail shape coupled; shell locking, reflection closure, deep branch routing, and radial confinement break it |
| narrower complex-action branch | original grown basin, second-family complex anchor row, alt connectivity failure as a boundary check | exact `gamma = 0` anchor plus crossover structure; boundary-sensitive and anchor-local |

## Why This Is Review-Safe

- this is a classifier, not a universal geometry theorem; the retained cards bound the claim
- the broad layer is backed by multiple family cards that share the same signed-control fixed point
- the distance tail is narrower because the first two grown families keep direction and tail together, while newer retained families break or flatten one of those pieces
- the complex-action branch is narrower still because it survives only on the exact `gamma = 0` anchor and crossover structure, and it is boundary-sensitive on adjacent families

## Final Verdict

**review-safe classifier: broad portable weak-field package, stricter distance tail, narrower complex-action branch**
