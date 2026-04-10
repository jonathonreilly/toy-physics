# Cycle-Break Frontier Slice Note

**Date:** 2026-04-10  
**Script:** `frontier_staggered_cycle_break_slice.py`

## Purpose

This note freezes a matched frontier slice around the first larger-graph break
in the retained cycle battery.

The retained battery rows are unchanged. The slice compares:

- a frontier branch on `random_geometric, side=18` with dense cross-color
  shortcuts at `extra=4,5,6`
- a quality-matched control with the same edge-count scale, but local and
  degree-balanced cross-color additions instead of long shortcuts

## Result

The slice cleanly separates the frontier from the control.

| Case | extra=4 | extra=5 | extra=6 |
|---|---:|---:|---:|
| Frontier | `9/9` | `8/9` | `8/9` |
| Control | `9/9` | `9/9` | `9/9` |

Representative frontier values:

- `extra=4`: `J_span=2.1718e-05`, `gauge=PASS`
- `extra=5`: `J_span=6.6346e-07`, `gauge=FAIL`
- `extra=6`: `J_span=6.6343e-07`, `gauge=FAIL`

Representative control values:

- `extra=4`: `J_span=2.6189e-05`, `gauge=PASS`
- `extra=5`: `J_span=3.3930e-05`, `gauge=PASS`
- `extra=6`: `J_span=3.2547e-05`, `gauge=PASS`

## Interpretation

The first break remains a **native gauge/current collapse under dense
shortcuts**. The matched local control shows that the failure is not just
edge-count or degree scale; it is tied to the long dense cross-color shortcut
geometry.

The force-first rows remain stable across the slice:

- Born
- linearity
- additivity
- force sign
- iterative stability
- norm
- family robustness
- force-gap characterization

## Takeaway

The retained cycle battery survives a quality-matched local control at the same
size and edge-count scale, but loses native gauge/current at the frontier when
long dense shortcuts are added.

That makes the frontier slice a genuine boundary probe, not just a larger-graph
repeat.
