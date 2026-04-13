# Distributed-Source Strong-Field Closure and Common Spacetime Candidate

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_distributed_source_spacetime_closure.py`  
**Status:** Exact finite-support source-model theorem plus bounded 4D metric candidate; not full nonlinear GR

## Purpose

The previous exact strong-field foothold only covered a **rank-one local
source**:

- `H_u = H_0 - u |0><0|`
- exact enhancement factor `(1 - u G_00)^-1`

That removed one heuristic, but left the obvious objection:

> the real strong-field source is not a single lattice site

This note extends the exact resolvent closure to a **finite-support diagonal
attractive source model**, then uses the resulting exterior harmonic field to
build one common static-isotropic spacetime candidate.

This is the first Codex-side gravity step that:

1. goes beyond the rank-one point source exactly, and
2. feeds both `g_ij` and `g_tt` from the same source-renormalized object

It still does **not** derive full nonlinear GR.

## Exact theorem: finite-support distributed source

Let:

- `H_0 = -Delta_lat`
- `S` be a finite support of lattice sites
- `P` inject the support basis into the full lattice basis
- `V` be a positive diagonal matrix on `S`
- `H_V = H_0 - P V P^T`
- `G_0 = H_0^-1`
- `G_S = P^T G_0 P`

Then the exact finite-rank Woodbury / Dyson identity gives:

`G_V P = G_0 P (I - V G_S)^-1`

This is the natural finite-support generalization of the rank-one formula

`G_u(:,0) = G_0(:,0) / (1 - u G_00)`.

So for any bare source weights `m` supported on `S`,

`phi = G_V P m = G_0 P q`

with

`q = (I - V G_S)^-1 m`.

This means the exact distributed-source field is a superposition of the bare
Green columns with **renormalized source weights** `q`.

## Exact consequence: exterior harmonicity

Because

`H_0 phi = P q`,

the exterior field obeys

`(-Delta_lat) phi = 0`

at every site outside `S`.

So the exact strong-field distributed-source model already gives the right
kind of exterior object:

- one harmonic field outside the matter support
- sourced by a support-renormalized effective source vector

This is stronger than the rank-one point-source foothold because it removes
the most obvious “single site only” complaint.

## Bounded common spacetime candidate

The remaining spacetime problem is not “invent a separate lapse.” It is:

> use the same exterior harmonic object to feed both sectors

Using the previously established static isotropic vacuum bridge, define:

- `psi = 1 + phi`
- `alpha psi = 1 - phi`
- `alpha = (1 - phi) / (1 + phi)`

Then both:

- `psi`
- `alpha psi`

are harmonic outside the support whenever `phi` is harmonic outside the
support.

So this candidate satisfies the static isotropic vacuum bridge equations on
the exterior:

- `(-Delta) psi = 0`
- `(-Delta)(alpha psi) = 0`

outside the matter support.

Within the static isotropic time-symmetric vacuum ansatz, those are exactly
the reduced Einstein vacuum equations. So the exterior test here is already
an Einstein-residual test **within that ansatz**.

That is the right kind of common temporal/spatial closure object.

## What the script verifies

### Exact checks

1. finite-support column identity in 1D
2. compressed distributed-source field in 1D
3. exterior harmonicity in 1D
4. finite-support column identity in 3D
5. compressed distributed-source field in 3D
6. exterior harmonicity in 3D

All of those are exact linear-algebra statements on finite lattices.

### Bounded checks

7. the common-source spatial candidate `psi = 1 + phi` satisfies the reduced
   static-isotropic Einstein residual
8. the common-source lapse candidate `alpha = (1 - phi)/(1 + phi)` satisfies
   the reduced static-isotropic Einstein residual through `alpha psi = 1 - phi`
9. the scaled candidate remains nondegenerate on the support

These are bounded because the temporal completion still uses the static
isotropic vacuum bridge rather than a direct derivation of the vacuum system
from the lattice Hamiltonian.

## What this does close

This closes a real sub-gap:

> the exact strong-field source-model foothold is no longer limited to a
> rank-one point source

The exact source-model theorem now covers a finite-support diagonal attractive
source class, with explicit support renormalization.

That is the strongest Codex-side strong-field gravity source result so far.

## What this does not close

This note does **not** close:

1. **the physical matter source model**
   - the theorem covers a finite-support diagonal attractive source class
   - it does not yet derive the actual many-body matter source from the full
     lattice Hamiltonian
2. **full nonlinear GR**
   - the common `alpha`/`psi` construction still uses the static isotropic
     vacuum bridge
3. **a general 4D field equation**
   - the result is still within the static isotropic exterior surface
4. **no-horizon / no-echo**
   - those remain downstream

## Honest status upgrade

Before this note:

- exact strong-field source closure existed only for a rank-one point source
- `g_tt` and `g_ij` still looked like different problems

After this note:

- exact strong-field source closure extends to a finite-support distributed
  source class
- one common exterior harmonic field can now be used to drive both sectors in
  a bounded spacetime candidate

So the gravity program is sharper:

1. exact source-model foothold beyond the point source: **done**
2. direct derivation of the static isotropic vacuum bridge from the lattice:
   **still open**
3. full nonlinear 4D closure: **still open**

## Practical next step

The next real gravity target is now narrower:

1. derive why the actual strong-field lattice matter source reduces to the
   finite-support source class above, or derive the correct broader class
2. derive the static isotropic vacuum bridge equations directly from the
   same lattice closure object, instead of importing them as a bounded bridge
3. only then promote a 4D strong-field metric candidate
