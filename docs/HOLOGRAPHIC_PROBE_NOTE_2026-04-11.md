# Holographic Boundary-Law Probe (Bounded Companion Note)

**Status:** bounded - bounded or caveated result note
## Status

`bounded companion`

This probe supports a bounded many-body-style boundary-law statement on the 2D
periodic staggered lattice using the Dirac-sea correlation-matrix construction.
It does **not** establish holography in the stronger AdS/CFT or quantum-gravity
sense.

## Runner

- Script: [frontier_holographic_probe.py](/Users/jonreilly/Projects/Physics/scripts/frontier_holographic_probe.py)
- Environment: `/tmp/physics_venv`
- Date rerun: `2026-04-18`

This note reflects the current-main minimum-image rerun on the periodic surface.

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

- `S vs |boundary|`: slope `0.186053`, intercept `-1.6446`, `R^2 = 0.970131`
- `S vs |A|`: slope `0.078409`, intercept `1.0056`, `R^2 = 0.937046`
- Boundary fit preferred over volume fit

Free (`G=0`):

- `S vs |boundary|`: slope `0.211399`, intercept `-0.5149`, `R^2 = 0.999375`
- `S vs |A|`: slope `0.085955`, intercept `2.6095`, `R^2 = 0.898533`
- Boundary fit preferred over volume fit

Gravity modification:

- area-law coefficient ratio `(gravity/free) = 0.8801`
- coefficient shift `-11.99%`
- `Delta S = S_grav - S_free`:
  - mean `-1.876233`
  - std `0.489731`
  - min `-2.538747`
  - max `-0.935096`

### Schmidt-rank scaling

Self-gravity (`G=10`):

- rank vs boundary: slope `1.4684`, `R^2 = 0.9790`
- rank vs volume: slope `0.6136`, `R^2 = 0.9296`

Free (`G=0`):

- rank vs boundary: slope `1.6455`, `R^2 = 0.9756`
- rank vs volume: slope `0.6862`, `R^2 = 0.9227`

In both cases, Schmidt rank tracks boundary more cleanly than volume.

### Per-lattice-size fit comparison

Self-gravity (`G=10`):

- side `8`: `R^2_bnd = 0.9951`, `R^2_vol = 0.8685`
- side `10`: `R^2_bnd = 0.9883`, `R^2_vol = 0.9276`
- side `12`: `R^2_bnd = 0.9882`, `R^2_vol = 0.9431`
- side `14`: `R^2_bnd = 0.9893`, `R^2_vol = 0.9501`

Free (`G=0`):

- side `8`: `R^2_bnd = 0.9997`, `R^2_vol = 0.8119`
- side `10`: `R^2_bnd = 0.9999`, `R^2_vol = 0.8642`
- side `12`: `R^2_bnd = 0.9999`, `R^2_vol = 0.8871`
- side `14`: `R^2_bnd = 0.9999`, `R^2_vol = 0.9035`

Every tested lattice size favors boundary scaling over volume scaling.

## Strongest honest claim

Within this corrected minimum-image rerun of the Dirac-sea
correlation-matrix construction on the 2D periodic staggered lattice,
entanglement entropy and Schmidt rank scale more cleanly with region boundary
size than with region volume, both in the free control and under self-gravity
(`G=10`). Gravity preserves the boundary-law preference while reducing the
fitted boundary-law coefficient by about `12.0%`.

## Boundaries of the claim

- This is a fixed-lattice, correlation-matrix probe.
- It is many-body-style because it fills negative-energy modes, but it is still
  a lattice-model construction, not a continuum quantum-gravity derivation.
- It does **not** prove holography in the stronger sense.
- It does **not** establish a Bekenstein-Hawking law or an AdS/CFT duality.
- The right interpretation is a bounded boundary-law result worth preserving for
  later publication triage.
