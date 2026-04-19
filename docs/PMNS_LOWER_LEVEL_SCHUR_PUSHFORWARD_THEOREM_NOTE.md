# PMNS Lower-Level Schur-Pushforward Theorem

**Date:** 2026-04-16  
**Status:** exact lower-level quotient theorem  
**Script:** `scripts/frontier_pmns_lower_level_schur_pushforward_theorem.py`

## Question

After the partition-response theorem, is the live PMNS lower-level gap still a
microscopic sector-operator law, or does the full microscopic source-response
already factor exactly through the Schur effective blocks?

## Bottom line

It factors exactly through the Schur effective blocks.

For the lower-level active/passive full baselines

`K_act^full = I - lambda_act (Y_full - I)`,

`K_pass^full = I - lambda_pass Y_full`,

and any support-restricted source `J_sup` on the `3 x 3` PMNS support, the full
microscopic source response

`log det(K_full + J_sup^full) - log det(K_full)`

depends only on the Schur effective baseline on that support.

Equivalently, the support block of `(K_full)^(-1)` is exactly the inverse of the
Schur effective baseline.

## What this closes

This kills the microscopic-completion ambiguity on the lower-level PMNS lane.

- distinct microscopic active-sector completions can realize the same effective
  active block
- distinct microscopic passive-sector completions can realize the same
  effective passive block
- those distinct completions produce identical lower-level response columns
- downstream PMNS closure data are identical across such completions

So the microscopic sector operator is exact quotient data once its Schur
effective block is fixed.

## What remains open

The remaining lower-level PMNS gap is not a microscopic sector-operator law.
It is the native law for the effective active/passive blocks that survive exact
Schur pushforward.

In other words, the live theorem has moved one layer down again:

- not “derive the response pack”
- not “derive the microscopic completion”
- now “derive the effective-block/source law”

## Consequence for the lane

The observation-free PMNS normalization/branch-selection lane is now sharper.

The existing lower-level stack already closes everything downstream of the
effective active/passive blocks:

- partition response gives the lower-level pack
- the lower-level pack gives the active source
- the active source fixes the branch, sheet, Hermitian data, masses, and PMNS

So the only live lower-level freedom is the effective-block law itself.

## Command

```bash
python3 scripts/frontier_pmns_lower_level_schur_pushforward_theorem.py
```
