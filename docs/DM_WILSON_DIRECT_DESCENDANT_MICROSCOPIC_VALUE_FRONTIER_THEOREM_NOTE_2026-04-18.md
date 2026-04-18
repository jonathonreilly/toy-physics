# DM Wilson Direct-Descendant Microscopic-Value Frontier Theorem

**Date:** 2026-04-18  
**Status:** exact current-`main` frontier theorem clarifying what remains open
on the direct Wilson-descendant route after auditing the local Schur note  
**Script:** `scripts/frontier_dm_wilson_direct_descendant_microscopic_value_frontier_theorem_2026_04_18.py`

## Question

After auditing
[DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_SOURCE_FAMILY_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_SOURCE_FAMILY_THEOREM_NOTE_2026-04-18.md),
what is the strongest honest current-`main` statement about the direct
Wilson-descendant route?

More concretely:

- does the live frontier still include a generic Wilson Hermitian source-family
  / `Psi` search,
- or has the route already reduced further than that?

## Bottom line

It has already reduced further.

The local Schur algebra is real, but it is **conditional downstream algebra**,
not a new Wilson-native bridge on current `main`.

Current `main` already proves:

1. once the full microscopic charge-preserving operator `D` is supplied, the
   chain

   `D -> D_- -> L_e = Schur_{E_e}(D_-) -> dW_e^H -> H_e -> packet -> eta`

   is algorithmic;
2. once `dW_e^H` is supplied, the downstream PMNS / transport chain is already
   algorithmic;
3. current `main` still does **not** contain a theorem-grade Wilson-to-`dW_e^H`
   descendant law or Wilson Hermitian source family under another name.

Therefore the honest remaining direct-descendant frontier is **not**:

- search generically for a `Psi` family,
- or repackage the local Schur algebra as if it were an upstream Wilson
  construction.

It is exactly:

- the actual microscopic value law of `D_-`, equivalently `L_e`,
- together with any Wilson-native support provenance still needed for `E_e`.

That is the real remaining object.

## What is already exact

### 1. The PMNS-assisted DM route is already reduced to microscopic `D`

From
[DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md):

- the remaining smallest science object is the actual microscopic
  charge-preserving operator `D`;
- once `D` is supplied, the exact chain to the near-closing DM value is
  algorithmic.

So the current stack already places the open value problem at microscopic `D`,
not at a generic downstream source family.

### 2. The charged route is already reduced further to `D_-` and `L_e`

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
  charge-`-1` source-response law;
- equivalently the remaining object may be phrased as evaluating the actual
  microscopic charge-`-1` operator `D_-` and its Schur pushforward.

So the direct route is already narrowed from full `D` to the charged block
`D_-`, equivalently `L_e`.

### 3. Once `dW_e^H` is known, the rest is already downstream

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- once `dW_e^H` is known, the selected `N_e` transport column is already
  algorithmic.

So no new theorem is needed at the packet / transport layer.

### 4. Current `main` still does not already realize a Wilson descendant law

From
[DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md):

- current `main` does **not** already contain
  a Wilson-to-`dW_e^H` descendant theorem,
- nor a Wilson Hermitian source family realizing that codomain.

So any note that still assumes the microscopic charged block and support split
has not yet supplied the missing current-bank Wilson object.

## Where the local Schur note actually sits

The local Schur note assumes:

1. an invertible charge-preserving microscopic operator
   `D = D_0 ⊕ D_- ⊕ D_+`;
2. a charged-support split `E_- = E_e ⊕ E_r` with `dim E_e = 3`;
3. then defines `Phi_e(Z) = I_e Z I_e^*` from that supplied support inclusion.

Under those hypotheses, the algebra is correct:

- the embedded family is structured;
- determinant responses reduce to `L_e`;
- the first variation is `Re Tr(L_e^(-1) X)`.

But this does **not** advance the current-`main` frontier unless it also
derives:

- the actual values of `D_-` or `L_e`,
- or the Wilson-native provenance of the charged support inclusion.

So the safe reading is:

- **conditional local unpacking of the already-known microscopic reduction**,

not:

- a new upstream Wilson-native descendant theorem on current `main`.

## Theorem 1: conditional local Schur algebra is downstream of the already-closed microscopic reduction

Assume:

1. the exact full microscopic reduction theorem;
2. the exact charged source-response reduction theorem;
3. the exact projected-source-law derivation theorem;
4. the exact current-bank boundary excluding an existing Wilson-side descendant
   law;
5. a supplied microscopic charge-preserving operator `D` and supplied charged
   support `E_e`.

Then the canonical embedded family `Phi_e(Z) = I_e Z I_e^*` and its
first-variation law on `dW_e^H` are downstream algebraic consequences of the
already-closed microscopic chain

`D -> D_- -> L_e -> dW_e^H -> H_e`.

Therefore that conditional local Schur algebra does not itself supply the
missing Wilson-native current-bank object.

### Reason

Once `D` is supplied, `D_-` is extracted canonically.
Once `D_-` and `E_e` are supplied, `L_e = Schur_{E_e}(D_-)` is fixed.
Once `L_e` is fixed, the Hermitian response law

`X -> Re Tr(L_e^(-1) X)`

is fixed, hence `H_e`, the packet, and the transport readout are fixed.

So all content beyond supplied `D` and `E_e` is already downstream algebra.

## Theorem 2: the honest direct-descendant frontier is microscopic value law plus support provenance

On current `main`, after the above reductions, the remaining direct
Wilson-descendant science object is exactly:

1. the actual microscopic value law of `D_-`, equivalently `L_e`;
2. the Wilson-native provenance of the charged support `E_e` if that support is
   meant to come from the Wilson side rather than be imported from the PMNS
   interface;
3. after that, the already-isolated right-sensitive selector law on the
   descended family.

No weaker target is honest anymore.

In particular, it is not enough to:

- posit a generic `Psi`,
- posit a generic `9`-probe family,
- or rephrase the conditional Schur reduction under Wilson language,

unless that work actually derives the missing microscopic values or support
provenance.

## Corollary 1: generic `Psi` search is no longer the right bottleneck

Because the conditional local Schur family is automatic once `D_- / L_e` and
`E_e` are supplied, the open problem is not “find some `Psi`.”

The open problem is:

- derive the actual microscopic charged data from `Cl(3)` on `Z^3`.

## Corollary 2: the next honest positive theorem should target `D_-` or `L_e` directly

The best positive direct-descendant target is therefore:

- an axiom-native value law for `D_-`,
- or directly for `L_e = Schur_{E_e}(D_-)`,
- together with any needed Wilson-native support-identification theorem for
  `E_e`.

That is the tightest direct route that still moves the science.

## What this closes

- the target-shape question after auditing the local Schur note
- the confusion between conditional local Schur algebra and a new upstream
  Wilson-native bridge
- the idea that the frontier is still a generic Wilson Hermitian source-family
  search

## What this does not close

- an actual value law for `D_-` or `L_e`
- Wilson-native support provenance for `E_e`
- the right-sensitive selector law on the descended family
- the DM flagship gate
