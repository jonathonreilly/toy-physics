# DM Wilson-to-`dW_e^H` Structured Extension Criterion Theorem

**Date:** 2026-04-18
**Status:** exact current-stack theorem identifying the weakest honest test for
when a generic Wilson Hermitian source family extends to the structured
rank-`3` embedding class
**Script:** `scripts/frontier_dm_wilson_to_dweh_structured_extension_criterion_theorem_2026_04_18.py`

## Question

After clarifying that the adjacent-chain route is only a normal form **inside**
the structured rank-`3` embedding class, what is the actual criterion that
tells us whether a generic Wilson Hermitian source family belongs to that
class at all?

## Bottom line

The right criterion is not another chain ansatz.

It is a **Jordan-Lie extension criterion** on the generic real-linear Hermitian
source map

`Psi : Herm(3) -> Herm(H_W)`.

There is always a unique complex-linear `*`-preserving extension

`Phi(X + iY) := Psi(X) + i Psi(Y)`, with `X, Y in Herm(3)`.

But that extension is a theorem-grade structured rank-`3` Wilson embedding
only if `Psi` satisfies:

1. **injectivity** on `Herm(3)`;
2. **rank-`3` unit image**:
   `rank(Psi(1_3)) = 3`;
3. **Jordan preservation**:
   `Psi(A o B) = Psi(A) o Psi(B)`;
4. **Lie preservation**:
   `Psi([A,B]_L) = [Psi(A), Psi(B)]_L`;

for all `A, B in Herm(3)`, where

- `A o B := (AB + BA)/2`,
- `[A,B]_L := (AB - BA)/(2i)`.

So the true next forcing question is:

- does a candidate Wilson Hermitian source family satisfy the Jordan-Lie
  extension criterion?

If yes, it extends to the structured class and the adjacent-chain normal form
is then without loss. If no, the candidate is outside that class and the chain
route would indeed be too specific for that candidate.

## What is already exact

### 1. The generic current-stack target is only a `9`-channel Hermitian source family

From
[DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md):

- the weakest honest Wilson target is one Hermitian source family with `9`
  real channels;
- that target is dimensionally minimal for arbitrary `Herm(3)` data.

So the generic target does **not** yet carry structured multiplication data.

### 2. The adjacent-chain route is only a normal form inside the structured class

From
[DM_WILSON_TO_DWEH_ADJACENT_CHAIN_NORMAL_FORM_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_ADJACENT_CHAIN_NORMAL_FORM_THEOREM_NOTE_2026-04-18.md):

- once a structured rank-`3` embedding `Phi_e` exists, the adjacent-chain
  path algebra is already without loss;
- but that note explicitly does **not** prove every generic Wilson realization
  extends to such a `Phi_e`.

So the missing theorem is exactly an extension test from generic `Psi` to
structured `Phi_e`.

## Theorem 1: every real-linear Hermitian source family has a unique complex `*`-preserving extension

Let

`Psi : Herm(3) -> Herm(H_W)`

be real-linear.

Then every matrix `Z in Mat_3(C)` has a unique decomposition

`Z = X + iY`, with `X, Y in Herm(3)`,

and therefore determines a unique complex-linear map

`Phi_Psi(Z) := Psi(X) + i Psi(Y)`.

Moreover:

1. `Phi_Psi` extends `Psi`;
2. `Phi_Psi(Z^*) = Phi_Psi(Z)^*`.

### Proof

For any `Z`, set

- `X := (Z + Z^*)/2`,
- `Y := (Z - Z^*)/(2i)`.

Then `X, Y` are Hermitian and `Z = X + iY`. Uniqueness follows because the
Hermitian and skew-Hermitian parts of a complex matrix are unique.

So `Phi_Psi` is well-defined and clearly complex-linear.

If `Z = X + iY`, then `Z^* = X - iY`, hence

`Phi_Psi(Z^*) = Psi(X) - i Psi(Y) = Phi_Psi(Z)^*`

because `Psi(X), Psi(Y)` are Hermitian.

Therefore every generic Hermitian source family has a unique complex
`*`-preserving extension. What is nontrivial is multiplicativity.

## Theorem 2: Jordan-Lie extension criterion for structured rank-`3` embeddings

Let

`Psi : Herm(3) -> Herm(H_W)`

be real-linear, and let `Phi_Psi` be its unique complex `*`-preserving
extension. Then `Phi_Psi` is a theorem-grade structured rank-`3` Wilson
embedding if and only if all of the following hold:

1. `Psi` is injective;
2. `rank(Psi(1_3)) = 3`;
3. for all `A, B in Herm(3)`,
   `Psi(A o B) = Psi(A) o Psi(B)`;
4. for all `A, B in Herm(3)`,
   `Psi([A,B]_L) = [Psi(A), Psi(B)]_L`.

### Proof

`(=>)`.

Assume `Phi_Psi` is a theorem-grade structured rank-`3` Wilson embedding. Then
its restriction `Psi` is injective, and `rank(Psi(1_3)) = rank(Phi_Psi(1_3)) =
3`.

For Hermitian `A, B`,

- `A o B` is Hermitian,
- `[A,B]_L` is Hermitian,
- and
  `AB = A o B + i [A,B]_L`.

Because `Phi_Psi` is multiplicative and `*`-preserving,

`Phi_Psi(A o B) = (Phi_Psi(A) Phi_Psi(B) + Phi_Psi(B) Phi_Psi(A))/2`,

`Phi_Psi([A,B]_L) = (Phi_Psi(A) Phi_Psi(B) - Phi_Psi(B) Phi_Psi(A))/(2i)`.

Restricting back to `Herm(3)` gives the Jordan and Lie identities for `Psi`.

`(<=)`.

Assume the four displayed conditions.

For Hermitian `A, B`,

`AB = A o B + i [A,B]_L`,

so

`Phi_Psi(AB) = Psi(A o B) + i Psi([A,B]_L)`.

Using the Jordan and Lie identities,

`Phi_Psi(AB) = Psi(A) o Psi(B) + i [Psi(A), Psi(B)]_L = Psi(A) Psi(B)`.

Thus `Phi_Psi` is multiplicative on pairs of Hermitian matrices.

Now write arbitrary complex matrices as

- `Z_1 = A + iB`,
- `Z_2 = C + iD`,

with Hermitian `A, B, C, D`.

By complex bilinearity and the already-proved Hermitian multiplicativity,
`Phi_Psi(Z_1 Z_2) = Phi_Psi(Z_1) Phi_Psi(Z_2)`.

So `Phi_Psi` is a complex `*`-homomorphism.

Injectivity of `Psi` implies injectivity of `Phi_Psi`: if
`Phi_Psi(A + iB) = 0`, then taking `*` and adding/subtracting gives
`Psi(A) = Psi(B) = 0`, hence `A = B = 0`.

Finally, `rank(Psi(1_3)) = 3` gives the rank-`3` image unit.

Therefore `Phi_Psi` is exactly the structured rank-`3` embedding sought.

## Corollary 1: finite basis checking is enough

Because the Jordan and Lie products are bilinear over `R`, it is enough to
check the criterion on any real basis of `Herm(3)`.

In particular, on the chain-generated Hermitian basis

- `D_1`, `D_2`, `D_3`,
- `X_12`, `Y_12`,
- `X_23`, `Y_23`,
- `X_13`, `Y_13`,

it is enough to verify the Jordan and Lie identities on basis pairs.

So the extension question is finite and reviewable.

## Corollary 2: this is the real forcing fork

For any candidate Wilson Hermitian source family `Psi`:

- if the criterion holds, then the candidate extends to the structured class,
  and the adjacent-chain route is without loss;
- if the criterion fails, then that candidate does **not** belong to the
  structured class, and any chain-based attack would be too specific for it.

So the next branch point is no longer vague.

It is exactly:

- positive structured extension,

or

- structured-extension obstruction.

## What this closes

- the weakest honest extension test from a generic Wilson Hermitian source
  family to a structured rank-`3` embedding
- the ambiguity about what “forced into the structured class” should mean
- the claim that we need to guess the chain ansatz before checking extension

## What this does not close

- a positive realization of `Psi` on the current stack
- a proof that the current Wilson bank satisfies the extension criterion
- a positive theorem that `dW_W o Phi_chain = dW_e^H`
- the DM microscopic selector law
- the DM flagship lane

## Why this matters

This is the correct next theorem surface.

The over-specificity question is now reduced to a concrete algebraic test, not
to intuition.
