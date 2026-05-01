# Top-Yukawa Heavy Kinetic-Mass Route Scout

**Date:** 2026-05-01  
**Status:** bounded support / heavy kinetic-mass route  
**Runner:** `scripts/frontier_yt_heavy_kinetic_mass_route.py`  
**Certificate:** `outputs/yt_heavy_kinetic_mass_route_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for a future nonzero-momentum heavy-correlator campaign and matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "No production nonzero-momentum correlator data or retained heavy-action matching theorem is present."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The static/HQET obstruction showed why a zero-momentum static correlator cannot
determine the absolute top mass: the additive rest mass can be rephased away.
This note tests the natural successor observable:

```text
E(p) - E(0) ~= p_hat^2 / (2 M_kin).
```

The additive rest-mass shift cancels in the energy difference, so a kinetic
mass can in principle be extracted without calibrating the static offset to the
observed top mass.

## Runner Result

```text
python3 scripts/frontier_yt_heavy_kinetic_mass_route.py
# SUMMARY: PASS=6 FAIL=0
```

The runner uses a synthetic lattice-NRQCD dispersion as a route witness, not as
physical data.  It verifies:

| Check | Result |
|---|---|
| scan over masses, shifts, and momenta runs | pass |
| additive mass shift cancels from `M_kin` | pass |
| low-momentum splittings recover `M_kin` | pass |
| pure static limit has no kinetic readout | pass |
| top-like heavy splitting is precision demanding | pass |

For a heavy dimensionless mass `M_kin = 80` on `L = 24`, the minimal momentum
splitting is

```text
Delta E(p_min) = 0.000425926
```

so a one-percent kinetic-mass extraction needs absolute energy-splitting
precision at roughly the `4.3e-6` level in lattice units.

## Consequence

This is a real route around the static additive-mass obstruction, but it is not
retained closure.  The missing artifacts are now explicit:

1. implement nonzero-momentum top/HQET correlator measurement;
2. include or derive the `1/M` kinetic operator on the `Cl(3)/Z^3` substrate;
3. extract `E(p)-E(0)` with jackknife/bootstrap errors;
4. derive matching from lattice `M_kin` to the SM top mass without observed-top
   calibration;
5. propagate the resulting mass through `y_t = sqrt(2) m_t / v`, with `v` as
   substrate input.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
