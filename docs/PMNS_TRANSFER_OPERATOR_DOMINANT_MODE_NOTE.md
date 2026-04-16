# PMNS Transfer-Operator Dominant Mode

**Date:** 2026-04-16  
**Status:** positive native transfer-operator theorem on the `hw=1` triplet  
**Script:** [`frontier_pmns_transfer_operator_dominant_mode.py`](../scripts/frontier_pmns_transfer_operator_dominant_mode.py)

## Question

Can a genuinely dynamical native law on the `hw=1` triplet recover any of the
active microscopic PMNS data from corner-to-corner transport?

## Bottom line

Yes. On the aligned `hw=1` active patch, the native positive transfer kernel

`T_seed = xbar I + ybar (C + C^2)`

has one dominant symmetric mode and one doubly-degenerate orthogonal mode.
Those two eigenvalues reconstruct the active seed pair exactly:

`lambda_+ = xbar + 2 ybar`

`lambda_- = xbar - ybar`

`xbar = (lambda_+ + 2 lambda_-)/3`

`ybar = (lambda_+ - lambda_-)/3`

This is a genuine dynamical law for the active microscopic block on the
`hw=1` triplet. It fixes the aligned seed pair and therefore reproduces the
weak-axis seed patch. It does not determine the `5`-real off-seed
corner-breaking source, because the dominant-mode projection collapses the
zero-sum breaking carrier back onto the aligned seed kernel.

## What is exact

The transfer-kernel route gives:

- an exact dominant mode on the aligned active patch
- an exact doubly-degenerate orthogonal mode
- an exact reconstruction of the aligned active seed pair
- an exact recovery of the weak-axis seed patch

The route is still native: it uses only the `hw=1` triplet transport kernel and
its `C3`-structured spectral decomposition.

## What it does not give

The transfer-operator route does **not** determine the generic `5`-real
corner-breaking source. That source remains outside the transfer-image of this
route.

So this is a positive but bounded dynamical law:

- it closes the aligned seed-pair subset
- it does not close the full off-seed microscopic value law

## Theorem

**Theorem (PMNS transfer-operator dominant-mode law).** On the aligned `hw=1`
active patch, the native transfer kernel `T_seed` has a unique dominant
symmetric mode and a doubly-degenerate orthogonal mode. Those two eigenvalues
reconstruct the active seed pair `(xbar, ybar)` exactly, and the same route
recovers the weak-axis seed patch. The route does not determine the `5`-real
corner-breaking source.

## Verification

```bash
python3 scripts/frontier_pmns_transfer_operator_dominant_mode.py
```
