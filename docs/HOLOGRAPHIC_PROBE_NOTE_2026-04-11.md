# Holographic Boundary-Law Probe (Retained Bounded Note)

## Status

`bounded-retained`

This probe supports a bounded many-body-style boundary-law statement on the 2D
periodic staggered lattice using the Dirac-sea correlation-matrix construction.
It does **not** establish holography in the stronger AdS/CFT or quantum-gravity
sense.

## Runner

- Script: [frontier_holographic_probe.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_holographic_probe.py)
- Environment: `/tmp/physics_venv`
- Date rerun: `2026-04-11`

## Method

For each 2D periodic lattice with side `8, 10, 12, 14`:

1. Evolve a staggered-fermion wavepacket for `30` CN steps.
2. Build the final Hamiltonian with either self-gravity (`G=10`) or free
   evolution (`G=0`).
3. Diagonalize the Hamiltonian and fill the negative-energy modes (Dirac sea).
4. Construct the one-body correlation matrix `C = V_filled V_filled^dagger`.
5. Restrict `C` to BFS-ball regions `A` of radius `R`.
6. Compute the free-fermion entanglement entropy from the restricted
   correlation matrix eigenvalues.
7. Compare linear fits of entropy `S` versus boundary size `|bnd|` and region
   size `|A|`.

This is a correlation-matrix boundary-law probe on a fixed lattice. It is not a
geometric or topological superposition result.

## Exact rerun numbers

### Global fits

Self-gravity (`G=10`):

- `S vs |boundary|`: slope `0.184363`, intercept `-1.6204`, `R^2 = 0.968212`
- `S vs |A|`: slope `0.077597`, intercept `1.0093`, `R^2 = 0.932788`
- Boundary fit preferred over volume fit

Free (`G=0`):

- `S vs |boundary|`: slope `0.210599`, intercept `-0.4811`, `R^2 = 0.999509`
- `S vs |A|`: slope `0.085619`, intercept `2.6319`, `R^2 = 0.898426`
- Boundary fit preferred over volume fit

Gravity modification:

- area-law coefficient ratio `(gravity/free) = 0.8754`
- coefficient shift `-12.46%`
- `Delta S = S_grav - S_free`:
  - mean `-1.912087`
  - std `0.511690`
  - min `-2.593837`
  - max `-0.937014`

### Schmidt-rank scaling

Self-gravity (`G=10`):

- rank vs boundary: slope `1.4729`, `R^2 = 0.9853`
- rank vs volume: slope `0.6153`, `R^2 = 0.9350`

Free (`G=0`):

- rank vs boundary: slope `1.6762`, `R^2 = 0.9842`
- rank vs volume: slope `0.6999`, `R^2 = 0.9333`

In both cases, Schmidt rank tracks boundary more cleanly than volume.

### Per-lattice-size fit comparison

Self-gravity (`G=10`):

- side `8`: `R^2_bnd = 0.9977`, `R^2_vol = 0.8534`
- side `10`: `R^2_bnd = 0.9908`, `R^2_vol = 0.9223`
- side `12`: `R^2_bnd = 0.9895`, `R^2_vol = 0.9408`
- side `14`: `R^2_bnd = 0.9901`, `R^2_vol = 0.9485`

Free (`G=0`):

- side `8`: `R^2_bnd = 0.9997`, `R^2_vol = 0.8205`
- side `10`: `R^2_bnd = 0.9998`, `R^2_vol = 0.8643`
- side `12`: `R^2_bnd = 0.9997`, `R^2_vol = 0.8874`
- side `14`: `R^2_bnd = 0.9998`, `R^2_vol = 0.9025`

Every tested lattice size favors boundary scaling over volume scaling.

## Strongest honest claim

Within this Dirac-sea correlation-matrix construction on the 2D periodic
staggered lattice, entanglement entropy and Schmidt rank scale more cleanly
with region boundary size than with region volume, both in the free control and
under self-gravity (`G=10`). Gravity preserves the boundary-law preference while
reducing the fitted boundary-law coefficient by about `12.5%`.

## Boundaries of the claim

- This is a fixed-lattice, correlation-matrix probe.
- It is many-body-style because it fills negative-energy modes, but it is still
  a lattice-model construction, not a continuum quantum-gravity derivation.
- It does **not** prove holography in the stronger sense.
- It does **not** establish a Bekenstein-Hawking law or an AdS/CFT duality.
- The right interpretation is a bounded boundary-law result worth preserving for
  later publication triage.
