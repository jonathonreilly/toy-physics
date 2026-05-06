# PR230 Two-Source Taste-Radial Schur-Subblock Witness

**Status:** bounded-support / two-source taste-radial Schur-subblock witness; strict Schur `K'(pole)` rows and canonical `O_H` authority absent
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_schur_subblock_witness.py`
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json`

The completed two-source taste-radial chunks now provide a real finite
same-ensemble source/complement subblock for the certified `s/x` chart:

```text
G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]
```

The runner validates chunks001-012 through the manifest/combiner path, checks
production seed control and non-readout metadata, and computes finite-mode
Schur diagnostics:

```text
Delta_sx = C_ss C_xx - C_sx^2
C_{s|x} = Delta_sx / C_xx
rho_sx = C_sx / sqrt(C_ss C_xx)
```

All ready rows have positive finite two-source Gram determinant.  This is a
genuine row artifact for the Schur route because it is not source-only data:
the complement source `x` is supplied by the same-surface taste-radial chart
and the completed chunks carry `C_ss`, `C_sx`, and `C_xx`.

It is not closure.  The witness is a correlator subblock, not the strict Schur
kernel-row packet required by the `K'(pole)` theorem.  It supplies no pole
location, no `A'`, `B'`, or `C'` pole derivatives, no FV/IR/zero-mode limiting
authority, no canonical `O_H` identity, and no source-Higgs normalization
`kappa_s`.

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_subblock_witness.py
# SUMMARY: PASS=16 FAIL=0
```
