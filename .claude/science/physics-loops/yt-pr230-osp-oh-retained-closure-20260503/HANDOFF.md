# Handoff

Block 1 completed the required first-principles stretch attempt on the live
`O_sp/O_H` blocker.

Result: no positive retained closure.  The current PR230 surface cannot derive
`O_sp = O_H` from source-only data, taste isotropy, static EW Higgs algebra,
one-Higgs monomial selection, D17/H_unit support, or current rank-one gates.

The new counterfamily keeps `O_sp` unit-normalized and the same-source top
readout fixed while varying the canonical-Higgs overlap and a finite
orthogonal neutral top coupling.  It would be distinguished by `C_sH/C_HH`
Gram purity, a W/Z response row, or a real dynamical rank-one neutral-scalar
theorem.

Verification:

```bash
python3 scripts/frontier_yt_osp_oh_identity_stretch_attempt.py
# SUMMARY: PASS=21 FAIL=0

python3 scripts/frontier_yt_pr230_source_overlap_route_selection.py
# SUMMARY: PASS=15 FAIL=0
```

Next exact action: pursue the highest-ranked positive route, source-Higgs Gram
purity with `O_sp` as the normalized source side.

## Finite-Source Calibration Checkpoint

The active multi-radius finite-source-linearity production job is now tracked
by `scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py`
and `outputs/yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json`.

Current result:

```bash
python3 scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py
# SUMMARY: PASS=7 FAIL=0
```

The checkpoint is still open because
`outputs/yt_pr230_fh_lsz_finite_source_linearity_L12_T24_calib001_2026-05-02.json`
has not landed.  When it finishes, rerun the calibration checkpoint,
response-window acceptance gate, retained-route certificate, and campaign
status certificate.  This remains response-window support only and does not
authorize retained/proposed-retained closure.

## Source-Higgs Contract Witness

The selected source-Higgs Gram-purity route now has an in-memory contract
witness:

```bash
python3 scripts/frontier_yt_source_higgs_gram_purity_contract_witness.py
# SUMMARY: PASS=12 FAIL=0
```

It verifies that a fully firewalled future pure O_sp-Higgs pole-residue
candidate would pass the postprocessor, while mixed, Ward-import, and
no-retained-route candidates are rejected.  Current production rows remain
absent, so this is exact support for the future acceptance surface only.

## 2026-05-04 Route Sweep Checkpoint

I refreshed the next queued closure routes while chunks027/028 and the
finite-source-linearity calibration job continued running.

Verification:

```bash
python3 scripts/frontier_yt_wz_response_measurement_row_contract_gate.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_same_source_wz_response_certificate_gate.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_wz_response_repo_harness_import_audit.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_neutral_scalar_dynamical_rank_one_closure_attempt.py
# SUMMARY: PASS=17 FAIL=0

python3 scripts/frontier_yt_pr230_source_overlap_route_selection.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# PASSing open certificate

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=166 FAIL=0
```

Result: no positive retained closure.  The W/Z route has a row-level contract
and certificate gate, but no W/Z response rows or harness exist.  The
rank-one route has conditional Perron support, but the direct positivity-
improving theorem is blocked by neutral-sector irreducibility.  The scalar
denominator / K-prime route has exact Schur-complement sufficiency and a row
contract, but no same-surface Schur A/B/C rows exist.

Live production sessions remain the immediate actionable path.  When
chunks027/028 or the finite-source calibration output land, rerun their gates
and then the aggregate retained/campaign certificates before updating the PR.

## 2026-05-04 Chunk029-030 Launch

With 10 CPU cores available, load near 4, and no duplicate chunk029/030
outputs present, I launched the next seed-controlled L12 pair:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 12x24 --masses 0.45,0.75,1.05 \
  --therm 1000 --measurements 16 --separation 20 \
  --engine numba --production-targets \
  --scalar-source-shifts=-0.01,0.0,0.01 \
  --scalar-two-point-modes '0,0,0;1,0,0;0,1,0;0,0,1' \
  --scalar-two-point-noises 16 \
  --production-output-dir outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk029 \
  --seed 2026051029 \
  --output outputs/yt_pr230_fh_lsz_production_L12_T24_chunk029_2026-05-01.json

python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 12x24 --masses 0.45,0.75,1.05 \
  --therm 1000 --measurements 16 --separation 20 \
  --engine numba --production-targets \
  --scalar-source-shifts=-0.01,0.0,0.01 \
  --scalar-two-point-modes '0,0,0;1,0,0;0,1,0;0,0,1' \
  --scalar-two-point-noises 16 \
  --production-output-dir outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk030 \
  --seed 2026051030 \
  --output outputs/yt_pr230_fh_lsz_production_L12_T24_chunk030_2026-05-01.json
```

Runtime PIDs at launch: chunk029 `81569`, chunk030 `81570`.  Monitor session
`45782` watches both outputs and will run the chunk target-timeseries,
multi-tau, combiner, ESS/autocorrelation, response-window, retained-route, and
campaign-status gates when both files land.

Claim boundary: these are production-support chunks only.  They do not
authorize retained/proposed-retained closure without the downstream scalar
LSZ, source-Higgs/WZ/rank-one, and retained-route gates.

## 2026-05-04 Chunk027-028 Packaging

Chunks027/028 landed and were repackaged after rerunning the stale generic
checkpoints against the updated 28-chunk combiner state.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 27
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 28
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_multitau_target_timeseries_checkpoint.py --chunk-index 27
# SUMMARY: PASS=19 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_multitau_target_timeseries_checkpoint.py --chunk-index 28
# SUMMARY: PASS=19 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_forensics.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=140 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=166 FAIL=0
```

Current production state: 28/63 L12 chunks ready, 448/1000 saved
configurations, target-observable ESS passed with limiting ESS
`387.5962268377635`, response-window acceptance still open, and retained
closure still unauthorized.

Next exact action: keep monitoring chunks029/030 and the finite-source
calibration job. When either lands, rerun the appropriate local gates and the
aggregate retained/campaign certificates before packaging the next checkpoint.

## 2026-05-04 Finite-Source Calibration Packaging

The multi-radius finite-source-linearity calibration output landed and was
processed:

```bash
python3 scripts/frontier_yt_fh_lsz_finite_source_linearity_calibration_checkpoint.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=140 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=166 FAIL=0
```

The calibration uses source shifts
`[-0.015, -0.01, -0.005, 0.0, 0.005, 0.01, 0.015]` and source radii
`[0.005, 0.01, 0.015]`.  The zero-source intercept fit is
`1.4328344029594695 +/- 35.72880463605988`, with maximum fractional deviation
from the intercept `4.94991790248229e-05`.

This retires the calibration awaiting-output state only.  The response-window
acceptance gate remains open, and retained closure is still unauthorized.

Next exact action: keep monitoring chunks029/030 and package them when their
outputs land.
