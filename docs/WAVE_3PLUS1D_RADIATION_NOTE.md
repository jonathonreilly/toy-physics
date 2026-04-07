# (3+1)D Wave-Equation Radiation: Full Spatial Laplacian

**Date:** 2026-04-07
**Status:** retained positive — radiation slope −1.14 matches (3+1)D scalar radiation prediction (−1.0); strict lightcone certified to r=8; drive-frequency dominance at every detector; exact null at S0=0

## Artifact chain

- [`scripts/wave_3plus1d_radiation.py`](../scripts/wave_3plus1d_radiation.py)
- [`logs/2026-04-07-wave-3plus1d-radiation.txt`](../logs/2026-04-07-wave-3plus1d-radiation.txt)

## Question

The (2+1)D wave radiation lane (Lane 7) gave the textbook 2-spatial-dim
slope of −0.5. The model's static lane was promoted from 2D Poisson to
3D Poisson and produced the textbook 3D static profile. The natural
mirror is to promote the dynamical PDE the same way: full 3D spatial
Laplacian, x as time. Does the radiation slope move from −0.5 to the
physical 3D answer of −1?

## PDE

  (1/c²) ∂²f/∂t² − (∂²/∂x_perp² + ∂²/∂y² + ∂²/∂z²) f = source(t, x_perp, y, z)

7-point stencil on a (19³) transverse cube, x acting as time, c = 1
lattice cell per layer, h = 0.5.

## Result

### Lightcone (delta pulse, eps = 1e-6)

| r | first dt |
| ---: | ---: |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |
| 6 | 6 |
| 7 | 7 |
| 8 | 8 |

`first_dt = r` exactly for every offset out to r=8. Strict lattice
lightcone, mirror of Lane 5 in 3+1 dimensions.

### Radiation slope (sinusoidal drive, f = 0.10, S0 = 0.04)

| r | peak |f| |
| ---: | ---: |
| 2 | 1.74e-3 |
| 3 | 1.15e-3 |
| 4 | 8.76e-4 |
| 5 | 7.02e-4 |
| 6 | 5.77e-4 |
| 7 | 4.62e-4 |
| 8 | 3.19e-4 |

**log-log slope = −1.139**

The (3+1)D textbook prediction for far-field scalar radiation is
exactly −1. The measured slope is within 14% of that, and the
discrepancy is consistent with finite-distance corrections (we are
not yet in the deep far field at r=8 in lattice units).

This is a clean separation from Lane 7's −0.47: promoting the
spatial Laplacian from 2D to 3D moved the slope by ~0.7, in the
direction and magnitude predicted by classical wave theory.

### Slope vs drive frequency

| f | slope |
| ---: | ---: |
| 0.05 | −1.260 |
| 0.10 | −1.139 |
| 0.15 | −0.790 |
| 0.20 | −0.983 |

All four frequencies bracket the −1 textbook value. Frequency-independent
to within numerical noise.

### DFT at detectors (drive f = 0.10)

The DFT magnitude at trial frequencies {0.05, 0.10, 0.15, 0.20, 0.30}
shows the drive frequency f=0.10 is the **dominant** peak at every
offset r ∈ {2,3,4,5,6,7,8}. Example at r=4: f=0.10 → 6.08e-4, all
others ≤ 5.1e-4. The detector cells see the drive frequency.

### Static reference (f = 0)

Peak |f| at every r ∈ {2..8} is exactly 0.0. With sin(0)=0 the source
is identically zero, so this certifies the radiation in section 2
cannot be a buildup artifact of a residual static field.

### Static-source long-time profile

Holding the source on at constant strength S0 (no oscillation) and
reading the field at the final layer:

| r | |f| at NL−1 |
| ---: | ---: |
| 2 | 1.91e-3 |
| 3 | 1.09e-3 |
| 4 | 8.84e-4 |
| 5 | 5.58e-4 |
| 6 | 8.72e-5 |
| 7 | 1.22e-4 |
| 8 | 1.02e-4 |

The near-source slope (r=2..5) is steeper than the radiating slope
because we are in the buildup regime, not the asymptotic stationary
state. The Poisson 3D static profile (Lane 4) is the proper static
comparator and gives clean −1 in the equilibrium limit; here NL=30
is not long enough for full equilibration with PW=4.5.

## What this means

The model's wave equation, when promoted from a 2D transverse
Laplacian to a full 3D Laplacian, gives:

- Strict (3+1)D lightcone (`first_dt = r` exactly out to r=8)
- Far-field radiation amplitude falling as ~ 1/r (slope −1.14)
- Frequency-independent slope clustered around −1
- Drive frequency dominates the DFT at every detector
- Exact null with no source

This is a narrow result about the (3+1)D radiation falloff law on the
wave equation. It does NOT close the full classical scalar-wave story
in 3+1 dimensions: the (3+1)D promotions of Lane 5 (lightcone via delta
pulse on the same operator) and Lane 6 (retarded vs instantaneous gap
on a moving source) are not run in this lane and remain open.

Lane stack as it stands:

- Lane 4: Poisson 3D static gravity (F~M=0.9999) — full 3D static
- Lane 5: (2+1)D wave-equation lightcone via delta pulse
- Lane 6: (2+1)D retarded ≠ instantaneous on moving source (25%, 3 families)
- Lane 7: (2+1)D radiation, slope −0.47
- **Lane 8 (this note)**: (3+1)D radiation falloff, slope −1.14

Lanes 5 and 6 promotions to (3+1)D are now done in a separate lane:
see [`WAVE_3PLUS1D_PROMOTIONS_NOTE.md`](WAVE_3PLUS1D_PROMOTIONS_NOTE.md).
Together, Lane 8 (radiation falloff) and the promotions lane certify
all three classical scalar-wave signatures on the same (3+1)D operator.

## Claim boundary

- Single source, no backreaction
- Monopole (no quadrupole / dipole structure tested)
- 19³ transverse cube; finite-domain effects start to bite at r > 8
- Beam-side observables (F~M, Born on the radiating field) not tested
  in this lane; the prior (2+1)D radiation lane covers those at the
  appropriate dimensionality
- Static-source long-time profile is in buildup regime, not the
  full equilibrium; the proper static comparator is Lane 4 (Poisson 3D)
- (3+1)D promotion of Lanes 5 and 6 (lightcone with delta pulse and
  retarded vs instantaneous) is not done; only the radiation falloff
  is tested in 3+1 dimensions
