# PR #230 FH Gauge-Response Mixed-Scalar Obstruction

**Status:** exact negative boundary / FH gauge-response mixed-scalar obstruction
**Runner:** `scripts/frontier_yt_fh_gauge_response_mixed_scalar_obstruction.py`
**Certificate:** `outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json`

## Result

The same-source W/Z response route cancels a common scalar source
normalization, but it still does not identify physical `y_t` if the measured
source pole has an orthogonal top-coupled scalar admixture.

Let the source pole be

```text
phi = cos(theta) h + sin(theta) chi
```

where `h` is the canonical Higgs radial mode and `chi` is an orthogonal scalar
that can couple to the top but not to the W mass.  Then

```text
dE_top/ds = k (y_h cos(theta) + y_chi sin(theta)) / sqrt(2)
dM_W/ds   = k g2 cos(theta) / 2
```

and the gauge-normalized response reads

```text
(g2/sqrt(2)) (dE_top/ds)/(dM_W/ds)
  = y_h + y_chi tan(theta).
```

So the ratio equals the physical canonical-Higgs Yukawa `y_h` only after an
extra purity premise is supplied.  The executable countermodel keeps the same
measured top slope, W slope, source overlap, and Higgs overlap while changing
`y_h` across:

```text
0.875, 1.25, 1.625
```

## Boundary

This is a boundary on a shortcut, not a no-go against the future response
route.  A same-source W/Z response harness can still be useful, but PR #230
closure requires one of:

- a source-pole equals canonical-Higgs theorem;
- a theorem that orthogonal scalar admixtures have zero top coupling;
- an independent measurement fixing the orthogonal top coupling.

The block does not use observed top, Yukawa, W/Z, or Higgs values; does not use
`H_unit` or Ward authority; and does not set `kappa_s = 1`.

## Verification

```bash
python3 scripts/frontier_yt_fh_gauge_response_mixed_scalar_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```
