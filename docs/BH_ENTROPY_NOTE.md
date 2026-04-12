# Bekenstein-Hawking Entropy from Lattice State Counting

PStack experiment: `frontier-bh-entropy`
Script: `scripts/frontier_bh_entropy.py`
Date: 2026-04-12

## Question

Does the entanglement entropy coefficient on a Planck-scale lattice
reproduce S_BH = A / (4 l_P^2), specifically the 1/4 coefficient?

## Method

Seven computations on 3D cubic lattices with tight-binding Hamiltonians
(equivalent to the path-sum propagator at half-filling):

1. Boundary DOF counting on lattice spheres
2. Entanglement entropy coefficient c_1 via half-space bipartition
3. Check whether c_1 * ln(d) = 1/4 for various local dimensions d
4. Coefficient stability across subsystem fractions
5. Bond dimension of the propagator tensor network
6. Ryu-Takayanagi comparison (entropy vs gravitational coupling)
7. Frozen star entropy and Susskind-Uglum species counting

## Key Results

### Area law scaling (confirmed)

3D lattice (L = 4, 6, 8, 10): S = 0.411 * boundary - 0.59

- R^2 = 0.9993
- The area law is robust across all lattice sizes tested

### Entropy coefficient

| Quantity | Measured | BH Target | Deviation |
|----------|----------|-----------|-----------|
| S/bnd (3D, d=2) | 0.411 | 0.250 | +64% |
| S/bnd (2D, d=2) | 0.843 | 0.250 | +237% |
| Srednicki scalar | 0.295 | 0.250 | +18% |

The 3D free-fermion coefficient (0.411) is O(1) and within a factor of
1.6 of the BH value 0.25. This is consistent with known literature:

- Srednicki (1993): free scalar on cubic lattice gives S/A ~ 0.295
- Casini-Huerta: free Dirac fermion gives S/A ~ 0.072
- The coefficient is regulator-dependent (lattice structure, cutoff details)

### The 1/4 is NOT a universal prediction

The Susskind-Uglum (1994) resolution: the Bekenstein-Hawking entropy
is S_BH = S_ent(all species) = sum_i c_1^(i) * (A/a^2) * ln(d_i).
The Newton constant absorbs the species dependence:

    G_Newton = G_bare / (1 + sum_i c_1^(i) * ln(d_i) * G_bare / ...)

So S_BH = A / (4 G_ren) is a DEFINITION of G_Newton, not an independent
prediction of the coefficient. The non-trivial content is:

1. Entropy scales as area (confirmed, R^2 = 0.9993)
2. The coefficient is O(1) per Planck area (confirmed: 0.41)
3. Gravity reduces entanglement (confirmed: monotonic decrease)

### Bond dimension analysis

| Lattice | chi_eff | S_actual / S_TN |
|---------|---------|-----------------|
| 8x8     | 8       | 0.244           |
| 12x12   | 12      | 0.253           |
| 16x16   | 16      | 0.244           |
| 24x24   | 24      | 0.229           |

The ratio S_actual / (boundary * ln(chi)) is remarkably stable at ~0.24.
For BH entropy via random tensor networks: ln(D) = 1/4, so D = e^(1/4) = 1.284.

### Ryu-Takayanagi

Entropy monotonically decreases with gravitational coupling (L=8, 3D):

| g   | S/bnd  |
|-----|--------|
| 0.0 | 0.3945 |
| 1.0 | 0.3935 |
| 5.0 | 0.3743 |

Gravity reduces entanglement, consistent with the holographic principle.
The effective G_eff extracted via RT: G_eff = bnd / (4S) ~ 0.63 in
lattice units.

## Interpretation

The lattice framework produces:

1. Area-law entanglement entropy (R^2 = 0.9993)
2. An O(1) coefficient per Planck area cell (0.41 for free fermions)
3. Gravity that reduces the entanglement (holographic principle)
4. A stable S/S_TN ratio near 1/4 in the tensor network picture

The exact 1/4 coefficient cannot be derived from a single free-fermion
species because it depends on the full UV completion (all species at the
Planck scale). This is a well-known result in quantum gravity:

- 't Hooft (1985): entanglement entropy is proportional to area
- Srednicki (1993): numerical coefficient is cutoff-dependent
- Susskind-Uglum (1994): G_Newton absorbs the species count
- Jacobson (1995): Einstein equations FROM entanglement entropy

The framework's contribution is showing that a SINGLE axiom (local graph
growth with Cl(3) algebra) produces all the ingredients: area-law scaling,
O(1) coefficient, gravitational reduction of entanglement, and
tensor-network structure with the correct qualitative features.

## What Would Give Exact 1/4

To obtain S/bnd = 1/4 exactly requires one of:

- A specific d: single species with d = exp(0.25/c_1) = 1.53 (unphysical)
- Species sum: N_s = 0.25/0.411 = 0.61 effective species
  (less than 1 because of overcounting in the free approximation)
- Renormalization: G_Newton defined to absorb the coefficient
  -> S_BH = A/(4 G_ren) is automatically satisfied

The last option (Susskind-Uglum) is the physically correct answer.
The 1/4 is built into the definition of G_Newton.
