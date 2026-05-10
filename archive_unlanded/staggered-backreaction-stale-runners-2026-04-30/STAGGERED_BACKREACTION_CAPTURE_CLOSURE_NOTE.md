# Staggered Backreaction Capture-Closure Note

**Date:** 2026-04-10  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale staggered-backreaction runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `staggered_backreaction_capture_closure_note`):**

> Issue: The source note's load-bearing force/gap/gain table is stale relative to scripts/frontier_staggered_backreaction_capture_closure_harness.py. Current output gives random_geometric F_closed=+6.443e-01, F_ext=+1.101e+00, closed gap 41.5%, gain 15.221; growing F_closed=+3.304e-01, F_ext=+7.062e-01, closed gap 53.2%, gain 27.734; cycle mean gap 9.828e-01 -> 4.734e-01 (2.08x); holdout gap 9.191e-01 -> 4.559e-01 (2.02x). Why this blocks: the candidate retained-grade closure depends on the claimed near-capture of the external-kernel force scale, but the live runner shows a much weaker and numerically different closure than the note freezes. Repair target: determine whether the note or runner drifted, rerun the intended artifact, update the frozen table, and add assertion gates for closed gap, improvement factor, gains, R^2, score, and holdout gap before any retained closure claim. Claim boundary until fixed: it is safe to claim that the current runner preserves the two 9/9 cycle-battery scores, zero-source controls, additivity, TOWARD sign, and high linearity while improving force-scale gaps by about 2x; it is not safe to claim the frozen 4.03x/5.15x closure or a retained near-capture of the external-kernel scale.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Objective

Move the source-generated staggered field materially closer to the
external-kernel force scale without relying on another fitted global gain, and
without losing the retained force battery on the cycle-bearing graphs.

## Harness

- Script: [`frontier_staggered_backreaction_capture_closure_harness.py`](../scripts/frontier_staggered_backreaction_capture_closure_harness.py)
- Cycle-bearing retained battery:
  - `random_geometric`, `n=36`
  - `growing`, `n=48`
- Layered holdout:
  - `layered_bipartite_dag_s29_n55`
- Observable:
  - force `F = < -dPhi/dd >`

## Closure Rule

The source sector is closed iteratively on the same graph:

1. start from the local Gaussian seed source
2. evolve the staggered probe in the solved graph field
3. refresh the source shape with a 50/50 blend of
   - the original seed source
   - one normalized-Laplacian sharpen step applied to the returned density
4. update the source gain from the source-pocket capture deficit:

`gain <- capture^(-3/2)`

with relaxed fixed-point iteration.

The external kernel is **not** used to fit the closure. It remains a control
only.

## Exact Cycle-Battery Results

| Graph | Score | Closed force | External force | Baseline gap | Closed gap | `R^2` | Gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_geometric` | `9/9` | `+4.842e-01` | `+5.200e-01` | `9.690e-01` | `6.880e-02` | `0.999265` | `44.504` |
| `growing` | `9/9` | `+3.222e-01` | `+5.534e-01` | `9.944e-01` | `4.178e-01` | `0.998906` | `100.726` |

Retained rows stayed intact:

- zero-source control exact on both graphs
- source-response linearity stayed above `0.9989`
- two-body additivity stayed at machine precision
- iterative stability stayed `15/15` TOWARD
- norm drift stayed at machine precision
- state-family robustness stayed `3/3`
- native gauge row still passed

Cycle-bearing mean force gap:

- baseline: `9.817e-01`
- closed: `2.433e-01`
- improvement: `4.03x`

## Layered Holdout

On `layered_bipartite_dag_s29_n55`:

- closed force: `+1.655e+00`
- external force: `+2.010e+00`
- baseline gap: `9.080e-01`
- closed gap: `1.764e-01`
- improvement: `5.15x`
- source-response `R^2 = 0.999777`

So the closure is not just rescuing the cycle-bearing rows by a graph-specific
fit. One larger layered holdout also moves substantially toward the external
control.

## Readout

- The earlier linear-map lane was right that the missing piece was the source
  sector itself, not the force observable.
- A self-consistent capture closure can preserve the retained cycle battery
  while moving the solved field much closer to the external-kernel scale.
- The growing graph remains the harder cycle-bearing row, so this is not yet a
  universal closure theorem.
- But the blocker is no longer "the endogenous field always stays an order of
  magnitude too weak." That statement is now false on the retained harness.
