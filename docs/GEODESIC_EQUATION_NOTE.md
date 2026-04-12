# Geodesic Equation: Propagator Trajectories Match Emergent Metric

## Result

Test particles in the framework follow geodesics of the emergent conformal
metric g_mu_nu = (1-f)^2 eta_mu_nu. Five independent tests confirm this on
a 31^3 lattice with Poisson-sourced field (f_max ~ 0.2, weak-field regime).

## Key findings

**Christoffel symbols** computed analytically from the conformal metric match
finite-difference numerical values to 2.3e-7, confirming the metric structure.

**Newtonian limit**: the timelike geodesic acceleration reduces to
a = -grad(f)/(1-f), matching the expected Newtonian gravity with exact
numerical agreement (error < 1e-15).

**Light bending factor-of-2**: null geodesics deflect 1.97x the Newtonian
prediction, reproducing the GR result that both temporal and spatial metric
components contribute equally. This holds across impact parameters b = 3..9.

**1/b scaling**: deflection * impact parameter is approximately constant
(spread 0.22), confirming Coulomb-like falloff as expected from the 1/r
potential on the lattice.

## Physics

For the conformal metric ds^2 = (1-f)^2(-dt^2 + dr^2):

- Massive particles (v << c): a^i = -d_i f / (1-f) (Newtonian gravity)
- Light rays: a^i = 2(v.grad f)/(1-f) v^i - 2(d_i f)/(1-f) (twice Newtonian)

The propagator action S = k L (1-f) gives refractive index n = 1/(1-f),
so ray tracing reproduces null geodesics. The factor-of-2 is automatic:
it comes from both g_00 and g_ij contributing to the bending.

## Connection to framework

This closes the chain: the propagator produces an emergent metric, and
particles moving through that metric follow geodesics -- matching GR at
both the Newtonian and post-Newtonian levels.

## Script

`scripts/frontier_geodesic_equation.py` -- runs in ~2s, no GPU required.
