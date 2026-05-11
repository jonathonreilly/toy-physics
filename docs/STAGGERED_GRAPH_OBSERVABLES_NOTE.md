# Staggered Graph Observables Note

**Status:** meta working-rule observables probe
**Claim type:** meta

**Audit-renaming perimeter (2026-05-08):**
The current generated audit ledger records this row `audited_renaming` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
meta`. The audit chain-closure explanation is exact: "The runner and
retained cited notes support the listed diagnostic values, but the
retained/secondary observable split is stipulated as a working rule.
The packet lacks a theorem deriving that scoring rule from the
transport law and graph topology." This rigorization edit only
sharpens the boundary of the renaming perimeter; nothing here
promotes audit status. The supported content of this note is the
methodological **working-rule** scoring on the three listed non-
cubic graph families: Born/linearity, norm preservation, force sign,
F∝M, achromatic force, equivalence, robustness, and gauge/current-
when-cycles are recorded as the **stipulated** retained-row split,
and centroid/shell/depth as **stipulated** secondary diagnostics.
This is a meta-level bookkeeping rule, not a derived theorem. The
supported perimeter is exactly the bookkeeping rule plus the
diagnostic-value table at n ∈ {36, 48, 36}; the rule itself is not
derived from the transport law and graph topology — that derivation
would be a separate theorem note and is the prescribed promotion
path. The audit-renaming verdict precisely reflects this status: the
note is correctly retagged from a positive-theorem framing to a meta
working-rule framing.

This note freezes the graph-native observable split for the staggered /
Kahler-Dirac lane.

## Goal

Tighten the observables used on non-cubic graph families so the retained rows
match the transport law and the graph topology.

## Families

- bipartite random geometric graph
- bipartite growing graph
- layered bipartite DAG-compatible graph

## First Probe

Script: [`frontier_staggered_graph_observables.py`](../scripts/frontier_staggered_graph_observables.py)

### Exact Results

| Family | n | Retained | Centroid shift | Shell bias | Gauge/current |
|---|---:|---:|---:|---:|---:|
| bipartite random geometric | 36 | `8/8` | `-1.110e-16` | `-4.345e-01` | `5.142e-03` PASS |
| bipartite growing | 48 | `8/8` | `+1.110e-16` | `-4.398e-01` | `9.054e-03` PASS |
| layered bipartite DAG-compatible | 36 | `8/8` | `+1.388e-17` | `-4.826e-01` | `N/A` |

## Retained Observables

- Born / linearity
- norm preservation
- force sign
- `F∝M`
- achromatic force
- equivalence
- robustness
- gauge / current only when the graph has cycles

## Secondary Diagnostics

- centroid shift
- shell bias
- depth response

These are useful for understanding recurrence and finite-size effects, but they
should not replace the retained force/current rows on graph families.

## Working Rule

- If the graph has cycles, gauge/current is a retained row.
- If the graph is DAG-compatible, gauge/current is `N/A`.
- Centroid-based gravity diagnostics remain secondary on non-cubic graphs.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_graph_portability_note](STAGGERED_GRAPH_PORTABILITY_NOTE.md)
- [staggered_graph_gauge_closure_results_2026-04-10](STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md)
