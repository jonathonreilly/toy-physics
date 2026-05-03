# Gauge-Vacuum Plaquette First-Sector First-Hankel to DM Boundary

**Date:** 2026-04-19  
**Status:** support - structural or confirmatory support note
that still has to be fixed before quantitative DM matching is the first
Hankel packet `(m1,m2)`, equivalently the first Jacobi layer
`(alpha0,beta1)`  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_first_hankel_to_dm_boundary_2026_04_19.py` (**MISSING — flagged for re-audit**)

> **Missing primary runner (2026-05-03 audit-repair scan):**
> The script above is referenced as this note's primary runner but does not
> exist in the current `scripts/` tree. Sibling notes in the same lane were
> archived to `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`;
> this note is left active pending a runner-rewrite decision. The audit
> verdict on this note will be redone once a working runner is registered
> or the note is moved to archive.

## Bottom line

The nilpotent-chain packet-to-DM boundary already closes the downstream local
interface once the actual Wilson/PF packet is supplied.

The new point is upstream:

- the earliest Wilson-side scalar packet feeding that interface is exactly the
  first Hankel packet `(m1,m2)`,
- equivalently the first Jacobi layer `(alpha0,beta1)`,
- and the current stack still leaves that packet open on the live route.

So the quantitative DM seam now starts exactly at the first-Hankel layer of
`K_6^env` after identity-rim reduction.

## Commands run

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_first_hankel_to_dm_boundary_2026_04_19.py
```

Expected summary:

- `PASS=5 FAIL=0`
