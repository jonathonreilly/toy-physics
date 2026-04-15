# Exact Hessian Selector Uniqueness Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_exact_hessian_selector_uniqueness.py`

## Role

This note closes the next ambiguity after exact Schur normal-form class
uniqueness:

> even if the exact Schur coarse operator stays in one normal-form class, could
> it still induce multiple competing local Hessian selectors inside that class?

On the current branch, the answer is no.

## Result

Across the full admissible exact Schur coarse-operator class at the current
intrinsic local/nonlocal budget scales, the local Hessian selector shape stays
unique at branch scale:

- maximum selector-shape relative `L2` drift stays small
- selector-shape correlation with the reference selector stays effectively one

So the remaining YT gap is no longer selector ambiguity inside the exact Schur
class.

## Meaning

This is stronger than the earlier leading-order Hessian note.

That earlier note showed why the selector exists and why it is positive local
at leading order. This note adds:

> once you restrict to the admissible exact Schur class, the local Hessian
> selector itself is unique at branch scale.

So the only remaining microscopic gap is not “which selector?” but whether the
true bridge belongs to that already-unique class.
