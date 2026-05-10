# Staggered Backreaction Prototype Results

**Date:** 2026-04-10  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale staggered-backreaction runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `staggered_backreaction_results_2026-04-10`):**

> Issue: The source note is stale relative to scripts/frontier_staggered_backreaction_prototype.py. Current output gives cycle-row R^2 values 0.9830 and 0.9864, so the runner summary reports only 1/3 families with R^2 > 0.99, not machine-precision linearity on all three; current force values are F_ext=+1.488e+00/+1.750e+00/+1.852e+00, F_solve=+5.593e-02/+6.788e-02/+2.183e-01, mean force gap 9.353e-01, and mean self-gap 2.887e-01, all materially different from the frozen table. Why this blocks: the candidate retained-grade prototype depends on its retained checks and exact force table, and the current artifact fails the stated all-family source-response check while moving the scale-gap numerics. Repair target: update the note from the current runner or restore the historical artifact, then add assertions for zero-source, R^2 thresholds, two-body residual, TOWARD counts, force gaps, self-gaps, and norm drift. Claim boundary until fixed: it is safe to claim that the current runner still has exact zero-source reduction, TOWARD force sign, additivity, and one-step endogenous TOWARD behavior, but with weak cycle-row source-response linearity and a large mean force gap 9.353e-01; it is not safe to retain the frozen prototype table or the all-family machine-precision linearity claim.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Question

Can the staggered force result survive when `Phi` is generated from a source
sector on the same graph, instead of being imposed externally?

## Harness

- Script: [`frontier_staggered_backreaction_prototype.py`](../scripts/frontier_staggered_backreaction_prototype.py)
- Families:
  - bipartite random geometric, `n=36`
  - bipartite growing, `n=48`
  - layered bipartite DAG-compatible, `n=36`
- Observable:
  - force `F = < -dPhi/dd >` on the evolved probe state
- Controls:
  - `Phi = 0`
  - external kernel `Phi_ext`
  - source-doubled response
  - one-step endogenous update from the evolved probe density

## First Retained Run

| Family | n | `Phi=0` | solved force | external force | force gap | source-response `R²` | two-body residual | one-step endogenous force | self gap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bipartite random geometric | 36 | `0.00e+00` | `+4.002e-02` | `+3.247e-01` | `8.767e-01` | `1.0000` | `1.862e-16` | `+1.184e-02` | `7.041e-01` |
| bipartite growing | 48 | `0.00e+00` | `+5.066e-02` | `+5.232e-01` | `9.032e-01` | `1.0000` | `2.874e-16` | `+1.782e-02` | `6.482e-01` |
| layered bipartite DAG-compatible | 36 | `0.00e+00` | `+2.127e-01` | `+1.714e+00` | `8.759e-01` | `1.0000` | `2.703e-16` | `+2.097e-01` | `1.453e-02` |

## Readout

- Zero-source reduction is exact on all three families.
- Source-response is linear to machine precision on all three families.
- Two-body additivity is machine precision on all three families.
- The force stays TOWARD on all three families, including the one-step
  endogenous update.
- The solved graph-Poisson field is much weaker than the external-kernel
  control on the cycle-bearing families, while the DAG-compatible family is
  much closer after the one-step endogenous update.

## Main Blocker

The backreaction field is not yet normalized tightly enough to replace the
external kernel as-is. The solver gives the right sign and the right linear
structure, but the force scale is still off by about an order of magnitude on
the cycle-bearing families. A small sweep over the Poisson screening and source
width did not materially change that gap, so this looks structural rather than
a simple normalization typo.

## Interpretation

- This is a real source-generated Phi prototype, not a self-gravity closure.
- The backreaction signal survives the endogenous update, so the transport law
  is not the immediate problem.
- The next step is to iterate the graph-solved Poisson update more aggressively
  and see whether the force scale can be brought onto the same footing as the
  external-kernel control without losing the TOWARD sign.
- Because the naive normalization sweep did not move the gap, the next probe
  should focus on iterative closure or a different source-to-field mapping, not
  on tiny parameter nudges.
