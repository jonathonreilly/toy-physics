# DM Wilson Direct-Descendant Constructive Transport Plateau Normalized Schur-Determinant Selector

**Date:** 2026-04-19  
**Status:** exact current-branch reduction of the Schur spectral-isotropy
selector family to one explicit local scalar law on the certified constructive
plateau set.

The previous plateau note isolated a coefficient-free source-side selector
family:

> maximize normalized Schur spectral isotropy of `H_e(L_e) = Herm(L_e^(-1))`.

This note turns that family into one exact local scalar:

```text
J_iso(H_e) = 27 det(H_e) / Tr(H_e)^3
           = 27 Delta_src / (R11 + R22 + R33)^3.
```

On the current certified constructive plateau witnesses `W0, W1, W2, W3`,
that scalar uniquely selects `W1`. The aligned-seed -> `W1` segment then has a
unique exact transverse constructive `eta_1 = 1` crossing. So the branch now
has a concrete exact local selector representative rather than only a spectral
family description.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_normalized_schur_determinant_selector_2026_04_19.py`

## Question

After the Schur spectral-isotropy selector note, what is still left before one
has the cleanest retained-closeout candidate the branch can honestly state?

The main remaining compression was:

- turn the family into one explicit exact scalar law on local source data;
- keep it coefficient-free;
- keep it local to the descended Schur block;
- and verify that it picks the same certified winner.

## Bottom line

The cleanest exact scalar representative is the normalized Schur determinant

```text
J_iso = 27 det(H_e) / Tr(H_e)^3.
```

This is the `3 x 3` AM-GM isotropy ratio:

- `0 < J_iso <= 1` for every positive `H_e`,
- `J_iso = 1` only at perfect spectral isotropy,
- it is scale-free,
- and it is basis-invariant.

Using the same-day Schur reduction theorem,

```text
det(H_e) = Delta_src,
Tr(H_e) = R11 + R22 + R33,
```

so the law is already an exact local scalar of the descended source response
pack.

On the certified constructive plateau witnesses:

- `J_iso(W1)` is strictly larger than `J_iso(W0)`, `J_iso(W2)`, and `J_iso(W3)`;
- its winner agrees with the full normalized spectral-isotropy family;
- so `W1` is the exact scalar-law endpoint.

The fully specified current closeout candidate is therefore:

```text
1. choose the constructive plateau endpoint by maximizing
   J_iso = 27 Delta_src / (R11 + R22 + R33)^3;
2. choose the unique eta_1 = 1 point on the aligned-seed -> W1 segment.
```

## Why this matters

This is the cleanest current compression of the source-side plateau science.

The branch no longer needs to say only

> “some Schur-concave spectral isotropy law.”

It can now say

> “the exact local scalar representative is the normalized Schur determinant.”

That is a real step toward retained closure because:

- it uses only exact local descended data;
- it needs no coefficient fitting;
- it is the natural `3 x 3` scale-free isotropy scalar;
- and it reproduces the previously certified `W1` endpoint.

## Relation to the previous same-day selector note

The earlier same-day selector note proved the family statement:

- `W1` is majorized by the other certified plateau spectra;
- so every strictly Schur-concave symmetric normalized spectral law selects
  `W1`.

The present note extracts the simplest exact scalar representative of that
family:

- `J_iso = 27 det(H_e) / Tr(H_e)^3`.

So this is not a new winner. It is the exact scalar-law compression of the
same winner.

## Honest scope

This still does **not** prove full retained closure in the strongest possible
sense. What remains open is narrower:

- derive from retained physics why `J_iso` is the physical law to maximize,
  rather than only the cleanest current exact selector representative;
- prove the same winner beyond the currently certified plateau witness set;
- derive the law reviewer-grade from `Cl(3)` on `Z^3`.

But it does close what was left at the current branch level:

- the selector family is now an explicit local scalar;
- the endpoint law is explicit;
- the path root is explicit.

## What this closes

- the gap between a whole spectral-isotropy family and one exact local scalar
  selector law;
- the need to state the plateau-breaker only in terms of eigenvalue families;
- the lack of a concrete source-response scalar representative for the current
  closeout candidate.

## What this does not close

- the derivation of the `J_iso` maximization principle from retained physics;
- a proof beyond the certified witness set `W0..W3`;
- the final reviewer-grade retained endpoint derivation.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_SCHUR_SPECTRAL_ISOTROPY_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_SCHUR_SPECTRAL_ISOTROPY_SELECTOR_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_normalized_schur_determinant_selector_2026_04_19.py
```

Expected:

- exact identity `J_iso = 27 Delta_src / (R11+R22+R33)^3`;
- unique certified plateau maximizer `W1`;
- unique exact constructive `eta_1 = 1` crossing on the aligned-seed -> `W1`
  segment;
- `PASS` with `FAIL=0`.
