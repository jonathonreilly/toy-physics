# Planck-Scale Boundary Multiplicity-Lift Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only exact carrier-level lift theorem plus sharp remaining scalar gap  
**Audit runner:** `scripts/frontier_planck_boundary_multiplicity_lift_theorem_lane.py`

## Question

The boundary lane had been reduced to one exact missing factor:

- the best canonical Schur-to-`C^16` quotient only sees the rank-2 projector

  `P_q = |t><t| + |s><s|`,

  with

  `|s> = (|x> + |y> + |z>) / sqrt(3)`,

  and therefore carries democratic mass `1/8`;

- the full coarse worldtube selector is the rank-4 projector

  `P_A = P_t + P_x + P_y + P_z`,

  and therefore carries democratic mass `1/4`.

The direct remaining question is:

> is the missing factor of `2` already forced by the accepted carrier structure,
> or is it still one extra imported multiplicity law?

Equivalently:

> why should the physical quantity be
>
> `2 Tr(rho_cell P_q)`
>
> rather than just
>
> `Tr(rho_cell P_q)`?

## Bottom line

The strongest honest result is **positive at the carrier-measure level**.

The missing factor of `2` is not arbitrary once one combines:

1. the exact section-canonical worldtube selector theorem, which forces the
   physical coarse sector to be the full four-axis projector `P_A`;
2. the exact bulk-to-boundary intertwiner theorem, which shows the minimal
   Schur carrier only sees the permutation-blind quotient projector `P_q`;
3. the exact `S_3` decomposition of the full axis carrier into

   `H_A = H_q (+) E`,

   where

   - `H_q = span{|t>, |s>}` is the visible quotient block,
   - `E` is the invisible 2-dimensional spatial doublet block;
4. the exact no-proper-quotient / physical-species semantics already earned on
   retained observable sectors;
5. the democratic `C^16` full-cell state `rho_cell = I_16 / 16`.

Those inputs force:

- `P_A = P_q + P_E`,
- `P_q P_E = 0`,
- `rank(P_q) = rank(P_E) = 2`,
- `Tr(rho_cell P_q) = Tr(rho_cell P_E) = 1/8`,
- hence

  `Tr(rho_cell P_A) = Tr(rho_cell P_q) + Tr(rho_cell P_E) = 2 Tr(rho_cell P_q) = 1/4`.

So the exact carrier-level multiplicity lift is:

> the full physical coarse worldtube mass is exactly twice the canonical
> Schur-quotient mass.

In that sense, the multiplicity/lift problem is **closed**:

`m_lift := Tr(rho_cell P_A) = 2 Tr(rho_cell P_q) = 1/4`.

What remains open is narrower:

> why the physical boundary pressure equals this lifted worldtube mass.

So this note does **not** close retained Planck. It closes the exact missing
factor of `2` and leaves only the scalar identification law

`p_phys = m_lift`.

## Inputs

This lane uses only already-earned branch-local results:

- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those lanes already fix exactly:

1. the physical coarse selector is the full four-axis worldtube projector

   `P_A = sum_(|eta|=1) P_eta`;

2. the canonical Schur-visible quotient projector is

   `P_q = |t><t| + |s><s|`;

3. the full democratic state is

   `rho_cell = I_16 / 16`;

4. the exact full axis mass is

   `m_axis = Tr(rho_cell P_A) = 1/4`;

5. no proper exact quotient/rooting/reduction preserving the retained
   observable-sector semantics is admissible on the accepted surface.

This note asks whether those inputs already force the missing multiplicity
factor.

## Setup

Work on the exact four-axis carrier

`H_A = span{|t>, |x>, |y>, |z>}`.

Let

`|s> = (|x> + |y> + |z>) / sqrt(3)`.

Let the exact spatial-doublet block be

`E = {a_x |x> + a_y |y> + a_z |z> : a_x + a_y + a_z = 0}`.

Choose any orthonormal basis `|e_1>`, `|e_2>` of `E`, for example

`|e_1> = (|x> - |y>) / sqrt(2)`,

`|e_2> = (|x> + |y> - 2 |z>) / sqrt(6)`.

Define

`P_q = |t><t| + |s><s|`,

`P_E = |e_1><e_1| + |e_2><e_2|`.

Because the four basis vectors `|t>`, `|s>`, `|e_1>`, `|e_2>` are orthonormal
and span `H_A`, one has

`P_A = P_q + P_E`.

## Theorem 1: exact lift decomposition of the full worldtube sector

On the four-axis carrier,

`H_A = H_q (+) E`,

where

- `H_q = span{|t>, |s>}`,
- `E` is the exact spatial `S_3` doublet block.

The corresponding projectors satisfy

- `P_A = P_q + P_E`,
- `P_q P_E = P_E P_q = 0`,
- `rank(P_q) = rank(P_E) = 2`.

### Proof

The decomposition

`H_A = span{|t>} (+) span{|s>} (+) E`

is exactly the `S_3` isotypic decomposition of the axis carrier. The first two
lines give the permutation-blind quotient `H_q`, while `E` is its orthogonal
complement inside the spatial block.

So `P_q` and `P_E` are orthogonal projectors onto complementary rank-2
subspaces, and their sum is the full projector on `H_A`, namely `P_A`.

This is the exact carrier-level origin of the missing multiplicity.

## Theorem 2: the invisible doublet is physical multiplicity, not quotient gauge

Assume:

1. the physical coarse boundary/worldtube selector is exactly `P_A`;
2. the minimal Schur carrier only sees the quotient block `P_q`;
3. no proper exact quotient/reduction of the retained observable sector is
   physically admissible.

Then the invisible doublet block `P_E` cannot be discarded as gauge or
bookkeeping redundancy. It is exact physical multiplicity carried by the full
worldtube sector.

### Reason

By the section-canonical worldtube-selector lane, the physical coarse carrier
is already the full four-axis channel `P_A`, not merely the quotient block
`P_q`.

By the bulk-to-`C^16` intertwiner lane, the minimal Schur route is blind to the
doublet and therefore sees only `P_q`.

If one were to replace the physical carrier `P_A` by the quotient carrier
`P_q`, one would be performing precisely the kind of proper exact reduction
that the retained observable-sector semantics disallow.

So the invisible block `P_E` is not removable redundancy. It is physical
multiplicity that must be counted when lifting from the Schur quotient to the
full worldtube sector.

## Theorem 3: democratic lifting gives the exact factor of `2`

Let

`rho_cell = I_16 / 16`.

Then:

- `Tr(rho_cell P_q) = rank(P_q) / 16 = 2/16 = 1/8`,
- `Tr(rho_cell P_E) = rank(P_E) / 16 = 2/16 = 1/8`,
- `Tr(rho_cell P_A) = rank(P_A) / 16 = 4/16 = 1/4`.

Therefore

`Tr(rho_cell P_A) = Tr(rho_cell P_q) + Tr(rho_cell P_E) = 2 Tr(rho_cell P_q)`.

### Consequence

The exact multiplicity-lift law is

`m_lift := Tr(rho_cell P_A) = 2 Tr(rho_cell P_q) = 1/4`.

So the missing factor is not an added normalization. It is the exact
dimension-two completion of the quotient block inside the full section-canonical
worldtube sector.

## Corollary: the multiplicity/lift problem is closed

The earlier open statement was:

> perhaps the physical quantity is `2 Tr(rho_cell P_q)` rather than
> `Tr(rho_cell P_q)`, but the factor of `2` still needs a theorem.

After Theorems 1 to 3, that factor is no longer a free choice.

It is forced by:

- full section-canonical coarse selector `P_A`,
- exact quotient-visible block `P_q`,
- exact invisible complement `P_E`,
- no-proper-quotient retained semantics,
- democratic full-cell state.

So the multiplicity subproblem is resolved exactly:

`2 = rank(P_A) / rank(P_q) = 4 / 2`.

## What remains open

This note does **not** prove:

`p_phys = Tr(rho_cell P_A)`.

It proves only the carrier-level lift

`Tr(rho_cell P_A) = 2 Tr(rho_cell P_q)`.

So the remaining Planck boundary problem is now one sharp scalar law:

> derive why the physical boundary pressure equals the lifted full worldtube
> mass `m_lift = Tr(rho_cell P_A) = 1/4`.

Equivalently on the action lane:

`nu = lambda_min(L_Sigma) + m_lift = 5/4`.

## Best honest verdict

This lane does not close retained Planck, but it does close one real missing
piece:

- **closed:** exact multiplicity/lift factor
  `Tr(rho_cell P_A) = 2 Tr(rho_cell P_q)`;
- **still open:** scalar identification
  `p_phys = Tr(rho_cell P_A)`.

That is a genuine improvement over the earlier state, where even the factor of
`2` itself had not been derived.
