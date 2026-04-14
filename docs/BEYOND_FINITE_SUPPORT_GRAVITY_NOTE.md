# Beyond Finite Support in Gravity: Exact Low-Moment Threshold and Long-Range Obstruction

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_beyond_finite_support_gravity.py`  
**Status:** sharp obstruction for generic long-range tails; bounded extension
for sufficiently fast-decaying noncompact sources

## Purpose

The bridge package is already exact on:

- compact finite support
- generic finite support inside the current Dirichlet box
- sufficiently fast-decaying noncompact tails

The only remaining support-class question is sharper:

> where exactly does the bridge stop when the source support becomes genuinely
> long-range?

This note answers that with the strictest clean statement available on the
current branch.

## Exact stop condition

The current bridge package uses a finite-shell / Schur / Dirichlet closure that
depends on finite low moments of the exterior source tail.

In 3D the relevant threshold is the second moment:

- finite monopole requires `sum rho < infinity`
- finite shell-stress closure requires `sum |x|^2 rho(x) < infinity`

For algebraic tails `rho(r) ~ r^{-p}` this gives the exact low-moment boundary:

- `p > 5`  -> the current bridge package remains truncation-stable
- `p = 5`  -> borderline logarithmic failure of the quadrupole / second moment
- `p < 5`  -> the second moment diverges and the current bridge package stops

So the exact support-class theorem stops at the finite-second-moment class.
It does **not** widen to generic long-range power-law support.

## What still widens

The bridge package does widen beyond compact support to:

- exponentially localized noncompact tails
- sufficiently steep algebraic tails with `p > 5`

At that level, truncation to the current finite sewing band is still
controlled.

## What fails

Generic long-range algebraic tails fail for one of two reasons:

- `p <= 3`: even the monopole is not well-defined
- `3 < p <= 5`: the monopole is finite, but the second moment / shell-stress
  closure is not, so the current bridge action remains tail-sensitive

This is the sharp obstruction: the bridge cannot be widened to arbitrary
noncompact long-range support without a new nonlocal or tensorially broader
bridge principle.

## Time-dependent sources

This note does **not** attempt time-dependent sources. The current bridge
theorem is static and equal-time; a time-dependent source would require a
frequency-resolved boundary operator, which is a separate obstruction.

## What the script checks

The runner tests four classes on the same box:

1. exponential tails (`e^{-r/\xi}`)
2. steep algebraic tails (`p = 5.5`)
3. borderline algebraic tails (`p = 5.0`)
4. long-range algebraic tails (`p = 4.5`, `p = 2.5`)

For each class it checks:

- tail monopole and second moment
- truncation error versus the full Poisson field
- box-size growth of the tail moments

The clean numerical message is:

- exponential tails are truncation-stable
- `p = 5.5` remains stable at current resolution
- `p = 5.0` is borderline and does not settle cleanly
- `p = 4.5` and `p = 2.5` are genuinely obstructed

## Practical conclusion

The bridge package now has a precise support-class frontier:

- compact support: exact
- generic finite support on the box: exact
- sufficiently fast-decaying noncompact tails: bounded extension
- generic long-range algebraic tails: obstructed at `p <= 5`

That is the sharpest support-class statement currently defensible on this
branch.
