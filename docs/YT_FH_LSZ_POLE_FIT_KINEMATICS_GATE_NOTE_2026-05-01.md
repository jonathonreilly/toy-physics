# PR #230 FH/LSZ Pole-Fit Kinematics Gate

**Status:** open / FH-LSZ scalar-pole kinematics gate blocks four-mode manifest as pole-fit evidence  
**Runner:** `scripts/frontier_yt_fh_lsz_pole_fit_kinematics_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json`

## Question

Can the current FH/LSZ scalar two-point momentum set, by itself, supply the
isolated scalar-pole derivative required by the same-source readout theorem?

## Result

No.  The manifests measure:

```text
0,0,0
1,0,0
0,1,0
0,0,1
```

On a cubic volume the three one-step axis modes are the same `p_hat^2` shell.
So each volume has only two shells total: `q=0` and one nonzero shell.  That can
form a finite positive-momentum secant for `Gamma_ss(q)`, but it cannot locate
an isolated scalar pole, determine `dGamma_ss/dp^2` at that pole, or control a
continuum remainder without importing a model.

## Claim Boundary

```text
proposal_allowed: false
```

This does not reject the current chunks as measurement support.  It blocks a
future completed four-mode chunk set from being treated as the scalar LSZ pole
derivative.  Retained closure still needs richer pole-fit kinematics or a
theorem, plus FV/IR/zero-mode control and the retained-proposal gate.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_pole_fit_kinematics_gate.py
python3 scripts/frontier_yt_fh_lsz_pole_fit_kinematics_gate.py
# SUMMARY: PASS=7 FAIL=0
```
