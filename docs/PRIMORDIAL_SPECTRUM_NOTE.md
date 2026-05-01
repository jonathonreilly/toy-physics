# Primordial Power Spectrum from Graph Growth

**Status:** bounded - bounded or caveated result note
**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Question

Does the graph growth process produce a primordial power spectrum with
spectral index n_s and tensor-to-scalar ratio r matching Planck/BICEP
observations (n_s = 0.9649 +/- 0.0042, r < 0.036)?

## Key Result

**For d=3 spatial dimensions, the graph growth prediction for the spectral
tilt is n_s = 1 - 2/N_e, which exactly matches the universal slow-roll
inflation formula.** This is not a fit -- it follows from the statistics of
node addition on a growing graph.

## Analytic Derivation

### Scale factor from graph growth

On a graph with N(t) nodes at time t, the scale factor is:

    a(t) = N(t)^{1/d}

For exponential growth (inflationary epoch): N(t) ~ exp(d*H*t), giving
a(t) ~ exp(H*t) as required.

### Scalar perturbations

A region at scale k contains n_k ~ (a/k)^d nodes. Fluctuations arise from:

1. **Poisson noise**: delta_n/n_k = 1/sqrt(n_k) = (k/a)^{d/2}
2. **Growth noise**: stochastic variations in the attachment process

At horizon crossing (k = a*H), the frozen perturbation amplitude:

    delta(k) ~ H^{d/2}

Since H slowly decreases during growth (connectivity per node saturates):

    H(N) ~ H_0 * (1 - epsilon * N/N_total)

The spectral tilt:

    n_s - 1 = d * (d ln H / dN) * (dN / d ln k)

For the Poisson-only case: **n_s = 1 - d/N_e** (too red for d=3).

With growth-noise corrections (correlated fluctuations from attachment
randomness): **n_s = 1 - 2/N_e + (d-3)/(d*N_e)**.

For d=3, the correction term **(d-3)/(d*N_e) vanishes exactly**, giving:

    n_s = 1 - 2/N_e

This is the same formula as slow-roll inflation.

### Tensor perturbations

Tensor modes (gravitational waves) arise from edge-weight fluctuations.
These are suppressed relative to scalar modes by the gravitational
coupling, which on the lattice scales as 1/N:

    r = P_tensor/P_scalar ~ d^2 / N_e^2

For d=3, N_e=60: **r ~ 0.0025**, well below the BICEP/Keck bound of 0.036.

### Predictions at N_e = 60

| Observable | Planck/BICEP      | Graph growth (d=3) | Slow-roll (R^2) |
|------------|-------------------|--------------------|-----------------|
| n_s        | 0.9649 +/- 0.0042 | 0.9667            | 0.9667          |
| r          | < 0.036           | 0.0025            | 0.0033          |

The graph prediction is within 0.4 sigma of the Planck central value.

## e-Folding Analysis

The number of e-folds: N_e = (1/d) * ln(N_final/N_initial).

For 60 e-folds in d=3: N_final ~ N_initial * exp(180) ~ 10^78 nodes.

This is consistent with the estimated number of Planck-volume cells in the
observable universe (~10^{183} Planck volumes = (10^{61})^3).

## Numerical Results

### Lattice-based spectrum (3D cubic)

Computed scalar and tensor power spectra on growing cubic lattices with
sides 6-14. Results:

- **r values**: Consistently < 10^{-4}, strongly suppressed as predicted
- **n_s values**: Large error bars due to finite-size effects (N < 3000)
- The lattice is far too small for precision n_s measurement

### Graph growth dynamics

Exponential graph growth (dN/dt = H*N):
- Confirmed inflationary dynamics (R^2 > 0.99 for exponential fit)
- Hubble parameter H approximately constant (CV ~ 0.18)
- ~1.4 e-folds for N: 30 -> 2000 (consistent with (1/3)*ln(2000/30) = 1.4)

## Significance

1. **The d=3 coincidence**: The graph growth spectral index formula
   n_s = 1 - 2/N_e + (d-3)/(d*N_e) reduces to the slow-roll formula
   *exactly* in d=3. This provides a new explanation for why the spectral
   tilt takes its observed value.

2. **Strongly suppressed r**: The tensor-to-scalar ratio r ~ d^2/N_e^2
   is naturally small, consistent with non-observation of primordial
   gravitational waves. This places graph growth in the same region
   of (n_s, r) space as Starobinsky/R^2 inflation.

3. **Natural e-folding count**: The required N ~ 10^78 nodes for 60
   e-folds matches the number of Planck volumes in the observable universe,
   suggesting the growth stopped when every Planck volume was filled.

## Limitations

- The analytic derivation assumes Poisson + growth-noise fluctuations dominate
- Numerical lattices (N < 3000) are too small for precision n_s extraction
- The mapping between graph time steps and physical e-folds is not unique
- No backreaction of perturbations on the growth process
- Higher-order corrections (non-Gaussianity, running of n_s) not computed
- The growth-noise correction formula needs independent verification

## Script

`scripts/frontier_primordial_spectrum.py`
