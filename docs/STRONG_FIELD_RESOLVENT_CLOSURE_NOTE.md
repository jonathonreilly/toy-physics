# Strong-Field Resolvent Closure for a Local Source

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_strong_field_resolvent_closure.py`  
**Status:** Exact subtheorem for the rank-one local-source model; not full nonlinear GR

## Purpose

The current strong-field metric note uses the backreaction factor

`(1 - phi(0))^-1`

inside the point-source self-consistency equation. That factor was previously
being used as a motivated closure ansatz.

This note isolates what can actually be proved:

> For an additive local attractive perturbation of the lattice Hamiltonian,
> the strong-field enhancement factor is an exact resolvent identity.

This does **not** close strong-field gravity. It removes one specific heuristic
from the current point-source derivation.

## Setup

The weak-field gravity chain already uses additive potential coupling:

`H(phi) = H_0 + phi`

For a local attractive source at the origin, take the exact rank-one model

`H_u = H_0 - u |0><0|`

with `u > 0`. Let

- `G_0 = H_0^-1`
- `P_0 = |0><0|`
- `G_00 = <0|G_0|0>`

Then the exact resolvent is

`G_u = (H_0 - u P_0)^-1`.

## Exact theorem

By the Sherman-Morrison / rank-one Dyson identity,

`G_u = G_0 + (u / (1 - u G_00)) G_0 P_0 G_0`.

Therefore the source column and source diagonal obey

- `G_u(x,0) = G_0(x,0) / (1 - u G_00)`
- `G_u(0,0) = G_00 / (1 - u G_00)`

This is exact on the finite lattice. No eikonal approximation is used.

The script verifies this directly in:

- 1D on a path lattice
- 3D on a small finite cubic lattice

to machine precision.

## Consequence for the current strong-field fixed point

If the local attractive potential is closed self-consistently by

`u G_00 = phi(0)`,

then the resolvent identity gives

`phi(x) = M G_u(x,0) = M G_0(x,0) / (1 - phi(0))`

and therefore

`phi(0) (1 - phi(0)) = M G_00`.

This is exactly the quadratic fixed-point equation used in the current
point-source strong-field note.

So the situation is now sharper:

- the enhancement factor itself is **not** ad hoc in the rank-one local-source
  model
- what remains open is the physical closure that identifies the actual
  strong-field lattice matter source with this rank-one model

## What this does close

This closes one specific sub-gap:

> The factor `(1 - phi(0))^-1` can be derived exactly from the resolvent of an
> additive rank-one attractive local potential.

That means the current point-source fixed-point profile is no longer just a
heuristic once that local-source model is accepted.

## What this does not close

This note does **not** close:

1. **full nonlinear GR**
   - no 4D spacetime closure is derived here
2. **the strong-field spatial metric**
   - the conformal metric still needs to be justified in the strong-field
     regime rather than carried over from the weak-field surface
3. **`g_tt`**
   - the temporal sector is untouched here
4. **distributed sources**
   - the theorem is for a rank-one local source, not an extended matter profile
5. **no-horizon / no-echo**
   - those remain downstream and conditional

## Honest status upgrade

Before this note:

- the point-source fixed-point law looked like a hand-inserted backreaction
  ansatz

After this note:

- the same fixed-point law is exact **within the rank-one additive local-source
  resolvent model**

That is a real upgrade, but still only a subtheorem.

## Paper-safe use

This note is **not** publication authority for a gravity promotion.

It is review-authority support for the research program:

- replace ad hoc strong-field closures with exact lattice resolvent identities
- then derive the full spacetime closure from that stronger base

## Practical next step

The next real gravity target remains:

1. derive the physical strong-field source model from the exact propagator /
   Hamiltonian, not just the rank-one toy
2. derive `g_tt` and `g_ij` from the same strong-field closure
3. only then revisit horizon / echo consequences
