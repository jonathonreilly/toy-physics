# Spectral Symmetry: Graph Discrete Symmetry Controls Decoherence

**Important:** this is a historical branch snapshot. For the current
review-safe read on `main`, see
[`docs/HIGHER_SYMMETRY_COMPARISON_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_COMPARISON_NOTE.md).
The retained takeaway from this line is only that `Z₂×Z₂` is an
exploratory decoherence-side lead, not a Born/gravity-validated successor.

**Date:** 2026-04-03
**Branch:** claude/distracted-napier
**Status:** Complete. Three-tier result: theorem, mechanism, quantitative scaling.

## The theorem (workstream 3)

On connected causal DAGs with linear path-sum propagation, the
per-layer transfer matrix product T_N...T_1 converges to rank-1.

Evidence: second singular value < 1e-30 at all tested N (12-80).
Lindeberg condition passes (no single layer dominates).

Consequence: any two initial conditions (slit A, slit B) produce
identical detector distributions at large N. Decoherence ceiling
is a spectral property of the matrix product.

## The mechanism (workstream 2)

Discrete symmetries of the graph force the transfer matrix product
to maintain rank > 1.

If the graph has Z₂ symmetry (y → -y), the transfer matrices
commute with the reflection operator R. The product decomposes
into even/odd sectors, each with its own rank-1 limit. Full
product maintains rank-2.

More symmetry = higher rank:
  Z₂: rank-2 (even/odd sectors)
  Z₂×Z₂: rank-4 (four quadrant sectors)

Slits at y > 0 and y < 0 map to different symmetry sectors.
They CANNOT converge by symmetry, regardless of N.

## The quantitative scaling

| Symmetry | Exponent | Prefactor | N_half | Born |
|----------|----------|-----------|--------|------|
| None (random) | -1.0 | ~0.3 | ~150 | perfect |
| Z₂ (y mirror) | -0.27 | 0.59 | 4.7M | perfect |
| Z₂×Z₂ (y+z) | -0.32 | 1.05 | 2.4M | perfect |

Z₂×Z₂ has the strongest absolute decoherence (38% at N=25,
22% at N=80) despite a slightly steeper exponent than Z₂.
The advantage is the prefactor: more sectors = more decoherence
at any given N.

## Joint coexistence (mirror S4 family)

At N=100 on mirror S4 (NPL_HALF=40, r=5, hybrid chokepoint):
  Born: 2.7e-15 (machine precision)
  Gravity: +2.81 (3.1 SE)
  Decoherence: 15% (pur_cl = 0.851)
  d_TV: > 0.5

Full four-way coexistence confirmed through N=100.

## Key findings

1. **The exact symmetry must be imposed.** Statistical y-symmetry
   (random uniform placement) gives intermediate results. The CLT
   breaks approximate symmetry at large N.

2. **Gravity requires asymmetric mass.** Mirror symmetry helps
   decoherence but symmetric mass placement cancels deflection.
   Asymmetric mass (y > 0 only) restores gravity.

3. **Born is unaffected.** All symmetry variants give Born = 1e-15
   to 3e-15 (machine precision) on standard linear propagator.

4. **Physical interpretation:** Spatial parity symmetry of the
   event space is a structural requirement for persistent decoherence.
   In standard physics, parity IS a fundamental discrete symmetry.

## What this means for the model

The discrete symmetry finding connects to the axioms:

Axiom 1 says reality is events + relations. The mirror symmetry
says the relations (edge structure) must respect a discrete spatial
symmetry. This is a constraint on the event space geometry.

Axiom 9 says measurement separates alternatives. The symmetry
ensures that "upper slit" and "lower slit" remain PERMANENTLY
distinct alternatives — the symmetry sectors are orthogonal
subspaces that cannot mix.

Axiom 10 says large-scale structure comes from persistent local
mechanisms. The Z₂ symmetry IS a persistent local mechanism —
it constrains every edge, not just a global property.

## Open questions

1. Does Z₂×Z₂ give stronger gravity than Z₂ with proper edge mirroring?
2. Can the symmetry be weakly broken (small explicit breaking parameter)
   while maintaining most of the decoherence improvement?
3. Does the exponent hierarchy generalize: Z₂^n → exponent ~ -1/2^n?
4. What is the physical interpretation of the Z₂×Z₂ group for a
   discrete spacetime model?

## Scripts

| Script | What it tests |
|--------|--------------|
| ceiling_formal_proof.py | Transfer matrix rank-1, Lyapunov spectrum |
| mirror_symmetric_dag.py | Z₂ decoherence, d_TV, CL bath |
| mirror_chokepoint_joint.py | Born + gravity + decoherence on chokepoint |
| mirror_scaled_joint.py | Scaling to N=80-100, multiple NPL/radius |
| approximate_mirror.py | Exact vs statistical vs asymmetric |
| higher_symmetry_dag.py | Z₂ vs Z₂×Z₂ vs ring vs random |
| quaternion_propagator.py | Non-commutative algebra (modest effect) |
| dynamical_topology.py | Amplitude-driven edge evolution |
| dynamical_soft_channels.py | Soft slit-specificity weighting |
| dynamical_cumulative_channels.py | Cumulative weights (saturates) |
| periodic_barriers.py | Multiple bottlenecks |
| tree_lattice_interpolation.py | Sweet spot at p=0.50 |
| dimensional_clt_rate.py | Higher dimension scaling (inconclusive) |
