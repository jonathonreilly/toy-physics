# Perron-Frobenius Step-2 Hermitian Source-Embedding Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem sharpening the Wilson compressed-route
frontier from the full matrix-source algebra to the weaker Hermitian source
embedding actually used by the response theorem, together with the matching
current-bank no-go  
**Script:** `scripts/frontier_perron_frobenius_step2_hermitian_source_embedding_target_2026_04_17.py`

## Question

After the Wilson compressed route has already been sharpened to

- the invariant matrix-source embedding
  `Phi_e : Mat_3(C) -> End(H_W)`,
- the finite nine-channel minimality theorem,
- and the single Hermitian resolvent-compression identity
  `H_e^(cand) = H_e`,

is the full complex source algebra `Mat_3(C)` really the minimal Wilson-side
object needed to state the compressed response theorem?

Or does the live theorem use only a smaller self-adjoint source object?

## Bottom line

It uses a smaller self-adjoint source object.

The full invariant Wilson matrix-source embedding

`Phi_e : Mat_3(C) -> End(H_W)`

is still a clean sufficient formulation. But the compressed response theorem
only probes Hermitian source directions.

So the exact minimal Wilson-side object needed to state the compressed route is
already the real-linear Hermitian restriction

`Psi_e := Phi_e |_(Herm(3)) : Herm(3) -> Herm(H_W)`,

with

- `Psi_e(1_3) = P_e`,
- `dim_R Im(Psi_e) = 9`,
- and basis images giving the minimal nine-channel Wilson Hermitian source
  family.

Therefore the Wilson compressed route now has two exact attack surfaces:

1. the stronger invariant algebra route through full `Phi_e`,
2. the weaker minimal response route through the Hermitian source embedding
   `Psi_e`.

The current exact bank still realizes neither one. It still lacks:

- theorem-grade `I_e / P_e`,
- theorem-grade `Phi_e`,
- and even theorem-grade rank-`3` Hermitian source embedding `Psi_e`.

So this note both:

- sharpens the minimal Wilson-side object actually used by the compressed
  theorem,
- and closes the matching weaker-object loophole on the current bank.

## What is already exact

### 1. The Wilson primitive is already packaged invariantly as `Phi_e`

From
[PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- theorem-grade `I_e / P_e` is exactly equivalent to one rank-`3` unital
  `*`-monomorphism

  `Phi_e : Mat_3(C) -> End(H_W)`,

- with

  `Phi_e(X) = I_e X I_e^*`,

  `Phi_e(1_3) = P_e`.

So the stronger invariant source-algebra target is already fixed.

### 2. The compressed response theorem only uses Hermitian source directions

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md):

- the live compressed theorem is

  `(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)` for every `X in Herm(3)`,

- equivalently the single operator identity

  `H_e^(cand) = H_e`.

So the active theorem only probes the self-adjoint part of the source algebra.

### 3. Nine Hermitian channels are already exact and minimal

From
[PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md)
and
[PERRON_FROBENIUS_STEP2_NINE_CHANNEL_MINIMALITY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_NINE_CHANNEL_MINIMALITY_NOTE_2026-04-17.md):

- the compressed route can be posed as a finite nine-channel Hermitian response
  family,
- and nine real channels are dimensionally minimal for arbitrary `Herm(3)`
  data.

So the weaker self-adjoint source object is already the exact finite witness
size.

### 4. The current bank still does not realize even the Wilson-side source family

From
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)
and
[PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md):

- the current bank still does not realize the Wilson-side charged source family
  / channel primitive,
- and still does not instantiate the embedded nine-probe explicit-response
  class.

So the weaker Hermitian restriction is not already hiding on the current bank
either.

## Theorem 1: every rank-`3` Wilson matrix-source embedding restricts to a rank-`3` Hermitian source embedding

Assume a theorem-grade rank-`3` Wilson matrix-source embedding

`Phi_e : Mat_3(C) -> End(H_W)`.

Define the Hermitian restriction

`Psi_e := Phi_e |_(Herm(3))`.

Then:

1. `Psi_e` is real-linear;
2. `Psi_e(Herm(3)) subset Herm(H_W)`;
3. `Psi_e(1_3) = P_e := Phi_e(1_3)`;
4. `Psi_e` is injective;
5. `Im(Psi_e)` is a real `9`-dimensional Hermitian source plane on the Wilson
   side;
6. for any Hermitian basis `B_1, ..., B_9`, the images

   `S_a := Psi_e(B_a)`

   form the minimal nine-channel Wilson Hermitian source family.

### Proof

Because `Phi_e` is complex-linear, its restriction to the real vector space
`Herm(3)` is real-linear.

Because `Phi_e` is `*`-preserving, for every `X = X^* in Herm(3)` one has

`Psi_e(X)^* = Phi_e(X)^* = Phi_e(X^*) = Phi_e(X) = Psi_e(X)`,

so `Psi_e(X)` is Hermitian.

Also

`Psi_e(1_3) = Phi_e(1_3) = P_e`.

Because `Phi_e` is injective on all of `Mat_3(C)`, its restriction is
injective on `Herm(3)`.

Since `dim_R Herm(3) = 9`, injectivity implies

`dim_R Im(Psi_e) = 9`.

Therefore for any Hermitian basis `B_1, ..., B_9`, the images

`S_a := Psi_e(B_a)`

are nine real-linearly independent Hermitian Wilson sources spanning the image
plane. By the nine-channel minimality theorem, that is exactly the minimal
finite Wilson source family size needed for arbitrary Hermitian target data.

## Theorem 2: the compressed response theorem depends only on the Hermitian source embedding

Assume:

1. the exact Hermitian resolvent-compression target theorem;
2. a theorem-grade Wilson matrix-source embedding `Phi_e`;
3. its Hermitian restriction `Psi_e`.

Then the full compressed response theorem may be written purely on the
Hermitian source plane:

`(d/dt) W[t Psi_e(X)] |_(t=0) = Re Tr(X H_e)` for every `X in Herm(3)`.

Equivalently, after choosing a Hermitian basis `B_1, ..., B_9` and writing
`S_a := Psi_e(B_a)`, it is enough to prove the nine basis-response identities

`(d/dt) W[t S_a] |_(t=0) = Tr(B_a H_e)`, `a = 1, ..., 9`.

So the full complex multiplication structure of `Mat_3(C)` is not used by the
compressed response theorem itself. It is a stronger invariant packaging of the
same Wilson source object.

### Proof

The Hermitian resolvent-compression target theorem already states that the
compressed response theorem is the family identity on all `X in Herm(3)`, and
that this family identity is equivalent to the nine basis equalities and to
the single operator identity `H_e^(cand) = H_e`.

But for `X in Herm(3)`,

`Phi_e(X) = Psi_e(X)`,

so the source paths appearing in that theorem are exactly the Hermitian-plane
paths

`J_X(t) = t Psi_e(X)`.

Therefore the compressed theorem depends only on the restriction `Psi_e`.

Restricting to a Hermitian basis gives the nine basis-response form, and the
Hermitian resolvent-compression target theorem already proves equivalence with
the full family identity and with `H_e^(cand) = H_e`.

## Corollary 1: the Wilson compressed route has a weaker exact attack surface than full `Phi_e`

The branch may now state the Wilson compressed frontier in two exact ways:

- stronger invariant form:
  realize a rank-`3` Wilson matrix-source embedding `Phi_e`,
- weaker minimal response form:
  realize a rank-`3` nine-dimensional Hermitian source embedding `Psi_e`.

Any theorem proving the weaker object is already enough to pose the compressed
response identity at the right finite Wilson source level.

## Corollary 2: the current-bank no-go sharpens at the weaker-object level too

Because the current bank still lacks:

- theorem-grade `I_e / P_e`,
- theorem-grade `Phi_e`,
- theorem-grade embedded nine-probe explicit-response data,
- and even the Wilson-side charged source family / channel primitive,

it also still does **not** realize theorem-grade Hermitian source embedding

`Psi_e : Herm(3) -> Herm(H_W)`.

So the weaker self-adjoint reformulation does not open a new loophole on the
present bank.

## What this closes

- one exact distinction between the stronger invariant Wilson source algebra
  `Phi_e` and the weaker minimal Hermitian source embedding `Psi_e`;
- one exact statement that the compressed response theorem only uses the
  Hermitian restriction;
- one sharper weaker-object no-go on the current bank.

## What this does not close

- a positive theorem-grade realization of `Psi_e`;
- a positive theorem-grade realization of `Phi_e`;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This changes the Wilson attack surface in a useful way.

The branch no longer has to choose only between:

- full invariant source-algebra realization, or
- vague compressed-route rhetoric.

It can now say exactly:

- the strong invariant target is `Phi_e`,
- but the compressed theorem itself only needs the weaker Hermitian source
  embedding `Psi_e`,
- and the current bank realizes neither one.

That is both cleaner under review and a better guide for positive
construction attempts.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_hermitian_source_embedding_target_2026_04_17.py
```
