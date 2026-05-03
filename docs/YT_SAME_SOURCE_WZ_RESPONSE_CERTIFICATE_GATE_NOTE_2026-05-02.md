# Same-Source W/Z Response Certificate Gate

**Status:** open / same-source WZ response certificate gate not passed  
**Runner:** `scripts/frontier_yt_same_source_wz_response_certificate_gate.py`  
**Certificate:** `outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json`

## Purpose

The gauge-normalized Feynman-Hellmann route could cancel the unknown source
normalization only if the W/Z side is a real same-source response measurement:

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds).
```

This gate defines what a future W/Z certificate must contain and rejects the
current shortcuts.

## Gate

A passing certificate must include production W or Z correlator mass fits under
the same scalar source used for `dE_top/ds`, a fitted `dM_W/ds` or `dM_Z/ds`,
covariance with the top response, and explicit sector-overlap plus
canonical-Higgs identity certificates.  It must also certify that observed W/Z
masses, static `v`, `H_unit`, and Ward authority were not used as selectors.

The current surface does not pass:

- no `outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json` exists;
- the W/Z response certificate builder records that same-source W/Z response
  rows are absent;
- static EW algebra gives `dM_W/dh = g2/2` after canonical `H` is assumed, not
  `dM_W/ds`;
- even real same-source W/Z slopes remain support-only until
  `k_top = k_gauge` and the canonical-Higgs pole identity are certified.

## Claim Boundary

This is an open gate, not retained or proposed-retained closure.  It does not
set `kappa_s = 1`, does not set `k_top = k_gauge`, and does not use observed
top, observed `y_t`, observed W/Z masses, `H_unit`, `yt_ward_identity`,
`alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.

## Verification

```bash
python3 scripts/frontier_yt_same_source_wz_response_certificate_gate.py
# SUMMARY: PASS=13 FAIL=0
```

Next action: produce real same-source electroweak W/Z mass-response rows, run
`scripts/frontier_yt_fh_gauge_mass_response_certificate_builder.py`, then
rerun this gate; or derive the sector-overlap / canonical-Higgs identity
directly.
