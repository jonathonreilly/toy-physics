# DM Wilson-to-`dW_e^H` Structured Model Realization Theorem

**Date:** 2026-04-18  
**Status:** exact constructive theorem showing the structured Wilson response
class is positively realizable for arbitrary Hermitian target `H_e`, even
though the Wilson-native bridge from the current bank remains open  
**Script:** `scripts/frontier_dm_wilson_to_dweh_structured_model_realization_theorem_2026_04_18.py`

## Question

Do we at least have a genuine **positive** realization of the structured
Wilson-to-`dW_e^H` class, or are we still only proving obstructions and target
equivalences?

## Bottom line

We do have a genuine positive realization, at the structured model level.

For any Hermitian target

`H_e in Herm(3)`

any nonzero real padding parameter `lambda`, and any unitary `U in U(3)`,
define on the parent space

`H_W := C^3`

the model data

- `I_e := U`,
- `Phi_e(X) := U X U^*`,
- `D_model^(-1) := U (H_e + i lambda 1_3) U^*`.

Then:

1. `Phi_e` is a theorem-grade rank-`3` structured embedding;
2. `D_model` is invertible because `lambda != 0`;
3. for every `X in Herm(3)`,

   `Re Tr(D_model^(-1) Phi_e(X)) = Tr(H_e X)`;

4. therefore the model observable responses realize exactly the charged
   projected Hermitian law

   `dW_e^H(X) = Re Tr(X H_e)`.

So the structured class is not merely logically consistent. It is explicitly
nonempty and constructive.

What remains open is not algebraic realizability. It is the **Wilson-native
realization problem**:

- derive such a structured realization from the actual current-bank Wilson
  parent rather than by hand-building `D_model`.

## What is already exact

### 1. The generic and structured targets are already fixed

From
[DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md):

- the weakest generic target is one `9`-channel Hermitian source family for
  `dW_e^H`.

From
[DM_WILSON_TO_DWEH_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md):

- the structured route is exactly:
  - one local generator layer `Phi_chain`,
  - plus one descended-response identity into `dW_e^H`.

So the branch already knows both the generic and structured targets.

### 2. The extension criterion already tells us what structured realization means

From
[DM_WILSON_TO_DWEH_STRUCTURED_EXTENSION_CRITERION_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_STRUCTURED_EXTENSION_CRITERION_THEOREM_NOTE_2026-04-18.md):

- a generic Hermitian source family extends to the structured rank-`3` class
  exactly when it satisfies injectivity, rank-`3` unit image, and Jordan-Lie
  preservation.

So the next positive question is whether that class is constructively nonempty.

## Theorem 1: explicit structured model realization for arbitrary `H_e`

Let `H_e in Herm(3)`, let `lambda` be any nonzero real number, and let
`U in U(3)`. Define:

- `H_W := C^3`,
- `I_e := U : C^3 -> H_W`,
- `Phi_e(X) := U X U^*`,
- `Psi_e := Phi_e |_(Herm(3))`,
- `D_model^(-1) := U (H_e + i lambda 1_3) U^*`.

Then:

1. `Phi_e` is a unital `*`-monomorphism
   `Mat_3(C) -> End(H_W)`;
2. `rank(Phi_e(1_3)) = 3`;
3. `Psi_e` satisfies the structured extension criterion;
4. the Hermitian resolvent compression is exactly

   `(I_e^* D_model^(-1) I_e + (I_e^* D_model^(-1) I_e)^*) / 2 = H_e`;

5. equivalently, for every `X in Herm(3)`,

   `Re Tr(D_model^(-1) Phi_e(X)) = Tr(H_e X)`.

### Proof

Items (1) and (2) are immediate because conjugation by a unitary is a unital
`*`-monomorphism of `Mat_3(C)` into `End(C^3)`, and

`Phi_e(1_3) = U 1_3 U^* = 1_3`

has rank `3`.

Since `Phi_e` is a `*`-monomorphism, its Hermitian restriction `Psi_e`
automatically satisfies injectivity, Jordan preservation, and Lie
preservation. Also

`Psi_e(1_3) = 1_3`

has rank `3`. So item (3) follows from the structured extension criterion.

Because `lambda != 0`, every eigenvalue of

`H_e + i lambda 1_3`

has nonzero imaginary part, so `D_model^(-1)` is invertible and `D_model`
exists.

Now

`I_e^* D_model^(-1) I_e = U^* U (H_e + i lambda 1_3) U^* U = H_e + i lambda 1_3`,

so its Hermitian part is exactly `H_e`. This gives item (4).

For Hermitian `X`,

`Re Tr(D_model^(-1) Phi_e(X))
 = Re Tr(U (H_e + i lambda 1_3) U^* U X U^*)
 = Re Tr((H_e + i lambda 1_3) X)
 = Tr(H_e X)`,

because `Tr(H_e X)` is real and `Tr(i lambda X)` is purely imaginary.

So item (5) holds, which is exactly the model realization of `dW_e^H`.

## Corollary 1: the structured class is explicitly nonempty

The positive structured Wilson-response class exists for every target
`H_e in Herm(3)`.

The special case `U = 1_3` gives the simplest canonical model.

So the current branch is not blocked by hidden inconsistency of the structured
class itself.

## Corollary 2: adjacent-chain normal form is positively inhabited too

Because `Phi_e` exists in the model realization, the adjacent-chain normal-form
theorem applies. So inside the model realization one may equivalently work
with:

- `Phi_chain`,
- the chain-generated Hermitian basis,
- and the descended-response identity checked on that basis.

So the local chain route is not only formally admissible. It is positively
inhabited inside the structured model class.

## Corollary 3: the remaining open problem is Wilson-native realization, not model existence

This theorem does **not** derive `D_model` from the current-bank Wilson parent.

So it does **not** close:

- the actual Wilson-to-`dW_e^H` bridge from the axiom,
- or the charged embedding/compression realization on the current bank.

What it does close is the weaker question:

- is the structured class itself constructively realizable at all?

The answer is yes.

## What this closes

- one explicit positive realization of the full structured response class for
  arbitrary target `H_e`
- one proof that the structured extension criterion is constructive, not merely
  a consistency filter
- one positive habitation result for the adjacent-chain normal form

## What this does not close

- a Wilson-native derivation of `I_e`, `Phi_e`, or `D_model` from the current
  bank
- a positive theorem that the current Wilson parent realizes this model class
- the right-sensitive selector law on `dW_e^H`
- the DM flagship gate

## Why this matters

This is the cleanest positive result available right now.

The branch no longer has to say only:

- “if a structured realization existed, here is how it would behave.”

It can now say:

- “the structured class is explicitly realizable for arbitrary `H_e`; the
  remaining problem is to realize it from the actual Wilson parent.”
