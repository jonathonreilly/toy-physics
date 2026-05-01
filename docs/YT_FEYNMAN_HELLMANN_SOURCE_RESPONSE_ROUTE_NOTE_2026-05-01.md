# Top-Yukawa Feynman-Hellmann Source-Response Route

**Date:** 2026-05-01  
**Status:** bounded-support / alternate observable route  
**Runner:** `scripts/frontier_yt_feynman_hellmann_source_response_route.py`  
**Certificate:** `outputs/yt_feynman_hellmann_source_response_route_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for a future scalar-source normalization theorem or production response measurement
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Scalar source normalization and production response data remain open imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This route asks whether PR #230 can avoid absolute top-mass extraction by using
a Feynman-Hellmann response:

```text
dE_top / ds = <top | dH/ds | top>
```

where `s` is a uniform scalar source coupled to the top bilinear.  This is a
physical correlator route, not the old `H_unit` matrix-element definition.

## Result

```text
python3 scripts/frontier_yt_feynman_hellmann_source_response_route.py
# SUMMARY: PASS=6 FAIL=0
```

The synthetic stress test shows:

| Check | Result |
|---|---|
| energy slope recovers source charge | passes |
| additive rest mass cancels in the slope | passes |
| source rescaling changes physical readout | passes |
| observed `m_t` / `y_t` used as proof input | no |
| `H_unit` matrix-element route used | no |

The positive part is real: an energy response can remove the static
additive-mass ambiguity that blocks zero-momentum HQET-style correlators.

The remaining blocker is also real: the slope is with respect to the lattice
source `s`.  If the physical Higgs fluctuation is `h = kappa_s s`, then the
physical readout is `dE/dh = (dE/ds) / kappa_s`.  Therefore this route still
requires either a scalar source-to-canonical-Higgs normalization theorem, a
scalar LSZ residue measurement, or production response data with that matching
bridge supplied.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not define `y_t` via `H_unit`.
- This note does not import observed top mass or observed `y_t`.
- This note does not set `Z_match` or the scalar-source normalization to one.
