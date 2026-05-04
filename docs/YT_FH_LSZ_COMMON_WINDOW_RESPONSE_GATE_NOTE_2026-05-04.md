# YT FH/LSZ Common-Window Response Gate

Date: 2026-05-04

PR: #230

Status: bounded support / common-window response gate passed as response
support; no readout switch and no retained closure proposal is authorized.

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
- fixed-window uncertainty is production-grade under the pooled independent
  chunk-scatter estimator;
- legacy response-window acceptance remains open, but replacement response-
  stability is passed as support;
- finite-source-linearity is now available as bounded response support;
- fitted response stability remains open, but replacement response stability
  is passed as support;
- scalar-LSZ and canonical-Higgs/source-overlap gates remain open.

Therefore the response-side common-window gate is passed as support, but no
physical readout switch is authorized.

## Claim Boundary

This gate is evidence-quality hygiene.  It does not compute or derive physical
`y_t`, does not authorize replacing the production readout with a physical
Yukawa readout, and does not identify `O_sp = O_H`.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action: use the response-side support only as a parent for
scalar-LSZ pole/FV/IR/model-class work and canonical-Higgs/source-overlap
closure.  Do not request a physical `y_t` readout switch until those
independent gates pass.
