# Top-Yukawa Production Resource Projection

**Date:** 2026-05-01  
**Status:** bounded support / production resource projection  
**Runner:** `scripts/frontier_yt_production_resource_projection.py`  
**Certificate:** `outputs/yt_production_resource_projection_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for planning the strict production run
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Resource projection is not measurement evidence and does not supply matching."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The direct measurement route remains one of the two honest PR #230 closure
routes.  This note converts the existing `12^3 x 24` numba mass-bracket run into
a production-scale resource estimate.

## Result

```text
python3 scripts/frontier_yt_production_resource_projection.py
# SUMMARY: PASS=7 FAIL=0
```

Benchmark:

| Quantity | Value |
|---|---:|
| benchmark volume | `12^3 x 24` |
| benchmark runtime | `566.650803 s` |
| benchmark protocol | `50` therm, `25` measurements, separation `5` |
| effective sweeps | `175` |
| seconds / effective sweep | `3.23800` |

Production protocol:

```text
1000 thermalization sweeps
1000 measurement configurations
20 sweeps between measurements
3 fermion bare-mass values
```

The projection is multi-day single-worker wall-clock across the three requested
volumes.  This is a planning result only; it is not production evidence.

## Non-Claims

- This note is not production data.
- This note is not a `y_t` derivation.
- This note does not make the strict runner pass.
- This note does not supply lattice-to-SM matching.
- This note does not use `H_unit` matrix-element authority.
