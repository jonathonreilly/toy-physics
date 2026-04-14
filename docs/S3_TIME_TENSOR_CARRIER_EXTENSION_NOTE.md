# Route 2 Tensor Carrier Extension: Exact Blocker on the Current Schur/Static Stack

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** Route 2 / worker 3  
**Purpose:** test whether the exact Schur boundary action plus static-constraint
lift can be minimally extended into a genuine tensor carrier rather than only a
scalar/kinetic semigroup

## Verdict

The answer on the current retained stack is **no**.

Route 2 already gives:

- exact `S^3` spatial closure
- exact anomaly-forced time with a single clock, `d_t = 1`
- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer operator `T_R = exp(-Lambda_R)`
- exact shell-to-`3+1` static-constraint lift
- exact microscopic Schur boundary action on the restricted bridge class

But those exact ingredients do **not** tensorize into a genuine tensor carrier
on the current support-side machinery.

## Exact blocker

The retained exact support-side stack is scalar/rank-one on the current `A1`
block:

1. the exact support Hessian has no mixed `A1`-bright block,
2. the exact support-to-active operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`.

So the current exact Schur/static stack cannot produce a nonzero exact tensor
carrier on

- `A1 x {E_x, T1x}`

and therefore cannot upgrade `Lambda_R` into a theorem-grade tensor dynamics
bridge.

## Exact route-2 ingredients already in hand

### Kinematics

The retained route-2 kinematic background is exact:

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

### Static lift

The exact shell-to-`3+1` static conformal lift on the current bridge surface
is already exact on the restricted class:

- [`OH_STATIC_CONSTRAINT_LIFT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_STATIC_CONSTRAINT_LIFT_NOTE.md)

So the missing piece is not time, not the shell bridge, and not the static
lift. The missing piece is the tensor carrier itself.

## Bounded staging object

The best bounded staging object remains the two-channel bright tensor prototype

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

- `A1 x {E_x, T1x}`

with exact support-side scalar

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

and exact canonical family law

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

That staging object is useful for bounded matching, but it is not an exact
tensor carrier.

## Practical conclusion

Route 2 still has a clean bounded kinetic lift:

- exact background: `PL S^3 x R`
- exact slice generator: `Lambda_R`
- bounded transfer operator: `T_R = exp(-Lambda_R)`

But the exact tensor-carrier extension does not exist on the current support
stack. The current Schur/static machinery is scalar/rank-one and cannot by
itself tensorize into a genuine `Theta_R -> Lambda_R` closure theorem.

## Next exact target

The only honest next tensor primitive is a new microscopic tensor operator
beyond the current support machinery.
