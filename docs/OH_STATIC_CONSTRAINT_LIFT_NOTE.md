# Exact Local Static-Constraint Lift on the Current Bridge Surface

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_oh_static_constraint_lift.py`  
**Status:** Exact local shell-to-`3+1` constraint lift on the current static conformal bridge surface

## Purpose

The strong-field gravity line had already fixed:

- the exact shell source on the sewing band
- the unique same-charge bridge
  - `psi = 1 + phi_ext`
  - `chi = 1 - phi_ext = alpha psi`
- the reduced and then pointwise shell stress law on the exact local `O_h`
  source class

What was still not said cleanly enough was whether this already gives a genuine
local shell-to-`3+1` lift, or only a collection of compatible formulas.

This note closes that specific gap on the current static conformal bridge
surface.

## Exact local lift

Start from the exact exterior projector field `phi_ext` and shell source

- `sigma_R = H_0 phi_ext`

on the sewing band

- `3 < r <= 5`.

With the exact same-charge bridge

- `psi = 1 + phi_ext`
- `chi = 1 - phi_ext = alpha psi`

define the local shell density and stress-trace pointwise by

- `rho = sigma_R / (2 pi psi^5)`
- `S = 0.5 rho (1/alpha - 1)`.

Then the discrete static conformal constraint pair is satisfied identically:

- `H_0 psi = 2 pi psi^5 rho`
- `H_0 chi = -2 pi alpha psi^5 (rho + 2S)`.

So the shell-to-`3+1` lift is no longer heuristic on this bridge surface. It
is an exact local identity once the exact lattice shell source and same-charge
bridge are in hand.

## Exact `O_h` consequence

On the exact local `O_h` source class, the script finds:

- the shell support remains exactly confined to `3 < r <= 5`
- the two local static conformal constraints hold to machine precision
- outside the shell, both channels are vacuum in the same discrete constraint
  sense
- the lifted shell density `rho` and stress-trace `S` are pointwise orbit laws
  on the whole sewing band

So on the exact local `O_h` class, the shell-side `3+1` lift is already exact
at orbit resolution.

## Bounded broader-family consequence

For the broader finite-rank family, the same local static conformal constraint
pair still holds exactly, while the remaining shell variation stays small:

- `rho` within-orbit spread below about `1.4%`
- `S` within-orbit spread below about `2.7%`

So the broader-family correction is not a failure of the local bridge lift. It
is only the small non-`O_h` shell variation already isolated elsewhere.

## What this closes

This closes the last shell-to-`3+1` ambiguity on the current bridge surface:

> on the exact local `O_h` source class, the exact shell source and unique
> same-charge bridge already admit an exact local static conformal constraint
> lift

That is a real restricted strong-field closure result.

## What this still does not close

This note still does **not** close:

1. a full pointwise Einstein/Regge theorem beyond the current static conformal
   bridge
2. fully general non-`O_h` strong-field closure
3. fully general nonlinear GR

## Updated gravity target

After this note, the remaining gravity problem is narrower again:

- the shell-to-`3+1` lift is no longer open on the current bridge surface
- the live blocker is now the final pointwise Einstein/Regge interpretation of
  that bridge closure, and then any broader extension beyond the current exact
  source classes
