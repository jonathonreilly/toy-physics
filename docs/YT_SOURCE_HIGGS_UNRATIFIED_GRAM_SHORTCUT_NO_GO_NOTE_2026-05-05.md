# PR230 Source-Higgs Unratified-Gram Shortcut No-Go

**Status:** exact negative boundary / unratified source-Higgs Gram shortcut is
not `O_H` authority
**Runner:** `scripts/frontier_yt_source_higgs_unratified_gram_shortcut_no_go.py`
**Certificate:** `outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json`

## Claim

The source-Higgs route can use the pole-level Gram relation

```text
Res(C_sH)^2 = Res(C_ss) Res(C_HH)
```

only after the second operator is a same-surface canonical-Higgs radial
operator with identity and normalization certificates.  Perfect Gram purity
against an unratified supplied operator is not a PR230 `O_H` certificate.

This closes the shortcut:

```text
perfect C_ss/C_sH/C_HH Gram relation against an unratified operator
  -> treat that operator as canonical O_H
  -> authorize source-Higgs physical y_t readout
```

## Result

The runner constructs a synthetic perfect-Gram witness with
`Res(C_ss)=4`, `Res(C_sH)=6`, and `Res(C_HH)=9`.  The Gram determinant is zero,
but the postprocessor contract still rejects the candidate because the
canonical-Higgs identity, identity certificate, normalization certificate, and
retained-route gate are absent.

It also records a counterfamily: the same unratified rows can coexist with
different canonical-Higgs overlaps.  Therefore the rows certify, at most,
purity relative to the supplied unratified operator, not purity relative to the
physical canonical `O_H`.

The existing reduced source-Higgs smoke run remains instrumentation only:
finite-mode rows exist, the operator is explicitly unratified, and it is not
used as a physical Yukawa readout.

## Boundary

This does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not create production source-Higgs rows, define `O_H` by notation or Gram
purity, use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed targets,
`alpha_LM`, plaquette, `u0`, or set `kappa_s`, `c2`, `Z_match`, or
`cos(theta)` to one.

## Verification

```bash
python3 scripts/frontier_yt_source_higgs_unratified_gram_shortcut_no_go.py
# SUMMARY: PASS=10 FAIL=0
```

Next action: supply a same-surface canonical-Higgs operator identity and
normalization certificate, then produce production `C_ss/C_sH/C_HH` pole
residues and rerun the source-Higgs builder, Gram-purity postprocessor,
retained-route certificate, and PR230 assembly gate.
