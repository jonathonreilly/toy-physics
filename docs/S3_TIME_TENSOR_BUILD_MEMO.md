# Route 2 Tensor Build Memo

**Date:** 2026-04-14  
**Scope:** `S^3` + anomaly-forced-time Route 2, with atlas support only

## Round verdict

Route 2 is now cleanly organized, but it is **not** closed.

The current exact stack gives:

- exact `S^3` spatial closure
- exact anomaly-forced single-clock time
- exact route-2 background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer / kinetic semigroup `T_R = exp(-Lambda_R)`
- exact scalar support law on the `A1` block
- exact support endpoint theorem for the scalar `A1` datum

What it does **not** yet give is the exact tensor-valued support primitive that
can carry the remaining bright-channel data into a theorem-grade dynamics law.

## 1. Exact objects already available

These objects are already exact and reusable as atlas tools:

### Kinematics

- `S^3` compactification
- anomaly-forced time, with `d_t = 1`
- route-2 background `PL S^3 x R`

### Slice structure

- exact Schur boundary action
- exact slice generator `Lambda_R`
- bounded one-step transfer law `T_R = exp(-Lambda_R)`

### Scalar support law

- exact support scalar
  - `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`
- exact endpoint values
  - `delta_A1(e0) = 1/6`
  - `delta_A1(s / sqrt(6)) = 0`
- exact projective family law
  - `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

### Atlas support

The atlas rows that directly support Route 2 are:

- `ANOMALY_FORCES_TIME_THEOREM.md`
- `OH_SCHUR_BOUNDARY_ACTION_NOTE.md`
- `OH_STATIC_CONSTRAINT_LIFT_NOTE.md`
- `S3_GENERAL_R_DERIVATION_NOTE.md`
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`

Those are the exact Route-2 support tools. The remaining S^3 boundary-link and cap-uniqueness rows are background-selection support only.

## 2. Exact sub-primitives still missing

The committee has now isolated the missing pieces cleanly.

### Missing primitive P1

An exact tensor-valued support observable on the microscopic block

- `A1 x {E_x, T1x}`

The current exact support machinery is scalar/rank-one on `A1`, so it cannot
produce this object.

### Missing primitive P2

Exact tensor endpoint coefficients at the two `A1` endpoints:

- `e0`
- `s / sqrt(6)`

The scalar endpoint theorem is exact, but the tensor endpoint coefficients are
still only bounded prototype data.

### Missing primitive P3

An exact support-to-slice time-coupling law.

We have a bounded staging law through

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

but no exact theorem that upgrades `T_R` from a bounded semigroup into a
tensor-carrying Route-2 dynamics law.

### Missing primitive P4

An exact `PL S^3 x R` spacetime dynamics theorem.

This is the final GR closure layer. It remains absent.

## 3. Which worker looks most promising

Among the three Route-2 workers, the most plausible path to the **first exact
new atlas tool** is **worker 2**.

Reason:

- worker 1 established the sharp blocker: the current exact support stack does
  not contain an exact tensor observable on `A1 x {E_x, T1x}`
- worker 3 produced the clean bounded coupling candidate `Theta_R^(0)`, but it
  is still a staging law, not an exact new tool
- worker 2 anchored the exact scalar endpoint theorem and made the remaining
  projective blindness explicit, which is the cleanest launch point for a new
  microscopic tensor primitive

So the ranking is:

1. worker 2: best path to the first exact new atlas tool
2. worker 3: best bounded bridge candidate, but not yet exact
3. worker 1: best blocker statement, but not a constructive path

## 4. Immediate next theorem

The next theorem should be:

> derive a genuinely new microscopic tensor primitive before exterior
> projection, capable of producing a nonzero tensor observable on
> `A1 x {E_x, T1x}`.

Stated operationally, the next exact theorem target is:

> an exact tensor-valued support observable that refines the scalar `A1`
> support law and supplies the tensor endpoint coefficients natively.

That is the first new atlas tool worth promoting from this round.

## 5. Committee conclusion

Route 2 is now mature enough to be treated as a tool-building program rather
than a single-theorem hunt.

The current clean chain is:

- exact `S^3`
- exact anomaly-forced time
- exact `PL S^3 x R`
- exact `Lambda_R`
- bounded `T_R`
- exact scalar `A1` support law
- exact scalar endpoint theorem
- missing exact tensor support observable

The next real theorem is the missing tensor primitive, not another transfer
matrix or another scalar rewrite.
