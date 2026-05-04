# PR #230 FH/LSZ Eight-Mode Noise Variance Gate

**Status:** bounded-support / FH-LSZ eight-mode noise variance gate passed for launch support  
**Runner:** `scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json`

## Question

Can the pole-fit-ready eight-mode L12 plan lower the scalar-LSZ stochastic
noise count from sixteen to eight while staying production-facing?

## Result

The paired x8/x16 calibration stream now passes the variance gate as launch
support.

The mode/noise budget found that eight modes with eight noises fit the current
foreground estimate:

```text
eight modes x8 noises: 11.3186 hours
```

But lowering from sixteen to eight stochastic vectors raises the noise-only
standard error by:

```text
sqrt(16 / 8) = 1.41421
```

That trade has now been accepted only for future pole-fit launch support after
the same-source production calibration passed:

```text
outputs/yt_pr230_fh_lsz_variance_calibration_L12_T24_x8_2026-05-01.json
outputs/yt_pr230_fh_lsz_variance_calibration_L12_T24_x16_2026-05-01.json
```

The consumable calibration contract is now the paired x8/x16 gate:

```text
scripts/frontier_yt_fh_lsz_paired_variance_calibration_gate.py
outputs/yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json
```

The eight-mode variance gate reads that paired certificate and marks x8 as
pole-fit launch support only. It still does not authorize retained/proposed-
retained `y_t` wording.

## Claim Boundary

```text
proposal_allowed: false
variance_gate_passed: true
```

This gate is launch control only.  It does not derive `kappa_s`, does not
supply production pole data, and does not permit using reduced pilots as
production evidence.

## Exact Next Action

Use the x8 setting only if a separate eight-mode pole-fit stream is launched.
Any such stream must still pass combiner, pole-fit, FV/IR/zero-mode,
model-class, source-Higgs/canonical-operator, and retained-proposal gates.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py
python3 scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py
# SUMMARY: PASS=11 FAIL=0
```
