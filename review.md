# Review: monday-koide

Branch reviewed: `origin/monday-koide`

Decision: not safe to land as a retained theorem.

The branch contains useful support-route algebra, but it still promotes the open charged-lepton physical-source selection premise into retained closure. A direct merge is also unsafe because the branch is stale against current `origin/main` and would delete the active open-science lane package and recent EW lattice theorem surfaces.

## Blocking Findings

### [P0] Retained Koide closure still promotes the open physical-source premise

File: `docs/KOIDE_Q_NATIVE_CLOSURE_VIA_OBSERVABLE_PRINCIPLE_LOCALITY_THEOREM_NOTE_2026-04-27.md`, lines 5-13

The note claims retained native closure by saying OP locality plus the retained three-generation structure supplies the missing physical premise. But the load-bearing step is still the unresolved identification that the physical charged-lepton scalar source/readout must be the strict onsite, C3-invariant source grammar rather than the broader projected grammar. Re-embedding the support/criterion algebra does not prove that retained charged-lepton physics forces this source choice, so this remains support/open-lane material, not a retained theorem safe for main.

### [P0] C3-invariance of the physical undeformed source is assumed, not derived

File: `docs/KOIDE_Q_NATIVE_CLOSURE_VIA_OBSERVABLE_PRINCIPLE_LOCALITY_THEOREM_NOTE_2026-04-27.md`, lines 206-228

The derivation moves from local OP sources on three sectors to C3-invariant physical undeformed sources, then concludes `J=sI` and `z=0`. That invariance/selection condition is exactly the missing charged-lepton physical-source premise. The retained notes establish locality and a three-generation structure, but not that the physical charged-lepton readout is forced to the C3-fixed onsite scalar source. Without that theorem, the `Q=2/3` closure claim is still a consequence of an assumed source grammar.

### [P1] Runner verifies algebra after imposing `J=sI`, not physical source selection

File: `scripts/frontier_koide_q_native_closure_via_observable_principle_locality.py`, lines 317-367

The runner constructs the onsite diagonal source, imposes C3 invariance to get `J=sI`, projects it to `z=0`, and then checks `z=0 => Q=2/3`. That is a clean replay of downstream algebra, but it does not independently verify that retained charged-lepton physics forces the physical source/readout onto this C3-fixed onsite route. The final retained-closure flags therefore certify compatibility with the assumed source choice, not discharge of the live residual.

## Dependent Cross-Sector Closure Findings

These are not new blockers introduced by `monday-koide`, but they matter because the branch leans on the same closure posture.

### [P0] Support-only CL3 notes are promoted into a retained cross-sector closure

File: `docs/CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`, lines 5-38

The note treats `CL3_COLOR_AUTOMORPHISM_THEOREM` and `CL3_TASTE_GENERATION_THEOREM` as retained closure authorities and then claims `N_gen = N_color = dim(Z^3) = 3` is now a retained theorem. On current `main`, both cited CL3 notes explicitly label themselves as support theorems, and the color note says it does not upgrade the accepted minimal-input surface. So this branch is still a status promotion, not a discharged retained closure.

### [P0] The generation side is upgraded from candidates to physical `N_gen` without proof

File: `docs/CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`, lines 127-153

The load-bearing Step 2/Step 3 move is not supported by the cited CL3 generation note. That source theorem only establishes three generation candidates or generation-analogous structures from the `hw=1` taste orbit. This branch silently upgrades that weaker support claim into exact physical `N_gen = 3` and then uses it to close `N_gen = N_color`, which is stronger than current `main` actually proves.

### [P1] The retained-input table and downstream promotion claim overstate the current authority surface

File: `docs/CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`, lines 96-107

The note says no support-tier inputs are used, but its own retained-input table includes five support notes plus three explicitly unmerged branches, and then Step 4 promotes all eight to retained. That is not a valid current-main authority surface. Even if the `Z^3` provenance motif were accepted as support, it would not automatically upgrade these support notes, especially the branches that are not on `main` at all.

### [P1] The runner hard-codes the closure package instead of verifying it

File: `scripts/frontier_ckm_koide_cross_sector_z3_closure.py`, lines 55-95

The replay is clean, but it assumes the disputed result at the top of the script by setting `N_GEN_FROM_Z3 = DIM_Z3 = 3` and `N_COLOR_FROM_Z3 = DIM_Z3 = 3`, then mostly checks file existence and downstream arithmetic. That means `PASS=23` certifies compatibility of the claimed closure with the assumed package; it does not verify that current-main retained authorities force the physical cross-sector identification.

## Salvage Path

This branch can be retained as support/open-lane material if it is reframed as a conditional route:

- Replace retained-closure language with support/open-lane language.
- Remove or rename `KOIDE_Q_RETAINED_NATIVE_CLOSURE=TRUE`.
- State the live assumption explicitly: if the physical charged-lepton scalar source/readout is onsite and C3-fixed, then the downstream algebra gives `z=0` and `Q=2/3`.
- Do not cite support-tier CL3 notes as retained authorities.
- Do not promote the dependent cross-sector Koide bridge branches to retained status.
- Rebase or selectively port only safe content onto current `origin/main`; do not merge the stale branch as-is.

## Resubmission Target

To become theorem-grade, the branch needs an independent retained proof that physical charged-lepton observables force the strict onsite, C3-invariant scalar source/readout grammar. Without that, the best status is support evidence for the charged-lepton source-selection open lane.
