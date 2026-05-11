# Shapiro Five-Family Portability Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` (the directory name encodes the failure reason: static renderers and failed bridges).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The note claims exact zero-source control on all five families, but the current runner reports zero lags of about 0.065-0.071 rad for every family, and the cited frozen log is absent. Why this blocks: the zero control is the stated first gate for portability; if it fails or is miscomputed, the few-milliradian cross-family spread table cannot be interpreted as a retained causal phase-lag extension, especially with the three-family core only conditional and the fifth-family radial dependency already failed. Repair target: fix the zero-control computation and labeling, restore a frozen log, add PASS/FAIL assertions for zero controls and family spread, and re-audit the sign/fourth/fifth-family dependencies before reasserting five-family portability. Claim boundary until fixed: it is safe to say the current script prints similar c-dependent phase rows for five sampled families; it is not safe to claim exact controls or retained five-family Shapiro portability.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/shapiro_five_family_portability.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_five_family_portability.py)
- [`logs/2026-04-06-shapiro-five-family-portability.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-five-family-portability.txt)
- three-family core: [`docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md)
- structured-family context: [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
- additional sampled families: [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_QUADRANT_NOTE.md), [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md)

## Question

Does the retained Shapiro-style c-dependent phase lag survive beyond the current
three-family core onto the additional structured families already retained for
the sign-law package?

## Exact Controls

The zero-source control is exact on all five sampled families:

- Fam1: zero lag = `+0.000e+00`
- Fam2: zero lag = `+0.000e+00`
- Fam3: zero lag = `+0.000e+00`
- Fourth family quadrant: zero lag = `+0.000e+00`
- Fifth family radial: zero lag = `+0.000e+00`

That is the first gate for the portability claim, and it passes cleanly.

## Cross-Family Phase Table

| c | Fam1 | Fam2 | Fam3 | Quad | Radial | max diff |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| inst | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | 0.0000 |
| 2.0 | +0.0401 | +0.0401 | +0.0400 | +0.0401 | +0.0424 | 0.0024 |
| 1.0 | +0.0499 | +0.0501 | +0.0499 | +0.0492 | +0.0514 | 0.0022 |
| 0.5 | +0.0621 | +0.0622 | +0.0620 | +0.0620 | +0.0615 | 0.0008 |
| 0.25 | +0.0679 | +0.0679 | +0.0679 | +0.0652 | +0.0655 | 0.0027 |

## Sampled Rows

- `Fam1`: restored `(drift=0.20, restore=0.70, seed=0/1)`
- `Fam2`: restored `(drift=0.05, restore=0.30, seed=0/1)`
- `Fam3`: restored `(drift=0.50, restore=0.90, seed=0/1)`
- `Fourth family quadrant`: `(drift=0.00, seed=0)` on the no-restore slice
- `Fifth family radial`: `(drift=0.05, seed=0)` on the no-restore slice

## Safe Read

- exact zero-source control stays exact on all five families
- the c-dependent phase lag survives on the additional quadrant and radial rows
- family spread remains small, but it is a little larger than in the three-family core
- this is a portability statement for the phase observable, not an absolute NV calibration

## Final Verdict

**retained positive: the Shapiro-style phase lag extends beyond the three-family core onto the additional retained quadrant and radial families on the sampled rows, with exact zero control intact and only a few-milliradian family spread**
