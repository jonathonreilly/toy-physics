# Route 2 New-Primitive Build Memo

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** synthesis chair for the Route 2 new-primitive committee  
**Scope:** compare the three construction attempts against the current Route 2
primitive chain and atlas support

## Committee verdict

Route 2 is no longer a search for a hidden GR closure theorem inside the
existing support stack.

The current exact stack already gives:

- exact `S^3` spatial closure
- exact anomaly-forced single-clock time
- exact route-2 background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer / kinetic semigroup `T_R = exp(-Lambda_R)`
- exact scalar support law on the `A1` block
- exact scalar support endpoint theorem for `delta_A1`

What it does **not** yet give is an exact tensor-valued support primitive on
`A1 x {E_x, T1x}`.

The current exact support machinery is scalar/rank-one on `A1`, so the direct
tensor-primitive attempt is dead on the present atlas.

## Compare the three construction attempts

### Attempt 1: direct new tensor primitive from the current support algebra

**Candidate**
- exact tensor-valued support observable on `A1 x {E_x, T1x}`

**Status**
- dead on the current atlas

**Reason**
- the exact support Hessian has no mixed `A1`-bright block
- the exact support-to-active operator is rank one and charge-only
- the exact support scalar `delta_A1` is blind to `E_x` and `T1x`
- the mixed support operator vanishes to machine precision

**Conclusion**
- the current support algebra cannot by itself produce a nonzero exact tensor
  observable
- do not spend more committee time trying to squeeze the primitive out of the
  present scalar/rank-one support stack

### Attempt 2: exact endpoint-coefficient theorem on the scalar support law

**Candidate**
- exact support endpoint theorem for `delta_A1`

**Status**
- exact and reusable

**Reason**
- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`
- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

**Why this is the most plausible first exact new atlas tool**
- it is already theorem-grade on `main`
- it is the only exact primitive here that cleanly exposes the projective
  `A1` datum
- it is the right launch point for a future tensor primitive because it fixes
  the scalar background variable before any tensor lift is attempted

**Conclusion**
- this is the best current exact tool to keep and reuse
- it is the cleanest exact foundation for the next tensor construction

### Attempt 3: bounded tensor prototype / transfer bridge

**Candidate**
- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`
- bounded `T_R = exp(-Lambda_R)` / `Theta_R^(0)` bridge

**Status**
- bounded but useful

**Reason**
- it is the cleanest staging object on the current tensor frontier
- it tracks the aligned `E_x` and `T1x` bright channels correctly
- it gives a useful comparison surface for future exact tools
- it does **not** become an exact tensor observable on the current support
  stack

**Conclusion**
- keep it as the bounded prototype and comparison surface
- do not promote it as the exact atlas tool

## Atlas support

The current atlas support confirms the same ranking:

- exact Route 2 support tools:
  - `ANOMALY_FORCES_TIME_THEOREM.md`
  - `OH_SCHUR_BOUNDARY_ACTION_NOTE.md`
  - `OH_STATIC_CONSTRAINT_LIFT_NOTE.md`
  - `S3_GENERAL_R_DERIVATION_NOTE.md`
  - `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- background-selection support only:
  - `S3_BOUNDARY_LINK_THEOREM.md`
  - `S3_CAP_UNIQUENESS_NOTE.md`

The atlas does not contain a hidden exact tensor carrier on the current support
stack. The committee’s blocker notes confirm that the mixed block is zero and
the support map remains scalar/rank-one.

## Immediate next theorem

The next theorem should be:

> derive a genuinely new microscopic tensor primitive before exterior
> projection, capable of producing a nonzero tensor observable on
> `A1 x {E_x, T1x}`.

Operationally, that means:

1. build a new tensor-valued support observable that is not the current
   scalar/rank-one support algebra
2. use the exact scalar endpoint law `delta_A1` as the background variable
   that the new tensor primitive must refine
3. only then attempt to upgrade the bounded `Theta_R^(0)` prototype into an
   exact atlas tool

## Final ranking

1. **Most plausible first exact new atlas tool:** the exact scalar endpoint
   theorem on `delta_A1`
2. **Bounded but useful:** `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`
3. **Dead:** direct tensor primitive from the current exact support algebra
   on `A1 x {E_x, T1x}`

That ranking is consistent with the current primitive chain, the tensor
blockers, the tensor prototype, and the atlas support.

