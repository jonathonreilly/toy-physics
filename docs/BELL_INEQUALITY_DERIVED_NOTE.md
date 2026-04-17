# Bell Inequality (CHSH) Violation from Cl(3) Taste Species on Z^d

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** ~2-5 minutes (dominated by 3D 4x4x4 eigenvalue decomposition)

## Claim

CHSH Bell violation with proper tensor product factorization on Z^d
lattices, using Poisson gravitational coupling between distinguishable
taste species from the Cl(3) staggered structure. No post-selection, no
sector restriction, full C^N tensor C^N Hilbert space.

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
  +--> 2^d taste species per physical site
         |
         +--> two DISTINGUISHABLE particles (different taste states)
         +--> tensor product H_A (x) H_B = C^N (x) C^N
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

### Ground state

| Lattice | N | N^2 | m | G | |S| | Violation |
|---|---|---|---|---|---|---|
| 1D N=8 | 8 | 64 | 0.1 | 1000 | >2.0 | YES |
| 2D 4x4 | 16 | 256 | 0.1 | 100 | 2.076 | YES |
| 3D 4x4x4 | 64 | 4096 | 0.1 | 2000 | 2.077 | YES |
| 3D 4x4x4 | 64 | 4096 | 0.1 | 5000 | 2.495 | YES |

### Dynamical (product initial state)

| Lattice | m | G | |S| | Route |
|---|---|---|---|---|
| 1D N=8 | 0.1 | 50 | 2.291 | product -> evolve |

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
| Distinguishable particles | Different taste species (2^d per site) | Cl(3) from A2 |
| Tensor product H_A (x) H_B | SINGLE_AXIOM_HILBERT_NOTE | A1+A2 |
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
- Distinguishable particles (different taste species), so no fermionic
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
