# PR #230 FH/LSZ Noise-Subsample Diagnostics

**Status:** bounded-support / FH-LSZ noise-subsample diagnostics harness  
**Runner:** `scripts/frontier_yt_fh_lsz_noise_subsample_diagnostics_certificate.py`  
**Certificate:** `outputs/yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json`

## Question

Can the production-facing scalar two-point harness emit the diagnostic fields
needed for a future eight-mode x8/x16 variance calibration?

## Result

Yes, as instrumentation support.  The scalar-LSZ analysis now carries
`noise_subsample_stability` at the top level and in each mode row.  The
diagnostic records split-noise means and the largest half-sample real-part
delta measured in units of the stochastic stderr.

The smoke certificates were rerun and validate the field shape:

```text
scalar two-point smoke: reduced_scope, two modes, two noises
joint FH/LSZ smoke: reduced_scope, two modes, two noises
```

This does not pass the eight-mode variance gate.  The smokes are reduced-scope,
one-configuration instrumentation checks, not production variance evidence.

## Claim Boundary

```text
proposal_allowed: false
```

The diagnostic is harness plumbing only.  It does not derive `kappa_s`, does
not set `kappa_s = 1`, and does not provide same-source production pole data.

## Exact Next Action

Use the new fields in a paired eight-mode x8/x16 calibration chunk, or keep the
x16 noise plan and schedule outside the 12-hour foreground window.  Either
path still requires the combiner, isolated-pole, FV/IR/zero-mode, and
retained-proposal gates.

## Verification

```bash
python3 -m py_compile scripts/yt_direct_lattice_correlator_production.py scripts/frontier_yt_fh_lsz_noise_subsample_diagnostics_certificate.py
python3 scripts/yt_direct_lattice_correlator_production.py --volumes 3x6 --masses 0.75 --therm 0 --measurements 1 --separation 0 --ape-steps 0 --engine python --scalar-two-point-modes '0,0,0;1,0,0' --scalar-two-point-noises 2 --output outputs/yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json
python3 scripts/yt_direct_lattice_correlator_production.py --volumes 3x6 --masses 0.75 --therm 0 --measurements 1 --separation 0 --ape-steps 0 --engine python --scalar-source-shifts=-0.02,0.0,0.02 --scalar-two-point-modes '0,0,0;1,0,0' --scalar-two-point-noises 2 --output outputs/yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json
python3 scripts/frontier_yt_fh_lsz_noise_subsample_diagnostics_certificate.py
# SUMMARY: PASS=9 FAIL=0
```
