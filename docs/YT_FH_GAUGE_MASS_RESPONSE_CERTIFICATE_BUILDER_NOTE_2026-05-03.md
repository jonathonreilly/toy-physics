# FH Gauge-Mass Response Certificate Builder

**Status:** open / same-source W/Z response rows absent
**Runner:** `scripts/frontier_yt_fh_gauge_mass_response_certificate_builder.py`
**Status Certificate:** `outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json`
**Future Candidate:** `outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json`

## Purpose

This runner is the executable input contract for the fallback physical-response
route.  If a future production measurement supplies W/Z mass fits under the
same scalar source used for `dE_top/ds`, the builder writes the candidate
certificate consumed by
`scripts/frontier_yt_same_source_wz_response_certificate_gate.py`.

The builder computes the gauge-normalized response ratio:

```text
y_t support ratio = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

but only as support.  It does not authorize retained or `proposed_retained`
wording.

## Required Input

The future row file must certify:

- production phase;
- same scalar source coordinate and at least three source shifts;
- W or Z mass fits from correlators, not static electroweak algebra;
- top response slope and W/Z mass-response slope with covariance;
- `g2` with a non-observational authority certificate;
- same-source sector-overlap and canonical-Higgs pole identity certificates;
- retained-route gate pass before any proposed-retained wording;
- no observed W/Z, top, or `y_t` selectors;
- no `H_unit`, Ward authority, `alpha_LM`, plaquette, `u0`, `c2 = 1`, or
  `Z_match = 1` as proof inputs.

## Current Result

No same-source W/Z mass-response measurement rows are present, so no candidate
certificate is written.  The existing W/Z response gate remains open.

## Claim Boundary

This builder does not claim retained or `proposed_retained` top-Yukawa closure.
It does not manufacture W/Z mass fits, does not turn static
`dM_W/dh = g2/2` into `dM_W/ds`, and does not set `kappa_s = 1` or
`k_top = k_gauge`.

## Verification

```bash
python3 scripts/frontier_yt_fh_gauge_mass_response_certificate_builder.py
# SUMMARY: PASS=2 FAIL=0
```
