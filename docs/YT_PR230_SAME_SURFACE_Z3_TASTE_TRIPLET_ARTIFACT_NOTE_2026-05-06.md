# PR230 Same-Surface Z3 Taste-Triplet Artifact

**Status:** exact-support / same-surface Z3 taste-triplet artifact; physical
neutral transfer still absent

**Runner:** `scripts/frontier_yt_pr230_same_surface_z3_taste_triplet_artifact.py`

**Certificate:** `outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json`

## Purpose

This block attacks the first missing premise in the Z3 primitive route:

```text
H1: a Z3 cyclic action on the PR230-relevant Higgs-like triplet is derived on
    the same Cl(3)/Z^3 surface.
```

The earlier Z3 primitive theorem proved the finite-matrix Perron-Frobenius
piece conditionally.  This note supplies a same-surface operator artifact for
the cyclic triplet basis itself.

## Exact Artifact

On `C^8 = (C^2)^{otimes 3}`, let

```text
S0 = sigma_x I I
S1 = I sigma_x I
S2 = I I sigma_x
```

and let `U` cyclically permute tensor factors:

```text
U |a,b,c> = |c,a,b>.
```

The runner verifies exactly:

- `U` is unitary;
- `U^3 = I`;
- `U S0 U^-1 = S1`, `U S1 U^-1 = S2`, and `U S2 U^-1 = S0`;
- each `S_i` is trace-zero and squares to identity;
- the `S_i` are Hilbert-Schmidt orthogonal;
- the PR230 source identity `I_8` is fixed by `U`;
- `I_8` has zero Hilbert-Schmidt overlap with every `S_i`.

Thus the PR230 taste surface really has an exact same-surface Z3 action on the
three taste-scalar axes.

## Boundary

This is not top-Yukawa closure.  It supplies the cyclic triplet action premise
for the neutral primitive route, but it does not supply:

- a physical same-surface neutral transfer operator;
- the lazy/aperiodic positive self term as dynamics;
- an off-diagonal neutral generator;
- a strict neutral primitive-cone certificate;
- canonical `O_H`;
- source-Higgs `C_sH/C_HH` pole rows.

The pure cyclic permutation is periodic, not primitive.  The lazy matrix
`(I + P)/2` is primitive as mathematics, but PR230 still needs a physical
same-surface action or row certificate that instantiates that lazy transfer.

## Non-Claims

This note does not claim retained or proposed-retained `y_t` closure.  It does
not identify the source `I_8` with trace-zero taste axes, does not define
`O_H`, `y_t`, or `y_t_bare`, and does not use `H_unit`, `yt_ward_identity`,
observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_same_surface_z3_taste_triplet_artifact.py
# SUMMARY: PASS=26 FAIL=0
```
