# Top-Yukawa Heavy Kinetic-Mass Matching Obstruction

**Date:** 2026-05-01  
**Status:** exact negative boundary / heavy kinetic matching obstruction  
**Runner:** `scripts/frontier_yt_heavy_kinetic_matching_obstruction.py`  
**Certificate:** `outputs/yt_heavy_kinetic_matching_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future heavy-action and lattice-to-SM matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The kinetic-action coefficient and lattice-to-SM matching factor remain open imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The nonzero-momentum route measures an energy splitting:

```text
Delta E(p) = E(p) - E(0).
```

That cancels the additive static rest mass.  This note checks whether the
splitting alone is enough to identify the SM top mass.

It is not.  The splitting fixes a kinetic combination unless the heavy-action
coefficient and lattice-to-SM matching are independently derived.

## Runner Result

```text
python3 scripts/frontier_yt_heavy_kinetic_matching_obstruction.py
# SUMMARY: PASS=5 FAIL=0
```

The runner holds a measured splitting fixed:

```text
p_hat^2 = 2
Delta E = 0.05
```

and shows that multiple kinetic-action pairs give the same splitting:

| `c2` | `M0_lat` | `Delta E` |
|---:|---:|---:|
| `0.5` | `10` | `0.05` |
| `1.0` | `20` | `0.05` |
| `2.0` | `40` | `0.05` |

Thus assuming `c2 = 1` is a hidden action-normalization premise unless that
coefficient is derived on the PR #230 substrate.

Even after a lattice kinetic mass is extracted, a matching factor changes the
SM mass and Yukawa readout while leaving the measured splitting fixed.

## Consequence

The heavy kinetic route remains the most concrete lightweight compute route,
but retained closure requires:

1. a theorem fixing the heavy kinetic-action coefficient `c2`;
2. a lattice-HQET/NRQCD-to-SM mass matching theorem that does not calibrate to
   the observed top mass;
3. production `E(p)-E(0)` data with uncertainty propagation;
4. only then, `y_t = sqrt(2) m_t / v`, with `v` treated as substrate input.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
