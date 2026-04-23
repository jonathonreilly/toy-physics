# Planck-Scale `C^16` Boundary Pressure Bridge Lane

**Date:** 2026-04-23  
**Status:** science-only reduction theorem / obstruction on the boundary route  
**Audit runner:** `scripts/frontier_planck_c16_boundary_pressure_bridge_lane.py`

## Question

Can the new `C^16` / taste-cell result kill the remaining boundary
normalization ambiguity?

More concretely:

- can the canonical `2^4 = 16` taste-cell carrier supply a same-surface value
  that matches the boundary pressure target
  `p_* = sup spec(G_Sigma) = 1/4`;
- does that make the boundary normalization `16` the **same theorem** as the
  structural `C^16` taste-cell `16`;
- or does it only sharpen the remaining bridge?

## Bottom line

It sharpens the bridge, but it does **not** yet close it.

The exact useful fact is:

- the primitive full-cell share on the democratic `C^16` carrier is
  `m_cell = 1/16`;
- the exact `hw=1` axis sector has four states, so its total democratic mass is
  `m_axis = 4 * (1/16) = 1/4`;
- this `m_axis = 1/4` is the **canonical `C^16` scalar that matches the
  boundary quarter target**.

So the strongest honest reduction is:

> if the physical boundary pressure is read from the `C^16` carrier, it cannot
> be the primitive taste-cell share `1/16`; it has to be the coarse
> `hw=1` axis-sector mass `1/4`.

On the exact Schur witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

the shifted family

`G_w = w I - L_Sigma`

hits the Planck boundary target exactly when

`w = lambda_min(L_Sigma) + m_axis = 1 + 1/4 = 5/4`.

So this lane isolates the exact remaining bridge:

`physical boundary pressure = C^16 axis-sector mass`.

That is stronger than numerology and weaker than full closure.

## Inputs

This lane uses only already-opened branch-local results:

- [PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md](./PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md)

What those lanes already give exactly:

- full democratic `C^16` taste-cell carrier;
- primitive taste-cell share `1/16`;
- exact democratic `hw=1` axis-sector carrier with `2` bits;
- canonical Schur boundary operator `L_Sigma`;
- exact quarter target as a boundary pressure/normalization law;
- exact witness shift requirement `w = 5/4`.

## Step 1: the full `C^16` carrier gives two canonical scalars

Work on the exact four-bit taste-cell basis

`H_cell = span{|eta> : eta in {0,1}^4}`.

Let

`rho_cell = I_16 / 16`

be the canonical democratic full-cell state.

For each primitive taste cell `eta`, define

`P_eta = |eta><eta|`.

Then every primitive cell has exact democratic share

`m_cell := Tr(rho_cell P_eta) = 1/16`.

Now define the exact `hw=1` axis sector

`A = {1000, 0100, 0010, 0001}`

with projector

`P_A = sum_(eta in A) P_eta`.

Then

`m_axis := Tr(rho_cell P_A) = 4/16 = 1/4`.

So the same `C^16` carrier already provides two distinct canonical scalars:

- fine primitive-cell share `m_cell = 1/16`;
- coarse axis-sector mass `m_axis = 1/4`.

## Theorem 1: primitive `1/16` is the wrong boundary value

The surviving boundary pressure target is

`p_* = 1/4`.

Therefore the primitive `C^16` taste-cell share cannot itself be the boundary
pressure:

`m_cell = 1/16 != 1/4 = p_*`.

So if a same-surface `C^16` bridge exists, it cannot read pressure directly
from the fine primitive-cell share.

This is a useful no-go because it kills the naive slogan

`boundary quarter = primitive one-sixteenth`

without reopening any wider ambiguity.

## Theorem 2: the canonical boundary-matching `C^16` scalar is the axis-sector mass

The exact `hw=1` axis-sector mass is

`m_axis = Tr(rho_cell P_A) = 1/4`.

This matches the boundary target **exactly**:

`m_axis = p_* = 1/4`.

So the only canonical `C^16` scalar on this branch that already lands on the
boundary target is the coarse axis-sector mass.

Equivalently:

`p_* = 4 * m_cell`.

This is the first real bridge between the structural `16` and the boundary
quarter:

- the structural `16` gives the fine primitive share `1/16`;
- the exact `3+1` axis reduction sums the four `hw=1` axis cells;
- that coarse same-carrier quantity is exactly `1/4`.

## Theorem 3: on the Schur witness the missing normalization law reduces to one bridge statement

On the exact boundary witness,

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`

has eigenvalues

`1`, `5/3`,

so

`lambda_min(L_Sigma) = 1`.

For the shifted same-eigenspace family

`G_w = w I - L_Sigma`,

the top pressure is

`p_*(w) = w - lambda_min(L_Sigma) = w - 1`.

Quarter therefore requires

`w = 1 + 1/4 = 5/4`.

Using the canonical `C^16` axis-sector mass,

`w = lambda_min(L_Sigma) + m_axis`.

So the exact remaining bridge can now be written in a fully reduced form:

> derive why the physical additive boundary pressure shift equals the
> `C^16` axis-sector mass.

This is the sharpest same-surface reduction now available on the boundary lane.

## Corollary: the bridge is coarse-grained, not fine-grained

Because

`m_axis = 4 * m_cell`,

the surviving bridge is not

`p_* = m_cell`,

but

`p_* = m_axis = 4 m_cell`.

So the boundary target does not identify directly with the fine taste-cell
share. It identifies, if at all, with the exact coarse `3+1` axis-sector
observable cut out of the same `C^16` carrier.

This is scientifically useful because it tells us what kind of future theorem
would count as a real close:

- not a theorem about one primitive cell;
- a theorem about the full four-axis worldtube channel selected from the
  democratic `C^16` carrier.

## Are the two `16`s now the same theorem?

No.

They are now linked by one exact carrier-level reduction, but they are still
not the same theorem.

The distinctions are:

1. **Structural `16`**

   `16 = 2^4`

   from the full four-bit taste-cell carrier.

2. **Boundary quarter**

   `1/4 = 4 * (1/16)`

   from summing the exact four-state `hw=1` axis sector of that carrier.

3. **Defect normalization `16`**

   `a^2 / l_P^2 = 16 q_*`

   from the separate minimal-defect Einstein/Regge coefficient chain.

Exact conventional Planck would make those chains agree numerically on one
lane, but this note does **not** prove they are one and the same theorem.

The strongest honest wording is:

> the structural `C^16` carrier supplies the canonical quarter-valued
> axis-sector observable that could close the boundary normalization problem,
> but the physical identification of boundary pressure with that observable
> remains open.

## What is actually proved

This lane proves four exact statements.

### Theorem A — Primitive share mismatch

The canonical primitive `C^16` taste-cell share is `1/16`, so it cannot equal
the surviving boundary quarter target.

### Theorem B — Canonical boundary-matching observable

The exact `hw=1` axis-sector mass on the same democratic `C^16` carrier is
`1/4`, which matches the boundary target exactly.

### Theorem C — Reduced shift law

On the canonical Schur witness, exact quarter is equivalent to

`w = lambda_min(L_Sigma) + m_axis`.

### Theorem D — Same carrier, not same theorem

The structural `16`, the coarse boundary `1/4`, and the separate
defect-normalization `16` are linked, but not identified, by the current lane.

## What is still open

The remaining gap is now very specific:

> prove that the physical boundary pressure/normalization law reads
> `p_*` from the `C^16` axis-sector mass.

Equivalently:

> prove that the additive boundary shift on the Schur carrier is
> `m_axis = 1/4`.

Without that, the new `C^16` result is not yet a full boundary close. What it
does give is the cleanest exact candidate value and the cleanest exact carrier
for that value.

## Best honest verdict

This lane lands outcome (2):

- **theorem identifying a canonical `C^16` quantity that matches boundary
  quarter:** YES
- **full same-surface derivation that the physical boundary pressure equals that
  quantity:** NOT YET
- **structural `16` and boundary normalization `16` become one theorem:** NO

So the boundary problem is now smaller than before:

- the carrier is fixed;
- the target value is fixed;
- the matching `C^16` observable is fixed;
- the only remaining burden is the physical bridge law
  `p_* = m_axis`.

## Reviewer-safe wording

> On the exact democratic `C^16` taste-cell carrier, each primitive cell has
> share `1/16`, while the exact `hw=1` axis sector has total mass `4/16 = 1/4`.
> Therefore the canonical `C^16` scalar that matches the surviving boundary
> pressure target is not the fine primitive-cell share but the coarse
> axis-sector mass. On the exact Schur witness this reduces the remaining
> normalization problem to one explicit bridge statement:
> the physical boundary pressure equals the `C^16` axis-sector mass. This
> links the structural `2^4 = 16` carrier to the quarter target exactly, but
> it does not yet prove that the structural `16` and the boundary
> normalization are the same theorem.
