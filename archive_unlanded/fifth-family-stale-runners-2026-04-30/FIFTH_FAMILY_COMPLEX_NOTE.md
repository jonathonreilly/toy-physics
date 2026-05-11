# Fifth Family Complex Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/fifth-family-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/fifth-family-stale-runners-2026-04-30/` (failure reason: stale runners — the live runner for the retained fifth-family complex companion is broken by an import mismatch, so the claimed anchor-row positive cannot be reproduced from current source)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: the live runner for the retained fifth-family complex companion is broken by an import mismatch, so the claimed anchor-row positive cannot be reproduced from the current source. Why this blocks: a hostile referee cannot accept a retained finite-computation claim from a stale frozen log when the present runner exits before computing Born, crossover, or F~M, and the upstream radial-shell family note has not itself been audited. Repair target: update FIFTH_FAMILY_COMPLEX_TARGETED.py to the current connectivity helper API or restore the missing _field_from_sources helper, rerun the anchor-row computation with explicit PASS thresholds for Born, crossover, and F~M, and audit/register FIFTH_FAMILY_RADIAL_NOTE.md as the base family dependency. Claim boundary until fixed: it is safe only to say a historical frozen log reported one drift=0.20, seed=0 complex companion candidate; it is not currently an audited retained anchor-row positive.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py)
- [`logs/2026-04-06-fifth-family-complex-targeted.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-complex-targeted.txt)
- [`docs/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_NOTE.md)

## Question

Does the retained radial-shell fifth-family basin also carry a narrow complex-action companion?

## Retained Anchor

The anchor row at:

- drift `0.20`
- seed `0`

retains the complex-action companion narrowly:

- exact `gamma = 0` baseline: clean
- Born proxy: `0.000e+00`
- `TOWARD -> AWAY` crossover: yes
- weak-field `F~M`: `1.000` at both `gamma = 0` and `gamma = 0.5`

## Narrow Read

The retained companion is real, but it is small:

- the anchor row carries the crossover
- the radial-shell family remains selective rather than family-wide
- the companion is therefore a narrow basin, not a broad closure

## Final Verdict

**retained narrow anchor-row positive**
