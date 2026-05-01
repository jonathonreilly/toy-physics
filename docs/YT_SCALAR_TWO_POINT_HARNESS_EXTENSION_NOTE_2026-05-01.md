# Top-Yukawa Scalar Two-Point Harness Extension

**Date:** 2026-05-01
**Status:** bounded-support / scalar two-point production-harness extension
**Runner:** `scripts/frontier_yt_scalar_two_point_harness_certificate.py`
**Smoke certificate:** `outputs/yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json`
**Certificate:** `outputs/yt_scalar_two_point_harness_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / scalar two-point production-harness extension
conditional_surface_status: conditional-support if production ensembles plus controlled pole/LSZ/canonical-Higgs normalization are later supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The harness emits finite C_ss/Gamma_ss estimates only; kappa_s still requires a controlled pole and canonical LSZ normalization."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Harness Addition

The direct-correlator production harness now accepts:

```text
--scalar-two-point-modes '0,0,0;1,0,0'
--scalar-two-point-noises N
```

When enabled, it estimates the same-source scalar two-point object:

```text
C_ss(q) = Tr[S V_q S V_-q]
Gamma_ss(q) = 1 / C_ss(q)
```

using a `Z2` stochastic trace estimator on the same additive scalar source
coordinate used by the Feynman-Hellmann response path.

Validation:

```text
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 3x6 \
  --masses 0.75 \
  --therm 0 \
  --measurements 1 \
  --separation 0 \
  --ape-steps 0 \
  --engine python \
  --scalar-two-point-modes '0,0,0;1,0,0' \
  --scalar-two-point-noises 2 \
  --output outputs/yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json

python3 scripts/frontier_yt_scalar_two_point_harness_certificate.py
# SUMMARY: PASS=9 FAIL=0
```

## Result

This is constructive route movement for the Feynman-Hellmann/LSZ path.  The
measurement object needed to determine `kappa_s` can now be emitted by the
production harness rather than only by a tiny exact standalone primitive.

The smoke output is still reduced-scope.  It does not prove a scalar pole, does
not control the continuum/finite-volume/IR limit, and does not match the source
residue to the canonical Higgs kinetic normalization used by `v`.

## Claim Boundary

This block does not authorize retained or proposed-retained top-Yukawa closure.
It does not set `kappa_s = 1`, does not use `H_unit`, does not use
`yt_ward_identity` as authority, and does not use observed top or Yukawa values
as proof selectors.

The exact next physical-response action is a production run that measures both:

- `dE_top/ds` from common-ensemble symmetric scalar-source shifts;
- same-source `C_ss(q)` across enough momentum points to fit the scalar
  denominator and compute `dGamma_ss/dp^2` at a controlled pole.
