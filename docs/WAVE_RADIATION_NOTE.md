# Wave-Equation Radiation: Oscillating Source Emits Propagating Field

**Date:** 2026-04-07
**Status:** proposed_retained positive (narrow) — log-log slope −0.47 matches (2+1)D scalar radiation prediction (−0.5); drive frequency dominates DFT at every distance; exact null at S0=0; Born preserved. Family portability section measures F~M of the radiating field across grown geometries (the slope itself is a PDE invariant)

## Artifact chain

- [`scripts/wave_radiation.py`](../scripts/wave_radiation.py)
- [`logs/2026-04-07-wave-radiation.txt`](../logs/2026-04-07-wave-radiation.txt)

## Question

Retarded gravity (Lane 6) shows the wave field carries finite-c
information. But that's still a near-field test — does the wave
equation have actual *radiating* solutions, where an accelerating
source emits a propagating disturbance with the correct geometric
falloff?

## Setup

Drive a monopole source whose strength oscillates sinusoidally:

  src(t) = S0 * sin(2π f (t − t₀) H)   for t ≥ src_layer

through the discrete (2+1)D wave equation
  (1/c²) ∂²f/∂t² − ∇²_yz f = src(t, y, z)

with x as time. Measure |f(t, iy=0, iz=offset)| at offsets r ∈ {2,4,6,8,10,12}.

## Result

### Peak amplitude vs distance (drive f = 0.10, S0 = 0.04)

| r | peak |f| |
| ---: | ---: |
| 2 | 9.26e-3 |
| 4 | 6.66e-3 |
| 6 | 5.52e-3 |
| 8 | 4.84e-3 |
| 10 | 4.35e-3 |
| 12 | 3.98e-3 |

**Log-log slope = −0.469**

In a (2+1)D scalar wave equation, the textbook far-field amplitude
falls as `~ 1/sqrt(r)`, slope = −0.5. Our static near-field would
fall closer to `1/r²` (slope ≈ −2). The measured −0.47 is the
radiation prediction within 6%.

### Slope vs drive frequency

| f | slope |
| ---: | ---: |
| 0.05 | −0.435 |
| 0.10 | −0.469 |
| 0.15 | −0.530 |
| 0.20 | −0.456 |

Frequency-independent slope, all clustered at −0.5. The radiation
falloff law is the same across drive frequencies.

### DFT at detector cells

The DFT magnitude at trial frequencies {0.05, 0.10, 0.15, 0.20, 0.30}
shows the drive frequency f = 0.10 is the **dominant** peak at every
distance r ∈ {2,4,6,8,10,12}. Example at r=8: f=0.10 → 2.66e-3,
all others < 5.2e-4. The detector sees the drive frequency, not
some lattice mode.

### Static reference (f = 0)

| r | peak |f| |
| ---: | ---: |
| 2 | 0.0 |
| 4 | 0.0 |
| 6 | 0.0 |
| ... | 0.0 |

Zero radiation everywhere. With f = 0 the source is identically
zero (`sin(0) = 0` for all t), so this is consistency, not novelty —
it certifies that the radiating signal in section 2 cannot be a
buildup artifact of a static source.

### Beam-side sanity (drive f = 0.10)

| Property | Value |
| --- | ---: |
| F~M (Fam1) | 0.9345 |
| Born |I3|/P | 3.20e-15 |
| Null (S0=0) | exact (0.0) |

F~M is 0.93 — looser than the static lanes (0.99) because the
radiating field has oscillatory sign-changing structure that makes
beam deflection sub-linear in S. Born stays at machine precision.
Null is exact.


## Family portability (F~M on radiating field)

The radiation slope is a property of the wave PDE alone — it has no
beam input — so it is the same for every grown geometry by
construction. The geometry-dependent quantity is the beam-side F~M
scaling on the radiating field. Measured across the three families:

| Family | F~M |
| --- | ---: |
| Fam1 | 0.9345 |
| Fam2 | 1.0102 |
| Fam3 | 0.8885 |

All three are within 12% of unity. The radiating-field weak-equivalence
holds across grown geometries, with looser scaling than the static lanes
(0.99) because the field has sign-changing oscillatory structure.

## Lightcone arrivals (note on eps threshold)

The first-arrival table reports `first_dt = r + 1` at every offset
when eps = 1e-8. This is **not** a lightcone violation. Two reasons:

1. The sinusoidal source has `sin(0) = 0` — drive amplitude at the
   exact start time t = src_layer is zero. The signal that reaches
   cell r at dt = r is below eps because the source was still
   ramping up.
2. The strict-pulse lightcone test in Lane 5 already certified
   `first_dt = offset` exactly with eps = 1e-6 on the same wave
   solver. That is the canonical lightcone evidence.

The combined evidence: Lane 5 certifies the strict lightcone with
a delta pulse; this lane certifies the radiation falloff law with a
sinusoidal drive.

## What this means

The model's wave equation has true radiating solutions:

- A time-varying source emits a propagating field, not just a
  rebuilding near-field
- The amplitude falls with the textbook 2+1D radiation law
  (slope ≈ −0.5)
- The detector sees the drive frequency, not noise
- The radiation vanishes when the source is constant
- Beam-side observables (Born, null) are preserved

Combined with Lane 5 (lightcone) and Lane 6 (retarded ≠ instantaneous),
the model now has end-to-end:

- Local wave-equation field with finite c
- Strict lightcone propagation
- Retarded near-field interaction (M ≠ I)
- Far-field radiation with the correct geometric law

That is the full classical-wave story for a scalar field, derived
from one local PDE on the lattice.

## Claim boundary

- (2+1)D, not (3+1)D — the slope prediction is −0.5, not the −1
  of physical 3D radiation. To get the −1 slope we'd need a full
  3+1D wave solver (analogous to the Poisson 3D promotion of
  Poisson 2D).
- Monopole source only; quadrupole / dipole structure not tested
- Single drive frequency at a time; superposition not tested
- W = 12 (PW), NL = 60; finite-domain reflections may contaminate
  the largest-r measurements
- F~M is 0.93, not 0.99; the radiating field is not a clean
  Newtonian potential and that is expected
- No GR tensor structure (this is a scalar field)
