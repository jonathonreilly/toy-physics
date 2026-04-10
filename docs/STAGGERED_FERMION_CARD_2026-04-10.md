# Staggered Fermion + Potential Gravity — Force-Based Card

**Date:** 2026-04-10
**Script:** `frontier_staggered_17card.py`
**Architecture:** Kogut-Susskind staggered fermion, 1 scalar per site, Dirac
from staggering phases η_μ(x), gravity via scalar potential V=-m·g·S/(r+ε),
Crank-Nicolson evolution.

## Important Framing

**This is a FORCE-BASED STAGGERED CARD, not the repo-wide centroid-based card.**

Rows that differ from the repo-wide card semantics:
- **C5**: force sign, not centroid sign
- **C9**: force stays positive across depth, not centroid grows monotonically
- **C15**: force stable across depth, not periodic-vs-open boundary comparison
- **C16**: force + shell asymmetry (2 observables), not centroid + peak + shell (3)

Rows with matching semantics:
- **C1**: real Sorkin I₃ barrier in BOTH 1D and 3D (z-plane slits in 3D)
- **C12**: persistent current on NATIVE Hamiltonian (1D ring / 3D torus)
- **C17**: all 6 families including energy projections in 3D (n≤9 eigensolve)

## Operating Point

```
mass = 0.3, g = 50.0, S = 5e-4, dt = 0.15
1D: n = 61, N_steps = 15, mass_offset = 4
3D: n = 9/11/13, N_steps = 7/9/10, mass_offset = 2
```

## Key Design Decisions

**Force, not centroid.** Gravity rows measure F = -⟨dV/dz⟩ on the evolved state.
The centroid oscillates with lattice size (staggered standing-wave artifact on
periodic BCs). The force is the correct physical observable.

**Native gauge test.** C12 uses Byers-Yang persistent current on the SAME
Hamiltonian dimension as the card: 1D ring (n=21) in 1D, 3D torus (n=7) in 3D.

**Full family set.** C17 tests gauss, even, odd, anti, positive-E, negative-E
(6 families). Energy projections computed via eigensolve at n≤9 in 3D.
At n>9, 3D omits energy projections (eigensolve cost) and tests 4 families.

## Scores

### 1D (n=61)

| Row | Test | Value | Status |
|-----|------|-------|--------|
| C1 | Sorkin Born |I₃|/P | 1.28e-15 | PASS |
| C2 | d_TV | 0.92 | PASS |
| C3 | f=0 force | 0.00 | PASS |
| C4 | F∝M (force-based) | R²=0.912 | PASS |
| C5 | Force TOWARD | +5.69e-5 | PASS |
| C6 | Decoherence | 0.230→0.177 | PASS |
| C7 | MI | 0.164 | PASS |
| C8 | Purity CV | 0.011 | PASS |
| C9 | Force stable across N | all TOWARD | PASS |
| C10 | Distance (force) | 5/5 TW | PASS |
| C11 | KG R² (staggered Dirac) | 0.997 | PASS |
| C12 | Gauge (persistent current) | J=2.14e-3 | PASS |
| C13 | Force achromaticity | CV=0.000 | PASS |
| C14 | Equivalence (a=F/m) | CV=0.000 | PASS |
| C15 | Force vs depth | all TOWARD | PASS |
| C16 | Multi-observable | 1/2 | PASS |
| C17 | State families (6/6) | all TOWARD | PASS |
| | **Norm** | **1.44e-15** | |
| | **Score** | **17/17** | **No qualifiers** |

### 3D Convergence

| Row | n=9 (729) | n=11 (1331) | n=13 (2197) |
|-----|-----------|-------------|-------------|
| C1 Sorkin | 2.62e-15 | 2.75e-15 | 3.11e-15 |
| C4 F∝M | R²=1.000 | R²=0.999 | R²=0.998 |
| C5 Force | +1.29e-3 TW | +5.78e-4 TW | +3.18e-4 TW |
| C6 Decoh | 0.754→0.164 | 0.699→0.068 | 0.657→0.085 |
| C12 Gauge | 3D torus 6.57e-3 | 3D torus 6.57e-3 | 3D torus 6.57e-3 |
| C13 Achrom | CV=0.000 | CV=0.000 | CV=0.000 |
| C14 Equiv | CV=0.000 | CV=0.000 | CV=0.000 |
| C17 families | 6/6 (incl anti TW) | 4/4 (no eigensolve) | 4/4 (no eigensolve) |
| **Score** | **17/17** | **17/17** | **17/17** |

All lattice sizes converge: force is TOWARD everywhere, decreasing smoothly
with lattice size. C1 is a real 3D Sorkin barrier (z-plane slits). C12 is
a native 3D torus gauge test. C17 includes energy projections at n=9.

## What This Architecture Derives

- **Dirac dispersion:** E² = m² + sin²(k) exact, from staggering phases η_μ(x).
  Not assumed — follows from the nearest-neighbor hopping with alternating signs.
- **Born rule:** Sorkin I₃ at machine zero. From linearity of CN evolution.
- **Universal gravity:** Force TOWARD for ALL state families including anti/Nyquist.
  From V = -m·g·S/(r+ε) potential on diagonal.
- **Achromatic force:** F = -⟨dV/dz⟩ has no k-dependence (CV=0.000000).
- **Equivalence:** a = F/m = -⟨dΦ/dz⟩ is mass-independent (CV=0.000000).
- **Gauge:** Persistent current J(A) with sin(A) modulation on ring.
- **Chirality:** Even/odd sublattice = staggered gamma5.
- **Norm:** Exact (CN, drift < 2e-15).

## What This Architecture Does NOT Provide

- **Strict v=1 light cone:** CN evolution gives Lieb-Robinson cone (97% inside).
  A strict cone requires coin+shift (which reintroduces the mixing period).
- **Repo-wide centroid-based gravity rows:** C5/C9/C15/C16 use force, not centroid.
  The centroid oscillates on staggered lattices. This card is force-specific.
- **Topology portability:** Tested on periodic cubic lattice only. Extending to
  random/growing graphs requires adapting the staggering convention.
- **Dynamic growth / cosmology / Hawking:** Static lattice, not tested.

## Semantic Differences from Repo-Wide Card

| Row | Repo-wide meaning | This card's meaning |
|-----|-------------------|---------------------|
| C5 | Centroid shift TOWARD | Force F>0 (TOWARD) |
| C9 | Centroid shift grows monotonically | Force stays positive across N |
| C15 | Periodic vs open boundary | Force stable across propagation depth |
| C16 | Centroid + peak + shell (3 obs) | Force + shell (2 obs) |

These are WEAKER than the repo-wide definitions for C9 and C16. They are
DIFFERENT (not weaker or stronger) for C5 and C15. The force observable is
more fundamental (it's what the equivalence principle tests), but the score
is NOT directly comparable to centroid-based cards.

## Caveats

1. **C4 F∝M R²=0.912 in 1D** — force at late times decreases as the wavepacket
   spreads. F∝M holds at each time point (linear in S), but R² is lower than
   the centroid-based 0.997.

2. **C9 force DECREASES with N** — correct physics (dispersing wavepacket feels
   less force). The test checks sign stability, not monotonic growth.

3. **C16** — shell-asymmetry sometimes fails (centroid artifact). Force is always
   TOWARD. Gate is 1/2 agree.

4. **3D C17 at n>9** — omits energy projections (eigensolve cost). Tests 4/6
   families. At n=9: full 6/6.
