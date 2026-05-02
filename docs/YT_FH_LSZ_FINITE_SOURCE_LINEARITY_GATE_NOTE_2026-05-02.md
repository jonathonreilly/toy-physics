# PR #230 FH/LSZ Finite Source-Linearity Gate

**Status:** open / FH-LSZ finite-source-linearity gate not passed  
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

## Calibration Manifest

The runner records a future L12 calibration command with:

```text
s in {-0.015, -0.010, -0.005, 0, +0.005, +0.010, +0.015}.
```

That manifest is planning support only.  Under the current source-count cost
model it projects beyond the 12-hour foreground window for one 16-measurement
L12 chunk, and it still would not determine `kappa_s` or the canonical-Higgs
identity.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat finite source slopes as physical `dE/dh`; it does not set
`kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use `H_unit`,
`yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`, plaquette,
or `u0` as proof authority.

## Next Action

Either schedule the multi-radius finite-source-linearity calibration with a
retained response-bound acceptance rule, or keep current single-radius chunks
as diagnostics while attacking scalar LSZ / canonical-Higgs identity directly.
