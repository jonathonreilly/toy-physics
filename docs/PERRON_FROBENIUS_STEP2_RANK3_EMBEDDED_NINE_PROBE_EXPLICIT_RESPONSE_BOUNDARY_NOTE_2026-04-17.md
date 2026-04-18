# Perron-Frobenius Step-2 Rank-3 Embedded Nine-Probe Explicit-Response Boundary

**Date:** 2026-04-17  
**Status:** exact science-only theorem sharpening the strongest live positive
compressed-route class to explicit source/response formulas and closing its
current-bank realization status  
**Script:** `scripts/frontier_perron_frobenius_step2_rank3_embedded_nine_probe_explicit_response_boundary_2026_04_17.py`

## Question

Can the strongest live compressed-route positive class

- a rank-3 Wilson-side charged embedding/compression, together with
- the induced embedded nine-probe Hermitian response family,

be sharpened beyond candidate-class rhetoric?

And does the current exact bank already realize even that sharpened class?

## Bottom line

Yes on theorem shape, no on current-bank realization.

If a Wilson-side rank-3 charged embedding/compression exists,

`I_e : C^3 -> H_W`,

or equivalently

`P_e = I_e I_e^*`,

then the strongest live positive compressed-route class sharpens to an exact
embedded-response formula.

Fix a standard Hermitian basis `B_1, ..., B_9` of `Herm(3)`. Define the
embedded Wilson-side probes

`J_a(t) = t I_e B_a I_e^*`,  `a = 1, ..., 9`.

Then the exact lattice observable generator

`W[J] = log |det(D+J)| - log |det D|`

has first variations

`r_a := (d/dt) W[J_a(t)] |_(t=0)`

given by

`r_a = Re Tr(D^(-1) I_e B_a I_e^*) = Re Tr(B_a M_e)`,

where

`M_e := I_e^* D^(-1) I_e`.

Therefore the nine embedded Wilson responses reconstruct the Hermitian
compression

`H_e^(cand) := (M_e + M_e^*) / 2`

exactly, because

`r_a = Tr(B_a H_e^(cand))`.

So the strongest live positive compressed-route class may now be stated
explicitly as:

- derive `I_e` or `P_e`,
- evaluate the nine Wilson responses to `J_a(t) = t I_e B_a I_e^*`,
- prove that the resulting Hermitian compression `H_e^(cand)` matches the
  charged projected-source target.

Equivalently, the explicit positive target is:

`H_e^(cand) = H_e`,

or in source-law language,

`(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`

for every `X in Herm(3)`.

However, the current exact bank still does **not** realize that sharpened
class. It still lacks:

- an explicit Wilson-side charged embedding/compression `I_e` or `P_e`,
- an exact theorem generating the nine embedded probe sources
  `I_e B_a I_e^*`,
- and an exact theorem matching those nine Wilson responses to `dW_e^H`.

So this is a stronger exact candidate theorem and a sharper exact
current-bank nonrealization statement, not a fake bridge proof.

## What is already exact

### 1. The live positive class is already the rank-3 embedded nine-probe class

From
[PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_CANDIDATE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_CANDIDATE_BOUNDARY_NOTE_2026-04-17.md):

- the strongest honest compressed-route positive class is already
  rank-3 embedded and nine-probe finite;
- everything weaker than that class is already dead.

### 2. The observable engine already fixes the exact first-variation grammar

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact Wilson-side observable generator is
  `W[J] = log |det(D+J)| - log |det D|`.

For any differentiable finite source path `J(t)` with `J(0) = 0`, finite
determinant calculus gives

`(d/dt) W[J(t)] |_(t=0) = Re Tr(D^(-1) J'(0))`.

So once a Wilson-side embedded source family is specified, its first
variations are explicit.

### 3. Nine Hermitian responses already determine the compressed codomain data

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- nine real Hermitian-basis responses determine the `3 x 3` Hermitian block
  exactly;
- once that Hermitian block is known, the downstream `N_e` packet and the
  selected transport column are already algorithmic.

So the explicit nine-probe class is not just finite. It is already sufficient.

### 4. The current bank still does not realize the embedded class

From
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the current bank still lacks explicit `I_e` or `P_e`.

From
[PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current bank still does not realize the compressed-route charged source
  family/channel.

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current bank still does not already contain the missing
  Wilson-to-`dW_e^H` law under another name.

So the sharpened explicit-response class is still unrealized on the current
bank.

## Theorem 1: exact explicit-response sharpening of the strongest live positive class

Assume:

1. the exact rank-3 embedded nine-probe candidate-boundary theorem;
2. the exact observable principle;
3. the exact projected-source-law derivation theorem;
4. a Wilson-side rank-3 charged embedding/compression `I_e : C^3 -> H_W`
   or `P_e = I_e I_e^*`.

Let `B_1, ..., B_9` be a standard Hermitian basis of `Herm(3)` and define

`J_a(t) = t I_e B_a I_e^*`.

Then:

1. the exact first variations are

   `r_a = (d/dt) W[J_a(t)] |_(t=0) = Re Tr(B_a M_e)`,

   where

   `M_e := I_e^* D^(-1) I_e`;

2. writing

   `H_e^(cand) := (M_e + M_e^*) / 2`,

   one has

   `r_a = Tr(B_a H_e^(cand))`;

3. the nine embedded Wilson responses therefore reconstruct
   `H_e^(cand)` exactly.

Therefore the strongest live positive compressed-route class sharpens to the
explicit embedded-response theorem candidate:

- derive `I_e`,
- evaluate the nine Wilson responses to `I_e B_a I_e^*`,
- identify the resulting reconstructed Hermitian compression with the charged
  projected-source target.

## Corollary 1: the positive compressed-route target is now formula-level explicit

The compressed route no longer needs to be stated merely as:

- “derive some charged source family.”

It may now be stated explicitly as:

- derive `I_e` and prove

  `(d/dt) W[t I_e X I_e^*] |_(t=0) = Re Tr(X H_e)`

  for every `X in Herm(3)`.

That is the exact formula-level sharpening of the strongest live positive class.

## Corollary 2: if that formula lands, only the known right-sensitive selector remains

Once the embedded-response identity above is proved, the compressed route
reduces exactly to the already-isolated right-sensitive selector on `dW_e^H`.

So this explicit-response candidate is the true last upstream bridge on the
compressed route.

## Theorem 2: exact current-bank nonrealization of the sharpened explicit-response class

Assume:

1. the exact charged-embedding boundary theorem;
2. the exact charged-source-family current-bank nonrealization theorem;
3. the exact Wilson-to-Hermitian current-bank nonrealization theorem;
4. the exact explicit-response sharpening above.

Then the current exact bank still does **not** realize:

1. an explicit Wilson-side charged embedding/compression `I_e` or `P_e`;
2. the induced embedded probes `J_a(t) = t I_e B_a I_e^*`;
3. an exact theorem identifying the nine Wilson first variations with the
   charged projected-source law.

Therefore the current exact bank still does **not** instantiate the sharpened
rank-3 embedded nine-probe explicit-response class.

## What this closes

- one exact formula-level sharpening of the strongest live positive
  compressed-route class;
- one exact identification of the reconstructed operator carried by those nine
  responses, namely the Hermitian compression `H_e^(cand)`;
- one sharper exact no-go: the current bank does not yet realize even this
  explicit-response class.

## What this does not close

- existence of `I_e` or `P_e`;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- the residual right-sensitive selector;
- global PF closure.

## Why this matters

This is a better theorem surface for hard review.

It replaces vague candidate language with explicit formulas, while also making
the negative statement sharper:

- not only is the compressed primitive still missing in general,
- the current bank still does not realize the strongest formula-level version
  of that primitive either.

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_rank3_embedded_nine_probe_explicit_response_boundary_2026_04_17.py
```
