# CKM Wolfenstein Parameters from BZ Corner Charge Geometry

## Status

**BOUNDED** -- not a closed CKM derivation.

Per `review.md`: CKM remains bounded until the Higgs Z_3 charge step is
L-independent.  This note investigates a specific algebraic route and
honestly reports what it achieves and where it fails.

## Theorem / Claim

**Bounded claim:** The BZ corner charge structure, combined with EWSB axis
selection, produces a qualitative structural distinction between the three
CKM mixing angles.  The Z_3 expansion parameter eps = 1/3 gives
order-of-magnitude agreement with the Cabibbo angle (within ~50%).

**Not claimed:** The Wolfenstein parameters (lambda, A, rho, eta) are NOT
algebraically derived from the BZ geometry.  Four specific obstructions
prevent closure.

## Assumptions

1. Three hw=1 BZ corners at positions (1,0,0), (0,1,0), (0,0,1) in
   (weak, color_1, color_2) space -- this is exact from the orbit algebra.

2. EWSB selects direction 1 (weak) as special -- exact from the framework.

3. Z_3 expansion parameter eps = 1/3 from the cubic lattice cyclic symmetry
   -- exact.

4. Froggatt-Nielsen Yukawa matrix Y_ij ~ eps^{sum_d |q_i^d - q_j^d|} --
   this is a MODEL ASSUMPTION, not derived from the lattice axioms.

5. Weak/color asymmetry in the FN suppression -- MODEL ASSUMPTION.

## What Is Actually Proved

### Exact results

1. **Charge structure:** The three BZ corners sit at standard basis positions
   in a 3D charge space.  All pairwise L_1 distances are exactly 2
   (democratic).

2. **EWSB decomposition:** After EWSB selects direction 1, the charge
   distances decompose into (weak, color) components:
   - Gen1-Gen2: (1, 1) -- one weak step, one color step
   - Gen1-Gen3: (1, 1) -- one weak step, one color step
   - Gen2-Gen3: (0, 2) -- zero weak steps, two color steps

3. **Structural distinction:** V_cb (Gen2-Gen3 mixing) involves ONLY color
   directions, while V_us and V_ub involve the weak direction.  This is an
   exact consequence of the charge geometry + EWSB.

4. **Democratic obstruction:** The Wolfenstein power counting (1, 2, 3)
   requires equal weak/color weights (r = 1), which recovers the democratic
   case.  The hierarchy then comes entirely from unitarity/diagonalization,
   not from the charge geometry.

### Bounded results

5. **Cabibbo angle:** eps = 1/3 gives |V_us| ~ 0.33, compared to the PDG
   value 0.225.  The ratio is 1.48 -- the right order of magnitude but 48%
   too large.

6. **V_cb from color-only suppression:** With eps_C = eps^{3/2}, the model
   gives |V_cb| ~ eps^3 = 0.037, compared to PDG 0.042 (ratio 0.88).
   This is a fit, not a derivation.

## What Remains Open

### Obstruction 1: eps != lambda

The Z_3 parameter eps = 1/3 = 0.333 does not equal the Cabibbo angle
sin(theta_C) = 0.225.  To close this gap requires a derived correction
factor, which is not currently available.

### Obstruction 2: Higgs Z_3 charge (review.md live blocker)

The FN mechanism requires the Higgs to carry Z_3 charge delta = 1.
Previous work showed this is either L-dependent on the staggered lattice
or an equal superposition of all Z_3 charges from the VEV structure.
This is the primary review blocker.

### Obstruction 3: Weak/color asymmetry not derived

The weighted-FN model needs a quantitative weak vs. color asymmetry
parameter.  The BZ geometry gives equal distances (2) in all directions.
EWSB qualitatively distinguishes directions but the quantitative
suppression ratio is not derivable from lattice geometry alone.

### Obstruction 4: V_us = V_ub degeneracy

Gen1-Gen2 and Gen1-Gen3 have identical (weak, color) distances = (1, 1).
The naive model gives |V_us| = |V_ub|, which disagrees with experiment
by a factor of ~57.  Resolution requires unitarity corrections or
additional structure beyond the simple FN picture.

## How This Changes The Paper

This note provides:

- A cleaner formulation of why CKM is bounded, with four explicit
  obstructions identified
- A structural result: V_cb is color-only while V_us/V_ub are
  weak+color (exact from the BZ geometry)
- Order-of-magnitude agreement for the Cabibbo angle (bounded)

It does NOT upgrade CKM from bounded to closed.  The paper should
continue to present CKM as a bounded consistency result.

## Commands Run

```bash
cd /Users/jonBridger/Toy\ Physics && python scripts/frontier_ckm_derived.py
```
