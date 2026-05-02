# PR #230 FH/LSZ Eight-Mode Noise Variance Gate

**Status:** open / FH-LSZ eight-mode noise variance gate not passed  
**Runner:** `scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json`

## Question

Can the pole-fit-ready eight-mode L12 plan lower the scalar-LSZ stochastic
noise count from sixteen to eight while staying production-facing?

## Result

No current-surface evidence passes that variance gate.

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

That trade can only be accepted after a same-source production calibration, or
after a theorem bounding the stochastic variance for the pole-fit modes.  The
current reduced smoke output is disqualified: it is reduced-scope, one
configuration, two modes, two noises, and the wrong volume.  The currently
running foreground chunk is four-mode/x16, and until it completes it is absent
from the combiner surface; in either case it is not an eight-mode/x8 variance
calibration.

## Claim Boundary

```text
proposal_allowed: false
variance_gate_passed: false
```

This gate is launch control only.  It does not derive `kappa_s`, does not
supply production pole data, and does not permit using reduced pilots as
production evidence.

## Exact Next Action

Either add a paired eight-mode x8/x16 calibration chunk with noise-subsample
diagnostics, or keep the x16 noise plan and schedule beyond the 12-hour
foreground window.  In both cases, any completed chunks must still pass the
combiner, pole-fit, FV/IR/zero-mode, and retained-proposal gates.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py
python3 scripts/frontier_yt_fh_lsz_eight_mode_noise_variance_gate.py
# SUMMARY: PASS=10 FAIL=0
```
