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

## The one remaining Nature-grade caveat

The last selector theorem on the PMNS-assisted `N_e` route is currently
**branch-global by constrained multistart scan**, not by a separate analytic
classification of all stationary components on the fixed seed surface.

More precisely:

- the relative-action theorem is exact at the effective-action reduction level
- the selector theorem finds exactly two stationary closure branches on the
  fixed native `N_e` seed surface under the current multistart constrained scan
- one branch has strictly lower action and gives exact closure

That is a strong branch-level result, but it is not the same thing as:

> a closed-form analytic uniqueness theorem proving that no additional
> disconnected stationary closure components exist anywhere on the full exact
> seed surface beyond those found by the constrained scan.

## Review verdict

### Working-branch verdict

On the refreshed branch, the DM closure route is complete enough to review as
an end-to-end constructive framework result.

### Nature-grade verdict

If the intended claim is:

> the sole axiom `Cl(3)` on `Z^3` forces one unique PMNS-assisted DM closure
> point with no remaining branch-global caveat,

then one more theorem would still strengthen the package:

- either an analytic all-components uniqueness theorem on the fixed `N_e` seed
  surface
- or a certified global optimization theorem on that exact surface whose
  hypotheses are proved inside the framework

Without that, the strongest perfectly honest wording is:

> the refreshed branch has an exact effective-action selector and a unique
> lowest-action closure branch on the current exact constrained branch scan.

## Recommendation

For review packaging, do **not** bury this point.

The package is strongest if it says both:

1. the old exact one-flavor `5.297x` miss is gone on the PMNS-assisted closure
   branch
2. the remaining review-sensitive issue is no longer physics content or a live
   placeholder, but only whether the selector branch uniqueness should be
   promoted from branch-scanned to fully analytic/global

That is the honest Nature-grade boundary.
