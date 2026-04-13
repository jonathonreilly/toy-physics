# Exact Rank-One Reduced Junction Operator

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_reduced_junction_operator.py`  
**Status:** Exact reduced-junction theorem plus bounded closure consequence

## Purpose

The gravity line had already shown:

- the radial DtN shell kernel is exact
- the anisotropic shell sector is one exact reduced DtN mode
- the amplitude of that mode is fixed by total charge on the current exact
  star-supported source class

That still left one structural question:

> is the reduced sewing law best thought of as several separately derived facts,
> or does it already collapse to one exact operator?

This note answers that cleanly.

## Reduced junction data

For a source field on the current star-supported exact source class, define the
reduced junction data to include:

- the radial shell kernel per unit charge
- the four anisotropic orbit-channel coefficients per unit charge
- the shell-mean total exterior response per unit charge
- the shell-mean anisotropic exterior response per unit charge

This is the exact reduced shell/exterior data the gravity program has already
been using.

## Exact rank-one operator

Apply this reduced-data extraction to the seven point-Green columns on the star
support.

The script finds:

1. all seven columns induce the same reduced junction vector
2. the resulting reduced-junction matrix therefore has rank one
3. it factors exactly as

   `J_red = v_red * (1,1,...,1)`

   i.e. one fixed reduced junction vector composed with the total-charge
   functional

So on the current reduced gravity surface:

> the sewing law is already one exact reduced junction operator

It is not a family of unknown closures.

## Exact agreement with the current exact source families

The script then checks:

1. the exact local `O_h` family
2. the broader exact finite-rank family

and finds that both lie on the same reduced-junction image to machine
precision.

So the source families already used in the gravity line are not exceptions.
They realize the same exact reduced junction operator.

## Interpretation

This is the clearest current statement of what has been solved in strong-field
gravity:

> on the reduced shell/exterior surface relevant to the present branch, the
> sewing law is an exact rank-one operator controlled entirely by total charge

That is a genuine closure of the reduced junction problem.

## What this closes

This closes another real ambiguity:

> on the current exact star-supported source class, the reduced sewing-shell law
> is not an open operator-level problem; it is one exact rank-one junction
> operator

## What this still does not close

This note still does **not** close:

1. the full lift from reduced shell/exterior data to the full nonlinear 4D
   spacetime theorem
2. the complete Einstein/Regge interpretation of that reduced operator
3. full nonlinear GR on the framework surface

## Updated gravity target

After this note, the remaining gravity blocker is sharper again:

- the reduced junction law itself is no longer open
- the live blocker is now the lift from that exact reduced junction operator to
  the full nonlinear 4D closure
