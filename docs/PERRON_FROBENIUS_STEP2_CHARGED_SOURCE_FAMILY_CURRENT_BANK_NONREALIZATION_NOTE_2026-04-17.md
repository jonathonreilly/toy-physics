# Perron-Frobenius Step-2 Charged Source-Family Current-Bank Nonrealization

**Date:** 2026-04-17  
**Status:** exact science-only nonrealization theorem for the remaining compressed-route primitive on the current bank  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_charged_source_family_current_bank_nonrealization_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the compressed PF route has been reduced to one Wilson-side charged source
family / channel primitive, does the **current exact bank** already supply that
primitive under another label?

## Bottom line

No.

The current exact bank does **not** already realize the Wilson-side charged
source family / channel needed by the compressed `Wilson -> dW_e^H` route.

What the bank already has:

- theorem-grade additive source-response machinery,
- the exact charged projected-source codomain `dW_e^H`,
- exact downstream reconstruction from `dW_e^H`,
- charged-support labels and codomain bookkeeping.

What it still does not have:

- the Wilson-side charged source family / channel whose responses land on that
  codomain.

## What is already exact

### 1. Response and reconstruction are present

From
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md):

- the compressed route is already reduced to one Wilson-side charged source
  family / channel primitive;
- the rest of the reconstruction algebra is already exact.

### 2. The current bank already lacks the corresponding Wilson-side charged embedding / compression object

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the branch still lacks the explicit Wilson-side charged embedding /
  compression object.

From
[PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md):

- that object cannot be obtained by pure support pullback.

### 3. The current bank already lacks the upstream Wilson-to-`dW_e^H` theorem

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current exact bank does **not** already contain the missing
  Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem under another name.

So the compressed-route primitive is not already realized upstream either.

## Theorem 1: exact nonrealization of the charged source family on the current bank

Assume the exact charged source-family target theorem, the exact charged
embedding boundary theorem, the exact charged-support pullback boundary theorem,
and the exact Wilson-to-Hermitian current-bank nonrealization theorem. Then:

1. the compressed route is reduced to one Wilson-side charged source family /
   channel primitive;
2. the current bank does not already supply the needed charged embedding /
   compression object;
3. the current bank does not already supply the corresponding Wilson-to-`dW_e^H`
   descendant theorem.

Therefore the current exact bank does **not** already realize the Wilson-side
charged source family / channel primitive required by the compressed route.

## Corollary 1: compressed-route construction now has no hidden-bank loophole left

The compressed route should no longer spend effort on:

- rescanning the current bank for a hidden source family,
- rephrasing support transport as if it were the missing channel,
- or treating existing response algebra as if it already supplied the source.

Those loopholes are now closed.

## Corollary 2: the compressed route is now a genuinely constructive one-primitive gap

What remains is not discovery of an already-landed object. It is positive
construction of one new Wilson-side charged source family / channel.

## What this closes

- one exact nonrealization statement for the remaining compressed-route
  primitive;
- one sharper closure of hidden-bank loopholes on the compressed PF route;
- one cleaner handoff to positive construction.

## What this does not close

- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- a positive global PF selector.

## Why this matters

This note means the compressed route is now fully audited:

- target identified,
- downstream algebra closed,
- hidden-bank loopholes closed.

The remaining work is genuinely constructive.

## Atlas inputs used

- [PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_charged_source_family_current_bank_nonrealization_2026_04_17.py
```
