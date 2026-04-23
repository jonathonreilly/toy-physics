# Planck-Scale Bulk/Boundary `C^16` Synthesis Lane

**Date:** 2026-04-23  
**Status:** science-only synthesis reduction theorem / sharp bridge classification  
**Audit runner:** `scripts/frontier_planck_bulk_boundary_c16_synthesis_lane.py`

## Question

The Planck boundary program now has three exact same-surface ingredients:

1. the bulk-induced Schur boundary carrier `L_Sigma`;
2. the canonical non-affine Schur vacuum law

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

3. the canonical `C^16` axis-sector mass

   `m_axis = 1/4`.

The exact remaining question is:

> do these three ingredients synthesize into one theorem that forces the
> physical boundary pressure,
> and if so is that theorem `p_* = p_vac(L_Sigma)`, `p_* = m_axis`, or a
> canonical conversion between them?

## Bottom line

The strongest honest result is a **sharp reduction theorem plus witness-level
no-go**, not a full Planck close.

The current same-surface stack proves:

1. the surviving bulk/action boundary pressure law is

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

2. the Schur boundary action itself forces the canonical vacuum scalar

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

3. the same structural `C^16` carrier that supplies the fine primitive
   one-sixteenth also supplies the coarse exact axis-sector mass

   `m_axis = 4 * (1/16) = 1/4`.

On the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

these give

- `lambda_min(L_Sigma) = 1`,
- `p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`,
- `m_axis = 1/4`.

Therefore:

- `p_vac(L_Sigma) != m_axis`,
- the canonical vacuum identification `p_* = p_vac(L_Sigma)` does **not**
  yield the Planck boundary target,
- the current same-surface synthesis does **not** collapse the structural
  `16`, the Schur vacuum law, and the boundary quarter into one theorem.
- these quantities remain distinct theorems even after the exact
  bulk/boundary/`C^16` reduction.

In plain terms: the current same-surface synthesis does not collapse the
structural `16`, the Schur vacuum law, and the boundary quarter into one
theorem; they remain distinct theorems.

The surviving load-bearing bridge is now explicit:

> if the boundary lane closes on this same-surface stack, it must close by
> the physical identification
>
> `p_* = m_axis`,
>
> equivalently
>
> `nu = lambda_min(L_Sigma) + m_axis`.

So the synthesis lane improves the program by proving exactly which bridge is
still real:

- not `p_* = p_vac`,
- not the canonical action normalizations `nu in {0, p_vac}`,
- but the still-open physical bridge from the bulk Schur carrier to the
  coarse `C^16` axis-sector observable.

## Inputs

This lane uses only already-earned branch-local results:

- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md](./PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)

What those lanes already fix exactly:

1. the canonical Schur witness

   `L_Sigma = [[4/3,1/3],[1/3,4/3]]`;

2. the exact boundary pressure family

   `p_*(nu) = nu - lambda_min(L_Sigma)`;

3. the canonical Schur vacuum density

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

4. the canonical `C^16` fine and coarse scalars

   `m_cell = 1/16`,
   `m_axis = 4 m_cell = 1/4`;

5. the action-side classification

   `nu in {0, p_vac(L_Sigma)}`

   for the current canonical same-surface vacuum normalizations.

This note asks whether those ingredients already synthesize into one forced
Planck theorem.

## Step 1: the synthesis data live on one lane but remain distinct quantities

There are now three exact scalars on the surviving Planck boundary lane.

### 1A. Bulk spectral datum

From exact bulk-to-boundary Schur completion:

`lambda_min(L_Sigma)`.

This is the carrier floor controlling the exact action pressure family

`p_*(nu) = nu - lambda_min(L_Sigma)`.

### 1B. Bulk vacuum datum

From the same Schur boundary action:

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

This is the exact non-affine vacuum density forced by the zero-source Gaussian
boundary action.

### 1C. `C^16` coarse datum

From the democratic `C^16` taste-cell carrier:

`m_cell = 1/16`,

and from the exact `hw=1` axis sector:

`m_axis = 4 m_cell = 1/4`.

This is the canonical `C^16` scalar that matches the surviving boundary
quarter target.

So the synthesis lane is not combining one scalar written three ways. It is
combining three exact same-surface scalars of different types:

- a Schur spectral floor,
- a Schur vacuum density,
- and a coarse `C^16` sector mass.

## Theorem 1: exact synthesis classification

Assume:

1. exact time-locked bulk-to-boundary Schur completion;
2. exact non-affine Schur vacuum law
   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;
3. exact `C^16` democratic carrier with axis-sector mass `m_axis = 1/4`;
4. exact action-native pressure law
   `p_*(nu) = nu - lambda_min(L_Sigma)`.

Then the current same-surface synthesis splits into exactly three candidate
identifications:

1. **vacuum synthesis**

   `p_* = p_vac(L_Sigma)`

   which is equivalent to

   `nu = lambda_min(L_Sigma) + p_vac(L_Sigma)`;

2. **axis synthesis**

   `p_* = m_axis`

   which is equivalent to

   `nu = lambda_min(L_Sigma) + m_axis`;

3. **canonical action normalization**

   `nu in {0, p_vac(L_Sigma)}`

   giving

   `p_* in {-lambda_min(L_Sigma), p_vac(L_Sigma) - lambda_min(L_Sigma)}`.

These are exact consequences of the already-opened lanes.

What the current stack does **not** provide is a theorem identifying

`p_vac(L_Sigma)` and `m_axis`,

or a theorem that converts one into the other canonically.

## Theorem 2: the exact witness rules out vacuum synthesis as Planck closure

On the exact witness

`L_Sigma = [[4/3,1/3],[1/3,4/3]]`,

we have:

`spec(L_Sigma) = {1, 5/3}`,

`lambda_min(L_Sigma) = 1`,

`det(L_Sigma) = 5/3`,

and for rank `n = 2`,

`p_vac(L_Sigma) = (1/4) log(5/3) ~= 0.127706`.

But the exact `C^16` axis-sector mass remains

`m_axis = 1/4`.

Therefore

`p_vac(L_Sigma) != m_axis`.

In particular:

1. the synthesis candidate `p_* = p_vac(L_Sigma)` does **not** yield the
   Planck boundary target `1/4` on the witness;
2. the current Gaussian-vacuum synthesis and the `C^16` quarter-valued axis
   synthesis are inequivalent.

This is the sharpest witness-level no-go now available.

## Theorem 3: the current canonical action normalizations also miss quarter

From the current action-side classification, the canonical same-surface
vacuum normalizations are

`nu_0 = 0`,

`nu_gauss = p_vac(L_Sigma)`.

So the corresponding exact pressures are

`p_*(nu_0) = -lambda_min(L_Sigma)`,

`p_*(nu_gauss) = p_vac(L_Sigma) - lambda_min(L_Sigma)`.

On the witness these are

`p_*(nu_0) = -1`,

`p_*(nu_gauss) = (1/4) log(5/3) - 1`.

Neither equals `1/4`.

So the current canonical action normalizations do not synthesize Planck on the
boundary lane either.

## Corollary: the load-bearing bridge is now unique

Because:

- `p_* = p_vac(L_Sigma)` fails on the witness,
- the canonical action normalizations fail on the witness,
- and `m_axis = 1/4` is still the only exact same-surface scalar already on
  the branch that matches the boundary target,

the surviving same-surface load-bearing bridge is reduced to:

`p_* = m_axis`.

Equivalently:

`nu = lambda_min(L_Sigma) + m_axis`.

On the witness this becomes

`nu = 1 + 1/4 = 5/4`.

So the bulk/boundary/`C^16` synthesis does not close Planck, but it does prove
which bridge is actually load-bearing.

## Theorem 4: no canonical conversion from `p_vac` to `m_axis` is currently supplied

On the witness, the unique scalar factor converting the Schur vacuum density
to the `C^16` axis mass is

`kappa_wit = m_axis / p_vac(L_Sigma) = 1 / log(5/3)`.

This is:

- not equal to `1`,
- not supplied by the current Schur action notes,
- not supplied by the current `C^16` notes,
- and not forced by the current action-side classification.

So any would-be conversion

`m_axis = kappa p_vac(L_Sigma)`

would require a new theorem for `kappa`; it is not already present in the
current same-surface stack.

That is the strongest honest obstruction to the hoped-for synthesis identity.

## Are the structural `16` and boundary quarter now the same theorem?

No.

The exact relationship is:

1. the structural `16` is the full democratic `C^16` carrier

   `16 = 2^4`;

2. the exact coarse `C^16` quarter is the axis-sector mass

   `m_axis = 4 * (1/16) = 1/4`;

3. the boundary quarter is the surviving physical pressure target

   `p_* = 1/4`;

4. the Schur vacuum density is a different exact scalar

   `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

So the structural `16` and boundary quarter are now linked by one exact
carrier-level coarse-graining step, but they still remain distinct theorems.

The branch does **not** currently prove:

- `boundary quarter = structural 16`,
- or `boundary quarter = Schur vacuum law`.

It proves only:

- the exact `C^16` carrier contains the canonical quarter-valued observable;
- the exact Schur boundary action contains a different canonical vacuum law;
- the witness excludes identifying those two scalars by any theorem already on
  the branch.

## What is actually proved

This synthesis lane proves five exact statements.

### Theorem A - Candidate synthesis classification

The current same-surface data reduce the possible synthesis laws to:

- `p_* = p_vac(L_Sigma)`,
- `p_* = m_axis`,
- or the canonical action normalizations `nu in {0, p_vac}`.

### Theorem B - Witness no-go for vacuum synthesis

On the exact witness,

`p_vac(L_Sigma) = (1/4) log(5/3) != 1/4 = m_axis`,

so the vacuum synthesis does not produce the Planck target.

### Theorem C - Witness no-go for canonical action normalizations

The canonical action choices `nu = 0` and `nu = p_vac(L_Sigma)` also fail to
produce quarter.

### Theorem D - Unique surviving load-bearing bridge

The only surviving same-surface bridge already matching the Planck boundary
target is

`p_* = m_axis`,

equivalently

`nu = lambda_min(L_Sigma) + m_axis`.

### Theorem E - Structural `16` and boundary quarter remain distinct

The structural `16`, the coarse `C^16` quarter, the Schur vacuum law, and the
physical boundary quarter are now tightly linked, but they are not yet one and
the same theorem.

## Final verdict

The bulk/boundary/`C^16` synthesis lane does not close Planck.

It does something narrower and important:

> it proves that the real remaining bridge is not the Schur vacuum law and not
> the current canonical action normalizations. The real remaining bridge is
> the physical identification of boundary growth pressure with the coarse
> quarter-valued `C^16` axis-sector observable.

That is the cleanest honest synthesis result currently available on this
program.
