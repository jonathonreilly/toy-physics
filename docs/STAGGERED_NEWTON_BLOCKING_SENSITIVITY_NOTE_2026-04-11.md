# Staggered Newton Blocking Sensitivity on the Open 3D Cubic Surface

**Date:** 2026-04-11  
**Status:** bounded companion on `main`
**Script:** `scripts/frontier_staggered_newton_blocking_sensitivity.py`

## Question

Does the Newton-compatible exponent in the open-cubic staggered Newton
reproduction lane depend delicately on the current `2x2x2` blocked readout, or
does it survive sensible coarse-grained trajectory observables and lattice
sizes?

This note stays strictly within the same bounded surface as the existing
staggered Newton reproduction lane:

- open 3D cubic staggered lattice
- external attractive source
- parity-coupled staggered Hamiltonian
- early-time trajectory response only

It does **not** touch the active staggered both-masses lane.

## Surface

- sides: `12, 14, 16`
- source offsets: `d = 3, 4, 5, 6`
- `mass = 0.30`
- `G = 50.0`
- `source_strength = 5e-4`
- `dt = 0.10`
- `N_steps = 12`
- packet width: `sigma = 1.30`

## Readouts tested

Four `z`-trajectory observables were compared:

1. `raw`
   - no blocking
   - site-level centroid
2. `z2`
   - axial coarse graining only
   - block shape `(1, 1, 2)`
3. `cube2`
   - the current retained staggered trajectory readout
   - block shape `(2, 2, 2)`
4. `cube4`
   - intentionally over-coarse stress test
   - block shape `(4, 4, 4)`

Each row measures the free-vs-gravitating early-time acceleration and fits
`|a| ~ d^alpha`.

## Exact outputs

### Raw centroid

- side `12`: `alpha = -1.914`, `R^2 = 0.9999`
- side `14`: `alpha = -2.104`, `R^2 = 0.9975`
- side `16`: `alpha = -1.914`, `R^2 = 0.9999`
- global: `alpha = -1.977`, `R^2 = 0.8411`
- all rows TOWARD: yes
- side-to-side exponent span: `0.190`

### Axial-only blocking `(1, 1, 2)`

- side `12`: `alpha = -1.975`, `R^2 = 1.0000`
- side `14`: `alpha = -1.997`, `R^2 = 0.9961`
- side `16`: `alpha = -1.975`, `R^2 = 1.0000`
- global: `alpha = -1.982`, `R^2 = 0.9232`
- all rows TOWARD: yes
- side-to-side exponent span: `0.022`

### Isotropic blocking `(2, 2, 2)`

- side `12`: `alpha = -1.975`, `R^2 = 1.0000`
- side `14`: `alpha = -1.997`, `R^2 = 0.9961`
- side `16`: `alpha = -1.975`, `R^2 = 1.0000`
- global: `alpha = -1.982`, `R^2 = 0.9232`
- all rows TOWARD: yes
- side-to-side exponent span: `0.022`

### Over-coarse blocking `(4, 4, 4)`

- side `12`: `alpha = -2.150`, `R^2 = 1.0000`
- side `14`: `alpha = -1.231`, `R^2 = 1.0000`
- side `16`: `alpha = -1.592`, `R^2 = 1.0000`
- global: `alpha = -1.658`, `R^2 = 0.2808`
- all rows TOWARD: yes
- side-to-side exponent span: `0.919`

## Interpretation

The Newton-compatible exponent is **not delicate** to the current `2x2x2`
blocking choice.

The stable result is:

- raw centroid already gives a near-Newton global exponent
- axial-only blocking and isotropic `2x2x2` blocking give essentially the same
  answer: `alpha ~= -1.98`
- the exponent remains TOWARD on every row across all three sizes

So the `2x2x2` observable is not a finely tuned one-off.

What the sweep actually shows is a cleaner and more bounded statement:

> on the open-cubic external-source staggered surface, the Newton-compatible
> exponent survives sensible trajectory readouts that suppress parity-scale
> beating, and fails only when the readout is made too coarse to resolve the
> local packet envelope.

That is stronger than the original single-observable note, but still bounded.

## Why `z2` and `cube2` coincide

For this lane the trajectory is read out along `z`, and the packet/source are
centered symmetrically in `x` and `y`. Under those conditions, the extra
coarse graining in `x` and `y` does not materially change the `z` envelope
observable. That is useful: it means the stable exponent is coming from axial
parity suppression, not from a special isotropic blocking trick.

## Why `cube4` fails

`(4, 4, 4)` is too coarse for this short-time surface. It washes together too
much of the local envelope and makes the extracted acceleration depend strongly
on how the packet sits inside the coarse block grid. The result remains
attractive but the exponent is no longer stable across sizes.

So the failure mode is **over-coarsening**, not sensitivity to the particular
`2x2x2` choice.

## Boundaries of the claim

This note does **not** establish:

- a staggered both-masses law
- a self-consistent staggered two-body law
- transfer to irregular graph families
- a retained trajectory card for the staggered lane

It only establishes blocking stability on the same external-source open-cubic
surface.

## Bottom line

On the open 3D cubic staggered surface:

- the Newton-compatible exponent survives `raw`, `z2`, and `2x2x2` readouts
- `2x2x2` is a reasonable blocked observable, not a delicate one-off
- the trajectory law breaks only when the readout is over-coarsened to
  `(4, 4, 4)`

So the next honest staggered step is **not** another blocking sweep. It is one
of:

- a staggered both-masses observable on the same bounded surface
- a self-consistent staggered two-body probe
- or a larger finite-size study that converts this bounded frontier result into
  a retained trajectory note
