# Perron-Frobenius Step-2 Hermitian Resolvent-Compression Target

**Date:** 2026-04-17  
**Status:** exact science-only theorem sharpening the compressed-route
explicit-response class to one operator identity and one sharper current-bank
no-go  
**Script:** `scripts/frontier_perron_frobenius_step2_hermitian_resolvent_compression_target_2026_04_17.py`

## Question

After the compressed-route class has already been sharpened to the explicit
embedded-response formulas

`J_a(t) = t I_e B_a I_e^*`,

`r_a = (d/dt) W[J_a(t)] |_(t=0) = Re Tr(B_a M_e)`,

`M_e = I_e^* D^(-1) I_e`,

is the next honest theorem surface still a family of nine response identities?

Or can the live target be sharpened one level further to one operator-level
identity?

## Bottom line

It sharpens one level further.

Once the rank-3 Wilson-side charged embedding/compression `I_e` exists, the
entire nine-probe explicit-response class is equivalent to one Hermitian
resolvent-compression identity:

`H_e^(cand) := (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`.

Equivalently:

`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)` for every `X in Herm(3)`.

So the strongest honest next theorem surface is no longer:

- derive nine separate Wilson response equalities,

but:

- derive `I_e` or `P_e`,
- and prove the single Hermitian resolvent-compression identity above.

That is sharper and cleaner because the nine-probe family is only the finite
coordinate form of that one operator equality.

The current bank still does **not** realize even that sharper target. It still
lacks:

- theorem-grade `I_e` / `P_e`,
- theorem-grade Wilson-side embedded probes,
- and theorem-grade identification of `H_e^(cand)` with the charged projected
  Hermitian target `H_e`.

So this note is both:

- a sharper positive target theorem surface,
- and a sharper exact current-bank no-go.

## What is already exact

### 1. The explicit-response class is already formula-level explicit

From
[PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md):

- the strongest live compressed-route class is already written in basis-probe
  form;
- the corresponding Wilson first variations already reconstruct
  `H_e^(cand)`.

### 2. Nine Hermitian responses already determine `H_e` exactly

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- a `3 x 3` Hermitian block is determined exactly by nine real linear
  responses on a standard Hermitian basis;
- once `H_e` is known, the downstream packet and selected transport column are
  already algorithmic.

So the nine-probe class is not an open-ended family. It is a finite coordinate
presentation of one Hermitian operator target.

### 3. The missing Wilson primitive is still `I_e / P_e`

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the current bank still lacks explicit Wilson-side `I_e` / `P_e`.

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current bank still does **not** already contain the missing
  Wilson-to-`dW_e^H` bridge under another name.

So the new sharper target still lives on the Wilson side.

## Theorem 1: the explicit-response family is equivalent to one Hermitian resolvent-compression identity

Assume:

1. the exact rank-3 embedded nine-probe explicit-response boundary theorem;
2. the exact projected-source-law derivation theorem;
3. a Wilson-side charged embedding/compression `I_e : C^3 -> H_W`, or
   `P_e = I_e I_e^*`.

Define

`M_e := I_e^* D^(-1) I_e`,

`H_e^(cand) := (M_e + M_e^*) / 2`.

Then the following are equivalent:

1. for every `X in Herm(3)`,

   `(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`;

2. for one standard Hermitian basis `B_1, ..., B_9`,

   `(d/dt) W[t I_e B_a I_e^*] |_(t=0) = Tr(B_a H_e)` for all `a = 1, ..., 9`;

3. the single operator identity holds:

   `H_e^(cand) = H_e`.

### Proof

By the explicit-response boundary theorem,

`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e^(cand))`

for every `X in Herm(3)`.

So statement (1) is exactly equivalent to

`Re Tr(X H_e^(cand)) = Re Tr(X H_e)` for every `X in Herm(3)`.

Because `H_e^(cand)` and `H_e` are Hermitian, this is just

`Tr(X H_e^(cand)) = Tr(X H_e)` for every `X in Herm(3)`.

The Hilbert-Schmidt pairing on `Herm(3)` is nondegenerate, so that is
equivalent to

`H_e^(cand) = H_e`.

Restricting `X` to any basis `B_1, ..., B_9` gives statement (2), and because
the same pairing remains nondegenerate in coordinates, (2) is again equivalent
to `H_e^(cand) = H_e`.

So all three statements are equivalent.

## Corollary 1: the strongest honest next positive target is one operator identity

The compressed-route frontier should now be stated as:

- derive `I_e` or `P_e`,
- prove

  `(I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2 = H_e`.

The nine-probe Wilson-response family is then only the coordinate witness of
that one operator theorem.

## Corollary 2: the current-bank no-go sharpens at the same level

The current bank does not merely lack:

- one generic charged source family.

It lacks the sharper object:

- theorem-grade realization of the Hermitian resolvent compression
  `H_e^(cand)`,
- and theorem-grade identification `H_e^(cand) = H_e`.

So the explicit-response frontier is now pinned exactly at one operator
identity, and that identity is still unrealized on the current bank.

## What this closes

- one exact reduction of the nine-probe explicit-response class to one operator
  identity;
- one sharper statement of the strongest honest positive compressed-route
  theorem target;
- one sharper current-bank no-go at the same operator level.

## What this does not close

- existence of `I_e` or `P_e`;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- the residual right-sensitive selector on `dW_e^H`;
- positive global PF closure.

## Why this matters

This is the cleanest review-safe formulation of the compressed-route frontier
so far.

The branch no longer needs to say only:

- “derive nine Wilson probes,”

or even:

- “derive an embedded response identity.”

It can now say the exact next theorem is:

- derive the Hermitian resolvent-compression identity on the charged rank-3
  Wilson support.

That is the right frontier object.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_hermitian_resolvent_compression_target_2026_04_17.py
```
