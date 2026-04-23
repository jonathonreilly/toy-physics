# Planck-Scale Boundary Observable-Principle Pressure Identification Lane

**Date:** 2026-04-23  
**Status:** science-only observable-principle identification theorem plus sharp
boundary-pressure no-go  
**Audit runner:** `scripts/frontier_planck_boundary_observable_principle_pressure_identification_lane.py`

## Question

The boundary route is now reduced to three exact same-surface quantities:

- the Schur vacuum density

  `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

- the action-native growth-pressure family

  `p_*(nu) = nu - lambda_min(L_Sigma)`;

- the `C^16` bridge candidate

  `m_axis = 1/4`.

The exact remaining question is:

> can the observable principle itself identify the **physical boundary
> pressure** with one of these quantities, using only same-surface
> observable/source-response grammar?

## Bottom line

Yes, but not in the direction needed for Planck closure.

The observable-principle side fixes one exact thing and rules out two others.

1. The exact boundary scalar observable selected by the observable-principle
   logic is the normalized Schur vacuum free energy

   `F_vac(L_Sigma) := -log Z_hat(L_Sigma) = (1/2) log det(L_Sigma)`,

   equivalently the density

   `p_obs(L_Sigma) := F_vac(L_Sigma)/n = p_vac(L_Sigma)`.

2. The semigroup top-growth pressure

   `p_* = sup spec(G_Sigma)`

   is **not** the current observable-principle scalar on the boundary route,
   because it is not additive on independent direct sums.

3. The `C^16` axis-sector mass

   `m_axis = 1/4`

   is also **not** selected by the current boundary observable grammar,
   because it needs an extra projector on a different carrier (`C^16`) rather
   than a scalar source-response on the Schur boundary mode space itself.

So the strongest honest statement is:

> if physical boundary pressure is required to be the current
> observable-principle scalar on the Schur boundary carrier, then it is
> exactly
>
> `p_phys = p_obs = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`,
>
> not `1/4`.

On the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

this gives

`p_phys = p_vac = (1/4) log(5/3) ~= 0.127706`,

so quarter is ruled out on the boundary route **if** one insists that the
physical boundary pressure is the current observable-principle scalar.

That is a real result. It means the remaining Planck option is now very
specific:

> quarter must come from a new non-scalar / block-selecting bridge beyond the
> current observable-principle scalar grammar.

## Inputs

This note uses only already-opened same-surface ingredients:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
- [PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)

What those notes already fix exactly:

1. additive scalar observable generators are forced by multiplicative partition
   factorization;
2. the Schur boundary action is exact on the current boundary carrier;
3. the normalized boundary Gaussian partition is

   `Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`;

4. the action-native growth-pressure family is

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

5. the `C^16` bridge candidate is the axis-sector mass

   `m_axis = 1/4`.

This note asks which, if any, of these the current observable principle can
actually identify as the **physical boundary pressure**.

## Step 1: exact boundary observable generator

On the exact Schur carrier, the source-free normalized Gaussian partition is

`Z_hat(L_Sigma) = det(L_Sigma)^(-1/2)`.

For independent boundary carriers

`L = L_1 (+) L_2`,

the partition factorizes exactly:

`Z_hat(L_1 (+) L_2) = Z_hat(L_1) Z_hat(L_2)`.

The observable-principle note already proved the scalar logic:

- multiplicative partition data;
- additive scalar observable on independent subsystems;
- minimal regularity;

force the logarithm.

So on the boundary route the exact additive scalar generator is

`F_vac(L_Sigma) := -log Z_hat(L_Sigma) = (1/2) log det(L_Sigma)`.

Dividing by carrier rank `n` gives the scalar density

`p_obs(L_Sigma) := F_vac(L_Sigma)/n = (1/(2n)) log det(L_Sigma)`.

This is exactly the previously derived Schur vacuum density:

`p_obs(L_Sigma) = p_vac(L_Sigma)`.

## Theorem 1: the observable principle identifies the scalar boundary observable with `p_vac`

Assume:

1. the exact Schur boundary action;
2. no extra carrier beyond the Schur boundary mode space;
3. scalar additivity on independent boundary carriers;
4. the same multiplicative-to-additive logic already used in
   [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).

Then the exact scalar boundary observable generator is

`F_vac(L_Sigma) = (1/2) log det(L_Sigma)`,

and the exact scalar boundary observable density is

`p_obs(L_Sigma) = (1/(2n)) log det(L_Sigma) = p_vac(L_Sigma)`.

So the current observable principle does make an exact identification:

`observable-principle scalar boundary pressure = p_vac(L_Sigma)`.

## Step 2: why `p_*` is not the current observable-principle scalar

The action-native semigroup pressure is

`p_* = sup spec(G_Sigma)`.

For independent blocks

`G = G_1 (+) G_2`,

one has

`sup spec(G_1 (+) G_2) = max(sup spec(G_1), sup spec(G_2))`.

So `p_*` is not additive on independent subsystems. It is a max law.

But the observable-principle scalar is additive by construction. Therefore
`p_*` cannot be identified with the current scalar observable principle on the
boundary route without introducing an extra block-selection law.

## Theorem 2: top-growth pressure is outside the current scalar observable grammar

On the current exact boundary route:

1. `F_vac(L)` is additive on direct sums;
2. `p_*(G) = sup spec(G)` is max-type on direct sums.

Therefore the current observable-principle scalar does **not** identify
physical boundary pressure with `p_*`.

Equivalently:

> to read physical boundary pressure as `p_*`, one needs a new non-additive
> block-selection or growth-selection principle beyond the present scalar
> observable grammar.

## Step 3: why `m_axis` is not the current boundary observable either

The `C^16` note proved that the exact canonical `C^16` scalar matching the
boundary quarter target is the axis-sector mass

`m_axis = 1/4`.

But this quantity lives on the democratic `C^16` taste-cell carrier and is
defined using the extra projector

`P_A = sum_(eta in hw=1 axis sector) P_eta`.

That is not the current Schur boundary scalar grammar.

The current boundary observable principle works on the Schur boundary mode
space and its scalar source-response data. It does **not** presently contain an
exact map

`Schur boundary mode space -> C^16 axis projector algebra`.

So the observable principle does not currently identify

`p_phys = m_axis`

on its own.

## Theorem 3: `m_axis` is a candidate bridge quantity, not the current scalar observable

Assume no new carrier map beyond the present Schur boundary observable grammar.
Then the current observable principle does **not** derive

`p_phys = m_axis`.

It only says:

- the scalar Schur observable is `p_vac(L_Sigma)`;
- `m_axis` is a different same-surface quantity on a different carrier that
  could close the boundary law only after an additional physical bridge.

So `m_axis` remains a serious candidate, but not an observable-principle
identification theorem.

## Minimal exact witness

Take the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

Then

`spec(L_Sigma) = {1, 5/3}`,

`det(L_Sigma) = 5/3`,

and `n = 2`.

Therefore the observable-principle scalar density is

`p_obs(L_Sigma) = p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`.

Meanwhile:

- the action-native family reads

  `p_*(nu) = nu - 1`;

- exact quarter would require

  `nu = 5/4`;

- the `C^16` axis-sector candidate is

  `m_axis = 1/4`.

So the witness exhibits the exact split:

`p_obs = (1/4) log(5/3)`,

`p_* (quarter) = 1/4`,

`m_axis = 1/4`.

The current observable-principle scalar picks the first value, not the latter
two.

## Corollary: if pressure is observable-principle scalar, the boundary route misses Planck

If one insists that the physical boundary pressure is the current
observable-principle scalar on the Schur carrier, then

`p_phys = p_obs = p_vac(L_Sigma)`.

On the exact witness this is not `1/4`, so exact boundary quarter is ruled out.

The action lane then fixes the corresponding vacuum density to

`nu_obs = lambda_min(L_Sigma) + p_obs`
`      = 1 + (1/4) log(5/3)`,

not `5/4`.

So the observable-principle route does not rescue quarter. It instead kills it
unless one goes beyond the current scalar grammar.

## Exact remaining choice

The branch now has an exact trichotomy.

1. **Observable-principle scalar route**

   `p_phys = p_vac(L_Sigma)`.

   This is now exact and same-surface, but it does **not** give quarter.

2. **Growth-pressure route**

   `p_phys = p_*(nu)`.

   This requires an extra non-additive growth-selection law not supplied by the
   current observable principle.

3. **`C^16` bridge route**

   `p_phys = m_axis`.

   This requires an extra carrier map / projector-selection law not supplied by
   the current boundary observable principle.

So the exact remaining choice is no longer numerical. It is conceptual:

> is physical boundary pressure the additive scalar observable of the Schur
> boundary carrier, or a different non-scalar/block-selected quantity?

That is now the clean frontier.

## Honest status

This note does **not** close Planck.

What it really closes is narrower and important:

- it identifies exactly what the current observable principle says on the
  boundary route;
- it proves that this current observable principle selects `p_vac`, not
  quarter;
- it turns the remaining Planck problem into one explicit physical bridge
  beyond the current scalar grammar.

That is the strongest honest observable-principle result I can justify on the
current boundary lane.
