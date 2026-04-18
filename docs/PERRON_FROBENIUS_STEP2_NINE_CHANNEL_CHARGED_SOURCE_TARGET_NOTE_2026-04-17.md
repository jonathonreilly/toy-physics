# Perron-Frobenius Step-2 Nine-Channel Charged Source Target

**Date:** 2026-04-17  
**Status:** exact science-only target theorem sharpening the compressed
Wilson-side primitive to a finite charged Hermitian response family  
**Script:** `scripts/frontier_perron_frobenius_step2_nine_channel_charged_source_target_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Question

If the compressed step-2 route is blocked by one Wilson-side charged source
family / channel, can that primitive be typed more concretely than “some new
cross-sector operator”?

## Bottom line

Yes.

On the compressed route, the minimal constructive Wilson-side target can be
taken as a finite **nine-channel charged Hermitian source family** on the
charged support `E_e`.

Why nine channels?

- `dW_e^H` is the charged projected Hermitian source law;
- `dW_e^H` reconstructs `H_e`;
- a `3 x 3` Hermitian block is determined exactly by nine real linear
  responses on the standard Hermitian basis.

So the compressed step-2A primitive is not an unconstrained operator search.
It may be posed as:

- derive a Wilson-side charged source family whose responses realize the nine
  Hermitian basis components needed to recover `dW_e^H` on `E_e`.

## What is already exact

### 1. The compressed route is already the clean first PMNS-side codomain

From
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md):

- the compressed route is blocked by one Wilson-side charged source family /
  channel primitive rather than by missing downstream reconstruction algebra.

From
[PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md):

- `Wilson -> dW_e^H` is already the clean fully typed compressed route.

### 2. `dW_e^H` already carries the right finite reconstruction target

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- for a `3 x 3` Hermitian block, the nine real linear responses on the
  standard Hermitian basis determine `H_e` exactly;
- once `dW_e^H` is known, `H_e`, the `N_e` packet, and the selected transport
  column are downstream algorithmic.

So the compressed route already identifies one finite sufficient response pack.

### 3. The observable principle already supplies the right response grammar

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- theorem-grade source-response machinery already exists on the Wilson side as
  exact derivatives of the lattice source generator.

So the remaining issue is no longer whether response grammar exists. It is
whether one can realize the **charged Hermitian response family** needed by
the compressed codomain.

### 4. The missing primitive is still Wilson-side

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the branch still lacks an explicit Wilson-side charged
  embedding/compression realization.

So the finite response family must be Wilson-side and charged, not another
downstream PMNS reformulation.

## Theorem 1: exact finite target refinement of the compressed primitive

Assume the exact compressed-route target theorem, the exact direct-`dW_e^H`
route reduction theorem, the exact projected-source-law derivation theorem,
the exact observable principle, and the exact charged-embedding boundary
theorem.

Then:

1. the compressed route is already reduced to one Wilson-side charged source
   family / channel primitive;
2. `dW_e^H` is the exact compressed codomain;
3. recovering `dW_e^H` is finitely equivalent to recovering the nine real
   Hermitian basis responses that determine `H_e`;
4. those responses belong on the Wilson side because the missing primitive is
   still the Wilson-side charged embedding/source realization.

Therefore the minimal constructive Wilson-side target may be posed as a
finite nine-channel charged Hermitian source family on `E_e`, rather than as
an unconstrained cross-sector operator search.

## Corollary 1: the next positive compressed-route attempt can be finite from the start

The next positive construction attempt on the compressed route may be framed
as:

- derive nine Wilson-side charged response channels realizing the Hermitian
  basis data of `dW_e^H`.

It does **not** need to start as:

- a completely open-ended full `D_-` operator theorem.

## Corollary 2: this does not remove the need for a Wilson-side embedding law

This note does **not** bypass the charged-embedding problem.

It only sharpens the target once that Wilson-side construction is attacked:

- the minimal sufficient compressed response family is finite and explicit.

## What this closes

- one exact refinement of the compressed step-2 primitive from “some source
  family” to a finite nine-channel Hermitian response family
- one exact reason that the compressed route can be attacked as a finite
  construction problem
- one exact separation between finite response-target shape and the still-open
  Wilson-side embedding realization

## What this does not close

- a positive Wilson-to-`dW_e^H` theorem
- a positive Wilson-to-`D_-` theorem
- the Wilson-side charged embedding/compression realization itself
- a nontrivial sole-axiom PMNS current law
- positive global PF closure

## Why this matters

This is the first constructive sharpening of the compressed PMNS route beyond
pure boundary language.

The branch now knows not only that the compressed primitive is smaller than the
strong route, but also that it can be posed as a finite charged Hermitian
response family rather than as an unconstrained operator hunt.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_nine_channel_charged_source_target_2026_04_17.py
```
