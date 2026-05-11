# Second Independent Grown Family

**Date:** 2026-04-06
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/grown-family-missing-artifacts-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/grown-family-missing-artifacts-2026-04-30/` (failure reason: missing artifacts — the load-bearing battery script `scripts/second_grown_family_battery.py` is explicitly labeled as not yet frozen, and no frozen output is provided in the artifact chain)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: The note's retained positive result rests on a missing artifact, scripts/second_grown_family_battery.py, explicitly labeled as not yet frozen, and no frozen output is provided in the artifact chain. Why this blocks: the quoted F~M, Born, gravity, and complex-action control-battery numbers are unreviewable from the allowed source and artifacts, so the candidate retained-grade second-family claim cannot be independently reproduced or checked. Repair target: restore or recreate the exact battery script, add a frozen log and preferably a PASS/FAIL assertion runner, or replace this note with audit-clean sign/complex second-family notes that actually carry the evidence. Claim boundary until fixed: it is safe to say this note records a historical candidate at drift=0.05, restore=0.30; it is not safe to claim a retained second independent grown family from the current artifact chain.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact chain

- [`scripts/second_grown_family_battery.py`](../scripts/second_grown_family_battery.py) (to be frozen)
- This note

## Question

Does a SECOND independent grown family (different drift/restore from the
retained center 0.2/0.7) independently produce gravity + Born + F~M ~ 1.0?

## Sweep result

9 candidate families tested. Best second candidate: **drift=0.05, restore=0.30**.

This is maximally distant from the retained center:
- drift: 0.05 vs 0.20 (4x different)
- restore: 0.30 vs 0.70 (very different architecture)

## Full control battery at drift=0.05, restore=0.30

| Test | Result | Pass? |
| --- | ---: | --- |
| Zero field control | delta=0.000, escape=1.000 | YES |
| F~M (6 seeds) | 0.993 +/- 0.008 | YES |
| Born (2 seeds) | 0.00e+00 | YES |
| Gravity TOWARD | 3/3 at gamma=0 | YES |
| Complex action crossover | TOWARD 3/3 → AWAY 0/3 | YES |

## What this means

Two independent grown families, at different points in parameter space,
both produce:
- F~M ~ 1.0 (Newtonian mass scaling)
- Born = 0 (structural linearity)
- Gravity TOWARD
- Complex action TOWARD→AWAY crossover

This is evidence that the physics is NOT specific to one growth-rule tuning.
It transfers across a significant region of parameter space.

## Claim boundary

Two specific grown families tested. No claim about the full drift/restore
space or about arbitrary growth rules.
