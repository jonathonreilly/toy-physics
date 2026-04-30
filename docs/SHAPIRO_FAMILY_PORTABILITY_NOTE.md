# Shapiro Family Portability Note

**Date:** 2026-04-06  
**Status:** proposed_retained positive - the c-dependent phase lag reproduces cleanly across the three portable grown families

## Artifact Chain

- [`scripts/shapiro_family_portability.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_family_portability.py)
- [`logs/2026-04-06-shapiro-family-portability.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-family-portability.txt)
- [`docs/SHAPIRO_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DELAY_NOTE.md)
- [`archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md)
- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)

## Question

Does the retained c-dependent phase-lag observable reproduce cleanly across the three portable grown families with the same seed-stable values?

## Exact Controls

The zero-source control is exact on all three families:

- Fam1: zero lag = `+0.000e+00`
- Fam2: zero lag = `+0.000e+00`
- Fam3: zero lag = `+0.000e+00`

That is the first gate for the portability claim, and it passes cleanly.

## Cross-Family Phase Table

| c | Fam1 | Fam2 | Fam3 | max diff |
| ---: | ---: | ---: | ---: | ---: |
| inst | +0.0000 | +0.0000 | +0.0000 | 0.0000 |
| 2.0 | +0.0401 | +0.0401 | +0.0400 | 0.0001 |
| 1.0 | +0.0499 | +0.0501 | +0.0499 | 0.0002 |
| 0.5 | +0.0621 | +0.0622 | +0.0620 | 0.0002 |
| 0.25 | +0.0679 | +0.0679 | +0.0679 | 0.0001 |

The seed rows remain stable within each family:
- the two retained seeds differ only at the `1e-4` to `1e-3` rad level
- the family means agree to within `0.0002 rad` at every `c`
- the phase lag grows monotonically as `c` decreases

## Safe Read

- the Shapiro-style phase lag is reproducible across all three portable grown families
- the zero-source control remains exact
- the portability statement is about the phase observable, not an absolute NV calibration
- the retained claim is proxy-level and family-portable, not a claim about a new value of `c`

## Final Verdict

**retained positive: the c-dependent phase lag reproduces cleanly across the three portable grown families with seed-stable values, and the exact zero control survives on all three**

