# Structured Chokepoint Bridge Extension Note

**Date:** 2026-04-04  
**Status:** bounded extension of the proposed_retained structured bridge pocket

This note records the narrow follow-up to the retained structured chokepoint
bridge.

Script:
[`scripts/structured_chokepoint_bridge_extension.py`](/Users/jonreilly/Projects/Physics/scripts/structured_chokepoint_bridge_extension.py)

Log:
[`logs/2026-04-04-structured-chokepoint-bridge-extension.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-structured-chokepoint-bridge-extension.txt)

## Setup

- same structured mirror-symmetric placement family as the retained bridge
- same layer-1 chokepoint connectivity
- same canonical mirror readout from `mirror_chokepoint_joint`
- only the layer count is widened
- default tested rows: `N = 60, 80, 100`
- canonical parameters retained from the base bridge:
  - `NPL_HALF = 25`
  - `grid_spacing = 1.0`
  - `connect_radius = 3.5`
  - `layer_jitter = 0.25`
  - `16` seeds

## What This Checks

The question is not whether a new generator family can be found.
It is whether the retained structured bridge pocket extends cleanly to
larger layer counts while keeping the canonical mirror readout fixed.

## Interpretation Rule

- If larger `N` stays Born-clean, keeps `k=0` pinned to zero, and preserves
  positive gravity, the bridge can be described as widened.
- If those conditions fail, the bridge remains a narrow retained pocket.
- Either way, this is still a bounded extension of the same structured family.

## Expected Readout

The extension should be interpreted alongside the base bridge note:
- [`docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md)

This note does not replace the canonical bridge note. It only answers the
larger-N follow-up.

## Retained Result

The larger-N replay widened the retained pocket on the same structured family.

| N | `d_TV` | `pur_cl` | `S_norm` | gravity | Born `|I3|/P` | `k=0` |
|---|---:|---:|---:|---:|---:|---:|
| 60 | `0.6440` | `0.8030±0.04` | `1.0043` | `+5.7613±0.892` | `0.00e+00±0.00` | `0.00e+00` |
| 80 | `0.6925` | `0.7712±0.03` | `0.9910` | `+4.3840±0.666` | `0.00e+00±0.00` | `0.00e+00` |
| 100 | `0.6947` | `0.8056±0.03` | `1.0158` | `+2.9007±1.054` | `0.00e+00±0.00` | `0.00e+00` |

Interpretation:
- Born stays at machine precision on the larger rows.
- `k=0` remains pinned to zero.
- gravity remains positive through `N=100`.
- the bridge widens, but only modestly; it is still a bounded pocket.
