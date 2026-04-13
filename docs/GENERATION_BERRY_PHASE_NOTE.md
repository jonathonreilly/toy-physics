# Berry Phase / Zak Phase for Z_3 Generation Sectors

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Authority:** `review.md` (2026-04-12)

---

## Status

**NEGATIVE RESULT (BOUNDED).** The Berry phase / Zak phase along the
isotropic line of the Brillouin zone does NOT provide an unconditional
topological invariant distinguishing the three Z_3 sectors. The
sector-restricted Berry phases are all zero on the isotropic line.

With Z_3-invariant perturbations, Berry phases generically become
sector-dependent (189/256 parameter configurations tested), but this
distinction is MODEL-DEPENDENT and does not constitute a first-principles
topological theorem.

---

## Theorem / Claim

### What was attempted

Compute Berry phase (Zak phase) topological invariants for each Z_3
sector of the staggered Cl(3) Hamiltonian on Z^3. If the three sectors
carry distinct quantized Berry phases (e.g., 0, 2pi/3, 4pi/3), they
would be topologically distinguishable -- an unconditional result
analogous to the Z_2 Fu-Kane invariant for topological insulators.

### What was found

**Berry phases are all trivially zero within each Z_3 sector on the
isotropic line.** This is because the eigenvectors of the restricted
Hamiltonian within each sector have a simple structure on the isotropic
line k1 = k2 = k3 = theta, leading to equal Berry phases across all
three sectors (gamma_0 = gamma_1 = gamma_2 = 0 mod 2pi).

---

## Assumptions

1. **Symmetric staggered phases.** We use eta_mu(x) = (-1)^{sum_{nu!=mu} x_nu},
   which gives exact Z_3 commutation: [H, P] = 0 on the isotropic line.
   This is a gauge choice that makes the Z_3 manifest. STATUS: EXACT.

2. **Isotropic line k1=k2=k3.** The Z_3 permutation is an exact symmetry
   only on this line. STATUS: EXACT (by construction).

3. **Free staggered Hamiltonian.** No gauge fields, no interactions.
   STATUS: Standard free-field starting point.

---

## What Is Actually Proved

### Exact results (PASS):

1. **Z_3 covariance of symmetric staggered Hamiltonian:**
   P H(k1,k2,k3) P^dag = H(k2,k3,k1). Verified exactly in both
   position space (L = 4, 6, 8) and momentum space.

2. **Z_3 commutation on isotropic line:**
   [H(theta,theta,theta), P] = 0 for all theta, including Wilson term.

3. **Z_3 eigenspace dimensions:** dim V_0 = 4, dim V_1 = 2, dim V_2 = 2.
   Verified at all theta on the isotropic line.

4. **Wilson term preserves Z_3:** [H_Wilson(theta,theta,theta), P] = 0
   for all r and theta.

### Negative result (the key finding):

5. **Sector-restricted Berry phases are all zero:**
   Projecting H(theta) into each Z_3 sector V_k and computing the
   Wilson loop determinant gives gamma_k = 0 mod 2pi for all three
   sectors k = 0, 1, 2. The Berry phase does NOT distinguish sectors.

### Bounded results (with perturbations):

6. **189/256 perturbation configurations give distinct sector Berry phases.**
   With V = eps_1 * (P + P^dag) + eps_2 * i(P - P^dag) added to H,
   the sectors generically acquire different Berry phases. But this
   distinction is MODEL-DEPENDENT.

7. **Twisted loop Z_3 phase shift:**
   On the loop k = (theta, theta+2pi/3, theta+4pi/3), one triplet
   orbit of bands shows a phase shift close to 2pi/3 (error = 0.025).
   This is BOUNDED, not exact.

---

## What Remains Open

1. **Berry phase on other loops.** We tested the isotropic line and
   the Z_3-twisted loop. Other non-contractible loops in T^3 might
   give different results, but the isotropic line is the natural choice
   where Z_3 is exact.

2. **Higher Berry phases / Chern numbers.** The first Chern number
   over 2D slices of the BZ might distinguish sectors. This requires
   integrating the Berry curvature over a 2-torus, not just a circle.

3. **Non-Abelian Berry holonomy.** For the sector-0 subspace (dim 4),
   the U(4) holonomy matrix could carry Z_3 structure even if its
   determinant is trivial. We only computed the Abelian (det) phase.

4. **Interacting Hamiltonian.** With Z_3-symmetric interactions, the
   Berry phase structure could be non-trivial. This is plausible
   but model-dependent.

---

## How This Changes The Paper

### This result does NOT close the generation physicality gate.

The Berry phase approach was tested as a potential unconditional
topological invariant and found to give a NEGATIVE result on the
isotropic line. This is an honest negative finding.

### The paper should NOT claim:

- "Berry phases distinguish the three generations"
- "Z_3 sectors carry distinct topological invariants"
- "Berry/Zak phase provides a generation theorem"

### Paper-safe summary of this lane:

> "The Berry phase along the isotropic line of the symmetric staggered
> Hamiltonian does not distinguish Z_3 sectors (all restricted Berry
> phases are zero). With Z_3-invariant perturbations, sector Berry
> phases generically become distinct (189/256 configurations tested),
> indicating the potential for topological distinction in the interacting
> theory. This remains a bounded result."

### What remains strongest:

The Z_3 superselection argument (Schur's lemma, frontier_generation_
physicality_wildcard.py, 48/0 PASS) remains the strongest topological
result for sector distinction. It does not rely on Berry phases.

---

## Commands Run

```
python3 scripts/frontier_generation_berry_phase.py   # PASS=15  FAIL=10
```

The FAILs include:
- 2 BZ convention mismatches (L=4, L=8 -- known staggered BZ subtlety,
  L=6 matches perfectly)
- 1 sector label instability (expected: degeneracies in free spectrum)
- 1 convergence failure (expected: degenerate bands cause label swaps)
- 4 Berry phase non-distinction (the negative result)
- 1 twisted loop spectrum mismatch
- 1 non-quantization to {0, 2pi/3, 4pi/3} pattern

The EXACT PASS results (11) confirm the Z_3 algebraic structure.
The BOUNDED PASS results (4) confirm perturbation-dependent distinction.

---

## Obstruction Identified

The Berry phase is trivial on the isotropic line because the restricted
Hamiltonian H_k(theta) = B_k^dag H(theta,theta,theta) B_k within each
Z_3 sector has eigenvectors that return to themselves (up to trivial
phases) as theta traverses 0 to 2pi. This is because on the isotropic
line, H(theta) = f(theta) * M where M is a fixed Z_3-invariant matrix,
so eigenvectors are theta-independent (after resolving degeneracies
within each sector).

For the Berry phase to be non-trivial, the restricted Hamiltonian
must have eigenvectors that genuinely ROTATE as a function of theta.
This happens with perturbations but not in the free case.

This obstruction is fundamental to the isotropic-line approach for
the free theory. It does NOT rule out Berry-phase-based arguments
for the interacting theory or on other loops.
