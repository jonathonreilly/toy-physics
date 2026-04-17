# Route 2 Primitive Chain: Axiom-First Build Program

**Date:** 2026-04-14  
**Purpose:** identify the missing Route-2 primitives cleanly, rank them by
dependency, and derive the smallest missing primitive from the current exact
and bounded stack so they can become future atlas tools

## Verdict

Route 2 is no longer a hunt for a hidden GR theorem.

The current retained stack already gives:

- exact `S^3` spatial compactification
- exact anomaly-forced single-clock time
- exact route-2 background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer / kinetic semigroup `T_R = exp(-Lambda_R)`

What it does **not** yet give is the tensor-valued dynamics carrier that
upgrades that semigroup into Einstein/Regge dynamics.

The smallest missing primitive is therefore **not** another scalar transfer
theorem. It is:

> an exact tensor-valued support observable on the microscopic block
> `A1 x {E_x, T1x}`.

That is the first new primitive that must be built if Route 2 is going to
become a theorem-grade gravity path.

## Existing exact and bounded inputs

The current reduction uses only the strongest already-audited route-2 and
tensor-frontier facts:

1. `S^3` is exact on the accepted compactification family.
2. anomaly-forced time is exact with `d_t = 1`.
3. the natural route-2 background is `PL S^3 x R`.
4. the exact Schur boundary action gives the slice generator `Lambda_R`.
5. the current route-2 dynamics law is bounded:
   - `T_R = exp(-Lambda_R)`
6. the observable principle remains scalar-only on this route.
7. the tensor boundary drive is bright only on the aligned support channels:
   - `E_x`
   - `T1x`
8. the remaining `A1` dependence is already organized by one exact
   support-side scalar:
   - `delta_A1 = phi_support(center)/Q - phi_support(arm_mean)/Q`
   - `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

Those facts are enough to derive the primitive chain below.

## Theorem: minimal Route-2 primitive reduction

On the current route-2 stack and current restricted gravity class:

1. the route-2 kinematic scaffold is exact:
   - `PL S^3 x R`
2. the slice generator `Lambda_R` and one-step transfer operator
   `T_R = exp(-Lambda_R)` are exact/bounded but scalar on the current route
3. the exact observable principle remains scalar-valued on this route
4. the non-scalar gravity response is already localized to a two-channel
   support sector:
   - `E_x`
   - `T1x`
5. the remaining scalar `A1` dependence of that non-scalar response is already
   reduced to the exact support-side scalar `delta_A1`

Therefore any exact Route-2 completion of the current strong-field package must
introduce at least one new tensor-valued primitive

- `Theta_R(delta_A1 ; E_x, T1x)`

on the microscopic support block `A1 x {E_x, T1x}`.

Moreover, once `Theta_R` is exact, the remaining `A1` dependence is already
organized by two endpoint evaluations:

- `Theta_R(e0 ; E_x, T1x)`
- `Theta_R(s / sqrt(6) ; E_x, T1x)`

and the current affine `delta_A1` law becomes the derived interpolation
surface rather than a free function.

So the first missing primitive is not:

- another transfer matrix
- another scalar Hessian
- another background-selection theorem

It is exactly:

> a tensor-valued support observable on `A1 x {E_x, T1x}`.

## Primitive chain

### Primitive P0: route-2 kinematic scaffold

**Object**
- exact background `PL S^3 x R`

**Status**
- already derived

**Current authorities**
- [S3_GENERAL_R_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
- [ANOMALY_FORCES_TIME_THEOREM.md](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)

**Atlas role**
- existing retained topology/spacetime tools

### Primitive P1: tensor-valued support observable

**Object**
- `Theta_R(delta_A1 ; E_x, T1x)` on the microscopic support block

**Status**
- not yet derived
- now identified as the smallest missing primitive

**What it must do**
- be exact on the current restricted class
- vanish when the bright tensor channels vanish
- reduce the current tensor frontier to one exact numerator object

**Future atlas role**
- route-2 tensor observable / tensor source tool

**Current bounded staging object**
- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`
- see [S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md](./S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md)

### Primitive P2: endpoint coefficient theorem

**Object**
- exact endpoint coefficients of `Theta_R` at
  - `e0`
  - `s / sqrt(6)`

**Status**
- not yet derived

**What it must do**
- fix the exact bright-channel coefficients at the two `A1` endpoints
- recover the current affine `delta_A1` law as a derived consequence

**Future atlas role**
- route-2 endpoint/normalization tool

### Primitive P3: support-to-slice time-coupling law

**Object**
- exact coupling from `Theta_R` into the route-2 slice dynamics

**Status**
- not yet derived

**What it must do**
- connect the new tensor support observable to `Lambda_R`
- upgrade `T_R = exp(-Lambda_R)` from a bounded semigroup into a
  tensor-carrying slice law

**Future atlas role**
- route-2 time-coupling / kinetic tool

### Primitive P4: spacetime dynamics closure

**Object**
- exact `PL S^3 x R` action / observable / uniqueness theorem for GR dynamics

**Status**
- not yet derived

**What it must do**
- close Einstein/Regge dynamics on the route-2 surface
- make the metric/curvature coupling theorem-grade rather than bounded

**Future atlas role**
- route-2 gravity closure tool

## Dependency ranking

The clean dependency order is:

1. `P1`: exact tensor-valued support observable
2. `P2`: exact endpoint coefficient theorem
3. `P3`: exact support-to-slice time-coupling law
4. `P4`: exact spacetime dynamics theorem

This order is forced by the current evidence:

- `P3` cannot be derived before `P1`, because the route-2 stack currently has
  no tensor-valued carrier to couple in time
- `P4` cannot be derived before `P3`, because the current semigroup is still
  scalar/static at the theorem level

## What has now been derived cleanly

The current build note derives one exact reduction result now:

> the smallest missing Route-2 primitive is `P1`, the tensor-valued support
> observable on `A1 x {E_x, T1x}`.

That is already a useful atlas-facing theorem shape because it prevents us
from wasting more time on:

- scalar-only route-2 observable work
- additional transfer-matrix rewrites
- further kinematic uniqueness refinements

## Immediate next derivation target

The next theorem should be:

> derive `Theta_R` exactly on the microscopic support block and show that its
> endpoint values at `e0` and `s / sqrt(6)` reproduce the current bright
> tensor law.

That is the first genuinely new route-2 tool worth trying to promote into the
atlas.

## Bottom line

Route 2 is now mature enough to treat as a tool-building program.

The primitive chain is:

- exact background `PL S^3 x R`
- exact tensor-valued support observable `Theta_R`
- exact endpoint coefficient theorem
- exact support-to-slice time-coupling law
- exact spacetime dynamics closure

And the smallest missing primitive, now derived cleanly from the current
stack, is the tensor-valued support observable `Theta_R` on
`A1 x {E_x, T1x}`.
