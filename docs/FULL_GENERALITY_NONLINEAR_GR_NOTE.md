# Full Generality Nonlinear GR Gap

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** bounded route to a coarse-grained exterior law; sharp obstruction for full nonlinear GR

## Purpose

The current branch already contains a real restricted strong-field package:

- exact local `O_h` shell closure
- exact same-charge bridge
- exact local static conformal lift
- exact microscopic Schur boundary action
- exact finite-rank source closure

The question here is narrower and harder:

> can that restricted Einstein/Regge lift be pushed to fully general nonlinear GR,
> or is a new principle missing?

This note does not re-prove the restricted package. It uses the current branch
results as inputs and asks what remains after the best coarse-grained exterior
projection is extracted.

## What the branch already shows

Two existing bounded results matter here:

- the exact finite-rank source class has a vacuum-close coarse-grained exterior
  law after radial harmonic projection
- the exact local `O_h` source class shows the same behavior, with an even
  smaller residual after coarse-graining

That is a genuine route forward, but it is only a route to a **scalar static
exterior law**.

The current restricted machinery determines:

- `phi`
- `psi = 1 + phi`
- `chi = 1 - phi`
- the diagonal static conformal candidate
- the shell boundary action
- the radial exterior projection `a/r`

It does **not** determine the full tensorial 3+1 geometry.

## Credible route that exists

There is a credible bounded route from the restricted strong-field lift to a
broader exterior law:

1. start from the exact finite-rank / exact `O_h` source data
2. coarse-grain the exterior shell to the radial harmonic law `phi_eff(r) = a/r`
3. use the resulting exterior projection as the macroscopic exterior field
4. test the corresponding static isotropic metric candidate

That route is real. It is already supported by the branch evidence.

But it stops at the exterior scalar law.

## Sharp obstruction

The obstruction to full nonlinear GR is not “we need a slightly better shell
fit.”

The obstruction is that the current exact source and bridge packages only fix
the scalar/static sector. They do not provide a theorem that promotes that
sector to the full tensorial `3+1` metric.

What is missing is a **tensorial matching / selection principle** that would:

1. determine the full lapse-shift-spatial metric, not just the scalar conformal
   factor
2. select the matching radius dynamically rather than by hand
3. control non-spherical perturbations and time-dependent degrees of freedom
4. explain why the isotropic coarse-grained exterior projection is the correct
   macroscopic representative of the exact microscopic field

That missing principle is exactly what full nonlinear GR needs and what the
current branch does not yet derive.

## Why the current route stops

The current branch shows that:

- the direct microscopic `3+1` candidate still has a nonzero Einstein residual
- the coarse-grained exterior projection sharply reduces that residual
- the residual reduction is real, but it is a projection result, not a full
  `3+1` tensorial closure theorem

So the codebase has a **good scalar exterior route** and a **sharp tensorial
obstruction**. It does not yet have full nonlinear GR.

## Exact blocker, localized

The exact blocker is:

> no theorem yet derives the tensorial `3+1` matching map from the microscopic
> exact source field to the macroscopic exterior metric

Equivalent phrasing:

> the branch can derive the scalar exterior projection, but not the full
> tensorial completion of that projection

This is the principle that would have to be added to make the result fully
general.

## What would close it

To turn the bounded route into a full nonlinear GR closure, the next theorem
would need to show one of:

1. the exact microscopic source data uniquely determine the full `3+1` metric
   sector, including non-isotropic and dynamical components
2. the coarse-grained exterior harmonic law is the unique tensorial completion
   of the microscopic bridge data
3. the `3+1` Einstein / Regge residual vanishes for the lifted field without
   imposing any static isotropic ansatz by hand

None of those are yet present on the branch.

## Verdict

- **Credible route present:** yes, to a coarse-grained scalar exterior law
- **Full nonlinear GR closable now:** no
- **Missing principle:** tensorial matching / completion from microscopic source
  data to the full `3+1` metric

So the remaining gap is localized, but it is still a genuine next-paper gap.
