# PR #230 W/Z Response Harness Implementation Plan

```yaml
actual_current_surface_status: bounded-support / WZ response harness implementation plan
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_wz_response_harness_implementation_plan.py`  
**Certificate:** `outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json`

## Purpose

The same-source W/Z response route is the main fallback if the source-Higgs
`O_sp/O_H` route remains blocked.  It can only work if PR #230 measures a real
W/Z mass response under the same scalar source used for the top
Feynman-Hellmann row.  Static electroweak algebra gives `dM_W/dh` after a
canonical Higgs field is supplied; it is not a measured `dM_W/ds`.

This note turns that fallback into a concrete implementation packet without
claiming physics closure.

## Required Work Units

The runner records five required blocks:

1. Define a same-source electroweak gauge/Higgs action block on the Cl(3)/Z3
   substrate, with the source coupled to the canonical Higgs radial direction.
2. Measure W/Z correlator masses at negative, zero, and positive source
   shifts with production errors and fit-window/systematic rows.
3. Fit `dE_top/ds` and `dM_W/ds` or `dM_Z/ds` on matched configurations with
   covariance.
4. Supply sector-overlap and canonical-Higgs pole-identity certificates, so a
   generic W/Z slope cannot hide an orthogonal neutral top-coupling direction.
5. Write the future W/Z measurement-row file and rerun the existing builder,
   W/Z gate, retained-route certificate, and campaign-status certificate.

## Validation

```text
python3 scripts/frontier_yt_wz_response_harness_implementation_plan.py
# SUMMARY: PASS=15 FAIL=0
```

## Claim Boundary

This is implementation support only.  It does not write
`outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json`, does not
treat the QCD harness W/Z absent guard as evidence, does not use static EW
gauge-mass algebra as `dM_W/ds`, and does not authorize retained or
`proposed_retained` wording.

Next action: either implement the EW same-source W/Z correlator workstream, or
continue the higher-priority source-Higgs, Schur, rank-one, and FH/LSZ chunk
routes already active in PR #230.

## Adapter Added

The mass-fit-to-response adapter is now explicit:

```text
scripts/frontier_yt_wz_mass_fit_response_row_builder.py
```

It consumes future W/Z correlator mass-fit rows, a matched same-source top
response certificate, and a non-observed `g_2` certificate, then emits the
measurement-row file consumed by the existing W/Z response certificate builder.
Scout mode writes only scout-named rows; strict mode remains blocked until the
future production inputs exist.
