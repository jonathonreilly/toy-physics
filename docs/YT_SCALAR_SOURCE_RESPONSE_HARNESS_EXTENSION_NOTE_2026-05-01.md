# Top-Yukawa Scalar-Source Response Harness Extension

**Date:** 2026-05-01
**Status:** bounded-support / scalar source response harness extension
**Runner:** `scripts/frontier_yt_scalar_source_response_harness_certificate.py`
**Certificate:** `outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support if production response data and scalar LSZ/canonical normalization are later supplied
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The harness extracts dE/ds only; kappa_s and production response data remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Result

The direct-correlator production harness now accepts explicit uniform scalar
source shifts:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 2x4 \
  --masses 0.75 \
  --scalar-source-shifts=-0.02,0.0,0.02 \
  --therm 0 \
  --measurements 1 \
  --separation 0 \
  --ape-steps 0 \
  --engine python \
  --output outputs/yt_direct_lattice_correlator_scalar_source_response_smoke_2026-05-01.json
```

The emitted certificate contains `scalar_source_response_analysis` with
energy fits versus the additive lattice source coordinate `s`, where the
fermion operator uses `m_bare + s`.

Validation:

```text
python3 scripts/frontier_yt_scalar_source_response_harness_certificate.py
# SUMMARY: PASS=8 FAIL=0
```

## Claim Boundary

This is an implementation and observable-design advance for the
Feynman-Hellmann route.  It is not retained closure:

- the measured slope is `dE/ds`, not physical `dE/dh`;
- `h = kappa_s s` remains open;
- `kappa_s = 1` is forbidden unless derived by scalar LSZ/canonical
  normalization;
- the smoke run is reduced-scope and not production evidence;
- any lattice-to-SM response matching must be derived and cannot be set to one.

The next physical-response route needs production source-response data plus a
scalar source-to-canonical-Higgs normalization theorem or direct scalar-residue
measurement.
