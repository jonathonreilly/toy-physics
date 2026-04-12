# Independent Spatial Metric Derivation

**Status:** review hold -- improved consistency derivation, gate not yet closed  
**Script:** `scripts/frontier_independent_spatial_metric.py`

## The Circularity Problem

The previous derivation of the spatial metric factor was circular:

1. Define the action: `S = L(1-f)`
2. Infer the line element: `ds = (1-f)dx`
3. Read off the metric: `g_xx = (1-f)^2`

Step 3 restates Step 1 -- it is a consistency argument, not a derivation.

## Independent Derivation via Laplacian Spectral Geometry

We derive `g_{xx} = (1-f)^{-2}` from three principles that do not
explicitly reuse the action `S = L(1-f)` as the metric ansatz.

### Step 1: Minimal coupling modifies the hopping amplitude

The propagator's step amplitude from site i to site j in a background
scalar field f is:

    A_{ij} = (1 - f_mid) * exp(i k L_{ij}) / L_{ij}^p * w(theta)

The factor `(1-f)` multiplying the amplitude is framed here as a
**geodesic deviation / volume element correction**: in a gravitational
potential, the density of paths between neighboring sites decreases by
a factor `(1-f)`, reducing the tunneling amplitude. This is a minimal
coupling prescription (analogous to Peierls substitution in EM), not a
metric readout.

### Step 2: The Laplacian weight is |amplitude|^2

The Hamiltonian is `H_{ij} = -A_{ij}`. The graph Laplacian relevant for
diffusion and metric extraction is the Hermitian operator:

    L = H^dagger H

whose off-diagonal entries are `|A_{ij}|^2 = (1-f)^2`.

This squaring is the **Born rule** -- the transition probability (which
determines the effective geometry for diffusion) is the square of the
amplitude. This is a general quantum mechanical principle, independent
of any particular action.

### Step 3: Spectral identification gives the metric

The eigenvalues of the modified Laplacian with `(1-f)^2` hopping scale as:

    lambda_n(f) = (1-f)^2 * lambda_n(0)

This is verified numerically (see `scripts/frontier_independent_spatial_metric.py`,
Approach 3b) to machine precision for all tested f values.

On a Riemannian manifold with conformal metric `g_{ij} = Omega^2 delta_{ij}`,
the Laplace-Beltrami operator in 1D is:

    Delta_g = Omega^{-2} * Delta_flat

Comparing with the lattice result `Delta_field = (1-f)^2 * Delta_flat`,
we identify:

    Omega^{-2} = (1-f)^2  =>  Omega = 1/(1-f)  =>  g_{xx} = 1/(1-f)^2

### Step 4: Weak-field limit matches Schwarzschild

    g_{xx} = 1/(1-f)^2 ~ 1 + 2f + 3f^2 + ...

With f = Phi (Newtonian potential), to first order:

    g_{xx} ~ 1 + 2 Phi

This is the Schwarzschild metric in isotropic coordinates.

## Supporting Numerical Evidence

### Approach 1: Green's function decay

The resolvent `G(x,y;E) = <x|(H-E)^{-1}|y>` decays exponentially
with effective distance. At the natural probe energy `E = -3.0` (center
of the band gap), the ratio `-log|G(f)|/-log|G(0)|` scales as
`(1-f)^{-1}` with R^2 = 0.996, confirming the effective distance
increases as `1/(1-f)`.

### Approach 2: Heat kernel diffusion

The heat kernel `K(x,y;t) = exp(-tL)` encodes geometry through
the diffusion width. With `(1-f)` hopping, `sigma ~ sqrt(1-f)`,
consistent with diffusion constant `D ~ (1-f)`. This independently
confirms the Laplacian weight scaling.

### Approach 3: Spectral eigenvalues

- With hopping `w = (1-f)`: eigenvalues scale as `(1-f)` (exact)
- With hopping `w = (1-f)^2`: eigenvalues scale as `(1-f)^2` (exact)

Both confirmed to machine precision on a periodic ring of 64 sites.

## Why This Is Stronger Than The Old Argument

| Step | Ingredient | Source |
|------|-----------|--------|
| 1 | Amplitude factor (1-f) | Geodesic deviation / volume element |
| 2 | Squaring: \|A\|^2 = (1-f)^2 | Born rule (quantum mechanics) |
| 3 | Lambda_n scaling | Direct numerical measurement |
| 4 | Delta_g = g^{xx} Delta_flat | Riemannian geometry |

The chain is:

    geodesic deviation -> Born rule -> spectral geometry -> metric

The `(1-f)^2` in the metric is not obtained by directly squaring the
action. It comes from **squaring the amplitude** after introducing the
field-dependent hopping.

## Why This Gate Is Still Not Closed

This note improves the old circularity problem, but it does **not** yet
justify unconditional promotion.

- the spectral and Born-rule steps are independent once the amplitude
  prefactor `(1-f)` is granted
- the unresolved step is the prefactor itself: it is still introduced as a
  minimal-coupling / geodesic-deviation prescription rather than derived
  directly from the axioms
- that means this is presently a stronger weak-field consistency derivation,
  not a fully independent closure of the spatial-metric gate

## Claim boundary

- stronger than the old action-restatement argument
- supports review-level consistency with the weak-field Schwarzschild spatial
  factor
- does not yet support an unconditional "derived from the axioms alone" claim
- do not promote to `main` until the `(1-f)` amplitude prefactor is itself
  independently forced rather than prescribed

## Script

Full numerical verification: `scripts/frontier_independent_spatial_metric.py`
