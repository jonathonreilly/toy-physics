# Staggered Newton Reproduction on an Open 3D Lattice

**Date:** 2026-04-11  
**Status:** bounded retained companion on `main`  
**Script:** `scripts/frontier_staggered_newton_reproduction.py`

## Question

Can the primary staggered architecture support a Newton-compatible **trajectory**
distance law on a 3D lattice, or is the trajectory observable itself still
broken even when the exact force law is clean?

This is the missing cross-architecture check relative to the Wilson side lane.

## Why a new observable was needed

The retained staggered card already showed a clean exact-force observable,
`F = -<dV/dz>`, but it explicitly avoided centroid-based gravity rows because
the raw staggered centroid oscillates with sublattice structure.

So this runner tests a trajectory readout that is more honest for the
staggered architecture:

- open 3D cubic staggered lattice
- literature-correct scalar/parity coupling
  - `H_diag = (m + V(x)) * epsilon(x)`
- external attractive source displaced along `+z`
- **2x2x2 blocked centroid** to suppress sublattice beating
- free-vs-gravitating subtraction on the same surface

The blocked readout is the key design choice. It asks whether the **envelope**
of the packet responds Newtonically, not whether the raw site-level staggered
oscillation can serve as a clean trajectory observable.

## Audited surface

- sides: `12, 14, 16`
- source offsets: `d = 3, 4, 5, 6`
- `mass = 0.30`
- `G = 50.0`
- `source_strength = 5e-4`
- `dt = 0.10`
- `N_steps = 12`
- packet width: `sigma = 1.30`
- source is an external attractive well
  - `V ~ -1/r`
- observable hierarchy:
  - exact force on the state
  - raw centroid kick
  - blocked `2x2x2` centroid kick

Two calibration choices matter:

1. `d = 2` was dropped because it is a near-field/regularization point and
   spoils the distance fit.
2. `sigma = 1.30` is broad enough that the blocked readout tracks the packet
   envelope rather than sublattice-scale beating.

## Exact outputs

### side = 12

- `d=3`: `F0 = +8.5715e-04`, `Ff = +7.1747e-04`, `block_a = +1.1574e-04`
- `d=4`: `F0 = +4.9691e-04`, `Ff = +4.9854e-04`, `block_a = +6.5480e-05`
- `d=5`: `F0 = +3.1243e-04`, `Ff = +3.2251e-04`, `block_a = +4.1949e-05`
- `d=6`: `F0 = +2.1428e-04`, `Ff = +2.1905e-04`, `block_a = +2.9515e-05`

Fits:

- `|F0| ~ d^-2.003` with `R^2 = 0.9994`
- `|a_block| ~ d^-1.975` with `R^2 = 1.0000`
- `|a_raw| ~ d^-1.914` with `R^2 = 0.9999`

### side = 14

- `d=3`: `F0 = +8.5715e-04`, `Ff = +6.3040e-04`, `block_a = +8.2784e-05`
- `d=4`: `F0 = +4.9691e-04`, `Ff = +4.5923e-04`, `block_a = +5.0381e-05`
- `d=5`: `F0 = +3.1243e-04`, `Ff = +3.0859e-04`, `block_a = +3.1197e-05`
- `d=6`: `F0 = +2.1428e-04`, `Ff = +2.1352e-04`, `block_a = +2.0773e-05`

Fits:

- `|F0| ~ d^-2.003` with `R^2 = 0.9994`
- `|a_block| ~ d^-1.997` with `R^2 = 0.9961`
- `|a_raw| ~ d^-2.104` with `R^2 = 0.9975`

### side = 16

- `d=3`: `F0 = +8.5715e-04`, `Ff = +7.1748e-04`, `block_a = +1.1574e-04`
- `d=4`: `F0 = +4.9691e-04`, `Ff = +4.9856e-04`, `block_a = +6.5480e-05`
- `d=5`: `F0 = +3.1243e-04`, `Ff = +3.2246e-04`, `block_a = +4.1949e-05`
- `d=6`: `F0 = +2.1428e-04`, `Ff = +2.1900e-04`, `block_a = +2.9515e-05`

Fits:

- `|F0| ~ d^-2.003` with `R^2 = 0.9994`
- `|a_block| ~ d^-1.975` with `R^2 = 1.0000`
- `|a_raw| ~ d^-1.914` with `R^2 = 0.9999`

### Global summary

- all exact-force rows are TOWARD
- all blocked-acceleration rows are TOWARD
- all raw-acceleration rows are also TOWARD on this tuned surface
- global exact-force fit: `|F0| ~ d^-2.003` with `R^2 = 0.9994`
- global blocked-trajectory fit: `|a_block| ~ d^-1.982` with `R^2 = 0.9232`

## Interpretation

On this open 3D cubic surface, the primary staggered architecture **does**
support a Newton-compatible distance law once the trajectory readout is
coarse-grained to remove the sublattice artifact.

That is the main result of this lane.

The important distinction is:

- the **architecture** was not the blocker
- the **raw trajectory observable** was the blocker

The blocked centroid is not cosmetic. It is the minimal readout that makes the
staggered packet’s envelope visible without confusing it with parity-scale
oscillation.

## Retention boundary

This note is retained only as a **bounded companion**, not as a new staggered
headline.

The safe statement is:

> the staggered architecture can reproduce a Newton-compatible 3D distance law
> on an open cubic lattice, but only when the trajectory observable is
> coarse-grained to suppress sublattice beating.

That is stronger than “trajectory physics fails on staggered,” but weaker than
“full Newton closure is retained on the staggered lane.”

What this note still does **not** claim:

1. a self-consistent two-body closure
2. a both-masses law
3. irregular-graph transfer
4. replacement of the force-based canonical staggered card

## Caveats

- This does **not** establish a full `F ∝ M / r^2` law on the staggered lane.
- It does **not** settle the both-masses question.
- It does **not** transfer automatically to irregular graph families.
- The surface is calibrated:
  - `d=2` is excluded
  - packet width matters
  - open boundaries are part of the fix

The duplicated `side=12` and `side=16` rows indicate that on this short-time,
central-window surface the packet does not yet feel the boundary; that is
useful for stability, but it also means this is a local bulk result rather
than a broad finite-size study.

## Bottom line

This lane answers the immediate architecture question cleanly:

- **Wilson is not the only architecture with a Newton-compatible distance law**
- **staggered can do it too**
- but only with an observable that respects the staggered architecture’s
  sublattice structure

The next honest step, if this is pushed further, is not another raw-centroid
sweep. It is one of:

- a staggered both-masses law on the same blocked readout
- a self-consistent staggered two-body observable
- or a larger finite-size study that turns this from a bounded frontier win
  into a retained staggered trajectory note
