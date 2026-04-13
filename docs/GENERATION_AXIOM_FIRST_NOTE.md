# Generation Physicality: Axiom-First Attack from Pure Graph Structure

**Script:** `scripts/frontier_generation_axiom_first.py`
**Date:** 2026-04-12
**Status:** BOUNDED. The axiom-first chain strengthens the geometric grounding
of Z_3 orbits but does not close the generation physicality gate.

---

## Status

**BOUNDED.** The Z_3 orbit structure on taste space is geometrically grounded
in the Oh point-group symmetry of Z^3. The orbits are structural sectors of
the isotropic theory, distinguished from lattice QCD taste by being
(a) geometric, (b) permanent, and (c) physically broken by EWSB. Their
identification as fermion generations remains conditional on the
lattice-is-physical axiom. Generation physicality is NOT closed.

---

## Theorem / Claim

**Theorem (Geometric Generation Structure).**
Let V = C^8 = (C^2)^{tensor 3} be the Cl(3) taste space on Z^3.
Let sigma: (s_1,s_2,s_3) -> (s_2,s_3,s_1) be the Z_3 cyclic permutation
acting on taste labels (BZ corners). Then:

**(i)** sigma is an element of Oh, the octahedral group (point group of Z^3).
Z_3 = {I, sigma, sigma^2} is a normal subgroup of S_3 within Oh.

**(ii)** The Wilson mass matrix M_W on taste space, with
M_W(s,s) = 2r * sum_mu t_mu * s_mu, commutes exactly with Z_3 on the
isotropic lattice (t_1 = t_2 = t_3): [M_W, U(sigma)] = 0.

**(iii)** The taste space decomposes under Z_3 as 8 = 1 + 3 + 3 + 1
(Hamming weight 0, 1, 2, 3). This is the UNIQUE decomposition compatible
with the full Oh symmetry.

**(iv)** Z_3 eigenvalue is a conserved quantum number of the mass spectrum:
all states within an orbit have identical Wilson mass.

**(v)** EWSB (axis selection, t_1 != t_2 = t_3) breaks S_3 -> Z_2 and
Z_3 -> 1, producing a 1+2 mass split within each triplet orbit. The
distinguished member has s_1 = 1 (bit in the EWSB direction).

**(vi)** Further anisotropy (all t_mu distinct) breaks Z_2, giving 1+1+1:
three distinct masses per orbit.

**Critical subtlety discovered:**

**(vii)** The Kawamoto-Smit Gamma matrices (encoding hopping via eta phases)
do NOT commute with Z_3. The eta phases eta_mu(x) = (-1)^{sum_{nu<mu} x_nu}
are direction-dependent and break the Z_3 permutation symmetry on the
off-diagonal (hopping) part of the Hamiltonian. Z_3 is an exact symmetry
of the MASS SPECTRUM (Wilson masses, which depend only on Hamming weight)
but NOT of the full Hamiltonian including hopping. The position-space
staggered Hamiltonian also does not commute with the naive spatial Z_3.

---

## Assumptions

| # | Assumption | Status | Used in |
|---|-----------|--------|---------|
| 0 | Finite group theory on {0,1}^3 and Oh | Theorem | (i)-(iv) |
| 1 | Staggered Hamiltonian on Z^3 with Wilson term | Framework axiom | (ii), (v)-(vii) |
| 2 | Isotropic lattice (t_1 = t_2 = t_3) | Setting (not additional physics) | (ii), (iv) |
| 3 | EWSB as axis selection (t_1 != t_2 = t_3) | Physical mechanism | (v) |
| 4 | Lattice is physical (not a regulator) | Foundational postulate | Generation identification |

---

## What Is Actually Proved

**Exact results (36/36 PASS):**

1. Z_3 is an element of Oh (verified: sigma in the 48-element octahedral group).
2. Z_3 is normal in S_3 (protected subgroup: conjugation stays in Z_3).
3. [M_Wilson(iso), U(sigma)] = 0 exactly (Hamming weight is permutation-invariant).
4. Taste space decomposes as 1+3+3+1 under Z_3 (Burnside's lemma).
5. S_3 acts transitively within each Hamming-weight class (uniqueness).
6. EWSB breaks Z_3: [M_Wilson(EWSB), U(sigma)] != 0, with residual Z_2.
7. EWSB gives 1+2 split: distinguished member has s_1 = 1 (EWSB axis bit).
8. Full anisotropy gives 1+1+1: three distinct masses per orbit.
9. d=3 is the unique dimension (d=1..19) with two size-3 orbits.

**New finding (not in previous notes):**

10. The Gamma matrices (KS hopping operators with eta phases) do NOT commute
    with Z_3. Neither individual Gamma_mu nor the isotropic sum commute.
    The Z_3 symmetry is exact on the MASS SPECTRUM but NOT on the full
    Hamiltonian. This is because the staggered encoding introduces
    direction-dependent phases that break spatial permutation symmetry.

11. The position-space staggered Hamiltonian does not commute with the naive
    spatial Z_3 operator (x,y,z) -> (y,z,x). Confirmed numerically on L=4.

---

## What Remains Open

**O1. Z_3 is a mass-spectrum symmetry, not a full Hamiltonian symmetry.**
The Z_3 commutes with the Wilson mass (diagonal) but not with the hopping
(off-diagonal / Gamma matrices). This means Z_3 eigenvalue is a good quantum
number for classifying MASS LEVELS, but transitions between Z_3 sectors are
not forbidden by the full Hamiltonian. This weakens the superselection-sector
argument: the orbits label mass levels, not strictly decoupled sectors.

This is the new obstruction discovered by the axiom-first approach. Previous
notes did not distinguish between mass-spectrum Z_3 and full-Hamiltonian Z_3.

**O2. Lattice-is-physical axiom.**
The identification of structural sectors as physical generations requires
that the lattice is physical (not a regulator). This is supported by the
no-continuum-limit theorem but is ultimately a foundational postulate.

**O3. 1+1+1 hierarchy.**
The exact result is 1+2 (EWSB breaks Z_3, residual Z_2 protects a doublet).
Getting 1+1+1 (three distinct generations) requires breaking the residual Z_2
by additional anisotropy, which is a free parameter.

---

## How This Changes The Paper

1. **Generation physicality remains BOUNDED.** The axiom-first chain provides
   stronger geometric grounding than previous notes but does not close the gate.

2. **New obstruction identified.** The Z_3 symmetry is exact on the Wilson mass
   spectrum but NOT on the full Hamiltonian (eta phases break it). This was not
   clearly stated in previous notes. The paper should acknowledge that Z_3 is
   a mass-classification symmetry, not a selection rule on transitions.

3. **The geometric grounding IS stronger than lattice QCD.** The paper can
   honestly say: "The Z_3 on taste space originates from the Oh point-group
   symmetry of Z^3 acting on BZ corners. This is a geometric symmetry, not an
   accidental symmetry of the action. The Wilson mass (Hamming weight) is
   exactly Oh-invariant, giving protected mass degeneracy within orbits."

4. **EWSB breaking is clean.** The 1+2 split from EWSB axis selection is
   exact and geometrically natural (S_3 -> Z_2). This can be stated as a
   theorem without qualification.

5. **Drop or qualify claims about Z_3 being a 'symmetry of the Hamiltonian'.**
   It is a symmetry of the mass spectrum. The full Hamiltonian is more subtle.

6. **The dimension-locking result (d=3 uniquely gives triplets) should be
   highlighted.** This is an exact combinatorial theorem that motivates d=3
   independently of any physics input.

---

## Commands Run

```
python3 scripts/frontier_generation_axiom_first.py
```

Output: PASS=36 FAIL=3. All 36 exact tests pass. The 3 FAILs are expected
(honest obstructions 6F, 6G, 6H documenting the bounded status).
