# PR230 Z3 Triplet Positive-Cone Support Certificate

**Status:** exact-support / Z3-triplet positive-cone H2 support; physical neutral transfer still absent

**Runner:** `scripts/frontier_yt_pr230_z3_triplet_positive_cone_support_certificate.py`

**Certificate:** `outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json`

## Purpose

The conditional Z3 primitive route had H1 supplied by the same-surface taste
triplet artifact, but still listed H2-H4 as missing.  This block supplies the
narrow algebraic part of H2: the three same-surface taste channels have a
nonzero equal-magnitude positive-cone realization.

For the trace-zero taste axes `S_i`, define

```text
Q_i^+ = (I + S_i)/2
Q_i^- = (I - S_i)/2.
```

The runner checks that the `Q_i^+` are Hermitian idempotent positive
semidefinite projectors, each with trace/rank `4` and Hilbert-Schmidt norm
`2`, and that the same Z3 tensor-cycle operator maps
`Q_0^+ -> Q_1^+ -> Q_2^+ -> Q_0^+` and likewise for `Q_i^-`.

## Boundary

This is a genuine same-surface algebraic support artifact, but it is not a
physical neutral transfer.  H3 and H4 remain absent:

- no same-surface lazy positive transfer or off-diagonal neutral generator;
- no proof that the transfer couples to the PR230 source/canonical-Higgs
  sector;
- no canonical `O_H` identity;
- no `C_sH/C_HH` source-Higgs pole rows;
- no retained/proposed-retained closure.

The certificate does not treat PSD cone support as dynamics and does not set
`kappa_s`, `c2`, `Z_match`, or the source-Higgs overlap to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_z3_triplet_positive_cone_support_certificate.py
# SUMMARY: PASS=19 FAIL=0
```
