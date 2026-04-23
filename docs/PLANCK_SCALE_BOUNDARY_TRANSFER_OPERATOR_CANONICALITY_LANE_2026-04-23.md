# Planck-Scale Boundary Transfer-Operator Canonicality Lane

**Date:** 2026-04-23  
**Status:** science-only theorem/obstruction on the time-locked boundary route  
**Audit runner:** `scripts/frontier_planck_boundary_transfer_operator_canonicality_lane.py`

## Question

On the surviving Planck boundary route, can the admitted exact `3+1` gravity
carrier itself force a **canonical positive boundary transfer/operator**
without tuned parameters?

Equivalently:

- is the collective boundary operator really determined by the admitted
  gravity carrier, or are we still choosing it;
- if the operator is forced, does the same-surface one-clock grammar also
  force its transfer law;
- and if that happens, does the Planck target
  `rho(T(1)) = e^(1/4)` follow, or fail sharply?

## Bottom line

The strongest honest result is:

1. the admitted exact `3+1` gravity carrier **forces a canonical boundary
   operator**;
2. that operator is the exact Schur / Dirichlet reduction of the positive
   bulk quadratic form on the time-locked boundary worldtube;
3. the admitted one-clock transfer grammar then forces the **no-parameter
   canonical transfer law**

   `T_can(tau) = exp(-tau L_Sigma)`;

4. because `L_Sigma` is positive semidefinite on the reduced carrier, the
   canonical transfer is always spectrally contractive:

   `rho(T_can(1)) = exp(-lambda_min(L_Sigma)) <= 1`;

5. therefore the canonical no-parameter boundary transfer law cannot realize
   the Planck boundary target

   `rho(T(1)) = e^(1/4) > 1`;

6. any exact quarter-pressure close on this route still needs one genuinely
   new theorem beyond canonical reduction:
   either a different carrier or an additive pressure normalization law.

So this lane does force something real:

> the canonical same-surface boundary operator is derived,
> but the canonical same-surface boundary **growth** law is obstructed.

That is stronger than the earlier transfer-operator note, because it removes
the ambiguity about what the untuned operator actually is.

## Inputs

This lane uses only exact ingredients already admitted elsewhere on the
branch:

- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](./UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
- [UNIVERSAL_GR_POSITIVE_BACKGROUND_EXTENSION_NOTE.md](./UNIVERSAL_GR_POSITIVE_BACKGROUND_EXTENSION_NOTE.md)
- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
- [S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md](./S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md)

What is already exact there:

- one derived clock on `PL S^3 x R`;
- exact time-lock `a_s = c a_t`;
- exact positive-background gravity carrier
  `K_GR(D) = H_D \otimes Lambda_R`;
- exact microscopic boundary action from Schur reduction;
- exact one-clock transfer grammar with
  `T_R = exp(-Lambda_R)`.

Those ingredients are enough to settle the canonicality question.

## Step 1: the boundary operator is forced by exact reduction

Split the exact positive quadratic carrier into boundary/worldtube variables
`x` and interior/bulk variables `y`:

`I(x,y) = 1/2 [x y]^T [[A, B], [B^T, C]] [x y]`,

with `C > 0`.

There are then two exact same-surface ways to eliminate the bulk:

1. stationary elimination:
   `partial_y I = 0`, so `y_* = -C^(-1) B^T x`;
2. Gaussian marginalization:
   integrate `exp(-I(x,y))` over `y`.

Both give the same reduced boundary quadratic form:

`I_Sigma(x) = 1/2 x^T L_Sigma x`

with exact coefficient

`L_Sigma = A - B C^(-1) B^T`.

So the reduced boundary operator is not a chosen packaging. It is forced by
the exact same microscopic quadratic carrier.

This is the boundary analogue of the earlier exact Schur boundary-action
results elsewhere on the branch.

## Step 2: the one-clock transfer law is also forced

The admitted one-clock route already fixes the sign and generator grammar on
the exact slice carrier:

`T_R(tau) = exp(-tau Lambda_R)`.

That matters here. Once the boundary operator has been forced to `L_Sigma`,
the no-parameter same-surface transfer law is not an arbitrary functional
`exp(-tau psi(L_Sigma))`. The exact route already tells us what the one-clock
law is:

- the generator enters linearly in the quadratic action;
- one clock means semigroup composition;
- the admitted sign is dissipative/contractive, not amplifying.

Therefore the canonical same-surface boundary transfer law is

`T_can(tau) = exp(-tau L_Sigma)`.

Replacing `L_Sigma` by `psi(L_Sigma)` would not be the same reduced carrier.
It would be a new model on top of the reduced carrier.

## Step 3: the canonical transfer is contractive

If `L_Sigma` is positive semidefinite, its eigenvalues satisfy

`lambda_i(L_Sigma) >= 0`.

Therefore the eigenvalues of `T_can(1)` are

`exp(-lambda_i(L_Sigma))`,

so

`rho(T_can(1)) = exp(-lambda_min(L_Sigma)) <= 1`.

If the reduced carrier is positive definite, then `lambda_min(L_Sigma) > 0`
and the inequality is strict:

`rho(T_can(1)) < 1`.

So the canonical same-surface transfer operator lies on the **decaying**
branch, not the growth/Perron branch needed for exact quarter pressure.

## Minimal exact witness

Take the rational witness already used in the earlier transfer note:

`A = [[2, 0], [0, 2]]`

`B = [[1, 0], [0, 1]]`

`C = [[2, 1], [1, 2]]`.

Then

`L_Sigma = A - B C^(-1) B^T`
`        = [[4/3, 1/3], [1/3, 4/3]]`.

Its eigenvalues are exactly

`1`, `5/3`.

Therefore the canonical one-step transfer has eigenvalues

`e^(-1)`, `e^(-5/3)`,

and exact spectral radius

`rho(T_can(1)) = e^(-1) < 1`.

This witness shows the issue sharply:

- the operator is exact;
- the transfer law is canonical;
- the sign is fixed;
- and the resulting pressure is negative, not `+1/4`.

## Theorem-level statement

**Theorem (Canonical boundary Schur-heat law and quarter-pressure obstruction).**
Assume:

1. the exact derived single-clock `3+1` route on `PL S^3 x R`;
2. exact time-lock `a_s = c a_t`;
3. the exact positive-background gravity carrier
   `K_GR(D) = H_D \otimes Lambda_R`;
4. exact same-surface bulk elimination on a boundary/interior split;
5. no additional boundary normalization, source shift, or nonlinear functional
   reweighting beyond the admitted one-clock transfer grammar.

Then:

1. the boundary quadratic operator is uniquely the exact Schur reduction
   `L_Sigma = A - B C^(-1) B^T`;
2. the canonical same-surface one-clock boundary transfer law is uniquely
   `T_can(tau) = exp(-tau L_Sigma)`;
3. `T_can(tau)` is a positive self-adjoint contraction in the admitted
   operator sense;
4. `rho(T_can(1)) = exp(-lambda_min(L_Sigma)) <= 1`;
5. therefore the canonical no-parameter boundary transfer law cannot realize
   exact quarter pressure
   `rho(T(1)) = e^(1/4)`.

Equivalently:

> the admitted `3+1` gravity carrier forces the canonical boundary operator,
> but the canonical same-surface transfer law lands on the wrong spectral
> branch for Planck.

## Corollary: exact quarter requires a new normalization theorem

To move the canonical transfer onto the quarter-pressure target one must pass
to a shifted family

`T_mu(tau) = exp(tau (mu I - L_Sigma))`.

Then

`rho(T_mu(1)) = exp(mu - lambda_min(L_Sigma))`.

Exact quarter requires

`mu = 1/4 + lambda_min(L_Sigma)`.

So on the witness above, where `lambda_min(L_Sigma) = 1`, exact quarter means

`mu = 5/4`.

That coefficient is not derived by canonical reduction. It is exactly one new
normalization datum.

This is the sharpest obstruction now available on the boundary-transfer route:

- the operator is no longer ambiguous;
- the remaining open bridge is one additive pressure theorem.

## What this closes

This note closes several previously loose possibilities:

- "maybe the canonical boundary operator itself is still a choice";
- "maybe once the Schur reduction is accepted, a positive growth transfer law
  comes for free";
- "maybe exact quarter is already hidden in the untuned boundary semigroup."

Those are no longer live.

## What remains open

Two possibilities remain:

1. a new same-surface theorem that fixes one additive pressure shift
   `mu` internally on the boundary worldtube;
2. a different same-surface boundary carrier whose canonical no-parameter
   transfer law is not contractive.

The current branch does not yet supply either.

## Honest status

This note does **not** derive exact conventional `a = l_P`.

It does something narrower but real:

> it derives the canonical boundary operator and shows that the canonical
> no-parameter transfer law is too contractive to close Planck.

So the remaining boundary problem is no longer "what operator should we use?"
It is:

> what exact same-surface theorem, if any, converts the canonical boundary
> Schur operator into a quarter-pressure law without importing the coefficient?
