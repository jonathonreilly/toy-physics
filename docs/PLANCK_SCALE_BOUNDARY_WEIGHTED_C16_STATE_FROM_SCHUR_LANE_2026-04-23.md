# Planck-Scale Boundary Weighted `C^16` State from Schur Lane

**Date:** 2026-04-23  
**Status:** science-only induced-state theorem plus strongest honest occupancy obstruction  
**Audit runner:** `scripts/frontier_planck_boundary_weighted_c16_state_from_schur_lane.py`

## Question

Can the remaining Planck boundary bridge be closed by deriving a **boundary-
induced weighted `C^16` state** from the exact Schur/Perron/transfer data,
rather than fixing the democratic `C^16` state and the `hw=1` sector mass by
hand?

More concretely:

- the section-canonical lane already forces the coarse four-axis worldtube
  projector

  `P_A = P_t + P_x + P_y + P_z`;

- the bulk-to-`C^16` intertwiner lane showed that the minimal Schur carrier
  sees only the 2-dimensional permutation-blind quotient

  `H_q = span{|t>, |s>}`,

  where

  `|s> = (|x> + |y> + |z>) / sqrt(3)`;

- the open problem is whether Schur/Perron data can induce a weighted state on
  the full `C^16` carrier whose coarse sector mass restores the missing
  factor-of-two or even lands directly on the physical pressure target.

The exact remaining question is:

> does the exact time-locked Schur/transfer stack canonically induce a weighted
> full-cell `C^16` state whose coarse sector mass is `1/4`, or does it only
> determine a conditional axis-sector state while leaving the missing
> multiplicity genuinely open?

## Bottom line

The strongest honest result is:

1. the current Schur/Perron stack **does** canonically induce a weighted
   `C^16` state on the coarse four-axis worldtube sector;
2. that induced state is obtained by:

   - passing to the minimal Schur quotient `H_q = span{|t>, |s>}`,
   - taking the normalized heat/Perron state
     `sigma_q(beta; w) = exp(beta (w I - L_Sigma)) / Tr exp(beta (w I - L_Sigma))`,
   - and lifting it equivariantly to the axis sector;

3. on the exact witness

   `L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

   the normalized quotient state is blind to the additive pressure shift
   `w`, and its lifted diagonal axis weights are **always**

   `m_t = 1/2`,
   `m_x = m_y = m_z = 1/6`;

4. so the current Schur/Perron data canonically determine the **conditional**
   weighted axis-sector state, but not the total occupation of that sector
   inside the full 16-state carrier;

5. if one asks for the least-informative full-cell extension consistent with
   that induced axis state, the exact maximum-entropy extension gives full-cell
   axis occupation

   `alpha(beta) = exp(S_axis(beta)) / (12 + exp(S_axis(beta)))`,

   where `S_axis(beta)` is the von Neumann entropy of the induced axis state;

6. because the Schur quotient is only 2-dimensional,

   `S_axis(beta) <= log 2`,

   so

   `alpha(beta) <= 2 / (12 + 2) = 1/7 < 1/4`;

7. in particular, no normalized Schur/Perron-induced weighted `C^16` state on
   the current same-surface grammar can canonically produce coarse sector mass
   `1/4`;

8. exact quarter would require one new multiplicity theorem beyond the current
   Schur/Perron data:

   - either a direct occupation law
     `Tr(rho_16 P_A) = 1/4`,
   - or an equivalent theorem promoting the invisible rank-2 doublet
     multiplicity into physical occupation.

So this lane does not close Planck. It does something more precise:

> the current boundary Schur/Perron stack canonically induces the **shape** of
> the axis-sector state, but not the **amount** of full-cell probability that
> lives on that sector.

That missing amount is exactly the remaining multiplicity/occupation theorem.

## Inputs

This lane uses only already-earned branch-local results:

- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_BULK_TO_C16_INTERTWINER_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_LANE_FULL_ASSUMPTION_STRESS_AUDIT_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_LANE_FULL_ASSUMPTION_STRESS_AUDIT_2026-04-23.md)

What those lanes already fix exactly:

1. the coarse worldtube sector `P_A` is section-canonical;
2. the minimal Schur boundary carrier only sees the quotient
   `H_q = span{|t>, |s>}`;
3. the full-axis democratic mass `1/4` is not faithfully seen by the minimal
   Schur quotient, which only carries `1/8`;
4. the current pressure target is still the additive shift/occupation target;
5. the assumption audit already identified "derive a boundary-induced weighted
   `C^16` state" as one of the best next attacks.

This note executes that attack directly.

## Setup

Write the exact axis carrier as

`H_A = span{|t>, |x>, |y>, |z>}`

and the minimal Schur quotient as

`H_q = span{|t>, |s>}`,

where

`|s> = (|x> + |y> + |z>) / sqrt(3)`.

Let

`V : H_q -> H_A`

be the canonical isometric embedding

`V|t> = |t>`,
`V|s> = |s>`.

Then

`P_q = V V^* = |t><t| + |s><s|`

is exactly the canonical rank-2 permutation-blind quotient from the earlier
intertwiner lane.

On the exact witness, the Schur operator on this quotient is

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

For any inverse-temperature/time parameter `beta >= 0` and additive shift
`w in R`, define the normalized quotient heat/Perron state

`sigma_q(beta; w) := exp(beta (w I - L_Sigma)) / Tr exp(beta (w I - L_Sigma))`.

The induced axis-sector state is then

`rho_A(beta) := V sigma_q(beta; w) V^*`.

This is the most direct normalized weighted `C^16` state the exact Schur route
can induce without introducing extra full-cell data.

## Theorem 1: normalized Schur/Perron states are blind to the additive pressure shift

For every `beta >= 0`,

`sigma_q(beta; w) = exp(-beta L_Sigma) / Tr exp(-beta L_Sigma)`.

### Proof

Because `w I` commutes with `L_Sigma`,

`exp(beta (w I - L_Sigma)) = exp(beta w) exp(-beta L_Sigma)`.

The scalar factor `exp(beta w)` cancels between numerator and denominator.

So the normalized induced state depends only on the Schur carrier
`L_Sigma`, not on the additive pressure shift.

This is already important:

> the exact quarter-closing datum `w = 5/4` from the pressure lane is invisible
> to every normalized Schur/Perron state on the current same-surface grammar.

So a weighted-state derivation can only succeed if the occupation theorem is
already implicit in the normalized Schur data themselves.

## Theorem 2: the exact witness induces a canonical weighted axis state

On the exact witness

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`,

the normalized quotient heat state always has the form

`sigma_q(beta) = [[1/2, c(beta)], [c(beta), 1/2]]`

for some real `c(beta)`, because every function of `L_Sigma` retains equal
diagonal entries.

Therefore the induced axis-sector state

`rho_A(beta) = V sigma_q(beta) V^*`

has exact diagonal primitive weights

`<t|rho_A(beta)|t> = 1/2`,

`<x|rho_A(beta)|x> = <y|rho_A(beta)|y> = <z|rho_A(beta)|z> = 1/6`,

for every `beta >= 0`.

So the current Schur route does canonically induce a weighted axis-sector
distribution:

- the temporal one-hot ray carries one-half of the axis-sector weight;
- each spatial one-hot ray carries one-sixth.

This is not democratic on the four axis rays, but it is fully canonical on the
current same-surface quotient grammar.

### Consequence

The Schur/Perron data fix the **internal shape** of the axis-sector state:

`(1/2, 1/6, 1/6, 1/6)`.

What they do **not** fix is the total full-cell occupation

`alpha := Tr(rho_16 P_A)`.

That is exactly the missing scalar bridge.

## Theorem 3: the canonical no-extra-datum full-cell extension still misses quarter

Decompose the full 16-state carrier as

`H_16 = H_A (+) H_perp`,

with

`dim(H_A) = 4`,
`dim(H_perp) = 12`.

Fix the induced axis-sector state `rho_A(beta)` from Theorem 2.

Among all block states on `H_16` whose restriction to `H_A` is the conditional
state `rho_A(beta)`, the least-informative no-extra-datum choice is the
maximum-entropy extension

`rho_16(beta) = alpha(beta) rho_A(beta) (+) (1 - alpha(beta)) I_12 / 12`,

where `alpha(beta)` is chosen by maximizing the full entropy.

The entropy is

`S_full(alpha) = h(alpha) + alpha S_axis(beta) + (1 - alpha) log 12`,

where

- `h(alpha) = -alpha log alpha - (1 - alpha) log (1 - alpha)`,
- `S_axis(beta) = -Tr(rho_A(beta) log rho_A(beta))`.

Stationarity gives

`alpha(beta) = exp(S_axis(beta)) / (12 + exp(S_axis(beta)))`.

But `rho_A(beta)` is supported on the 2-dimensional quotient image
`V(H_q)`, so

`rank rho_A(beta) <= 2`

and therefore

`S_axis(beta) <= log 2`.

Hence

`alpha(beta) <= 2 / (12 + 2) = 1/7 < 1/4`.

So even the canonical no-extra-datum maximum-entropy extension of the induced
Schur weighted state cannot restore the missing factor or reach exact quarter.

This is the strongest honest obstruction on the weighted-state route:

> Schur/Perron data can determine the conditional axis-sector state, but they
> cannot canonically determine enough full-cell occupation to make
> `Tr(rho_16 P_A) = 1/4`.

## Exact witness endpoints

Two exact limits make the obstruction transparent.

### High-temperature / zero-time endpoint

At `beta = 0`,

`sigma_q(0) = I_2 / 2`.

So

`S_axis(0) = log 2`

and the canonical full-cell maximum-entropy occupation is

`alpha(0) = 2 / 14 = 1/7`.

### Perron / zero-temperature endpoint

As `beta -> +oo`, the normalized quotient state collapses to the Perron
projector of the smallest Schur eigenvalue, so

`S_axis(+oo) = 0`

and

`alpha(+oo) = 1 / 13`.

Thus the whole exact canonical family lies in the narrow interval

`1/13 <= alpha(beta) <= 1/7`,

which stays strictly below quarter.

## Corollary: what quarter would require

To get

`Tr(rho_16 P_A) = 1/4`,

one would need

`alpha = 1/4`.

On the maximum-entropy formula that means

`exp(S_axis) = 4`,

equivalently

`S_axis = log 4`.

But that would require a genuinely rank-4 democratic axis-sector state,
whereas the current Schur/Perron route sees only the rank-2 quotient
`span{|t>, |s>}`.

So exact quarter on this route is equivalent to one new multiplicity theorem:

> promote the invisible rank-2 sector omitted by the minimal Schur quotient
> into physical occupation.

This is the same missing factor-of-two seen on the intertwiner lane, now
re-expressed as an entropy/occupation obstruction.

## Best honest verdict

This lane does **not** close Planck.

What it does close:

1. a canonical Schur-induced weighted `C^16` axis-sector state exists;
2. it is exact and does not need the democratic `C^16` state as an input;
3. it fixes the internal axis-ray weighting
   `(1/2, 1/6, 1/6, 1/6)`;
4. the normalized Schur/Perron route is blind to the additive quarter-closing
   shift;
5. the strongest no-extra-datum full-cell extension of that induced state has
   sector mass at most `1/7`, never `1/4`.

So the remaining scientific target is now very explicit:

> either derive a genuine multiplicity/occupation theorem that lifts the
> Schur-induced quotient state to a full rank-4 axis occupancy,
> or abandon the hope that normalized Schur/Perron data alone can force
> exact Planck quarter on the boundary lane.
