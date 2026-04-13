# Generation Entanglement: SLOCC Classification of the Cl(3) Taste Space

**Date:** 2026-04-12
**Lane:** generation physicality
**Script:** `scripts/frontier_generation_entanglement.py`

## Status

**BOUNDED** -- The entanglement perspective provides a physically motivated
identification of the generation subspace but does not independently close
the generation physicality gate.

## Theorem / Claim

**Exact claim (paper-safe):**

> The hw=1 taste orbit is the unique 3-dimensional subspace of the Cl(3) =
> (C^2)^{otimes 3} taste space whose generic states are W-class entangled
> (zero 3-tangle, nonzero pairwise concurrence). This provides a physical
> interpretation of the generation subspace as the pairwise-entangled sector
> of a 3-qubit system.

**Not claimed:**

- "3 generations = 3 W-class states" (individual basis states are separable)
- "SLOCC classification gives 3 generations" (it gives 1 W class, not 3)
- "Entanglement closes the generation physicality gate"
- "SLOCC classes are preserved by taste dynamics"

## Assumptions

The analysis requires only:

1. Cl(3) = (C^2)^{otimes 3} (the standard Kawamoto-Smit identification)
2. The SLOCC classification of 3-qubit entanglement (Dur-Vidal-Cirac 2000)
3. The Coffman-Kundu-Wootters 3-tangle as SLOCC invariant

No dynamics, no lattice size dependence, no fitted parameters.

## What Is Actually Proved

### Level A: Exact algebraic facts (theorem-grade)

1. All 8 computational basis states |s1,s2,s3> are **separable** (product states).
   They are NOT in any nontrivial SLOCC entanglement class.

2. The Hamming weight decomposition 8 = 1+3+3+1 coincides exactly with the
   qubit permutation group S_3 orbits on {0,1}^3.

3. The standard W state W = (|100> + |010> + |001>)/sqrt(3) is the equal
   superposition of the hw=1 orbit members.

4. The 3-tangle (Cayley hyperdeterminant) discriminates:
   - tau(W) = 0 exactly (W-class signature)
   - tau(GHZ) = 1 exactly (GHZ-class signature)

5. Pairwise concurrences:
   - W: C_{ij} = 2/3 for all pairs (pairwise entanglement)
   - GHZ: C_{ij} = 0 for all pairs (purely tripartite entanglement)

6. The W-bar state (|011> + |101> + |110>)/sqrt(3) from hw=2 is also
   W-class with tau = 0.

### Level B: Structural connections (bounded)

1. **Every generic state in the hw=1 subspace is W-class**: 50/50 random
   states in span{|100>, |010>, |001>} have 3-tangle = 0 and are not
   separable. Same for the hw=2 subspace.

2. The hw=1 subspace carries the 3-dim **permutation representation** of S_3,
   which decomposes as trivial(1) + standard(2). This is the 1+2 split.

3. Z_3 eigenstates in the hw=1 sector (with Z_3 charges q=0,1,2) are all
   W-class with definite cyclic eigenvalue omega^{-q}.

4. **SLOCC classes are NOT preserved** by the Cl(3) taste Hamiltonian:
   the Gamma matrices mix Hamming weight sectors, so time evolution can
   take a W-class state to a GHZ-class state.

### Level C: Obstructions

1. **Basis states are separable, not W-class.** The states |100>, |010>,
   |001> are product states. Calling them "W-class states" is incorrect.
   The W class is a property of their superposition.

2. **SLOCC gives 1 class, not 3.** The W entanglement class is a single
   equivalence class. To extract "3 generations" one must additionally
   decompose it by Z_3 charge or S_3 representation labels.

3. **Entanglement identifies the subspace but does not split it.**
   The hw=1 subspace is the natural home of W-class entanglement.
   But dim(subspace) = 3 does not equal "3 distinct physical objects"
   without a splitting mechanism.

4. **Dynamics do not preserve SLOCC classes.** The taste Hamiltonian
   can evolve W-class states into GHZ-class states, so SLOCC class
   is not a conserved quantum number.

## What Remains Open

1. Whether any physical mechanism (EWSB, anomaly, dynamics) selects the
   hw=1 W-class subspace as the physically relevant generation sector.

2. Whether the Z_3 eigenvalue decomposition within the W-class subspace
   has a dynamical or anomaly-based justification beyond the kinematic
   permutation symmetry.

3. Whether SLOCC non-preservation by the Hamiltonian is an obstruction
   or irrelevant (if the generation structure is set at the kinematic
   level before dynamics).

## How This Changes The Paper

This note provides supplementary physical interpretation, not a new closure:

- The paper can cite the W-class characterization as motivation for why
  the hw=1 subspace is physically distinguished (pairwise entanglement
  vs tripartite entanglement).
- This does NOT upgrade the generation physicality lane from "open" or
  "bounded" to "closed."
- The honest contribution: a well-studied quantum information framework
  (Dur-Vidal-Cirac SLOCC classification) naturally singles out the same
  3-dimensional subspace that the Z_3 orbits produce.

## Commands Run

```
python3 scripts/frontier_generation_entanglement.py
# Exit code: 0
# PASS=35 FAIL=0
```
