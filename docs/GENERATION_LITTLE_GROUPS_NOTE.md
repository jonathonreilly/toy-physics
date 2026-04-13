# Generation Little Groups: Obstruction Note

**Date:** 2026-04-12
**Lane:** Generation physicality
**Script:** `scripts/frontier_generation_little_groups.py`

## Status

**OPEN** -- the little-group argument does not close generation physicality.

## Theorem / Claim

**Attempted claim (REFUTED):** The staggered KS eta phases break Oh to D2h,
placing the three X-point BZ corners (hw=1) in different orbits, making them
physically inequivalent by standard crystallography.

**Actual result:** The staggered Hamiltonian has the FULL Oh symmetry,
realized through combined coordinate permutations and taste-space unitaries.
The three X points are in the SAME orbit.  The little-group argument fails.

## Assumptions

None beyond the standard staggered Cl(3) Hamiltonian on Z^3:
- Hopping phases: eta_1 = 1, eta_2 = (-1)^{n_1}, eta_3 = (-1)^{n_1+n_2}
- Anti-Hermitian nearest-neighbor hopping with PBC

## What Is Actually Proved

The following are exact algebraic facts, verified numerically on L=4 and L=6
lattices with all 13 checks passing:

1. **Diagonal-gauge symmetry group = D2h (8 elements).**
   The Oh elements that preserve eta phases under diagonal (site-dependent
   phase) gauge transformations form D2h = {I, C2x, C2y, C2z, i, sigma_x,
   sigma_y, sigma_z}.  No axis permutation or C4 rotation survives in this
   subgroup.

2. **Full symmetry group = Oh (48 elements).**
   Every Oh element can be implemented as a symmetry through a combined
   operation S_g = (coordinate permutation) x (taste-space unitary U_g),
   where U_g is an off-diagonal unitary on the 8-dim internal space.
   Verified by Tr(H^k) = Tr((P_g H P_g^T)^k) for all even k up to 20,
   for all 48 Oh elements.

3. **Explicit C3 construction.**
   The symmetry S = P_{C3}^T @ U (where U is found via Schur decomposition)
   satisfies ||S H S^dag - H|| < 5e-14 and ||SS^dag - I|| < 4e-14.

4. **q=0 sector preservation.**
   S maps the q=0 sector (which contains all 8 BZ corners) to itself.
   Verified by checking Tr(S P_{q0} S^dag P_{q0}) = dim(q=0) = 8.

5. **Orbit structure.**
   Under the full Oh symmetry with taste unitaries, the 8 BZ corners form
   4 orbits: {Gamma}, {X1,X2,X3}, {M1,M2,M3}, {R}.
   The three hw=1 corners are in the SAME orbit.

## What Remains Open

Generation physicality.  The little-group/orbit argument cannot distinguish
the three hw=1 species because they are related by the full Oh symmetry
acting on coordinate + taste space.  Any argument for generation physicality
must break or circumvent this symmetry.

Possible routes still open:
- EWSB breaking of the taste symmetry (the CW selector breaking S_3 to Z_2)
- Wilson-like terms that explicitly break the taste symmetry
- Anomaly-based arguments that distinguish the species dynamically
- Interaction effects that break the free-field taste symmetry

## How This Changes The Paper

This result does NOT close the generation physicality gate.  It documents
a sharp obstruction: the free staggered Hamiltonian has too much symmetry
(full Oh on coordinate + taste) to distinguish the three hw=1 species by
crystallographic methods alone.

Paper-safe wording remains:
> exact 1+2 split; bounded 1+1+1 hierarchy model; generation physicality
> still open

The note supersedes any earlier claim that eta phases break Oh to D2h in
a way that distinguishes the X points.  The D2h result is correct for
diagonal-gauge transformations but misses the off-diagonal taste unitaries
that restore full Oh.

## Commands Run

```
python3 scripts/frontier_generation_little_groups.py
```

Exit code: 0
Result: PASS=13 FAIL=0
