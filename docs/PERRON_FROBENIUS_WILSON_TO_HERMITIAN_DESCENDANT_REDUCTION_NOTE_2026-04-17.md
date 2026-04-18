# Perron-Frobenius Wilson-to-Hermitian Descendant Reduction

**Date:** 2026-04-17  
**Status:** exact science-only reduction theorem for the first honest PMNS-side descendant target  
**Script:** `scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_reduction_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

If step 2 is attacked honestly, what is the first PMNS-side descendant theorem
that would actually matter?

## Answer

It is not yet a full Wilson-to-PMNS selector theorem.

The first honest target is narrower:

- a **Wilson-to-Hermitian descendant theorem** landing in the charged-sector
  source-response object
  `dW_e^H`,
  equivalently the charged-support Schur pushforward of the microscopic
  charge-`-1` object `D_-`.

That is the right first target because the current bank already proves:

1. `dW_e^H = Schur_{E_e}(D_-)` on the charged support;
2. `dW_e^H` reconstructs `H_e` exactly;
3. on `N_e`, `H_e` determines the transport packet exactly;
4. the projected-source triplet channels `gamma`, `E1`, `E2` are exact linear
   functionals of `dW_e^H`;
5. once selected-branch Hermitian data are known, the branch side is already
   intrinsically readable from `H`.

So the first honest Wilson descendant target is:

- `Wilson -> D_- -> dW_e^H -> H_e`

not:

- “PMNS somehow.”

## Setup

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
  charge-`-1` source-response law,
- `dW_e^H` reconstructs `H_e` exactly,
- on `N_e`, `H_e` determines the transport packet,
- evaluating `D_-` or `dW_e^H` from the sole axiom is still open.

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- once `dW_e^H` is known, the selected transport column is already algorithmic.

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md):

- the channels `gamma`, `E1`, and `E2` are exact linear functionals of
  `dW_e^H`.

From [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md):

- once selected-branch Hermitian data are known, the branch side is already
  intrinsically readable from the positive polar section `H^(1/2)`,
- but the residual post-Hermitian sheet datum is still not fixed by `H` alone.

From
[DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md):

- after the Hermitian codomain is reached, the remaining blocker is a
  right-sensitive microscopic selector law on
  `dW_e^H = Schur_{E_e}(D_-)`.

## Theorem 1: exact reduction of the first PMNS-side descendant target

On the current exact stack, a Wilson-to-Hermitian descendant theorem landing in
`D_-` or directly in `dW_e^H` would already close the first nontrivial PMNS
codomain needed for the PF lane.

More precisely, once a theorem of the form

- `I_e^* T_Wilson I_e -> D_-`, or
- `P_e T_Wilson P_e -> dW_e^H`,

is available, the following objects become downstream algorithmic:

1. the charged Hermitian block `H_e`,
2. the selected `N_e` transport packet,
3. the projected-source triplet channels `(gamma, E1, E2)`,
4. the branch-side positive polar representative `H_e^(1/2)`.

Therefore the first honest step-2A descendant target is exactly:

- **Wilson-to-Hermitian descendant reduction into `D_- / dW_e^H / H_e`.**

## Corollary 1: the aligned seed carrier is now definitively too small

The aligned dominant-mode law remains real, but it reconstructs only the
aligned seed pair.

By contrast, `dW_e^H` already carries:

- the exact Hermitian block,
- the selected transport packet,
- and the exact projected-source channel data.

So the first meaningful PMNS-side codomain is not the aligned seed carrier. It
is the Hermitian source-response codomain.

## Corollary 2: the residual PMNS last mile starts only after the Hermitian codomain lands

Once the Hermitian codomain is reached, the remaining PMNS-side blocker is no
longer a generic descendant problem. It is the right-sensitive microscopic
selector law on `dW_e^H`, equivalently the residual non-Hermitian/current
object already isolated elsewhere.

So the route order sharpens again:

1. `Wilson -> D_- / dW_e^H / H_e`
2. then, if needed, `dW_e^H ->` right-sensitive selector / `J_chi`

## What this closes

- one exact reduction of the first honest PMNS-side descendant target
- one exact reason `dW_e^H / H_e` is the right first codomain
- one exact separation between the Hermitian descendant target and the residual
  non-Hermitian last mile

## What this does not close

- the Wilson-to-`D_-` theorem itself
- the Wilson-to-`dW_e^H` theorem itself
- the residual right-sensitive selector law
- global PF compatibility

## Atlas inputs used

- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md)
- [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md)
- [DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_reduction_2026_04_17.py
```
