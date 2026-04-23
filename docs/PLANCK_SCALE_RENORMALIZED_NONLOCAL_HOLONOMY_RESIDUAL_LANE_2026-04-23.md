# Planck-Scale Renormalized / Nonlocal Holonomy Residual Lane

**Date:** 2026-04-23  
**Status:** science-only second-wave narrowing / classification note  
**Audit runner:** `scripts/frontier_planck_renormalized_nonlocal_holonomy_residual_lane.py`

## Question

After the first-wave holonomy notes ruled out:

- the resolved-weight linear same-defect `Spin(3)` class;
- the canonical local gauge-invariant character-deficit class;
- finite combinatorial nonlocal eigenphase functionals; and
- positive normalized nonlocal pooling of the canonical local scalars,

could exact conventional `a = l_P` still arise from a more exotic
**renormalized**, **infinite-volume**, or **non-extensive** nonlocal holonomy
object without smuggling in the target coefficient by hand?

## Bottom line

Not cleanly.

On the homogeneous replicated minimal-defect family, the sharp second-wave
residual collapses in two broad ways:

1. **additive / power-law thermodynamic residuals**  
   On exact replicated copies of the same minimal spinorial defect, additive
   holonomy data scales like `N q_loc`. Any power-law renormalization gives
   only three possibilities:
   - `infinity` if the renormalization is too weak,
   - `q_loc = 1 - sqrt(2)/2` if it is exactly extensive,
   - or `0` if it is too strong.  
   Density subtraction kills the residual identically. So this class produces
   no new exact coefficient.

2. **direct-sum spectral / log-determinant residuals**  
   For the replicated minimal holonomy block `U_min^(⊕ N)`, the normalized
   spectral generator is exactly

   `g(z) = -(1/N) log det(I - z U_min^(⊕ N)) = -log(1 - sqrt(2) z + z^2)`,

   independent of `N`. So the infinite-volume / renormalized limit again adds
   no new coefficient; it just repackages the same one-loop holonomy data.
   Exact conventional Planck can be hit only by choosing a special evaluation
   point `z = z_*` satisfying `g(z_*) = 1/16`, and that `z_*` explicitly
   contains the target coefficient.

So the residual holonomy lane is now much sharper:

> renormalization by itself does not generate the missing exact coefficient.
> On the clean replicated-family test, it either collapses to `0`, to the same
> old overshooting local constant, or to a one-parameter spectral family whose
> exact hit is just tuned evaluation.

That is a real no-go/classification result, even though it is not a universal
impossibility theorem over every conceivable infinite object.

## Inputs

This lane uses:

- [PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md](./PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_EXOTIC_NONLOCAL_HOLONOMY_LANE_2026-04-23.md](./PLANCK_SCALE_EXOTIC_NONLOCAL_HOLONOMY_LANE_2026-04-23.md)

## Exact target and the homogeneous replicated test family

The elementary same-process reduction already isolated the exact target:

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

On the minimal positive cubical defect,

`eps_* = pi/2`,

exact conventional `a = l_P` requires

`q_* = eps_* / (8 pi) = 1/16`.

Now take the homogeneous replicated minimal spinorial family:

- one minimal local holonomy block `U_min` with defect `eps_* = pi/2`;
- eigenvalues `exp(+- i pi/4)`;
- canonical local scalar deficit

  `q_loc = 1 - sqrt(2)/2`.

Replicate this exact block `N` times with no extra datum. This is the cleanest
thermodynamic-limit test for any renormalized nonlocal holonomy proposal,
because all large-volume structure is present while the one-block holonomy data
stays exact and controlled.

## Class I: additive and power-law thermodynamic residuals

Suppose the nonlocal holonomy observable is additive on disjoint identical
blocks:

`F_N = N q_loc`.

Now allow the most obvious renormalized / non-extensive scalings:

`R_alpha(N) = N^(-alpha) F_N = N^(1-alpha) q_loc`.

Then:

- if `alpha < 1`, `R_alpha(N) -> infinity`;
- if `alpha = 1`, `R_alpha(N) -> q_loc = 1 - sqrt(2)/2`;
- if `alpha > 1`, `R_alpha(N) -> 0`.

So power-law renormalization on the exact replicated family produces no new
finite nonzero coefficient besides the already-known overshooting local value
`q_loc`.

The same is true for density subtraction. If one subtracts the exact intensive
density from the extensive quantity,

`F_N - N q_loc = 0`

identically for every `N`.

Therefore:

> additive / power-law renormalized residuals do not generate a clean new
> target on the homogeneous replicated family. They yield only `infinity`,
> `q_loc`, or `0`.

To force the exact Planck target on this class, one would have to insert an
extra conversion constant

`C = (1/16) / q_loc = 1 / (16 - 8 sqrt(2))`,

so that `C q_loc = 1/16`.

But that constant is not produced by the additive replicated holonomy data
itself. It is exactly the missing coefficient in a new disguise.

## Class II: direct-sum spectral / log-determinant residuals

The most natural genuinely infinite / renormalized nonlocal holonomy object is
not a raw sum but a spectral generator. On the exact replicated block family,
take

`U_N = U_min^(⊕ N)`.

Then for the normalized direct-sum log-determinant generator,

`g_N(z) = -(1/N) log det(I - z U_N)`,

one gets the exact factorization

`det(I - z U_N) = det(I - z U_min)^N`.

Therefore

`g_N(z) = -log det(I - z U_min)`.

For the minimal spinorial defect with eigenvalues `exp(+- i pi/4)`,

`det(I - z U_min) = (1 - z e^(i pi/4))(1 - z e^(-i pi/4))`

and hence

`g_N(z) = g(z) = -log(1 - sqrt(2) z + z^2)`,

exactly independent of `N`.

So the renormalized / infinite-volume spectral limit contributes no new
coefficient whatsoever. It collapses to a one-parameter analytic function of
the same one-loop holonomy data.

### Why this still does not close exact Planck

The target is

`q_target = 1/16`.

On this spectral class:

- `g(0) = 0`;
- `g'(0) = sqrt(2)`;
- `g(1) = -log(2 - sqrt(2)) > 1/16`.

So the family does pass through the target range, and by continuity there is a
real `z_* in (0, 1)` with

`g(z_*) = 1/16`.

But solving that equation gives

`z_* = (sqrt(2) +- sqrt(4 e^(-1/16) - 2)) / 2`.

So the exact evaluation point already contains `e^(-1/16)`, i.e. the target
coefficient itself.

This means:

> the direct-sum spectral family can reproduce the target only by choosing a
> tuned evaluation point that already encodes the answer.

That is not a clean datum-free derivation. It is a reparameterization of the
target.

## Combined theorem-level statement

**Theorem (renormalized nonlocal holonomy residual classification on the
homogeneous replicated family).**  
Assume the elementary Planck reduction

`a^2 / l_P^2 = 8 pi q_* / eps_*`

on the minimal cubical defect `eps_* = pi/2`, and test the residual holonomy
route on the homogeneous replicated minimal spinorial family with local scalar

`q_loc = 1 - sqrt(2)/2`.

Then:

1. any additive / power-law renormalized thermodynamic residual yields only
   `infinity`, `q_loc`, or `0`, and density subtraction gives zero exactly;
2. the normalized direct-sum spectral / log-determinant class collapses
   exactly to the one-loop function

   `g(z) = -log(1 - sqrt(2) z + z^2)`,

   independent of the replication parameter `N`;
3. exact Planck on this spectral class requires a tuned evaluation point
   `z = z_*` whose exact formula already contains the target coefficient.

Consequently no clean datum-free renormalized / infinite direct-sum holonomy
residual on this replicated-family test derives exact conventional `a = l_P`.

## What this closes

This closes the cleanest remaining second-wave loophole on the holonomy side:

> maybe a thermodynamic or renormalized holonomy residual produces the missing
> exact coefficient even though every finite local or finite nonlocal class
> misses it.

Answer:

- not on additive/power-law replicated residuals;
- not on normalized direct-sum spectral/log-determinant residuals.

Renormalization alone does not create the missing coefficient.

## What survives

This note still does **not** prove that every imaginable infinite holonomy
object is dead.

What survives is much narrower and much less clean:

- a non-direct-sum infinite object with extra global structure;
- a renormalization prescription whose evaluation point is fixed by a new
  theorem not internal to the holonomy lane;
- or a route that is no longer fundamentally holonomy-native and instead
  becomes a collective gravitational boundary-density or information/action
  theorem.

At that point, the work is effectively leaving the clean holonomy lane anyway.

## Safe wording

**Can claim**

- additive/power-law thermodynamic residuals on the homogeneous replicated
  minimal-defect family give only `infinity`, `q_loc`, or `0`;
- density subtraction kills the additive residual exactly;
- normalized direct-sum spectral/log-determinant renormalization collapses to
  the one-loop function `g(z) = -log(1 - sqrt(2) z + z^2)`;
- exact conventional `a = l_P` on that spectral class requires a tuned
  evaluation point that already encodes the target coefficient;
- the clean renormalized nonlocal holonomy residual lane is therefore sharply
  narrowed, not closed.

**Cannot claim**

- that every conceivable infinite or renormalized holonomy construction is
  universally impossible;
- that exact conventional `a = l_P` has been derived from renormalized
  holonomy;
- that the surviving Planck program no longer needs the boundary-density or
  information/action lanes.
