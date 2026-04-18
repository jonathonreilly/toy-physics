# Staggered Self-Consistent Two-Body Channel on an Open 3D Lattice

**Date:** 2026-04-11  
**Status:** bounded companion on `main`
**Script:** `scripts/frontier_staggered_self_consistent_two_body.py`

## Question

Can the primary staggered architecture support a **genuine self-consistent
two-body channel**, rather than only external-source Newton reproduction?

This lane is the missing primary-architecture follow-up to:

- the external-source staggered Newton reproduction
- the Wilson open-surface two-body lane

The target was not “another external well.” The target was:

- two separate staggered orbitals
- one shared self-consistent Poisson field
- self-only controls
- an observable that respects staggered sublattice structure

## Design

Open 3D cubic staggered lattice with parity-correct scalar coupling:

- `H_diag = (m + Phi) * epsilon(x)`
- two separate orbitals `psi_A`, `psi_B`
- shared field:
  - `Phi = Phi_A + Phi_B`
  - `(L + mu^2 I) Phi_A = G |psi_A|^2`
  - `(L + mu^2 I) Phi_B = G |psi_B|^2`
- self-only controls:
  - `psi_A` evolves under `Phi_A`
  - `psi_B` evolves under `Phi_B`

Two observable layers were audited:

1. **Exact partner-force channel**
   - on A: force from `Phi_B` only
   - on B: force from `Phi_A` only
   - “toward” is defined as positive:
     - A is on the left, so inward is `+x`
     - B is on the right, so inward is `-x`

2. **Blocked trajectory channel**
   - `2x2x2` blocked centroids on the left/right halves
   - mutual inward shift:
     - `dxA_mut = xA_shared - xA_self`
     - `dxB_mut = xB_self - xB_shared`
   - positive means extra inward motion under the shared field

## Audited surface

- sides: `12, 14, 16`
- separations: `d = 3, 4, 5, 6, 7`
- `mass = 0.30`
- `G = 50.0`
- `mu2 = 0.001`
- `dt = 0.08`
- `N_steps = 6`
- packet width: `sigma = 0.80`

The packet width is a real calibration choice here:

- broad packets (`sigma ~ 1.3`) soften the self-consistent partner-force law
  toward `d^-1.6`
- this narrower surface (`sigma = 0.80`) recovers a near-Newton force law

That means this is a **bounded calibrated surface**, not yet a universal
staggered two-body closure.

## Exact outputs

### side = 12

- `d=3`: `F_A(t0)=+4.9557e-01`, `F_B(t0)=+4.9557e-01`, `F_early=+4.9555e-01`, `dxA_mut=-1.5381e-03`, `dxB_mut=+2.0548e-03`, `block_early=+1.5846e-04`
- `d=4`: `F_A(t0)=+2.8695e-01`, `F_B(t0)=+2.8695e-01`, `F_early=+2.8695e-01`, `dxA_mut=-1.5404e-03`, `dxB_mut=+1.5540e-03`, `block_early=+7.8614e-06`
- `d=5`: `F_A(t0)=+1.8543e-01`, `F_B(t0)=+1.8543e-01`, `F_early=+1.8543e-01`, `dxA_mut=-1.8609e-03`, `dxB_mut=+1.4985e-03`, `block_early=-1.0972e-04`
- `d=6`: `F_A(t0)=+1.3118e-01`, `F_B(t0)=+1.3118e-01`, `F_early=+1.3118e-01`, `dxA_mut=-1.7390e-03`, `dxB_mut=+1.7090e-03`, `block_early=-4.4328e-06`
- `d=7`: `F_A(t0)=+9.5877e-02`, `F_B(t0)=+9.5877e-02`, `F_early=+9.5877e-02`, `dxA_mut=-1.4739e-04`, `dxB_mut=+4.3521e-04`, `block_early=+1.0048e-04`

Fits:

- `|F_partner(t0)| ~ d^-1.935` with `R^2 = 0.9999`
- `|F_partner(early)| ~ d^-1.935` with `R^2 = 0.9999`

### side = 14

- `d=3`: `F_A(t0)=+4.9006e-01`, `F_B(t0)=+4.9006e-01`, `F_early=+4.9003e-01`, `dxA_mut=+3.0232e-04`, `dxB_mut=+2.4505e-04`, `block_early=+1.1521e-04`
- `d=4`: `F_A(t0)=+2.8115e-01`, `F_B(t0)=+2.8115e-01`, `F_early=+2.8114e-01`, `dxA_mut=+2.4352e-03`, `dxB_mut=-1.3380e-03`, `block_early=+2.6551e-04`
- `d=5`: `F_A(t0)=+1.8025e-01`, `F_B(t0)=+1.8025e-01`, `F_early=+1.8025e-01`, `dxA_mut=+8.3624e-03`, `dxB_mut=-7.5154e-03`, `block_early=+2.6953e-04`
- `d=6`: `F_A(t0)=+1.2762e-01`, `F_B(t0)=+1.2762e-01`, `F_early=+1.2762e-01`, `dxA_mut=+1.1983e-02`, `dxB_mut=-1.1934e-02`, `block_early=+1.5320e-05`
- `d=7`: `F_A(t0)=+9.4718e-02`, `F_B(t0)=+9.4718e-02`, `F_early=+9.4718e-02`, `dxA_mut=+7.7746e-03`, `dxB_mut=-8.1980e-03`, `block_early=-1.6973e-04`

Fits:

- `|F_partner(t0)| ~ d^-1.942` with `R^2 = 1.0000`
- `|F_partner(early)| ~ d^-1.942` with `R^2 = 1.0000`

### side = 16

- `d=3`: `F_A(t0)=+4.8676e-01`, `F_B(t0)=+4.8676e-01`, `F_early=+4.8669e-01`, `dxA_mut=-4.4075e-03`, `dxB_mut=+4.7683e-03`, `block_early=+6.3426e-04`
- `d=4`: `F_A(t0)=+2.7742e-01`, `F_B(t0)=+2.7742e-01`, `F_early=+2.7742e-01`, `dxA_mut=-8.5876e-03`, `dxB_mut=+8.5189e-03`, `block_early=+3.2597e-05`
- `d=5`: `F_A(t0)=+1.7653e-01`, `F_B(t0)=+1.7653e-01`, `F_early=+1.7653e-01`, `dxA_mut=-4.5631e-03`, `dxB_mut=+4.1731e-03`, `block_early=-4.2355e-04`
- `d=6`: `F_A(t0)=+1.2441e-01`, `F_B(t0)=+1.2441e-01`, `F_early=+1.2441e-01`, `dxA_mut=-2.0937e-04`, `dxB_mut=+1.6606e-04`, `block_early=-1.5834e-05`
- `d=7`: `F_A(t0)=+9.2436e-02`, `F_B(t0)=+9.2436e-02`, `F_early=+9.2436e-02`, `dxA_mut=-5.1731e-03`, `dxB_mut=+5.4787e-03`, `block_early=+3.9312e-04`

Fits:

- `|F_partner(t0)| ~ d^-1.965` with `R^2 = 0.9999`
- `|F_partner(early)| ~ d^-1.965` with `R^2 = 0.9999`

### Global summary

- partner-force attractive rows: `15/15`
- blocked inward rows: `10/15`
- global `|F_partner(t0)| ~ d^-1.947` with `R^2 = 0.9992`
- global `|F_partner(early)| ~ d^-1.947` with `R^2 = 0.9992`

## What this closes

This closes one important gap on the primary staggered architecture:

- there is a **real self-consistent two-body channel**
- it is visible in an exact, partner-only force observable
- it is near-Newton on this calibrated open-cubic surface

That is materially stronger than external-source reproduction alone.

## What still fails

The blocked trajectory channel is still not the retained readout.

Why:

- `dxA_mut` and `dxB_mut` often have opposite signs on the same row
- the mean blocked inward shift is tiny (`~1e-4`)
- the blocked inward sign survives only `10/15` rows

So the failure mode is clean:

- **force channel works**
- **trajectory channel still does not cleanly survive the staggered architecture**

That is consistent with the broader repo story: on staggered lattices, exact
force observables are much cleaner than centroid-style trajectory observables.

## Retention boundary

This remains bounded because it does **not** close full Newton on the
primary architecture.

What is still missing:

1. a staggered **both-masses** law on the same surface
2. a trajectory observable that survives without this force-first fallback
3. extension beyond the open cubic calibration surface

So the safe statement is:

> the primary staggered architecture supports a genuine self-consistent
> two-body attraction channel in an exact partner-force observable, with a
> near-Newton distance law on a calibrated open-cubic surface, but the
> trajectory-level mutual channel remains noisy.

## Bottom line

This lane improves the repo in a precise way:

- external-source staggered Newton reproduction is no longer the ceiling
- staggered now has a **self-consistent two-body** positive
- but it is still a **force-led** positive, not a full trajectory closure
