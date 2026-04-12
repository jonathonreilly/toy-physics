# Spectral Radius vs Dimension -- Propagator Normalization Check

**Script:** `scripts/frontier_spectral_radius_dimension.py`
**PStack:** `frontier-spectral-radius-dimension`

## Question

Does the path-sum propagator's single-layer transfer matrix have bounded spectral radius (rho <= 1) at d=3 but unbounded (rho > 1) at d > 3? If so, the propagator is non-normalizable above d=3, giving a hard dimension selection.

## Method

For d = 1 through 5, build the transfer matrix M that maps transverse amplitudes from one x-slice to the next. M_{ji} = exp(ikS) * w(theta) * h^{d-1} / L^p, where L is the hop length, S = L(1-f) the action, and w(theta) the angular kernel (cos^2, Gaussian, or flat).

Nine experiments:
1. Spectral radius vs d at fixed h=1 for multiple (k, f)
2. Spectral radius vs attenuation power p
3. Spectral radius vs lattice spacing h (continuum limit)
4. Kernel comparison (cos^2, Gaussian, flat)
5. Normalized transfer matrix (M / M_forward)
6. Row-sum (Gershgorin bound) scaling with d
7. Nearest-neighbor (NN) transfer matrix vs all-to-all
8. NN spectral radius vs lattice size (thermodynamic limit)
9. Critical attenuation p_c for NN matrix

## Key Results

**Raw transfer matrix (h=1, all-to-all):** rho > 1 for all d >= 2. Row-sum bound grows monotonically: 1.0, 2.0, 5.2, 12.9, 21.8 for d = 1..5. No sharp cutoff at d=3.

**Nearest-neighbor transfer matrix:** rho_nn converges with lattice size but remains > 1 for d >= 2. The NN row bound scales as 3^{d-1} (coordination number): 1.7, 3.2, 6.4, 13.9 for d = 2..5.

**Continuum limit (h -> 0):** The row sum scales as h^{d-1-p}. For p=1, row_sum ~ h^{d-2}. At d=2, rho stays O(1) as h -> 0 (marginal). At d >= 3, rho -> 0 as h -> 0 (bounded in the continuum limit). This is graded, not a sharp cutoff.

**Kernel dependence:** cos^2 gives the tightest rho; flat kernel gives the largest. All kernels show the same monotonic growth with d.

## Verdict

The original hypothesis -- rho(M) <= 1 iff d <= 3 -- is **not confirmed**.

The spectral radius provides graded suppression (higher d requires stronger phase cancellation), but no sharp d <= 3 boundary. At fixed lattice spacing h=1, rho > 1 for all d >= 2. In the continuum limit, h^{d-2} scaling makes all d >= 3 formally bounded, which is the opposite of the prediction.

Dimension selection in this model must arise from a different mechanism, such as self-consistency of the gravitational field, Born rule constraints, or Poisson equation structure -- as explored in `frontier_dimension_selection.py`.

## Bounded Claims

- The transfer matrix spectral radius grows monotonically with d for all tested kernels and parameters
- NN spectral radius converges to a finite (> 1) limit in the thermodynamic limit for d >= 2
- The continuum-limit scaling h^{d-2} does not produce a sharp d <= 3 cutoff
- These results are for lattice propagators with 1/L^p attenuation and angular kernels; different propagator definitions could change the picture
