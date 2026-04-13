# EWSB Generation Cascade: Mass Hierarchy from CW Symmetry Breaking

**Script**: `scripts/frontier_ewsb_generation_cascade.py`
**Status**: exact `1+2` boundary verified; bounded `1+1+1` model support
**Depends on**: `frontier_graph_first_selector_derivation`, `frontier_ewsb_s3_breaking`, `frontier_generation_physicality`, `frontier_matter_assignment_theorem`

## Strongest Safe Result

Let V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 be the graph-shift selector on the 3-cube taste graph. Then:

1. **V_sel breaks S_3 -> Z_2** by selecting one axis as "weak" (EWSB).

2. **The selected axis breaks Z_3 cyclic symmetry**: the orbit member whose "1" is in the selected direction is distinguished from the other two.

3. **At the exact symmetry level**: the selected axis gives a `1+2` mass structure,
   `M = diag(m_v, m_0, m_0)`.

4. **A bounded hierarchy mechanism exists**: the weak-direction member couples
   directly to the Higgs VEV while the color-direction members couple only
   radiatively.

5. **What remains open**: the further `Z_2 -> trivial` split giving
   `m_2 != m_3` is not derived from first principles on the current surface.
   The Jordan-Wigner / taste-breaking section below is a bounded mechanism
   model, not a closed theorem.

## Key Insight

The CW selector that determines the weak axis also breaks the Z_3 generation symmetry. This is because the three members of the Z_3 orbit T_1 = {(1,0,0), (0,1,0), (0,0,1)} project differently onto the selected axis:

- **(1,0,0)**: "1" is in the weak direction. Couples to the Higgs VEV via Gamma_1, connecting to the singlet (0,0,0) at Hamming weight 0. Gets a large self-energy correction.
- **(0,1,0)**: "1" is in a color direction. Gamma_1 connects it to (1,1,0) in T_2 at Hamming weight 2. Gets a smaller radiative correction.
- **(0,0,1)**: "1" is in the other color direction. Gamma_1 connects it to (1,0,1) in T_2. Same as (0,1,0) at leading order (residual Z_2).

## Proof Structure

### Step 1: EWSB mass matrix

With the VEV phi = (v, 0, 0), the Yukawa mass operator is M = y*v*Gamma_1. Since Gamma_1^2 = I_8, all orbit members get the same tree-level mass. The splitting must come from higher-order (radiative) effects.

The gauge-scalar coupling Tr[B_k Gamma_mu B_k Gamma_mu] is direction-dependent, so direction 1 is distinguished from directions 2,3. The exact residual `1+2` statement is established by the selector/Hessian/intermediate-state structure, not by requiring the bare direction-2 and direction-3 traces to coincide entrywise.

### Step 2: Z_3 breaking

The Z_3 permutation sigma maps S_1 -> S_3 -> S_2 -> S_1. After EWSB with the VEV in direction 1, sigma does not preserve the VEV: sigma(v,0,0) = (0,0,v) != (v,0,0). Only the Z_2 swap of directions 2,3 survives.

The Hessian of V_sel at the VEV confirms:
- d^2V/dphi_1^2 = 0 (flat direction -- Goldstone)
- d^2V/dphi_2^2 = d^2V/dphi_3^2 = 64 v^2 (massive, Z_2 degenerate)

The radiative mass splitting is:
- m_heavy/m_0 = 1 + (g^2/16pi^2) * log(M_Pl/v) ~ 1.10
- m_light/m_0 = 1 + (g^2/16pi^2) * O(1) ~ 1.003

### Step 3: Color cascade (Z_2 breaking)

The residual Z_2 between directions 2 and 3 is broken by the Jordan-Wigner structure of the Kawamoto-Smit representation:
- Gamma_2 = sigma_z x sigma_x x I (1 JW string)
- Gamma_3 = sigma_z x sigma_z x sigma_x (2 JW strings)

The O(a^2) taste-breaking corrections from the lattice are JW-dependent:
- delta_m^2(dir 2) ~ alpha_s * (1 + beta * n_JW(2)) = alpha_s * (1 + beta)
- delta_m^2(dir 3) ~ alpha_s * (1 + beta * n_JW(3)) = alpha_s * (1 + 2*beta)

This splits m_2 from m_3, completing the cascade S_3 -> Z_2 -> trivial.

### Step 4: Mass ratios

Three hierarchy mechanisms are consistent with observations:

| Mechanism | m_top : m_charm : m_up |
|-----------|----------------------|
| Loop suppression | 1 : 0.0027 : 7.3e-6 |
| Loop + large log | 1 : 0.10 : 0.011 |
| Froggatt-Nielsen (taste scale) | 1 : 0.08 : 0.006 |
| **Observed** | **1 : 0.0073 : 1.3e-5** |

The pure loop-suppression factor g^2/(16pi^2) ~ 0.003 matches the charm/top ratio to within an order of magnitude. The up/top ratio requires either large logs or a Froggatt-Nielsen-like suppression from the Z_3 structure.

## Current Boundary

What is exact:
1. the selector picks a weak axis
2. the selected axis distinguishes one orbit member from the residual pair
3. the symmetry-level generation structure is `1 + 2`

What is bounded/model-level:
1. the residual `2 -> 1 + 1` split
2. the order-of-magnitude hierarchy estimates

So this lane strengthens the generation story, but it does **not** by itself
close the generation physicality gate.

## Caveats

1. **Quantitative precision**: The mass ratios are order-of-magnitude, not exact. A full computation would require the 2-loop CW potential with the complete lattice dispersion relation.

2. **JW beta coefficient**: The JW correction parameter beta_JW = 0.1 used in the
   residual `Z_2`-breaking calculation is a model input, not derived from first
   principles. A lattice perturbation theory computation at O(g^2 a^2) would
   be needed to promote this section.

3. **Tree-level degeneracy**: At tree level, all orbit members have the same mass. The hierarchy is entirely radiative, which is physically correct (SM Yukawa hierarchies are not explained at tree level either) but requires the full loop computation for precision.
