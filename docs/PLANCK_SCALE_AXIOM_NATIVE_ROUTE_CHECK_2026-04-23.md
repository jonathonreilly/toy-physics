# Planck-Scale Axiom-Native Route Check

**Date:** 2026-04-23  
**Status:** science-only route audit for the Planck lane  
**Audit runner:** `scripts/frontier_planck_axiom_native_route_check.py`

## Question

Is the current direct worldtube / cell-counting route actually the right place
to seek an axiom-native Planck derivation, or has the branch drifted into a
clever but non-native detour?

## Verdict

**Mostly yes, but with one important correction.**

The current branch is on the **right geometric route**, but the final theorem
should no longer be sought as a boundary-specific packet or pressure law.
It should be sought **one level upstream** as a general primitive-cell
source-free state theorem.

More bluntly:

- the worldtube / cell-counting route is the right place to identify the
  counted object;
- it is **not** the right place to keep hunting for the last theorem as if it
  were a special boundary thermodynamics fact;
- the last native theorem is better stated as:

  > **source-free primitive-cell traciality / no-datum local state selection**
  > on `M_16(C)`.

So the branch should **keep** the current direct route, but it should treat the
remaining gap as a framework-level local-state theorem, not a boundary-scalar
or worldtube-combinatorics theorem.

## Why the current route is still the right backbone

Three major things have now been closed honestly on this branch:

1. the old scalar "boundary pressure" language was stripped away and replaced
   by a direct finite-cell coefficient chain;
2. the elementary counting bridge itself is closed:

   `c_cell(rho) = Tr(rho P_A)`;

3. the factor-of-two issue is closed natively by the full packet lift
   `P_A = P_q + P_E`.

That means the current route is no longer wandering through arbitrary
normalization stories. It has isolated the right local observable:

`P_A`,

the exact minimal one-step worldtube packet on the primitive `C^16` cell.

That is real progress, and it is much more native than the older Schur/free-
energy packaging.

## Why the remaining blocker is not really a boundary theorem anymore

The source-free derivation note now proves that the accepted direct stack leaves
a 7-parameter family of full-cell source-free candidate states.

So after the counting theorem, the only live issue is:

> which state on the primitive one-cell algebra counts as the source-free
> no-datum local state?

That is not specific to:

- boundary pressure,
- Schur reduction,
- or even the worldtube packet itself.

It is a framework-level local-state theorem on the primitive cell algebra.

So if the branch keeps treating the last step as a special Planck-only boundary
coefficient puzzle, it is on the wrong level of description.

## Comparison with the alternative routes

The current direct route is still better than the main alternatives on the
branch.

### 1. Gravity/action unit-map route

This route is still structurally important, but the current admitted family is
blocked by the scale-ray no-go in
[PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md).

So by itself it does not fix the absolute scale.

### 2. Local holonomy / character-deficit routes

These have been sharply boxed out:

- [PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md)

The obvious local `Spin(3)` coefficient classes miss exact conventional
Planck.

### 3. Horizon entropy route

The current admissible carrier family is already reduced negatively; it is not
the clean live place to seek a retained close.

### 4. Information/action route

Still suggestive, but still farther from retained closure than the direct
finite-cell route.

So the direct route remains the best live native route on the branch.

## The correction: move the last theorem upstream

The more native formulation is now:

1. primitive one-cell carrier `C^16`;
2. source-free/no-datum local state theorem on `M_16(C)`;
3. direct counting theorem `c_cell(rho) = Tr(rho P_A)`;
4. exact packet rank `rank(P_A) = 4`;
5. therefore quarter;
6. therefore Planck.

That is cleaner than:

`boundary pressure -> boundary normalization -> quarter`.

And it is also cleaner than:

`packet combinatorics -> maybe special shell symmetry -> quarter`.

The direct theorem candidate in
[PLANCK_SCALE_SOURCE_FREE_LOCAL_AUTOMORPHISM_TRACIALITY_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_AUTOMORPHISM_TRACIALITY_CANDIDATE_2026-04-23.md)
is therefore the right next theorem target.

## Strongest argument in favor of the route

The route has already done the hard reduction work:

- it identified the counted object exactly;
- it eliminated quotient undercounting;
- it eliminated the scalar Schur/free-energy coefficient as the answer;
- it reduced the live gap to a primitive-cell state law.

That is exactly what a good native route should do.

## Strongest argument against the route

The last theorem candidate now looks more like a general local-vacuum theorem
than a Planck-specific theorem. If the framework cannot justify a source-free
tracial state on the primitive cell, then this route will stall permanently no
matter how much more boundary packet machinery is added.

So the route is only right if the branch is willing to shift the final search
target to that more general theorem.

## Honest final read

The current direct worldtube/cell-counting route is **directionally right**,
but only after a level shift:

- keep the direct route for the geometry/counting half;
- stop searching for the final bridge inside boundary-scalar packaging;
- pursue the last theorem as a **primitive-cell source-free traciality**
  theorem.

If that theorem lands, this route is the best candidate for an axiom-native
Planck close on the current branch.

If it does not, the branch should stop calling this close and treat Planck as
still pinned/conditional.

## Safe wording

**Can claim**

- the direct worldtube/cell-counting route is the right surviving geometric
  backbone;
- the last blocker is no longer a special boundary-pressure theorem;
- the most native remaining target is a primitive-cell source-free traciality
  theorem;
- alternative routes are currently more blocked than this one.

**Cannot claim**

- that the branch already has an axiom-native retained Planck derivation;
- that more boundary packet combinatorics alone will finish the lane;
- that the primitive-cell traciality theorem is already part of the accepted
  retained surface.

## Changed files

- `docs/PLANCK_SCALE_AXIOM_NATIVE_ROUTE_CHECK_2026-04-23.md`
- `scripts/frontier_planck_axiom_native_route_check.py`
