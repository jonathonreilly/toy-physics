# DM Wilson Direct Descendant Local Schur Source-Family Theorem

**Date:** 2026-04-18  
**Status:** exact positive direct-descendant theorem showing the first honest
Wilson-to-`dW_e^H` route is already local to the charged Schur block and does
not require full global Wilson-parent correctness  
**Script:** `scripts/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_SOURCE_FAMILY_THEOREM_2026_04_18.py`

## Question

After the Wilson-parent audit, what is the strongest honest positive theorem
we can still prove for the direct-descendant route without assuming the full
Wilson parent stack is already correct?

More concretely:

- can the Wilson-side Hermitian source family / `Psi` route into `dW_e^H`
  already be derived from the exact observable principle plus the charged
  microscopic block,
- or does that still depend on the unresolved global parent-identification
  story?

## Bottom line

Yes.

The direct-descendant route is already exact at the **local charged Schur
level**.

Assume only:

1. an invertible charge-preserving microscopic operator
   `D = D_0 ⊕ D_- ⊕ D_+`;
2. the charged-support split `E_- = E_e ⊕ E_r` with `dim E_e = 3`;
3. the observable principle
   `W[J] = log |det(D+J)| - log |det D|`.

Then the canonical support embedding

`Phi_e(Z) := I_e Z I_e^*`

already gives a theorem-grade rank-`3` Wilson Hermitian source family on the
charged support, and its first variations satisfy

`(d/dt) W[t Phi_e(X)] |_(t=0) = Re Tr(L_e^(-1) X) = Tr(H_e X)`

for every Hermitian `X`, where

- `L_e = Schur_{E_e}(D_-)`,
- `H_e = (L_e^(-1) + (L_e^(-1))^*) / 2`.

So the positive Wilson-to-`dW_e^H` descendant law is already local and exact
once the charged microscopic block is supplied. It does **not** require the
stronger assumption that the whole global Wilson-parent story has already been
proved correct.

What remains open is narrower:

- evaluate the actual microscopic charged Schur block `L_e`,
- verify that the intended Wilson stack supplies the right `D_-` and support
  `E_e`,
- then attack the right-sensitive selector law on the descended family.

## What is already exact

### 1. The observable principle already fixes the source-response engine

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact source generator is
  `W[J] = log |det(D+J)| - log |det D|`;
- its first variations are exact source responses of the microscopic operator.

So the direct route should be phrased in terms of determinant response, not a
new imported parent formalism.

### 2. The DM lane already fixes the right compressed codomain

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
and
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
  charge-`-1` source-response law;
- once `dW_e^H` is known, the downstream `H_e -> |U_e|^2^T ->` selected DM
  transport column chain is already algorithmic.

So the direct-descendant route only needs to reach `dW_e^H`, not the full
global parent.

### 3. The audit already showed why the global parent should not be assumed

From
[DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md](./DM_WILSON_PARENT_CORRECTNESS_AUDIT_NOTE_2026-04-18.md):

- the gauge-side transfer parent and the determinant-weighted retained parent
  are not yet theorem-grade identified as one object;
- the current stack does not yet fix unique framework-point parent data;
- the safe positive continuation is therefore the direct-descendant route.

So the direct theorem has to bypass that unresolved global identification.

## Setup

Write the charge-`-1` block on the split support `E_- = E_e ⊕ E_r` as

`D_- = [[A, B], [C, F]]`,

with `A : E_e -> E_e`, `F : E_r -> E_r`, and assume `F` is invertible so the
charged Schur complement exists:

`L_e := A - B F^(-1) C = Schur_{E_e}(D_-)`.

Let

`I_e : C^3 -> E_-`

be the isometric support inclusion onto `E_e`.

For every `Z in Mat_3(C)`, define the Wilson-side embedded source

`Phi_e(Z) := I_e Z I_e^* in End(E_-)`.

On the full microscopic space, the corresponding source insertion is

`J_Z := 0_(E_0) ⊕ Phi_e(Z) ⊕ 0_(E_+)`.

## Theorem 1: the charged support embedding is already a structured rank-`3` source family

The map

`Phi_e : Mat_3(C) -> End(E_-)`

is a unital `*`-monomorphism onto the rank-`3` support algebra on `E_e`.

Equivalently, its Hermitian restriction

`Psi_e := Phi_e |_(Herm(3))`

is already a theorem-grade Wilson Hermitian source family satisfying the
structured extension criterion.

### Proof

Because `I_e^* I_e = 1_3`,

`Phi_e(Z_1) Phi_e(Z_2)
 = I_e Z_1 I_e^* I_e Z_2 I_e^*
 = I_e Z_1 Z_2 I_e^*
 = Phi_e(Z_1 Z_2)`.

Also,

`Phi_e(Z^*) = I_e Z^* I_e^* = Phi_e(Z)^*`,

so `Phi_e` is a `*`-homomorphism.

If `Phi_e(Z) = 0`, then

`0 = I_e^* Phi_e(Z) I_e = Z`,

so `Phi_e` is injective.

Finally,

`Phi_e(1_3) = I_e I_e^* = P_e`,

the projector onto `E_e`, hence `rank(P_e) = 3`.

So `Phi_e` is exactly a structured rank-`3` embedding, and `Psi_e` is its
canonical Hermitian source family.

## Theorem 2: exact direct-descendant Schur reduction of the determinant response

For every `Z in Mat_3(C)` and every scalar `t` in the common invertibility
domain,

`det(D + t J_Z) / det(D) = det(L_e + t Z) / det(L_e)`.

In particular, for Hermitian `X in Herm(3)`,

`W[t J_X] = log |det(L_e + t X)| - log |det(L_e)|`.

### Proof

Because `D = D_0 ⊕ D_- ⊕ D_+`,

`det(D + t J_Z)
 = det(D_0) det(D_+)
   det([[A + t Z, B], [C, F]])`.

Since `F` is invertible, block determinant factorization gives

`det([[A + t Z, B], [C, F]])
 = det(F) det((A + t Z) - B F^(-1) C)
 = det(F) det(L_e + t Z)`.

Likewise,

`det(D) = det(D_0) det(D_+) det(F) det(L_e)`.

Dividing cancels the ambient factors and leaves

`det(D + t J_Z) / det(D) = det(L_e + t Z) / det(L_e)`.

Taking `log |.|` gives the displayed formula for `W[t J_X]`.

## Theorem 3: the first variation is exactly `dW_e^H`

For Hermitian `X in Herm(3)`,

`(d/dt) W[t J_X] |_(t=0) = Re Tr(L_e^(-1) X)`.

If

`H_e := (L_e^(-1) + (L_e^(-1))^*) / 2`,

then equivalently

`(d/dt) W[t J_X] |_(t=0) = Tr(H_e X)`.

So the descended observable law on the canonical embedded family is exactly
the charged projected Hermitian law `dW_e^H`.

### Proof

By Theorem 2,

`W[t J_X] = log |det(L_e + t X)| - log |det(L_e)|`.

Differentiating at `t = 0` and using the exact logarithmic determinant
derivative,

`(d/dt) log det(L_e + t X) |_(t=0) = Tr(L_e^(-1) X)`.

Because `W` uses `log |det|`, the derivative is the real part:

`(d/dt) W[t J_X] |_(t=0) = Re Tr(L_e^(-1) X)`.

For Hermitian `X`,

`Re Tr(L_e^(-1) X)
 = Tr(((L_e^(-1) + (L_e^(-1))^*) / 2) X)
 = Tr(H_e X)`.

This is exactly the `3 x 3` Hermitian response law on the charged support.

## Corollary 1: the direct-descendant route is local to `L_e`

If two different ambient microscopic completions

- have the same charged support `E_e`,
- have the same charged Schur complement `L_e`,
- but differ elsewhere in `D_0`, `D_+`, or the unresolved completion of
  `D_-`,

then they induce exactly the same normalized source-response law on the
embedded family `Phi_e(Herm(3))`.

So the first Wilson-to-`dW_e^H` theorem is local to the charged Schur block.
It is not load-bearing on full global parent correctness.

## Corollary 2: the structured extension question is automatically resolved locally

Because `Phi_e` is already a unital rank-`3` `*`-monomorphism, its Hermitian
restriction automatically satisfies:

- injectivity,
- rank-`3` unit image,
- Jordan preservation,
- Lie preservation.

So the direct-descendant family lies inside the structured class without any
extra chain ansatz or auxiliary forcing theorem.

## Corollary 3: nine Hermitian probes reconstruct `H_e` exactly

On any real basis `B_1, ..., B_9` of `Herm(3)`, the response values

`r_a := (d/dt) W[t J_(B_a)] |_(t=0) = Tr(H_e B_a)`

determine `H_e` exactly because `dim_R Herm(3) = 9`.

So once the actual local Schur block `L_e` is known, the whole charged
Hermitian law is reconstructible by a finite Wilson-side probe family.

## Positive consequence

This is the strongest honest positive direct-descendant statement available
without assuming full Wilson-parent correctness:

- the first Wilson-to-`dW_e^H` bridge is already exact and local,
- the canonical source family is already structured,
- ambient parent uncertainty only matters through the actual value of `L_e`,
  not through a separate global parent-identification theorem.

So the next positive task is now sharper:

- derive or evaluate the actual microscopic charged Schur block `L_e`,
  or equivalently the actual `D_-` data on `E_e ⊕ E_r`,
- then use the exact descended family to attack the right-sensitive selector.

## What this closes

- one exact positive Wilson Hermitian source-family route into `dW_e^H`
  without assuming full global Wilson-parent correctness;
- one exact determinant-response identity showing the direct-descendant route
  depends only on the charged Schur block `L_e`;
- one exact reason the structured class is already locally realized by the
  support inclusion `I_e`.

## What this does not close

- the actual microscopic evaluation of `D_-` or `L_e` from `Cl(3)` on `Z^3`;
- a proof that the currently intended Wilson stack supplies the correct charge
  split and charged support data;
- the right-sensitive selector law on the descended family;
- the DM flagship gate.

## Why this matters

This note changes what “positive Wilson progress” should mean after the audit.

It is no longer necessary to pretend the whole Wilson parent is already proved
correct before any descendant theorem can be written. The first honest
descendant theorem is already available at the local charged Schur level.

That means the remaining Wilson-native science is now concentrated on one real
object:

- the actual microscopic charged Schur block `L_e`.
