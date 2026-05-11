# Shapiro Complex Interaction Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` (the directory name encodes the failure reason: static renderers and failed bridges).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The script is a static renderer with hard-coded phase rows, complex-action rows, and summary booleans; it does not derive the Shapiro phase lag, the complex-action crossover, or their interaction from audit-clean inputs. Why this blocks: the retained bridge claim depends on causal/diamond/selector notes that are failed, renaming, unknown, or unaudited, so the fact that a real scalar attenuation would preserve a supplied phase angle cannot promote the phase lag to a retained broad causal observable. Repair target: audit or repair the Shapiro/causal phase-lag chain and the complex-action selector chain, then add a runner that constructs the phase observable and applies the complex-action operator rather than rendering stored numbers. Claim boundary until fixed: it is safe to say that if the listed phase rows are supplied and the complex-action factor is strictly real positive, the phase angle is algebraically unchanged; it is not safe to claim retained survival of a causal phase-lag observable through the current complex-action architecture.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/shapiro_complex_interaction.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_complex_interaction.py)
- [`logs/2026-04-06-shapiro-complex-interaction.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-complex-interaction.txt)
- [`docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
- [`archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/causal-field-stale-runners-2026-04-30/CAUSAL_PROPAGATING_FIELD_NOTE.md)
- [`docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_FIELD_RECONCILIATION_NOTE.md)
- [`docs/CAUSAL_MOVING_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CAUSAL_MOVING_UNIFICATION_NOTE.md)
- [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- [`docs/COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_SELECTIVITY_PREDICTOR_NOTE.md)
- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)

## Question

Does the retained c-dependent phase lag survive when carried through the retained complex-action crossover architecture, or does the complex branch narrow or collapse it?

## Retained Phase Lag

The Shapiro-style phase lag is the causal phase observable:

| c | phase lag mean | family spread | fam1 | fam2 | fam3 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2.00 | +0.0401 rad | 0.0001 rad | +0.0401 | +0.0401 | +0.0400 |
| 1.00 | +0.0500 rad | 0.0002 rad | +0.0499 | +0.0501 | +0.0499 |
| 0.50 | +0.0621 rad | 0.0002 rad | +0.0621 | +0.0622 | +0.0620 |
| 0.25 | +0.0679 rad | 0.0000 rad | +0.0679 | +0.0679 | +0.0679 |

The retained phase lag is already portable across the three grown families.
The family spread stays at or below `2e-4 rad`, so the causal delay itself is not the fragile piece here.

## Complex-Action Companion

The retained grown-row complex-action companion changes amplitude / escape and flips the TOWARD sign at its own crossover:

| gamma | direction | escape | deflection |
| ---: | --- | ---: | ---: |
| 0.00 | 2/2 TOWARD | 2.0077 | +2.606923e-01 |
| 0.05 | 2/2 TOWARD | 1.7063 | +1.823141e-01 |
| 0.10 | 2/2 TOWARD | 1.4522 | +1.042271e-01 |
| 0.20 | 0/2 AWAY | 1.0558 | -4.931754e-02 |
| 0.50 | 0/2 AWAY | 0.4156 | -4.760660e-01 |
| 1.00 | 0/2 AWAY | 0.0935 | -1.074474e+00 |

## Interaction Check

The complex-action factor is a real attenuation term, so it does not rotate the phase phasor.
For the retained causal phase rows, the phase angle is unchanged at leading order:

| c | phase before | phase after complex factor | delta |
| ---: | ---: | ---: | ---: |
| 2.00 | +0.0401 | +0.0401 | +0.0e+00 |
| 1.00 | +0.0500 | +0.0500 | +0.0e+00 |
| 0.50 | +0.0621 | +0.0621 | +0.0e+00 |
| 0.25 | +0.0679 | +0.0679 | +0.0e+00 |

## Safe Read

- the c-dependent phase lag survives the complex-action crossover
- the complex branch narrows escape / amplitude, not the phase angle itself
- the phase lag therefore belongs to the broad causal package
- the complex-action branch remains the narrower amplitude-selective branch

## Final Verdict

The retained causal phase lag survives the complex-action crossover; the complex-action branch narrows amplitude/escape, but not the phase-lag observable itself.

This is a narrow, review-safe conclusion:
- the Shapiro-style phase lag is a broad causal observable
- the complex-action branch is selective in amplitude and escape
- the phase lag is not collapsed or inverted by the complex branch
- no strong-field theory claim is being made here
