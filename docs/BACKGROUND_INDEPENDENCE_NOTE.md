# Background Independence: Effective Geometry Differs from Input Graph

## Result

On a fixed cubic lattice (N=20, uniform 6-neighbor connectivity), the
effective geometry seen by the propagator changes in response to a
gravitational source. Four independent measurements confirm this.

## Setup

- 3D cubic lattice, Poisson-sourced gravitational field f
- Propagator edge weight: w = exp(-k(1-f)), where f > 0 near mass
- Green's function G from the weighted Laplacian (eps*I - L_eff)^{-1}

## Test 1: Non-uniform edge weights

Flat lattice has uniform w = exp(-k). With gravity, edges near mass are
18.8% stronger than far from mass (w/w_flat = 1.21 at r=1 vs 1.02 at r=8).
The effective graph has position-dependent connectivity.

## Test 2: Effective metric differs from flat

Define d_eff(r) = -log|G(r)|. With gravity, Delta_d = d_grav - d_flat is
+0.10 at r<=3 (near mass) and -0.01 at r>=6 (far from mass). The effective
distance profile changes shape -- the propagator sees a curved metric.

## Test 3: Spectral dimension changes

The heat-kernel spectral dimension d_s (from random walk return probability
on the weighted graph) is ~2.9 on the flat lattice. With gravity:
- Center (f=1.23): d_s = 2.74, Delta = -0.17
- Near (r=2, f=0.18): d_s = 2.77, Delta = -0.14
- Mid (r=5, f=0.04): d_s = 2.85, Delta ~ 0
- Far (r=8, f=0.01): d_s = 2.54, Delta ~ 0

Gravity reduces the effective dimension near the source.

## Test 4: Geometry responds to matter placement

Adding a second mass B changes the effective distance from mass A:
- RMS metric shift ~0.03 (both mass B placements)
- Along the direction toward B: RMS = 0.038
- Perpendicular to B: RMS = 0.022
- The shift is anisotropic -- geometry responds directionally to matter

## Key Statement

Although the graph topology is fixed, the effective geometry -- as measured
by propagator Green's functions, spectral dimension, and connectivity --
changes in response to the gravitational field. The input graph provides the
substrate; the geometry is an output.

## Script

`scripts/frontier_background_independence.py` (N=20, M=5, k=1, ~1.3s runtime)
