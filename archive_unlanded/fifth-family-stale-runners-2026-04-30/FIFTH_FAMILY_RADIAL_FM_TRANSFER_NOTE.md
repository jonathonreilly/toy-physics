# Fifth Family Radial F~M Transfer Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/fifth-family-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/fifth-family-stale-runners-2026-04-30/` (failure reason: stale runners — the live F~M transfer runner is broken by an import/API mismatch, so the sampled weak-field rows cannot be recomputed from the live repo)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: the current runner for the fifth-family radial F~M transfer is broken by an import/API mismatch, so the sampled weak-field rows cannot be recomputed from the live repo. Why this blocks: a retained finite-computation claim cannot rest only on a stale frozen log when the present script exits before calculating either F~M value, especially with the base radial-family note still unaudited. Repair target: restore or relocate _build_radial_shell_connectivity, _field_from_sources, _centroid_z, and _propagate under the imported API or update this runner to its current helper module, then rerun with explicit PASS thresholds and audit/register FIFTH_FAMILY_RADIAL_NOTE.md as the base family dependency. Claim boundary until fixed: it is safe to say the historical log reported two sampled rows with near-unit F~M; it is not currently an audited retained weak-field transfer.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py)
- [`logs/2026-04-06-fifth-family-radial-fm-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-fm-transfer.txt)
- [`docs/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_NOTE.md)

## Sample Rows

- drift `0.05`, seed `0`: `F~M = 0.999040`
- drift `0.30`, seed `1`: `F~M = 0.999839`

## Safe Read

- weak-field mass scaling is retained on the sampled fifth-family rows
- the transfer is narrow and should be read as a basin result, not a universal theorem

