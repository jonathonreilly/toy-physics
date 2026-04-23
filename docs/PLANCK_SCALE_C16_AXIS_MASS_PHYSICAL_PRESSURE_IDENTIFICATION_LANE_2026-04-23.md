# Planck-Scale `C^16` Axis-Mass Physical-Pressure Identification Lane

**Date:** 2026-04-23  
**Status:** science-only endpoint no-go plus exact reduction theorem  
**Audit runner:** `scripts/frontier_planck_c16_axis_mass_physical_pressure_identification_lane.py`

## Question

The boundary program has now been reduced to one sharp possible close:

`physical boundary pressure = C^16 axis-sector mass`.

Can that statement be derived directly from the accepted same-surface stack, or
does it remain one genuinely new physical law?

More concretely:

- the Schur boundary side gives the exact carrier `L_Sigma`, the exact scalar
  observable
  `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`,
  and the exact action pressure family
  `p_*(nu) = nu - lambda_min(L_Sigma)`;
- the `C^16` side gives the exact coarse worldtube scalar
  `m_axis = Tr(rho_cell P_A) = 1/4`;
- the surviving Planck boundary target is exactly `1/4`.

The exact remaining question is:

> does the current same-surface grammar already force
>
> `p_phys = m_axis`,
>
> or is that still the one missing worldtube/projector law?

## Bottom line

It is still the one missing physical law.

The strongest honest endpoint is:

1. the current observable-principle scalar on the Schur boundary carrier is
   exactly
   `p_obs = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;
2. the current action-native growth pressure is exactly
   `p_*(nu) = nu - lambda_min(L_Sigma)`;
3. the exact `C^16` quantity matching quarter is the coarse axis-sector mass
   `m_axis = 1/4`;
4. but `m_axis` lives on a different carrier and needs the extra projector
   `P_A`, while the current scalar boundary grammar does not supply an exact
   map
   `Schur boundary carrier -> C^16 axis projector algebra`;
5. therefore the current same-surface stack does **not** derive
   `p_phys = m_axis`;
6. exact boundary Planck closure on this route is now equivalent to one new
   theorem:

   `p_phys = Tr(rho_cell P_A) = m_axis`,

   equivalently on the action lane,

   `nu = lambda_min(L_Sigma) + m_axis`.

On the canonical witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

this becomes

`nu = 1 + 1/4 = 5/4`.

So the direct endpoint is:

> the boundary lane is now closed as a reduction theorem, not as a retained
> Planck theorem. If this route is to close, it must close by a new
> worldtube-projector identification law.

## Inputs

This note uses only already-earned branch-local results:

- [PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_REFERENCE_EXHAUSTION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_REFERENCE_EXHAUSTION_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_BOUNDARY_C16_SYNTHESIS_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_BOUNDARY_C16_SYNTHESIS_LANE_2026-04-23.md)

What those lanes already fix exactly:

1. on the Schur boundary carrier, the current scalar observable is

   `p_obs = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

2. on the action lane, the exact growth pressure family is

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

3. the only canonical same-surface vacuum-action densities presently earned are

   `nu in {0, p_vac(L_Sigma)}`;

4. on the democratic `C^16` carrier, the exact `hw=1` axis-sector mass is

   `m_axis = Tr(rho_cell P_A) = 1/4`;

5. on the canonical witness,

   `lambda_min(L_Sigma) = 1`,
   `p_vac(L_Sigma) = (1/4) log(5/3)`,
   `m_axis = 1/4`.

This note asks whether those inputs already force the physical identification

`p_phys = m_axis`.

## Step 1: the two surviving candidate quantities live on different carrier grammars

The Schur boundary route and the `C^16` route now each produce one exact
quarter-relevant quantity, but they do so in different ways.

### 1A. Schur boundary scalar grammar

The current observable-principle note proves that the scalar boundary observable
selected by multiplicative partition factorization is

`p_obs(L_Sigma) = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

This quantity:

- lives on the Schur boundary mode space;
- is scalar and additive on independent direct sums;
- needs no extra projector beyond the boundary carrier itself.

### 1B. `C^16` axis-sector projector grammar

The `C^16` bridge note proves that the exact quarter-valued same-carrier
quantity is

`m_axis = Tr(rho_cell P_A) = 1/4`,

where

- `rho_cell = I_16 / 16` is the democratic full-cell state;
- `P_A` projects onto the exact four-state `hw=1` axis sector
  `{1000, 0100, 0010, 0001}`.

This quantity:

- lives on the democratic `C^16` taste-cell carrier;
- is not the current Schur scalar observable;
- explicitly uses an extra coarse projector `P_A`.

So the two sides are not the same current observable written two ways. They are
different exact quantities living on different exact carrier grammars.

## Theorem 1: the current same-surface stack does not derive `p_phys = m_axis`

Assume only the already-earned branch-local inputs listed above.

Then the current same-surface stack proves all of the following:

1. if physical boundary pressure is identified with the current scalar
   observable-principle quantity on the Schur carrier, then

   `p_phys = p_vac(L_Sigma)`;

2. if physical boundary pressure is identified with the action-native growth
   pressure, then it has the form

   `p_phys = p_*(nu) = nu - lambda_min(L_Sigma)`;

3. the exact `C^16` quarter-valued candidate is

   `m_axis = Tr(rho_cell P_A) = 1/4`;

4. but the current accepted stack does not supply an exact carrier/projector
   theorem pulling the Schur boundary observable into the `C^16` axis projector
   algebra.

Therefore the current same-surface stack does **not** derive

`p_phys = m_axis`.

### Proof sketch

Item (1) is exactly the observable-principle boundary note.  
Item (2) is exactly the action-pressure note.  
Item (3) is exactly the `C^16` bridge note.  
Item (4) is exactly what the synthesis note isolates: the Schur scalar
`p_vac(L_Sigma)` and the coarse `C^16` quantity `m_axis` remain distinct exact
theorems, and the present stack contains no equality theorem between them.

So the branch does not have a hidden retained derivation of

`p_phys = m_axis`.

## Step 2: family-level obstruction

The non-derivation above is not just a witness accident.

Consider the positive symmetric family

`L(r) = [[1 + r, r], [r, 1 + r]]`,

with `0 < r < 1`.

Then:

- `lambda_min(L(r)) = 1`;
- `det(L(r)) = 1 + 2r`;
- the current scalar boundary observable is

  `p_vac(L(r)) = (1/4) log(1 + 2r)`.

So the Schur scalar observable varies with `r`, while the coarse `C^16`
quantity remains fixed:

`m_axis = 1/4`.

This means the current Schur scalar grammar does not secretly force quarter
even on the simplest positive same-symmetry family. Quarter enters only if one
adds a new constant/projector datum beyond the current scalar Schur observable.

## Theorem 2: the direct endpoint is one new worldtube-projector law

Under the same inputs, exact boundary Planck closure on the current route is
equivalent to one new identification theorem:

`p_phys = Tr(rho_cell P_A) = m_axis`.

On the action lane this is equivalent to

`nu = lambda_min(L_Sigma) + m_axis`.

### Proof

From the action-pressure lane,

`p_*(nu) = nu - lambda_min(L_Sigma)`.

Therefore:

`p_*(nu) = m_axis`

if and only if

`nu = lambda_min(L_Sigma) + m_axis`.

So once the `C^16` side has isolated `m_axis` as the right quarter-valued
candidate, the entire remaining closure problem is equivalent to one physical
law: identify the physical boundary pressure with the coarse axis-sector mass,
or equivalently identify the physical boundary vacuum-action density with
`lambda_min + m_axis`.

Nothing weaker closes the route, and nothing else remains hidden in the current
stack.

## Corollary: on the canonical witness the entire open content is `nu = 5/4`

On the canonical Schur witness,

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

we have

`lambda_min(L_Sigma) = 1`,

and from the `C^16` bridge lane

`m_axis = 1/4`.

So the exact remaining bridge collapses to

`nu = 1 + 1/4 = 5/4`.

This is already sharper than the old normalization-language presentation. It is
no longer "find a good boundary coefficient." It is "derive why the physical
boundary worldtube pressure is read on the coarse axis-sector projector."

## What would count as a real close now

The only acceptable close on this route would be a theorem of the following
type:

1. construct an exact same-surface map from the physical boundary worldtube
   carrier to the democratic `C^16` axis-sector projector algebra; or
2. derive directly that the physical boundary growth pressure is the coarse
   four-axis worldtube mass
   `Tr(rho_cell P_A)`;
3. thereby derive
   `nu = lambda_min(L_Sigma) + m_axis`.

Anything weaker is not retained Planck closure on this lane.

## Direct conclusion

The last boundary lane is now concluded directly and honestly:

- the current boundary stack does **not** derive
  `p_phys = m_axis`;
- the boundary route is therefore **not** retained Planck closure on current
  inputs;
- the exact open content is one new worldtube-projector law;
- absent that law, the route should remain classified as an open/bounded bridge
  rather than a closed retained theorem.

That is the clean endpoint of the current same-surface boundary program.
