# Exact Hessian Selector Uniqueness Note

**Date:** 2026-04-15 (claim narrowed 2026-05-01)
**Status:** bounded support theorem (selector DIRECTION uniqueness; selector SHAPE drift bounded but above branch budget)
**Primary runner:** `scripts/frontier_yt_exact_hessian_selector_uniqueness.py`

## Role

This note characterises the next ambiguity after exact Schur normal-form
class uniqueness:

> even if the exact Schur coarse operator stays in one normal-form class, could
> it still induce multiple competing local Hessian selectors inside that class?

On the current package, the answer is partial: the selector **direction**
is essentially unique across the admissible Schur class, but the selector
**shape** still has measurable drift above the branch-budget tolerance.

## Result (claim narrowed 2026-05-01)

Across the full admissible exact Schur coarse-operator class at the current
intrinsic local/nonlocal budget scales, the runner measures:

| quantity                                       | value             | claim |
|------------------------------------------------|-------------------|-------|
| min Hessian eigenvalue (positive-definiteness) | 3.76e+01          | PASS — every operator in the class stays SPD |
| min selector-shape correlation w/ reference    | 0.9974            | PASS at "direction-uniqueness" (corr > 0.99) |
| max selector-shape relative L2 drift           | 7.20e-02 (~7.2%)  | PASS at "bounded drift" (< 10%); FAIL at branch-budget tolerance (1.2%) |

So the substantive content is:

1. **Selector existence + positivity:** every admissible Schur coarse
   operator in the tested class produces a positive-definite local Hessian.
2. **Selector direction uniqueness:** the selector unit-vector cosine with
   the reference selector stays above 0.99 across the entire admissible
   class. The *direction* of the selector is essentially unique.
3. **Bounded shape drift:** the selector L2 magnitude varies by up to
   ~7.2% across the admissible class. This is bounded — it is not
   unbounded ambiguity — but it is NOT inside the branch-budget tolerance
   of 1.2% required for a strict "uniqueness theorem".

An earlier draft of this note claimed full selector uniqueness on the
tested scale and said "the remaining YT gap is no longer selector
ambiguity." That over-stated the result: the runner's own checks
(`max rel L2 drift < 2.5e-2`, `min corr > 0.999`) failed against the
measurement. The narrowed claim above is what the data actually
support, and it is what the runner now classifies PASS/FAIL against.

## Meaning

This is stronger than the earlier leading-order Hessian note in two
respects:

> once you restrict to the admissible exact Schur class:
>   - the local Hessian remains SPD,
>   - the selector direction is essentially unique (correlation > 0.99).

But it does **not** strengthen to full shape uniqueness inside branch
budget. The remaining microscopic gap therefore decomposes into two
sub-gaps, not one:

(a) selector shape uniqueness still has a ~7% residual norm drift across
    the admissible Schur class, above the branch-budget tolerance (1.2%);
(b) the open question of whether the true bridge belongs to that
    admissible class at all (unchanged).

Closing (a) requires either tightening the admissible class (more
restrictive intrinsic budgets, or an additional invariant constraint
that picks a smaller subclass) or exhibiting a bound on observable
sensitivity to the residual norm drift. The runner now reports both
the bounded-direction-uniqueness PASS and the branch-budget FAIL
explicitly so the residual is auditable rather than hidden.
