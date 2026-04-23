# Planck-Scale Non-Schur Axis Occupation Law Lane

**Date:** 2026-04-23  
**Status:** science-only exact classification theorem plus sharpest non-Schur close candidate  
**Audit runner:** `scripts/frontier_planck_non_schur_axis_occupation_law_lane.py`

## Question

The boundary Planck route is now reduced to one last scalar statement:

`p_phys = Tr(rho_cell P_A)`,

where:

- `P_A` is the already-forced coarse four-axis `hw=1` worldtube packet;
- the factor-of-two lift from the Schur-visible quotient to the full packet is
  already exact;
- the current normalized Schur/Perron stack still does **not** supply total
  packet occupation `1/4`.

So the remaining question is:

> can one derive a native **non-Schur** occupation law on the full physical
> time-locked `C^16` cell that forces
>
> `alpha := Tr(rho_cell P_A) = 1/4`,
>
> or is quarter still one extra imported datum?

## Bottom line

The strongest honest result is an exact **classification plus reduction**
theorem on the full physical cell.

1. On the exact time-locked four-bit cell, the current non-Schur source-free
   data do **not** force the democratic state.
2. What they do force is a finite orbit classification:

   - after time-lock, the residual exact symmetry is spatial permutation
     `S_3`, not full transitivity on all sixteen cells;
   - every diagonal `S_3`-invariant occupation law is classified by **eight
     orbit weights**
     `a_(t,w)`, one for each pair
     `(t,w) in {0,1} x {0,1,2,3}`,
     where `t = eta_t` and
     `w = eta_x + eta_y + eta_z`;
   - the forced packet occupation is therefore

     `alpha = a_(1,0) + 3 a_(0,1)`.

3. The normalized Schur/Perron lane fixes only the **shape inside** the packet:

   `a_(1,0) = alpha / 2`,
   `a_(0,1) = alpha / 6`,

   equivalently the internal axis weights are always

   `(1/2, 1/6, 1/6, 1/6)`,

   but the total packet occupation `alpha` remains free.

4. So quarter is not hidden in the current Schur data, and it is not forced by
   time-lock plus residual spatial isotropy alone.

5. The sharpest exact close candidate is one stronger non-Schur principle:

   > source-free full-cell occupation is invariant under the full four-bit
   > local flip group `G_4 ~= (Z_2)^4`.

6. Under that additional principle the occupation law is uniquely

   `rho_cell = I_16 / 16`,

   hence

   `alpha = Tr(rho_cell P_A) = 4 / 16 = 1/4`.

So this lane does **not** close Planck unconditionally. It does something more
useful:

> it identifies the exact remaining obstruction on the non-Schur route:
> current accepted data classify full-cell occupation only up to eight orbit
> weights, and exact quarter follows iff one adds a new full-cell
> shell-mixing / flip-transitivity principle.

This is stronger and cleaner than the older endpoint `p_phys = Tr(rho_cell
P_A)`, because it says exactly what is already forced and exactly what is not.

## Inputs

This lane uses:

- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md](./PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those inputs already fix:

1. the physical coarse worldtube packet is the full four-axis projector
   `P_A`;
2. the missing factor-of-two lift from the Schur quotient to the full packet is
   already exact:

   `P_A = P_q + P_E`,
   `Tr(rho_cell P_A) = 2 Tr(rho_cell P_q) = 1/4`;

3. the normalized Schur/Perron lane fixes only the **conditional** axis-sector
   shape and its canonical no-extra-datum extension still satisfies

   `1/13 <= alpha <= 1/7 < 1/4`;

4. the exact `C^16` cell carrier has a canonical democratic state
   `I_16 / 16`, but this route still needs to explain why that state should be
   physically read;
5. spatial cube flips are already exact native taste operations on the
   three-bit cube carrier.

This note asks what the current non-Schur route really forces on the full
time-locked four-bit cell.

## Setup

Work on the exact four-bit cell basis

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`.

Let:

- `P_eta = |eta><eta|`,
- `w_s(eta) = eta_x + eta_y + eta_z`,
- `A = {eta : |eta| = 1}`,
- `P_A = sum_(eta in A) P_eta`.

After time-lock, one temporal bit is distinguished, while the residual exact
symmetry still permutes the three spatial bits. So the exact residual group on
the primitive cell labels is

`G_res = S_3`,

acting only on `(eta_x, eta_y, eta_z)`.

Its orbits are classified by the pair

`(t,w) = (eta_t, w_s(eta)) in {0,1} x {0,1,2,3}`.

There are therefore exactly eight residual orbit classes.

## Definition: current non-Schur source-free occupation law

Call a full-cell occupation state `rho` **currently admissible on the non-Schur
route** if:

1. it is diagonal on the primitive cell projectors `P_eta`;
2. it is normalized and positive;
3. it is invariant under the exact residual group `G_res = S_3`.

This is intentionally the weakest honest full-cell occupation grammar
compatible with the current time-locked boundary lane. It does **not** assume a
new shell-mixing or full-cell transitivity law.

## Theorem 1: exact classification of current non-Schur occupation laws

Every currently admissible occupation state has the form

`rho = sum_(t=0)^1 sum_(w=0)^3 a_(t,w) Pi_(t,w)`,

where:

- `a_(t,w) >= 0`,
- `Pi_(t,w)` is the projector onto the residual orbit
  `{eta : eta_t = t, w_s(eta) = w}`,
- and normalization is

  `sum_(t,w) binom(3,w) a_(t,w) = 1`.

### Proof

Diagonality means

`rho = sum_eta p(eta) P_eta`.

Residual `S_3` invariance means

`p(eta) = p(sigma eta)`

for every spatial permutation `sigma`.

Therefore `p(eta)` can depend only on the residual orbit data `(eta_t,w_s)`.
So there are exactly eight orbit weights `a_(t,w)`, one for each pair
`(t,w) in {0,1} x {0,1,2,3}`.

The orbit `(t,w)` contains exactly `binom(3,w)` states, hence normalization is

`sum_(t,w) binom(3,w) a_(t,w) = 1`.

This is the complete classification.

## Corollary 1: the forced packet occupation is not fixed by current data

The already-forced coarse packet `P_A` consists of:

- one temporal one-hot state with orbit label `(1,0)`,
- three spatial one-hot states with orbit label `(0,1)`.

Therefore every currently admissible full-cell occupation law gives

`alpha := Tr(rho P_A) = a_(1,0) + 3 a_(0,1)`.

So the current non-Schur route does **not** yet fix `alpha`.

This is the exact remaining obstruction in occupation-language.

## Theorem 2: normalized Schur/Perron data fix only the packet shape

The weighted-`C^16` state lane already proves that normalized Schur/Perron data
fix the conditional axis-sector weights to

`(1/2, 1/6, 1/6, 1/6)`.

Equivalently, on the current orbit classification,

`a_(1,0) = alpha / 2`,
`a_(0,1) = alpha / 6`,

with `alpha = a_(1,0) + 3 a_(0,1)`.

So the Schur data determine the **shape inside** `P_A`, but not its total
occupation.

### Consequence

The current normalized Schur stack can tell us:

- how the packet mass splits between the temporal and spatial one-hot rays;

but it cannot tell us:

- how much full-cell probability lives on the packet in the first place.

That is why the weighted Schur lane still stays below quarter.

## Step 3: the strongest exact close candidate

The present classification makes the next move unambiguous.

If one strengthens the occupation law by requiring invariance under the full
four-bit local flip group

`G_4 = {X_g : X_g |eta> = |eta xor g|, g in {0,1}^4} ~= (Z_2)^4`,

then the action is transitive on the sixteen primitive cells, so every cell has
equal occupation.

This collapses the eight-orbit family to the unique state

`rho_cell = I_16 / 16`.

Then automatically

`alpha = Tr(rho_cell P_A) = 4 / 16 = 1/4`.

## Theorem 3: full flip-transitivity forces exact quarter

Assume:

1. the physical coarse selector is the already-forced projector `P_A`;
2. the source-free full-cell occupation law is invariant under the full
   four-bit flip group `G_4`.

Then the full-cell occupation state is uniquely

`rho_cell = I_16 / 16`,

and the packet occupation is exactly

`alpha = Tr(rho_cell P_A) = 1/4`.

### Proof

The `G_4` action is transitive on `{0,1}^4`, since

`X_(eta xor xi) |eta> = |xi>`.

So every primitive probability is equal to one common constant `c`.
Normalization gives `16 c = 1`, hence `c = 1/16`.

The packet `P_A` has rank `4`, so

`alpha = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

## Why this is not yet a retained close

This theorem is exact, but the new principle is stronger than what the current
lane has already earned.

- The site-phase / cube-shift note gives an exact native `Z_2^3` flip algebra
  on the three-bit taste cube.
- Time-lock gives the derived fourth bit and the exact `3+1` split.
- But the current accepted stack does **not** yet prove that source-free
  occupation on the full time-locked four-bit cell is invariant under the full
  shell-mixing group `G_4`.

So the remaining non-Schur burden is no longer a floating coefficient. It is
one clean physical principle:

> does the derived temporal bit participate in the same source-free local
> flip-equivalence as the three spatial taste bits?

If yes, quarter follows exactly. If not, the current route remains open with
eight orbit weights.

## Corollary: exact boundary quarter under the new occupation law

If physical boundary pressure is read as the occupation of the forced coarse
worldtube packet on the full-cell state from Theorem 3, then

`p_phys = alpha = Tr((I_16 / 16) P_A) = 1/4`.

On the action lane this is equivalent to

`delta = 1/4`,
`nu = lambda_min(L_Sigma) + 1/4 = 5/4`

on the canonical witness.

## Honest endpoint

The strongest honest result is now:

1. current accepted non-Schur data classify full-cell occupation by eight orbit
   weights and therefore leave `alpha` genuinely open;
2. normalized Schur/Perron data fix only the internal packet shape;
3. exact quarter follows from one stronger full-cell principle, namely full
   four-bit flip-transitivity of the source-free occupation law.

So this lane does not yet give unconditional native Planck closure.
It gives the sharpest exact reduction currently available:

> the non-Schur route is open by one shell-mixing / full-cell transitivity law,
> not by a mysterious missing coefficient.
