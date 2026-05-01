# Top-Yukawa Static Mass Matching Obstruction

**Date:** 2026-05-01  
**Status:** exact negative boundary / static mass matching obstruction  
**Runner:** `scripts/frontier_yt_static_mass_matching_obstruction.py`  
**Certificate:** `outputs/yt_static_mass_matching_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future static-mass matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Absolute m_t remains an open matching input on the static route."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The HQET route can avoid the current-scale `am_top >> 1` numerical obstruction
only by subtracting the heavy rest mass.  This note records the formal matching
obstruction that follows.

## Static Correlator Identity

For a static heavy correlator,

```text
C(t; am0, E) = A exp[-(am0 + E) t].
```

After the standard static rephasing,

```text
C_sub(t; E) = exp(am0 t) C(t; am0, E) = A exp[-E t].
```

The subtracted correlator no longer contains the absolute rest mass `am0`.

## Runner Result

```text
python3 scripts/frontier_yt_static_mass_matching_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The runner holds the same subtracted static correlator fixed for three
different absolute masses:

| Absolute mass | `am0` | `sqrt(2) m / v` |
|---:|---:|---:|
| `120.0 GeV` | `56.6227` | `0.689245` |
| `172.56 GeV` | `81.4234` | `0.991134` |
| `230.0 GeV` | `108.5264` | `1.321053` |

All three have identical subtracted correlators and different `y_t`.

The decomposition of the absolute mass into a bare static term and additive
residual mass is also nonunique:

```text
am0 + delta_m = constant.
```

## Consequence

A static/HQET direct route needs a real matching condition:

```text
delta_m(a) from the retained gauge action
+ conversion from static energy to SM top mass
+ no observed m_t or H_unit/Ward y_t authority as selector
```

Until that matching theorem exists, the static route is an engineering option,
not a direct retained-closure route.

## Non-Claims

- This note does not reject static/HQET simulation methods.
- This note does not produce a top mass measurement.
- This note does not define `y_t` through `H_unit`.
- This note does not use observed top mass as a selector.
