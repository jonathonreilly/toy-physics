# Lambda Gauge / Observables Quotient Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** test whether the current lambda family is removed by quotient-local observables or survives in the best global observables

## Verdict

The current atlas splits `lambda` into two different roles:

1. On the **local quotient** of the current observable stack, `lambda` is invisible.
2. On the **best global observable** currently available, `lambda` is still exact and measurable.

So the exact answer is:

> `lambda` is gauge on the local quotient, but it is not eliminated by the full current observable set.

That means we do **not** yet have a global theorem saying `lambda` can be dropped.

## Exact lambda-independent quotient data

The following are lambda-independent in the current atlas:

- the exact `Pi_A1` core projection onto lapse plus spatial trace;
- the normalized weight-1 lift Gram data;
- the local curvature-side observables on the punctured dark bundle;
- the Route-2 time semigroup factor `exp(-t Lambda_R)`.

These objects factor through the observable quotient and do not choose a section in the weight-1 multiplicity space.

## Exact lambda-sensitive data

The surviving global observable is the winding-one dark-plane holonomy:

`Hol_lambda(gamma) = 2 pi lambda`

for a loop that winds once around the dark singular set.

That is not fixed by:

- `Pi_A1`;
- the local curvature quotient;
- punctured-bundle flatness;
- cut-domain trivialization;
- Route-2 semigroup transport.

So the best current observable remains lambda-sensitive.

## Time component

The Route-2 time factor does not select `lambda`.

The semigroup transport `exp(-t Lambda_R)` is exact and contractive, but it acts on the time/slice factor separately from the dark-plane multiplicity choice. In the current atlas, time transport therefore does not canonize the one-parameter lift family.

## Strongest exact quotient statement

The strongest exact statement supported by the current atlas is local, not global:

`(Pi_A1 core, normalized weight-1 quotient data, local curvature observables) / SO(2)`

is lambda-independent.

But the global holonomy character is still:

`A_lambda = lambda d vartheta_R`

and that remains a genuine one-parameter family.

## Bottom line

The current atlas does not remove `lambda`.

It shows that `lambda` is invisible to the local quotient observables, but it also shows that the full observable set still contains an exact lambda-sensitive holonomy character. So `lambda` is not yet optional in the global theory surface.
