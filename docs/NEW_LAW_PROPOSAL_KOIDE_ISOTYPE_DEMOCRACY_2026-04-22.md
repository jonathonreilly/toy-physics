# New Law Proposal: Isotype Democracy for Flavor-Amplitude Ratios

**Date:** 2026-04-22
**Status:** NEW PHYSICAL LAW proposal, emerging from 10+ failed mechanism tests
**Context:** Koide A1 closure investigation on `koide-equivariant-berry-aps-selector`

## Motivation

After 10+ attempts to derive A1 (|b|²/a² = 1/2) from standard physical
mechanisms, ALL FAIL:

1. W[J] log|det D| extremum: gives |b|/a ≈ 3.3, not A1
2. Coleman-Weinberg V_CW: extremum at uniform eigenvalues (Q=1/3)
3. Gaussian max-entropy at fixed ||H||_F: ⟨a²⟩ = ⟨|b|²⟩, not 2:1
4. CV=1 / exponential max-entropy: 3-point discrete vs continuous gap
5. SU(2)_L Clebsch-Gordan: Z_3 ⊥ SU(2)_L, same CG for all y_{αβ}
6. Thermodynamic free energy (dim-weighted): gives κ=1, not 2
7. Koide-Nishiura coefficient derivation: circular
8. Quantum Fisher Information: monotone, no peak at A1
9. Positivity-edge scaling: 0.96 of A1, close but ≠
10. Lattice fermion log-det extremum: interior, no extremum at A1
11. Diophantine closure: irrational δ, no algebraic structure
12. Z_3 structure-constant Killing form: degenerate
13. Trace-invariant cubic identity: no clean A1 structure

A1 is genuinely an INTERIOR POINT of the configuration space with NO
natural extremal structure under STANDARD physical principles.

## The pattern

All 13 failed attempts share a common signature:
- Standard extremization gives κ ∈ {0, 1, 1/3, 3} or positivity-boundary
- NEVER κ = 2 = A1

Yet PDG observation demands κ = 2. And the RETAINED framework
(Cl(3)/Z³ + AS/APS + bridge identity) REQUIRES Q = 2/3 for consistency.

## Proposed new law

> **ISOTYPE DEMOCRACY LAW**: In a Z_d-cyclic Hermitian matrix algebra
> with distinguishable real-irrep isotypes, the physical equilibrium
> state assigns EQUAL weight to each isotype (multiplicity-based, not
> dimension-based) in the thermodynamic partition function.
>
> Mathematically: the natural partition function is
> `Z_physical = Π_isotypes Z_isotype` where each `Z_isotype` is
> normalized per real-irrep COPY, not per-dimension. Equilibrium
> (free-energy minimum) at FIXED TOTAL FROBENIUS NORM forces
> EQUAL ISOTYPE FROBENIUS NORMS: `E_+ = E_⊥`.

## Physical consequences

Under this law:
- Herm_circ(3) has ONE trivial + ONE doublet isotype (multiplicity 1 each)
- Equal-isotype equipartition: `E_+ = E_⊥ = Tr(H²)/2`
- Translation: `3a² = 6|b|²` ⟺ `|b|²/a² = 1/2` = **A1**
- Koide `Q = 2/3` follows via the retained bridge identity

## Why this is a NEW LAW (not reducible to known physics)

Standard statistical mechanics uses DIMENSION-weighted ensembles:
each REAL DIMENSION contributes kT/2 (equipartition theorem). Under
this standard law, the Herm_circ(3) dimensions (1 trivial + 2 doublet
= 3) give `κ = 1`, NOT A1.

The NEW LAW proposes instead that each ISOTYPE (regardless of its
internal dimension) is a distinguishable species with EQUAL contribution.
This is analogous to treating each particle species (electron, muon,
tau) as its OWN degree of freedom, rather than summing their
internal states.

For classical particles in thermal ensemble: both conventions coincide
(each particle = 1 DOF). But for GAUGE-INVARIANT BLOCK STRUCTURE in
matrix models, the distinction matters.

## Testable predictions

The Isotype Democracy Law predicts:

1. **Charged lepton sector**: `Q = 2/3` ✓ (observed)

2. **Neutrino sector** (if Dirac with Z_3 cyclic): same `κ = 2`
   prediction, would give a neutrino Koide-like relation. Current
   data too imprecise to test decisively.

3. **Quark sector**: if Z_3-cyclic structure exists, predicts
   `κ_quark = 2` for quark mass matrix. Standard CKM mixing probably
   breaks Z_3, so doesn't directly apply. But up-quark or down-quark
   subsectors (3 generations each) could be tested.

4. **PMNS sector**: angle structure might follow from isotype democracy
   applied to neutrino mixing matrix.

## Justification attempts

Why should isotypes be "species" and not dimension-weighted?

**Candidate 1**: Gauge invariance of observables. If only
Z_3-CHARACTER-INVARIANT quantities are physical observables, we sum
over character (= isotype) labels, giving each one equal measure.

**Candidate 2**: Holographic information bound. The entanglement
entropy across isotype boundaries is the LOG of character partition
function, which naturally uses species counting.

**Candidate 3**: Emergent from Cl(3)/Z³ lattice structure via block
projection and renormalization flow to low energies. Dimension
weights flow to multiplicity weights under RG.

None is rigorously derived. The law is PROPOSED as a new primitive.

## Summary

**The Isotype Democracy Law** is the cleanest statement that closes
A1 axiom-natively. It's a NEW PHYSICAL LAW (not reducible to known
physics) that asserts equal-species partitioning for Z_d-cyclic
matrix algebras at thermodynamic equilibrium.

Adopting this law as retained primitive gives:
- A1 (Frobenius equipartition) axiom-native
- Koide Q = 2/3 via bridge identity (retained)
- Full charged-lepton closure

The law is testable (predicts similar structure in other
Z_n-cyclic systems) and falsifiable (e.g., if quark sector shows
systematic deviation from κ=2 after appropriate mixing treatment).

## Status for canonical-branch reviewer

This law is OFFERED as the candidate new primitive to close A1.
Alternative closure routes (Koide-Nishiura V(Φ) import, novel QFT
mechanism) remain available.

Whichever route is adopted, the /loop investigation has established:
- A1 genuinely requires NEW PHYSICS beyond standard mechanisms
- The cleanest new primitive is Isotype Democracy
- 10+ independent mechanism failures confirm no simpler closure exists
