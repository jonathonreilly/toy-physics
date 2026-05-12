# PR230 Top-Mass-Scan Subtraction-Contract Applicability Audit

**Status:** exact negative boundary: top mass-scan response rows do not satisfy
the additive-top subtraction row contract

**Runner:**
`scripts/frontier_yt_pr230_top_mass_scan_subtraction_contract_applicability_audit.py`

**Certificate:**
`outputs/yt_pr230_top_mass_scan_subtraction_contract_applicability_audit_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / top mass-scan response harness does not satisfy the additive-top subtraction row contract
conditional_surface_status: conditional-support if future same-ensemble rows provide mixed-source T_total, strict A_top, W/Z response, matched covariance, strict g2/v, and accepted action authority
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Purpose

The W/Z physical-response repair route has an exact support contract:

```text
y_t = g2 (T_total - A_top) / (sqrt(2) W).
```

The newest top mass-scan harness serializes per-configuration slopes from the
existing three-mass top correlator scan.  This block checks whether those rows
can be admitted as the strict additive-top subtraction packet.  They cannot.

## Inputs

- `outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json`
- `outputs/yt_pr230_top_mass_scan_response_harness_smoke_2026-05-12.json`
- `outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json`
- `outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json`
- `outputs/yt_pr230_block35_post_block34_physical_bridge_admission_checkpoint_2026-05-11.json`
- W/Z physical-response, covariance, and `g2` authority gates

## Result

The runner verifies:

- the mass-scan rows are under the source coordinate
  `uniform additive Dirac bare mass m_bare`;
- the serialized row keys are `slope_dE_dm_bare_tau1` and
  `slope_dE_dm_bare_by_tau`, not `dE/dh`, `T_total`, `A_top`, or `W`;
- the harness records `physical_higgs_normalization = not_derived` and
  `used_as_physical_yukawa_readout = false`;
- the existing additive-top Jacobian rows are bounded support, not strict
  subtraction rows;
- the strict subtraction packet is absent: no mixed-source total top rows, no
  strict additive-top rows, no W/Z rows, no matched covariance, no strict
  `g2`/`v`, no accepted action, and no subtracted readout certificate.

Therefore the top mass-scan rows remain support for a future same-ensemble
subtraction/covariance packet only.  They do not repair the W/Z route on the
current surface.

## Boundary

This is not a permanent no-go against the subtraction repair.  It identifies
the exact required future packet:

- `T_total`, the mixed-source total top response row;
- `A_top`, the strict additive top response row in the same coordinate
  convention;
- `W` or `Z`, production W/Z response rows under the same source shifts;
- matched covariance for `T_total`, `A_top`, `W/Z`, and `g2` or `v`;
- strict non-observed `g2` or explicit `v` authority;
- accepted same-source EW/Higgs action authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/W/Z/`y_t` or
`g2` selectors, `alpha_LM`, plaquette, `u0`, unit normalization, or
`A_top = 0` by convention.  It does not treat `dE/dm_bare` as `dE/dh`, does not
treat mass-scan support as W/Z response, and does not infer matched covariance.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_top_mass_scan_subtraction_contract_applicability_audit.py
python3 scripts/frontier_yt_pr230_top_mass_scan_subtraction_contract_applicability_audit.py
# SUMMARY: PASS=16 FAIL=0
```
