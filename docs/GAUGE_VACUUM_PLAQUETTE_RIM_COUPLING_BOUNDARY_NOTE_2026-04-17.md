# Gauge-Vacuum Plaquette Rim-Coupling Boundary

**Date:** 2026-04-17  
**Status:** exact local boundary theorem on the plaquette PF lane; the current
stack already fixes the theorem-grade local marked data `exp[(beta/2)J]` and
`D_beta^loc`, and now also fixes the full-slice rim lift `B_beta(W)` at the
level of an exact local Wilson/Haar integral, but explicit closed-form
`beta = 6` evaluation is still not derived  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_rim_coupling_boundary.py`

## Question

If the live constructive target is now `K_6^env / B_6`, what exactly is already
proved on the local rim side, and what exact local object is still missing?

## Answer

The theorem-grade local marked content already fixed on the source sector is:

- the exact marked half-slice operator `exp[(beta/2)J]`,
- the exact normalized four-link local Wilson factor `D_beta^loc`.

After trivial-channel normalization, the non-marked mixed-link factors are
already proved to be rep-independent scalars on the marked source sector.
So there is no hidden local environment sequence left inside the mixed kernel.

More sharply:

- `D_beta^loc` is the sharp local marked mixed-kernel boundary operator already
  proved on the marked class sector,
- `exp[(beta/2)J]` is also exact, but it is the half-slice plaquette
  multiplier rather than the missing rim functional itself.

The new retained compressed rim-functional uniqueness theorem now closes the
left boundary functional on every retained marked class sector: it is the
universal Peter-Weyl evaluation functional `K(W)`.

What is still missing is explicit framework-point evaluation of the local
boundary lift

`B_beta(W)`

whose action on the full orthogonal slice Hilbert space compresses to that
retained left boundary functional.

The new full-slice rim-lift integral-boundary theorem now fixes that full rim
map at the integral-expression level:

`B_beta(W)(U)
 = integral_(Omega^rim(U)) dmu_H(Xi^rim)
     exp[(beta / 3) A^rim(U, Xi^rim; W)]`.

Its canonical class-sector descendant is

`eta_beta(W) = P_cls B_beta(W)`.

So the current stack no longer lacks the local construction class of the rim
map. What it still lacks is explicit closed-form `beta = 6` evaluation of
that already-identified local integral and its compressed descendant. The
current runner on the older transfer lane still uses a witness boundary state
rather than an evaluated one.

So the next local derivation target is exactly:

- explicit `beta = 6` evaluation of the Wilson rim-coupling lift `B_6(W)`.

## Setup

From the exact source-sector matrix-element factorization theorem:

- the marked half-slice contribution is exactly `exp[(beta/2)J]`.

From the exact local/environment factorization theorem:

- the normalized mixed-kernel local marked contribution is exactly
  `D_beta^loc`,
- non-marked mixed-link factors are trivial-channel scalars after
  normalization.

From the exact spatial-environment transfer theorem:

- one orthogonal-slice kernel `K_beta^env` exists,
- one boundary state `eta_beta(W)` exists and is induced by local rim coupling,
- but the current theorem surface does not yet derive the map producing
  `eta_beta(W)`.

## Theorem 1: the theorem-grade local marked boundary content is already exhausted by `exp[(beta/2)J]` and `D_beta^loc`

On the marked class sector, the exact local Wilson data already proved on
`main` are:

- `exp[(beta/2)J]`,
- `D_beta^loc`.

After trivial-channel normalization, no further representation-dependent local
mixed-link operator remains on the marked source sector.

So the current exact stack has already exhausted the theorem-grade local
mixed-kernel data.

Among those two exact objects, the sharper boundary-side local operator is
`D_beta^loc`: it is the exact normalized four-link marked mixed-kernel factor.
The half-slice multiplier `exp[(beta/2)J]` remains exact and indispensable, but
it is not yet the missing rim functional.

## Corollary 1: the retained left boundary functional is already closed

On the retained marked class sector, the later compressed rim-functional
uniqueness theorem now gives one exact universal left boundary functional:

`K(W) = sum d_(p,q) conj(chi_(p,q)(W)) chi_(p,q)`.

So the branch no longer has to treat retained class-sector `W`-dependence as
open on the left boundary side.

## Corollary 2: the missing local issue is explicit evaluation of the full slice lift

Since the transfer theorem still uses `eta_beta(W)` through one exact
boundary-amplitude law, and since the new full-slice rim-lift theorem already
fixes `B_beta(W)` as the corresponding local Wilson/Haar integral, the
remaining local issue is not:

- `D_beta^loc`,
- nor another retained class-sector `W`-dependence formula,
- nor the construction class of the full slice lift itself,
- nor another marked mixed-kernel coefficient sequence.

It is exactly:

- explicit framework-point evaluation of the Wilson rim-coupling lift
  `B_beta(W)` on the slice Hilbert space, together with explicit evaluation of
  its compressed descendant `eta_beta(W)`.

At the framework point, that means:

- evaluate `B_6(W)`.

## What this closes

- exact clarification of what is already theorem-grade on the local rim side
- exact clarification that `exp[(beta/2)J]` and `D_beta^loc` exhaust the proved
  local mixed-kernel content
- exact identification of the remaining local target as explicit evaluation of
  the full slice lift `B_6(W)`

## What this does not close

- explicit evaluated formula for the full slice lift `B_6(W)`
- explicit evaluated full-slice `eta_6`
- explicit `K_6^env`
- explicit `S_6^env`
- explicit `rho_(p,q)(6)`
- explicit framework-point plaquette PF data

## Why this matters

This removes the last ambiguity on the local side of the PF lane.

The branch no longer has to say vaguely that “rim coupling is missing.”
It now says exactly what local theorem step is still absent:

- explicit `beta = 6` evaluation of the full-slice rim lift `B_6(W)`.

That is the next real derivation target if we want to move from the current
kernel/rim compression theorem to actual plaquette environment construction.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_rim_coupling_boundary.py
```
