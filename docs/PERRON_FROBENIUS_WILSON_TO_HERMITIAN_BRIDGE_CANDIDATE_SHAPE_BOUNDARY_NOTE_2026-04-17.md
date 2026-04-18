# Perron-Frobenius Wilson-to-Hermitian Bridge Candidate Shape Boundary

**Date:** 2026-04-17  
**Status:** exact science-only shape boundary for future positive step-2A bridge candidates  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_wilson_to_hermitian_bridge_candidate_shape_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the PF lane has already proved that the current bank does not contain the
missing Wilson-to-`D_-` / Wilson-to-`dW_e^H` bridge, what **shape** can a
future positive step-2A bridge candidate honestly have?

## Bottom line

The wrong candidate classes are now exactly ruled out.

A future positive step-2A bridge candidate cannot be:

1. another additive scalar observable in the present `log|det|` grammar;
2. another support-only intertwiner on the taste-cube / BZ-corner side;
3. another bank scan over existing Wilson, observable, and PMNS tools.

The minimal admissible shape is instead:

- a genuinely new **matrix-valued cross-sector descendant/intertwiner law**
  landing in the charged Hermitian codomain
  `D_- / dW_e^H / H_e`,
- and, if step 2B is still needed after that, a genuinely new
  **sector-sensitive, inter-sector, non-additive mixed bridge** on the PMNS
  selector side.

So the future step-2A bridge must already be more structured than anything in
the current scalar or support bank.

## Exact inputs

### 1. The codomain is charged-sector and matrix-valued

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
and
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- the first honest step-2A target is the charged chain

  `Wilson -> D_- -> dW_e^H -> H_e`;

- `dW_e^H = Schur_{E_e}(D_-)`;
- `dW_e^H` reconstructs the Hermitian charged block `H_e`.

So the codomain is not scalar. It is charged-sector operator/Hermitian data.

### 2. The present observable grammar is scalar and additive

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the retained observable generator is

  `W[J] = log|det(D+J)| - log|det D|`;

- its local observables are scalar source derivatives.

From
[PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md](./PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md):

- that present scalar grammar is block-local on independent lepton blocks and
  does not realize the missing PMNS inter-sector bridge.

So another scalar additive observable cannot honestly be the step-2A bridge.

### 3. The present support intertwiner is support-only

From [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):

- the existing exact intertwiner bridges support-side taste-cube and
  BZ-corner structures;
- its safe role is support transport only.

So another support-only intertwiner cannot honestly be the charged-sector
Wilson descendant law either.

### 4. The PMNS positive extension class is already typed

From
[PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md](./PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md)
and
[PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md):

- any future positive PMNS selector realization must be sector-sensitive,
  inter-sector, and non-additive;
- the reduced surviving class carries only one amplitude slot after reduction.

So if step 2B remains after the Hermitian descendant lands, its admissible
shape is already known too.

## Theorem 1: admissible candidate shape for a future positive step-2A bridge

Assume the exact step-2A codomain reduction, the exact current-bank
nonrealization theorem, the exact scalar observable principle, the exact PMNS
scalar-bridge nonrealization theorem, the exact site-phase / cube-shift support
intertwiner, and the exact PMNS minimal positive extension theorem. Then any
future positive candidate for the missing Wilson-to-Hermitian bridge must:

1. be **non-scalar** relative to the present additive `log|det|` observable
   grammar;
2. be **more than support transport** relative to the present taste-cube /
   BZ-corner intertwiner;
3. be **matrix-valued on the charged-sector codomain**
   `D_- / dW_e^H / H_e`;
4. and, if a residual PMNS last mile survives, couple to a
   **sector-sensitive inter-sector non-additive mixed bridge** downstream.

Therefore the admissible future bridge search should exclude scalar-observable
and support-only constructions from the outset.

## Corollary 1: the candidate search space is now much smaller

The honest step-2A search is not:

- another determinant-source scalar theorem,
- another support-side intertwiner theorem,
- another scan for a hidden current-bank carrier.

It is:

- a genuinely new cross-sector operator law with charged Hermitian output.

## Corollary 2: step 2A and step 2B now have distinct shape signatures

The branch can now state the shape difference cleanly:

- step 2A must land in charged-sector operator/Hermitian data;
- step 2B, if still needed, must activate one sector-sensitive mixed-bridge
  amplitude.

So the two remaining positive objects are not only sequentially distinct. They
are structurally distinct too.

## What this closes

- one exact exclusion of scalar-only and support-only candidate classes for the
  missing step-2A bridge;
- one sharper structural signature for future positive bridge candidates;
- one cleaner separation between step-2A and step-2B candidate searches.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a nonzero reduced bridge amplitude;
- a positive global PF selector.

## Why this matters

This note is useful because it saves the branch from chasing the wrong theorem
families.

The repo can now say, exactly:

- the bridge is not already in the bank,
- the minimal positive completion class is known,
- and the admissible step-2A candidate shape already excludes scalar and
  support-only constructions.

## Atlas inputs used

- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md](./PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md](./PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md)
- [PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_wilson_to_hermitian_bridge_candidate_shape_boundary_2026_04_17.py
```
