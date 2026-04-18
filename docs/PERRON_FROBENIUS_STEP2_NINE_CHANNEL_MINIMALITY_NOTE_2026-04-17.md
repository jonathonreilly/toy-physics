# Perron-Frobenius Step-2 Nine-Channel Minimality

**Date:** 2026-04-17  
**Status:** exact science-only lower-bound theorem for the finite Wilson compressed-route response target  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_nine_channel_minimality_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the Wilson compressed route has already been sharpened to:

- one rank-3 Wilson matrix-source embedding `Phi_e` or equivalently `I_e / P_e`,
- one Hermitian resolvent-compression identity `H_e^(cand) = H_e`,
- and one finite nine-channel Hermitian response family,

is the number `9` only a convenient coordinate choice?

Or is it the exact minimal number of real Wilson response channels needed to
determine an arbitrary charged Hermitian `3 x 3` target?

## Bottom line

It is minimal.

The compressed codomain is the charged Hermitian block `H_e`, which lives in
the real vector space `Herm(3)`.

That space has real dimension `9`.

So any finite Wilson response realization of the form

`H -> (ell_1(H), ..., ell_m(H)) in R^m`

can determine arbitrary `H_e` only if the response map is injective.
But no real-linear map from a `9`-dimensional real space into `R^m` with
`m < 9` can be injective.

Therefore:

- fewer than nine real Wilson response channels cannot determine arbitrary
  charged Hermitian target data;
- the existing nine-channel compressed target is not only sufficient;
- it is the exact minimal finite channel count.

So the branch now knows the coordinate-level compressed Wilson target sharply:

- one operator identity in invariant form,
- equivalently nine real response channels in coordinate form,
- and no finite shortcut below nine.

## What is already exact

### 1. The compressed codomain is already a `3 x 3` Hermitian target

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- for a `3 x 3` Hermitian block, the nine real linear responses on the
  standard Hermitian basis determine `H_e` exactly;
- therefore `dW_e^H` fixes `H_e` exactly.

So the compressed route is already organized around a finite real Hermitian
target, not an open-ended operator class.

### 2. The Wilson-side explicit-response class already lands on that Hermitian space

From
[PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md):

- once a rank-3 Wilson-side charged embedding/compression exists,
  `J_a(t) = t I_e B_a I_e^*` gives exact first variations;
- those responses reconstruct
  `H_e^(cand) := (I_e^* D^(-1) I_e + (I_e^* D^(-1) I_e)^*) / 2`.

So the coordinate response problem already lives on `Herm(3)` exactly.

### 3. The whole response family is already equivalent to one operator identity

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md):

- the full explicit-response family is equivalent to the single identity
  `H_e^(cand) = H_e`;
- the nine basis equalities are only the coordinate form of that one operator
  theorem.

So the response-count question is purely about the minimal coordinate witness
for that already fixed invariant target.

### 4. The Wilson primitive is already packaged as a matrix-source embedding

From
[PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- the Wilson-side primitive may be stated as a rank-3 matrix-source embedding
  `Phi_e : Mat_3(C) -> End(H_W)`;
- the corresponding embedded probes are `J_X(t) = t Phi_e(X)`.

So the lower-bound question belongs exactly on the Wilson compressed-route
source side already isolated by the branch.

## Theorem 1: fewer than nine real Wilson channels cannot determine arbitrary `H_e`

Assume the exact projected-source-law derivation theorem, the exact
rank-3 embedded explicit-response theorem, the exact Hermitian
resolvent-compression target theorem, and the exact Wilson matrix-source
embedding target theorem.

Let `V := Herm(3)`, viewed as a real vector space.
Then `dim_R V = 9`.

Let `ell_1, ..., ell_m : V -> R` be any real-linear response channels.
Form the response map

`L : V -> R^m`,

`L(H) := (ell_1(H), ..., ell_m(H))`.

If `m < 9`, then `L` cannot be injective.
Hence such a channel family cannot determine arbitrary `H in Herm(3)`.

### Proof

Because `V = Herm(3)` has real dimension `9`, every linear map
`L : V -> R^m` with `m < 9` has

`rank(L) <= m < 9`.

By rank-nullity,

`dim ker(L) = 9 - rank(L) > 0`.

So there exists some nonzero `K in Herm(3)` with `L(K) = 0`.
Then for every `H in Herm(3)`,

`L(H + K) = L(H)`.

Therefore the channel data do not distinguish `H` from `H + K`, and so do not
determine arbitrary Hermitian target data.

On the other hand, the projected-source-law derivation theorem already gives a
nine-channel Hermitian-basis family that determines `H_e` exactly.

Therefore the exact minimal finite number of real response channels needed to
determine arbitrary charged Hermitian `3 x 3` target data is `9`.

## Corollary 1: the existing nine-channel compressed target is dimensionally sharp

The theorem-grade finite compressed Wilson target may still be written as:

- derive nine real Wilson response channels on the charged rank-3 support,
- reconstruct `H_e`,
- equivalently prove `H_e^(cand) = H_e`.

But this is now known to be dimensionally optimal.

It is not merely:

- one convenient basis choice among many smaller finite packs.

There is no smaller finite pack for arbitrary `H_e`.

## Corollary 2: no honest compressed-route closure can use eight or fewer generic real channels

Any claimed Wilson compressed-route proof that purports to determine arbitrary
`dW_e^H` or arbitrary `H_e` from fewer than nine real response channels must
be using extra structure beyond the current target class.

Without such extra structure, eight or fewer real channels cannot separate all
Hermitian `3 x 3` targets.

So review should reject any generic compressed-route closure claim below the
nine-channel threshold.

## What this closes

- one exact lower bound on the finite Wilson compressed-route response count;
- one exact statement that the nine-channel target is minimal, not just
  sufficient;
- one review-safe exclusion of generic eight-channel-or-smaller shortcut
  claims.

## What this does not close

- existence of `I_e`, `P_e`, or `Phi_e`;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- the residual right-sensitive selector on `dW_e^H`;
- positive global PF closure.

## Why this matters

This note removes one more ambiguity from the Wilson compressed-route front.

The branch no longer has to say only:

- the compressed target is finite.

It can now say:

- the compressed target saturates the exact finite lower bound.

That is a cleaner theorem surface under hard review because it rules out
underspecified "small response pack" shortcuts.

## Atlas inputs used

- [DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_EXPLICIT_RESPONSE_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_RESOLVENT_COMPRESSION_TARGET_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_nine_channel_minimality_2026_04_17.py
```
