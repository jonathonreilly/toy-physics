# Dispersion Running-Exponent Fingerprint

**Date:** 2026-04-12
**Status:** bounded review candidate -- running-exponent fingerprint on cubic/Wilson, non-standard on staggered

## Artifact chain

- [`scripts/frontier_dispersion_running_exponent.py`](../scripts/frontier_dispersion_running_exponent.py)

## Question

What particle type does the path-sum propagator describe at different
momentum scales?  Specifically, does the dispersion relation look
Schrodinger (quadratic), relativistic (linear), or Klein-Gordon
(quadratic-to-linear crossover)?

## Why this replaces the earlier global-R^2 fit

The previous dispersion study (`frontier_dispersion_relation.py`) fitted
a global polynomial omega^2 = k^2 + c4*k^4 and found anomalous scaling
of c4 with lattice spacing.  A single R^2 number cannot distinguish
between a uniformly quadratic dispersion and one that transitions from
quadratic to linear at a crossover scale.  The running exponent
alpha_eff(k) = d log|Omega - Omega(0)| / d log k resolves this.

## Method

For each architecture (cubic, staggered, Wilson) at h = 0.5:

1. Build the Fourier-space transfer function M_hat(k_y) for transverse
   wavenumber k_y (same kernel as the original dispersion script).
2. Extract Omega(k) = -Im[log(M_hat(k))] / h (unwrapped phase).
3. Compute the running exponent alpha_eff(k) via log-log finite
   differences of |Omega(k) - Omega(0)|.
4. Fit alpha in two windows:
   - alpha_lo: k < pi/4 (low-k)
   - alpha_hi: pi/4 < k < pi/2 (high-k, pre-aliasing)
5. Search for a crossover wavenumber k_* between the two regimes.

Classification targets:
- Schrodinger: alpha_lo ~ 2, alpha_hi ~ 2
- Linear (relativistic): alpha_lo ~ 1, alpha_hi ~ 1
- Klein-Gordon: alpha_lo ~ 2, alpha_hi ~ 1, finite k_*

## Results

| Architecture | alpha_lo | alpha_hi | k_*  | Classification |
|--------------|----------|----------|------|----------------|
| cubic        | 2.09     | 2.19     | none | Schrodinger    |
| staggered    | 2.39     | 2.54     | none | non-standard   |
| Wilson       | 2.09     | 2.19     | none | Schrodinger    |

- Cubic and Wilson: alpha ~ 2 in both windows (within tolerance 0.4).
  Classified as Schrodinger-type quadratic dispersion.
- Staggered: alpha elevated above 2.0 in both windows (2.39/2.54),
  falling outside the Schrodinger classification tolerance.
- No Klein-Gordon crossover detected in any architecture.
- Wilson develops a phase discontinuity near k_y ~ pi (Brillouin zone
  edge) due to the doubler-removal term, but the low-k and mid-k
  windows are unaffected.

## What is supported

- At h = 0.5 with cos^2 kernel, k_phase = 5, p = 1, the cubic and
  Wilson architectures produce a Schrodinger-type (alpha ~ 2) dispersion
  across both momentum windows.
- The running-exponent diagnostic cleanly distinguishes architectures
  that the earlier global R^2 fit could not separate.

## What is not supported

- No architecture shows a Klein-Gordon (quadratic-to-linear) crossover.
- The staggered lattice does not fit any clean particle-type category.
- This study is at a single lattice spacing (h = 0.5) and does not
  establish continuum-limit behavior.
- The Schrodinger classification does not by itself imply a
  non-relativistic particle -- it may reflect the specific choice of
  kernel and parameters.

## Missing closure

- Continuum limit: repeat at multiple h values to check whether
  alpha_lo and alpha_hi are stable or h-dependent.
- Parameter sensitivity: vary k_phase and p to determine whether the
  Schrodinger classification is robust.
- The staggered architecture's non-standard exponent needs separate
  investigation (likely related to the alternating-sign hop structure).
