# CKM Charge Selection -- Honest Status Note

**Date:** 2026-04-12 (updated)  
**Status:** BOUNDED -- quantitative hierarchy unsolved.  
**Script:** `scripts/frontier_ckm_dynamical_selection.py`  
**Review source:** `docs/CODEX_MACMINI_FEEDBACK_CKM_GAUGE_2026-04-12.md`

**Primary gap:** The quantitative CKM hierarchy (why V_us ~ 0.22,
V_cb ~ 0.04, V_ub ~ 0.004) is not derived from the lattice. The
framework provides the Z_3 symmetry structure that gives three
generations and suggests a Froggatt-Nielsen-like texture, but the
specific quantitative values of the mixing angles remain open. This is
a genuine unsolved physics problem, not a matter of precision or
matching coefficients -- the mechanism that generates the observed
hierarchy has not been identified within the framework.

---

## What this lane actually is

The script explores whether Z_3^3 directional charges from the lattice
can be narrowed to a specific Froggatt-Nielsen charge assignment using
symmetry arguments. It is a **charge-pattern selection** study.

It is **not** a quantitative CKM derivation. The script's own predicted
CKM elements do not match observation:

| Element | Script output | PDG 2024 |
|---------|--------------|----------|
| V_us | 0.111 | 0.224 |
| V_cb | 0.111 | 0.042 |
| V_ub | 0.012 | 0.004 |

These are off by factors of 2-3. The script does not close CKM.

---

## What IS derived vs what is ASSUMED

### Derived (or at least shown)

1. **Z_3 charge range covers the needed FN range.**
   The Z_3^3 directional charges naturally produce values in the 0-6 range,
   which is the range needed for realistic Froggatt-Nielsen textures. This
   is a structural fact of the lattice symmetry.

2. **S_3 symmetry can prefer (5,3,0) under Interpretation B.**
   Among many low-chi-squared charge assignments, the S_3 permutation
   symmetry of the three lattice directions singles out (5,3,0) -- but
   only under one of two tested interpretations.

### Assumed (not derived)

1. **Interpretation B (why not A?).**
   The script tests two interpretations of how S_3 symmetry classes map
   to generations. Interpretation A gives the wrong charges; Interpretation B
   gives the target. The choice of B over A is not derived from any deeper
   principle -- it is selected because it works.

2. **Higgs Z_3 charge delta = 1.**
   The down-sector derivation assumes a generation-dependent Higgs shift
   with delta = (1,1,0), where generation 3 is exempt. This rule is chosen
   to recover the target charges, not derived from the lattice structure.

3. **Froggatt-Nielsen mechanism with epsilon = 1/3.**
   The FN mechanism itself and the specific expansion parameter epsilon = 1/3
   are inputs, not outputs. The identification epsilon = 1/3 is what makes
   the Cabibbo angle come out right, but this identification is assumed.

4. **O(1) coefficients.**
   The FN texture approach assumes that O(1) prefactors in the mass matrix
   are all roughly 1. The factor-of-2 discrepancies in V_us etc. live
   precisely in this O(1) ambiguity.

---

## Strongest honest claim

> Z_3^3 directional charges naturally reach the observed FN charge range,
> and an additional S_3-based symmetry principle can be used to prefer one
> charge pattern over many low-chi-squared alternatives.

This is much weaker than "CKM is derived from the lattice."

---

## What would need to be derived to upgrade this

To turn this into a genuine CKM derivation, the following gaps must close:

1. **Derive why Interpretation B is physically forced**, not merely viable.
   Currently the two interpretations are equally valid readings of the S_3
   action on generations.

2. **Derive the Higgs Z_3 charge rule** delta = 1 from the lattice structure
   or from a symmetry principle that is already established.

3. **Derive why generation 3 is exempt** from the Higgs shift. The current
   script handles this as a special case.

4. **Derive epsilon = 1/3** from the lattice, rather than identifying it
   post hoc from the observed Cabibbo angle.

5. **Reproduce quantitative CKM elements** (V_us, V_cb, V_ub) to within
   their experimental uncertainties, not just the correct order of magnitude.

6. **Anomaly cancellation does not help.** The script's own anomaly
   cancellation analysis does not select the target charges. This is
   noted honestly in the script itself.

---

## Relationship to Cabibbo/Jarlskog predictions

The Cabibbo angle and Jarlskog invariant numbers quoted elsewhere in this
project (0.3% and 2.1% matches) come from a **different calculation** --
the Z_3 baryogenesis phase delta = 2pi/3 in `scripts/frontier_baryogenesis.py`.

That calculation uses the CP phase from Z_3 symmetry combined with an
assumed FN parameter. It does not go through the charge-selection machinery
in this script. The two lanes should not be conflated.

See `docs/CABIBBO_JARLSKOG_PREDICTION_2026-04-12.md` for the honest
framing of that separate result.
