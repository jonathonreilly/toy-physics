# Planck-Scale Time-Locked Gravitational Transfer-Operator Lane

**Date:** 2026-04-23  
**Status:** science-only third-wave classification theorem / candidate class  
**Audit runner:** `scripts/frontier_planck_timelocked_gravitational_transfer_operator_lane.py`

## Question

After the time-lock theorem

`a_s = c a_t`,

the surviving boundary route is already very narrow:

- not RT/Widom;
- not local curvature density;
- not naive cell counting;
- not finite-state or finite-dimensional algebraic transfer.

What, then, is the strongest honest same-surface class for a future
gravitational boundary transfer operator `T_grav`?

## Bottom line

Time-lock does not derive exact Planck by itself, but it does sharpen the
surviving boundary route into one specific theorem shape:

> any acceptable same-surface gravitational boundary transfer law must be a
> **one-clock positive semigroup on the time-locked boundary worldtube**, and
> if it comes from the admitted discrete `3+1` gravity carrier, its generator
> must be a **collective boundary Schur-complement reduction** of a positive
> one-clock completion of the exact global gravitational operator.

Equivalently, after time-lock the surviving boundary target is no longer best
phrased as

`rho(T_grav) = e^(1/4)`

on an arbitrary weighted transfer matrix.

It is better phrased as:

> derive a canonical collective boundary generator `G_Sigma` on the exact
> time-locked spacetime surface and prove its top pressure is
>
> `p_* := sup spec(G_Sigma) = 1/4`.

Then

`rho(T_grav(1)) = e^(p_*) = e^(1/4)`

follows automatically.

That is a real tightening of the route because the transcendental target is
converted into an additive one-clock generator theorem.

## Inputs

This lane uses only the already narrowed same-surface ingredients:

- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md)
- [PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md)
- [S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md](./S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md)
- [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](./UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)

From these notes we already have:

1. one derived clock on the `3+1` route;
2. exact time-lock
   `a_s = c a_t`;
3. an exact discrete-global gravitational carrier family on `PL S^3 x R`,
   with global operator class
   `K_GR(D) = H_D \otimes Lambda_R`;
4. a boundary-route reduction saying any surviving exact `1/4` theorem must be
   genuinely collective.

## Why time-lock changes the transfer problem

Before time-lock, a boundary transfer problem could still hide one unphysical
anisotropy parameter:

`beta = (c a_t / a_s)^2`.

After time-lock that freedom is gone:

`beta = 1`.

So there is now one exact physical clock step on the spacetime lattice.

That means any same-surface boundary evolution on a boundary worldtube

`W_Sigma = Sigma x Z`

must compose in the one remaining clock variable. The exact structural law is
therefore semigroup composition:

`T_grav(tau_1 + tau_2) = T_grav(tau_1) T_grav(tau_2)`.

On a strongly continuous positive family this is equivalent to

`T_grav(tau) = exp(tau G_Sigma)`

for one generator `G_Sigma`.

This is the first real improvement supplied by time-lock: the boundary route is
not just some weighted transfer matrix with target root `e^(1/4)`. It is a
one-clock generator problem.

## Candidate class from the exact `3+1` gravity carrier

The exact global discrete `3+1` gravity side already carries a one-clock
operator family on `PL S^3 x R`.

To obtain a boundary transfer law from that same surface, split the exact
time-locked carrier degrees of freedom into:

- boundary/worldtube variables `B`;
- interior/bulk variables `I`.

Take any positive one-clock completion of the admitted gravitational carrier,
written on this split as the block operator

`M(D) = [[M_BB, M_BI], [M_IB, M_II]]`

with `M_II > 0`.

Then exact elimination of the interior variables gives the boundary effective
quadratic form with generator

`L_Sigma(D) := M_BB - M_BI M_II^(-1) M_IB`.

This is the canonical Schur-complement reduction of the same-surface
gravitational operator to the boundary worldtube.

This class is attractive for three reasons:

1. it is **same-surface**: no external entropy carrier is introduced;
2. it is **time-locked**: the reduction lives on the one derived clock;
3. it is **collective**: eliminating the bulk generically couples distant
   boundary variables.

So the strongest surviving candidate class is:

`T_grav(tau) = exp(tau G_Sigma(D))`

where `G_Sigma(D)` is the positive semigroup generator associated to a
time-locked boundary Schur reduction of the exact global gravity carrier.

The exact generator normalization remains open. A future same-surface theorem
would have to show either

- `G_Sigma = -L_Sigma + w_Sigma I`,

or an equivalent positivity-improving form, with no imported coefficient.

## Why the reduced carrier is genuinely collective

The surviving boundary route cannot reduce to local geometry. The Schur class
explains exactly why.

Even if the direct boundary block is local or diagonal, bulk elimination
generically creates off-diagonal boundary couplings:

`L_Sigma = M_BB - M_BI M_II^(-1) M_IB`.

The second term is nonlocal on the boundary whenever the interior propagator
`M_II^(-1)` links separated boundary attachments.

So this class is:

- not a local curvature density;
- not naive independent cell counting;
- not the free-fermion RT/Widom class;
- not a finite-memory boundary code.

It is a genuinely collective boundary-worldtube carrier induced by the exact
bulk gravity surface.

### Minimal exact witness

Take the exact rational block family

`M_BB = [[2, 0], [0, 2]]`

`M_BI = [[1, 0], [0, 1]]`

`M_II = [[2, 1], [1, 2]]`.

Then

`M_II^(-1) = (1/3) [[2, -1], [-1, 2]]`

and therefore

`L_Sigma = M_BB - M_BI M_II^(-1) M_IB`
`        = [[4/3, 1/3], [1/3, 4/3]]`.

So a diagonal local boundary block reduces to a dense collective boundary
operator after exact bulk elimination. That is the minimal algebraic witness
for why the surviving transfer class is intrinsically collective.

## Pressure formulation of the exact `1/4` target

The second real gain from time-lock is that the surviving exact Planck target
can be written additively.

If

`T_grav(tau) = exp(tau G_Sigma)`

and the semigroup is positivity-improving on the relevant boundary worldtube
state space, then the leading growth rate is

`p_* := sup spec(G_Sigma)`.

So on one exact time step,

`rho(T_grav(1)) = exp(p_*)`.

The old boundary target

`rho(T_grav(1)) = e^(1/4)`

is therefore exactly equivalent to

`p_* = 1/4`.

This does not close the coefficient. But it does convert the surviving route
from a transcendental Perron-root target into a same-surface additive pressure
target on the time-locked generator.

That is cleaner and more physical.

## The theorem-level statement

**Theorem (Time-locked gravitational transfer-operator classification).**
Assume:

1. the exact derived single-clock `3+1` route;
2. the exact time-lock `a_s = c a_t`;
3. the exact discrete-global gravitational carrier family on `PL S^3 x R`;
4. the earlier boundary reductions ruling out local geometry, RT/Widom, naive
   cell counting, finite-state collective codes, and finite-dimensional
   algebraic transfer carriers.

Then any acceptable surviving same-surface boundary transfer route must satisfy:

1. it lives on the boundary worldtube `W_Sigma = Sigma x Z` of the time-locked
   spacetime surface;
2. it composes in the one exact clock variable and therefore belongs to a
   one-clock semigroup class
   `T_grav(tau) = exp(tau G_Sigma)`;
3. if it is induced from the admitted gravity carrier by exact bulk
   elimination, its effective boundary generator is a Schur-complement
   reduction of a positive one-clock completion of the global gravitational
   operator;
4. this effective boundary generator is generically collective/nonlocal on the
   boundary, even when the bare boundary block is local;
5. exact conventional Planck on this route is equivalent to the additive
   pressure theorem
   `sup spec(G_Sigma) = 1/4`.

So the surviving boundary route is no longer "some weighted transfer matrix."
It is specifically a **time-locked collective boundary semigroup / Schur
pressure theorem**.

## What this closes

This note closes several sloppy formulations of the remaining boundary route.

It is no longer honest to describe the live target as:

- "maybe a different finite transfer matrix lands `e^(1/4)`";
- "maybe some local horizon density becomes collective after all";
- "maybe time does not matter to the boundary coefficient."

After time-lock and the earlier no-gos, the surviving route is much more
specific:

- a one-clock boundary semigroup;
- induced from the same-surface gravity carrier;
- collective by Schur reduction;
- with additive top pressure `1/4`.

## What this does not close

This note does **not** prove:

- the existence of the canonical positive one-clock completion `M(D)`;
- that the required semigroup is positivity-improving on the physical
  boundary-worldtube state space;
- that the exact top pressure really is `1/4`;
- or that the information/action route is dead.

It gives the sharper target class only.

## Safe wording

Safe:

> On the exact time-locked `3+1` surface, the surviving boundary route reduces
> to a one-clock collective boundary semigroup induced by a Schur-complement
> reduction of the same-surface gravity carrier. Exact conventional Planck
> would then amount to the additive pressure theorem
> `sup spec(G_Sigma) = 1/4`.

Not safe:

> We already derived the boundary transfer operator and proved its pressure is
> `1/4`.

## Bottom line

Time-lock still does not give exact Planck.

But it does change the surviving boundary route in one important way:

> the correct target is now a **time-locked collective boundary pressure
> theorem**, not another arbitrary transfer-matrix coefficient hunt.
