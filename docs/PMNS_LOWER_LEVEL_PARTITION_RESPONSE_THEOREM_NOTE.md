# PMNS Lower-Level Partition Response Theorem

**Date:** 2026-04-16  
**Status:** exact lower-level source-response theorem  
**Script:** `scripts/frontier_pmns_lower_level_partition_response_theorem.py`

## Question

Is the lower-level PMNS response pack still an imported object, or is it
already native once the lower-level baselines are fixed?

## Bottom line

It is native.

For the lower-level active/passive baselines

`K_act = I - lambda_act (Y_act - I)`,

`K_pass = I - lambda_pass Y_pass`,

the exact Grassmann partition amplitude is

`Z[J] = det(K + J)`.

Its matrix-unit source coefficients recover the full response kernel:

`d/dt log det(K + t E_ij)|_{t=0} = (K^{-1})_{ji}`.

So the lower-level response columns are exact partition-response coefficients of
the native source-deformed determinant, not an imported ansatz.

## What this closes

Once the lower-level baselines are fixed:

- the active/passive lower-level response columns are exact native data
- the existing lower-level PMNS closure stack reconstructs the active block and
  passive block exactly
- the active 4-real source is fixed exactly from the active response profile
- the PMNS branch, sheet, Hermitian data, masses, and PMNS matrix are fixed
  downstream with no PMNS-side target inputs

So the response pack itself is no longer the live gap.

## What remains open

This theorem is no longer the last word on the lower-level gap.

The follow-on Schur-pushforward theorem shows that microscopic sector
completions are quotient data on this lane. So the live remaining theorem is
now:

> derive or select the effective active/passive blocks that source that
> lower-level pack from `Cl(3)` on `Z^3`.

So the observation-free branch-selection problem has been pushed down from the
response pack past microscopic completion and onto the effective-block/source
law.

## Consequence for the lane

This remains a real positive advance.

The live normalization/branch-selection lane should no longer be phrased as:

- “derive the lower-level response pack”
- “derive the microscopic sector completion”

It should now be phrased as:

- “derive the effective active/passive block law whose exact
  partition-response pack is already known to close PMNS downstream”

## Command

```bash
python3 scripts/frontier_pmns_lower_level_partition_response_theorem.py
```
