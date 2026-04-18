# Perron-Frobenius PMNS Descendant Target Decomposition

**Date:** 2026-04-17  
**Status:** exact science-only target theorem for the PMNS side of step 2  
**Script:** `scripts/frontier_perron_frobenius_pmns_descendant_target_decomposition_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

If the missing theorem is a Wilson-to-PMNS descendant / intertwiner theorem,
what should that theorem actually land in?

## Answer

It should **not** be phrased as “recover the aligned PMNS seed carrier” and it
should **not** jump directly to full selector closure.

The clean step-2 target already decomposes into two pieces:

1. **Hermitian descendant target.**  
   Land the Wilson descendant law in the PMNS Hermitian response data
   (`dW_e^H`, `H_e`, and the corresponding selected-branch Hermitian packet).

2. **Residual non-Hermitian current target.**  
   After the Hermitian target is reached, the remaining PMNS-side last mile is
   the native nontrivial current `J_chi` or an equivalent right-sensitive
   datum.

So the PMNS side of the global PF program is not one theorem. It is one
two-stage descendant target.

## Why the Hermitian target is the right first codomain

From [PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md):

- if the nontrivial `hw=1` source/transfer pack is supplied, the retained PMNS
  lane reconstructs the downstream Hermitian / PMNS data exactly.

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md):

- the projected Hermitian response pack `dW_e^H` already carries the triplet
  channels `gamma`, `E1`, and `E2` by exact linear formulas.

From [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md):

- once selected-branch Hermitian data are known, the branch side is already
  intrinsically readable from the positive polar section `H^(1/2)`.

So a Wilson descendant that lands in the Hermitian PMNS codomain would already
unlock real downstream structure.

## Why the Hermitian target is still not the full PMNS last mile

From [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md):

- Hermitian data are still sheet-even.

From [PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md](./PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md):

- the smallest remaining PMNS-side source object is the native complex current
  `J_chi`,
- and the current retained sole-axiom routes still force `J_chi = 0`.

So even after a Hermitian descendant theorem, the PMNS lane may still need one
extra non-Hermitian or right-sensitive current law.

## Theorem 1: exact decomposition of the PMNS descendant target

On the current exact bank, the clean PMNS-side step-2 target decomposes as:

1. **First descendant target:** derive a Wilson-to-Hermitian descendant /
   intertwiner theorem landing in projected Hermitian response data.
2. **Second descendant target:** derive a Wilson-to-`J_chi` theorem, or an
   equivalent non-Hermitian / right-sensitive descendant law, if the Hermitian
   target still leaves the PMNS last mile open.

Therefore the honest step-2 attack is not “derive PMNS somehow.” It is:

- first `Wilson -> dW_e^H / H`,
- then, if needed, `Wilson -> J_chi`.

The new reduction note
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
sharpens the first arrow one level further:

- the first honest codomain is the charged-sector Schur-pushforward chain
  `Wilson -> D_- -> dW_e^H -> H_e`,
- because once `dW_e^H` is known, `H_e`, the selected transport packet, and
  the projected-source triplet channels are already downstream algorithmic.

## Corollary 1: the aligned seed carrier is too small as the main codomain

The aligned dominant-mode theorem is real, but by itself it only reconstructs
the aligned seed pair.

That is too small to serve as the main step-2 codomain because:

- it does not carry the full supplied-pack reconstruction content,
- it does not already expose the projected Hermitian downstream channels,
- and it does not isolate the residual non-Hermitian last mile.

## Corollary 2: the smallest honest PMNS last-mile target is already explicit

If a Hermitian descendant theorem lands first, the smallest remaining PMNS-side
target is already known:

- one native complex current `J_chi`.

So the PMNS last mile is not vague anymore either.

## What this closes

- one exact decomposition of the PMNS side of step 2 into Hermitian and
  non-Hermitian subtargets
- one exact reason the Hermitian codomain is the right first target
- one exact reason the current `J_chi` is still the likely residual last mile

## What this does not close

- the Wilson-to-Hermitian descendant theorem itself
- the Wilson-to-`J_chi` theorem itself
- a nontrivial sole-axiom PMNS current law
- global PF compatibility

## Atlas inputs used

- [PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md)
- [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md)
- [PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md](./PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_pmns_descendant_target_decomposition_2026_04_17.py
```
