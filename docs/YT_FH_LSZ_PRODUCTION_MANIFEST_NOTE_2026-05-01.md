# Top-Yukawa Joint FH/LSZ Production Manifest

**Date:** 2026-05-01
**Status:** bounded-support / joint FH-LSZ production manifest
**Runner:** `scripts/frontier_yt_fh_lsz_production_manifest.py`
**Certificate:** `outputs/yt_fh_lsz_production_manifest_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / joint FH-LSZ production manifest
conditional_surface_status: production-planning support only
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "A command manifest is not production evidence and does not derive kappa_s."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Manifest

The runner converts the existing FH production protocol, joint harness
certificate, and joint resource projection into exact production commands for:

- `12x24`;
- `16x32`;
- `24x48`.

Each command includes masses `0.45,0.75,1.05`, scalar source shifts
`-0.01,0.0,0.01`, same-source scalar two-point modes
`0,0,0;1,0,0;0,1,0;0,0,1`, 16 scalar two-point noise vectors, 1000
thermalization sweeps, 1000 saved configurations, separation 20,
`--production-targets`, and `--resume`.

Validation:

```text
python3 scripts/frontier_yt_fh_lsz_production_manifest.py
# SUMMARY: PASS=9 FAIL=0
```

## Claim Boundary

This is launch planning, not evidence.  The projected joint route remains about
`3630.28` single-worker hours before pole-fit and autocorrelation tuning.  The
postprocess gates still require production certificates, correlated `dE/ds`
fits, same-source `Gamma_ss(q)` pole fits, finite-volume/IR/zero-mode control,
and a retained-proposal certificate before any retained wording is allowed.
