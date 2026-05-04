# YT FH/LSZ Paired Variance Calibration Completion Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded launch support only; closure proposal is not authorized.

## Scope

The paired x8/x16 variance-calibration stream completed for the eight-mode
pole-fit launch shape. The purpose was narrow: check whether the eight-mode
x8 scalar-LSZ stochastic plan can be accepted for future pole-fit launch
support by comparing it to the same-source x16 run.

This is not physical `y_t` evidence. It does not provide a scalar pole
identity, finite-volume or IR control, model-class closure, source-Higgs
overlap, or a canonical `O_H` certificate.

## Production Outputs

x8 calibration:

- output: `outputs/yt_pr230_fh_lsz_variance_calibration_L12_T24_x8_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_variance_calibration/L12_T24_x8/L12xT24/ensemble_measurement.json`
- seed: `2026051801`
- runtime: `3910.5432710647583` seconds
- scalar two-point noises: `8`
- scalar two-point modes: `[[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 0, 0], [2, 1, 0], [2, 1, 1], [2, 2, 0]]`
- source slope: `6.64547882321856`
- source slope error: `13.517312027498434`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.925512747229414 GeV`, `y_t(v) = 0.022546995604941784`

x16 calibration:

- output: `outputs/yt_pr230_fh_lsz_variance_calibration_L12_T24_x16_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_variance_calibration/L12_T24_x16/L12xT24/ensemble_measurement.json`
- seed: `2026051801`
- runtime: `4842.528575897217` seconds
- scalar two-point noises: `16`
- scalar two-point modes: `[[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1], [2, 0, 0], [2, 1, 0], [2, 1, 1], [2, 2, 0]]`
- source slope: `6.64547882321856`
- source slope error: `13.517312027498434`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.925512747229414 GeV`, `y_t(v) = 0.022546995604941784`

The gate compares the paired outputs under the manifest contract. The matched
central rows pass the configured stability thresholds, so x8 can be used as
bounded launch support for a later pole-fit stream. The identical seed is part
of the same-source calibration design and must not be treated as independent
physics replication.

## Certificates

- `outputs/yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json`:
  `PASS=8 FAIL=0`, `variance_calibration_gate_passed=true`
- `outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json`:
  `PASS=11 FAIL=0`, `variance_gate_passed=true`
- retained-route certificate: `PASS=155 FAIL=0`
- campaign-status certificate: `PASS=181 FAIL=0`

## Claim Boundary

The calibration does not derive `kappa_s`, `Z_match`, `c2`, `cos(theta)`,
source-Higgs overlap, scalar LSZ normalization, scalar-pole FV/IR control,
model-class closure, or a physical `y_t` readout.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue the L12 chunk stream through chunks057-063, then
run the next retained-closure gates over the complete `63/63` L12 support
surface before deciding whether a separate eight-mode pole-fit stream is worth
launching. PR #230 remains draft/open.
