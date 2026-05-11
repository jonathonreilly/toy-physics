# Unified Basin Freeze: Both Basins Pass Zero/Neutral Controls

**Date:** 2026-04-06
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/unified-basin-signed-source-salvage-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/unified-basin-signed-source-salvage-2026-04-30/` (failure reason: the note combines two different surfaces as one "unified" basin and is contradicted by the available complex-basin runner, which gives exact gamma=0 + Born proxy survivors 0/2)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: The note combines two different surfaces as one unified basin: NONLABEL_GROWN_BASIN_TARGETED still gives 3/3 signed-source rows with exact zero/neutral controls, but complex_action_kernel_vs_gravity is a fixed-row kernel/generic-vs-gravity separation test, not a nearby basin; the actual FIXED_FIELD_COMPLEX_GROWN_BASIN runner gives exact gamma=0 + Born proxy survivors 0/2. Why this blocks: the claim that one grown connectivity family supports both couplings across a small nearby basin with exact controls is not computed by the supplied runners and is contradicted by the available complex-basin runner. Repair target: provide a single unified runner over the same drift/restore neighborhood and seed set, with explicit zero/neutral/gamma=0/Born assertions for both coupling surfaces, or split the note into separate retained/failed components. Claim boundary until fixed: safe to claim the signed-source non-label basin currently passes 3/3 at restore 0.60/0.70/0.80, and the kernel-vs-gravity fixed-row runner separates absorption from gravity-specific deflection; not safe to claim a unified two-coupling basin.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Control gate results

### Complex-action basin (drift=0.20, restore=0.70)

| Field | gamma=0 escape | gamma=0.5 escape | Crossover? |
| --- | ---: | ---: | --- |
| ZERO | 1.0000 | 1.0000 | NO (clean) |
| NEUTRAL (f=0.01) | 1.4497 | 0.6231 | YES (expected: any f!=0) |
| GRAVITY (s=0.004) | 1.0302 | 0.9605 | YES (gravity-specific: TOWARD→AWAY) |

The ZERO control is exactly clean. The crossover at gamma=0.5 is a property
of the complex action kernel (any nonzero field triggers decay), not specific
to 1/r field structure. The gravity-specific claim is the deflection direction
change (TOWARD at gamma=0, AWAY at gamma=0.5).

### Non-label drift basin (drift=0.20, restore=0.70)

| seed | zero source | neutral (+/-) | +/- ratio | 2x ratio |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.000000 | 0.000000 | -1.000 | 1.996 |
| 1 | 0.000000 | 0.000000 | -0.937 | 1.927 |
| 2 | 0.000000 | 0.000000 | -0.959 | 1.954 |

Zero control exact, neutral cancellation exact, charge linearity 93-100%.

## Frozen claim

The narrow review-safe statement:

**One retained grown connectivity family (drift=0.2, restore=0.7) supports
both signed-source and complex-action couplings across a small nearby basin,
with exact zero and neutral controls passing cleanly.**

This is NOT a family-wide transfer claim. It is NOT geometry-generic.
It applies to the specific grown-row neighborhood around the retained
moderate-drift center.

## What this does NOT claim

- Does not claim the basin extends to other drift/restore values
- Does not claim any geometry-generic transfer
- Does not claim the complex-action crossover is unique to gravity
  (the neutral field also shows a crossover)
- Does not claim the h=0.125 continuum limit extends
