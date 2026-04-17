# Valley-Linear Mirror Transfer Note

**Date:** 2026-04-04  
**Status:** bounded mirror/random-DAG transfer replay frozen on disk

## One-line read

On the canonical 3D DAG generators, valley-linear is **not** a universal
transfer winner: it improves the random-DAG family relative to spent-delay,
but spent-delay still has the edge on the mirror family.

That makes the lane useful as a branch-specific transfer diagnostic, not as a
unification theorem.

## Primary artifact

- Script: [`scripts/valley_linear_mirror_transfer.py`](/Users/jonreilly/Projects/Physics/scripts/valley_linear_mirror_transfer.py)
- Log: [`logs/2026-04-04-valley-linear-mirror-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-valley-linear-mirror-transfer.txt)

The replay keeps fixed:

- the canonical 3D DAG generators
- the same barrier / slit geometry
- the same detector readout
- the same field shape and strength
- the same action toggle

It changes only the graph family:

- `random`
- `mirror`

and compares the two action laws:

- spent-delay
- valley-linear `S = L(1-f)`

## Frozen replay result

| family | action | TOWARD | mean delta |
|---|---:|---:|---:|
| random | spent-delay | `11/36` | `-0.770064` |
| random | valley-linear | `18/36` | `+0.000155` |
| mirror | spent-delay | `24/36` | `+0.545083` |
| mirror | valley-linear | `23/36` | `+0.036664` |

## Safe interpretation

- On the random DAG family, valley-linear improves the TOWARD fraction
  relative to spent-delay in this frozen replay.
- On the mirror family, spent-delay still has the stronger TOWARD rate and
  larger mean delta.
- Valley-linear does not dominate both families simultaneously.
- The replay is therefore a **transfer diagnostic**, not a proof that one
  action replaces the other.

## What this is not

- A theorem that valley-linear is the continuum limit of spent-delay.
- A proof that the mirror/random DAG split is resolved.
- A replacement for the canonical lattice action notes.

## Why it matters

This note makes the architecture split harder to misread:

- regular ordered lattice lanes can favor valley-linear
- irregular/random DAG lanes can still favor spent-delay
- the mirror family sits between those extremes

That is exactly the kind of bounded branch fact a reviewer can inspect without
having to buy a broader unification claim.
