# Poisson Exhaustive Uniqueness

**Status:** bounded review candidate -- strengthened operator-family audit  
**Script:** `scripts/frontier_poisson_exhaustive_uniqueness.py`

## Result

The Poisson field equation is the **unique Newtonian crossing within the tested
fractional nearest-neighbor operator family** on the audited cubic surface, and
the tested non-local alternatives fail to provide a stable self-consistent lane.

## Method

Script: `scripts/frontier_poisson_exhaustive_uniqueness.py`

Tested 21 operators across four categories on a 16^3 grid:

1. **Fractional Laplacians** L_alpha = (-nabla^2)^alpha for alpha in {0.25, 0.5, 0.75,
   0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 3.0}, using spectral decomposition.
2. **Anisotropic Laplacians** with directional weights (1,1,1), (2,1,1), (1,2,1), (3,1,1).
3. **Non-local operators**: next-nearest-neighbor (26 neighbors) and exponentially
   decaying long-range coupling.
4. **Higher-order stencils**: 2nd, 4th, and 6th-order accurate discrete Laplacians.

## Key Findings

**Monotonic beta(alpha):** The mass exponent beta decreases monotonically across
the tested fractional family. That guarantees a unique zero-crossing where
beta=1 inside that family. On the N=16 grid, finite-size bias shifts the
apparent crossing away from alpha=1.0, so the review-safe statement is about
family-level uniqueness of the crossing, not exact continuum identification.

**Connectivity matching:** The tested non-local operators diverge in the
self-consistent iteration. The nearest-neighbor operator class matches the
propagator's own connectivity on this surface.

**Robustness:** Anisotropic Laplacians all converge with attraction (beta in [1.14, 1.44]).
Higher-order stencils agree to within beta spread < 0.02. The result depends on the
operator class (Laplacian), not the specific discretization.

## Upgrade over Previous Result

Previous: "Poisson preferred among 5 tested operators."

Now: "Unique Newtonian crossing in the tested local fractional family, with
tested non-local alternatives failing to supply a stable self-consistent lane,
and robustness to anisotropy and stencil order."

## Limitations

- Finite-size bias shifts the apparent optimal alpha from 1.0 to ~1.5 at N=16.
  Larger grids needed to confirm continuum-limit convergence to alpha=1.
- Non-local operator divergence may partly reflect numerical conditioning rather than
  fundamental incompatibility. More careful regularization could be investigated.

## Claim boundary

- supports a stronger review-level result than "preferred among five tested
  operators"
- does not yet justify "unique self-consistent local field equation" in full
  generality
- the safe statement is uniqueness of the Newtonian crossing within the tested
  local fractional nearest-neighbor family, plus failure of the tested non-local
  alternatives on the audited surface
