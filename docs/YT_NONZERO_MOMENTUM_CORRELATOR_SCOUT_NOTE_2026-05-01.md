# Top-Yukawa Nonzero-Momentum Correlator Scout

**Date:** 2026-05-01  
**Status:** bounded support / nonzero-momentum correlator scout  
**Runner:** `scripts/frontier_yt_nonzero_momentum_correlator_scout.py`  
**Certificate:** `outputs/yt_nonzero_momentum_correlator_scout_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for a future heavy kinetic-mass production campaign and matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The scout uses a tiny cold gauge field and lacks production statistics plus a retained heavy matching bridge."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The heavy kinetic-mass route requires an actual nonzero-momentum correlator
measurement, not just a synthetic dispersion witness.  This scout reuses the
existing PR #230 production harness primitives:

```text
staggered Dirac builder
+ CG propagator solve on D^\dagger D
+ point-source staggered propagator
```

and adds a cos-projected momentum channel on a tiny cold gauge field.

## Runner Result

```text
python3 scripts/frontier_yt_nonzero_momentum_correlator_scout.py
# SUMMARY: PASS=7 FAIL=0
```

Key checks:

| Check | Result |
|---|---|
| production harness imported | pass |
| CG solves converge | max residual `2.266e-11` |
| momentum correlators real in the even channel | pass |
| nonzero-momentum energies order correctly | pass |
| heavier mass has smaller `p_min` splitting | pass |
| kinetic-mass extraction finite | pass |

For the tiny `4^3 x 8` cold-gauge scout, the extracted minimum-momentum
splittings are:

| bare mass | `Delta E(p_min)` | `M_kin` proxy |
|---:|---:|---:|
| `1.0` | `0.293893332451` | `3.40259505604` |
| `2.0` | `0.105654546834` | `9.46480799899` |
| `5.0` | `0.0194199170766` | `51.4935257475` |

The monotonic behavior is exactly the needed engineering signal: the
nonzero-momentum channel can expose kinetic mass information that the static
zero-momentum channel removes.

## Consequence

This is still not production evidence.  It is a lightweight method scout that
turns the heavy kinetic route into an actionable implementation task:

1. add production-mode momentum projection to the direct-correlator harness;
2. run nonzero-momentum correlators over gauge ensembles;
3. extract `E(p)-E(0)` with jackknife/bootstrap uncertainties;
4. derive matching from lattice kinetic mass to SM top mass without observed
   top calibration.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
