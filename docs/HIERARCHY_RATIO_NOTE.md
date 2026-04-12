# Hierarchy Ratio: Gravity/EM Coupling Constraints

**Status:** Bounded negative (honest null result with structural insight)
**Script:** `scripts/frontier_hierarchy_ratio.py`
**Surface:** 16^3 cubic lattice, k=4.0, Dirichlet BC

## Question

In nature, gravity is weaker than electromagnetism by a factor of ~10^36 (comparing G*m_p^2 to e^2 in natural units). Does the path-sum framework constrain or predict this ratio?

## Method

Four tests on a 3D lattice:
1. Sweep gravitational coupling G through self-consistent Poisson iteration
2. Sweep EM coupling q through ray-deflection Coulomb measurement
3. Compute the ratio of natural scales
4. Run both sectors simultaneously across a grid of (G, q) values

## Results

### Gravity sector
- Self-consistent iteration converges for G in [0.01, 20] on a 16^3 lattice
- Field profile: phi ~ 1/r^{0.83} (finite-size suppression from beta=1)
- Stability boundary: G_max ~ 20 (lattice units)
- G enters the field equation (nabla^2 f = -G*rho), dimensionally [length^2]

### EM sector
- Ray deflection follows power law with slope -1.1 (finite-size effect on 1/r^2)
- Deflection is exactly linear in q: slope and R^2 are identical for all q
- No upper stability limit for q in the ray-sum approach (EM is a phase, not a self-consistent loop)
- q is dimensionless (gauge coupling in the action S += q*V)

### Combined system
- Mixed residual R_GE = 0 to machine precision (< 10^{-14}) for all 20 tested (G,q) pairs
- Gravity convergence is completely independent of q
- No preferred ratio G/q^2: all tested ratios from 0.004 to 1000 work equally well

### The ratio
- G_nat/q_nat^2 ~ 0.008 (lattice units), but this is not meaningful because the two couplings have different dimensions and independent constraints
- The physical hierarchy G*m^2/e^2 ~ 10^{-36} requires knowing the proton mass m_p, which the framework does not predict

## Key Finding

**The framework does not constrain the gravity/EM hierarchy.** The two sectors are strictly independent:
- Gravity enters through the scalar field f in S = L(1-f), self-consistently sourced by Poisson
- EM enters through the phase q*V in the action, with no back-reaction loop
- The mixed residual R_GE = 0 exactly (linearity of action accumulation)
- G convergence does not depend on q, and vice versa

The apparent hierarchy is dimensional: G has units [length^2] while q is dimensionless. The physical ratio G*m^2/q^2 depends on the mass m of the particles being compared, which means the hierarchy problem is really a mass-spectrum problem (why m_proton << m_Planck), not a coupling-ratio problem.

## What the framework does constrain

1. **Poisson uniqueness:** Self-consistency selects the graph Laplacian as the unique field equation (established in `frontier_self_consistent_field_equation.py`)
2. **Sector independence:** Gravity and EM do not interfere (R_GE = 0 exactly)
3. **Stability bound:** G has a lattice-dependent upper bound for convergence
4. **EM linearity:** The Coulomb sector is exactly linear in the coupling q

## Honest assessment

This is a null result for the hierarchy problem. The framework correctly reproduces both gravitational and electromagnetic behavior, but treats their couplings as independent free parameters. Solving the hierarchy would require a mechanism that relates the mass spectrum to the lattice structure -- something not present in the current formulation.
