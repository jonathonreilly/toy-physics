# `S^3` + Anomaly-Forced Time: Observable-Hessian Route

**Date:** 2026-04-14
**Claim type:** open_gate
**Status:** open - scalar-only observable route; no tensor/time-coupling law
**Primary runner:** `scripts/frontier_universal_gr_tensor_action_blocker.py`

## Verdict

The observable principle remains scalar-only on this route.

The current atlas gives an exact route-2 kinematic background:

- `S^3` topology;
- anomaly-forced time with `d_t = 1`;
- the natural background `PL S^3 x R`.

The exact observable principle from the axiom gives the scalar generator

```text
W[J] = log|det(D+J)| - log|det D|
```

and local scalar observables are its source-response coefficients. That is
enough to supply the route-2 selector observable

```text
O_lift = 1
```

but it does not supply a tensor-valued time-curvature or time-coupling law.

## Atlas Support

The relevant route ingredients are already represented in the repo:

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  gives the scalar source generator;
- [`S3_ANOMALY_SPACETIME_LIFT_NOTE.md`](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
  records the `PL S^3 x R` kinematic lift and missing dynamics bridge;
- [`S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md`](S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md)
  records the bounded transfer-matrix bridge candidate.

Those inputs support the route-2 background and the bounded transfer
candidate. They do not supply an exact tensor observable or exact dynamics
bridge from the scalar source generator.

## Route-2 Hessian Result

The source generator is scalar by construction. Its local second derivative is
a scalar bilinear form:

```text
d^2 W / (d j_x d j_y)
  = - Re Tr[(D+J)^(-1) P_x (D+J)^(-1) P_y]
```

On the route-2-sized exact block, this yields a real symmetric scalar Hessian
over scalar source projectors. It does not generate a tensor-valued
time-coupling law.

The best exact route-2 observable remains the kinematic selector:

```text
O_lift = 1[S^3 closed] * 1[d_t = 1]
```

That is a valid background predicate, not a metric carrier.

## Sharp Blocker

The route is blocked because:

1. the observable principle is scalar-only on this route;
2. the exact Hessian lives in scalar source space, not tensor source space;
3. route 2 does not add a new tensor-valued source operator;
4. the atlas still lacks an exact dynamics bridge that turns the scalar
   generator into a GR time-curvature law.

Equivalently, route 2 gives an exact kinematic lift and a bounded transfer
matrix, but the observable principle does not upgrade that lift into an exact
tensor/time-coupling theorem.

## Conclusion

The observable-Hessian route does not close the last law. It proves the sharp
negative boundary that, on the current route-2 atlas, `W = log|det(D+J)|`
remains a scalar source generator, so the Hessian cannot supply the missing
tensor/time-coupling law for full GR.
