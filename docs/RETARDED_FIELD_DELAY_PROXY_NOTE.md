# Retarded Field Delay Proxy

**Date:** 2026-04-05
**Status:** bounded retarded-field intermediate-layer phase-lag probe

## Artifact chain

- [`scripts/retarded_field_delay_proxy_probe.py`](/Users/jonreilly/Projects/Physics/scripts/retarded_field_delay_proxy_probe.py)
- [`logs/2026-04-05-retarded-field-delay-proxy-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-retarded-field-delay-proxy-probe.txt)

## Question

Can a minimal retarded-field extension produce a compact intermediate-layer
phase lag while still reducing to the instantaneous weak-field baseline at
`mix = 0`?

This note is intentionally narrow:

- one retarded-field blend parameter `mix`
- one observable: phase lag at a fixed intermediate probe patch
- one weak-field recovery check at `mix = 0`

## Frozen result

The frozen log uses the retained 3D DAG family with:

- `seeds = 6`
- `layers = 18`
- `nodes/layer = 32`
- `probe_layer = 9`
- `mass_layer = 12`
- `mass_count = 8`
- `K = 5.0`

Frozen readout:

| mix | phase lag (rad) | amp ratio | seeds |
| --- | ---: | ---: | ---: |
| `0.00` | `+0.000000` | `1.0000` | `6` |
| `0.25` | `+2.644361` | `1.0214` | `6` |
| `0.50` | `-0.022984` | `1.1361` | `6` |
| `1.00` | `-0.259181` | `0.7282` | `6` |

## Safe read

The strongest bounded statement is:

- the retarded blend produces a real intermediate-layer phase-lag proxy
- the response is non-monotonic in `mix`, so treat the numbers as a proxy
  rather than a smooth universal law
- the weak-field limit at `mix = 0` returns to the instantaneous baseline
- this is a delay / redshift proxy, not a broad gravitational-wave claim

## Relation to the moonshot branch

Read this together with:

- [`docs/MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md)
- [`docs/MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md)
- [`docs/PHYSICS_FIRST_ATTACK_PLAN.md`](/Users/jonreilly/Projects/Physics/docs/PHYSICS_FIRST_ATTACK_PLAN.md)

This branch is viable only if the lag remains a real retained observable and
not just a scheduling artifact from the blend.

## Branch verdict

This probe is **bounded and reviewable** if the lag survives the frozen replay.
If the effect collapses to zero or becomes numerically unstable, it should be
frozen as a clean negative.
