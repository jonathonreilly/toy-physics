# PR #230 Same-Source EW Action Certificate Builder

```yaml
actual_current_surface_status: open / same-source EW action certificate absent
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_wz_same_source_ew_action_certificate_builder.py`
**Certificate:** `outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json`

## Purpose

This is a non-chunk closure artifact for PR #230.  The source-Higgs and W/Z
response bypasses both need a same-surface electroweak action block, not static
EW algebra after a canonical Higgs field is assumed.

The builder defines the future acceptance schema for
`outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json`.  A valid
certificate must provide dynamic `SU(2)_L` and `U(1)_Y` fields, a dynamic Higgs
doublet, the gauge-covariant Higgs kinetic term, a scalar source coupled to the
centered `Phi^dagger Phi` composite on the same source coordinate, W/Z
correlator observables, and references to the Higgs mass-source action bridge,
canonical-Higgs, sector-overlap, and W/Z mass-fit certificates.

## Current Result

No same-source EW action certificate is present on the current PR #230 surface.
The gate therefore remains open.  Static `dM_W/dh`, native gauge structural
support, and the QCD top FH/LSZ harness do not satisfy the contract.

## Verification

```bash
python3 scripts/frontier_yt_wz_same_source_ew_action_certificate_builder.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not synthesize W/Z rows, define `O_H` by fiat, treat static EW algebra as
measurement data, or use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.

Exact next action for this route: supply a real same-source EW action
certificate satisfying this schema, attach the Higgs mass-source action bridge
for `dS/ds=sum O_H`, then implement W/Z correlator mass-fit rows or
source-Higgs `C_sH/C_HH` rows with identity certificates.
