# Top-Yukawa Joint Feynman-Hellmann / Scalar-LSZ Harness Certificate

**Date:** 2026-05-01
**Status:** bounded-support / joint Feynman-Hellmann scalar-LSZ harness
**Runner:** `scripts/frontier_yt_fh_lsz_joint_harness_certificate.py`
**Smoke certificate:** `outputs/yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json`
**Certificate:** `outputs/yt_fh_lsz_joint_harness_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / joint Feynman-Hellmann scalar-LSZ harness
conditional_surface_status: conditional-support if production data plus controlled scalar-pole LSZ/canonical-Higgs normalization are supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Joint observable plumbing is present, but kappa_s and production pole/response evidence remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Joint Observable Bundle

The production harness can now emit both physical-response ingredients in one
run:

```text
dE_top/ds from symmetric scalar-source shifts
C_ss(q) = Tr[S V_q S V_-q]
Gamma_ss(q) = 1 / C_ss(q)
```

Smoke command:

```text
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 3x6 \
  --masses 0.75 \
  --therm 0 \
  --measurements 1 \
  --separation 0 \
  --ape-steps 0 \
  --engine python \
  --scalar-source-shifts=-0.02,0.0,0.02 \
  --scalar-two-point-modes '0,0,0;1,0,0' \
  --scalar-two-point-noises 2 \
  --output outputs/yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json

python3 scripts/frontier_yt_fh_lsz_joint_harness_certificate.py
# SUMMARY: PASS=10 FAIL=0
```

## Result

This is constructive measurement support.  The exact production bundle needed
for the physical-response route is now represented by one harness path:

- measure `dE_top/ds` on common gauge configurations;
- measure same-source `C_ss(q)`/`Gamma_ss(q)` on those configurations;
- fit the scalar denominator and pole derivative;
- derive `kappa_s` by canonical-Higgs LSZ normalization;
- only then convert `dE_top/ds` to physical `dE_top/dh`.

## Claim Boundary

The smoke output is reduced-scope.  It is not production evidence, not a
controlled pole fit, and not a canonical Higgs normalization theorem.  It does
not set `kappa_s = 1`, does not use `H_unit`, does not use `yt_ward_identity`
as authority, and does not use observed top or Yukawa values as proof
selectors.
