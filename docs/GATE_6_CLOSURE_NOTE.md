# Gate 6: CKM Structure -- Bounded Consistency

**Status:** Bounded consistency, not derived  
**Codex objection:** "Interpretation B derived -- not closed; Higgs-charge step not universal"  
**Scripts:** `frontier_ckm_dynamical_selection.py`, `frontier_generation_physicality.py`

---

## What is proven

1. **Z_3 texture exists.** The Z_3 cyclic permutation acting on the three
   taste-triplet states produces a generation-dependent phase structure.
   When the three spatial hopping amplitudes are not equal (t_x != t_y != t_z),
   the up-type and down-type mass eigenbases are misaligned. This misalignment
   is a geometric consequence of the Z_3 action on anisotropic couplings.

2. **The Z_3 phase gives a CP-violating invariant.** The Z_3 root of unity
   exp(2pi*i/3) contributes a CP phase delta = 2pi/3. The resulting Jarlskog
   invariant J(Z_3) = 7.6e-5 is within a factor of 2.5 of the measured value
   J(PDG) = 3.1e-5. This is order-of-magnitude agreement for a parameter-free
   geometric prediction.

3. **The Z_3^3 charge range covers the Froggatt-Nielsen window.** The
   directional charges from Z_3^3 naturally span the range 0-6, which is the
   range needed for realistic Froggatt-Nielsen textures. This is a structural
   fact of the lattice symmetry group.

4. **S_3 symmetry can select a preferred charge pattern.** Among many
   low-chi-squared charge assignments, the S_3 permutation symmetry of the
   three lattice directions singles out the (5,3,0) pattern under one of two
   tested interpretations (Interpretation B).

## What is NOT derived

1. **The choice of Interpretation B over A.** The script tests two
   interpretations of how S_3 symmetry classes map to generations.
   Interpretation A gives wrong charges; B gives the target. The selection
   of B is empirical, not derived from any deeper principle.

2. **The Higgs Z_3 charge assignment.** The down-sector mass matrix uses a
   generation-dependent Higgs shift delta = (1,1,0), where generation 3 is
   exempt. This rule is chosen to recover the observed pattern, not derived
   from the lattice structure.

3. **The Froggatt-Nielsen expansion parameter.** The identification
   epsilon = 1/3 is what makes the Cabibbo angle come out. This value is not
   derived; it is selected because it works.

4. **Quantitative CKM elements.** The script's predicted CKM elements are off
   by factors of 2-3 from PDG values (V_us = 0.111 vs 0.224, V_cb = 0.111 vs
   0.042). These discrepancies live in the O(1) ambiguity of the
   Froggatt-Nielsen approach.

## Honest accounting

| Input | Status |
|-------|--------|
| Z_3 generation structure | Derived (Gate 2) |
| Z_3 CP phase delta = 2pi/3 | Derived (geometric) |
| Jarlskog invariant J ~ 10^{-5} | Consistent (factor 2.5) |
| Z_3^3 charge range | Structural fact |
| S_3 charge selection | Conditional on Interpretation B |
| Higgs charge delta = (1,1,0) | Assumed (1 bounded input) |
| epsilon = 1/3 | Assumed |
| Quantitative V_ij values | Not reproduced (factor 2-3 off) |

## Paper-safe claim

> The Z_3 generation texture combined with a Higgs charge assignment gives CKM
> structure consistent with the observed pattern at the order-of-magnitude
> level. The CP phase delta = 2pi/3 and the Jarlskog invariant J ~ 10^{-5}
> are geometric consequences of Z_3. The quantitative CKM matrix requires the
> Higgs charge assignment as one bounded input and an FN expansion parameter
> as a second. This is bounded consistency -- not a derivation -- with two
> named inputs beyond the lattice axiom.
