# Gauge-Vacuum Plaquette First-Sector Tail Underdetermination Theorem

**Date:** 2026-04-19
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_2026_04_19.py`

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/` (the directory name encodes the failure reason: declared runner path is missing).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: the note declares an exact runner and expected PASS=6, but the runner path is missing, so the two-extension underdetermination construction is not reproducible from the allowed artifacts. Why this blocks: the theorem requires verifying exact agreement on the retained packet and triple while showing different Perron states and Perron/Jacobi packets; prose alone does not establish those equalities and separations. Repair target: restore the runner or replace it with a current executable proof that constructs the zero extension and positive decaying tail extension, checks retained-packet/triple equality, and prints the Perron/Perron-Jacobi separation checks. Claim boundary until fixed: safely claim only that tail completion is posed as the remaining framework-point seam; do not claim a retained underdetermination theorem or explicit inequivalent extension pair.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Question

Once the completed first-sector triple determines a retained packet, and that
retained packet already has an explicit full factorized-class extension, is the
full framework-point packet now determined?

## Answer

No.

Take two full extensions that agree exactly on the retained first-symmetric
packet:

- the zero extension,
- and one positive decaying higher-weight-tail extension.

These two explicit extensions:

- agree exactly on the retained first-sector packet,
- reconstruct the same retained three-sample triple `Z_min`,
- but induce different Perron states and different Perron/Jacobi packets for
  the same explicit source operator `J`.

So the remaining framework-point seam is now specific:

> the higher-weight tail completion of the retained packet,
> equivalently the actual Wilson environment packet.

## Commands run

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_tail_underdetermination_theorem_2026_04_19.py
```

Expected summary:

- `PASS=6 FAIL=0`
