# Teleportation 3D Resource Probe

**Date:** 2026-04-26 (numerics refreshed 2026-05-10 from current runner output)
**Status:** planning / first artifact; not a promotion claim
**Claim type:** bounded_theorem
**Runner:** `scripts/frontier_teleportation_3d_resource_probe.py`

## Review scope (numeric refresh 2026-05-10)

Generated-audit context flagged the prior table as carrying stale
numerical values relative to current runner output. The repair target:

> other: refresh `docs/TELEPORTATION_3D_RESOURCE_PROBE_NOTE.md` from the
> current runner output and rerun the compile/run commands, preserving
> the explicit `Psi+` Bell-frame boundary.

This pass refreshes the `G=500` row (`Bell*`, `Phi+` overlap, `F_phi`,
`F_best`, `Slog`, `negativity`), the null/`G=100` no-signaling columns,
and the `G=1000` sampled mean/min/max fidelity summary directly from
`python3 scripts/frontier_teleportation_3d_resource_probe.py` on
2026-05-10. Qualitative content, acceptance gates, scope, and the
explicit `Psi+` Bell-frame boundary are unchanged. No promotion claim;
the source claim type remains `bounded_theorem`, and the independent
audit ledger owns any audit outcome or effective status.

## Scope

This note records the smallest-surface 3D spatial pressure test for the
Poisson-backed taste-qubit teleportation resource. The audited geometry is
`3D side=2`, with `N=8` sites and dense two-species Hilbert dimension `64`.

The extraction keeps the last Kogut-Susskind taste bit as the retained logical
qubit and traces cells plus spectator taste bits. The protocol uses the
retained-axis logical convention. Raw `xi_5` is not used as traced logical `Z`.

This remains ordinary quantum state teleportation planning only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_3d_resource_probe.py
python3 scripts/frontier_teleportation_3d_resource_probe.py
```

Default settings:

```text
dimension = 3
side = 2
mass = 0
G values = 0, 100, 500, 1000
input probes = 70 states (six Pauli-axis states + 64 random states)
seed = 20260425
```

## Results

| case | full CHSH | best Bell | label | `Phi+` overlap | fixed `Phi+` `F_avg` | best-frame `F_avg` | logical CHSH | negativity | Bob pairwise no-record distance | high |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `3d_side2_null` | `2.00000` | `0.500000` | `Psi+` | `0.500000` | `0.666667` | `0.666667` | `2.00000` | `0.000000` | `2.776e-16` | no |
| `3d_side2_G100` | `2.16713` | `0.887978` | `Psi+` | `0.112022` | `0.408015` | `0.925319` | `2.53149` | `0.387978` | `2.220e-16` | no |
| `3d_side2_G500` | `2.75551` | `0.991220` | `Psi+` | `0.008780` | `0.339187` | `0.994146` | `2.80370` | `0.491220` | `2.498e-16` | yes |
| `3d_side2_G1000` | `2.80922` | `0.997724` | `Psi+` | `0.002276` | `0.334850` | `0.998483` | `2.82200` | `0.497724` | `2.220e-16` | yes |

The `G=0` null remains non-resource. The non-null `G=500` and `G=1000`
rows are high-fidelity logical Bell resources after tracking the Bell frame.
They land in the `Psi+` frame, not the fixed `Phi+` frame. Therefore:

- fixed `Phi+` teleportation is poor for these rows;
- a known retained-axis Bob-side `X` frame maps the resource to `Phi+`;
- the best-frame average fidelities are `0.994146` and `0.998483`.

For the best default row, `3d_side2_G1000`:

```text
ground energy = -114.870237352
Bell* = 0.997724 (Psi+)
fixed-Phi+ F_avg = 0.334850
best-frame F_avg = 0.998483
sampled mean/min/max fidelity = 0.998523 / 0.997724 / 1.000000
Bob no-record pairwise input distance = 2.220e-16
Bob marginal bias from I/2 = 4.764e-02
```

The Bob marginal bias is a resource imperfection, not input information. The
pre-message input-independence check is the pairwise no-record distance across
Alice inputs.

## Acceptance Gates

The default run reports `PASS` for:

- `3D side=2` null control stays non-resource;
- at least one non-null `3D side=2` high Bell-frame resource exists;
- Bob pre-message input-independence is clean;
- retained-axis extraction is used instead of raw `xi_5` as traced `Z`;
- larger 3D surfaces are not claimed by this artifact.

## Interpretation

The smallest exact 3D spatial surface does contain a strong Poisson-backed
logical Bell resource in the retained-axis extraction. This is the first
bounded 3D resource-positive result for the teleportation lane.

The positive resource is frame-positive rather than fixed-`Phi+` positive:
the dominant Bell sector is `Psi+`. This is not a no-signaling issue and not a
new physics claim. It means the protocol must carry the Bell-frame convention
or supply a known retained-axis local frame correction before applying the
standard feed-forward map.

## Limitations

- Exact smallest 3D surface only: `side=2`, `N=8`, two-species dimension `64`.
- No `3D side=4` dense diagonalization or sparse scaling result is supplied.
- The resource is obtained by offline diagonalization and tracing, not by a
  physical preparation/readout workflow.
- The Bell frame must be tracked explicitly; fixed `Phi+` would fail on the
  positive `Psi+` rows.
- Bell measurement, readout, feed-forward, and Bob correction remain ideal
  retained-logical operations.
- Scope remains ordinary quantum state teleportation only.
