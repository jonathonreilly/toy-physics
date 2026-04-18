# Perron-Frobenius Step-2 Charged Embedding Boundary

**Date:** 2026-04-17  
**Status:** exact science-only boundary theorem for the missing Wilson-side charged embedding/compression object  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_charged_embedding_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

Once the PF lane has already fixed:

- the first honest codomain `D_- / dW_e^H / H_e`,
- the minimal positive completion class,
- the admissible candidate shape,
- and the admissible operator-level proof form,

what exact primitive is still missing **before** one can even write a genuine
positive Wilson-side bridge candidate?

## Bottom line

The missing primitive is an explicit **Wilson-side charged embedding /
compression object** realizing the charged support on the parent Wilson space.

The current bank already has:

1. the PMNS-side charged support label `E_e`;
2. the charged Schur codomain `dW_e^H = Schur_{E_e}(D_-)`;
3. the correct future operator form
   `I_e^* T_Wilson I_e -> D_-` or `P_e T_Wilson P_e -> dW_e^H`.

But it still does **not** have:

- an explicit Wilson-side operator `I_e` or `P_e` whose theorem-grade role is
  to embed/compress the Wilson parent object onto that charged support.

So the next constructive step-2A primitive is no longer vague. It is exactly:

- a Wilson-side charged embedding/compression realization.

## What is already present

### 1. The PMNS side fixes the charged support label

From
[DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md):

- the lepton supports `E_nu` and `E_e` are fixed;
- once the Hermitian pair is supplied, the PMNS projector packet is automatic.

So the charged support label is already known on the PMNS side.

### 2. The charged codomain itself is already exact

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H = Schur_{E_e}(D_-)`;
- `dW_e^H` reconstructs `H_e`.

So the downstream charged Hermitian codomain is already exact once the
microscopic charge block is supplied.

### 3. The future theorem form is already fixed schematically

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
and
[PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md):

- the admissible operator-level target forms are

  `I_e^* T_Wilson I_e -> D_-`,

  or

  `P_e T_Wilson P_e -> dW_e^H`.

So the branch already knows what the theorem should look like once the charged
embedding/compression object exists.

### 4. But the current bank still does not realize that embedding/compression object

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the existing Wilson, observable, support, and PMNS tools do not yet realize
  the missing cross-sector descendant law.

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md):

- support-only transport is excluded;
- scalar-only observable constructions are excluded.

So the charged embedding/compression object is not already supplied by the
current support bank or by the current scalar observable bank.

## Theorem 1: exact missing primitive before a positive step-2A candidate can exist

Assume the exact PMNS projector-interface theorem, the exact charged
source-response reduction theorem, the exact Wilson-to-Hermitian descendant
reduction theorem, the exact step-2 operator-form boundary theorem, and the
exact current-bank nonrealization theorem. Then:

1. the PMNS-side charged support `E_e` is fixed;
2. the charged Schur codomain `dW_e^H = Schur_{E_e}(D_-)` is fixed;
3. the future positive theorem form is already known schematically as a Wilson
   compression/intertwiner into `D_-` or `dW_e^H`;
4. but no explicit Wilson-side charged embedding/compression object realizing
   that schematic form is yet present in the current bank.

Therefore the next missing constructive primitive on step 2A is exactly a
Wilson-side charged embedding/compression realization.

## Corollary 1: the search target is now narrower than “find an intertwiner”

The next honest positive step is not:

- generic intertwiner rhetoric,
- generic operator analogies,
- another support-side transport note.

It is:

- an explicit charged embedding/compression object on the Wilson parent space.

## Corollary 2: once that primitive lands, the candidate theorem can finally be concrete

After an explicit Wilson-side charged embedding/compression object is derived,
the schematic forms

- `I_e^* T_Wilson I_e -> D_-`,
- `P_e T_Wilson P_e -> dW_e^H`

stop being just theorem-form placeholders and become concrete candidate
operator laws.

## What this closes

- one exact identification of the next missing primitive on step 2A;
- one sharper distinction between codomain data and Wilson-side embedding data;
- one clearer constructive target for the next theorem search.

## What this does not close

- an explicit Wilson-side charged embedding/compression object;
- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note keeps the branch from skipping a hidden prerequisite.

The repo now knows:

- the codomain,
- the admissible candidate shape,
- the admissible proof form,

and now also:

- the missing Wilson-side primitive needed before a real operator candidate can
  even be instantiated.

## Atlas inputs used

- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_charged_embedding_boundary_2026_04_17.py
```
