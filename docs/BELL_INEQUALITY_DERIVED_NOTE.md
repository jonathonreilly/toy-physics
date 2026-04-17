# Bell Inequality (CHSH) Violation with Explicit Cl(3) Taste Measurements

**Date:** 2026-04-16
**Status:** RETAINED
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** ~2-5 minutes (dominated by 3D 4x4x4 eigenvalue decomposition)

## Claim

CHSH Bell violation on a tensor product Hilbert space C^N ⊗ C^N with:

- **Tensor factors = two distinguishable fermion species** (two flavors
  from the framework's retained multi-flavor content — different
  generations, flavors, or colors). The tensor product is genuine and
  the commutation [O_A, O_B] = 0 is automatic for single-species
  operators.
- **Measurements = explicit Cl(3) taste operators** built from the
  Kogut-Susskind spin-taste decomposition (Part 1 of the runner
  constructs them in the (cell, taste) basis and verifies the
  identification with the site-basis sublattice parity and pair-hop
  at machine precision).
- **Entanglement source = periodic Poisson coupling** (D5) between the
  two species. G=0 null control gives |S| = 2.000 exactly on every
  lattice.

## What IS explicitly derived

1. **KS spin-taste decomposition.** Each single-particle staggered
   lattice C^N factors as C^{N_cells} ⊗ C^{2^d} under the KS block
   decomposition (2^d sites per physical cell, 2^d taste states per
   cell). Site coordinates (x_1, ..., x_d) decompose as
   x_μ = 2·X_μ + η_μ with X ∈ cells, η ∈ {0,1}^d the taste bits.

2. **Cl(3) taste operators ξ_μ.** Constructed explicitly on the 2^d
   taste space per cell as σ-matrices on the taste qubits. The function
   `build_cell_taste_operator` in the runner builds I_cells ⊗ (Pauli
   product on taste qubits) in the full site basis.

3. **Z = I_cells ⊗ ξ_5.** The site-basis sublattice parity operator
   equals the explicit KS taste operator ξ_5 = σ_z ⊗ σ_z ⊗ ... ⊗ σ_z
   (product of σ_z on all d taste qubits). Verified at machine precision
   in Part 1 of the runner for d = 1, 2, 3.

4. **X = I_cells ⊗ ξ_last.** The site-basis pair-hop operator equals
   the explicit KS taste operator ξ_last = I ⊗ ... ⊗ I ⊗ σ_x
   (σ_x on the last taste qubit only). Verified at machine precision.

5. **Pauli algebra {Z, X} = 0.** Follows from σ_z σ_x = -σ_x σ_z on
   the shared taste qubit. Also verified directly at machine precision.

6. **Tensor product bipartition.** From SINGLE_AXIOM_HILBERT_NOTE; two
   distinguishable species give automatic [O_A ⊗ I, I ⊗ O_B] = 0.

## What is NOT claimed

- The bipartition is NOT obtained by projecting onto taste eigenstates
  of a single species. Each species carries its full 2^d-dim taste
  Hilbert space per cell; the bipartition comes from the two species
  being different particles.
- H1 is NOT a taste-projected kinetic operator. H1 is the full
  staggered Dirac Hamiltonian (hopping + mass), which does mix tastes.
  What is taste-preserving is each species' IDENTITY (Alice stays
  Alice); taste measurements on a single species' full Hilbert space
  are well-defined regardless of the internal taste dynamics.

## Derivation chain

```
A1 (graph axiom)
  |
  +--> Z^d periodic lattice (1D, 2D, 3D)
  |
A2 Cl(3) (Clifford algebra)
  |
  +--> staggered Dirac fermion (Kogut-Susskind)
  |      |
  |      +--> sublattice parity Z = (-1)^{x+y+z}  [eigenvalues +/-1]
  |      +--> pair-hop X (swap within (2k,2k+1))   [eigenvalues +/-1]
  |      +--> Y = iZX completes Pauli triple
  |      +--> {Z,X} = 0, Z^2 = X^2 = I verified on every lattice
  |
  +--> KS spin-taste decomposition (standard staggered-fermion tech)
         |
         +--> single-particle C^N = C^{N_cells} ⊗ C^{2^d}
         +--> taste algebra Cl(3): ξ_μ = Pauli on μ-th taste qubit
         +--> site-basis Z == I_cells ⊗ ξ_5 (verified in Part 1)
         +--> site-basis X == I_cells ⊗ ξ_last (verified in Part 1)
         |
         +--> two distinguishable fermion species (different flavors)
         +--> tensor product H_A ⊗ H_B = C^N ⊗ C^N
         +--> [ξ_μ^A ⊗ I, I ⊗ ξ_ν^B] = 0 (automatic, tensor product)
                |                         (SINGLE_AXIOM_HILBERT_NOTE)
                |
                +--> [O_A (x) I, I (x) O_B] = 0  AUTOMATIC
                |
                +--> H = H1(x)I + I(x)H1 + G * sum_ij V(i,j) |i><i|(x)|j><j|
                       |
                       +--> H1 = staggered Dirac (hopping + mass)
                       +--> V(i,j) = periodic Poisson Green's function (D5)
                       |
                       +--> G=0: |S| = 2.000 exactly (null control)
                       +--> G>0: |S| > 2 (Bell violation)
                       |
                       +--> Horodecki formula: T_ij = <psi|O_i^A(x)O_j^B|psi>
                            S = 2*sqrt(t1 + t2), t1,t2 largest evals of T^T*T
```

## Results

All numbers below reproduce from the current runner
(`scripts/frontier_bell_inequality.py`). Reviewer-verified as of
2026-04-16.

### Ground state (best per lattice)

| Lattice | N | N^2 | m | G | |S| | Violation |
|---|---|---|---|---|---|---|
| 1D N=8 | 8 | 64 | 0.0 | 1000 | 2.823 | YES |
| 1D N=8 | 8 | 64 | 0.1 | 50 | 2.070 | YES |
| 2D 4x4 | 16 | 256 | 0.0 | 1000 | 2.668 | YES |
| 2D 4x4 | 16 | 256 | 0.1 | 1000 | 2.577 | YES |
| 3D 4x4x4 | 64 | 4096 | 0.1 | 2000 | 2.077 | YES |
| 3D 4x4x4 | 64 | 4096 | 0.1 | 5000 | 2.495 | YES |

### Reviewer-verified cheap cases (for reproducibility)

| Lattice | m | G | |S| |
|---|---|---|---|
| 1D N=8 | 0.1 | 0 | 2.0000 (null) |
| 1D N=8 | 0.1 | 50 | 2.0704 |
| 2D 4x4 | 0.1 | 100 | 1.9994 (no violation at this point) |
| 2D 4x4 | 0.1 | 500 | 2.3589 |
| 2D 4x4 | 0.1 | 1000 | 2.5769 |

2D 4x4 requires larger G (≥ ~500) for ground-state violation at
m=0.1. Earlier reports of 2D 4x4 violation at G=100 conflated a
dynamical-sweep point with the ground-state table and are retracted.

### Dynamical (product initial state)

| Lattice | m | G | |S| | t_best | Route |
|---|---|---|---|---|---|
| 1D N=8 | 0.1 | 50 | 2.288 | 6.75 | product -> evolve |
| 1D N=8 | 0.0 | 50 | 2.294 | 4.50 | product -> evolve |
| 1D N=8 | 0.0 | 100 | 2.311 | 10.00 | product -> evolve |

### Null controls

| Lattice | G | |S| | Note |
|---|---|---|---|
| 1D N=8 | 0 | 2.000 | Exactly classical bound |
| 2D 4x4 | 0 | 2.000 | Exactly classical bound |
| 3D 4x4x4 | 0 | 2.000 | Exactly classical bound |

**G=0 gives |S| = 2.000 exactly on ALL lattices tested.** The Bell
violation requires gravitational coupling. This is the critical null
control: without the Poisson interaction, the tensor product state
remains separable regardless of mass or lattice geometry.

### Algebraic verifications

| Check | 1D N=8 | 2D 4x4 | 3D 4x4x4 |
|---|---|---|---|
| Z^2 = I | PASS | PASS | PASS |
| X^2 = I | PASS | PASS | PASS |
| {Z,X} = 0 | PASS | PASS | PASS |
| [O_A, O_B] = 0 | PASS | PASS | PASS |

## What is framework-native

| Ingredient | Origin | Axiom |
|---|---|---|
| Z^d lattice | Graph structure | A1 |
| Staggered Dirac fermion | Kogut-Susskind construction | Cl(3) from A2 |
| Sublattice parity Z = (-1)^{x+y+z} | Intrinsic to Z^d bipartite structure | A1 |
| Pair-hop X (swap in (2k,2k+1)) | Z^d nearest-neighbor connectivity | A1 |
| Pauli algebra {Z,X}=0, Z^2=X^2=I | Verified on every lattice | A1+A2 |
| Tensor product H_A ⊗ H_B | SINGLE_AXIOM_HILBERT_NOTE | A1+A2 |
| Two distinguishable fermion species with KS taste structure | retained multi-species matter content, each carrying the KS spin-taste decomposition and Cl(3) taste algebra on its internal taste factor | Cl(3) from A2 plus retained matter content |
| Measurement operator Z | Sublattice parity = ξ_5 (product of all Cl(3) taste generators) | Cl(3) from A2 |
| Measurement operator X | Pair-hop = Cl(3) rotation in taste algebra | Cl(3) from A2 |
| [O_A, O_B] = 0 | Automatic from tensor product | A1+A2 |
| Periodic Poisson Green's function | Graph Laplacian pseudoinverse | D5 |
| Product initial state | No entanglement inserted | -- |
| CHSH Horodecki formula | Standard quantum information | -- |

## Protocol

1. Build periodic staggered lattice on Z^d (1D, 2D, or 3D).
2. Construct single-particle staggered Hamiltonian H1 with hopping and
   Dirac mass m*(-1)^{x+y+z}.
3. Construct periodic Poisson Green's function V(i,j) via graph
   Laplacian eigendecomposition, excluding the zero mode.
4. Build the two-particle Hamiltonian on C^N tensor C^N:
   H = H1 (x) I + I (x) H1 + G * sum_ij V(i,j) |i><i| (x) |j><j|.
5. Construct sublattice measurement operators Z, X, Y = iZX.
6. Verify Pauli algebra (Z^2=I, X^2=I, {Z,X}=0) on each lattice.
7. Compute CHSH via Horodecki formula on the ground state or on a
   dynamically evolved product initial state.
8. Confirm G=0 null control: |S| = 2.000 exactly.

## Honest boundaries

### What this IS

- CHSH > 2 on a proper tensor product bipartition C^N (x) C^N.
- Distinguishable particles (different fermion species), so no fermionic
  anticommutation ambiguity.
- Full Hilbert space (no sector projection, no post-selection).
- [O_A, O_B] = 0 is automatic and verified.
- G=0 null control cleanly separates gravitational from kinematic effects.
- Poisson coupling is the sole entanglement source.

### What requires caution

- **Large G required for 3D.** The coupling G needed to see violation
  scales with dimension. On the 3D 4x4x4 lattice, G >= 2000 is needed
  for ground-state violation. This is a strong-coupling regime.
- **Lattice-size dependence not fully characterized.** The results are
  on small lattices (N=8, 4x4, 4x4x4). Scaling behavior to larger
  lattices has not been mapped.
- **G scales with dimension.** 1D violation appears at moderate G
  (~50), 2D at G~100, 3D at G~2000. The physical interpretation of
  these coupling strengths relative to a continuum limit is not
  established.
- **The Poisson coupling is diagonal** (V(i,j) |i><i| (x) |j><j|).
  This is a density-density interaction. The off-diagonal (hopping)
  part of the Hamiltonian provides the dynamics, while the Poisson
  coupling provides the entangling interaction.
- **Product initial state for dynamics** is both particles at the same
  site (site 0). This is a specific choice; other initial conditions
  have not been surveyed.
- **The dynamical CHSH oscillates.** The peak values reported are
  maxima over the evolution window, not equilibrium values.
- **Continuum limit.** The lattice spacing a is implicit (a=1).
  Connecting G to a physical gravitational constant requires a
  continuum-limit prescription that is not part of this note.
- **This is not a loophole-free Bell test.** It is a theoretical
  computation showing that the framework Hamiltonian produces states
  that violate the CHSH inequality with proper local bipartition.

### What this does NOT claim

- Does not claim to derive the Tsirelson bound from the framework.
- Does not claim the G values correspond to physical gravitational
  coupling constants.
- Does not claim universality across lattice sizes (only small lattices
  tested).
- Does not address the detection loophole or any experimental
  considerations.

## How the gap is closed

The reviewer's concern was that the runner did not construct the
Cl(3) taste structure explicitly — Z and X were position-basis
operators, not taste operators. This is now closed.

**The closure is in the IDENTIFICATION, verified numerically.**
Part 1 of the runner now calls `taste_identity_check`, which:

1. Explicitly constructs the (cell, taste) factorization of each
   single-particle Hilbert space, using x_μ = 2·X_μ + η_μ to
   decompose each site coordinate into a cell coordinate X_μ and
   a taste bit η_μ ∈ {0,1}.

2. Builds the KS taste operators as I_cells ⊗ (Pauli product on
   taste qubits) via `build_cell_taste_operator`.

3. Compares the site-basis Z and X operators to the explicit taste
   operators ξ_5 and ξ_last, verifying equality at machine
   precision on 1D (N=8), 2D (4×4), and 3D (4×4×4).

Output from the current runner:

```
1D N=8 KS taste identification:
  Z == I_cells ⊗ ξ_5  (ξ_5 = σ_z⊗...⊗σ_z on 1 taste qubits):  PASS
  X == I_cells ⊗ ξ_last (σ_x on last taste qubit only):       PASS
2D 4x4 KS taste identification:
  Z == I_cells ⊗ ξ_5  (ξ_5 = σ_z⊗...⊗σ_z on 2 taste qubits):  PASS
  X == I_cells ⊗ ξ_last (σ_x on last taste qubit only):       PASS
3D 4x4x4 KS taste identification:
  Z == I_cells ⊗ ξ_5  (ξ_5 = σ_z⊗...⊗σ_z on 3 taste qubits):  PASS
  X == I_cells ⊗ ξ_last (σ_x on last taste qubit only):       PASS
```

**The tensor bipartition is between two distinguishable fermion
species (flavors), not between two taste eigenstates of one species.**
This is the honest identification:

- Species A: flavor 1 fermion on the full staggered lattice
- Species B: flavor 2 fermion on the full staggered lattice
- Each species' single-particle space is C^N = C^{N_cells} ⊗ C^{2^d}
- Tensor product: C^N ⊗ C^N
- [O_A ⊗ I, I ⊗ O_B] = 0 for any species-A and species-B operators
- Measurement operators used (Z, X) are Cl(3) taste operators acting
  within each species' taste factor

The framework retains multiple distinguishable fermion species
(quark flavors, lepton flavors, three generations, three colors —
see the retained gauge and matter closure). Any two such species
provide the tensor factors required for this construction.

The gap is closed: the Cl(3) taste operators ξ_5 and ξ_last are
explicitly constructed in code, and the site-basis Z and X operators
used in the CHSH computation are verified to equal these taste
operators at machine precision on every tested lattice.

## Comparison with previous approach

The earlier version of this script used identical fermions in the
antisymmetric subspace with sector projection (Alice-1-Bob-1 sector).
That approach had two issues:

1. **Fermionic anticommutation** made [O_A, O_B] = 0 non-trivial to
   establish in the antisymmetric Fock space.
2. **Sector projection** (post-selection onto the Alice-1-Bob-1 sector)
   introduced a loophole.

The current approach resolves both by using distinguishable taste
species on C^N (x) C^N, where commutativity is automatic and no
post-selection is needed.

## What this adds to the publication surface

Previously retained:
- Born rule I_3 = 0 (pairwise interference)
- Gravitational entanglement (BMV-like, delta_S > 0)

This result adds:
- Explicit CHSH Bell violation on a proper tensor product bipartition
- G=0 null control confirming Poisson coupling as the entanglement mechanism
- Multi-dimensional verification (1D, 2D, 3D Z^3)
- No post-selection or sector restriction
- Pauli algebra from lattice structure verified

## Reproducibility

```
cd /path/to/Physics
python3 scripts/frontier_bell_inequality.py
```

Runtime: ~2-5 minutes total (3D points dominate). Requires numpy, scipy.
