# Planck-Scale Boundary Unit-Bearing Action/Pressure Lane

**Date:** 2026-04-23  
**Status:** science-only action/pressure reduction theorem plus sharp obstruction  
**Audit runner:** `scripts/frontier_planck_boundary_unit_bearing_action_pressure_lane.py`

## Question

After the time-lock theorem, exact Schur boundary action, canonical boundary
operator theorem, and quarter-normalization obstruction, what is the
**strongest action-native statement** one can make about the remaining Planck
boundary coefficient?

More concretely:

- does the exact Einstein/Regge-style boundary action on the time-locked
  carrier still allow the full affine gauge
  `G -> lambda G + mu I`;
- or does the microscopic action already kill some of that freedom;
- and if exact quarter does not yet follow, what is the exact remaining
  physical theorem we still need?

## Bottom line

The strongest honest result is stronger than the earlier affine-gauge note.

Once the exact same-surface Schur boundary action and exact one-clock grammar
are imposed, the multiplicative `lambda` freedom is no longer admissible.

What survives is only a **unit-bearing additive vacuum-action density**
`nu`.

Equivalently:

1. exact Schur reduction fixes the boundary Hessian/operator `L_Sigma`
   itself;
2. exact one-clock transfer fixes the coefficient with which `L_Sigma`
   enters the generator;
3. any same-surface action preserving the exact Euler-Lagrange law and exact
   Hessian can differ from the canonical action only by an additive
   worldtube-vacuum term;
4. on the reduced unit carrier this is one real density `nu`, giving

   `G_nu = nu I - L_Sigma`,

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

5. exact quarter is therefore not an affine tuning problem anymore. It is
   equivalent to one single missing theorem:

   `nu = lambda_min(L_Sigma) + 1/4`;

6. on the exact rational witness
   `L_Sigma = [[4/3,1/3],[1/3,4/3]]`,
   `lambda_min(L_Sigma) = 1`,
   so exact quarter means

   `nu = 5/4`;

7. if one keeps the canonical empty-vacuum normalization
   `I(0 ; 0) = 0`,
   then `nu = 0`, hence the boundary pressure is forced to

   `p_* = -lambda_min(L_Sigma)`,

   which is `-1` on the witness and therefore sharply incompatible with
   exact quarter.

So the sharp scientific update is:

> the remaining boundary problem is no longer a generic normalization gauge;
> it is the missing theorem for a nonzero unit-bearing boundary vacuum-action
> density on the time-locked Schur carrier.

That is the cleanest action-native reduction I can justify on current inputs.

## Inputs

This lane uses only already-earned exact ingredients on the branch:

- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
- [S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md](./S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md)

What is exact there already:

- exact microscopic Schur boundary action
  `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`;
- exact one-clock transfer backbone
  `T_R = exp(-Lambda_R)`;
- exact time-lock
  `a_s = c a_t`;
- exact bulk-to-boundary Schur completion on the time-locked carrier;
- exact canonical boundary operator
  `L_Sigma`;
- and the earlier normalization note, which showed quarter is not fixed by the
  broad affine class.

This note asks what remains once one insists on the **exact action** rather
than on the broad affine generator class.

## Step 1: exact Schur action kills the multiplicative ambiguity

On the time-locked boundary carrier, the exact reduced microscopic action has
the canonical quadratic form

`I_can(b ; j) = 1/2 b^T L_Sigma b - j^T b`.

Now consider any same-surface action on the same boundary variables `b` and
sources `j` that claims to preserve:

1. the exact Schur Hessian,
2. the exact Euler-Lagrange equation,
3. the exact one-clock transfer grammar,
4. and no new source-dependent imported data.

If its quadratic part were rescaled,

`I_lambda(b ; j) = lambda/2 b^T L_Sigma b - j^T b`,

then its Hessian would be `lambda L_Sigma`, not `L_Sigma`, and its stationary
equation would become

`lambda L_Sigma b - j = 0`,

so the exact Schur response law would be changed to

`b = (1/lambda) L_Sigma^(-1) j`.

Therefore multiplicative rescaling is not a harmless normalization on the
exact action lane. It changes the microscopic operator and the exact response.

This is the key upgrade over the earlier affine-gauge note:

> once the exact boundary action itself is retained, `lambda != 1` is no
> longer same-surface.

## Step 2: only an additive vacuum-action density survives

Fix the exact Hessian `L_Sigma` and exact source coupling `-j^T b`.
Then any same-surface action preserving those data can differ from
`I_can` only by a term independent of `b`.

On a boundary worldtube `W_Sigma(tau) = Sigma x [0,tau]`, one-clock additivity
forces that term to be extensive in `tau`:

`I_tau(b ; j) = tau (1/2 b^T L_Sigma b - j^T b) - C(tau)`,

with

`C(tau_1 + tau_2) = C(tau_1) + C(tau_2)`.

Hence

`C(tau) = nu tau`

on the reduced unit carrier, or more generally

`C(tau) = sigma_Sigma |W_Sigma(tau)|`

before reduction to unit boundary measure. So the surviving unit-bearing
extension is uniquely an additive vacuum-action density.

The exact admissible action family is therefore

`I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`.

That is the strongest same-surface action theorem I can justify from the
existing action/Regge inputs.

## Theorem 1: exact action-native reduction of the boundary normalization problem

Assume:

1. exact time-lock `a_s = c a_t`;
2. exact microscopic Schur boundary action on the retained carrier;
3. exact one-clock transfer grammar generated by that boundary action;
4. no new source-dependent import and no change of boundary variables.

Then every same-surface boundary action preserving the exact Hessian and exact
Euler-Lagrange law has the unique form

`I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`.

Equivalently:

> the broad affine family collapses, on the exact action lane, to a
> one-parameter additive vacuum-density family.

## Step 3: induced pressure law

Because the one-clock generator is read from the exact action backbone,
the corresponding semigroup family is

`T_nu(tau) = exp(tau (nu I - L_Sigma))`.

So the top pressure is

`p_*(nu) = sup spec(nu I - L_Sigma)`
`        = nu - lambda_min(L_Sigma)`.

This is the exact unit-bearing pressure law on the retained action lane.

The remaining boundary Planck problem is therefore no longer:

`choose a good normalization on G`.

It is now:

> derive the physical boundary vacuum-action density `nu`.

## Theorem 2: exact quarter is equivalent to one vacuum-density law

Exact quarter pressure

`p_* = 1/4`

holds on the retained action lane if and only if

`nu = lambda_min(L_Sigma) + 1/4`.

So exact Planck closure on the boundary route is equivalent to one new theorem:

> the time-locked Schur boundary worldtube carries the exact vacuum-action
> density `nu = lambda_min(L_Sigma) + 1/4`.

On the exact witness

`L_Sigma = [[4/3,1/3],[1/3,4/3]]`,

we have

`lambda_min(L_Sigma) = 1`,

so exact quarter becomes

`nu = 5/4`.

This is sharper than the previous `mu = lambda + 1/4` affine line. On the
exact action lane there is only one surviving number.

## Step 4: canonical empty-vacuum normalization gives a sharp obstruction

The exact Schur boundary action has the canonical unsourced vacuum value

`I_can(0 ; 0) = 0`.

If that empty-vacuum normalization is retained on the Planck boundary lane,
then the additive vacuum density must vanish:

`nu = 0`.

But then the pressure law becomes

`p_*(0) = -lambda_min(L_Sigma)`.

So on the exact witness:

`p_*(0) = -1`.

That is not merely “not quarter.” It lands on the wrong sign branch entirely.

So the sharpest current obstruction is:

> exact quarter on the retained action lane requires a nonzero boundary
> vacuum-action density. If one insists on canonical zero-vacuum
> normalization, quarter is impossible.

In short: **canonical zero-vacuum normalization** and exact quarter are
incompatible on the current witness.

## Minimal exact witness

Use the same rational Schur witness already forced elsewhere:

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

Its eigenvalues are exactly

`1`, `5/3`.

Therefore:

- canonical action lane (`nu = 0`) gives
  `p_* = -1`;
- exact quarter requires
  `nu = 5/4`;
- and the Planck boundary problem is fully reduced to one missing density.

## What this closes

This note closes the strongest action-native reduction currently available:

> on the exact time-locked Schur carrier, the remaining boundary Planck
> coefficient is not an arbitrary affine normalization. It is one
> vacuum-action density.

That is a real scientific tightening.

## What this does not close

This note still does **not** derive the needed density.

It does **not** yet prove:

1. an exact microscopic theorem forcing `nu = 5/4` on the witness;
2. an exact gravitational boundary vacuum term or GHY/BH-style same-surface
   coefficient theorem inside the current accepted stack;
3. exact conventional Planck closure.

## Bottom line

The cleanest action-native statement now is:

> the exact Schur boundary action already fixes the operator scale, so the
> full affine boundary normalization gauge is too broad on the retained
> action lane.
>
> What actually remains is one unit-bearing additive vacuum-action density
> `nu`.
>
> Exact quarter is equivalent to deriving that density, and canonical
> zero-vacuum normalization rules quarter out sharply.
