# PR230 MC Target-Time-Series Krylov/Transfer No-Go After Block43

**Status:** exact negative boundary: MC target time series are not a
same-surface OS transfer, Krylov generator, neutral `O_H` bridge, or
`C_sH`/`C_HH` pole-row substitute

**Runner:**
`scripts/frontier_yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43.py`

**Certificate:**
`outputs/yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / MC target time series are not a same-surface OS transfer, Krylov generator, or neutral O_H bridge
conditional_surface_status: conditional-support if future production supplies Euclidean C_ss(tau), C_sH(tau), C_HH(tau) pole rows or a same-surface neutral transfer/off-diagonal generator independent of MC configuration ordering
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Purpose

Block43 established that the complete FH-LSZ target-time-series packet is
source-coordinate support, not a same-surface neutral transfer or canonical
Higgs bridge.  Block44 closes the adjacent shortcut: interpreting the
per-configuration Monte Carlo sample order as an Euclidean time direction and
then trying to reconstruct an OS transfer kernel or Krylov/Lanczos neutral
generator from that order.

The packet is useful production support for ensemble means, variances,
autocorrelation/ESS, and source-coordinate target statistics.  Its
`configuration_index` is run-control metadata.  It is not an operator
time-separation coordinate.

## Inputs

- Full FH-LSZ L12 target-time-series checkpoint:
  `outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json`
- Block43 full target-time-series neutral-transfer lift no-go:
  `outputs/yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json`
- FH-LSZ target-time-series Higgs-identity no-go:
  `outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json`
- FH-LSZ autocorrelation ESS gate:
  `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`
- OS transfer-kernel artifact gate:
  `outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json`
- Same-surface neutral multiplicity-one gate:
  `outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json`
- Full assembly and campaign status gates:
  `outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json`,
  `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

## Result

The runner checks all 63 production chunks and verifies the target-time-series
schema:

- expected source modes are present;
- each mode carries 16 samples;
- samples are indexed by `configuration_index`;
- no row supplies `tau`, `time_separation`, `euclidean_time`, source/sink time,
  transfer-kernel, Krylov-basis, Lanczos-tridiagonal, `C_sH`, or `C_HH` keys.

It then builds a deterministic permutation witness on chunk001, mode `0,0,0`.
Reversing or sorting the same `C_ss` sample multiset preserves the ensemble
mean and variance, but changes the lag-one covariance.  Therefore any
transfer/Krylov construction that depends on the MC sample order would depend
on arbitrary run-control ordering rather than an operator-time separation.

## Boundary

This is not a no-go against future source-Higgs closure.  It is a no-go
against one current-surface shortcut:

- MC target time series are source-coordinate ensemble samples;
- MC configuration order is not Euclidean operator time;
- MC autocorrelation is not an OS transfer kernel;
- `C_ss` samples are not strict `C_sH`/`C_HH` pole rows;
- Krylov/Lanczos reconstruction needs a physical Euclidean correlation matrix
  or an explicit same-surface neutral transfer/off-diagonal generator.

The route reopens if future production supplies physical Euclidean-time
`C_ij(tau)` rows, strict `C_ss/C_sH/C_HH` pole residues with scalar-LSZ/FV/IR
control, or a same-surface neutral transfer primitive independent of MC
configuration ordering.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed targets,
`alpha_LM`, plaquette, or `u0`.  It does not treat `dE/ds` as `dE/dh`, set
`kappa_s`, `c2`, `g2`, `Z_match`, or any overlap to one, treat MC
autocorrelation as OS transfer, or relabel source-only `C_ss` samples as
`C_sH`/`C_HH` evidence.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43.py
python3 scripts/frontier_yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43.py
# SUMMARY: PASS=17 FAIL=0
```
