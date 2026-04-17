# Universal GR Invariant-Frame Obstruction Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** universal representation/invariant route only  
**Purpose:** decide whether the universal complement admits a canonical frame
from representation-theoretic invariants alone

## Verdict

No canonical complement frame is forced by the current invariant data.

The strongest invariant-frame candidate derivable from the present universal
stack is not a full section of the complement bundle. It is the
`Pi_A1`-anchored orbit bundle:

`P_curv^cand = (Pi_A1, O_{E \oplus T1}, \omega_MC)`

with canonical invariant core

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

That candidate is exact, but it stops at the orbit bundle. The complement is
still not canonically sectioned.

## What is exact

The current universal stack already supplies:

- the exact scalar observable generator `W[J]`;
- the exact `3+1` background `PL S^3 x R`;
- the exact tensor-valued variational candidate
  `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`;
- the exact unique symmetric `3+1` quotient kernel on the finite prototype;
- the exact invariant `A1` projector `Pi_A1`;
- the exact shared-axis weight decomposition of the universal complement.

The invariant section is the rank-2 projector onto:

- lapse `h_00`;
- spatial trace `tr(h_ij)`.

Those two channels are canonical. The complement is not.

## Weight decomposition

After the shared bright axis is fixed, the universal complement decomposes
under the residual `SO(2)` stabilizer into:

- four invariant directions;
- two exact weight-1 doublets;
- one exact weight-2 sector.

The weight-1 doublets are the crucial point. They are equivalent copies of
the same `SO(2)` representation, so the multiplicity space is nontrivial.
Representation-theoretic invariants can identify the isotypic block, but they
cannot choose a preferred basis within that block.

Equivalently, the normalized lift family

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`

survives exactly because the weight-1 multiplicity space is not broken by the
current invariant tensors.

## Generator algebra

The full spatial rotation algebra on the universal `3+1` basis acts
nontrivially on the complement and has rank 3 at the Lie-algebra level.

What matters is not that the action is small. It is that the action is
homogeneous:

- `Pi_A1` is invariant to machine precision;
- the complement remains an `SO(3)` orbit bundle;
- no invariant tensor in the current atlas selects a preferred complement
  axis or a preferred complement section.

So the generator algebra is rich enough to move the complement, but the
current invariants are not strong enough to canonically pin it down.

## Quotient-kernel spectrum

The unique symmetric `3+1` quotient kernel is nondegenerate on the finite
prototype.

That is important but not decisive:

- the quotient kernel has no hidden null directions;
- its spectrum is invariant under valid frame rotations;
- therefore the spectrum does not break the residual complement orbit.

So quotient-kernel uniqueness does not produce a canonical complement frame.
It only confirms that the tensor candidate is unique on the symmetric
quotient.

## Exact obstruction

The exact obstruction is now sharp:

> the current invariant tensors determine the `Pi_A1` core and the orbit
> bundle on `E \oplus T1`, but they do not determine a canonical section of
> that bundle.

More explicitly:

1. `Pi_A1` is canonical.
2. the complement is an `SO(3)` orbit bundle.
3. the weight-1 complement sectors appear with multiplicity two.
4. the quotient-kernel spectrum is frame-invariant.
5. therefore no representation-theoretic invariant in the current atlas
   selects a unique universal complement frame.

So the strongest exact statement is a no-go:

> representation-theoretic invariants alone do not canonically fix the
> universal complement frame.

## Strongest candidate

The strongest invariant-frame candidate currently supported is:

`P_curv^cand = (Pi_A1, O_{E \oplus T1}, \omega_MC)`

with the exact residual gauge

`SO(3)`.

This is the best covariant completion available today, but it is not a
canonical frame. It is an invariant core plus an orbit bundle.

On the shared-axis weight-1 sector, the residual real commutant is 8D, so
the multiplicity space is large enough to support an entire circle of
normalized lifts and therefore cannot be canonically sectioned by invariant
tensors alone.

## Honest status

The current universal representation/invariant route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- blocked at the canonical complement-frame level.

The complement is orbit-canonical, not section-canonical.
