# Local Bridge Uniqueness on the Star-Supported Strong-Field Class

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_local_bridge_uniqueness.py`  
**Status:** Exact affine-bridge theorem plus bounded nonlinear exclusion on current source class

## Purpose

After the shell source, same-charge bridge, local static-constraint lift, and
microscopic boundary action were all derived, one real conceptual gap still
remained:

> perhaps the current bridge is only one convenient local reparameterization of
> the exterior field, and a different nonlinear local bridge could close the
> same shell law

This note closes that local-reparameterization ambiguity on the current
star-supported finite-rank class.

## Exact affine-bridge theorem

Let `phi_ext` be the exact exterior projector field. On the exterior bulk it is
discrete harmonic:

- `H_0 phi_ext = 0`.

Now consider any local scalar bridge channel of the form

- `u = F(phi_ext)`

and demand that it too be exterior harmonic on the same bulk for the whole
star-supported finite-rank class.

Because harmonicity on the graph is exactly the discrete mean-value property,
this forces

- `F(mean(neighbors)) = mean(F(neighbors)))`

on the nontrivial exterior value sets realized by the class.

The only scalar maps preserving all such averages are affine maps. So any local
scalar bridge channel that remains exterior harmonic on the current class must
have the form

- `F(phi) = a + b phi`.

Then:

- boundary normalization fixes `a = 1`
- same-charge inheritance fixes `b = 1` for the spatial channel
- the attractive temporal branch fixes the sign for the temporal channel

So the native bridge

- `psi = 1 + phi_ext`
- `chi = 1 - phi_ext = alpha psi`

is the unique local scalar exterior-harmonic bridge on the current
star-supported class.

## Bounded nonlinear exclusion

The script checks random star-supported finite-rank examples and compares the
affine bridge with quadratic local deformations

- `F(phi) = 1 + phi + a_2 phi^2`.

It finds:

- the affine bridge remains exterior harmonic to machine precision
- quadratic deformations produce immediate bulk residual away from the shell
- the same failure appears directly as a discrete Jensen/mean-value gap on
  nontrivial neighbor data

So nonlinear local bridge reparameterizations are not just unfavored. They fail
the exact exterior-harmonic requirement on the current class.

## What this closes

This closes the local bridge ambiguity:

> on the current star-supported finite-rank class, the native same-charge
> bridge is the unique local scalar exterior-harmonic bridge

That materially narrows the remaining bridge-side gravity gap.

## What this still does not close

This note still does **not** close:

1. nonlocal or tensorially broader bridge structures beyond the local scalar
   bridge class
2. a full pointwise Einstein/Regge theorem beyond the current static conformal
   bridge
3. fully general nonlinear GR

## Updated gravity target

After this note, the remaining gravity problem is narrower again:

- local scalar bridge freedom is no longer open on the current class
- the live gap is now genuinely beyond the current static conformal bridge,
  not within its local scalar reparameterizations
