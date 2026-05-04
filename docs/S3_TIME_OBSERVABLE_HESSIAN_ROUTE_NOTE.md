# `S^3` + Anomaly-Forced Time: Observable-Hessian Route

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** Final-law committee / observable-principle student  
**Purpose:** test whether the exact source generator `W = log|det(D+J)|`
can produce a route-2 time-curvature or time-coupling law on
`PL S^3 x R` beyond the scalar kinematic selector

## Verdict

**The observable principle remains scalar-only on this route.**

The current atlas gives an exact route-2 kinematic background:

- `S^3` topology is closed
- anomaly-forced time is exact with `d_t = 1`
- the natural background is `PL S^3 x R`

The exact observable principle from the axiom gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`

and local scalar observables are its source-response coefficients.

That is already enough to supply the route-2 selector observable

`O_lift = 1`

but it does **not** supply a tensor-valued time-curvature or time-coupling
law.

## Exact atlas support

The relevant canonical rows in the derivation atlas are:

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  - `log|det(D+J)|` is the unique additive CPT-even scalar generator on the
    exact Grassmann Gaussian surface
- [`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)
  - anomaly cancellation plus chirality force the single-clock `d_t = 1`
- [`S3_GENERAL_R_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
  - the spatial compactification is `PL S^3`
- [`S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md`](./S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md)
  - Route 2 already has the bounded transfer-matrix bridge candidate
    `T_R = exp(-Lambda_R)`

So the atlas already supports the route-2 background and the bounded
transfer candidate. What it does **not** supply is an exact tensor observable
or exact dynamics bridge from the scalar source generator.

## Exact route-2 observable result

The source generator is scalar by construction.

Its local second derivative is a scalar bilinear form:

`∂²W / ∂j_x ∂j_y = - Re Tr[(D+J)^(-1) P_x (D+J)^(-1) P_y]`

On the route-2-sized exact block, this yields only a real symmetric scalar
Hessian over scalar source projectors. It does not generate a tensor-valued
time-coupling law.

The best exact route-2 observable remains the kinematic selector:

`O_lift = 1[S^3 closed] * 1[d_t = 1]`

That is a valid background predicate, not a metric carrier.

## Sharp blocker

The route is blocked because:

1. the observable principle is scalar-only on this route;
2. the exact Hessian lives in scalar source space, not tensor source space;
3. Route 2 does not add a new tensor-valued source operator;
4. the atlas still lacks an exact dynamics bridge that turns the scalar
   generator into a GR time-curvature law.

Equivalently:

> Route 2 gives an exact kinematic lift and a bounded transfer matrix,
> but the observable principle does not upgrade that lift into an exact
> tensor/time-coupling theorem.

## Conclusion

The observable-Hessian route does **not** close the last law.

It proves a sharp negative statement:

> on the current Route-2 atlas, `W = log|det(D+J)|` remains a scalar source
> generator, so the Hessian cannot supply the missing tensor/time-coupling
> law for full GR.

The remaining missing object is still an exact dynamics bridge on
`PL S^3 x R`, not a better scalar selector.
