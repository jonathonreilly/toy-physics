# Top-Yukawa HQET Direct-Route Requirements

**Date:** 2026-05-01  
**Status:** route requirement / HQET shortcut no-go  
**Runner:** `scripts/frontier_yt_hqet_direct_route_requirements.py`  
**Certificate:** `outputs/yt_hqet_direct_route_requirements_2026-05-01.json`

```yaml
actual_current_surface_status: route requirement / no-go for HQET as zero-import shortcut
conditional_surface_status: conditional-support for a future heavy-top matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Absolute m_top is underdetermined without a heavy-mass matching theorem or external calibration."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The relativistic direct-correlator route is blocked at the current scale because
the physical top corresponds to

```text
am_top = 81.423428.
```

A natural alternative is a static or heavy-quark effective correlator.  This
note checks whether that route can determine the absolute top mass and `y_t`
without the fine lattice.

## Result

```text
python3 scripts/frontier_yt_hqet_direct_route_requirements.py
# SUMMARY: PASS=7 FAIL=0
```

The static rephasing that makes the heavy correlator tractable also removes the
absolute heavy rest mass from the normalized correlator:

```text
C_static(t) / C_static(0) = exp(-E_residual t).
```

The runner holds the normalized static correlator fixed for three different
absolute masses:

| Absolute mass | `am_abs` at current scale | `sqrt(2) m / v` |
|---:|---:|---:|
| `100.0 GeV` | `47.1856` | `0.574371` |
| `172.56 GeV` | `81.4234` | `0.991134` |
| `250.0 GeV` | `117.9639` | `1.435927` |

All three have the same normalized static correlator after mass subtraction,
but they imply different `y_t`.

## Consequence

HQET is still a possible engineering strategy for a production campaign, but it
is not a zero-import shortcut to retained closure.  It needs:

```text
static additive mass renormalization
+ lattice-HQET-to-SM top mass matching
+ uncertainty propagation into y_t = sqrt(2) m_t / v
```

Without that matching theorem or a measured calibration, the absolute top mass
is underdetermined.

## Non-Claims

- This note does not reject HQET as an engineering strategy.
- This note does not certify direct `y_t` measurement.
- This note does not use observed top mass as a proof input.
- This note does not define `y_t` through an `H_unit` matrix element.
