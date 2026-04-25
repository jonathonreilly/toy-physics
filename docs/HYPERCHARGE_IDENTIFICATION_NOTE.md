# Hypercharge U(1)_Y Identification from the Commutant

## Statement

**Theorem.** The unique traceless U(1) direction in the commutant algebra
su(3) + u(1) of {SU(2)\_weak, SWAP\_{23}} in End(C^8) matches the Standard
Model hypercharge assignments on the left-handed doublet surface.

## Setup

The taste space C^8 = (C^2)^{x3} carries two structures:

1. **SU(2)\_weak**: S\_i = sigma\_i/2 on factor 1, derived from the bipartite
   lattice structure.
2. **SWAP\_{23}**: exchanges tensor factors 2 and 3, from the Z\_2 spatial
   permutation symmetry.

The commutant of {SU(2), SWAP\_{23}} in End(C^8) is gl(3,C) + gl(1,C),
established in `frontier_su3_commutant.py`. The mechanism:

- SU(2) on factor 1 forces the commutant to be gl(4,C) on factors 2,3
  (by Schur's lemma).
- SWAP\_{23} decomposes C^4 = C^2 x C^2 into Sym^2(C^2) = C^3 and
  Anti^2(C^2) = C^1.
- gl(4) restricted to this decomposition = gl(3) + gl(1).
- Compact + traceless form: su(3) + u(1).

## The U(1) Generator

The commutant gl(3) + gl(1) contains two independent U(1) generators:

- P\_sym: the projector onto Sym^2(C^2) (center of gl(3))
- P\_anti: the projector onto Anti^2(C^2) (the gl(1))

General U(1): Y(a,b) = a P\_sym + b P\_anti, embedded in C^8 as I\_2 x Y.

Eigenvalues on C^8: a (x6 quark states), b (x2 lepton states).

**Tracelessness condition** (removing the trivial overall phase):

    6a + 2b = 0  =>  b = -3a

This leaves a unique traceless generator (up to normalization):

    Y = a (P_sym - 3 P_anti)

## Proof: This Matches Hypercharge

### 1. Eigenvalue Matching

With conventional normalization a = 1/3:

| Subspace | Multiplicity | Y value | SM identification |
|----------|-------------|---------|-------------------|
| (2,3) = C^2 x Sym^2(C^2) | 6 | +1/3 | Left-handed quark doublet |
| (2,1) = C^2 x Anti^2(C^2) | 2 | -1 | Left-handed lepton doublet |

These match the Standard Model hypercharge values on the left-handed
doublet surface:
- Q\_L = (u\_L, d\_L): Y = +1/3
- L\_L = (nu\_L, e\_L): Y = -1

### 2. Electric Charge

With T\_3 = sigma\_3/2 on the weak factor and Q = T\_3 + Y/2:

| Particle | T\_3 | Y | Q = T\_3 + Y/2 |
|----------|------|---|----------------|
| u\_L (3 colors) | +1/2 | +1/3 | +2/3 |
| d\_L (3 colors) | -1/2 | +1/3 | -1/3 |
| nu\_L | +1/2 | -1 | 0 |
| e\_L | -1/2 | -1 | -1 |

All charges match the Standard Model exactly.

### 3. Uniqueness

The argument is purely algebraic:

1. The commutant contains a 2-dimensional space of U(1) generators
   (center of u(3), plus the explicit u(1)).
2. The tracelessness condition imposes one linear constraint.
3. This reduces the space to **dimension 1** -- a unique generator up to
   normalization.
4. That unique generator has eigenvalue ratio 1:(-3) on (2,3) vs (2,1).
5. This matches hypercharge on the left-handed doublet surface.

### 4. Consistency Checks on the Left-Handed Surface

For the 8 left-handed states:

- **Tr[Y] = 0**: 6(1/3) + 2(-1) = 0. The traceless direction removes the
  overall phase.
- **Tr[Y {S\_i, S\_j}] = 0**: The SU(2)^2-U(1) mixed trace vanishes on this
  left-handed surface because Tr\_color[Y] = 3(1/3) + 1(-1) = 0.
- **Tr[Y^3] != 0**: Expected on a left-handed-only surface. Full anomaly
  cancellation requires the right-handed fermions as well.

### 5. GUT Normalization

The GUT-normalized hypercharge Y\_GUT = sqrt(3/5) Y\_SM. The ratio
Tr[Y^2] = 8/3 and Tr[T\_a^2]\_SU(3) = 1 are consistent with the standard
SU(5) embedding.
This squared-trace arithmetic is now packaged as the standalone retained
subtheorem
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md).

## Key Insight

The hypercharge identification is not an additional input or assumption.
It is a **consequence** of three ingredients on the left-handed surface:

1. C^8 = (C^2)^{x3} (taste space from the staggered lattice)
2. SU(2)\_weak on factor 1 (from bipartite structure)
3. SWAP\_{23} symmetry (from spatial permutation)

The commutant algebra forces su(3) + u(1), and within that algebra the
traceless U(1) generator is **unique up to normalization** and matches
hypercharge.

## Files

- `scripts/frontier_hypercharge_identification.py`: Full numerical verification
- `scripts/frontier_su3_commutant.py`: Prior result establishing the commutant
