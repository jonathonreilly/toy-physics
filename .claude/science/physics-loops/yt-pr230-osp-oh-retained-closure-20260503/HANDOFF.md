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
