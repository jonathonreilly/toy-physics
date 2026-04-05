# Source-Resolved Propagating Green Pocket

**Date:** 2026-04-05  
**Status:** retained exact-lattice same-site-memory positive

This note freezes the smallest exact-lattice same-site-memory harness that
could still be compared directly against the retained static Green control and
the instantaneous `1/r` comparator.

The script is:

- [`scripts/source_resolved_propagating_green_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_propagating_green_pocket.py)

## Setup

- exact 3D lattice: `h = 0.5`, `W = 3`, `L = 20`
- source cluster: clipped cross5 local cluster, leaving 4 in-bounds nodes
- source ladder: `s = {0.001, 0.002, 0.004, 0.008}`
- same-site memory field: Green-like layer recurrence with `mix = 0.9`
- control comparison: instantaneous `1/r` field and static source-resolved Green field

## Hard gates

The retained exact-lattice run passes all requested gates:

- exact zero-source reduction: `0.0`
- all-TOWARD on the source ladder: `4/4`
- dynamic `F~M`: `1.00`
- mean `|dynamic/instantaneous|`: `1.420`
- mean `|dynamic/static Green|`: `1.149`

## Frozen values

| `s` | instantaneous shift | static Green shift | propagating shift | `prop/inst` | `prop/green` |
|---:|---:|---:|---:|---:|---:|
| `0.001` | `+1.713544e-03` | `+2.139974e-03` | `+2.460113e-03` | `1.436` | `1.150` |
| `0.002` | `+3.440703e-03` | `+4.279368e-03` | `+4.919670e-03` | `1.430` | `1.150` |
| `0.004` | `+6.936763e-03` | `+8.557987e-03` | `+9.837774e-03` | `1.418` | `1.150` |
| `0.008` | `+1.410179e-02` | `+1.712572e-02` | `+1.967434e-02` | `1.395` | `1.149` |

The instantaneous, static Green, and propagating responses all keep the same
weak-field sign and preserve linear mass scaling on this exact-lattice family.

## Causal observable

The same-site memory field is not identical to the static Green control:

- mean `prop - green = +1.197212e-03`

That is the smallest retained layer-memory observable in this pocket. It is
nontrivial, but it remains bounded and does not claim transverse transport, a
finite-speed field equation, or a full self-consistent GR sector.

## Safe read

This is a bounded exact-lattice positive:

- the same-site memory field keeps the weak-field `TOWARD` sign
- it preserves the Newtonian mass-scaling class on the tested source ladder
- it stays within the requested amplitude ratio band
- it is distinguishable from the static Green control by a small layer-memory
  offset

What it is **not**:

- a full self-consistent propagating-field theory
- a genuine transverse transport or finite-speed field model
- a horizon / black-hole result
- a claim that the generated geometry sector is closed
