# Perron-Frobenius Step-2 Wilson Local Hermitian Chain-Plane Target

**Date:** 2026-04-18  
**Status:** exact science-only theorem identifying the sharpest local Wilson
constructive primitive with one invariant Hermitian chain-plane embedding on the
physical nearest-neighbor lattice  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_local_hermitian_chain_plane_target_2026_04_18.py`

## Question

After the Wilson compressed route has already been reduced to one minimal local
Hermitian nearest-neighbor `4`-source packet, is that packet only a convenient
coordinate presentation?

Or is there already an exact invariant local object carrying the same content?

## Bottom line

There is already an exact invariant local object.

Let

- `X_12 := E_12 + E_21`,
- `Y_12 := -i E_12 + i E_21`,
- `X_23 := E_23 + E_32`,
- `Y_23 := -i E_23 + i E_32`,

and define the real Hermitian nearest-neighbor chain plane

`V_chain^H := span_R{ X_12, Y_12, X_23, Y_23 } subset Herm(3)`.

Then the remaining Wilson constructive primitive is already exactly equivalent
to:

- one real-linear injective Hermitian source embedding
  `Psi_chain : V_chain^H -> Herm(H_W)`.

So the live Wilson source-side target may now be stated invariantly and
locally as:

- realize the Hermitian chain-plane embedding on one adjacent nearest-neighbor
  two-edge chain of the physical lattice.

The current bank still does **not** realize even that restricted local
embedding.

## What is already exact

### 1. The weaker Wilson source-side target is already `Psi_e`

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- the compressed Wilson response theorem uses only the Hermitian restriction

  `Psi_e : Herm(3) -> Herm(H_W)`,

- not the full complex source algebra `Phi_e`.

### 2. The remaining local constructive primitive is already the Hermitian `4`-packet

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md):

- the remaining Wilson local source primitive is exactly one local Hermitian
  nearest-neighbor `4`-source packet.

### 3. That local packet is already minimal on the physical lattice

From
[PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md](./PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md):

- no honest generic local Hermitian `3`-source shortcut exists on this
  Wilson lane.

So the local packet already has the correct finite size. The only remaining
question is whether it can be written more invariantly.

## Theorem 1: the local Hermitian `4`-source packet is exactly one Hermitian chain-plane embedding

The following are equivalent:

1. theorem-grade realization of one local Hermitian nearest-neighbor
   `4`-source packet on the adjacent two-edge chain;
2. theorem-grade realization of one real-linear injective Hermitian embedding

   `Psi_chain : V_chain^H -> Herm(H_W)`.

### Proof

`(1) => (2)`.

Assume the local Hermitian `4`-source packet has been realized. By definition,
that means there are Hermitian Wilson-side sources

- `S(X_12)`,
- `S(Y_12)`,
- `S(X_23)`,
- `S(Y_23)`,

that are real-linearly independent and attached to the adjacent
nearest-neighbor chain.

Define `Psi_chain` on the displayed basis by

- `Psi_chain(X_12) := S(X_12)`,
- `Psi_chain(Y_12) := S(Y_12)`,
- `Psi_chain(X_23) := S(X_23)`,
- `Psi_chain(Y_23) := S(Y_23)`,

and extend real-linearly to all of `V_chain^H`.

Because the source images are Hermitian, the image lies in `Herm(H_W)`. Because
the four packet elements are real-linearly independent, the map is injective.

So `(1)` gives a real-linear injective Hermitian embedding
`Psi_chain : V_chain^H -> Herm(H_W)`.

`(2) => (1)`.

Assume a real-linear injective Hermitian embedding `Psi_chain` is given.
Evaluate it on the displayed basis of `V_chain^H`. The resulting four Hermitian
Wilson-side sources

- `Psi_chain(X_12)`,
- `Psi_chain(Y_12)`,
- `Psi_chain(X_23)`,
- `Psi_chain(Y_23)`

form one local Hermitian nearest-neighbor `4`-source packet. Injectivity
ensures they are real-linearly independent.

So `(2)` gives theorem-grade realization of the local Hermitian `4`-source
packet.

Therefore the two formulations are exactly equivalent.

## Theorem 2: whenever `Psi_e` exists, the local chain-plane target is exactly its restriction

Assume theorem-grade Hermitian source embedding

`Psi_e : Herm(3) -> Herm(H_W)`.

Then the local Hermitian chain-plane target is the restricted map

`Psi_chain := Psi_e |_(V_chain^H)`.

In particular, any future positive theorem-grade realization of `Psi_e`
automatically realizes the local chain-plane embedding.

### Proof

Because `V_chain^H subset Herm(3)`, the restriction `Psi_e |_(V_chain^H)` is
well-defined and real-linear.

Because `Psi_e` maps Hermitian matrices to Hermitian Wilson-side operators, the
restriction maps `V_chain^H` into `Herm(H_W)`.

Because `Psi_e` is injective, its restriction is injective on `V_chain^H`.

So `Psi_chain := Psi_e |_(V_chain^H)` is exactly the required real-linear
injective Hermitian chain-plane embedding.

## Corollary 1: the sharpest positive Wilson source theorem can now be stated invariantly and locally

The next positive Wilson step may now be phrased as:

- derive one theorem-grade Hermitian chain-plane embedding
  `Psi_chain : V_chain^H -> Herm(H_W)`

on one adjacent nearest-neighbor two-edge chain of the physical lattice.

This is sharper than:

- an abstract charged source family,
- a generic two-edge complex law,
- or a basis-dependent `4`-packet statement without the underlying local
  invariant subspace.

## Corollary 2: the current bank still does **not** realize even the local chain-plane embedding

If the current bank realized `Psi_chain` at theorem grade, then by Theorem 1 it
would realize the local Hermitian nearest-neighbor `4`-source packet.

But the current bank still does **not** realize that local Hermitian
`4`-source packet.

So the current bank still does **not** realize even the restricted local
Hermitian chain-plane embedding.

## What this closes

- exact identification of the minimal local Hermitian Wilson packet with one
  invariant local Hermitian chain-plane embedding
- exact alignment between the abstract weaker Wilson object `Psi_e` and the
  physical nearest-neighbor local target
- exact statement that the current bank still fails even this restricted local
  embedding

## What this does not close

- a positive realization of the local Hermitian chain-plane embedding
- a positive realization of the full Hermitian source embedding `Psi_e`
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the cleanest local invariant Wilson source surface now available.

The live positive Wilson route is no longer best read only as:

- one minimal local Hermitian nearest-neighbor `4`-source packet.

It is now:

- one theorem-grade Hermitian embedding of the physical nearest-neighbor
  chain plane `V_chain^H`.
