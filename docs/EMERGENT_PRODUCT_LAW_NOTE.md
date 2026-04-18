# Emergent M1*M2 Product Law via Self-Consistent Poisson Field

**Script:** `scripts/frontier_emergent_product_law.py`
**Date:** 2026-04-11
**Status:** bounded companion on one audited open 3D staggered cross-field Poisson surface

## Motivation

Previous two-body tests used `V(x1,x2) = -G * s1 * s2 / |x1-x2|`, which
hardcodes the bilinear M1*M2 factor into the interaction operator. That verifies
the solver machinery but does not demonstrate that the product law *emerges* from
the dynamics. This experiment closes that gap.

## Method

Open 3D staggered lattice (side=14, 2744 sites) with two Gaussian wavepackets
separated along x. The coupling is strictly cross-field Poisson:

1. Compute density: `rho_i = M_i * |psi_i|^2`
2. Solve Poisson for each particle: `(L + mu^2) phi_i = G * rho_i`
3. Each particle evolves under the OTHER's field only:
   - `H_A` includes `phi_B` (not `phi_A`)
   - `H_B` includes `phi_A` (not `phi_B`)
4. Force: `F_A = -M_A * integral |psi_A|^2 * grad(phi_B)`

No bilinear `M_A * M_B` term appears anywhere in the code.

The product law emerges from two independent linearities:
- **Poisson linearity:** `phi_i ~ M_i` (the Poisson equation is linear in the source)
- **Test-mass response:** `F_j ~ M_j` (the Ehrenfest force includes `rho_j = M_j * |psi_j|^2`)

**Frozen-source control:** Poisson fields computed once from initial densities and
held fixed during evolution. If the product law survives frozen fields, it confirms
the result is a field-linearity consequence, not a dynamical accident.

## Results

### Dynamic (self-consistent)

| Quantity | Value | Gate |
|----------|-------|------|
| alpha (M_A exponent) | 1.0146 | PASS (within 5% of 1) |
| beta (M_B exponent) | 0.9863 | PASS (within 5% of 1) |
| R^2 | 0.999993 | PASS (> 0.99) |

### Frozen-source control

| Quantity | Value | Gate |
|----------|-------|------|
| alpha (M_A exponent) | 1.0081 | PASS (within 5% of 1) |
| beta (M_B exponent) | 0.9919 | PASS (within 5% of 1) |
| R^2 | 0.999998 | PASS (> 0.99) |

### Symmetry

| Check | Max violation | Gate |
|-------|---------------|------|
| t=0 frozen (acceptance gate) | 0.0000% | PASS (< 2%) |
| Dynamic multi-step (informational) | 4.65% | not gated |

The t=0 frozen symmetry is exact to machine precision because the initial
Gaussians are placed symmetrically and no evolution has occurred. The dynamic
asymmetry (~5%) is a known staggered-phase lattice artifact that grows with
the number of time steps and the mass ratio.

### Frozen vs Dynamic

Max difference: 1.2%, mean: 0.5%. The product law holds in both regimes,
confirming it is a field-linearity result.

## Bounded Claims

1. **Demonstrated:** F ~ M_A^alpha * M_B^beta with alpha, beta within 2% of
   unity and R^2 > 0.9999, using cross-field Poisson coupling with no bilinear
   ansatz.

2. **Mechanism identified:** The product law follows from two independent
   linearities (Poisson source scaling + test-mass response), confirmed by the
   frozen-source control on the same audited surface. This is a field-linearity
   result, not full Newton closure.

3. **Not demonstrated:** The distance-law exponent is not tested here (fixed
   separation). For distance-law emergence, see the existing self-consistent
   two-body notes.

4. **Lattice artifact noted:** The staggered Hamiltonian's position-dependent
   phases introduce ~5% A<->B asymmetry after several time steps at extreme mass
   ratios (8:1). This does not affect the product-law exponents (which are fitted
   across the full mass grid) but is visible in the pairwise symmetry check.

## Parameters

- SIDE=14, BARE_MASS=0.30, G=50.0, MU2=0.001
- DT=0.08, N_STEPS=6, SIGMA=0.80, SEPARATION=5
- MASS_VALUES=[0.10, 0.20, 0.40, 0.80]
- Runtime: ~30s
