# Bell Inequality (CHSH) Violation on a Two-Species Tensor Product

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED (generic two-species model; identification
of tensor factors with specific Cl(3) taste operators is not yet derived
and is noted as an open gap below)
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** ~2-5 minutes (dominated by 3D 4x4x4 eigenvalue decomposition)

## Claim

CHSH Bell violation with a proper tensor product factorization
C^N ⊗ C^N on Z^d lattices, using Poisson gravitational coupling
between two distinguishable fermion species on the staggered
Hamiltonian. No post-selection, no sector restriction, full
Hilbert space.

**What the Bell bipartition IS:** a generic two-species tensor
product — two distinguishable fermion slots on the same staggered
lattice, each with its own single-particle Hamiltonian, coupled by
the Poisson Green's function.

**What the Bell bipartition is NOT (yet):** an explicit construction
from the Cl(3) taste operators {ξ_1, ξ_2, ξ_3}. The script uses
H1 ⊗ I + I ⊗ H1 with identical H1, not a projection onto specific
taste subspaces. Identifying the two factors with physical Cl(3)
taste species is an open derivation gap; see "Open gap" below.

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
  +--> 2^d taste species per physical cell [motivation, not used explicitly]
         |
         +--> two DISTINGUISHABLE particle slots (generic bipartition)
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
| Two distinguishable particles | Generic bipartition (framework has multiple species; specific taste identification open) | see "Open gap" |
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
- **Does not derive the Bell bipartition from Cl(3) taste operators.**
  See "Open gap" below.

## Open gap: tensor factors vs Cl(3) taste operators

The script constructs the two-particle Hamiltonian as a generic
bipartite tensor product:

    H = H1 ⊗ I + I ⊗ H1 + G * Σ_ij V(i,j) |i⟩⟨i| ⊗ |j⟩⟨j|

with identical single-particle H1 on both slots. This is a valid
tensor product factorization — Alice's operators act on the first
slot, Bob's on the second, [O_A ⊗ I, I ⊗ O_B] = 0 automatically —
but it is NOT yet a construction from the Cl(3) taste operators
{ξ_1 = σ_x ⊗ I ⊗ I, ξ_2 = I ⊗ σ_x ⊗ I, ξ_3 = I ⊗ I ⊗ σ_x}
that live on the staggered hypercube.

A full derivation from the taste structure would require:

1. Working on the 2^d-sized taste hypercube per physical unit cell.
2. Projecting onto specific taste subspaces (e.g., ξ_1 = +1 for
   Alice, ξ_1 = -1 for Bob) to define the two parties.
3. Showing that the staggered Hamiltonian restricted to each
   taste subspace reduces to the single-particle H1 used here.
4. Deriving the Poisson coupling between the two taste subspaces
   from the framework's self-consistent field equation (D5).

Without steps 1-4, the "distinguishable taste species" framing is
a physically motivated interpretation rather than a derivation.
The framework DOES have multiple distinguishable fermion species
(different flavors, generations, colors — see the retained gauge
and generation structure), and two such species would obey the
tensor product structure used here. But the specific identification
with taste operators is not constructed in this script.

**Honest status:** this is a valid Bell violation on a generic
two-species tensor product model that the framework supports. The
reduction to an explicit Cl(3) taste construction is an open gap.

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
