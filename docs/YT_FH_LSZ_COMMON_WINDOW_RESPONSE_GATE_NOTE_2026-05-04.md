# YT FH/LSZ Common-Window Response Gate

Date: 2026-05-04

PR: #230

Status: open / response-gate contract; no readout switch and no retained
closure proposal is authorized.

## Purpose

The common-window provenance audit showed that the current fitted `dE/ds`
instability is driven by mixed source-shift fit windows.  This note records the
predeclared gate that would be required before a fixed common window could be
used as a physical response readout.

## Gate Criteria

A common-window readout request must satisfy all of the following before any
physics readout switch can be considered:

- stable fixed-window central response;
- production-grade fixed-window uncertainty;
- response-window acceptance gate passed;
- finite-source-linearity gate passed;
- fitted-response or replacement-readout stability passed;
- scalar-LSZ and canonical-Higgs/source-overlap closure supplied separately.

## Current Result

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_common_window_response_gate.py
# SUMMARY: PASS=12 FAIL=0
```

Current surface:

- fixed `tau=10..12` central response is stable;
- fixed-window uncertainty is not production-grade;
- response-window acceptance remains open;
- finite-source-linearity remains open;
- fitted response stability remains open;
- scalar-LSZ and canonical-Higgs/source-overlap gates remain open.

Therefore the gate is not passed and no readout switch is authorized.

## Claim Boundary

This gate is evidence-quality hygiene.  It does not compute or derive physical
`y_t`, does not replace the production readout, and does not identify
`O_sp = O_H`.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action: improve the fixed-window estimator until the common-window
response is production-grade, then pass finite-source-linearity and
response-window acceptance before any readout-switch request.  This still
remains downstream of scalar-LSZ and canonical-Higgs/source-overlap closure.
