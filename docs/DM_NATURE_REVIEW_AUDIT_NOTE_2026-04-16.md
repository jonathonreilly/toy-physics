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

The review situation is now materially stronger.

What is now closed exactly:

- the PMNS-assisted `N_e` closure problem factors through one exact reduced
  domain, the fixed native `N_e` seed surface
- the active chart is exact and surjective on that surface
- the `eta` map factors exactly through that surface
- the certified global selector theorem now gives a finite stationary set on
  that exact reduced domain and proves the low-action closure branch is the
  unique global minimum on it

So the older review question

> do we need a separate theorem about components beyond the exact reduced
> surface?

is answered **no** for the scoped `N_e` closure claim, and the stronger
same-surface uniqueness/minimality question is also now answered positively.

The strengthened exact picture is:

- the admissible PMNS-assisted domain is the fixed native `N_e` seed surface
- the certified reduced-surface optimization finds three stationary closure
  branches on that domain
- the low branch is the unique global minimum
- the next branch is separated by a finite action gap

What is still *not* claimed:

- a separate closed-form algebraic elimination theorem for every symbolic
  stationary component in the abstract beyond the certified reduced-surface
  global-minimum theorem

## Review verdict

### Working-branch verdict

On the refreshed branch, the DM closure route is complete enough to review as
an end-to-end constructive framework result.

### Nature-grade verdict

If the intended claim is:

> the PMNS-assisted `N_e` closure problem is fully reduced and internally
> closed on its exact admissible domain,

then the current branch is already strong enough.

If the intended claim is the still-stronger one:

> there is a closed-form analytic elimination of every symbolic stationary
> component on that same reduced surface,

then the package still does not claim that.

But that is now stronger than the Nature-grade closure need. The physically
relevant uniqueness/minimality statement on the exact admissible domain is
already certified.

## Recommendation

For review packaging, do **not** bury this point.

The package is strongest if it says both:

1. the old exact one-flavor `5.297x` miss is gone on the PMNS-assisted closure
   branch
2. the older “beyond the reduced surface” loophole is closed, and the
   reduced-surface selector is now globally certified there

The only remaining stronger ask is aesthetic: a prettier fully symbolic
stationary elimination theorem, not a missing uniqueness/minimality result for
the closure claim itself.
