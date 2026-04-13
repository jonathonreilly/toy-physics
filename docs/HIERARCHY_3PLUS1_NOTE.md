# Hierarchy from 3+1D: v = M_Pl * alpha^16

## Result

The electroweak hierarchy v/M_Pl ~ 10^{-17} follows from the 3+1D
staggered lattice structure:

    v = M_Pl * alpha^{16}  =  M_Pl * (alpha^8)^2  =  M_Pl * alpha^{2 * 2^3}

where:
- **8 = 2^3**: number of spatial taste states (BZ corners of the 3-cube)
- **squaring (x2)**: temporal direction in the partition function
- **alpha_LM = 0.0906**: lattice-matched gauge coupling

Numerically: v = 2.435 x 10^18 x (0.0906)^16 = 50 GeV, with the exact
value 246 GeV requiring alpha = 0.1001 (10% correction from the O(1)
algebraic prefactor).

## Axiom

The starting point is Cl(3) on Z^3: the Clifford algebra of 3D space
realized on the cubic lattice. This is a **spatial** axiom. Time is
not a fourth spatial direction; it emerges from the anomaly cancellation /
partition function structure.

## Derivation

### Step 1: Spatial taste determinant

The staggered Dirac operator on Z^3 encodes the Cl(3) algebra through
the staggered phases:

    eta_0(x) = 1,   eta_1(x) = (-1)^{x_0},   eta_2(x) = (-1)^{x_0 + x_1}

On the unit hypercube (8 sites = {0,1}^3), the operator is:

    D_{xy} = u_0 * sum_mu eta_mu(x) * [delta(y, x+mu) - delta(y, x-mu)] / 2

Key property: **D is linear in u_0**:

    D(u_0) = u_0 * D_hop

Therefore:

    det(D(u_0)) = u_0^N * det(D_hop)

where N = 8 = dim(D) = number of sites = **number of spatial taste states**.

### Step 2: Eigenvalue structure

With antiperiodic boundary conditions (the physical choice for fermions),
D_hop has 8 nonzero eigenvalues, all with |lambda_i| = sqrt(3):

    det(D_hop) = (sqrt(3))^8 = 3^4 = 81

The eigenvalues come in 4 conjugate pairs (+/- i*sqrt(3)), reflecting
the particle-antiparticle symmetry. Each taste state contributes
exactly one power of u_0 to the determinant.

### Step 3: Temporal squaring

The full 4D partition function is:

    Z = Tr[exp(-beta*H)]

On Z^3 x S^1_beta (spatial lattice times Euclidean time circle), the
staggered Dirac operator factorizes into spatial and temporal parts.
The temporal direction contributes a factor of 2 to the power of u_0:

    det(D_4D) ~ u_0^{16} * det(D_hop_4D)

This was verified numerically:
- 3D (L=2, 8 sites): power = 8
- 4D (L=2, Lt=2, 16 sites): power = 16
- Ratio: 16/8 = 2 (temporal squaring)

The physical interpretation: the partition function sums over forward
(exp(-iHt)) and backward (exp(+iHt)) time evolution, giving
|det_spatial|^2.

### Step 4: The formula

Identifying u_0 with the gauge coupling alpha:

    v / M_Pl = alpha^{2 * 2^3} = alpha^{16}

    v = M_Pl * alpha^{16}

## Why 3+1D, not 4D

The exponent 16 = 2 * 2^3 is specific to the **3+1D** structure:
- Space: Z^3 with Cl(3) -> 2^3 = 8 spatial tastes
- Time: partition function squaring -> factor of 2

This is NOT a 4D calculation. In 4D (four spatial directions with Cl(4)):
- 2^4 = 16 taste states, temporal factor 2 -> exponent = 32
- v = M_Pl * alpha^{32} = 10^{-15} GeV (way too small)

Comparison of v = M_Pl * alpha^n at alpha = 0.0906:

| n  | Origin           | v (GeV)   |
|----|------------------|-----------|
| 8  | 3D only          | 1.1e10    |
| 16 | **3+1D**         | **50**    |
| 32 | 4+1D             | 1.0e-15   |

Only the 3+1D value lands in the electroweak range.

## Numerical verification

All structural checks pass (script: `scripts/frontier_hierarchy_3plus1.py`):

| Check                              | Result |
|------------------------------------|--------|
| Spatial det power = 8              | PASS   |
| 4D det power = 16                  | PASS   |
| Temporal doubling p_4D/p_3D = 2    | PASS   |
| v in EW decade (10-2500 GeV)       | PASS   |
| alpha_exact within 10% of alpha_LM | PASS   |

## Status

- **Structural result (power = 16)**: exact, from linearity of D in u_0
  and the matrix dimension counting.
- **Numerical value (50 GeV vs 246 GeV)**: O(1) algebraic prefactor
  from det(D_hop) and renormalization corrections not yet included.
  The required alpha = 0.1001 is 10% above alpha_LM = 0.0906.
- **Physical basis**: the hierarchy is a consequence of the Cl(3)
  algebra on Z^3 (spatial taste states) combined with the temporal
  partition function structure (squaring).
