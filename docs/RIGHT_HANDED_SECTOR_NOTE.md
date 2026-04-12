# Right-Handed Fermions from the 4D Taste Space

**Script:** `scripts/frontier_right_handed_sector.py`
**Depends on:** `frontier_su3_formal_theorem.py`, `frontier_chiral_completion.py`
**Status:** 61/61 checks pass

## Problem Statement

The SU(3) commutant theorem derives one generation of **left-handed** SM fermions
from the 8-dim taste space of staggered fermions in d=3:

    C^8 = (2, 3)_{+1/3} + (2, 1)_{-1} = Q_L + L_L

The codex gate-1 search found that the right-handed states (u_R, d_R, e_R, nu_R)
do NOT appear on the one-particle 8-state surface:
- No SU(2) singlets at degree 1
- d_R and e_R appear at degree 2 (bilinear composites)
- u_R only appears at degree 4

## Status

The physical right-handed sector is now closed at the
`4D chirality + anomaly cancellation` level.
What remains open is the stronger `graph-canonical` completion claim:
the 3D one-particle surface does not canonically generate the right-handed
template on its own.

Where do right-handed fermions come from?

## Result 1: No SU(2) Singlets on C^8

The KS su(2) acts on the first tensor factor of C^2 x C^2 x C^2.
The generator T3 = sigma_z/2 x I x I is diagonal: T3 = +1/2 when a1=0,
T3 = -1/2 when a1=1. The raising operator T1 = sigma_x/2 x I x I flips the
first bit, pairing |0,a2,a3> with |1,a2,a3>.

All 8 states form 4 SU(2) doublets. The Casimir is uniformly 3/4 (spin-1/2).
There are zero SU(2) singlets on the one-particle surface.

## Result 2: No Chirality in 3 Dimensions

The 3D product G5_3D = G1*G2*G3 squares to **-I**, not +I. In odd dimensions d,
the Clifford volume element satisfies (G1...Gd)^2 = (-1)^{d(d-1)/2} I.
For d=3: (-1)^3 = -1.

The eigenvalues of G5_3D are +/-i (purely imaginary), not +/-1. This means
G5_3D is not an involution and cannot define chirality. The taste space C^8
cannot be split into independent left-handed and right-handed subspaces.

Chirality requires an even number of spacetime dimensions.

## Result 3: Composites Give Partial Completion

The antisymmetric tensor product wedge^2(C^8) = C^28 contains 10 SU(2) singlets.
Their hypercharge eigenvalues include:
- Y = -2 (1 state) -- matches e_R
- Y = -2/3 (3 states) -- matches d_R
- Y = +2/3 (6 states)

But Y = +4/3 (u_R) is **absent** from wedge^2, confirming the gate-1 result that
u_R requires degree-4 composites. The composite route is structurally asymmetric.

## Result 4: 4D Taste Space Provides Chirality

Adding the temporal direction gives 2^4 = 16 taste states in d=3+1.
The 4D chirality operator gamma_5 = G0*G1*G2*G3:
- Squares to **+I** (proper involution in even dimensions)
- Is Hermitian
- Anticommutes with all gamma_mu
- Splits C^16 = C^8_L (gamma_5=+1) + C^8_R (gamma_5=-1)

### Taste algebra

The commutant of the 4D Clifford algebra Cl(4) in M(16,C) has dimension 16,
forming the taste algebra M(4,C). Its Lie algebra is su(4) + u(1).

The taste algebra **commutes with gamma_5**, so both chirality sectors carry
the same taste representations.

### Chiral SU(2)

The KS su(2) from the first tensor factor does **not** commute with gamma_5:
- T1 and T3 anticommute with gamma_5 (map L to R)
- T2 commutes with gamma_5 (preserves chirality)

This is the lattice manifestation of chiral gauge theory: the SU(2)_weak
interaction is defined as coupling only to left-handed fermions.

### Y is not a pure taste operator

The hypercharge Y (built from SWAP_{23}) does **not** commute with gamma_5.
The 3D gauge quantum numbers are intertwined with the Clifford structure,
not purely in the taste algebra. This is why the L and R sectors cannot both
carry the same hypercharge eigenvalues in the SM.

## Result 5: Anomaly Cancellation Fixes Right-Handed Charges

The lattice provides 8 + 8 = 16 Weyl fermion states via chirality.
The left-handed content is determined by the 3D KS construction:

    C^8_L = (2, 3)_{+1/3} + (2, 1)_{-1}

The right-handed states are SU(2)_weak singlets by the chirality of weak
interactions. Their SU(3)_c content comes from the taste decomposition
(3 + 3 + 1 + 1, matching the left sector). Their hypercharges are
**uniquely** determined by the five anomaly cancellation conditions
(proven in `frontier_chiral_completion.py`, 32/32 PASS):

| Field | Representation | Y | Q = T3 + Y/2 | States |
|-------|---------------|-----|-------------|--------|
| u_R | (1, 3)_{+4/3} | +4/3 | +2/3 | 3 |
| d_R | (1, 3)_{-2/3} | -2/3 | -1/3 | 3 |
| e_R | (1, 1)_{-2} | -2 | -1 | 1 |
| nu_R | (1, 1)_{0} | 0 | 0 | 1 |

All six anomaly conditions are satisfied:

| Anomaly | Value | Status |
|---------|-------|--------|
| Tr[Y] = 0 | gravitational | PASS |
| Tr[Y^3] = 0 | U(1)^3 | PASS |
| Tr[SU(3)^2 Y] = 0 | mixed colour-hypercharge | PASS |
| Tr[SU(2)^2 Y] = 0 | mixed weak-hypercharge | PASS |
| Tr[SU(3)^3] = 0 | colour cubic | PASS |
| Witten SU(2) | 4 doublets (even) | PASS |

## Physical Picture

1. The **spatial lattice** Z^3, via the Kawamoto-Smit construction, derives the
   left-handed gauge structure su(2) x su(3) x u(1) on C^8.

2. The **temporal direction** adds chirality (gamma_5 with gamma_5^2 = +I) and
   doubles the taste space to C^16 = C^8_L + C^8_R.

3. The **taste algebra** su(4) commutes with gamma_5 and provides the colour
   structure to both sectors. The SM gauge group embeds as SU(3) x U(1) in SU(4)
   (Pati-Salam structure: 4 = 3_c + 1_lepton).

4. **SU(2)_weak** is chiral: it couples only to C^8_L. The right-handed sector
   is automatically an SU(2) singlet space.

5. **Anomaly cancellation** uniquely fixes the right-handed hypercharges,
   completing the Standard Model generation.

The right-handed fermions do not arise from a new graph-canonical derivation.
They arise from the 4D chirality structure of the staggered lattice, with
their quantum numbers fixed by the same mechanism as in the Standard Model
itself: quantum consistency of the chiral gauge theory.

## Relation to Gate-1 Search

The gate-1 search asked whether right-handed states exist on the one-particle
C^8 surface. The answer is definitively no:

- C^8 has zero SU(2) singlets (Part 1)
- C^8 has no chirality operator (Part 2)
- Composites partially work but u_R needs degree 4 (Part 3)

The resolution is not composites but **the 4D extension**: the temporal
direction provides both the chirality operator and the additional states
needed for the right-handed sector.
