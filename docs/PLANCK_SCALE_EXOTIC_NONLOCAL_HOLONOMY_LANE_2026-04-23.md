# Planck-Scale Exotic / Nonlocal Holonomy Lane

**Date:** 2026-04-23  
**Status:** science-only narrowing / classification note on the surviving
holonomy route  
**Audit runner:** `scripts/frontier_planck_exotic_nonlocal_holonomy_lane.py`

## Question

After ruling out exact conventional `a = l_P` on:

- the resolved-weight linear same-defect `Spin(3)` class, and
- the canonical gauge-invariant same-defect character-deficit class,

could exact Planck still hide in a more exotic **nonlinear** or **nonlocal**
holonomy functional?

## Bottom line

Only in a very narrow and much less canonical sense.

Two broad datum-free subclasses can now be ruled out cleanly:

1. **finite combinatorial nonlocal eigenphase functionals**  
   If the action phase is read from a finite word / tensor / direct-sum
   `Spin(3)` holonomy construction with only combinatorial normalization, then
   the effective coefficient `q_* / eps_*` remains rational. Exact Planck on
   the elementary reduction would require

   `q_* / eps_* = 1 / (8 pi)`,

   so this whole class is impossible.

2. **positive normalized nonlocal aggregates of the canonical local scalar
   deficits**  
   The best local gauge-invariant scalar already has exact floor

   `q_loc,min = 1 - sqrt(2)/2`

   on the minimal cubical defect `eps = pi/2`. Any positive normalized
   internal mean or barycentric aggregate of such local scalars stays above the
   same floor, so it also cannot force exact Planck.

So the surviving holonomy route is now much narrower:

> if exact conventional `a = l_P` is still hiding in a holonomy functional, it
> must come from a **non-extensive**, **non-internal**, or otherwise
> non-canonical reparameterization, or from an infinite / renormalized nonlocal
> object rather than any clean finite same-surface holonomy construction.

That is a real narrowing, even though it is not yet a closure.

## Inputs

This lane uses:

- [PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md](./PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_SPIN3_WEIGHT_HOLONOMY_CLASSIFICATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md](./PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIT_BEARING_CANDIDATE_CLASSIFICATION_THEOREM_2026-04-23.md)

## Exact target on the minimal cubical defect

The elementary reduction already proved

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

On the minimal positive cubical defect

`eps_min = pi/2`,

exact conventional `a = l_P` would require

`q_* = eps_min / (8 pi) = 1/16`,

equivalently

`q_* / eps_* = 1 / (8 pi)`.

That is the exact target any exotic holonomy law must hit.

## Class I: finite combinatorial nonlocal eigenphase functionals

### Setup

Take finitely many same-axis elementary holonomies

`U(eps) in Spin(3)`.

Allow the most obvious nonlocal extensions of the local resolved-weight idea:

- finite products / words of commuting same-axis holonomies;
- finite direct sums and tensor products of finite-dimensional `Spin(3)`
  carriers;
- extraction of a resolved eigenphase on that finite carrier;
- finite combinatorial normalization, such as division by the number of loops,
  by a dimension, or by another rational count.

This is already substantially broader than the one-loop linear class.

### Exact reduction

On any finite-dimensional `Spin(3)` carrier, every resolved weight lies in

`(1/2) Z`.

Tensor products add weights, direct sums take unions of weights, and products
of same-axis holonomies add the corresponding angles. Therefore every resolved
phase coming from a finite word/tensor construction has the form

`q_* = c eps_*`,

with

`c in Q`

after any finite combinatorial normalization.

The reason is simple:

- before normalization, the coefficient is a finite sum of half-integers, hence
  itself in `(1/2) Z`;
- dividing by a finite count or dimension keeps it rational.

But exact conventional Planck would require

`c = 1 / (8 pi)`.

Since `pi` is irrational, `1 / (8 pi) notin Q`.

Therefore:

> no finite combinatorial nonlocal eigenphase functional can force exact
> conventional `a = l_P`.

### What this rules out

This rules out a broad class that still felt "live" after the local no-go
notes:

- averaging resolved eigenphases over several plaquettes;
- taking tensor-product carriers before reading the phase;
- reading one finite multi-loop holonomy word instead of one local loop;
- or any finite mixture of those moves with purely combinatorial normalization.

All such constructions still miss the exact coefficient for the same reason:
they stay on a rational coefficient lattice.

## Class II: positive normalized aggregates of the canonical local scalar classes

The earlier local-holonomy no-go notes already showed:

- the linear resolved-weight class misses exact Planck;
- the best canonical gauge-invariant same-defect scalar on the minimal cubical
  defect has exact lower bound

  `q_loc,min = 1 - sqrt(2)/2 ~= 0.292893`.

But exact Planck at the same defect needs

`q_target = 1/16 = 0.0625`.

So the best local canonical scalar already overshoots by a factor of more than
four.

Now take any finite nonlocal aggregate built from positive local scalar values
`q_1, ..., q_n` satisfying

`q_i >= q_loc,min`,

and require the aggregate to be an **internal mean** or **positive normalized
pooling law**:

- arithmetic mean,
- weighted barycenter with positive weights summing to `1`,
- geometric mean,
- harmonic mean,
- or any other internal mean obeying

  `min_i q_i <= M(q_1, ..., q_n) <= max_i q_i`.

Then automatically

`M(q_1, ..., q_n) >= q_loc,min > 1/16`.

Therefore:

> no positive normalized nonlocal pooling of the canonical local scalar
> deficits can force exact conventional `a = l_P`.

This closes the most natural "nonlocal nonlinear rescue" of the existing local
scalar families. Pooling several overshooting positive local defects never
produces the smaller exact target.

## Combined theorem-level statement

**Theorem (exotic/nonlocal holonomy narrowing).**
Assume the elementary Planck reduction

`a^2 / l_P^2 = 8 pi q_* / eps_*`

on the minimal cubical defect `eps_* = pi/2`.

Then exact conventional `a = l_P` is impossible on each of the following two
broad holonomy subclasses:

1. **finite combinatorial nonlocal eigenphase functionals**, where `q_*` is
   extracted from a finite word / tensor / direct-sum `Spin(3)` holonomy
   construction with only combinatorial normalization;
2. **positive normalized nonlocal aggregates of the canonical local scalar
   deficits**, where the aggregate is an internal mean of local same-defect
   gauge-invariant scalars.

In case (1), `q_* / eps_*` remains rational, while exact Planck would require
`1 / (8 pi)`.  
In case (2), the aggregate remains bounded below by the exact local floor
`1 - sqrt(2)/2`, while exact Planck would require `1/16`.

So the surviving holonomy route, if any, must lie outside both broad datum-free
classes.

## What survives

This note does **not** kill every imaginable holonomy idea.

What still survives is much narrower:

- a **non-internal** nonlinear reparameterization of a local or pooled holonomy
  scalar;
- a holonomy functional that is **not extensive/additive** under finite
  composition;
- an **infinite** or renormalized nonlocal holonomy object rather than a clean
  finite same-surface construction;
- or a route that ceases to be fundamentally holonomy-native and instead
  becomes a boundary-density or information/action theorem.

Those are still logically possible. They are just much less canonical than the
finite datum-free classes treated here.

## What this closes

This closes the loophole:

> maybe exact conventional `a = l_P` is still hiding in an obvious finite
> nonlinear or nonlocal holonomy refinement of the local classes already
> studied.

Answer: not in the two broad classes above.

So the holonomy lane is now much more sharply reduced than before.

## Safe wording

**Can claim**

- finite combinatorial nonlocal eigenphase functionals are ruled out for exact
  conventional `a = l_P`;
- positive normalized nonlocal pooling of the canonical local scalar deficits
  is also ruled out;
- any surviving holonomy route must be far more exotic than the finite,
  datum-free classes already on the table.

**Cannot claim**

- that every nonlinear holonomy functional is dead;
- that exact conventional `a = l_P` has been derived;
- that the boundary-density or information/action routes are closed.
