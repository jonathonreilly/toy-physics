# Perron-Frobenius Step-2 Wilson Compressed-Resolvent Block Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem collapsing theorem-grade Wilson
matrix-source realization together with the Hermitian resolvent-compression
identity to one invariant rank-3 Wilson compressed-resolvent block law, and
carrying the matching sharper current-bank no-go  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_compressed_resolvent_block_target_2026_04_17.py`

## Question

After the Wilson compressed route has already been sharpened to

- the invariant rank-3 Wilson matrix-source embedding
  `Phi_e : Mat_3(C) -> End(H_W)`,
- the weaker Hermitian source embedding `Psi_e : Herm(3) -> Herm(H_W)`,
- and the single operator identity
  `H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`,

is the strongest honest next theorem pair still best written as:

- realize `Phi_e` or equivalently `I_e / P_e`,
- and separately prove `H_e^(cand) = H_e`?

Or can the whole Wilson-side target be collapsed one level further to a single
invariant compression law on the parent Wilson resolvent itself?

## Bottom line

It collapses one level further.

Define the Hermitian Wilson resolvent

`S_W := (D^(-1) + (D^(-1))^*) / 2`.

Then the theorem-grade pair

- a rank-3 Wilson matrix-source embedding `Phi_e`, equivalently `I_e / P_e`,
- and the Hermitian resolvent-compression identity `H_e^(cand) = H_e`,

is exactly equivalent to one invariant rank-3 Wilson compressed-resolvent
block law:

- there exists a rank-3 orthogonal projector `P_e` on `H_W` such that the
  compressed Hermitian Wilson resolvent block

  `P_e S_W P_e |_(Ran(P_e))`

  is unitarily equivalent to the charged Hermitian target `H_e`.

Equivalently, after choosing an isometry `I_e : C^3 -> H_W` with

`P_e = I_e I_e^*`,

the whole theorem pair is just

`P_e S_W P_e = I_e H_e I_e^*`.

So the strongest honest next Wilson compressed-route theorem surface is now no
longer two separate items. It is one invariant rank-3 Wilson compressed block
identity.

That is cleaner under review because it removes the remaining source-path and
coordinate rhetoric. Any future positive Wilson compressed-route theorem must
actually exhibit a rank-3 Wilson support whose Hermitian resolvent block is
the charged target.

The current exact bank still does **not** realize even that sharper object.
It still lacks:

- theorem-grade `I_e / P_e`,
- theorem-grade `Phi_e`,
- theorem-grade `Psi_e`,
- and therefore theorem-grade rank-3 Wilson compressed-resolvent block law.

So this note is both:

- one sharper positive target theorem surface,
- and one sharper invariant current-bank no-go.

## What is already exact

### 1. The Wilson primitive is already packaged as `Phi_e`, equivalently `I_e / P_e`

From
[PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- theorem-grade `I_e / P_e` is exactly equivalent to theorem-grade rank-3
  Wilson matrix-source embedding `Phi_e`,
- with

  `Phi_e(X) = I_e X I_e^*`,

  `Phi_e(1_3) = P_e`.

So the missing Wilson-side realization class is already exact.

### 2. The response theorem is already equivalent to one Hermitian resolvent-compression identity

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md):

- once `I_e` exists, the full explicit-response family is equivalent to

  `H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`.

So the live Wilson theorem pair is already:

- realize `I_e / P_e`,
- prove that the Hermitian compressed resolvent equals `H_e`.

### 3. The compressed theorem already uses only the Hermitian source plane

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- the compressed response theorem depends only on the Hermitian restriction
  `Psi_e`,
- but the current bank still does **not** realize even theorem-grade `Psi_e`.

So the remaining target may safely be sharpened on the Hermitian compressed
Wilson side without losing any live theorem content.

### 4. The current bank still lacks the rank-3 Wilson support itself

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md),
[PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md),
and
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current bank still lacks theorem-grade `I_e / P_e`,
- pure support pullback does not produce that object,
- and the compressed Wilson-side source family is still unrealized.

So the sharpened compressed-resolvent block law is not already hidden on the
current bank either.

## Theorem 1: `Phi_e` plus `H_e^(cand) = H_e` is equivalent to one invariant Wilson compressed-resolvent block law

Let

`S_W := (D^(-1) + (D^(-1))^*) / 2`.

Then the following are equivalent:

1. there exists a theorem-grade rank-3 Wilson matrix-source embedding
   `Phi_e : Mat_3(C) -> End(H_W)`, equivalently an isometry
   `I_e : C^3 -> H_W` and projector `P_e = I_e I_e^*`, such that

   `H_e^(cand) := (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`;

2. there exists an isometry `I_e : C^3 -> H_W` with `P_e = I_e I_e^*` such
   that

   `P_e S_W P_e = I_e H_e I_e^*`;

3. there exists a rank-3 orthogonal projector `P_e` such that the compressed
   Hermitian Wilson resolvent block

   `P_e S_W P_e |_(Ran(P_e))`

   is unitarily equivalent to `H_e`.

### Proof

`(1) => (2)`.

Assume `I_e` exists and `H_e^(cand) = H_e`.
Because `P_e = I_e I_e^*` and `I_e^* I_e = 1_3`,

`P_e S_W P_e = I_e (I_e^* S_W I_e) I_e^*`.

But

`I_e^* S_W I_e = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e^(cand)`.

So

`P_e S_W P_e = I_e H_e^(cand) I_e^* = I_e H_e I_e^*`.

`(2) => (3)`.

The map `I_e : C^3 -> Ran(P_e)` is unitary onto `Ran(P_e)`.
So the identity

`P_e S_W P_e = I_e H_e I_e^*`

says exactly that the compressed operator on `Ran(P_e)` is unitarily
equivalent to `H_e`.

`(3) => (1)`.

Assume `P_e S_W P_e |_(Ran(P_e))` is unitarily equivalent to `H_e`.
Choose a unitary `I_e : C^3 -> Ran(P_e)` implementing that equivalence.
Then `P_e = I_e I_e^*`, and define

`Phi_e(X) := I_e X I_e^*`.

By the Wilson matrix-source embedding theorem, this is a theorem-grade rank-3
Wilson matrix-source embedding.

Also the implemented unitary equivalence gives

`P_e S_W P_e = I_e H_e I_e^*`.

Compressing by `I_e^*` and `I_e` yields

`I_e^* S_W I_e = H_e`.

But by definition of `S_W`,

`I_e^* S_W I_e = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e^(cand)`.

So `H_e^(cand) = H_e`.

Thus all three statements are equivalent.

## Corollary 1: the strongest honest next Wilson compressed-route theorem surface is one projector-compression law

The branch may now state the Wilson compressed frontier as:

- realize a rank-3 orthogonal projector `P_e`,
- and prove

  `P_e ((D^(-1) + (D^(-1))^*) / 2) P_e |_(Ran(P_e)) ~= H_e`,

  equivalently

  `P_e S_W P_e = I_e H_e I_e^*`.

That is stronger and cleaner than stating separately:

- realize `Phi_e`,
- prove `H_e^(cand) = H_e`.

Those are exactly the coordinate/source-algebra form of the same Wilson block
law.

## Corollary 2: once the Wilson block law lands, the source-embedding data follow canonically

As soon as a rank-3 Wilson projector `P_e` with the compressed-resolvent block
law is realized:

- choose any isometry `I_e : C^3 -> Ran(P_e)`,
- define `Phi_e(X) = I_e X I_e^*`,
- and recover the compressed response identity

  `(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`

  for every `X in Herm(3)`.

So the invariant Wilson block law is not weaker than the current theorem pair.
It is exactly the same theorem pair in sharper form.

## Theorem 2: the current bank still does not realize even that invariant Wilson block law

Assume the exact charged-embedding boundary theorem, the exact charged-support
pullback boundary theorem, the exact charged-source-family current-bank
nonrealization theorem, the exact Wilson matrix-source embedding target
theorem, and the exact Hermitian-source / resolvent-compression target
theorems.

Then the current exact bank still does **not** realize:

1. a theorem-grade rank-3 Wilson projector `P_e`;
2. a theorem-grade rank-3 Wilson matrix-source embedding `Phi_e`;
3. even the weaker Hermitian source embedding `Psi_e`;
4. therefore any rank-3 Wilson compressed Hermitian resolvent block
   unitarily equivalent to `H_e`.

Therefore the current exact bank still does **not** instantiate the sharper
projector-compression law

`P_e S_W P_e |_(Ran(P_e)) ~= H_e`.

### Proof

By the charged-embedding boundary theorem, the current bank still lacks the
Wilson-side charged embedding/compression object `I_e / P_e`.

By the charged-support pullback boundary theorem, that object cannot be
obtained by pure support pullback from the current support bank.

By the charged-source-family current-bank nonrealization theorem, the current
bank still does not realize the Wilson-side compressed source family/channel
primitive.

By the Wilson matrix-source embedding target theorem and the Hermitian-source
target theorem, lack of theorem-grade `I_e / P_e` means lack of theorem-grade
`Phi_e` and even lack of theorem-grade `Psi_e`.

But by Theorem 1 above, realization of the invariant Wilson block law is
equivalent to realization of theorem-grade `Phi_e` together with
`H_e^(cand) = H_e`.

So the current bank does not realize the invariant Wilson compressed-resolvent
block law either.

## What this closes

- one exact collapse of the live Wilson theorem pair to one invariant rank-3
  projector-compression law on the Hermitian Wilson resolvent;
- one exact statement that theorem-grade `Phi_e` and `H_e^(cand) = H_e` are
  only the source-algebra presentation of that block law;
- one sharper invariant no-go: the current bank still does not realize even
  that block law.

## What this does not close

- a positive theorem-grade realization of `P_e`;
- a positive theorem-grade realization of `Phi_e`;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- a positive global PF selector.

## Why this matters

This is the cleanest Wilson-side statement on the compressed route so far.

The branch no longer has to say only:

- realize `Phi_e`,
- prove `H_e^(cand) = H_e`.

It can now say the exact next theorem is:

- realize a rank-3 Wilson support whose compressed Hermitian resolvent block
  is the charged target `H_e`.

That is the sharpest honest theorem surface on the Wilson compressed-route
front now available.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_wilson_compressed_resolvent_block_target_2026_04_17.py
```
