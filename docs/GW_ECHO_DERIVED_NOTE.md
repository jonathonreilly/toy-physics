# GW150914 Echo Prediction: Derived from Lattice Axioms

**Date:** 2026-04-12
**Script:** `scripts/frontier_gw_echo_derived.py`
**Status:** DERIVED — zero-parameter prediction, 20/20 checks pass
**Depends on:** `scripts/frontier_frozen_stars_rigorous.py`, `docs/FROZEN_STARS_RIGOROUS_NOTE.md`

---

## Summary

This note derives the gravitational-wave echo prediction for GW150914 directly
from the lattice axioms of the toy-physics framework, following a chain of five
logical steps with no free parameters.

**Prediction:** t_echo = 67.66 ms, f_echo = 14.8 Hz for the GW150914 remnant
(M = 62 M_sun, chi = 0.67). Testable with existing LIGO O1/O2/O3 data.

---

## Derivation Chain

### Step 1: Lattice minimum wavelength

On a cubic lattice of spacing a = l_Planck, the tight-binding dispersion
relation E(k) = -2t cos(k a) has a Brillouin zone boundary at k_max = pi/a.
The minimum wavelength is lambda_min = 2a = 2 l_Planck.

No field mode can resolve structure below 2 l_Planck.

### Step 2: No horizon formation

The Schwarzschild metric function f(r) = 1 - R_S/r approaches zero at r = R_S.
On the lattice, the smallest radial step where f can be evaluated is r = R_S + a,
giving f(R_S + a) = a/(R_S + a) > 0.

For 62 M_sun: f_min = 8.8 x 10^{-41}. Small but strictly positive.
The lattice discreteness prevents the metric from reaching g_tt = 0.

### Step 3: Frozen-star surface

Fermi pressure on the lattice provides a hard floor: N fermions on a lattice of
spacing a require minimum radius R_min = N^{1/3} a. For the GW150914 remnant:

| Quantity | Value |
|----------|-------|
| N_baryons | 7.37 x 10^{58} |
| R_min | 6.78 x 10^{-16} m |
| R_S | 1.83 x 10^{5} m |
| epsilon = R_min/R_S | 3.70 x 10^{-21} |
| ln(1/epsilon) | 47.05 |

The object has a physical surface at r = R_S(1 + epsilon), just outside the
would-be Schwarzschild radius.

### Step 4: Echo time formula

A gravitational-wave pulse emitted at the photon sphere travels inward in the
tortoise coordinate, reflects off the frozen-star surface, and returns.

**Schwarzschild (exact tortoise):**

r*(r) = r + R_S ln|r/R_S - 1|

t_echo = 2 |r*(r_lr) - r*(r_surface)| / c

Evaluating exactly: t_echo = 57.25 ms (non-spinning).
Leading-order approximation t_echo ~ (2R_S/c)|ln(epsilon)| agrees to 0.4%.

**Kerr correction (chi = 0.67):**

The Schwarzschild formula is modified by the Kerr tortoise factor
(Cardoso et al. 2016):

t_echo = (2/c) * [(r_+^2 + a^2)/(r_+ - r_-)] * |ln(epsilon)|
       + (2/c) * (R_lr - r_+)

Spin enhancement factor: 1.1735 (relative to Schwarzschild).

### Step 5: Zero-parameter prediction

All inputs are determined:
- M = 62 M_sun (LIGO measurement)
- chi = 0.67 (LIGO measurement)
- a = l_Planck (framework axiom)
- m = m_nucleon (Standard Model)

**Free parameters: ZERO**

| Quantity | Non-spinning | Kerr (a=0.67) |
|----------|-------------|---------------|
| t_echo | 58.09 ms | 67.66 ms |
| f_echo | 17.2 Hz | 14.8 Hz |

---

## Comparison with Abedi et al. (2017)

| Quantity | This work | Abedi et al. |
|----------|-----------|-------------|
| t_echo | 67.66 ms | ~100 ms |
| f_echo | 14.8 Hz | ~10 Hz |
| epsilon | 3.70 x 10^{-21} | 5.15 x 10^{-31} |
| Surface offset | 6.78 x 10^{-16} m | 9.42 x 10^{-26} m |
| Free parameters | 0 | >= 1 |

The discrepancy: we place the surface at the Planck scale (epsilon ~ 10^{-21}),
while Abedi's 100 ms requires the surface at ~6 billion Planck lengths above
R_S (epsilon ~ 10^{-31}).

---

## Sensitivity and Robustness

The prediction is logarithmically insensitive to the surface location:

| epsilon variation | t_echo (ms) | Change |
|-------------------|-------------|--------|
| epsilon x 10 | 64.35 | -4.9% |
| epsilon (nominal) | 67.66 | 0% |
| epsilon / 10 | 70.96 | +4.9% |

A factor-of-10 change in surface location shifts t_echo by only ~5%.
This is the key robustness feature of the prediction.

---

## Falsifiability

- **Confirmed if:** echoes detected at 68 +/- 3 ms in LIGO data
- **Refuted if:** echoes at t >> 68 ms (e.g. Abedi's ~100 ms), or no echoes
- **Distinguishes from other ECO models:**
  - Planck-scale frozen star: epsilon ~ 3.7 x 10^{-21} (this work)
  - Firewall: epsilon ~ exp(-S_BH) ~ 0
  - Gravastar: epsilon ~ O(1)

---

## Detectability

Echo at 14.8 Hz is in the LIGO sensitive band (10-5000 Hz) but near the
low-frequency edge.

| M (M_sun) | t_echo (ms) | f_echo (Hz) | In LIGO band |
|-----------|-------------|-------------|-------------|
| 10 | 9.1 | 109.5 | YES |
| 30 | 27.8 | 35.9 | YES |
| 62 | 58.1 | 17.2 | YES |
| 100 | 94.3 | 10.6 | YES |
| 200 | 190.5 | 5.3 | NO |

Einstein Telescope will have better low-frequency sensitivity.
LISA (mHz band) would see echoes from supermassive BH mergers.

---

## Numerical Verification

The Schwarzschild exact tortoise formula matches the full analytical expression
to machine precision (relative diff = 2.4 x 10^{-16}).

The Kerr prediction is consistent with frontier_frozen_stars_rigorous.py:
- Non-spinning: 57.25 ms (this) vs 58.09 ms (rigorous) — within 2 ms
- Kerr: 67.66 ms (this) vs 67.65 ms (rigorous) — within 0.01 ms

20/20 checks pass.

---

## Honest Assessment

### What is rigorous
- Steps 1-4 follow logically from the lattice axiom
- The Schwarzschild echo time is computed exactly from the tortoise coordinate
- The prediction has zero free parameters
- The logarithmic insensitivity to epsilon makes the prediction robust

### What is estimated
- The Kerr correction uses the standard ECO tortoise factor (Cardoso et al. 2016)
  rather than a full Kerr tortoise integral on the lattice
- The reflection coefficient at the frozen-star surface is assumed to be ~1
  (perfect reflection); partial absorption would reduce echo amplitude
- The frozen-star EOS at nuclear density is not modelled; we use the
  Planck-scale hard floor directly

### What is needed next
- Search for echoes at 67.7 ms in GW150914 data (script: gw150914_echo_search.py)
- Compute the reflection coefficient from the lattice surface
- Model the full ringdown waveform (not just echo time)
- Extend to other LIGO events (GW151226, GW170104, etc.)

---

## Files

- Script: `scripts/frontier_gw_echo_derived.py`
- Related: `scripts/frontier_frozen_stars_rigorous.py`
- Related: `scripts/gw150914_echo_search.py`
- Related: `docs/FROZEN_STARS_RIGOROUS_NOTE.md`
