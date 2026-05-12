# PR230 Neutral Off-Diagonal Post-Block45 Applicability Audit

**Status:** exact negative boundary: post-Block45 artifacts do not reopen the
neutral off-diagonal generator or primitive-transfer route

**Runner:**
`scripts/frontier_yt_pr230_neutral_offdiagonal_post_block45_applicability_audit.py`

**Certificate:**
`outputs/yt_pr230_neutral_offdiagonal_post_block45_applicability_audit_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / post-Block45 artifacts do not reopen the neutral off-diagonal generator or primitive-transfer route
conditional_surface_status: conditional-support if a future same-surface physical neutral transfer/off-diagonal generator, primitive-cone certificate, strict source-Higgs row packet, or strict W/Z physical-response packet lands
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Purpose

The neutral off-diagonal generator no-go predates the latest Block43-45 source
target-time-series and tau-row audits.  This block checks whether that older
negative result is still applicable after the new evidence, rather than
closing the route by stale memory.

It also records the live-worker boundary: active or queued Schur higher-shell
production intent is not completed same-surface evidence until JSON outputs
and certificates land.

## Inputs

- Neutral off-diagonal generator derivation attempt:
  `outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json`
- Burnside / neutral multiplicity / OS-transfer gates:
  `outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json`,
  `outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json`,
  `outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json`
- Two-source primitive-transfer candidate and H3/H4 aperture:
  `outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json`,
  `outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json`
- Blocks 43-45:
  `outputs/yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json`,
  `outputs/yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json`,
  `outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json`
- Source-Higgs time-kernel manifest and aggregate gates:
  `outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json`,
  `outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json`,
  `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

## Result

The runner verifies:

- the original neutral off-diagonal no-go remains present and negative;
- finite `C_sx` support is not a physical neutral transfer;
- H3/H4 physical transfer/coupling remains absent;
- Block43 target time series do not supply neutral transfer;
- Block44 MC sample order does not supply OS/Krylov transfer;
- Block45 tau-keyed top/scalar correlators do not supply source-Higgs rows;
- no completed neutral off-diagonal, primitive-cone, source-Higgs,
  source-Higgs time-kernel, W/Z matched-response, or Schur higher-shell row
  artifact is present;
- active or queued Schur higher-shell work is not evidence until its completed
  JSON/certificates land.

## Boundary

This is not a permanent no-go against the neutral route.  It is a current
post-Block45 applicability audit.  The route reopens only with a completed
same-surface H3/H4 artifact, such as a physical neutral transfer/off-diagonal
generator, a strict primitive-cone/Burnside certificate, strict
`C_ss/C_sH/C_HH(tau)` rows with canonical `O_H` authority, or a strict W/Z
physical-response packet with absolute authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed targets,
`alpha_LM`, plaquette, or `u0`.  It does not treat finite `C_sx` covariance,
MC target time series, ordinary top tau rows, reduced smoke, or active worker
intent as a physical transfer generator or source-Higgs pole evidence.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_offdiagonal_post_block45_applicability_audit.py
python3 scripts/frontier_yt_pr230_neutral_offdiagonal_post_block45_applicability_audit.py
# SUMMARY: PASS=14 FAIL=0
```
