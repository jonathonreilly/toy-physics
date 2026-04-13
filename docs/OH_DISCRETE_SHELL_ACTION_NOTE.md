# Exact Discrete Junction Action on the `O_h` Sewing Shell

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_oh_discrete_shell_action.py`  
**Status:** Exact reduced shell action plus bounded finite-rank consequence

## Purpose

The current strong-field chain already has:

- an exact discrete DtN shell kernel
- an exact rank-one reduced junction operator
- an exact pointwise shell law on the local `O_h` class

What was still missing was the variational statement that packages those facts
as a genuine discrete shell action rather than only as a solved boundary map.

This note supplies that missing step.

## Exact reduced shell action

Let `z` denote the charge-normalized reduced shell/junction data vector
extracted from the exact star-support DtN problem, and let `v_red` be the
unit-charge reduced junction vector from the same operator.

Define the discrete reduced shell functional

`J(z) = 1/2 || z - v_red ||_2^2`

This is the exact quadratic shell action on the current reduced gravity
surface.

Its Euler-Lagrange equation is immediate:

`∇J(z) = z - v_red = 0`

so the unique stationary point is

`z = v_red`

That is exactly the reduced junction law already extracted from the star-
support DtN operator.

## Pointwise `O_h` lift

On the exact local `O_h` source class, the sewing band `3 < r <= 5` already
has vanishing within-orbit spread for the shell observables. So the reduced
stationary point lifts pointwise on the full shell band:

- the reduced action is stationary at `z = v_red`
- the `O_h` orbit spread is zero
- therefore the reduced law is already the exact pointwise shell law on
  `3 < r <= 5`

So the exact `O_h` sewing law is not just a boundary map. It is the stationary
point of a discrete junction action on the orbit quotient of the sewing shell.

## Regge-style interpretation

This is a Regge-style lift in the minimal discrete sense:

- the shell data are treated as finitely many hinge/orbit variables
- the action is quadratic and local on those discrete variables
- stationarity reproduces the shell junction law exactly

It is still not a full simplicial Einstein-Hilbert derivation. It is the exact
boundary-action form of the already-solved `O_h` shell closure.

## Bounded finite-rank consequence

For the broader exact finite-rank source family, the same reduced action is
still exact on the reduced coordinates, but the pointwise lift is only
approximate because the within-orbit spread is bounded rather than zero.

So the new variational statement is exact on the local `O_h` class and
bounded on the larger exact family.

## What this closes

This closes the last operator-level ambiguity on the exact local `O_h` shell:

> the sewing law is not only an exact DtN boundary map; it is also the unique
> stationary point of a discrete quadratic shell action on the reduced
> junction data

## What this still does not close

This note still does **not** close:

1. a microscopic derivation of the quadratic shell action from the lattice
   Hamiltonian or simplex action
2. a full simplicial Regge-Einstein derivation of the 4D metric closure
3. the remaining bounded corrections for the broader finite-rank family

## Updated gravity target

After this note, the live target narrows again:

- the `O_h` shell law now has an exact discrete stationary-action form
- the remaining theorem target is to derive that action as a Schur-complement
  boundary functional of the microscopic lattice dynamics, rather than
  inserting the reduced DtN operator as input
