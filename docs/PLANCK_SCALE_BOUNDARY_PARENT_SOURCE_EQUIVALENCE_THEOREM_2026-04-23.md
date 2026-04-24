# Planck-Scale Boundary Parent Source Equivalence Theorem

**Date:** 2026-04-23
**Status:** parent-source closure of the Schur/event common-source bridge
**Verifier:** `scripts/frontier_planck_boundary_parent_source_equivalence_theorem.py`

## Question

The current final pressure point is:

> why are the Schur normal-ordered pressure and the primitive event insertion
> source two representations of the same gravitational boundary-action source?

Can that common-source identification be derived from the already retained
boundary carrier structure?

## Result

Yes, on the retained primitive boundary-action object class.

There is a unique parent one-cell gravitational boundary source:

`B_parent := (H_A, P_A)`,

where

`H_A = span{|t>, |x>, |y>, |z>}`,

and

`P_A = |t><t| + |x><x| + |y><y| + |z><z|`.

The event source is the faithful representation of this parent:

`U_A(s) = exp(s P_A)`.

The Schur source is the quotient-shape representation of the same parent:

`H_A = H_q (+) E`,

where

`H_q = span{|t>, |s>}`,

`|s> = (|x> + |y> + |z>) / sqrt(3)`,

and `E` is the spatial doublet complement. The minimal Schur carrier sees the
quotient block `H_q`; no-proper-quotient semantics restores the retained
doublet multiplicity `E`.

Therefore the Schur scalar source is not the quotient-only mass

`Tr(rho_cell P_q) = 1/8`.

It is the multiplicity-completed parent mass

`Tr(rho_cell P_A) = Tr(rho_cell(P_q + P_E)) = 1/4`.

So the Schur normal-ordered pressure and the event insertion generator are two
reductions of one parent source. Same-source covariance is no longer an
independent bridge; it follows from parent-source uniqueness.

## Inputs

This theorem uses already earned statements:

1. the physical one-step boundary/worldtube carrier is the full four-axis
   packet `P_A`;
2. the minimal Schur carrier sees only the permutation-blind quotient
   `P_q = |t><t| + |s><s|`;
3. the full axis carrier decomposes as

   `H_A = H_q (+) E`;

4. the doublet `E` is retained physical multiplicity, not quotient gauge;
5. the source-free cell state is `rho_cell = I_16 / 16`;
6. primitive incidence unit semantics excludes `alpha P_A` with
   `alpha != 1`;
7. no hidden source-free boundary-action scalar excludes additive constants not
   carried by retained primitive incidences.

None of these inputs contains `nu = 5/4`, `a = l_P`, or the desired density.

## Theorem 1: uniqueness of the parent primitive boundary source

An admissible parent one-cell gravitational boundary source must be:

1. local on the primitive boundary event cell;
2. supported on one-step boundary/worldtube incidences;
3. time-complete;
4. spatially isotropic;
5. unit-valued on each retained primitive incidence;
6. free of proper quotienting of retained physical multiplicity.

The only operator satisfying these conditions is

`P_A = P_t + P_x + P_y + P_z`.

### Proof

One-step support restricts the source to the four Hamming-weight-one axis
atoms. Time-completeness includes `P_t`. Spatial isotropy includes the full
spatial orbit `P_x + P_y + P_z`. Unit incidence semantics gives coefficient
one on every included atom. No-proper-quotient semantics prevents replacing
the four-dimensional axis carrier by its two-dimensional permutation-blind
quotient.

Therefore the unique parent source is `P_A`.

## Theorem 2: event reduction is faithful

The faithful event representation of the parent source is the finite
one-parameter insertion group

`U_A(s) = exp(s P_A)`.

The associated normalized generator is

`d/ds log Tr(rho_cell U_A(s))|_(s=0) = Tr(rho_cell P_A)`.

This is the event reduction of the parent source.

## Theorem 3: Schur reduction is quotient shape plus retained multiplicity

The minimal Schur boundary carrier is two-dimensional. Therefore it cannot
faithfully carry the rank-four axis projector `P_A`.

The exact quotient theorem gives the unique permutation-blind quotient

`H_q = span{|t>, |s>}`,

with projector

`P_q = |t><t| + |s><s|`.

The full parent carrier decomposes as

`P_A = P_q + P_E`,

where `P_E` is the projector onto the retained spatial doublet.

Thus the Schur reduction has two parts:

1. quotient **shape** on `H_q`, encoded by the Schur operator `L_Sigma`;
2. retained **multiplicity completion** by `P_E`, required because the parent
   source is `P_A`, not `P_q`.

So the Schur normal-ordered scalar source is the multiplicity-completed parent
source, not the quotient-only source.

## Theorem 4: quotient-only Schur pressure changes the source

Suppose the Schur source were read as `P_q` only.

Then the event source and Schur source would be different parent sources:

`P_A` versus `P_q`.

Their difference is the retained doublet

`P_E = P_A - P_q`.

Since `P_E` is retained physical multiplicity, discarding it is a proper
quotient of the physical boundary source.

Therefore quotient-only Schur pressure is not the same gravitational
boundary-action source. It changes the target.

## Corollary 1: common-source covariance is derived

The event representation and the Schur representation are both reductions of
the same parent source `P_A`:

- event reduction: faithful finite source `exp(s P_A)`;
- Schur reduction: quotient shape `L_Sigma` plus retained multiplicity
  `P_q + P_E = P_A`.

Therefore their scalar infinitesimal generators must agree. If they did not,
the quotient of the two source groups would be a hidden source-free scalar, as
proved by the same-source covariance theorem.

Thus

`p_Schur = p_event`.

## Corollary 2: the additive density is fixed

The Schur normal-ordered pressure is

`p_Schur = nu - lambda_min(L_Sigma)`.

The event Ward derivative is

`p_event = Tr(rho_cell P_A)`.

Parent-source equivalence gives

`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`.

Since `rho_cell = I_16/16` and `rank(P_A)=4`,

`Tr(rho_cell P_A) = 4/16 = 1/4`.

On the rational witness `lambda_min(L_Sigma)=1`, hence

`nu = 5/4`.

## Corollary 3: conventional Planck length

The microscopic boundary density is

`S_micro/k_B = (1/4) A/a^2`.

The standard gravitational area/action density is

`S_grav/k_B = A/(4 l_P^2)`.

Equating the same physical boundary density gives

`a = l_P`.

## Remaining Rejection

The remaining possible rejection is now only upstream:

> deny that the physical gravitational boundary-action source belongs to the
> retained primitive one-step boundary/worldtube object class.

If that denial is made, the reviewer is no longer contesting the coefficient
or the Schur/event common-source bridge. They are rejecting the physical
identification of the Planck lane as the primitive gravitational boundary
action lane.

Within the retained primitive boundary-action object class, the parent source
is unique and the Schur/event equivalence is closed.
