# DM Nature Review Audit

**Date:** 2026-04-16  
**Scope:** refreshed DM closure branch on `codex/dm-main-refresh`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Purpose

Record the top-to-bottom internal review status of the refreshed DM closure
package before external review.

This note is intentionally harsher than the working theorem notes. Its job is
to say what is actually airtight today and what still depends on a bounded or
branch-scoped argument.

## What is closed cleanly

The following parts of the chain are now internally closed on the refreshed
branch:

1. exact source/kernel side
2. exact projection law
3. exact equilibrium bookkeeping
4. exact `H_rad(T)` transport side
5. exact PMNS packet localization on the one-sided `N_e` flavored route
6. exact seed-relative effective action from the sole-axiom observable
   principle
7. exact low-action PMNS-assisted closure branch giving
   `eta / eta_obs = 1`

So the branch now has a real end-to-end constructive closure route.

## Nature-grade uniqueness status

The new reduction-exhaustion theorem changes the scope of the old caveat.

What is now closed exactly:

- the PMNS-assisted `N_e` closure problem factors through one exact reduced
  domain, the fixed native `N_e` seed surface
- the active chart is exact and surjective on that surface
- the `eta` map factors exactly through that surface

So the older review question

> do we need a separate theorem about components beyond the exact reduced
> surface?

is now answered **no** for the scoped `N_e` closure claim. There is no larger
admissible PMNS-assisted search space outside that reduced surface.

What is still true:

- the selector theorem on that exact surface is branch-global by constrained
  multistart scan plus finite action-gap separation
- it is not a separate closed-form analytic classification of every stationary
  component on that same surface

## Review verdict

### Working-branch verdict

On the refreshed branch, the DM closure route is complete enough to review as
an end-to-end constructive framework result.

### Nature-grade verdict

If the intended claim is only:

> the PMNS-assisted `N_e` closure problem is fully reduced and internally
> closed on its exact admissible domain,

then the current branch is already strong enough.

If the intended claim is the stronger one:

> the sole axiom `Cl(3)` on `Z^3` forces one unique PMNS-assisted DM closure
> point with no remaining branch-global caveat,

then one more theorem would still strengthen the package:

- either an analytic all-components uniqueness theorem on the fixed `N_e` seed
  surface itself
- or a certified global optimization theorem on that exact surface whose
  hypotheses are proved inside the framework

Without that, the strongest perfectly honest wording is:

> the refreshed branch has an exact effective-action selector and a unique
> lowest-action closure branch on the exact reduced surface under the current
> constrained branch scan.

## Recommendation

For review packaging, do **not** bury this point.

The package is strongest if it says both:

1. the old exact one-flavor `5.297x` miss is gone on the PMNS-assisted closure
   branch
2. the older “beyond the reduced surface” loophole is closed, and the only
   remaining review-sensitive issue is whether the selector branch uniqueness
   on that exact surface should be promoted from branch-scanned to fully
   analytic/global

That is the honest Nature-grade boundary.
