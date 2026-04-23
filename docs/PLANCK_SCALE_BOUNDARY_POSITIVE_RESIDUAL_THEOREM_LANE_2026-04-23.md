# Planck-Scale Boundary Positive-Residual Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only exact decomposition theorem plus smallest remaining readout law  
**Audit runner:** `scripts/frontier_planck_boundary_positive_residual_theorem_lane.py`

## Question

The action lane has already reduced the boundary coefficient problem to

`nu = lambda_min(L_Sigma) + delta`,

with exact action pressure

`p_*(nu) = delta`.

The immediate obstruction is now sharp:

- the currently earned scalar same-surface residuals are negative;
- exact Planck quarter needs the positive residual
  `delta = 1/4`;
- the branch already isolates one exact positive quarter-valued same-surface
  quantity,
  `m_axis = Tr(rho_cell P_A) = 1/4`,
  where `P_A` is the section-canonical coarse four-axis worldtube projector.

The exact question is:

> can the positive residual theorem be closed directly on the action side,
> and if not, what is the smallest remaining law?

## Bottom line

The strongest honest result is:

1. within the current scalar Schur/vacuum grammar, there is an exact **sign
   obstruction**: the retained same-surface residuals are negative on the
   whole positive witness family;
2. on the same branch-local stack, time-lock plus exact `3+1` axis structure
   forces the coarse worldtube selector onto the unique residual-invariant
   projector

   `P_A = P_t + P_s`;

3. on the exact democratic `C^16` carrier, the corresponding section-canonical
   sector share is uniquely

   `delta_pos := Tr(rho_cell P_A) = 4/16 = 1/4 = m_axis`;

4. therefore the action lane now has an exact **positive-residual
   decomposition theorem**:

   - scalar same-surface residuals do not supply the needed sign;
   - the unique current positive same-surface residual compatible with the
     section-canonical worldtube sector is `m_axis = 1/4`;

5. under the single additional readout law

   `delta = Tr(rho_cell P_A)`,

   exact action closure follows immediately:

   `nu = lambda_min(L_Sigma) + m_axis`,
   `p_* = m_axis = 1/4`;

6. on the canonical witness
   `L_Sigma = [[4/3,1/3],[1/3,4/3]]`,
   this is

   `nu = 1 + 1/4 = 5/4`.

So the direct action-side frontier is no longer a coefficient search. It is
one readout statement:

> the positive vacuum-action residual is the democratic share of the
> section-canonical four-axis worldtube sector.

That is the smallest remaining new law on this route.

## Inputs

This lane uses only branch-local results already isolated elsewhere:

- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)

What those lanes already fix exactly:

1. the retained one-clock action family

   `I_nu(tau ; b, j) = tau (1/2 b^T L_Sigma b - j^T b - nu)`;

2. the exact action pressure law

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

3. the exact decomposition variable

   `nu = lambda_min(L_Sigma) + delta`,
   so
   `p_* = delta`;

4. the current scalar same-surface residuals

   `delta_0 = -lambda_min(L_Sigma)`,
   `delta_gauss = p_vac(L_Sigma) - lambda_min(L_Sigma)`;

5. the coarse section-canonical worldtube projector

   `P_A = P_t + P_s = sum_(|eta|=1) P_eta`;

6. the democratic full-cell state

   `rho_cell = I_16 / 16`;

7. the exact quarter-valued `C^16` quantity

   `m_axis = Tr(rho_cell P_A) = 1/4`.

This note combines those facts directly on the action side.

## Step 1: scalar same-surface residuals have the wrong sign

From the decomposition lane,

`delta_0 = -lambda_min(L_Sigma)`,

and on the positive witness family

`L(r) = [[1 + r, r], [r, 1 + r]]`,

one has

`lambda_min(L(r)) = 1`,
`p_vac(L(r)) = (1/4) log(1 + 2r)`,

so

`delta_gauss(L(r)) = (1/4) log(1 + 2r) - 1 < 0`

for `0 < r < 1`.

Therefore the current scalar Schur/vacuum grammar does not merely fail to
produce quarter. It produces negative residuals on the retained witness family.

That proves the direct scalar route has a sign obstruction.

## Theorem 1: no positive residual is supplied by the current scalar Schur grammar

Assume only the retained scalar same-surface action data:

1. `p_*(nu) = nu - lambda_min(L_Sigma)`;
2. the canonical action-side values
   `nu in {0, p_vac(L_Sigma)}`;
3. the retained positive witness family
   `L(r) = [[1 + r, r], [r, 1 + r]]`, `0 < r < 1`.

Then the corresponding scalar residuals are

`delta_0(L(r)) = -1`,

`delta_gauss(L(r)) = (1/4) log(1 + 2r) - 1`,

and both are negative on the retained family.

So the current scalar Schur grammar does **not** derive any positive residual,
let alone the quarter-valued one.

This is the exact sign obstruction.

## Step 2: the coarse positive sector is now fixed

The worldtube-selector lane proves:

- on the minimal nonzero shell `S_1`, the only residual-invariant projectors
  are
  `0`, `P_t`, `P_s`, and `P_A`;
- requiring the selector to be local, minimal-shell, time-complete, and
  spatially isotropic uniquely forces

  `P_A = P_t + P_s`.

So the branch no longer has an arbitrary positive sector search.
At the coarse worldtube level the positive sector is fixed.

## Step 3: the section-canonical positive sector has exact democratic mass `1/4`

On the democratic full-cell state

`rho_cell = I_16 / 16`,

every basis direction carries mass `1/16`.

The section-canonical worldtube sector `P_A` has rank `4`, so its exact
democratic sector share is

`Tr(rho_cell P_A) = 4/16 = 1/4`.

This is exactly the previously isolated

`m_axis = 1/4`.

So once the worldtube sector is fixed, the positive same-surface quantity is
also fixed.

## Theorem 2: uniqueness of the current positive same-surface residual candidate

Assume:

1. the coarse worldtube selector is required to be residual-invariant,
   minimal-shell, time-complete, and spatially isotropic;
2. the positive residual is read as the democratic share of the selected
   coarse worldtube sector on the same `C^16` carrier.

Then the unique admissible projector is `P_A`, and the unique corresponding
positive residual is

`delta_pos = Tr(rho_cell P_A) = 1/4 = m_axis`.

### Proof

By the section-canonical worldtube theorem, the only admissible projector under
the listed carrier constraints is `P_A`.

By democratic full-cell weighting,

`Tr(rho_cell P_t) = 1/16`,
`Tr(rho_cell P_s) = 3/16`,
`Tr(rho_cell P_A) = 4/16 = 1/4`.

So once `P_A` is fixed, the corresponding democratic sector share is fixed as
well, and it is positive and quarter-valued.

There is therefore no remaining coefficient freedom on this positive-residual
route.

## Step 4: exact action closure under the sector-share readout law

By the action decomposition,

`p_* = delta`.

By Theorem 2, the unique current positive same-surface residual candidate is

`delta_pos = m_axis = 1/4`.

So if the positive residual is read on the section-canonical worldtube sector,
then

`delta = m_axis`,

hence

`nu = lambda_min(L_Sigma) + m_axis`,

and

`p_* = m_axis = 1/4`.

This is an exact action-side closure statement once the residual readout law is
accepted.

## Theorem 3: conditional exact positive-residual closure on the action lane

Assume:

1. the exact action decomposition
   `nu = lambda_min(L_Sigma) + delta`;
2. the section-canonical worldtube selector theorem forcing `P_A`;
3. the positive residual readout law

   `delta = Tr(rho_cell P_A)`.

Then

`delta = m_axis = 1/4`,

and therefore

`p_* = 1/4`,

`nu = lambda_min(L_Sigma) + 1/4`.

On the canonical witness with `lambda_min(L_Sigma) = 1`, this is

`nu = 5/4`.

So the direct action-side closure is exact under one new readout law and no new
coefficient search.

## Corollary: the smallest remaining law is not numerical

The remaining open content is **not**:

- a new floating coefficient,
- a new affine normalization scan,
- or a reopened scalar Schur search.

It is only the physical identification

`delta = Tr(rho_cell P_A)`.

In plain terms:

> the boundary vacuum-action residual is the democratic share of the
> section-canonical four-axis worldtube sector.

That is the smallest remaining new law on the current action-side route.

## What this does and does not close

What this note closes:

1. the scalar Schur/vacuum route is fully sign-obstructed for positive
   residuals;
2. the positive same-surface sector is no longer ambiguous at the coarse
   worldtube level;
3. the positive residual candidate is uniquely fixed to `m_axis = 1/4`;
4. the action-side coefficient `nu = 5/4` is exact once that readout law is
   accepted.

What this note does **not** yet close:

1. it does not derive the residual readout law from the current scalar
   observable principle alone;
2. it does not prove that the physical boundary pressure must be read as a
   democratic sector share rather than as the scalar Schur observable;
3. it therefore does not yet upgrade the route to retained no-import closure.

## Honest verdict

The positive-residual theorem is now as sharp as it can honestly be on the
current branch:

- **negative scalar residuals are ruled out** as a source of quarter;
- **the unique positive same-surface residual candidate is fixed** as
  `m_axis = 1/4`;
- **exact action closure follows conditionally** from one explicit readout law.

So the current direct frontier is:

> not “find the number,”
> but “derive why the action residual is read on the section-canonical
> worldtube sector.”
