# PR230 W/Z Smoke-To-Production Promotion No-Go Note

**Status:** exact negative boundary / WZ smoke rows cannot be promoted to
production WZ response.

This block closes the obvious shortcut opened by the W/Z smoke-schema harness:
using the synthetic smoke rows as if they were production W/Z mass-response
measurements.  The runner
`scripts/frontier_yt_pr230_wz_smoke_to_production_promotion_no_go.py`
reloads the smoke-schema gate and the strict W/Z response builders/gates, then
checks that the smoke artifact has no proposal authority.

## Certified Boundary

The smoke artifact is intentionally useful only as schema plumbing.  The
certificate verifies that:

- the analysis phase is `scout`;
- `metadata.wz_mass_response.implementation_status` is
  `smoke_schema_enabled_not_ew_production`;
- `production_wz_rows_written` is false;
- row sources are marked `synthetic_scout_contract_not_EW_field`;
- same-source, sector-overlap, canonical-Higgs, and retained-route identity
  certificates are false;
- top/W covariance is absent;
- non-observed `g2` authority is absent;
- the strict same-source EW action, W/Z correlator mass-fit path, strict W/Z
  response rows, matched top/W covariance, and same-source W/Z gate all remain
  open or blocked;
- full assembly, retained-route, and campaign certificates still deny proposal
  authority.

## Claim Boundary

The W/Z smoke rows cannot be promoted to production W/Z response evidence.
Promotion would import the same-source EW action, W/Z production rows, matched
covariance, `g2`, sector identity, and canonical-Higgs/source-overlap
certificates that the smoke path explicitly does not supply.

This is not retained or proposed-retained top-Yukawa closure.  It is a
firewall against treating a schema artifact as physical `y_t` evidence.

## Verification

```bash
python3 -m py_compile \
  scripts/frontier_yt_pr230_wz_smoke_to_production_promotion_no_go.py

python3 scripts/frontier_yt_pr230_wz_smoke_to_production_promotion_no_go.py
# SUMMARY: PASS=22 FAIL=0
```

Certificate:

- `outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json`
