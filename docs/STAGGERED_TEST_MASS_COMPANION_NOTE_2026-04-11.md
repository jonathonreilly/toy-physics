# Staggered Test-Mass / Source-Mass Companion on an Open 3D Lattice

**Date:** 2026-04-11  
**Status:** bounded frontier companion on `claude/sleepy-cerf`  
**Script:** `scripts/frontier_staggered_test_mass_companion.py`

## Question

Can the primary open-cubic staggered architecture support a bounded
**source-mass scaling companion** that is as close as possible to the retained
Wilson weak-field test-mass lane, without pretending to close a both-masses
law?

That means:

- one static source packet
- one normalized test packet
- source-only Poisson field
- a weak-field operating point
- a trajectory observable that respects staggered sublattice structure

## Design

Open 3D cubic staggered lattice with parity-correct scalar coupling:

- `H_diag = (m + Phi) * epsilon(x)`
- source packet:
  - Gaussian
  - **not** normalized
  - amplitude sweep changes `M_source = sum |psi_source|^2`
- test packet:
  - Gaussian
  - normalized
  - evolved in the source-only static field
- field solve:
  - `(L + mu^2 I) Phi = G |psi_source|^2`
- free control:
  - identical test packet with `Phi = 0`

Two observables are frozen:

1. **Exact inward force**
   - `F_toward = -F_x`
   - test packet sits to the right of the source, so positive means toward the
     source

2. **Blocked-envelope early acceleration**
   - `2x2x2` blocked centroid on the right half
   - `dx_mut = x_free - x_grav`
   - early-time second difference of `dx_mut`

This is deliberately the same observable hierarchy as the retained staggered
open-cubic companions:

- exact force first
- blocked trajectory readout second

## Audited surface

- sides: `14, 16, 18`
- separations: `d = 4, 5, 6`
- source amplitudes: `A = 0.4, 0.6, 0.8, 1.0, 1.2`
- `mass = 0.30`
- `G = 0.005`
- `mu2 = 0.001`
- `dt = 0.08`
- `N_steps = 10`
- `sigma_source = 1.30`
- `sigma_test = 1.10`

Why this counts as weak field on this surface:

- `phi_peak` stays in the range
  - `1.1053e-03 .. 3.6711e-02`
- with bare mass `m = 0.30`, the largest audited `phi_peak / m` is about
  `0.12`

So this is well below the strong-backreaction regime that would contaminate a
source-mass fit.

## Exact result

Every audited row is inward in both observables:

- inward exact-force rows: `45/45`
- inward blocked-accel rows: `45/45`

### Source-mass exponent by side and separation

The exact-force source-mass law is numerically exact on every row:

| side | d | `|F_toward| ~ M_source^beta_F` | `R^2` |
|---|---:|---:|---:|
| 14 | 4 | `1.0001` | `1.000000` |
| 14 | 5 | `1.0001` | `1.000000` |
| 14 | 6 | `1.0001` | `1.000000` |
| 16 | 4 | `1.0001` | `1.000000` |
| 16 | 5 | `1.0001` | `1.000000` |
| 16 | 6 | `1.0000` | `1.000000` |
| 18 | 4 | `1.0000` | `1.000000` |
| 18 | 5 | `1.0000` | `1.000000` |
| 18 | 6 | `1.0000` | `1.000000` |

Range:

- `beta_F = 1.0000 .. 1.0001`

The blocked-envelope trajectory companion is also strongly linear:

| side | d | `|a_block| ~ M_source^beta_a` | `R^2` |
|---|---:|---:|---:|
| 14 | 4 | `1.0197` | `0.999965` |
| 14 | 5 | `1.0194` | `0.999965` |
| 14 | 6 | `1.0193` | `0.999966` |
| 16 | 4 | `1.0134` | `0.999983` |
| 16 | 5 | `1.0133` | `0.999983` |
| 16 | 6 | `1.0131` | `0.999984` |
| 18 | 4 | `1.0095` | `0.999991` |
| 18 | 5 | `1.0094` | `0.999992` |
| 18 | 6 | `1.0093` | `0.999992` |

Range:

- `beta_a = 1.0093 .. 1.0197`

### Representative rows

- `side=14, d=4, A=1.2`
  - `M_source = 17.6164`
  - `phi_peak = 3.6378e-02`
  - `F_toward = +4.1831e-04`
  - `a_block = +8.8242e-03`

- `side=16, d=5, A=1.0`
  - `M_source = 12.2336`
  - `phi_peak = 1.8207e-02`
  - `F_toward = +1.9202e-04`
  - `a_block = +7.9467e-03`

- `side=18, d=6, A=0.8`
  - `M_source = 7.8295`
  - `phi_peak = 8.7544e-03`
  - `F_toward = +8.6515e-05`
  - `a_block = +3.8145e-03`

## Interpretation

This closes a **bounded source-mass companion** on the primary staggered
architecture.

What is strong:

- the exact-force source-mass law is effectively exact on the audited surface
- the blocked-envelope trajectory companion is also close to linear and stays
  inward on every row
- the result is portable across:
  - three sides
  - three separations
  - five source amplitudes

What this means physically:

- on the open-cubic staggered surface, once the source is held static and the
  test packet is normalized, the source-mass channel is clean
- the primary staggered architecture is therefore not limited to external
  distance-law reproduction only; it also supports a bounded weak-field
  source-mass companion

## Exact boundary

This note is intentionally narrower than the retained Wilson test-mass package.

It does **not** claim:

1. a both-masses law
2. a self-consistent two-body mass law
3. a standalone distance-law closure
4. irregular-graph transfer
5. replacement of the retained staggered open-cubic distance companion

Why not:

- the source packet is static, so this is a **test-mass/source-mass** lane
- the distance exponent on this short-window blocked readout is not the target
  observable here
- the self-consistent staggered two-body lane remains a separate, force-led
  note with its own limitations

The safe reading is:

> On the primary open-cubic staggered architecture, a weak-field static-source
> companion gives exact source-mass scaling in the force observable and
> near-linear source-mass scaling in the blocked-envelope trajectory observable,
> across a bounded side-and-separation surface.

## Relation to the existing retained package

This is the primary-architecture analogue of the retained Wilson weak-field
companion, but it is not a replacement for it.

The Wilson package still carries:

- the same-convention continuum companion
- the bounded test-mass distance-law story on that architecture

This new staggered note adds:

- a primary-architecture weak-field **source-mass** companion
- using the staggered-safe blocked-envelope readout rather than a raw centroid

## Bottom line

The bounded frontier conclusion is:

> the primary open-cubic staggered architecture supports a clean weak-field
> source-mass companion, but this is still a source-only test-mass lane, not a
> both-masses or self-consistent mass-law closure.
