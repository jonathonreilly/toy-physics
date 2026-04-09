# Growing Graph Dynamic Limit Diagnostic Note

**Date:** 2026-04-06  
**Status:** bounded static-control no-go

## Artifact chain

- [`scripts/growing_graph_dynamic_limit_diag.py`](/Users/jonreilly/Projects/Physics/scripts/growing_graph_dynamic_limit_diag.py)
- [`logs/2026-04-06-growing-graph-dynamic-limit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-growing-graph-dynamic-limit.txt)

## Why this exists

The earlier dynamic-propagation idea did not beat the frozen static control in
this replay. The growth story is stronger if it is told through a stable
expansion proxy rather than through a noisy transport signal.

This diagnostic compares two things:

- frontier-delay growth on the existing frontier-growing prototype family
- the dynamic-propagation visibility drop on the evolving causal-DAG family

## What was tested

The diagnostic reports:

- frontier delay, mean delay, RMS delay, and width against a frozen static
  control
- dynamic-propagation visibility drop `V_static - V_grown` across several
  graph sizes

## Controls

Held fixed across the replay:

- the same generated DAG family and seed schedule
- the same source, detector, barrier, and slit geometry
- the same `k` band
- the same layer counts and growth protocol

Only the second-half wiring is randomized in the grown branch.

## Frozen replay

The retained run gives:

- frontier delay: `3.000 -> 22.000`
- frontier-delay slope: `+0.9325` hops/step
- static control frontier delay: `3.000`
- dynamic visibility drop at `n_layers = 10`: `+0.0492` with `4/10` positive
  seeds
- dynamic visibility drop at `n_layers = 15`: `+0.0366` with `4/10` positive
  seeds
- dynamic visibility drop at `n_layers = 20`: `+0.0224` with `2/10` positive
  seeds

The 2026-04-06 replay matched the same shape exactly:

- frontier delay still grows cleanly against the frozen static control
- dynamic visibility drop still weakens with graph size and remains
  seed-dependent
- no monotone dynamic-propagation order parameter emerged from the static
  comparison

## Safe read

The strongest safe conclusion is:

- frontier delay is the clean retained expansion observable
- the dynamic-propagation visibility signal is weak, seed-dependent, and not
  monotone with graph size
- the growth lane is therefore better framed as a graph-expansion proxy than
  as a transport/decoherence derivation
- the dynamic-propagation lane is a review-safe no-go under the current frozen
  static-control comparison

The old graph-ladder work is still useful here, but only as an architecture
guide:

- fixed connectivity survived position noise better than recomputed geometry
- naive KNN/floor rules were too weak
- geometry-sector or other structured local rules can matter, but only if they
  beat the static control and preserve the signed far-field package

That means the transfer lesson is:

- keep frontier delay as the promoted observable
- use connectivity design to support it
- do not reopen dynamic-propagation as the main expansion law unless it clearly
  beats the static control and recovers monotonicity

For the synthesized transfer lesson, see:

- [`docs/GROWING_GRAPH_FRONTIER_ARCHITECTURE_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_FRONTIER_ARCHITECTURE_TRANSFER_NOTE.md)

## What this does not claim

- no cosmology derivation
- no de Sitter claim
- no unitarity or field-theory claim

## Final verdict

**retain frontier expansion and freeze the dynamic-propagation lane as a
bounded static-control no-go**
