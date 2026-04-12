# Modified Dispersion Relation from Discrete Propagator

**Date:** 2026-04-11
**Status:** anomalous scaling -- c4 coefficient present but does not scale as h^2

## Artifact chain

- [`scripts/frontier_dispersion_relation.py`](../scripts/frontier_dispersion_relation.py)

## Question

Does the path-sum propagator on a discrete lattice produce a modified
dispersion relation omega^2 = k^2 + c4 * k^4 + ... with c4 scaling as
h^2 (standard lattice correction)?  If so, what effective Planck energy
does this predict, and is it consistent with Fermi LAT bounds?

## Method

Propagate plane waves exp(i k x) through one layer of the path-sum
transfer kernel on a 3D cubic lattice.  The Fourier-space transfer
function M_hat(k_y) gives omega(k_y) via the unwrapped phase.
Fit omega(k) and omega^2(k) as polynomials in k^2 in the low-k regime
(k < 0.3 * k_max) to extract the c4 coefficient.

Tested three lattice architectures (cubic, staggered, Wilson) and two
angular kernels (cos^2, Gaussian) at four lattice spacings
h = 1.0, 0.5, 0.25, 0.125.

## Results

### c4 coefficients (omega^2 fit)

| Architecture | Kernel | h=1.0 | h=0.5 | h=0.25 | h=0.125 |
| --- | --- | ---: | ---: | ---: | ---: |
| cubic | cos2 | +1.5e-2 | -1.1e-1 | +7.3e-4 | +2.1e-3 |
| cubic | gauss | -2.8e-1 | -1.0e+0 | -2.9e-2 | -3.1e-2 |
| staggered | cos2 | -2.4e-1 | +5.9e-1 | -7.3e-4 | -1.9e-4 |
| staggered | gauss | -4.0e-1 | +4.5e+0 | +1.0e-2 | -6.4e-3 |
| wilson | cos2 | +1.5e-2 | -1.1e-1 | +7.3e-4 | +2.1e-3 |
| wilson | gauss | -2.8e-1 | -1.0e+0 | -2.9e-2 | -3.1e-2 |

### Scaling of |c4| with h

| Architecture | Kernel | alpha | A | R^2 |
| --- | --- | ---: | ---: | ---: |
| cubic | cos2 | 1.58 | 3.7e-2 | 0.40 |
| cubic | gauss | 1.47 | 5.8e-1 | 0.56 |
| staggered | cos2 | 4.05 | 8.0e-1 | 0.80 |
| staggered | gauss | 2.67 | 1.7e+0 | 0.59 |

Wilson identical to cubic (Wilson term only affects high-k doublers).

### Key findings

1. **c4 is nonzero:** The discrete propagator does produce a k^4
   correction to the dispersion relation.  This is a genuine signature
   of discreteness.

2. **Scaling is anomalous:** The c4 coefficient does NOT scale as h^2
   for cubic/Wilson lattices (alpha ~ 1.5, not 2.0).  The power-law
   model itself is a poor fit (R^2 ~ 0.4-0.6).  This means the
   correction does not behave like a standard lattice artifact.

3. **Sign of c4 is not stable:** For the cos^2 kernel, c4 flips sign
   between h values.  For the Gaussian kernel on cubic/Wilson, c4
   is consistently negative (subluminal correction).

4. **Architecture dependence is large:** The staggered lattice gives
   qualitatively different c4 (different sign, different scaling
   exponent alpha ~ 4).  Cubic and Wilson are identical.

5. **Fermi LAT consistency:** Despite the anomalous scaling, if the
   lattice spacing is Planckian, all architectures give effective
   Planck energies E_eff ~ 10^19 GeV, far above the Fermi LAT n=2
   bound of 6.3 x 10^10 GeV.

### Effective Planck energies (assuming h = l_Planck)

| Architecture/Kernel | E_Planck_eff (GeV) | Fermi LAT status |
| --- | ---: | --- |
| cubic/cos2 | 6.3e+19 | consistent |
| cubic/gauss | 1.6e+19 | consistent |
| staggered/gauss | 9.4e+18 | consistent |

### Predicted photon speed deviation at 10 GeV

All combinations give |v - 1| ~ 10^{-37} to 10^{-38}, many orders of
magnitude below any foreseeable measurement capability.

## Bounded claims

1. The path-sum propagator on a discrete lattice produces a nonzero k^4
   correction to the dispersion relation.

2. The correction does NOT scale as h^2 (standard lattice artifact).
   The scaling exponent is anomalous (alpha ~ 1.5 for cubic, ~2.7-4
   for staggered).  This means the correction has a different
   character from textbook lattice discretization.

3. The c4 coefficient depends on both the angular kernel and the
   lattice architecture.  Cubic and Wilson give identical results;
   staggered differs qualitatively.

4. If the lattice spacing is Planckian, the predicted photon speed
   deviation is far below current experimental sensitivity
   (|v-1| ~ 10^{-37} at 10 GeV).

5. The model is NOT falsified by Fermi LAT data, but the prediction
   is also not testable with current or near-future instruments.

## What this does NOT establish

- That the anomalous scaling is physically meaningful (it could be an
  artifact of the 1D Fourier-space projection used here)
- That c4 converges to a definite value in the continuum limit
  (the sign-flipping for cos^2 kernel suggests it may not)
- A clean, architecture-independent prediction for Lorentz violation

## Status

The k^4 correction exists but its scaling is anomalous and
architecture-dependent.  This is an honest negative result for the
hypothesis that the model makes a clean Lorentz-violation prediction.
The effective Planck energy is consistent with all bounds, but the
prediction is many orders of magnitude below experimental reach.
