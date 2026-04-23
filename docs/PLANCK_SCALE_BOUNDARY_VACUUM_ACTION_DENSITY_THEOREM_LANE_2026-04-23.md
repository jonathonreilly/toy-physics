# Planck-Scale Boundary Vacuum-Action Density Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only reduction theorem / obstruction on the remaining unit-bearing boundary coefficient  
**Audit runner:** `scripts/frontier_planck_boundary_vacuum_action_density_theorem_lane.py`

## Question

The boundary route is now narrowed to one exact unit-bearing target:

`nu = lambda_min(L_Sigma) + 1/4`

on the retained action-pressure lane, with witness value `nu = 5/4`.

The exact remaining question is therefore:

> can the same-surface gravity/action principles already on the branch derive
> the boundary vacuum-action density `nu`;
> and if not, what do they force instead?

## Bottom line

The strongest honest result is a **vacuum-normalization classification theorem
plus sharp no-go**, not a Planck close.

The exact time-locked Schur boundary action does **not** leave an arbitrary
vacuum coefficient. It leaves exactly two canonical same-surface vacuum
normalizations:

1. **empty-vacuum action normalization**

   `I_nu(tau ; 0, 0) = 0`

   which forces

   `nu = 0`;

2. **Gaussian vacuum-pressure matching**

   where the additive vacuum-action density is required to equal the exact
   same-surface Schur vacuum free-energy density, forcing

   `nu = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

So the current same-surface gravity/action stack narrows `nu` to the canonical
set

`nu in {0, p_vac(L_Sigma)}`.

Exact quarter on the action-pressure lane would instead require

`nu_quarter(L_Sigma) = lambda_min(L_Sigma) + 1/4`.

On the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

these three values are

- `nu_0 = 0`,
- `nu_gauss = (1/4) log(5/3) ~= 0.127706`,
- `nu_quarter = 5/4`.

Therefore:

- canonical zero-vacuum normalization is sharply incompatible with quarter;
- canonical Gaussian vacuum-pressure matching is also sharply incompatible
  with quarter;
- the current same-surface gravity/action principles do **not** derive the
  Planck boundary coefficient.

The remaining microscopic datum is now explicit:

> a new vacuum reference law beyond the two canonical same-surface choices,
> or a new theorem identifying the physical pressure shift with some other
> exact carrier quantity such as the `C^16` axis-sector mass.

That is the cleanest boundary-coefficient reduction I can justify on current
inputs.

## Inputs

This lane uses only already-earned same-surface ingredients:

- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)

What those lanes already fixed exactly:

1. the surviving action family

   `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

2. the induced pressure law

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

3. quarter pressure is equivalent to

   `nu_quarter(L_Sigma) = lambda_min(L_Sigma) + 1/4`;

4. the exact same-surface Gaussian vacuum density

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

5. the exact `C^16` bridge reduction

   `p_* = m_axis = 1/4`

   as a possible new carrier-level law, not an earned action theorem.

This note asks what the current same-surface action principles really force
about `nu` itself.

## Step 1: the surviving action family

The earlier action-pressure lane already showed that once the exact Schur
Hessian, exact Euler-Lagrange law, and exact one-clock backbone are retained,
the old affine gauge collapses to

`I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`.

So deriving `nu` is now the entire remaining action-side problem.

## Step 2: two canonical same-surface vacuum normalizations

There are only two canonical vacuum normalizations still present on the same
surface.

### 2A. Empty-vacuum action normalization

The bare microscopic action is normalized at the empty unsourced boundary
configuration:

`I_nu(tau ; 0, 0) = -tau nu`.

So if one insists that the exact empty-vacuum action vanish, one gets

`nu = 0`.

This is the strongest form of the earlier zero-vacuum obstruction.

### 2B. Gaussian vacuum-pressure matching

The non-affine boundary note already proved that the exact source-free Schur
carrier has normalized vacuum free-energy density

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

If the additive vacuum-action density is required to match the exact
same-surface Gaussian vacuum density, then

`nu = p_vac(L_Sigma)`.

This is the only canonical nonzero same-surface value currently available from
the retained Schur boundary action itself.

## Theorem 1: vacuum-normalization classification on the current action lane

Assume:

1. exact time-locked Schur boundary carrier;
2. exact surviving action family
   `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;
3. no imported boundary carrier beyond the current same-surface action stack.

Then the current same-surface gravity/action principles supply exactly two
canonical values for `nu`:

1. `nu_0(L_Sigma) = 0`
   from empty-vacuum action normalization;
2. `nu_gauss(L_Sigma) = (1/(2n)) log det(L_Sigma)`
   from Gaussian vacuum-pressure matching.

No current theorem on the branch forces

`nu = lambda_min(L_Sigma) + 1/4`.

So the action lane is reduced to a canonical dichotomy, not closed.

## Theorem 2: quarter is obstructed on both canonical normalizations

Let

`nu_quarter(L_Sigma) := lambda_min(L_Sigma) + 1/4`.

For every positive boundary carrier `L_Sigma > 0`:

1. `nu_0(L_Sigma) != nu_quarter(L_Sigma)`,
   because `lambda_min(L_Sigma) > 0`, so `nu_quarter(L_Sigma) > 1/4`;
2. `nu_gauss(L_Sigma) = nu_quarter(L_Sigma)`
   only if the carrier satisfies the special spectral constraint

   `det(L_Sigma) = exp(2n (lambda_min(L_Sigma) + 1/4))`.

That constraint is not supplied by the current Schur/action notes.

So exact quarter on the boundary action lane is not a consequence of the
current same-surface vacuum normalizations.

## Minimal exact witness

Take the exact rational witness already fixed by the boundary lanes:

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

Then

`spec(L_Sigma) = {1, 5/3}`,

`lambda_min(L_Sigma) = 1`,

`det(L_Sigma) = 5/3`,

and `n = 2`.

Therefore:

- empty-vacuum action normalization gives

  `nu_0 = 0`;

- Gaussian vacuum-pressure matching gives

  `nu_gauss = (1/4) log(5/3) ~= 0.127706`;

- exact quarter would require

  `nu_quarter = 1 + 1/4 = 5/4`.

Neither canonical same-surface value matches the required quarter value.

So on the witness, the current gravity/action principles rule quarter out
rather than derive it.

## Corollary: the remaining microscopic datum is explicit

Because the branch already has:

- the exact carrier `L_Sigma`,
- the exact pressure law `p_*(nu) = nu - lambda_min(L_Sigma)`,
- the exact Gaussian vacuum density `p_vac(L_Sigma)`,
- and the exact `C^16` bridge candidate `p_* = m_axis = 1/4`,

the remaining action-side microscopic datum is now completely explicit.

One still needs one new theorem of one of the following forms:

1. a **new vacuum reference law** selecting
   `nu = lambda_min(L_Sigma) + 1/4`;
2. a **bridge law** identifying the physical pressure shift with the `C^16`
   axis-sector mass, equivalently
   `nu = lambda_min(L_Sigma) + m_axis`;
3. or a no-go theorem proving that one of the canonical values
   `nu in {0, p_vac(L_Sigma)}` is mandatory, which would kill quarter on the
   boundary route completely.

That is the sharpest current reduction.

## What is actually proved

This lane proves:

1. the current same-surface action lane supplies a canonical dichotomy
   `nu in {0, p_vac(L_Sigma)}`;
2. quarter requires the different value
   `nu_quarter(L_Sigma) = lambda_min(L_Sigma) + 1/4`;
3. on the exact witness, both canonical values miss the quarter target
   sharply;
4. so the current same-surface gravity/action principles do not derive the
   Planck boundary vacuum-action density.

## Bottom line

The boundary vacuum-action density problem is now reduced as far as the
current action stack honestly goes.

The branch does **not** derive `nu = 5/4`.

It does derive that the current same-surface gravity/action principles only
support:

- `nu = 0`, or
- `nu = (1/(2n)) log det(L_Sigma)`,

and therefore a Planck close would need one genuinely new microscopic vacuum
law beyond the present Schur/action machinery.
