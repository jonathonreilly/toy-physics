# Staggered Graph Failure Map Note

**Date:** 2026-04-10  
**Status:** proposed_retained adversarial boundary map

This note freezes the first adversarial failure map for the retained staggered /
Kahler-Dirac force lane.

## Question

Where does the retained staggered battery fail when we deliberately inject:

- odd-cycle defects
- parity ambiguity / wrap inconsistencies
- dense shortcuts
- high-degree contamination

## Harness

- Script: [`frontier_staggered_graph_failure_map.py`](../scripts/frontier_staggered_graph_failure_map.py)
- Battery: Born/linearity, norm, force sign, `F∝M`, achromatic force,
  equivalence, robustness, gauge if cycles exist

## First Retained Run

| Family | n | same-color edges | long-edge frac | max degree | retained | gauge | classification |
|---|---:|---:|---:|---:|---:|---|---|
| control random geometric | 36 | `0` | `0.00` | `4` | `8/8` | PASS | baseline |
| odd-cycle defect | 48 | `1` | `0.00` | `5` | `8/8` | PASS | structural break |
| parity wrap inconsistency | 36 | `1` | `0.47` | `3` | `8/8` | N/A | structural break |
| dense shortcuts | 36 | `0` | `0.06` | `4` | `8/8` | PASS | graceful degradation |
| high-degree contamination | 49 | `0` | `0.08` | `12` | `8/8` | PASS | graceful degradation |

## Readout

- Odd-cycle defects are structural breaks: a single same-color edge is enough to
  violate the retained bipartite/parity assumptions.
- Parity wrap inconsistencies are also structural breaks, even when the retained
  force battery itself still passes.
- Dense shortcuts and high-degree contamination are degradations, not immediate
  failures, as long as the retained force battery stays intact.
- Gauge/current remains conditional on cycles, but it is not the leading
  discriminator here.

## Caveat

This is a boundary map, not a replacement for the canonical force-based
staggered card. Its job is to say where the retained transport law stops being
portable.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_graph_portability_note](STAGGERED_GRAPH_PORTABILITY_NOTE.md)
