# Static Isotropic Vacuum Bridge

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_static_isotropic_vacuum_bridge.py`  
**Status:** BOUNDED bridge result; not a framework derivation of full GR

## Purpose

The current gravity program has a real asymmetry:

- the weak-field spatial sector is much stronger than before
- the temporal sector `g_tt` is still not derived from the same strong-field
  object

This note isolates one useful bridge fact:

> If the exterior strong-field metric is static, isotropic, vacuum, and
> conformally flat in standard 3+1 form, then the lapse is fixed by the same
> harmonic data that fixes the spatial conformal factor.

This does **not** derive full nonlinear GR from the lattice. It sharpens the
remaining target by showing that, on the isotropic vacuum surface, the lapse is
not an independent free function.

## Setup

Take the static isotropic ansatz

`ds^2 = -alpha(r)^2 dt^2 + psi(r)^4 (dx^2 + dy^2 + dz^2)`

with:

- zero shift
- vacuum exterior
- time-symmetric slice (`K_ij = 0`)
- asymptotic flatness

In this standard setting, the vacuum constraint system reduces to:

- `Delta psi = 0`
- `Delta (alpha psi) = 0`

outside the source.

So the two radial functions are harmonic on the exterior domain.

## Exterior harmonic family

For a spherically symmetric exterior harmonic function with asymptotic value
`1`, the only radial form is

`h(r) = 1 + c/r`.

Therefore the static isotropic vacuum family takes the form

- `psi(r) = 1 + a/r`
- `alpha(r) psi(r) = 1 + b/r`

for constants `a`, `b`.

If we further require the weak-field Newtonian limit to match the already
retained gravity surface, then:

- the spatial conformal factor carries the same `1/r` data as the exterior
  lattice Green function
- the lapse must reproduce the same weak-field redshift

That fixes the isotropic Schwarzschild relation

`alpha(r) = (1 - a/r) / (1 + a/r)`.

Equivalently:

- `psi(r) = 1 + a/r`
- `alpha(r) psi(r) = 1 - a/r`

Both are harmonic outside the source.

## What the script checks

The companion script verifies, numerically on radial grids:

1. `Delta psi = 0` for `psi = 1 + a/r`
2. `Delta (alpha psi) = 0` for `alpha = (1 - a/r)/(1 + a/r)`
3. asymptotic flatness
4. the weak-field expansions:
   - `alpha = 1 - 2a/r + O(r^-2)`
   - `psi^4 = 1 + 4a/r + O(r^-2)`

These checks confirm that the isotropic Schwarzschild pair is exactly the
radial harmonic pair compatible with this bridge system.

## What this buys us

This is useful because it narrows the strong-field gravity problem:

- if the lattice program can derive the **static isotropic vacuum system**
  itself, then the temporal lapse is no longer an extra unknown
- the common strong-field closure target becomes:
  - derive `psi`
  - derive that `alpha psi` obeys the same exterior harmonic structure
  - then a 4D metric candidate is fixed

So the unresolved problem is sharper than “derive all of GR from scratch.”
It is:

> derive why the lattice chooses the static isotropic vacuum bridge equations
> from the same exact strong-field closure object that already controls the
> spatial sector.

## What this does not prove

This note does **not** prove:

1. that the framework derives the vacuum Einstein equations
2. that the lattice strong-field source reduces to this static vacuum system
3. that the full strong-field metric is already closed
4. that horizon / echo / singularity claims follow

Those remain open.

## Paper-safe use

This is **not** a flagship-paper promotion note.

It is a research-organization note that clarifies the remaining gravity target:

- the next exact step is not another phenomenology signature
- it is a common temporal/spatial closure law

## Practical conclusion

Current gravity state remains:

- retained:
  - Poisson / Newton weak-field core
  - weak-field WEP
  - weak-field time dilation
- still open:
  - full nonlinear GR / strong-field closure

This note narrows the open target by showing what the temporal sector must look
like **if** the lattice strong-field exterior reduces to a static isotropic
vacuum system.
