# Perron-Frobenius Step-2 Wilson Matrix-Source Embedding Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem sharpening the missing Wilson-side
`I_e / P_e` primitive to an equivalent rank-3 matrix-source embedding and
closing the sharper current-bank no-go on that invariant form  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_matrix_source_embedding_target_2026_04_17.py`

## Question

After the compressed-route frontier has already been sharpened to the single
Hermitian resolvent-compression identity

`H_e^(cand) = (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`,

is the right missing Wilson-side object still best stated as:

- an isometry `I_e : C^3 -> H_W`, or
- a rank-3 projector `P_e = I_e I_e^*`?

Or can the same frontier be stated more invariantly as one operator-algebra
object on the Wilson source side?

## Bottom line

It can be stated more invariantly.

The theorem-grade Wilson-side primitive

- `I_e`,
- `P_e`,
- and the induced embedded probes `I_e X I_e^*`

is exactly equivalent to one rank-3 Wilson **matrix-source embedding**

`Phi_e : Mat_3(C) -> End(H_W)`

with

`Phi_e(X) = I_e X I_e^*`,

`Phi_e(1_3) = P_e`,

and

`rank(Phi_e(1_3)) = 3`.

So the strongest honest next compressed-route object is no longer just:

- “find some `I_e / P_e`”,

but more sharply:

- realize a theorem-grade rank-3 Wilson matrix-source embedding of the charged
  `3 x 3` source algebra.

That is review-safer because it removes arbitrary coordinate rhetoric and pins
the missing object to one invariant source-algebra realization class.

The current exact bank still does **not** realize theorem-grade rank-3 Wilson
matrix-source embedding data, and so it still does **not** realize even that
sharper object.
It still lacks:

- theorem-grade `I_e / P_e`,
- theorem-grade embedded matrix units,
- and theorem-grade Wilson source embedding `Phi_e`.

So this note is both:

- one sharper positive target theorem surface,
- and one sharper current-bank no-go on the same class.

## What is already exact

### 1. The explicit-response class is already formula-level explicit

From
[PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md):

- once a rank-3 Wilson-side charged embedding/compression exists, the probes
  `J_a(t) = t I_e B_a I_e^*` are explicit;
- the nine responses reconstruct the Hermitian compression
  `H_e^(cand)`.

So the current compressed-route frontier already lives on embedded Wilson
sources, not abstract downstream algebra.

### 2. The whole explicit-response family is already equivalent to one operator identity

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md):

- the full nine-probe family is only the coordinate form of
  `H_e^(cand) = H_e`;
- the current bank still lacks theorem-grade `I_e / P_e`.

So the next sharpening should act on the Wilson primitive itself.

### 3. The observable engine already fixes the response grammar on embedded sources

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact Wilson observable generator is
  `W[J] = log |det(D+J)| - log |det D|`;
- for differentiable source paths `J(t)` with `J(0)=0`,

  `(d/dt) W[J(t)] |_(t=0) = Re Tr(D^(-1) J'(0))`.

So once the Wilson source insertion map is fixed, the responses are already
theorem-grade.

### 4. The current bank still does not realize the Wilson primitive under another name

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md),
[PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md),
and
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current bank still lacks explicit `I_e / P_e`;
- pure support pullback does not realize that object;
- and no hidden Wilson-side charged source family is already present.

So the sharpened source-algebra formulation is not already supplied either.

## Theorem 1: `I_e`, `P_e`, and rank-3 Wilson matrix-source embedding are equivalent data

Let `H_W` be a finite-dimensional Wilson parent space. Then the following are equivalent:

1. an isometry `I_e : C^3 -> H_W`;
2. a rank-3 orthogonal projector `P_e` together with a matrix-unit system
   `F_ij` on `Ran(P_e)`, `i,j = 1,2,3`;
3. a unital `*`-monomorphism

   `Phi_e : Mat_3(C) -> End(H_W)`

   such that

   `rank(Phi_e(1_3)) = 3`.

Moreover, under this equivalence one has

`Phi_e(X) = I_e X I_e^*`,

`P_e = Phi_e(1_3) = I_e I_e^*`.

### Proof

`(1) => (3)`.

Given `I_e`, define

`Phi_e(X) := I_e X I_e^*`.

Then `Phi_e` is linear, multiplicative, and `*`-preserving, because `I_e^* I_e
= 1_3`. Also

`Phi_e(1_3) = I_e I_e^*`

is an orthogonal projector of rank `3`.

`(3) => (2)`.

Let `E_ij` be the standard matrix units of `Mat_3(C)` and define

`F_ij := Phi_e(E_ij)`.

Because `Phi_e` is a `*`-monomorphism, the `F_ij` satisfy the exact matrix-unit
relations

`F_ij F_kl = delta_jk F_il`,

`F_ij^* = F_ji`.

Also

`P_e := Phi_e(1_3) = F_11 + F_22 + F_33`

has rank `3`. Since the `F_ii` are nonzero orthogonal projections summing to a
rank-`3` projection, each `F_ii` has rank `1`. So the `F_ij` form a rank-`3`
matrix-unit system on `Ran(P_e)`.

`(2) => (1)`.

Pick unit vectors `u_i` spanning the one-dimensional ranges of `F_ii`. Then
the matrix-unit relations force

`F_ij = |u_i><u_j|`.

Define `I_e : C^3 -> H_W` by `I_e e_i = u_i`. The vectors `u_i` are
orthonormal, so `I_e` is an isometry and

`I_e E_ij I_e^* = F_ij`.

By linearity,

`Phi_e(X) = I_e X I_e^*`

for every `X in Mat_3(C)`.

So all three data are equivalent.

## Corollary 1: the compressed-route frontier may be stated as one Wilson matrix-source embedding theorem

The embedded probe family

`J_X(t) = t I_e X I_e^*`

may be rewritten as

`J_X(t) = t Phi_e(X)`.

So the compressed-route explicit-response target is equivalently:

- derive a theorem-grade rank-3 Wilson matrix-source embedding `Phi_e`,
- and prove

  `(d/dt) W[t Phi_e(X)] |_(t=0) = Re Tr(X H_e)`

  for every `X in Herm(3)`.

Equivalently, after choosing the associated isometry `I_e`,

- prove

  `(I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`.

So the strongest honest next compressed-route theorem surface is now one
source-algebra embedding law together with the same Hermitian
resolvent-compression identity.

## Corollary 2: the current-bank no-go sharpens at the same invariant level

Because the current exact bank still does **not** realize theorem-grade
`I_e / P_e`, it also does **not** realize:

- theorem-grade embedded matrix units `F_ij`,
- or theorem-grade rank-3 Wilson matrix-source embedding `Phi_e`.

So the bank does not merely miss one coordinate presentation of the Wilson
primitive. It misses the entire invariant source-algebra realization class.

## What this closes

- one exact equivalence between `I_e`, `P_e`, and a rank-3 Wilson
  matrix-source embedding;
- one cleaner invariant statement of the strongest honest next compressed-route
  object;
- one sharper no-go that the current bank still lacks even that invariant
  source-algebra object.

## What this does not close

- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- theorem-grade identification of the resulting Hermitian compression with
  `H_e`;
- the residual right-sensitive selector on `dW_e^H`;
- positive global PF closure.

## Why this matters

This is the cleanest Wilson-side formulation of the compressed-route frontier
so far.

The branch no longer has to frame the next target only as:

- “find `I_e / P_e`,”

which still sounds coordinate-dependent.

It can now state the same frontier more invariantly:

- realize the rank-3 charged matrix-source algebra on the Wilson parent space,
- then prove its Hermitian resolvent compression matches `H_e`.

That is the right review-safe object.

## Atlas inputs used

- [PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_wilson_matrix_source_embedding_target_2026_04_17.py
```
