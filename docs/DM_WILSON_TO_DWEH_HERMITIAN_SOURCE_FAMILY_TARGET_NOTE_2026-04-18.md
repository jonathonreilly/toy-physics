# DM Wilson-to-`dW_e^H` Hermitian Source-Family Target

**Date:** 2026-04-18
**Status:** exact current-`main` target theorem isolating the weakest honest
constructive Wilson-side object upstream of the DM selector
**Script:** `scripts/frontier_dm_wilson_to_dweh_hermitian_source_family_target_2026_04_18.py`

## Question

After the current `main` reduction has already shrunk the PMNS-assisted DM
route to the charged projected Hermitian codomain

`dW_e^H = Schur_Ee(D_-)`,

what is the weakest honest constructive Wilson-side object worth attacking
next?

Is the next theorem target:

- a new internal scalar selector on `H(m, delta, q_+)`,
- more downstream packet algebra,
- or a smaller upstream source-response object?

## Bottom line

A smaller upstream source-response object.

The weakest honest constructive target is:

- one **Wilson-side Hermitian source family** with nine real channels whose
  first variations reconstruct `dW_e^H`.

Equivalently, the weakest target may be phrased as:

- one real-linear Wilson descendant map
  `Psi_W : Herm(3) -> Herm(H_W)`,
  whose basis responses recover the full charged projected Hermitian law.

Why nine?

- because `dW_e^H` reconstructs `H_e` exactly;
- `H_e` is a `3 x 3` Hermitian block;
- `dim_R Herm(3) = 9`;
- and fewer than nine generic real response channels cannot determine an
  arbitrary Hermitian target.

So the next constructive route is not:

- another internal selector functional on the live DM source sheet.

It is:

- a Wilson-side Hermitian source family whose responses land on `dW_e^H`.

## What is already exact on current `main`

### 1. The codomain `dW_e^H` is already the right compressed object

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
  charge-`-1` source-response law.

From
[DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md):

- once `dW_e^H` is known, the selected `N_e` transport column is already
  downstream algorithmic.

So the live route is already compressed to the correct codomain.

### 2. `dW_e^H` reconstructs `H_e` exactly

The charged projected Hermitian law consists of the nine real linear responses

`X -> Re Tr(X H_e)` on `Herm(3)`.

Therefore `dW_e^H` determines the full charged Hermitian block `H_e` exactly.

### 3. `H_e` already fixes the packet and the flavored transport readout

On the charged-lepton-active branch:

- `H_e` fixes the packet `|U_e|^2^T`,
- the exact flavored transport selector then chooses the relevant column,
- and the PMNS-assisted near-closing value is already recovered.

So the remaining work is not downstream packet or transport algebra.

## Theorem 1: a nine-channel Wilson Hermitian source family is sufficient

Let `B_1, ..., B_9` be any real basis of `Herm(3)`.

Assume there exists a Wilson-side Hermitian source family

`S_1, ..., S_9 in Herm(H_W)`

whose first variations satisfy

`(d/dt) W[t S_a] |_(t=0) = Re Tr(B_a H_e)` for `a = 1, ..., 9`.

Then:

1. the nine response values determine `H_e` exactly;
2. `H_e` determines the charged-lepton-active packet exactly;
3. the exact flavored transport selector determines the relevant `N_e` column
   algorithmically;
4. therefore the whole compressed DM route downstream of `dW_e^H` is already
   fixed.

So a nine-channel Wilson Hermitian source family is a sufficient constructive
target.

## Theorem 2: fewer than nine generic real channels are insufficient

Because `dim_R Herm(3) = 9`, any generic finite response family with fewer
than nine real channels leaves a nontrivial blind direction in `Herm(3)`.

Equivalently:

- with only eight generic real channels, there exist distinct Hermitian targets
  with identical eight-channel response data;
- therefore eight channels do not generically determine `H_e`;
- therefore eight channels do not generically determine `dW_e^H`.

So nine real channels are not only sufficient. They are dimensionally minimal
for a generic Hermitian reconstruction route.

## Consequence

The weakest honest positive theorem target on current `main` is now fixed:

- build a Wilson-side Hermitian source family with nine real channels whose
  responses land on `dW_e^H`.

Only after that should the branch attack:

- right-sensitive dominance on the descended family,
- or any PF-style selector theorem on that family.

## What this closes

- the target-shape question for the next constructive DM attack;
- the claim that the next route should be a new internal scalar on
  `H(m, delta, q_+)`;
- the claim that more downstream packet algebra is the live bottleneck.

## What this does not close

- a positive Wilson-to-`dW_e^H` theorem;
- a positive Wilson-to-`D_-` theorem;
- a replacement for the current imposed source-branch rule;
- the DM flagship lane itself.

## Why this matters

This note puts the first honest post-review constructive target in a form that
is:

- upstream of the current selector obstruction,
- compatible with the exact current `main` reduction,
- and small enough to attack directly.

The next positive route is therefore not:

- “search more selector functionals”.

It is:

- “realize one Wilson Hermitian source family for `dW_e^H`”.
