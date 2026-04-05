# Moonshot Frontier Brainstorm V2 Note

**Date:** 2026-04-05  
**Status:** updated moonshot portfolio after the reopened bridge lanes

This note is intentionally compact. It ranks the live frontier after the new
bounded bridge results and keeps each candidate tied to one minimal observable,
one exact reduction / falsifier, one reason it could matter outside this repo,
and one reason it could still fail.

## Current Live Portfolio

1. **Self-consistent propagating field on retained grown geometry**
2. **Grown trapping / frontier transport on the retained moderate-drift row**
3. **Adaptive readout on top of the compact repeated-update source object**
4. **Split-shell generated-family transfer**
5. **One unifying shell-localization architecture that can tie the three lanes
   together**

The ranking is not based on novelty alone.
It is based on which lane best combines:

- a new observable
- a strict reduction check
- a plausible route to later unification
- a chance of raising external interest if it works

## 1. Self-Consistent Propagating Field on Retained Grown Geometry

- Minimal observable: detector-line phase ramp or `escape(gamma) / escape(0)`
  on the retained grown row.
- Exact reduction / falsifier: `gamma = 0` must reproduce the frozen grown
  baseline exactly, and any stronger field update must not rely on ad hoc
  renormalization to make the causal observable appear.
- Why it could raise external interest: this is the cleanest path to a real
  causal-field sector on generated geometry, and it could unify the wavefield,
  source-object, and trapping/frontier threads.
- Why it could fail: the field stays flat once reduction is enforced, or it
  only works after tuning away the weak-field baseline.

## 2. Grown Trapping / Frontier Transport

- Minimal observable: `frontier_bias = (P_frontier - P_core) / P_det` on the
  retained grown row, tracked against trap coupling.
- Exact reduction / falsifier: `eta = 0` must reproduce the frozen grown
  baseline exactly.
- Why it could raise external interest: it is the cleanest strong-field
  observable now on retained grown geometry, and it already looks more
  structure-sensitive than plain escape alone.
- Why it could fail: the frontier bias remains only a transport reshaping
  effect, with no deeper causal or horizon-like structure emerging.

## 3. Adaptive Readout on the Compact Repeated-Update Object

- Minimal observable: detector support drops while the source object remains
  smaller than the broad control, with `TOWARD` and near-linear `F~M`.
- Exact reduction / falsifier: remove the adaptive contour and recover the
  compact repeated-update readout exactly.
- Why it could raise external interest: it is the best current route to closing
  the source/readout asymmetry without throwing away the weak-field law.
- Why it could fail: the detector can be localized a bit, but the mass law or
  sign starts to drift as soon as the readout becomes genuinely selective.

## 4. Split-Shell Generated-Family Transfer

- Minimal observable: a new generated family that increases detector support
  and moves `F~M` closer to `1` relative to the compact bridge family.
- Exact reduction / falsifier: exact zero-source reduction must stay clean, and
  the split-shell family must beat the current compact bridge on both support
  and weak-field fidelity.
- Why it could raise external interest: it weakens the “exact-lattice only”
  objection and gives a real portability story for the weak-field mechanism.
- Why it could fail: the family widens support but still stops short of a clean
  weak-field law, leaving the bridge broadened but not solved.

## 5. One Unifying Shell-Localization Architecture

- Minimal observable: a single shell or contour variable that can describe the
  trapping/frontier lane, the adaptive readout lane, and the generated-family
  support transfer lane with one common handle.
- Exact reduction / falsifier: each sublane must still recover its own frozen
  baseline when the new shell knob is turned off.
- Why it could raise external interest: if one shared shell-localization
  mechanism explains three currently separate bridge results, the program gets
  a much cleaner architecture story instead of three disconnected positives.
- Why it could fail: the common shell only exists as a post-hoc re-labeling of
  three different effects, with no real shared mechanism underneath.

## Ranking Rationale

1. Self-consistent propagating field on retained grown geometry
2. One unifying shell-localization architecture
3. Grown trapping / frontier transport
4. Adaptive readout on the compact repeated-update source object
5. Split-shell generated-family transfer

The top-ranked idea is still the self-consistent propagating field, but the
newly reopened bridges make the unification question more interesting:

- trapping/frontier already gives a bounded strong-field knob
- adaptive readout already gives a bounded detector-side localization knob
- split-shell transfer already gives a bounded geometry-transfer knob

The best moonshot is the one that can explain those three knobs with one
mechanism instead of treating them as unrelated wins.

## Bottom Line

The next batch should not just chase more positives.
It should ask whether the reopened bridge results are all shadows of one
shared shell-localization architecture, and if not, whether the propagating
field lane is the one thing that can still unify them.
