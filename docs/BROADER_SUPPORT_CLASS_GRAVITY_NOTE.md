# Broader Support-Class Gravity: Noncompact Tail Extension and Long-Range Obstruction

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_broader_support_class_gravity.py`  
**Status:** bounded support-class widening beyond compact support, plus a
sharp obstruction for generic long-range algebraic tails

## Purpose

The compact finite-support bridge package is already exact on the current box:

- exact shell source
- exact same-charge bridge
- exact local static-constraint lift
- exact microscopic Schur boundary action
- exact microscopic Dirichlet principle
- support-agnostic across generic finite support on the current Dirichlet box

The remaining question is genuinely broader:

> can the same bridge package be widened to noncompact / long-range support
> classes, or does a sharp decay threshold obstruct it?

This note answers that in the only honest way left:

- yes, the bridge widens to sufficiently fast-decaying noncompact sources
  with finite low moments
- no, it does **not** widen to generic algebraic long-range tails

## Exact support-class widening

Let `rho(x)` be a noncompact but decaying source on the same Dirichlet box.
Write the tail moments outside a matching radius `R` as

- `Q_tail(R) = sum_{|x| > R} rho(x)`
- `M2_tail(R) = sum_{|x| > R} |x|^2 rho(x)`

If the tail decays exponentially, both moments shrink rapidly with `R`, and
the current finite-shell bridge can be widened by truncation with controlled
error. The source is noncompact, but the relevant tail leakage is still
summable and the shell action remains effectively local at the working
resolution.

The same bounded extension persists for sufficiently steep algebraic tails
with finite monopole and quadrupole content. On the current box, the practical
threshold is the finite-second-moment condition:

- `sum |x|^2 rho(x) < infinity`

This is the right notion of “broader support class” for the current bridge
surface.

## Sharp obstruction for generic long-range tails

For algebraic sources `rho(r) ~ r^{-p}` in `d = 3`:

- if `p <= 3`, even the total charge diverges, so the monopole shell law is
  not well-defined
- if `3 < p <= 5`, the monopole is finite but the quadrupole / second-moment
  tail is not, so the local shell action is still sensitive to the long-range
  tail
- only for `p > 5` do the first two moments remain finite in the continuum
  sense needed by the current bridge package

So the bridge does **not** widen to generic long-range power-law support.
The obstruction is not geometric accident; it is the loss of finite low
moments, which the current shell/Dirichlet closure uses implicitly.

## What the script checks

The runner compares four source classes on the same box:

1. exponentially localized noncompact tail
2. algebraic tail with `p > 5`
3. algebraic tail with `3 < p <= 5`
4. algebraic tail with `p <= 3`

For each class it measures:

- monopole tail mass beyond the matching radius
- second-moment tail beyond the matching radius
- exterior truncation error between the full source field and the truncated
  finite-shell approximation

The bounded result is:

- exponential tails are compatible with truncation-stable bridge closure
- steep algebraic tails can be approximated if the low moments stay finite
- generic long-range algebraic tails fail the same finite-shell criterion

## What this closes

This closes the last reasonable “maybe the bridge just needs a broader support
class” escape hatch:

> the exact bridge package widens beyond compact finite support only to the
> extent that the source tail is sufficiently localized to keep the low
> moments finite

## What this still does not close

This note still does **not** close:

1. full nonlinear GR in full generality
2. a truly universal noncompact bridge principle for arbitrary algebraic tails
3. a new tensorial / nonlocal bridge law that would bypass the moment
   obstruction

## Practical conclusion

The remaining gravity gap is now sharply split:

- bounded extension exists for exponentially localized and steep-tail sources
- generic long-range support is obstructed by moment divergence
- the only truly open path to full generality is a new nonlocal or tensorially
  broader bridge principle
