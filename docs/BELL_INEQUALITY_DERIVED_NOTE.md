# Bell Inequality Violation from the Local Tensor Product Axiom

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED — CHSH violation with proper local bipartition
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** < 1 second

## Result

Starting from a product state on a 4-site staggered lattice, the
framework's Poisson gravitational coupling dynamically produces CHSH
Bell violation with proper local bipartition:

| Route | |S| | Classical bound | Tsirelson (2.828) | Parameters |
|---|---|---|---|---|
| Dynamical (product -> evolve) | **2.828** | 2.0 | 99.99% | m=0.5, G=10, t=6.0 |
| Ground state | **2.051** | 2.0 | 6.2% | m=0.5, G=20 |
| G=0 null control | **2.000** | 2.0 | 0% (no violation) | any m |

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
  |       +---> Poisson coupling is the ONLY Alice-Bob link
  |       |     (cross-boundary hopping excluded in sector)
  |       +---> dynamics create entanglement across Alice-Bob cut
  |       +---> CHSH -> 2*sqrt(2) at t = 6.0
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
6. **Result:** |S| = 2.828 at t = 6.0 (99.99% of Tsirelson bound)

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

- **Minimal lattice:** 4 sites (the minimal Bell configuration). Scaling
  to larger lattices has not been tested.
- **Sector restriction:** the Alice-1-Bob-1 sector excludes cross-boundary
  hopping (site 1↔2, site 3↔0). This is physically analogous to a Bell
  test where particles stay in their respective labs. The Poisson
  interaction is the ONLY Alice-Bob coupling in this sector.
- **1D periodic, not Z^3:** the Poisson Green's function is the 1D
  periodic form (D5 applied to Z^1). The retained publication surface
  uses Z^3 with 1/r Poisson/Newton. The 1D result is framework-native
  (D5 holds on any graph) but not on the publication surface.
- **Effective Ising model:** in the sector, the Poisson coupling reduces
  to an Ising interaction J*σ_z^A ⊗ σ_z^B with J = -G/16. The dynamics
  are those of the transverse-field Ising model, which is well-known to
  produce entanglement. The framework contribution is deriving J from the
  Poisson Green's function.
- **Time-dependent:** the dynamical violation oscillates; it is not a
  steady state. The near-Tsirelson value at t=6.0 is a peak, not an
  equilibrium.
- **The ground-state violation is modest** (|S| = 2.051, 6% of Tsirelson)
  and occurs only at moderate-to-strong coupling (G ≥ 5).

## What this adds

Demonstrates CHSH Bell violation with a valid local bipartition on
a minimal lattice, using framework-native ingredients:

- **Local tensor product** → proper Alice/Bob factorization
- **Commuting local algebras** → [O_A, O_B] = 0 verified
- **Framework dynamics** → product state → CHSH near 2√2
- **Gravitational interaction** → Poisson coupling is the sole
  entanglement source (G=0 gives exactly |S|=2, no violation)

Previously retained:
- Born rule I_3 = 0 (pairwise interference)
- Gravitational entanglement (BMV-like, δS > 0)

This result adds:
- Explicit CHSH Bell violation with proper local bipartition
- Identification of Poisson coupling as the Bell-violation mechanism
- G=0 → |S|=2.000 null control confirming gravity is required

## Reproducibility

```
python3 scripts/frontier_bell_inequality.py
```

Runtime: < 1 second. Requires numpy, scipy.
