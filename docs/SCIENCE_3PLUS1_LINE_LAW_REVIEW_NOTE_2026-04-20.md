# Science `3plus1` Line-Law Review

**Date:** 2026-04-20  
**Branch:** `codex/science-3plus1-line-law`  
**Status:** not yet safe to promote as a full flagship DM-gate closure

## Scope

This review covers the new Wilson/DM route centered on:

- the first-sector retained packet and first-Hankel boundary
- the new least-positive-bulk completion principle
- the retained `3d+1 -> 3d` complement-line packet
- the `rho1` orientation / least-distortion selector
- the claimed closure endpoint on the enlarged Wilson/DM stack

Core files reviewed:

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md)
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_EXACT_SOLVE_DOUBLET_THEOREM_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_EXACT_SOLVE_DOUBLET_THEOREM_NOTE_2026-04-20.md)
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md)
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md)

and the matching runners.

## Review verdict

The branch has real new science, but it has **not yet proved full flagship closure**.

What is already real:

1. the upstream first-sector packet work is meaningful
2. the `dW_e^H` even-split layer is real
3. the sparse-face exact target preimage is real
4. the new branch significantly sharpens the Wilson-side route into a concrete enlarged-stack candidate

What is still missing:

1. the new Wilson-side completion rule is still a **new principle**, not a retained derivation
2. the claimed exact complement-line doublet is still certified by **hardcoded witnesses**, not a solved/exhausted theorem
3. the `rho1` selector is only shown to choose **A over B**, not to minimize over the full exact solution set
4. the endpoint therefore overstates the branch as having removed the final line-law seam

## What already looks solid

### A. Truncated retained packet / first-Hankel boundary

The upstream packet route is worth keeping.

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md)
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_FIRST_HANKEL_TO_DM_BOUNDARY_NOTE_2026-04-19.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_FIRST_HANKEL_TO_DM_BOUNDARY_NOTE_2026-04-19.md)

These notes do real narrowing work:

- the retained first-sector triple already fixes one explicit retained packet `rho_ret`
- the earliest Wilson-side scalar seam really does start at the first-Hankel / first-Jacobi layer

### B. `dW_e^H` even-split layer

- [frontier_dm_leptogenesis_dweh_even_split_transfer_layer.py](../scripts/frontier_dm_leptogenesis_dweh_even_split_transfer_layer.py)

This runner establishes a real exact codomain refinement:

- the unsymmetrized even split is exactly `(S12, S13)`
- it is strictly finer than the current triplet package
- it reproduces the known target preimage on the sparse face

This is legitimate support science on the open DM gate.

### C. Sparse-face exact target preimage

- [frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem.py](../scripts/frontier_dm_leptogenesis_k00_sparse_face_target_preimage_theorem.py)

This also looks real:

- the observed live target has an exact constructive preimage on the exact sparse face `y2 = 0`
- the remaining microscopic object really is a low-support right-sensitive face law

Again, this is a real narrowing theorem on the open gate.

## Missing items before this can be promoted as closure

### 1. Derive the least-positive-bulk rule, or label it honestly as a new principle

Current state:

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md)
- [frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py](../scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py)

What the branch proves now:

- once `rho_ret` is fixed, the zero extension is coefficientwise least
- therefore it minimizes positive bulk-tail functionals

What it does **not** yet prove:

- why physics/Wilson structure forces that rule

So the current theorem is:

- a mathematically coherent **selection principle**

not yet:

- a retained/theorem-native Wilson derivation

To close this item, do one of:

1. derive least-positive-bulk completion from a real Wilson-side variational, extremal, Perron, or first-layer structural theorem; or
2. keep it explicitly labeled as a new enlarged-stack principle and stop using it as if it were retained closure.

### 2. Replace hardcoded `LINE_A` / `LINE_B` with a real solve theorem

Current state:

- [frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19.py](../scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19.py)
- [frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_2026_04_20.py](../scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_2026_04_20.py)

The helper currently contains explicit arrays:

- `LINE_A`
- `LINE_B`

The "exact-solve doublet theorem" then checks that:

- `LINE_A` hits the target
- `LINE_B` hits the target
- they are distinct

That is **not** yet an exact-solve theorem for the full complement-line problem.

To close this item, the branch needs a genuine solve/exhaustion result:

1. write down the exact target-hitting equations for the complement line on the selected branch
2. prove the full normalized real solution set
3. show that the only solutions are exactly two points up to sign, namely the present `A` and `B`

If exact symbolic exhaustion is too hard, an acceptable intermediate result would be:

- a certified solve theorem reducing the set to two isolated real roots with a numerical certificate strong enough to justify the doublet claim

### 3. Prove the selector over the full solution set, not only over `A` and `B`

Current state:

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md)
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md)

Right now the selector theorem proves:

- `key(A) < key(B)`

where the key is:

- projector Frobenius distance to the `rho1` slice
- then boundary-anchor loss

That is only enough if the solution set is already proved to be exactly `{A, B}` up to sign.

So the selector law is not closure-grade until item 2 is closed.

To close this item, prove:

1. the full exact target-hitting solution set is the orientation doublet, and
2. the `rho1` least-distortion law is uniquely minimizing on that full set

### 4. Recut the endpoint note until the above steps are proved

Current state:

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md)
- [frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_closure_endpoint_2026_04_20.py](../scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_closure_endpoint_2026_04_20.py)

The endpoint currently composes:

- the new bulk-completion principle
- the selected first-layer Wilson/Perron packet
- one imported explicit line witness
- the existing sparse-face DM target preimage

That is enough for:

- a strong enlarged-stack support/candidate packet

It is not yet enough for:

- "the DM flagship gate is closed positively"
- "no remaining branch-choice or slice-law seam"

So until items 1-3 are closed, this endpoint note should be read only as:

- enlarged-stack candidate closeout

not:

- authoritative flagship closure

## One cleanup issue

The upstream packet script

- [frontier_gauge_vacuum_plaquette_first_sector_truncated_environment_packet_theorem_2026_04_19.py](../scripts/frontier_gauge_vacuum_plaquette_first_sector_truncated_environment_packet_theorem_2026_04_19.py)

currently references a missing note filename:

- `docs/GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md`

while the branch contains the script

- [frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17.py](../scripts/frontier_gauge_vacuum_plaquette_retained_class_sampling_inversion_2026_04_17.py)

and the review logic only needs the finite-sampling/inversion fact. This is a fixable branch hygiene issue and should be corrected.

## Practical next-step list for the worker

1. Close the bulk-completion rule:
   derive it from Wilson/Perron structure, or relabel it as an added enlarged-stack principle.
2. Replace witness certification with a real complement-line solve:
   no hardcoded `A/B` dependence in the theorem.
3. Prove the exact solution set is precisely the orientation doublet up to sign.
4. Prove the `rho1` selector is uniquely minimizing on that full solution set.
5. Only then restore a real closure-endpoint theorem.

## Current best honest packaging

If no further proof is added, the branch is still worth salvaging as:

- a Wilson/`dW_e^H` support packet
- a real upstream narrowing of the open DM flagship route
- an enlarged-stack candidate closure route

But it should **not** yet be landed or described as a full flagship closeout on `main`.
