# Bell Inequality: Native Pauli Algebra and CHSH on Z^d

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED — structural theorem exact; dynamical route exploratory
**Script:** `scripts/frontier_bell_inequality.py`
**Runtime:** < 1 second

## Result

The staggered lattice Z^d carries a native Pauli algebra. Any singlet
state on that algebra saturates the CHSH Tsirelson bound:

| Test | |S| | Bound | Status |
|---|---|---|---|
| Singlet on sublattice Pauli algebra | 2.8284271247 | 2.0 (classical) | VIOLATION |
| Same | 2.8284271247 | 2.8284271247 (Tsirelson) | SATURATED |

The correlator E(0, theta) = -cos(theta) matches the exact singlet
prediction to < 3 x 10^-16 across all tested angles.

The Pauli algebra is confirmed on lattice sizes N = 6, 10, 20, 50, 100
— it is a structural property of Z^d, not a finite-size artifact.

## What is framework-native

### The sublattice Pauli algebra

On any adjacent even-odd pair of sites in Z^d:

| Operator | Origin | Definition |
|---|---|---|
| Z (sigma_z) | sublattice parity | (-1)^{x_1+...+x_d}, intrinsic to Z^d |
| X (sigma_x) | nearest-neighbor hop | lattice hopping operator restricted to the pair |

These satisfy all Pauli algebra requirements:

| Property | Value | Required |
|---|---|---|
| Z^2 = I | True | yes |
| X^2 = I | True | yes |
| {Z, X} = 0 | True | yes |
| Z eigenvalues | {+1, -1} | yes |
| X eigenvalues | {+1, -1} | yes |

**No external spin or polarization degree of freedom is imported.** The
Pauli algebra emerges from the lattice geometry alone.

### The derivation chain

```
Cl(3) on Z^3 (framework axiom)
  |
  +---> Z^d has bipartite (even/odd) structure
  |       |
  |       +---> sublattice parity Z = sigma_z (intrinsic)
  |       +---> nearest-neighbor hop X = sigma_x (intrinsic)
  |       +---> {Z, X} = 0, Z^2 = X^2 = I (verified)
  |       +---> Pauli algebra on every adjacent pair
  |
  +---> unitarity (A2) -> Hilbert space
  |       |
  |       +---> tensor product for two particles
  |       +---> antisymmetric (singlet) state exists
  |
  +---> Pauli algebra + singlet -> CHSH = 2*sqrt(2) (theorem)
```

## What is NOT proven dynamically

**Part B of the script tested whether the lattice Hamiltonian dynamically
produces Bell-violating states from product initial conditions. It does
not** — at least not in the specific qubit subspace tested:

| Route | Max |S| in subspace | Entanglement produced? | CHSH > 2? |
|---|---|---|---|
| Fermionic (antisymmetric) | 1.72 | Yes (S = ln(2)) | No |
| Contact interaction (U=4) | 1.92 | Yes (S up to 1.03) | No |

Both routes generate entanglement (the full-Hilbert-space entropy grows),
but the entanglement does not concentrate in the specific 2x2 qubit
subspace used for CHSH measurement. The qubit-subspace fraction drops
below 1% by t = 2.

This is an honest negative: the lattice dynamics spread amplitude across
the full Hilbert space, and the projected CHSH in the initial qubit
subspace does not exceed the classical bound. A more sophisticated
measurement protocol (optimized over all possible local observables, or
using a different entangled subspace) might recover violation, but that
is future work.

## Claim boundary

**Retained structural claim:**

> The staggered lattice Z^d carries a native Pauli algebra on every
> adjacent even-odd site pair: sublattice parity = sigma_z, nearest-
> neighbor hop = sigma_x. These satisfy Z^2 = X^2 = I and {Z, X} = 0
> at every lattice size. Any singlet state on this algebra produces
> maximal CHSH violation (|S| = 2*sqrt(2), Tsirelson bound saturated).

**Honest boundary:**

- The structural theorem shows the lattice CAN carry Bell-violating
  states with intrinsic operators. It does not show the dynamics
  PRODUCE such states from generic initial conditions.
- The singlet in Part A is the natural antisymmetric state of two
  particles on adjacent sites. It is not dynamically produced in the
  script.
- The dynamical test (Part B) is exploratory and currently negative
  in the tested qubit subspace.

**What this adds to the framework:**

1. Identifies the staggered sublattice structure as carrying spin-1/2
   physics (Pauli algebra) natively — connecting lattice geometry to
   quantum information theory.
2. Shows the framework's Hilbert space is "maximally quantum" — the
   Tsirelson bound is saturated, not just exceeded. This rules out
   any sub-quantum or super-quantum modification.
3. Completes the chain: axioms -> complex amplitudes -> entanglement ->
   Bell violation -> quantum nonlocality, all on intrinsic operators.

## Impact assessment

**For the paper:** This is a clean bounded-retained companion result.
It adds structural depth (the lattice carries spin-1/2 natively) but
is not a new headline prediction or a new closure gate.

**For the program:** Moderate. It fills a gap (Bell violation was never
explicitly shown) and connects the staggered structure to quantum
information. But the Born rule (I_3 = 0) already established the
framework as quantum — this is a more detailed structural confirmation,
not a qualitative breakthrough.

**Honest comparison to other retained results:** This is at the same
level as the I_3 = 0 Born rule theorem — a structural consequence of
unitarity on a lattice. It does not rise to the level of the gravity
derivation, gauge sector closure, or generation structure.

## Reproducibility

```
python3 scripts/frontier_bell_inequality.py
```

Runtime: < 1 second. Requires numpy and scipy.
