# Top-Yukawa Interacting Kinetic Background Sensitivity

**Date:** 2026-05-01  
**Status:** bounded support / interacting kinetic background sensitivity  
**Runner:** `scripts/frontier_yt_interacting_kinetic_background_sensitivity.py`  
**Certificate:** `outputs/yt_interacting_kinetic_background_sensitivity_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for future interacting kinetic-renormalization theorem or production evidence
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Interacting kinetic coefficient depends on gauge dynamics; no production ensemble or matching theorem is present."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The free Wilson-staggered action fixes the free kinetic coefficient.  This note
tests whether that free result can be used as a zero-import stand-in for the
interacting SU(3) kinetic readout.

## Result

```text
python3 scripts/frontier_yt_interacting_kinetic_background_sensitivity.py
# SUMMARY: PASS=6 FAIL=0
```

The runner measures the same momentum-projected kinetic proxy on three small
fixed backgrounds at `m=2.0`:

| background | plaquette | `M_kin(p_min)` proxy |
|---|---:|---:|
| cold | `1.000000` | `39.7541468294` |
| constant spatial phase | `1.000000` | `46.7925766809` |
| random projected `eps=0.05` | `0.9766775999` | `12.1021659111` |

The relative spread is `1.05497`.

## Consequence

The interacting kinetic coefficient is not certified by the free dispersion
alone.  Before the kinetic route can close PR #230, it needs either:

1. production ensemble measurement of the kinetic observable; or
2. a retained theorem deriving the interacting kinetic renormalization and
   lattice-to-SM matching.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
