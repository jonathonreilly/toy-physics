# Generation Physicality: Theorem Note

## Status

**Conditional theorem, not closure.** The Z_3 orbit algebra is exact (Level A).
The physical identification of orbits as fermion generations is conditional on
the taste-physicality assumption (Level B). Six obstructions remain open
(Level C). This gate is not closed.

---

## Theorem / Claim

**Conditional Theorem.** Let L = Z^3 be the d=3 cubic lattice with staggered
fermions, and let sigma: (s1,s2,s3) -> (s2,s3,s1) be the Z_3 cyclic
permutation acting on the 2^3 = 8 taste states s in {0,1}^3.

**(A) Exact algebra (no assumptions):**

1. The 8 taste states decompose under Z_3 as 8 = 1 + 3 + 3 + 1, with orbits
   partitioned by Hamming weight |s| = 0, 1, 2, 3. Verified by enumeration
   and Burnside's lemma: (8+2+2)/3 = 4 orbits.

2. The orbit sizes are the binomial coefficients C(3,k) = 1, 3, 3, 1. This is
   dimension-locked: d=3 is the unique dimension giving two size-3 orbits.

3. Each triplet orbit carries the regular representation of Z_3, with
   eigenvalues 1, omega, omega^2 where omega = exp(2*pi*i/3).

4. The permutation representation 3_perm decomposes under S_3 as 1 + 2
   (trivial singlet + standard doublet). The triplet is S_3-reducible.

5. The staggered phase rule eta_mu = (-1)^{sum_{nu<mu} x_nu} is invariant
   under relabeling of axes. The breaking S_3 -> Z_3 requires additional
   physics (anisotropy or EWSB), not the staggered construction alone.

**(B) Conditional on taste-physicality (a = l_Planck physical, no continuum limit):**

IF the lattice spacing is a physical minimum length, THEN:

6. The Wilson mass m_W(s) = 2r|s|/a gives 4 distinct mass levels by Hamming
   weight, producing physical inter-orbit mass splitting.

7. Anisotropy t_x != t_y != t_z breaks Z_3, splitting intra-orbit degeneracy.

8. The Z_3 CP phase delta = 2*pi/3 gives a Jarlskog invariant
   J(Z_3) = 7.6 x 10^{-5}, a factor 2.5 from J(PDG) = 3.1 x 10^{-5}.
   (Mixing angles taken from PDG; only the CP phase is predicted.)

9. Anisotropy forces inter-generation mixing when up-type and down-type
   sectors have different anisotropy parameters.

---

## Assumptions

The result rests on a hierarchy of assumptions, each explicitly named:

| # | Assumption | Status | Used in |
|---|-----------|--------|---------|
| 0 | Finite group theory on {0,1}^3 | Theorem (no assumption) | A1-A5 |
| 1 | **Taste-physicality**: a = l_Planck is physical, no continuum limit | Axiom (not derivable) | B1-B6, all physical claims |
| 2 | Wilson term with r ~ O(1) | Model input (not derived) | B1, mass splitting |
| 3 | Anisotropy t_x != t_y != t_z | Model input (origin unspecified) | B2, B5, mass hierarchy |
| 4 | Different aniso for up/down sectors | Model input (requires Yukawa sector) | B5, CKM |
| 5 | Froggatt-Nielsen epsilon = 1/3 | Fitted parameter | CKM magnitudes |
| 6 | Higgs charge delta = (1,1,0) | Fitted parameter | Down-sector masses |

Assumptions 0-1 are the foundation. Assumptions 2-6 are additional model
inputs needed for quantitative predictions.

---

## What Is Actually Proved

**Proved unconditionally (Level A, 6/6 tests pass):**

- The orbit decomposition 8 = 1+3+3+1 is a theorem of finite group theory.
- Hamming weight is orbit-constant (permutation-invariant sum).
- d=3 uniquely gives triplet orbits among small dimensions.
- Z_3 eigenvalues on triplets are 1, omega, omega^2.
- The triplet is S_3-reducible (1+2). Three distinct generations require Z_3,
  not S_3, as the operative symmetry.
- The Z_3 orbit structure is a labeling fact about BZ corners. It is not a
  dynamical symmetry of the position-space Hamiltonian.

**Proved conditionally (Level B, 6/6 tests pass, given taste-physicality):**

- Inter-orbit mass splitting from Wilson term.
- Intra-orbit splitting from anisotropy.
- Distinct O(a^2) gauge corrections by orbit.
- CP phase delta = 2*pi/3 forced by Z_3 representation theory.
- Inter-generation mixing forced by Z_3 breaking (but CKM magnitudes need
  free parameters).
- Finite-lattice spectrum consistent with 1+3+3+1 structure.

---

## What Remains Open

Six obstructions identified (Level C, all marked FAIL as expected):

**C1. Taste-physicality is not derivable.** The entire physical interpretation
rests on the claim that a = l_Planck is physical and there is no continuum
limit. This is an axiom of the framework, not a theorem. A referee who
maintains that the lattice is a regulator (not fundamental) will reject the
generation identification, and the framework has no internal argument to
refute this. This is the **central obstruction**.

**C2. Mass hierarchy is not predicted.** The Wilson mass gives a linear
hierarchy 0:1:2:3 in Hamming weight. The SM hierarchy is geometric
(~1:200:3500 for leptons). The mismatch is a factor ~7 in log space. To
recover the observed hierarchy, one needs anisotropy parameters, radiative
corrections, or Froggatt-Nielsen fits -- all free inputs.

**C3. Singlet identification is ambiguous.** The two Z_3 singlets (0,0,0) and
(1,1,1) have no generation quantum number. Their identification as sterile
neutrino and Planck-mass state is physically motivated but not derived. The
framework does not dynamically select among alternatives.

**C4. Quark/lepton distinction is not derived.** The two triplet orbits T1
(|s|=1) and T2 (|s|=2) are gauge-connected: the Clifford algebra Gamma
matrices mix them (Gamma_1 and Gamma_3 connect T1 to T2). They are not
independent gauge sectors. The assignment of T1 to quarks and T2 to leptons
(or vice versa) is an interpretation, not a consequence of the algebra.

**C5. CKM magnitudes require free parameters.** Only the CP phase
(delta = 2*pi/3) and the existence of mixing are parameter-free predictions.
The Cabibbo angle, individual CKM elements, and mass ratios all require
additional inputs (epsilon, anisotropy, Higgs charges).

**C6. No dynamical generation distinction.** In the free staggered theory, the
only observable differences between orbits are mass and O(a^2) gauge
corrections -- both contingent on taste-physicality. There is no dynamical
mechanism (beyond kinematics) that makes different generations scatter
differently. Non-trivial flavor physics requires interactions beyond the free
Hamiltonian.

---

## How This Changes The Paper

1. **Gate 2 remains bounded, not closed.** The gate status should be updated
   from "bounded -- exact algebra retained, physical interpretation
   conditional" to "bounded -- conditional theorem established, central
   obstruction identified." The obstruction (taste-physicality is an axiom)
   is structural and cannot be removed by computation.

2. **The paper should state the conditional theorem explicitly.** The result
   "taste-physicality => 3-generation structure with CP violation" is clean
   and rigorous. It should be presented as a conditional implication, not as
   a derivation of generations from first principles.

3. **The paper should not claim mass hierarchy prediction.** The Wilson
   hierarchy (linear 0:1:2:3) does not match the SM (geometric). Any
   realistic hierarchy requires free parameters. This should be stated
   honestly as an open problem.

4. **The CP phase delta = 2*pi/3 is the strongest parameter-free prediction.**
   This gives J(Z_3)/J(PDG) = 2.48 -- within a factor of 3. This is the one
   quantitative prediction that does not require fitted inputs and should be
   highlighted as such.

5. **The quark/lepton distinction needs new physics.** The Gamma matrices mix
   T1 and T2. Identifying them as separate sectors (quarks vs leptons) requires
   a mechanism beyond the free Clifford algebra. This is an honest gap that
   should be flagged as a direction for future work.

6. **Drop the Wilson-entanglement argument.** (Already withdrawn in prior
   Gate 2 note.) The Wilson deformation test proves fragility, not physicality.

---

## Commands Run

```
python3 scripts/frontier_generation_physicality.py
```

Output: PASS=13 FAIL=6. All Level A (6) and Level B (7) tests pass.
All Level C tests that are expected to fail (6) do fail, documenting the
obstructions. One Level C test (C7, conditional theorem validity) passes.
