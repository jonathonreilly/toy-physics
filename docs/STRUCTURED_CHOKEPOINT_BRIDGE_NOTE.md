# Structured Chokepoint Bridge Note

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded finite structured-chokepoint card on the named `N = 25, 40, 60` slice with the registered canonical readout — no architecture-level bridge closure, no asymptotic behavior, and no readout-independent survival is asserted; runner prints diagnostics rather than enforcing hard pass thresholds. Not a tier-ratifiable bridge pocket theorem.

This note freezes the bridge between the structured-placement lane and the
canonical mirror chokepoint readout.

Script:
[`scripts/structured_chokepoint_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/structured_chokepoint_bridge.py)

Log:
[`logs/2026-04-04-structured-chokepoint-bridge.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-structured-chokepoint-bridge.txt)

## Setup

- structured mirror placement inspired by the structured growth lane
- strict layer-1 chokepoint connectivity
- canonical linear Born + gravity + decoherence readout from the mirror chokepoint harness
- `NPL_HALF = 25` (`50` total nodes per layer)
- `grid_spacing = 1.0`
- `connect_radius = 3.5`
- `layer_jitter = 0.25`
- `16` seeds
- `N = 25, 40, 60`

## Retained Rows

The bridge pocket is Born-clean at machine precision and keeps positive
gravity across the narrow probe set.

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|
| 25 | `0.9626` | `0.9473±0.00` | `1.0125` | `+6.4026±0.185` | `6.77e-16` | `0.00e+00` |
| 40 | `0.8850` | `0.9491±0.01` | `0.9948` | `+7.4729±0.305` | `8.14e-16` | `0.00e+00` |
| 60 | `0.6440` | `0.8030±0.04` | `1.0043` | `+5.7613±0.892` | `6.56e-16` | `0.00e+00` |

## Narrow Read

- The structured bridge stays Born-clean on the canonical readout.
- The `k=0` control remains pinned to zero.
- The structured placement does not erase the decoherence signal; `N=60`
  drops to `pur_cl = 0.8030±0.04`.
- The bridge is bounded, not asymptotic: the retained statement is narrow and
  tied to this structured slice.

## Interpretation

This is the cleanest claim available for the structured chokepoint bridge:

- structured placement survives the canonical mirror-harness readout
- Born stays at machine precision
- gravity is positive across the retained rows
- the decoherence side remains below the ceiling on the largest retained row
- the pocket is real, but only as a bounded narrow bridge


## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, medium criticality, 5 transitive
descendants):

> Issue: the runner supports the finite N=25,40,60 structured
> chokepoint card, but the note promotes that selected slice as a
> retained bridge pocket without a registered canonical-readout
> dependency or theorem selecting the graph parameters. Why this
> blocks: a hostile auditor can verify the printed table, but cannot
> infer architecture-level bridge closure, asymptotic behavior, or
> readout-independent survival from the current packet; the runner
> also prints diagnostics rather than enforcing hard assertions.

## What this note does NOT claim

- An architecture-level bridge closure theorem.
- Asymptotic behavior of the chokepoint card beyond `N = 25, 40, 60`.
- Readout-independent survival of the bridge pocket.
- A registered theorem selecting the graph parameters.

## What would close this lane (Path A future work)

Reinstating a retained bridge pocket would require:

1. A registered canonical-readout dependency.
2. A theorem selecting the graph parameters from upstream primitives.
3. Hard runner-side pass thresholds (not just printed diagnostics).
4. Architecture-level closure or asymptotic behavior beyond the
   tested `N` slice.
