# DM Numerator Direct-Observable Authority Note

**Date:** 2026-04-14  
**Branch:** `codex/dm-across-the-line`  
**Scope:** DM numerator authority surface only

---

## Status

**BOUNDED / OPEN**

This note consolidates the branch-safe numerator authority surface across the
direct-observable route, the Coulomb-from-lattice route, and the final-gaps
route. It does **not** promote the full DM lane to closed. `review.md` still
wins on overall lane status: DM relic mapping remains bounded/open.

The purpose here is narrower:

- keep the numerator-side claims internally consistent
- separate what is derived from what is still bounded
- isolate the remaining open bridge so it is easy to attack next

---

## Consolidated Authority Surface

The branch now has three mutually reinforcing numerator results:

1. **Direct-observable `sigma_v` route**
   - `sigma_v` is treated as a direct observable of the Hamiltonian `H`
   - the lattice T-matrix / optical-theorem route is the preferred numerator
     surface
   - this is the strongest live route for the annihilation coefficient

2. **Coulomb-from-lattice route**
   - the static Coulomb potential is a lattice Green's-function observable
   - `V(r) = -C_F * g^2 * G(r)` is the native bridge
   - the far-field Coulomb form is therefore derived from lattice potential
     theory, not imported as a standalone perturbative ansatz

3. **Final-gaps route**
   - the `sigma_v` coefficient surface is tightened to the algebraic
     `C = pi` form on the reviewed lattice kinematics
   - the lattice master equation to Boltzmann coarse-graining is the lattice
     dynamics, not an imported cosmology scaffold
   - this materially sharpens the numerator-side bridge, but it does not by
     itself close the full relic lane

Taken together, these three notes give one coherent numerator story:

    H -> T-matrix -> sigma_v
    H -> lattice Green's function -> Coulomb potential -> Sommerfeld factor
    lattice master equation -> Boltzmann coarse-graining

That is the branch's current numerator authority surface.

---

## What Is Derived

The following are branch-safe as derived or strengthened derived claims:

- the Coulomb potential has a native lattice Green's-function route
- the `sigma_v` surface has a native direct-observable route through `H`
- the finite-lattice optical-theorem / T-matrix machinery is the right
  numerator language
- the `sigma_v` coefficient surface is algebraically tightened to `C = pi`
  on the reviewed lattice kinematics
- the master equation is lattice-native dynamics, and Boltzmann coarse-
  graining follows from the reviewed lattice reduction story

These are real numerator advances. They should be treated as branch authority.

---

## What Is Bounded

The following remain bounded and should stay labeled that way:

- the gauge-normalization issue should no longer be presented as a simple
  scanned free parameter if `G_BARE_RIGIDITY_THEOREM_NOTE.md` survives
  review; until that theorem candidate is fully accepted, keep the
  normalization issue explicit and bounded
- finite-lattice and Born-level caveats still matter for the cross-section
  surface
- the thermodynamic-limit and radiation-era bridges are still not complete
  theorem-grade closures
- the full relic mapping is still bounded because the numerator is not yet
  enough to close the complete cosmological ratio on its own; the next honest
  full-lane blocker is the denominator `eta`

This is the important status boundary: the numerator is stronger, but the
lane is still not closed.

---

## What Remains Open

The live open pieces are:

1. **Gauge-normalization integration**
   - the direct-observable route removes the old separate-coupling ambiguity
   - the newer branch question is whether the rigidity-theorem route is
     accepted as authority
   - if it is accepted, `g_bare` stops being the paper's headline blocker

2. **Full numerator-to-relic normalization closure**
   - the branch still needs a clean thermodynamic / radiation-era bridge from
     the strengthened numerator to the final relic ratio

3. **Denominator `eta`**
   - once the gauge-normalization issue is narrowed, `eta` becomes the next
     honest full-lane blocker
   - the strongest fallback surface is `R(eta)`
   - the cleaner theorem-grade research path is leptogenesis, not the current
     EWBG transport stack

4. **Secondary `k = 0` / radiation-era wording**
   - the freeze-out expansion surface is materially narrowed
   - the residual issue is now more about exact claim language and
     normalization than about a missing numerator-side computation

5. **Authority normalization across notes**
   - the note set should keep `DM_DIRECT_OBSERVABLE_NOTE.md`,
     `DM_COULOMB_FROM_LATTICE_NOTE.md`, and `DM_FINAL_GAPS_NOTE.md`
     synchronized in wording
   - none of them should overstate closure relative to `review.md`

The open part is therefore not "more numerator algebra" first. It is the
remaining framework-normalization and relic-bridge boundary around the
strengthened numerator.

---

## Preferred Next Attack

The preferred next attack is:

1. keep the direct-observable route as the primary numerator workstream
2. use the Coulomb-from-lattice result as the native potential bridge
3. carry the final-gaps result forward as the numerator coefficient and
   Boltzmann-strengthening layer
4. package the paper surface around `R(eta)` while the denominator remains
   open
5. if denominator work resumes, treat leptogenesis as the cleaner theorem
   program and do not revert to EWBG transport as the default flagship route

If the branch needs a second-order alternative after that, the best next
candidate is still the direct-observable stack plus source-response /
determinant style tooling, not a return to transport-tuning as the primary
answer.

---

## Branch-Safe Summary

The honest branch-safe summary is:

- numerator structure is now materially stronger and partly derived
- the Coulomb shape is native
- `sigma_v` has a direct-observable route
- the coefficient and Boltzmann bridge are tightened
- the overall DM lane is still bounded/open because the full relic bridge is
  not closed yet
- the numerator no longer needs to be sold through an old free-`g` window
- once the gauge-normalization question is narrowed, the next honest blocker
  is `eta`, not missing numerator algebra

That is the status this branch should preserve until the remaining bridge is
actually closed.
