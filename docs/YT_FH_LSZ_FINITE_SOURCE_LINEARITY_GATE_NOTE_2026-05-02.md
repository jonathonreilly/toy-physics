# PR #230 FH/LSZ Finite Source-Linearity Gate

**Status:** bounded-support / finite-source-linearity gate passed as response support  
**Runner:** `scripts/frontier_yt_fh_lsz_finite_source_linearity_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json`

## Purpose

The finite source-shift derivative no-go shows that the current
`[-0.01, 0, +0.01]` response window is not enough to certify
`dE/ds|_0`.  This note turns that into an acceptance gate for future FH/LSZ
production chunks.

## Gate

Current chunks have one nonzero source radius:

```text
delta = 0.01
```

For a general odd response,

```text
S(delta) = [E(+delta)-E(-delta)]/(2 delta)
         = dE/ds|_0 + c3 delta^2 + c5 delta^4 + ...
```

one radius cannot separate the intercept from nonlinear source response.

A production-grade finite-source-linearity gate therefore requires:

- common gauge configurations across all source shifts;
- symmetric source shifts about zero;
- at least three nonzero source radii unless a retained response-bound theorem
  supplies a higher-order remainder bound;
- an accepted fit of `S(delta)` versus `delta^2`;
- scalar LSZ, FV/IR/model-class, and canonical-Higgs identity gates after the
  zero-source derivative is accepted.

## Calibration Checkpoint

The runner originally recorded a future L12 calibration command with:

```text
s in {-0.015, -0.010, -0.005, 0, +0.005, +0.010, +0.015}.
```

That calibration output is now present and consumed by the gate.  It supplies
three nonzero source radii on a common calibration ensemble and an accepted
central fit

```text
S(delta) = intercept + curvature * delta^2
```

with max fractional deviation from the intercept
`4.94991790248229e-05`.  The finite-source-linearity gate therefore passes as
response support only.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_finite_source_linearity_gate.py
# SUMMARY: PASS=15 FAIL=0
```

This does not determine `kappa_s`, scalar LSZ, FV/IR/model-class control, or
the canonical-Higgs identity.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat finite source slopes as physical `dE/dh`; it does not set
`kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use `H_unit`,
`yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`, plaquette,
or `u0` as proof authority.

## Next Action

Rerun response-window acceptance and common-window gates with finite-source
linearity available as bounded response support.  Remaining blockers are
response-window acceptance, fitted/replacement response stability, scalar LSZ,
and canonical-Higgs/source-overlap closure.
