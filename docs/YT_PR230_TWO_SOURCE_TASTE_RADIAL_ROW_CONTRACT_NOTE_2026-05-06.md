# PR230 Two-Source Taste-Radial Row Contract Note

**Date:** 2026-05-06  
**Status:** bounded-support / two-source taste-radial `C_sx/C_xx` row contract; production rows absent  
**Claim type:** support_boundary  
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_row_contract.py`  
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json`

```yaml
actual_current_surface_status: bounded-support / two-source taste-radial C_sx/C_xx row contract; production rows absent
conditional_surface_status: conditional-support if production rows are run with this schema and a separate canonical O_H/source-overlap or physical-response bridge closes
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

The previous action certificate realized the taste-radial second source as the
gauge-covariant blocked-hypercube vertex
`X=(X_1+X_2+X_3)/sqrt(3)`.  This note records the next row-level contract:
when that source is passed through the stochastic source/operator trace
harness, the analysis exposes explicit `C_sx` and `C_xx` fields.

The legacy `C_sH/C_HH` schema remains present for compatibility, but the new
metadata marks the operator as a second source `x`, not as canonical Higgs
`O_H`.  The aliases are intentionally exact labels over the same finite
source/operator trace values:

```text
C_sx = C_sH_schema_field
C_xx = C_HH_schema_field
```

## Boundary

This is not a production row certificate.  The runner uses a tiny finite smoke
only to verify schema and firewall behavior.  It does not write
`outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json`,
does not extract pole residues, does not derive `kappa_s`, and does not
identify `x` with canonical `O_H`.

The row contract is useful because it removes a naming/schema ambiguity before
production: future measured rows can now be audited as `C_sx/C_xx` second-source
rows without importing forbidden canonical-Higgs normalization.

## Validation

```text
python3 scripts/frontier_yt_pr230_two_source_taste_radial_row_contract.py
# SUMMARY: PASS=12 FAIL=0
```

The exact next action is to run production `C_sx/C_xx` rows using this schema,
then supply either canonical `O_H`/source-overlap authority or a genuine
same-source physical-response bypass before retained-route gates can pass.
