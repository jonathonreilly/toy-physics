# Critical Exponents vs Topology

**Date:** 2026-04-10
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/topology-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.
**Script:** `frontier_critical_exponents.py`

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/topology-stale-runners-2026-04-30/` (failure reason: stale runners — the note's current-output table is stale relative to `scripts/frontier_critical_exponents.py`; live runner output differs from the table and half the rows are degenerate)
- **Audit verdict_rationale (quoted verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json)):**

  > Issue: the source note's current-output table is stale relative to scripts/frontier_critical_exponents.py; the live output gives random_geometric_s8 degenerate at G_crit=1.0, random_geometric_s10 beta=0.7328 at G_crit=2.0, growing_n64 beta=0.3675 at G_crit=14.0, layered_cycle_8x8 beta=0.3348 at G_crit=5.0, and both causal-DAG rows degenerate. Why this blocks: a hostile physicist cannot retain the note's specific beta table or six-family interpretation when half the current rows are degenerate and the fit values have changed. Repair target: update the note to the live runner output, fix the runner path registration to scripts/frontier_critical_exponents.py, add assertions for fit/degenerate acceptance criteria, and rerun any intended multi-size or multi-seed checks before promoting topology-dependence beyond a scout. Claim boundary until fixed: it is safe to say the current runner is a finite-size scout with three nondegenerate fits whose beta values differ across topology labels; it is not safe to retain the stale table or any universality-class inference.

- **Do-not-cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Question

Does the self-gravity localization onset show the same fitted exponent on all
admissible graph families, or does the exponent depend on topology?

## Probe

- Evolve staggered self-gravity on representative admissible graph families.
- Use the order parameter `op(G) = max(0, 1 - width_self / width_free)`.
- Fit the onset branch to `op(G) ~ A * (G - G_crit)^beta`.

This is a **finite-size onset characterization**, not a universal critical-law
proof.

## Current outputs

| Family label | Base family | n | G_crit | beta | R² | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `random_geometric_s8` | random geometric | 64 | 18.0 | 0.1744 | 0.8506 | fit |
| `random_geometric_s10` | random geometric | 100 | 10.0 | 0.4600 | 0.9700 | fit |
| `growing_n64` | growing | 64 | 50.0 | 0.6453 | 0.9759 | fit |
| `layered_cycle_8x8` | layered cycle | 64 | 24.0 | 0.1315 | 0.8086 | fit |
| `causal_dag_10x6` | causal DAG | 55 | 28.0 | 0.0769 | 0.9403 | fit |
| `causal_dag_8x8` | causal DAG | 57 | `1.0` | `nan` | `nan` | degenerate |

## Honest reading

- The fitted `beta` values vary substantially across admissible graph families.
- That is evidence for **topology-dependent finite-size onset behavior**.
- It is **not yet** evidence for a new universality class in the strong sense,
  because:
  - the fits are still finite-size and single-geometry representatives
  - one DAG configuration is degenerate
  - there is no proper finite-size scaling collapse yet

## What this closes

- The project no longer needs to assume mean-field exponents by default.
- There is now a concrete, script-backed reason to treat topology as an active
  variable in the localization transition.

## What remains open

1. finite-size scaling on each family, not just one representative graph
2. multi-seed robustness
3. holdout graph families
4. an order parameter that remains clean on both cycle-bearing and DAG-like
   families
