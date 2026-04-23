# Planck-Scale Boundary Bulk-to-`C^16` Intertwiner Lane

**Date:** 2026-04-23  
**Status:** science-only exact quotient theorem plus faithful-intertwiner no-go  
**Audit runner:** `scripts/frontier_planck_boundary_bulk_to_c16_intertwiner_lane.py`

## Question

Can the remaining Planck boundary bridge be closed by an exact same-surface
intertwiner from the canonical Schur boundary carrier to the democratic
`C^16` axis-sector projector algebra?

More concretely:

- the bulk/boundary route fixes the canonical Schur boundary carrier
  `L_Sigma` on a **2-dimensional** reduced boundary/worldtube space;
- the `C^16` route fixes the exact axis-sector projector
  `P_A` on a **4-dimensional** `hw=1` axis carrier
  `A = {t, x, y, z}`;
- the surviving quarter-valued candidate is
  `m_axis = Tr(rho_cell P_A) = 1/4`.

The exact remaining question is:

> does minimal time-locked Schur completion canonically pull back to the full
> axis projector `P_A`, or does it only see a smaller quotient of that
> carrier?

## Bottom line

The strongest honest result is a **faithful-intertwiner no-go plus exact
quotient theorem**, not a full Planck close.

What is forced:

1. the canonical Schur boundary carrier is 2-dimensional;
2. the full `C^16` axis projector `P_A` has rank `4`;
3. therefore no linear map between the minimal Schur carrier and the axis
   sector can realize `P_A` faithfully as an exact pullback/pushforward
   projector, because every operator of the form `J^* J` or `J J^*` from a
   2-dimensional carrier has rank at most `2`;
4. if one requires the bulk-to-boundary map to be blind to the labels
   `x, y, z` and depend only on the collective time-locked boundary grammar,
   then the unique surviving quotient of the axis carrier is the 2-dimensional
   singlet block

   `H_q = span{|t>, |s>}`,

   where

   `|s> = (|x> + |y> + |z>) / sqrt(3)`;

5. the corresponding canonical quotient projector is

   `P_q = |t><t| + |s><s|`

   with rank `2`;

6. under the exact democratic full-cell state

   `rho_cell = I_16 / 16`,

   the full axis mass is

   `Tr(rho_cell P_A) = 4/16 = 1/4`,

   but the canonical quotient mass is only

   `Tr(rho_cell P_q) = 2/16 = 1/8`.

So the highest-value conclusion is:

> Schur completion of the minimal time-locked boundary worldtube does **not**
> canonically pull back to the full `hw=1` axis projector `P_A`.
> It canonically lands only on the 2-dimensional singlet quotient `P_q`,
> and that quotient carries mass `1/8`, not `1/4`.

Therefore exact quarter on this route would still need one extra theorem
beyond the canonical intertwiner:

- either a multiplicity-restoration law
  `Tr(rho_cell P_A) = 2 Tr(rho_cell P_q)`,
- or a different non-minimal carrier that retains the invisible `E` doublet.

## Inputs

This lane uses only already-earned branch-local results:

- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md](./PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)

What those lanes already fix exactly:

1. the canonical Schur witness

   `L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`

   on a 2-dimensional boundary carrier;

2. the exact democratic `C^16` full-cell state

   `rho_cell = I_16 / 16`;

3. the exact axis-sector projector on the four `hw=1` axis states

   `P_A = P_t + P_x + P_y + P_z`;

4. the exact quarter-valued same-carrier scalar

   `m_axis = Tr(rho_cell P_A) = 1/4`.

This note asks whether the Schur carrier can be canonically intertwined to the
full axis projector itself.

## Setup

Write the exact axis carrier as

`H_A = span{|t>, |x>, |y>, |z>}`.

Let the spatial permutation group `S_3` act by permuting `|x>, |y>, |z>` and
fixing `|t>`.

The exact full-axis projector is

`P_A = |t><t| + |x><x| + |y><y| + |z><z| = I_(H_A)`.

Because the minimal Schur boundary carrier has dimension `2`, any exact
intertwiner to/from that carrier must pass through a rank-`<= 2` image.

The collective time-locked boundary grammar also has no residual labels
distinguishing `x`, `y`, `z` individually. So any canonical map must be
blind to spatial permutations.

## Theorem 1: no faithful exact intertwiner to the full axis projector

Let `H_Sigma` be the canonical Schur boundary carrier with

`dim(H_Sigma) = 2`.

Let `J` be any linear map between `H_Sigma` and `H_A`.

Then:

- `rank(J^* J) <= 2`,
- `rank(J J^*) <= 2`.

But

`rank(P_A) = 4`.

Therefore no such `J` can satisfy a faithful projector identity with the full
axis projector, for example

- `J^* J = P_A`, or
- `J J^* = P_A`.

So the minimal Schur carrier cannot be faithfully intertwined with the full
`C^16` axis projector.

This kills the strongest possible version of the hoped-for route:

> the canonical boundary carrier does **not** have enough exact slots to carry
> the full rank-4 axis projector data.

## Theorem 2: the unique canonical quotient is the singlet block

Inside `H_A`, define the exact spatial singlet

`|s> = (|x> + |y> + |z>) / sqrt(3)`.

Then the `S_3`-fixed subspace of `H_A` is exactly

`Fix(S_3) = span{|t>, |s>}`.

Its orthogonal complement inside the spatial three-state block is the exact
doublet

`E = {a_x |x> + a_y |y> + a_z |z> : a_x + a_y + a_z = 0}`,

with dimension `2`.

So the exact decomposition is

`H_A = span{|t>} (+) span{|s>} (+) E`.

If the boundary map is required to be blind to spatial labels and live on the
minimal 2-dimensional Schur carrier, then it must factor through the quotient

`H_q := span{|t>, |s>}`.

Equivalently, the canonical quotient projector is

`P_q = |t><t| + |s><s|`.

This is the unique rank-2 permutation-blind quotient compatible with the
minimal Schur boundary carrier.

## Theorem 3: the canonical quotient carries mass `1/8`, not `1/4`

Because the full democratic state is scalar,

`rho_cell = I_16 / 16`,

every orthonormal direction in the 16-state carrier has exact weight `1/16`.

Therefore:

- the full axis projector has democratic mass

  `Tr(rho_cell P_A) = rank(P_A) / 16 = 4/16 = 1/4`;

- the canonical quotient projector has democratic mass

  `Tr(rho_cell P_q) = rank(P_q) / 16 = 2/16 = 1/8`.

So the exact same-surface quotient from the axis carrier to the minimal Schur
carrier loses half of the axis mass:

`Tr(rho_cell P_A) = 2 Tr(rho_cell P_q)`.

This is the sharpest direct obstruction on the intertwiner route.

It means the quarter does **not** survive the canonical quotient unchanged.

## Corollary: what the intertwiner route actually reduces to

The bulk-to-boundary intertwiner route is now reduced to one explicit extra
law:

> either restore the missing factor of `2`,
> or prove that the physical boundary pressure is not read on the minimal
> quotient `P_q` but on a lifted carrier that still counts the discarded
> doublet multiplicity.

In formula form, the surviving Planck bridge is no longer simply

`p_phys = Tr(rho_cell P_A)`.

It is now:

`p_phys = 2 Tr(rho_cell P_q)`

or an equivalent non-minimal lift.

That is strictly sharper than the earlier open statement `p_phys = m_axis`,
because it says exactly where the missing quarter sits relative to the best
canonical intertwiner available on the current same-surface stack.

## Best honest verdict

This lane does not close Planck. It improves the frontier by proving a better
no-go and a sharper target:

- **No faithful full-axis intertwiner:** exact and closed.
- **Best canonical quotient:** exact and closed.
- **Mass carried by that quotient:** exact and equal to `1/8`.
- **Remaining bridge:** one extra multiplicity/lift theorem taking `1/8` to
  `1/4`.

So the route is no longer:

- “maybe Schur completion canonically is the full axis projector.”

It is now:

- “Schur completion canonically sees only the singlet quotient; quarter would
  require restoring the discarded doublet multiplicity.”

## Reviewer-safe wording

> On the minimal time-locked boundary route, the canonical Schur carrier is
> 2-dimensional, while the full `hw=1` axis projector on the democratic
> `C^16` carrier has rank 4. Therefore no faithful exact intertwiner from the
> minimal Schur carrier to the full axis projector exists. Requiring the map
> to be blind to spatial-axis labels forces a unique rank-2 quotient,
> `H_q = span{|t>, (|x>+|y>+|z>)/sqrt(3)}`. Under the exact democratic
> full-cell state this quotient carries mass `1/8`, whereas the full axis
> projector carries mass `1/4`. Thus the canonical intertwiner route narrows
> the remaining Planck bridge to one explicit multiplicity/lift theorem rather
> than closing it outright.
