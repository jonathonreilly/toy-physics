# Top-Yukawa Direct-Correlator Momentum Harness Extension

**Date:** 2026-05-01  
**Status:** bounded support / production-harness extension  
**Harness:** `scripts/yt_direct_lattice_correlator_production.py`  
**Smoke certificate:** `outputs/yt_direct_lattice_correlator_momentum_harness_smoke_2026-05-01.json`
**Validation runner:** `scripts/frontier_yt_momentum_harness_extension_certificate.py`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for future production nonzero-momentum kinetic-mass evidence
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The extension adds measurement machinery only; no production ensemble or heavy matching theorem is supplied."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## What Changed

The PR #230 production harness now supports optional momentum-projected
correlators via:

```text
--momentum-modes '0,0,0;1,0,0;1,1,0'
```

The implementation reuses the existing staggered Dirac construction and CG
propagator inversion, then records:

- cos-projected momentum correlators for the selected mass point;
- effective energies for each momentum channel;
- kinetic-mass proxies from `E(p)-E(0)`.

## Smoke Run

```text
python3 scripts/yt_direct_lattice_correlator_production.py \
  --volumes 4x8 \
  --masses 2.0 \
  --therm 0 \
  --measurements 1 \
  --separation 0 \
  --overrelax 0 \
  --ape-steps 0 \
  --momentum-modes '0,0,0;1,0,0;1,1,0' \
  --output outputs/yt_direct_lattice_correlator_momentum_harness_smoke_2026-05-01.json \
  --production-output-dir outputs/yt_direct_lattice_correlator_momentum_smoke \
  --engine python
```

The smoke certificate is deliberately reduced-scope.  It proves only that the
production harness can emit momentum-analysis fields.

Validation:

```text
python3 scripts/frontier_yt_momentum_harness_extension_certificate.py
# SUMMARY: PASS=6 FAIL=0
```

Smoke kinetic proxies:

| momentum | `Delta E` | `M_kin` proxy |
|---|---:|---:|
| `(1,0,0)` | `0.0251546085064` | `39.7541468294` |
| `(1,1,0)` | `0.0482879340015` | `41.4182143294` |

The large errors are expected for a one-configuration cold-gauge smoke run.

## Consequence

The heavy kinetic route is now an implementation route, not just a paper route.
The remaining blockers are unchanged:

1. production gauge ensembles with momentum projection enabled;
2. heavy-action or lattice-HQET/NRQCD matching from `M_kin` to SM `m_t`;
3. uncertainty propagation into `y_t = sqrt(2) m_t / v`.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
