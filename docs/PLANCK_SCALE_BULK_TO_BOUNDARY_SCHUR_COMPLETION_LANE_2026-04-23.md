# Planck-Scale Bulk-to-Boundary Schur Completion Lane

**Date:** 2026-04-23  
**Status:** science-only fourth-wave theorem / obstruction on the boundary route  
**Audit runner:** `scripts/frontier_planck_bulk_to_boundary_schur_completion_lane.py`

## Question

The time-locked boundary program is already narrowed to a collective
bulk-induced carrier on the exact `3+1` surface.

So the right next question is:

> if the boundary carrier is obtained by exact bulk elimination on the
> time-locked spacetime surface, what is actually forced?

More concretely:

- is the boundary law really forced to be a Schur-complement reduction?
- is positivity forced?
- is a positivity-preserving one-clock transfer normalization forced?
- can this kill the remaining scale freedom and force exact conventional
  `a = l_P`?

## Bottom line

Partly, but not all the way.

Exact bulk elimination on the time-locked spacetime carrier **does** force:

1. an exact quadratic boundary/worldtube action on the Schur-complement
   operator

   `L_Sigma = M_BB - M_BI M_II^(-1) M_IB`;

2. positivity of that quadratic boundary form whenever the completed bulk
   operator is positive;
3. genuine collective/nonlocal boundary coupling after bulk elimination, even
   if the bare boundary block is local.

But exact bulk elimination does **not** force:

1. the sign with which `L_Sigma` enters a physical one-clock transfer
   generator;
2. the additive normalization / pressure offset of that generator;
3. the exact quarter-pressure coefficient;
4. or the final Planck anchor.

So this lane closes the **carrier** much more sharply than before, but it does
not close the **coefficient**.

The strongest honest verdict is:

> the exact time-locked boundary route is forced into a positive
> bulk-to-boundary Schur-complement carrier class, but Schur completion alone
> still leaves a one-parameter normalization obstruction. Therefore it does
> not yet kill the remaining scale freedom.

## Inputs

This lane uses only already-opened Planck structures:

- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md)
- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](./UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
- [S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md](./S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md)
- [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](./OH_SCHUR_BOUNDARY_ACTION_NOTE.md)

The lane imports no external continuum theorem.

## Setup

Work on the exact time-locked spacetime surface, so there is one derived clock
and

`a_s = c a_t`.

Let `B` denote boundary/worldtube variables and `I` denote interior/bulk
variables on a fixed boundary worldtube `W_Sigma = Sigma x Z`.

Assume the exact same-surface completed quadratic carrier is represented on
`B (+) I` by a positive symmetric block operator

`M = [[M_BB, M_BI], [M_IB, M_II]]`

with

`M_IB = M_BI^T`,

and with strictly positive interior block

`M_II > 0`.

Then the quadratic action is

`Q(b,i) = 1/2 [b,i]^T M [b,i]`.

The exact bulk-eliminated boundary operator is the Schur complement

`L_Sigma := M_BB - M_BI M_II^(-1) M_IB`.

## Theorem 1: bulk elimination forces the Schur boundary action

For every boundary configuration `b`,

`Q(b,i)`
`= 1/2 (i + M_II^(-1) M_IB b)^T M_II (i + M_II^(-1) M_IB b)`
`  + 1/2 b^T L_Sigma b`.

Therefore the exact interior minimizer is

`i_*(b) = - M_II^(-1) M_IB b`,

and the exact effective boundary action is

`Q_eff(b) = min_i Q(b,i) = 1/2 b^T L_Sigma b`.

So on the admitted time-locked surface the bulk-to-boundary reduction is not a
heuristic packaging. It is the exact Schur-complement pushforward of the same
quadratic bulk carrier.

This is the exact analogue of the older microscopic shell Schur theorem, but
now phrased on the Planck boundary lane.

## Theorem 2: positivity of the quadratic boundary carrier is forced

Because `M_II > 0`, the completion-of-squares identity above implies

`Q_eff(b) = min_i Q(b,i) >= 0`

whenever `M >= 0`.

So:

- if the completed bulk carrier is positive semidefinite, then
  `L_Sigma >= 0`;
- if the completed bulk carrier is positive definite, then
  `L_Sigma > 0`.

This is the strongest exact positivity statement that bulk elimination really
forces.

What it does **not** force is a positive semigroup on a chosen cone. That is a
different dynamical statement.

## Theorem 3: collectivity is forced generically by bulk elimination

Even if the bare boundary block `M_BB` is local or diagonal, the Schur term

`M_BI M_II^(-1) M_IB`

generically creates dense boundary couplings.

So once the boundary carrier is induced from exact bulk elimination, the
surviving route is no longer honestly describable as local horizon density or
independent cell counting. Collectivity is not a later embellishment. It is
forced by the bulk propagator.

### Minimal exact witness

Take

`M_BB = [[2, 0], [0, 2]]`

`M_BI = [[1, 0], [0, 1]]`

`M_II = [[2, 1], [1, 2]]`.

Then

`M_II^(-1) = (1/3) [[2, -1], [-1, 2]]`,

and therefore

`L_Sigma = [[4/3, 1/3], [1/3, 4/3]]`.

So a diagonal local boundary block reduces to a dense positive collective
boundary operator after exact bulk elimination.

## Theorem 4: Schur completion does not force transfer positivity or the quarter coefficient

Bulk elimination produces the quadratic carrier `L_Sigma`, but not yet the
physical dynamical identification.

There are still at least two unresolved moves:

1. **sign / cone choice**

   The quadratic carrier itself does not decide whether the physical one-clock
   generator is of growth type, decay type, resolvent type, or another
   positivity-improving transform of `L_Sigma`.

   On the exact witness above:

   - `L_Sigma` has positive off-diagonal entries, so it is compatible with a
     standard Metzler-style growth generator;
   - `-L_Sigma` has negative off-diagonal entries, so it is not.

   Bulk elimination gives `L_Sigma`; it does not decide that physical transfer
   must use `+L_Sigma` rather than `-L_Sigma` or another same-eigenspace
   transform.

2. **additive normalization**

   Even after a sign choice, any candidate generator family

   `G_w := G_0 + w I`

   has exactly the same eigenspaces and shifts the top pressure by

   `p_*(w) = p_*(0) + w`.

   Therefore the exact quarter target

   `p_* = 1/4`

   is not forced by Schur completion alone. It is equivalent to fixing one
   remaining normalization constant `w`.

This is the sharpest current obstruction on the bulk-to-boundary lane.

## Theorem 5: Schur completion preserves the scale ray

Suppose the completed same-surface bulk carrier still inherits the current
gravity/action homogeneity:

`M(lambda) = kappa(lambda) M(1)`,

for some positive homogeneous factor `kappa(lambda)`.

Then its Schur complement scales by the same factor:

`L_Sigma(lambda)`
`= M_BB(lambda) - M_BI(lambda) M_II(lambda)^(-1) M_IB(lambda)`
`= kappa(lambda) L_Sigma(1)`.

So Schur completion by itself does **not** create a non-homogeneous unit
anchor. It preserves the scale-ray structure of the underlying bulk family.

There are then only two ways left to break the ray:

1. derive a new same-surface normalization principle that fixes the additive
   pressure offset;
2. derive a genuinely non-homogeneous bulk completion, not just its Schur
   pushforward.

Without one of those, exact conventional `a = l_P` does not follow.

## The theorem-level statement

**Theorem (Bulk-to-boundary Schur completion classification / obstruction).**
Assume:

1. the exact time-locked `3+1` spacetime surface;
2. a positive same-surface quadratic bulk completion on boundary-plus-interior
   degrees of freedom with strictly positive interior block;
3. exact boundary reduction by bulk elimination.

Then:

1. the exact effective boundary/worldtube action is forced to be the Schur
   quadratic form
   `Q_eff(b) = 1/2 b^T L_Sigma b`;
2. positivity of the quadratic boundary carrier is forced from positivity of
   the bulk completion;
3. collectivity/nonlocality of the boundary carrier is generically forced by
   the Schur term;
4. but neither transfer-generator sign, nor positivity-preserving cone, nor
   additive pressure normalization is fixed by Schur completion alone;
5. if the bulk completion remains homogeneous on the current unit-map ray,
   then the Schur boundary carrier remains homogeneous as well;
6. therefore the bulk-to-boundary Schur completion lane does **not** by itself
   kill the remaining scale freedom or derive exact conventional
   `a = l_P`.

Equivalently: the lane now closes the exact boundary **carrier class**, but the
live open step is the **normalization law** that would turn that carrier into
the quarter-pressure theorem.

## What this closes

This note closes several weaker or sloppier readings of the surviving boundary
route.

Closed:

- "maybe collectivity is optional"
- "maybe exact bulk elimination is not really forcing the boundary carrier"
- "maybe positivity of the boundary quadratic form is still open"

Not closed:

- "the physical one-clock transfer generator is now fully derived"
- "the exact quarter coefficient follows automatically from Schur completion"
- "the remaining scale freedom is gone"

## Safe wording

Safe:

> On the exact time-locked spacetime surface, exact bulk elimination forces a
> positive collective Schur-complement boundary carrier. What remains open is
> the normalization law that turns that carrier into the physical
> quarter-pressure theorem.

Not safe:

> The bulk-to-boundary Schur reduction already proves exact conventional
> `a = l_P`.

## Bottom line

The boundary route is now cleaner:

- exact Schur carrier: yes
- forced quadratic positivity: yes
- forced collectivity: yes
- forced quarter coefficient: no
- forced Planck anchor: no

The missing theorem is no longer vague. It is:

> derive the same-surface normalization law that fixes the physical pressure of
> the Schur boundary carrier, instead of leaving it free up to additive shift.
