# Perron-Frobenius Step-2 Charged Source-Family Target

**Date:** 2026-04-17  
**Status:** exact science-only target theorem isolating the remaining constructive primitive on the compressed route  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_charged_source_family_target_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After all current step-2A reductions, is the compressed route still missing a
large reconstruction package, or is one smaller primitive left?

## Bottom line

One smaller primitive is left.

The branch already has:

1. the exact additive source-response principle from the lattice Grassmann
   Gaussian;
2. the exact charged projected-source law `dW_e^H` as the right compressed
   codomain;
3. the exact downstream reconstruction chain from `dW_e^H` to `H_e`, packet
   data, and the triplet channels `(gamma, E1, E2)`.

So the compressed route is **not** blocked by missing downstream reconstruction
algebra.

The remaining constructive primitive is:

- a Wilson-side charged source family / channel whose source responses land on
  the charged projected Hermitian law.

## What is already exact

### 1. The observable/source-response machinery already exists

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact additive scalar generator is
  `W[J] = log |det(D+J)| - log |det D|`;
- source derivatives are exact source responses built from the lattice
  operator.

So the branch already has theorem-grade source-response machinery.

### 2. The compressed codomain is already the right one

From
[PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md):

- `Wilson -> dW_e^H` is the fully typed compressed route;
- once it lands, only the right-sensitive selector remains downstream.

### 3. Downstream reconstruction from `dW_e^H` is already exact

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- `dW_e^H` reconstructs `H_e`;
- on `N_e`, the transport-relevant selected column is already algorithmic.

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md):

- the constructive triplet channels `(gamma, E1, E2)` are exact linear
  functionals of the projected Hermitian response pack.

So once the compressed source law is supplied, the rest is already exact.

### 4. The current bank still lacks the Wilson-side primitive

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the branch still lacks an explicit Wilson-side charged embedding /
  compression object.

From
[PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md):

- that object cannot be obtained by pure support pullback.

So the missing primitive must be genuinely Wilson-side and charged.

## Theorem 1: exact reduction of the compressed-route constructive primitive

Assume the exact observable principle, the exact direct-`dW_e^H` route
reduction theorem, the exact projected-source law derivation theorem, the exact
projected-source triplet sign theorem, and the exact charged-embedding /
support-pullback boundary theorems. Then:

1. theorem-grade source-response machinery is already present;
2. the compressed codomain `dW_e^H` is already identified;
3. downstream reconstruction from `dW_e^H` is already exact;
4. the current bank still lacks the Wilson-side charged embedding/source
   primitive needed to make those responses land on that codomain.

Therefore the remaining constructive primitive on the compressed route is
exactly a Wilson-side charged source family / channel, not more downstream
reconstruction algebra.

## Corollary 1: the next positive construction attempt should target source family, not readout

The next step should be framed as:

- derive a Wilson-side charged source family whose responses produce the
  projected Hermitian law.

It should **not** be framed as:

- invent more `dW_e^H -> H_e` algebra,
- invent more packet readout formulas,
- or invent more `(gamma, E1, E2)` translation formulas.

Those are already done.

## Corollary 2: the compressed route is now a one-primitive construction problem

On the current bank, the compressed route is reduced to:

1. build the Wilson-side charged source family / channel;
2. then use the already exact reconstruction stack.

## What this closes

- one exact identification of the remaining constructive primitive on the
  compressed route;
- one exact separation between missing Wilson-side source family and already
  closed downstream response algebra;
- one cleaner specification of the next positive theorem target.

## What this does not close

- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- a positive global PF selector.

## Why this matters

This note prevents the branch from spending further effort on solved algebra.

The remaining positive work is now sharper than before:

- derive the charged Wilson-side source family / channel,
- then let the exact response/reconstruction stack do the rest.

## Atlas inputs used

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_charged_source_family_target_2026_04_17.py
```
