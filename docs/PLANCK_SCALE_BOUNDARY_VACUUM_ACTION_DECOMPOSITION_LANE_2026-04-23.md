# Planck-Scale Boundary Vacuum-Action Decomposition Lane

**Date:** 2026-04-23  
**Status:** science-only decomposition reduction theorem plus sign obstruction  
**Audit runner:** `scripts/frontier_planck_boundary_vacuum_action_decomposition_lane.py`

## Question

Can the remaining Planck boundary coefficient be derived by a more physical
decomposition of the boundary vacuum-action density itself?

More concretely:

- the exact action lane already reduced the microscopic family to

  `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

- the exact pressure law is

  `p_*(nu) = nu - lambda_min(L_Sigma)`;

- the `C^16` lane isolates the exact coarse axis-sector mass

  `m_axis = 1/4`;

- exact Planck quarter would therefore follow if one could derive

  `nu = lambda_min(L_Sigma) + m_axis`.

The exact remaining question is:

> does the current same-surface stack derive a canonical decomposition of
> `nu` into a Schur spectral floor plus an exact positive residual, and if so
> does that residual land on `1/4` without importing the target?

## Bottom line

Not yet. But the decomposition route can now be stated much more sharply.

The strongest honest result is:

1. every same-surface boundary vacuum-action law on the retained action lane
   has a unique **floor-plus-residual decomposition**

   `nu = lambda_min(L_Sigma) + delta`;

2. under that decomposition the exact action pressure is simply

   `p_* = delta`;

3. therefore exact quarter is equivalent to one very specific residual law:

   `delta = 1/4`;

4. the currently earned same-surface residuals are:

   - `delta_0 = -lambda_min(L_Sigma)` from empty-vacuum normalization;
   - `delta_gauss = p_vac(L_Sigma) - lambda_min(L_Sigma)` from Gaussian
     vacuum matching;

5. on the canonical witness
   `L_Sigma = [[4/3,1/3],[1/3,4/3]]`,
   these become

   - `delta_0 = -1`,
   - `delta_gauss = (1/4) log(5/3) - 1 ~= -0.872294`,
   - `delta_quarter = 1/4`;

6. so the current same-surface decomposition route does not merely miss
   quarter; it points to the **wrong sign**. The retained scalar/vacuum
   residuals are negative, whereas exact quarter needs a positive residual;

7. the only exact positive residual candidate currently isolated on the branch
   is the coarse `C^16` axis-sector mass

   `m_axis = 1/4`;

8. therefore, if the vacuum-action decomposition route is real, it must close
   by one new theorem of the form

   `delta = m_axis`,

   equivalently

   `nu = lambda_min(L_Sigma) + m_axis`.

So the route is reduced to one load-bearing positive-residual identification
law. It is not yet derived from the current exact stack.

## Inputs

This lane uses only already-earned branch-local ingredients:

- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)

What those notes already fix exactly:

1. the retained one-clock action family

   `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

2. the exact action-native pressure law

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

3. the canonical same-surface vacuum values

   `nu in {0, p_vac(L_Sigma)}`;

4. the exact Schur vacuum density

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

5. the exact `C^16` coarse residual candidate

   `m_axis = 1/4`;

6. the exact time-lock `a_s = c a_t`, which ensures the decomposition is being
   posed on the reduced one-clock boundary worldtube rather than on a hidden
   anisotropic two-scale surface.

This note asks what the decomposition route itself actually forces.

## Step 1: universal floor-plus-residual decomposition

On the retained action lane, define the residual

`delta := nu - lambda_min(L_Sigma)`.

Then every admissible boundary vacuum-action density decomposes uniquely as

`nu = lambda_min(L_Sigma) + delta`.

Substituting this into the exact pressure law gives

`p_*(nu) = nu - lambda_min(L_Sigma) = delta`.

So the action lane already proves a useful exact equivalence:

> deriving the physical boundary pressure is the same problem as deriving the
> residual part of the boundary vacuum-action density above the Schur spectral
> floor.

This is the cleanest decomposition statement on the current action route.

## Theorem 1: exact residual reformulation of the Planck boundary problem

Assume:

1. the exact time-locked one-clock boundary action family
   `I_nu(tau ; b, j)`;
2. the exact action-native pressure law
   `p_*(nu) = nu - lambda_min(L_Sigma)`.

Then every same-surface boundary vacuum-action density has the unique
decomposition

`nu = lambda_min(L_Sigma) + delta`,

and the corresponding physical action pressure is exactly

`p_* = delta`.

Therefore exact boundary quarter

`p_* = 1/4`

is equivalent to the single residual law

`delta = 1/4`.

This removes a layer of clutter: the open problem is not “which `nu`?” in the
abstract, but “which residual above the Schur floor?”

## Step 2: the currently earned residuals

The present same-surface stack gives exactly two canonical action-side values
for `nu`.

### 2A. Empty-vacuum residual

Empty-vacuum normalization gives

`nu_0 = 0`.

So the associated residual is

`delta_0 = nu_0 - lambda_min(L_Sigma) = -lambda_min(L_Sigma)`.

On every positive carrier this is strictly negative.

### 2B. Gaussian residual

Gaussian vacuum matching gives

`nu_gauss = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

So the associated residual is

`delta_gauss = p_vac(L_Sigma) - lambda_min(L_Sigma)`.

This is the strongest current nonzero same-surface residual derived from the
exact Schur action itself.

## Theorem 2: the current same-surface decomposition route has the wrong sign

Take the positive symmetric Schur family

`L(r) = [[1 + r, r], [r, 1 + r]]`,

with `0 < r < 1`.

Then:

1. `lambda_min(L(r)) = 1`;
2. `det(L(r)) = 1 + 2r`;
3. the Gaussian vacuum density is

   `p_vac(L(r)) = (1/4) log(1 + 2r)`;

4. because `1 < 1 + 2r < 3`, one has

   `0 < p_vac(L(r)) < (1/4) log 3 < 1`;

5. therefore the Gaussian residual satisfies

   `delta_gauss(L(r)) = p_vac(L(r)) - 1 < (1/4) log 3 - 1 < 0`;

6. while empty-vacuum normalization gives

   `delta_0(L(r)) = -1 < 0`.

So on the entire retained positive witness family, the currently earned
same-surface residuals are negative, whereas exact Planck quarter requires the
positive residual

`delta_quarter = 1/4`.

This is stronger than “quarter is not yet derived.” It shows:

> the current scalar/vacuum decomposition route points away from quarter by
> sign, not just by value.

## Minimal exact witness

On the canonical boundary witness

`L_Sigma = [[4/3,1/3],[1/3,4/3]]`,

one has:

- `spec(L_Sigma) = {1, 5/3}`;
- `lambda_min(L_Sigma) = 1`;
- `det(L_Sigma) = 5/3`;
- `p_vac(L_Sigma) = (1/4) log(5/3)`.

So the three residuals are exactly:

- `delta_0 = -1`;
- `delta_gauss = (1/4) log(5/3) - 1 ~= -0.872294`;
- `delta_quarter = 1/4`.

Thus neither currently canonical decomposition lands anywhere near the quarter
residual.

## Step 3: the only live positive residual candidate

The branch already isolated one exact positive quarter-valued quantity:

`m_axis = Tr(rho_cell P_A) = 1/4`

on the democratic `C^16` carrier.

So the decomposition route now has one very sharp possible close:

`delta = m_axis`,

equivalently

`nu = lambda_min(L_Sigma) + m_axis`.

On the exact witness this is

`nu = 1 + 1/4 = 5/4`.

This does **not** follow from the current scalar/vacuum/action grammar. It is
precisely the new positive-residual law that would have to be proved.

## Theorem 3: exact reduction of the decomposition route

Assume only the already-earned inputs listed above.

Then the vacuum-action decomposition route reduces exactly to the following
fork:

1. the current same-surface scalar/vacuum route gives residuals
   `delta in {-lambda_min(L_Sigma), p_vac(L_Sigma) - lambda_min(L_Sigma)}`,
   which are negative on the retained positive witness family;
2. exact Planck quarter requires the positive residual
   `delta = 1/4`;
3. the only exact positive quarter-valued candidate currently isolated on the
   branch is
   `m_axis = 1/4`;
4. therefore any successful close on this route must prove one new
   same-surface positive-residual theorem

   `delta = m_axis`,

   or an equally canonical theorem landing the same positive quarter residual.

So the decomposition lane is now fully reduced:

> not to an arbitrary normalization problem,
> but to one missing positive worldtube residual law.

## Best honest verdict

This route did not produce a retained Planck closure.

What it did produce is the sharpest decomposition statement I can justify:

- the action side always splits into a Schur floor plus residual;
- the current exact residuals are negative;
- quarter needs a positive residual;
- the only current exact positive candidate is the coarse `C^16` axis-sector
  mass.

So the direct scientific target is now explicit:

> derive the physical positive residual law
>
> `delta = m_axis`,
>
> or prove that no such same-surface identification exists.
