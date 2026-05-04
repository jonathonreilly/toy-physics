# PR #230 FH/LSZ Pole-Fit Mode/Noise Budget

**Status:** bounded-support / FH-LSZ pole-fit mode-noise budget  
**Runner:** `scripts/frontier_yt_fh_lsz_pole_fit_mode_budget.py`  
**Certificate:** `outputs/yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json`

## Question

Can an L12 foreground chunk use enough scalar-LSZ momentum shells for a pole
fit without exceeding the current 12-hour chunk budget?

## Result

The current four-mode, sixteen-noise plan fits the foreground estimate but is
not pole-fit ready:

```text
current four modes x16 noises: 11.3186 hours, one nonzero shell
```

An eight-mode, sixteen-noise plan is pole-fit kinematics ready, but does not
fit the foreground window:

```text
eight modes x16 noises: 21.45 hours
```

An eight-mode, eight-noise plan keeps the same solve-budget factor as the
current four-mode/sixteen-noise plan:

```text
eight modes x8 noises: 11.3186 hours
```

This is a constructive launch option, not evidence.  The paired x8/x16
variance calibration now passes and accepts the eight-mode/x8 setting as
launch support only.  Future eight-mode chunks must not be combined as a
homogeneous pole-fit ensemble with the four-mode chunk set, and the result
still needs production completion, pole/model-class control, FV/IR control,
canonical-Higgs/source-overlap closure, and retained-proposal certification.

## Claim Boundary

```text
proposal_allowed: false
```

The mode/noise trade does not derive `kappa_s`, does not supply production
data, and does not replace the isolated-pole, FV/IR/zero-mode, or
retained-proposal gates.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_pole_fit_mode_budget.py
python3 scripts/frontier_yt_fh_lsz_pole_fit_mode_budget.py
# SUMMARY: PASS=10 FAIL=0
```
