# Staggered Backreaction Active-Gauge Edge Selection Note

**Date:** 2026-04-24  
**Script:** `scripts/frontier_staggered_backreaction_active_gauge_edge_selection.py`  
**Status:** active-field gauge obstruction resolved by a graph-native edge rule

## Question

The first backreaction stress split found:

- all non-gauge source-sector rows passed on the larger stress families
- active-field gauge/current failed on two cycle-bearing stress graphs

The failure used the default DFS-selected cycle edge inherited from the
portability harness.  This note tests whether that failure is intrinsic to the
active resistance-Yukawa source field, or whether it is an edge-selection
artifact.

## Rule

Keep the active field fixed:

```text
Phi = K rho,
K_ij = exp(-1.50 R_eff(i,j)) / (R_eff(i,j) + 0.10).
```

Only replace the flux edge by a deterministic graph-native rule:

```text
source-proximal non-bridge edge
  = nearest-to-source edge whose removal does not disconnect the graph.
```

This edge is selected before measuring current.  The max-current edge is
reported only as a diagnostic ceiling, not as the scored row.

## Exact Results

| Family | n | Legacy edge | Legacy current span | Source edge | Source current span | Periodic residual | Max edge | Max span | Status |
|---|---:|---|---:|---|---:|---:|---|---:|---|
| random-geometric stress | 81 | `15-6` | `6.262e-10` | `0-1` | `3.194e-02` | `4.872e-17` | `0-1` | `3.194e-02` | PASS |
| growing stress | 82 | `6-0` | `1.293e-02` | `0-7` | `2.000e-02` | `2.358e-18` | `7-14` | `4.620e-02` | PASS |
| chorded-grid stress | 144 | `21-7` | `3.497e-10` | `0-12` | `2.096e-02` | `2.330e-17` | `1-2` | `2.895e-02` | PASS |
| layered DAG stress | 66 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

Thresholds:

- current span must exceed `1e-4`
- periodic residual must stay below `1e-8`

Readout:

- source-proximal active-gauge pass count: `3/3`
- legacy DFS-edge pass count: `1/3`
- minimum source-edge current span: `2.000e-02`

## Interpretation

The active-field gauge failure in
`STAGGERED_GRAPH_OBSERVABLES_BACKREACTION_STRESS_NOTE_2026-04-24.md` was not an
intrinsic incompatibility between the resistance-Yukawa source sector and
native current response.

It was an edge-selection artifact:

- the DFS-selected edge can sit outside the active source pocket and carry
  near-zero persistent current
- a source-proximal non-bridge edge carries a clean, periodic current response
  on all cycle-bearing stress graphs

So the corrected active-field gauge rule is:

> score gauge/current on a source-proximal non-bridge cycle edge, not an
> arbitrary DFS cycle edge.

## Boundary

This does not change the force/source rows from the previous note.  It changes
the active-field gauge-row convention.

Retain the combined result as:

- **source-sector rows:** pass on all four stress families
- **active-field gauge/current:** passes on all three cycle-bearing stress
  families under the source-proximal non-bridge flux-edge rule
- **DAG-compatible family:** remains `N/A` for gauge/current

Future backreaction cards should explicitly state the flux-edge rule.  A
plain DFS cycle edge is no longer an acceptable gauge-row convention when an
active source field localizes the current response.
