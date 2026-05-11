# Fifth Family Radial Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/fifth-family-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/fifth-family-stale-runners-2026-04-30/` (failure reason: stale runners — shared helper import mismatch causes the declared sweep, basin, and F~M transfer scripts to exit before computing the audited observables)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: the current radial-shell fifth-family artifact chain is broken by a shared helper import mismatch across the sweep, basin, and F~M transfer scripts. Why this blocks: a retained finite basin cannot be audited from stale frozen logs when the present scripts exit before checking zero-source control, neutral cancellation, sign orientation, or F~M, and downstream companion notes already fail for the same reason. Repair target: restore or move the radial-shell helper API used by these scripts, or update the scripts to import the current implementation, then rerun the sweep, basin, and F~M transfer with explicit PASS thresholds for the two retained rows and the boundary row. Claim boundary until fixed: it is safe only to say historical logs reported a narrow sampled radial-shell basin; it is not currently an audited retained fifth structured family.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/FIFTH_FAMILY_RADIAL_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_SWEEP.py)
- [`scripts/FIFTH_FAMILY_RADIAL_BASIN.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_BASIN.py)
- [`scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py)
- [`logs/2026-04-06-fifth-family-radial.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial.txt)
- [`logs/2026-04-06-fifth-family-radial-basin.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-basin.txt)
- [`logs/2026-04-06-fifth-family-radial-fm-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-fm-transfer.txt)

## Question

Does a genuinely different structured connectivity family survive the exact zero/neutral gate on the no-restore grown slice?

## Retained Rows

Sampled rows supporting the narrow basin:

- drift `0.05`, seed `0`
- drift `0.30`, seed `1`

Both rows satisfy:
- exact zero-source baseline
- exact neutral same-point cancellation
- sign orientation
- weak-field linearity near `F~M = 1`

## Boundary Row

The interior probe at:

- drift `0.20`, seed `0`

fails sign orientation even though exact controls remain clean. That makes this family selective, not broad.

## Safe Read

- the radial-shell connectivity rule is a real fifth structured family basin on the sampled rows
- the basin is narrow and seed-selective
- the miss is a sign-orientation boundary, not a control leak

