# Top-Yukawa Momentum Pilot Scaling Note

**Date:** 2026-05-01  
**Status:** bounded support / momentum pilot scaling  
**Pilot certificate:** `outputs/yt_direct_lattice_correlator_momentum_pilot_certificate_2026-05-01.json`  
**Validation runner:** `scripts/frontier_yt_momentum_pilot_scaling_certificate.py`  
**Validation certificate:** `outputs/yt_momentum_pilot_scaling_certificate_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for future production momentum-enabled correlator evidence
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Reduced-scope cold-gauge pilot with large finite-volume drift and no matching theorem."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

After adding `--momentum-modes` support to the production harness, this pilot
tests the kinetic route on small cold volumes:

```text
4^3 x 8
6^3 x 12
8^3 x 16
```

with one configuration per volume and three bare masses.  This is intentionally
not production evidence.

## Runner Result

```text
python3 scripts/frontier_yt_momentum_pilot_scaling_certificate.py
# SUMMARY: PASS=8 FAIL=0
```

The selected-mass `p_min` kinetic proxies are:

| volume | `Delta E(p_min)` | `M_kin` proxy |
|---|---:|---:|
| `4^3 x 8` | `0.0251546085064` | `39.7541468294` |
| `6^3 x 12` | `0.0295401199162` | `16.9261330495` |
| `8^3 x 16` | `0.0176967906734` | `16.5506404081` |

The full relative spread is `0.950562`, which is far too large for a strict
result.  The larger cold volumes are roughly consistent with each other, with
`L=6`/`L=8` relative spread `0.022433`, but that is still a cold-gauge,
one-configuration scaling hint rather than production evidence.

## Consequence

The pilot confirms the implementation path and just as importantly confirms
that reduced-scope cold-gauge data cannot be certified as production.  The
kinetic route still requires:

1. gauge ensembles with real statistics;
2. controlled finite-volume and finite-spacing treatment;
3. a derived heavy-action coefficient and matching theorem;
4. uncertainty propagation into `m_t` and `y_t`.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
