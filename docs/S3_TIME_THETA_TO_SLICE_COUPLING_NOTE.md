# Route 2 `Theta_R` to Slice Coupling: Bounded Candidate and Exact Blocker

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** Route 2 / worker 3  
**Purpose:** identify the cleanest current law that couples the missing tensor
support observable `Theta_R` into the exact slice generator `Lambda_R` /
bounded transfer law `T_R = exp(-Lambda_R)` on `PL S^3 x R`

## Verdict

The cleanest current answer is **bounded, not exact**.

The route-2 stack already gives:

- exact `S^3` spatial closure
- exact anomaly-forced time with a single clock, `d_t = 1`
- exact route-2 background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer operator `T_R = exp(-Lambda_R)`

The missing object is still the exact tensor-valued support observable on
`A1 x {E_x, T1x}`. On the exact support-side stack, that exact tensor carrier
does not exist.

So the best current law is a **bounded staging law**:

> `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

with the remaining `A1` dependence organized by the exact support scalar

> `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

That bounded law can feed the route-2 slice bridge only as a source-side
staging observable. It does **not** upgrade `Lambda_R` into an exact
Einstein/Regge dynamics theorem.

## Exact route-2 ingredients already in hand

### Kinematics

The retained kinematic background is exact:

- `PL S^3 x R`

from:

- [`S3_GENERAL_R_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
- [`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)

### Slice generator

The exact microscopic shell action supplies the exact slice generator:

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

from:

- [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md)

The induced transfer operator is the bounded one-step law:

- `T_R = exp(-Lambda_R)`

## Bounded `Theta_R` staging law

The current best route-2 tensor staging object is the bright-channel pair:

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block:

- `A1 x {E_x, T1x}`

The exact support-side scalar that survives shell-blindness is:

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

with exact canonical family law:

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

The current bounded prototype is affine in that exact scalar:

- `gamma_E(delta) = a_E + b_E delta`
- `gamma_T(delta) = a_T + b_T delta`

This is the cleanest current coupling candidate from the tensor support side
into the route-2 slice bridge.

## Why the coupling is only bounded

The retained exact support-side machinery is still scalar/rank-one on the
current `A1` block.

The exact support Hessian has no mixed `A1`-bright block, the support scalar
is blind to `E_x` and `T1x`, and the support-to-active operator is rank one
and charge-only. Therefore the current exact support stack cannot generate a
nonzero exact tensor observable on `A1 x {E_x, T1x}`.

That means the route-2 tensor observable can only enter the slice law as a
bounded source-side staging object for now.

## What the bounded coupling law is

The cleanest current route-2 coupling statement is:

1. the exact scalar slice generator remains `Lambda_R`
2. the bounded transfer law remains `T_R = exp(-Lambda_R)`
3. the missing tensor support observable is staged by
   `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`
4. `Theta_R^(0)` is organized by the exact support scalar `delta_A1`
5. the exact route-2 dynamics bridge is still missing

So the current law is a **source-augmented bounded bridge candidate**, not an
exact time-coupling theorem.

## Sharp blocker

The exact blocker is still the same one:

> there is no exact tensor-valued support observable on `A1 x {E_x, T1x}`
> in the current retained support-side machinery.

Without that exact tensor carrier, `Theta_R` cannot be coupled to `Lambda_R`
as a theorem-grade GR dynamics law.

## Practical conclusion

Route 2 now has the cleanest current answer available:

- exact background: `PL S^3 x R`
- exact slice generator: `Lambda_R`
- bounded transfer operator: `T_R = exp(-Lambda_R)`
- bounded tensor staging observable: `Theta_R^(0)(q)`

That is the right tool-chain for future atlas work, but it is not yet an exact
`Theta_R -> Lambda_R` closure theorem.
