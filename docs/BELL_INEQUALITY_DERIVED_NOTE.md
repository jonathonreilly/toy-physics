# Bell Inequality Violation from the Local Tensor Product Axiom

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED — CHSH violation with proper local bipartition
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** < 1 second

## Result

Starting from a product state on the 4-site staggered lattice, the
framework's own Hamiltonian (staggered hopping + periodic Poisson gravity)
dynamically produces maximal CHSH Bell violation:

| Route | |S| | Classical bound | Tsirelson | Parameters |
|---|---|---|---|---|
| Dynamical (product -> evolve) | **2.828** | 2.0 | 2.828 (saturated) | m=0.5, G=10, t=6.0 |
| Ground state | **2.051** | 2.0 | — | m=0.5, G=20 |

## Valid Alice/Bob factorization

The framework axiom (`SINGLE_AXIOM_HILBERT_NOTE`) is a local tensor
product Hilbert space H = H_0 ⊗ H_1 ⊗ H_2 ⊗ H_3. This provides the
Bell factorization directly:

- **Alice** owns factors {0, 1} (one even-odd site pair)
- **Bob** owns factors {2, 3} (one even-odd site pair, spatially separated)
- **[O_A, O_B] = 0** is automatic from the tensor product structure

Verified explicitly:

| Check | Result |
|---|---|
| [Z_A, Z_B] = 0 | True |
| [Z_A, X_B] = 0 | True |
| [X_A, Z_B] = 0 | True |
| [X_A, X_B] = 0 | True |
| Z_A^2 = X_A^2 = I | True |
| {Z_A, X_A} = 0 | True |
| Z_B^2 = X_B^2 = I | True |
| {Z_B, X_B} = 0 | True |

## Derivation chain

```
Cl(3) on Z^3 (framework axiom)
  |
  +---> local tensor product Hilbert space (SINGLE_AXIOM_HILBERT_NOTE)
  |       |
  |       +---> Alice = factors {0,1}, Bob = factors {2,3}
  |       +---> [O_A, O_B] = 0 (automatic)
  |
  +---> sublattice parity Z = (-1)^x on each pair -> Alice/Bob qubits
  +---> pair-hop X on each pair -> measurement angle rotation
  +---> {Z, X} = 0, Z^2 = X^2 = I -> Pauli algebra per party
  |
  +---> staggered Hamiltonian (hopping + Dirac mass)
  +---> periodic Poisson coupling (D5, self-consistent field)
  |       |
  |       +---> product initial state
  |       +---> dynamics create entanglement across Alice-Bob cut
  |       +---> CHSH = 2*sqrt(2) at t = 6.0
  |
  +---> ground state with Poisson coupling
          +---> CHSH = 2.051 at G = 20
```

## Protocol

1. **Lattice:** 4 sites, periodic BC, staggered mass m = 0.5
2. **Interaction:** periodic Poisson Green's function, G = 10
3. **Initial state:** product |Alice on site 0⟩ ⊗ |Bob on site 2⟩
4. **Evolution:** staggered Hamiltonian with Poisson coupling in the
   Alice-1-Bob-1 sector (proper tensor product factorization)
5. **Measurement:** local sublattice Pauli operators per party
6. **Result:** |S| = 2.828 at t = 6.0 (Tsirelson saturated)

## What is framework-native

| Ingredient | Origin |
|---|---|
| Local tensor product H | framework axiom (SINGLE_AXIOM_HILBERT_NOTE) |
| Alice/Bob spatial separation | disjoint factors of the tensor product |
| [O_A, O_B] = 0 | automatic from tensor product |
| Sublattice parity Z | intrinsic to Z^d bipartite structure |
| Pair-hop X | Z^d nearest-neighbor connectivity |
| Pauli algebra {Z, X} = 0 | verified on the lattice |
| Staggered Hamiltonian | Kogut-Susskind from Cl(3) |
| Periodic Poisson coupling | D5 (self-consistent propagator + field) |
| Product initial state | no entanglement inserted |

## Parameter dependence

The dynamical violation exists across a wide range:

| mass | G | Best |S| | Best time |
|---|---|---|---|
| 0.5 | 10 | 2.828 | 6.0 |
| 0.5 | 20 | 2.823 | 1.1 |
| 1.0 | 20 | 2.822 | 3.2 |
| 2.0 | 20 | 2.443 | 1.0 |
| 5.0 | 50 | 2.091 | 7.5 |

At G = 0 (no gravity), |S| reaches exactly 2.000 (the classical bound)
but does not exceed it. The Bell violation requires the gravitational
interaction — confirming that the framework's Poisson coupling is the
entanglement source.

## Honest boundaries

- The lattice is 4 sites (the minimal Bell configuration). Scaling to
  larger lattices has not been tested in this script.
- The sector restriction (Alice-1-Bob-1) excludes leaking amplitude.
  On the full unrestricted lattice, the sector weight and the effect
  of cross-boundary hopping need further study.
- The Poisson Green's function used is the 1D periodic form. The
  retained 3D surface (Z^3 Poisson/Newton) has not been tested here.
- The Tsirelson saturation at G=10 occurs at a specific evolution time
  (t=6.0). The violation oscillates with time; it is not a steady state.

## What this adds

This completes the quantum nonlocality chain with a valid Bell test:

- **Local tensor product** → proper Alice/Bob factorization
- **Commuting local algebras** → [O_A, O_B] = 0 verified
- **Framework dynamics** → product state → CHSH = 2√2
- **Gravitational interaction** → the entanglement source is Poisson coupling

Previously retained:
- Born rule I_3 = 0 (pairwise interference)
- Gravitational entanglement (BMV-like, δS > 0)

Now also retained:
- CHSH Bell violation with proper local bipartition

## Reproducibility

```
python3 scripts/frontier_bell_inequality.py
```

Runtime: < 1 second. Requires numpy, scipy.
