# DM Wilson Direct-Descendant Constructive Transport Plateau Schur Spectral-Isotropy Selector

**Date:** 2026-04-19  
**Status:** exact current-branch positive plateau-breaker candidate on the
current certified constructive witness set.

The science that closes the current plateau issue is:

> a coefficient-free value law on the normalized Schur-side spectrum of
> `H_e(L_e) = Herm(L_e^(-1))`.

On the current certified constructive transport plateau witnesses
`W0, W1, W2, W3`, that law has a clean answer:

- `W1` has the most isotropic normalized Schur spectrum;
- more sharply, the normalized `W1` spectrum is majorized by the normalized
  spectra of `W0`, `W2`, and `W3`;
- therefore every strictly Schur-concave symmetric law of the normalized
  spectrum uniquely selects `W1` on this certified witness set.

Representative winners include:

- Shannon entropy,
- the Renyi entropy family,
- participation ratio,
- normalized log-determinant / AM-GM isotropy,
- inverse condition number.

The aligned-seed -> `W1` affine segment then has a unique exact transverse
`eta_1 = 1` crossing, so the branch now carries a fully specified
source-visible selector candidate:

```text
1. choose the constructive plateau endpoint W1 by maximal normalized
   Schur spectral isotropy;
2. choose the unique eta_1 = 1 point on the aligned-seed -> W1 segment.
```

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_schur_spectral_isotropy_selector_2026_04_19.py`

## Question

After the affine-observable no-go, what kind of science would actually close
the current plateau issue?

The answer cannot just be “some other score.” It has to be:

- coefficient-free,
- source-visible but transport-blind,
- naturally expressible on the local Schur-side data,
- and strong enough to pick one certified plateau witness.

## Bottom line

The first current-branch family that does that is normalized Schur spectral
isotropy.

Write the positive spectrum of

```text
H_e(L_e) = Herm(L_e^(-1))
```

as `lambda_1 >= lambda_2 >= lambda_3 > 0`, and normalize it to the simplex

```text
p(H_e) = (lambda_1, lambda_2, lambda_3) / Tr(H_e).
```

On the certified witness set:

- all four witnesses realize the same transport-optimal favored-column orbit,
  so transport does not distinguish them;
- but the four normalized Schur spectra are distinct;
- and `p(W1)` is more isotropic than the others in the precise majorization
  sense.

For `3`-component probability vectors, that means:

- the largest cumulative weight of `W1` is smallest,
- the two-largest cumulative weight of `W1` is also smallest,
- so `W1` is the unique maximizer of every strictly Schur-concave symmetric
  normalized spectral law on this witness set.

That is a whole source-side selector family, not a one-off fitted expression.

## Why this is the right kind of science

This law has exactly the right scope for the current gap.

It is:

- **source-side:** it depends on `H_e(L_e)`, hence on local Schur data;
- **transport-blind:** all four witnesses keep the same transport column orbit;
- **coefficient-free:** no affine weights need to be supplied by hand;
- **nonlinear enough:** it escapes the previous affine no-go;
- **endpoint-selecting:** it uniquely picks `W1`.

So this is the first actual positive answer to the question

> what source-visible law could break the constructive plateau?

## Relation to the earlier path law

The earlier same-day path theorem gave the support-level candidate

```text
choose the unique eta_1 = 1 point on the aligned-seed -> W0 path.
```

The present note changes the endpoint science.

It does **not** recover the old hand-chosen endpoint `W0`. It selects `W1`.
So, if this selector is retained, the honest updated law is:

```text
choose W1 by Schur spectral isotropy,
then choose the unique eta_1 = 1 point on the aligned-seed -> W1 path.
```

The resulting exact root is constructive, positive-branch, and locally
full-rank, and it is macroscopically distinct from the old hand-chosen
canonical-path root.

## What this closes

- the question of what kind of science can actually break the current plateau
  without free coefficients;
- the endpoint ambiguity on the current certified witness set;
- the need to keep using a hand-chosen constructive endpoint if one wants a
  source-visible plateau-breaker now.

## What this does not close

- a retained derivation of why normalized Schur spectral isotropy is the
  physical law;
- a proof beyond the current certified witness set `W0..W3`;
- the final reviewer-grade derivation from `Cl(3)` on `Z^3`.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_schur_spectral_isotropy_selector_2026_04_19.py
```

Expected:

- `W1` majorized by `W0`, `W2`, and `W3` in normalized Schur spectrum;
- all representative spectral-isotropy laws select `W1`;
- the aligned-seed -> `W1` segment has one exact transverse `eta_1 = 1`
  crossing;
- `PASS` with `FAIL=0`.
