# Shapiro Delay Note

**Date:** 2026-04-06  
**Status:** proposed_retained canonical replay of the discrete Shapiro-style phase lag

## Artifact Chain

- [`scripts/shapiro_phase_lag_probe.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_phase_lag_probe.py)
- [`logs/2026-04-06-shapiro-delay-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-delay-probe.txt)
- [`archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md)
- [`archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)
- [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)

## Question

What is the canonical in-repo replay for the retained c-dependent phase lag,
keeping the exact zero control explicit and the seed-stable delay table intact?

## Exact Control

- `c = inst`: phase lag `0.000 rad` on all three families
- exact null survives by construction

## Retained Phase Lag

| c | phase lag mean | family spread | fam1 | fam2 | fam3 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `2.00` | `+0.0401 rad` | `0.0001 rad` | `+0.0401` | `+0.0401` | `+0.0400` |
| `1.00` | `+0.0500 rad` | `0.0002 rad` | `+0.0499` | `+0.0501` | `+0.0499` |
| `0.50` | `+0.0621 rad` | `0.0002 rad` | `+0.0621` | `+0.0622` | `+0.0620` |
| `0.25` | `+0.0679 rad` | `0.0000 rad` | `+0.0679` | `+0.0679` | `+0.0679` |

## Seed Stability

- the retained replay is seed-stable to three significant figures
- family spread across the portable-grown replay stays at or below `2e-4 rad`
- the phase lag increases monotonically as the field propagation speed decreases

## Narrow Read

- the phase lag is the discrete Shapiro-delay observable
- the observable is portable across the three retained grown families
- the observable remains proxy-level; absolute NV units are still external calibration work

## Final Verdict

**the retained c-dependent phase lag is a portable, seed-stable discrete
Shapiro-delay observable with an exact zero control and family spread below
2e-4 rad**
