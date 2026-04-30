# Growing Graph Frontier Expansion Proxy Note

**Date:** 2026-04-05  
**Status:** support - structural or confirmatory support note

## One-line read

This note freezes one narrow expansion observable on the existing growing-graph
prototype family:

- static graph control: the step-0 frozen seed graph
- growing graph observable: frontier delay from the source center to the
  farthest reachable node

The claim is intentionally narrow:

- the growing graph shows a monotone increase in frontier delay
- the static control does not produce any expansion by itself
- this is a graph-expansion proxy, not a cosmology claim

## Primary artifact

- Script: [`scripts/growing_graph_frontier_expansion.py`](/Users/jonreilly/Projects/Physics/scripts/growing_graph_frontier_expansion.py)

## What was tested

The probe starts from the existing growing-network prototype and measures one
observable across the snapshot sequence:

- frontier delay = max unweighted graph distance from the seed center
- mean delay
- RMS delay
- delay width

The comparison is against a frozen no-growth control built from the same seed
graph.

## Frozen replay

On the retained run:

- step 0 frontier delay: `3.000`
- step 20 frontier delay: `22.000`
- frontier-delay slope: `+0.9325` hops/step
- static control frontier delay: `3.000`
- control is flat by construction

## Review-safe read

The retained statement is only:

- the growing graph expands its frontier delay relative to the frozen control
- the control chain is static and does not generate expansion on its own

What this does **not** establish:

- de Sitter expansion
- a cosmological metric
- any claim about the universe
- any asymptotic theorem beyond the tested prototype family

## Why this is worth keeping

This is the first clean expansion-style observable on the prototype family that
can be checked without invoking cosmology rhetoric.

If later work finds a stronger metric-style proxy, this note becomes the narrow
baseline for that upgrade. For now it is a deliberately small retained result.
