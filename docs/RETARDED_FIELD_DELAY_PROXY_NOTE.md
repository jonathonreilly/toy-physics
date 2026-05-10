# Retarded Field Delay Proxy

**Date:** 2026-04-05 (audit-status note added 2026-05-10)
**Status:** bounded retarded-field intermediate-layer phase-lag probe

## Artifact chain

- [`scripts/retarded_field_delay_proxy_probe.py`](/Users/jonreilly/Projects/Physics/scripts/retarded_field_delay_proxy_probe.py)
- [`logs/2026-04-05-retarded-field-delay-proxy-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-retarded-field-delay-proxy-probe.txt)

## Audit-status note (2026-05-10)

The 2026-05-05 audit verdict (`audited_conditional`, chain_closes=false)
ratified the bounded compact-probe scope of this note — the runner
genuinely computes the frozen retarded-field phase-lag table on the
generated 3D DAG family with `seeds=6, layers=18, nodes/layer=32,
probe_layer=9, mass_layer=12, mass_count=8, K=5.0, mix ∈ {0.0, 0.25,
0.5, 1.0}`, and the `mix=0` row recovers the instantaneous baseline
exactly — but flagged that the moonshot-branch citations are not
retained-grade.

> "The runner output matches the note and the runner source performs
> an actual numerical replay rather than printing constants. However,
> the restricted packet cites unaudited upstream authorities, so the
> audit chain cannot close to retained grade under the rubric."

Per-input current status (one-hop deps):

- [`MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md`](MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md)
  — `audited_conditional` (bounded moonshot trapping probe).
- [`MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md`](MINIMAL_BIDIRECTIONAL_TRAPPING_PROBE_NOTE.md)
  — `audited_conditional` (bounded moonshot bidirectional-trapping probe).

The "Relation to the moonshot branch" section below cites these two
notes plus `PHYSICS_FIRST_ATTACK_PLAN.md` as related-context only;
they are not used as authority closure for the retarded-blend
phase-lag readout.

Admitted-context inputs (carrier framework, not derived in this note):

- generated 3D DAG constructor `generate_3d_dag` and the
  `field_laplacian` / `field_causal_sum` / `propagate` operators from
  `scripts/causal_field_gravity.py` (the retarded blend is a
  parameterised mix of the instantaneous Laplacian field and the
  causal-sum field on the same DAG)

Configured probe parameters (proxy thresholds, not derived):

- six seeds, 18 layers, 32 nodes/layer, probe_layer=9, mass_layer=12,
  mass_count=8, K=5.0
- four mix values `{0.0, 0.25, 0.5, 1.0}` measured at one fixed
  intermediate probe patch
- frozen phase-lag readout `(0.00, 0.25, 0.50, 1.00) ↔ (+0.0000,
  +2.6444, -0.0230, -0.2592)` rad with weak-field recovery at
  `mix = 0` exact

Blocked-on: this note stays `audited_conditional` until the moonshot
branch authorities advance to retained-grade or are removed from the
citation chain. The bounded compact-probe statement itself — that the
retarded blend produces a real intermediate-layer phase lag in this
configured replay and that `mix = 0` returns to the instantaneous
baseline exactly — is unaffected by this status note; the change is
purely upstream propagation accounting on the moonshot-branch citation
edges. This is a delay / redshift proxy, not a broad gravitational-wave
claim.

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
