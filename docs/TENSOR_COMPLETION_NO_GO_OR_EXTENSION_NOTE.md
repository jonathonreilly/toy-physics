# Tensor Completion No-Go / Extension Split

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** scalar-only completion remains ruled out; positive route reduced to one tensor kernel/source-map theorem family

## Purpose

This note records the sharpened split after the new tensor matching theorem.

The current branch already had:

- exact restricted shell/junction closure
- exact microscopic Schur boundary action
- exact restricted discrete Einstein/Regge lift
- sharp no-go for scalar-trace-only completion

The new theorem adds one more exact localization:

> the smallest tensor completion compatible with the retained restricted family
> is scalar shell data plus one shift-like and one traceless-shear boundary
> coordinate.

So the remaining gap is no longer an unspecified tensor mystery.

## Closed negative statement

The scalar-only route remains dead.

No completion principle that factors only through the current scalar shell
trace / Schur data can determine the full `3+1` metric on this branch.

That no-go is exact and unchanged.

## Positive extension that survives

What survives as a real positive route is narrower:

1. retain the exact scalar shell trace `f`
2. augment it by two non-scalar tensor boundary coordinates
   - `a_vec`
   - `a_tf`
3. derive a shell-local tensor boundary action
   - symmetric positive-definite kernel `K_tensor`
4. derive the microscopic source drive `eta`

Then the tensor stationarity equation would be

`K_tensor [a_vec, a_tf]^T = eta`

coupled to the already exact scalar shell law.

## What the branch now knows exactly

The branch now knows:

- fewer than two extra non-scalar shell coordinates cannot work on the current
  audited family
- two extra coordinates are locally sufficient to capture the tested mixed
  vector/shear tangent directions
- the missing theorem is therefore not “invent a new gravity metric”; it is
  “derive one rank-two tensor boundary block from the microscopic source data”

## What this means for full GR

This does **not** yet retain full nonlinear GR.

But it does reduce the open gravity problem to one precise operator family:

> the microscopic tensor source-map / boundary-kernel theorem beyond the exact
> scalar shell action.

If that theorem lands on the current restricted class, gravity upgrades from
restricted scalar strong-field closure to a genuine restricted tensor
completion theorem.

If it fails, the failure should now be visible as a direct obstruction in the
attempt to derive `K_tensor` and `eta`, not as another diffuse gap.

## Practical next move

The next honest gravity attack is therefore:

1. derive candidate microscopic observables whose shell reduction yields
   `a_vec` and `a_tf`
2. derive their Schur/Dirichlet boundary kernel
3. test whether the resulting tensor shell action closes the restricted class
4. only then ask about widening beyond that class
