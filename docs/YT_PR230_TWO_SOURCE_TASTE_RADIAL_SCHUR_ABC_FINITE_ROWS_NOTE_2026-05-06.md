# PR230 Two-Source Taste-Radial Schur A/B/C Finite Rows

**Status:** bounded-support / finite Schur A/B/C inverse-block rows from
two-source taste-radial correlator subblocks; strict pole rows absent
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_schur_abc_finite_rows.py`
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json`

The completed chunks001-028 provide finite same-ensemble source/complement
correlator blocks for the certified `s/x` chart:

```text
G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]
```

This runner computes the finite inverse-block rows

```text
K(q) = G(q)^(-1) = [[A_f(q), B_f(q)], [B_f(q), C_f(q)]]
Delta_sx = C_ss C_xx - C_sx^2
A_f = C_xx / Delta_sx
B_f = -C_sx / Delta_sx
C_f = C_ss / Delta_sx
```

It also computes zero-to-first-shell finite differences for `A_f`, `B_f`, and
`C_f`, and checks the inverse identity `G K = I` chunk by chunk.  On
chunks001-028 the row audit is clean, all finite inverse rows are finite with
positive `Delta_sx`, and the maximum inverse-identity residual is below
`1e-10`.

This is real Schur-route progress because it is built from measured
`C_ss/C_sx/C_xx` rows rather than from source-only data.  It is still not
closure.  These are finite inverse-correlator-block rows on a partial
`ready=28/63` packet, not strict neutral-kernel `A/B/C` pole rows, not
isolated-pole `K'(pole)` derivatives, not FV/IR authority, not canonical
`O_H`, and not `kappa_s`.

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_schur_abc_finite_rows.py
# SUMMARY: PASS=17 FAIL=0
```
