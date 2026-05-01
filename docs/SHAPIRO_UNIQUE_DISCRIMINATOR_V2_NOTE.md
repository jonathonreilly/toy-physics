# Shapiro Unique Discriminator V2 Note

**Date:** 2026-04-06  
**Status:** support - structural or confirmatory support note

## Artifact Chain

- [`scripts/shapiro_unique_discriminator_v2.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_unique_discriminator_v2.py)
- [`logs/2026-04-06-shapiro-unique-discriminator-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-unique-discriminator-v2.txt)
- retained Shapiro chain:
  - [`docs/SHAPIRO_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DELAY_NOTE.md)
  - [`docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md)
  - [`archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md)
  - [`archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
  - [`docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)

## Question

Now that the retained c-dependent Shapiro-style phase lag is portable across
the retained families, can we find a stronger discriminator than the detector
phase lag alone?

## Search Result

The answer is no, not with the current retained channels.

The retained boundary result is:

- exact zero control stays exact
- the causal phase lag is portable across the three retained grown families
- the static cone-shape proxy reproduces the same c-dependent phase curve
  exactly
- static scheduling does not reproduce the curve and stays near-flat

The phase table is:

| mode | c=2.0 | c=1.0 | c=0.5 | c=0.25 |
| --- | ---: | ---: | ---: | ---: |
| causal dynamic cone | `+0.0372` | `+0.0446` | `+0.0569` | `+0.0662` |
| static cone shape | `+0.0372` | `+0.0446` | `+0.0569` | `+0.0662` |
| static scheduling | `+0.0446` | `+0.0445` | `+0.0446` | `+0.0450` |

## Boundary Read

The cleanest interpretation is:

- the detector-line phase lag is real, portable, and seed-stable
- but it is not a unique causal-propagation discriminator
- a static cone-shape field family can mimic the full lag curve exactly
- static scheduling cannot, so it remains the weaker proxy

This is therefore a boundary result, not a stronger discriminator result.

## Best Remaining Boundary

The best remaining boundary is that the Shapiro-style phase lag is:

- a portable proxy-level observable
- compatible with causal propagation
- not unique against static field-shape effects

If we want a stricter causal discriminator, we will need a second observable
that static cone-shape fields do not reproduce.

## Final Verdict

**boundary result: the detector-line phase lag is portable and real, but a
static cone-shape proxy reproduces it exactly, so the current lane freezes as
the best remaining boundary rather than a unique discriminator**
