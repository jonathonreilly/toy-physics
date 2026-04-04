# Evolving Network Prototype V4 Note

**Date:** 2026-04-04  
**Status:** bounded structured-connectivity Gate B prototype, not a dynamics theorem

## One-line read

This v4 pass tests a single connectivity-first growth rule:

- crystal-like templating with a restoring force toward grid positions
- fixed-offset connectivity preserved by construction
- KNN connectivity recomputed from the same grown positions as the control

The point is to see whether structured connectivity keeps the Gate B response
more stable than geometry-recomputed connectivity.

## Primary artifact

- Script: [`scripts/evolving_network_prototype_v4.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v4.py)
- Log: [`logs/2026-04-04-evolving-network-prototype-v4.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v4.txt)

## What v4 changes relative to v3

v3 improved the imposed control but still lived in the hard-gap pruning lane.
v4 changes the question:

- instead of pruning a random DAG harder or softer,
- it grows a near-regular geometry with explicit restoring force,
- then asks whether fixed connectivity beats KNN on the same positions.

That is a cleaner test of the new connectivity lesson:

- position noise is tolerated
- connectivity construction is the bottleneck

## Frozen replay result

The frozen log should be read as a bounded control audit with three rows:

- ordered baseline
- crystal-like structured growth
- KNN control on the same grown positions

The frozen replay lands as a mixed but useful result:

| family | toward | mean delta | alpha |
|---|---:|---:|---:|
| ordered | `0.0/9` | `-0.000058` | `0.00` |
| crystal | `2.0/9` | `-0.000037` | `0.83` |
| KNN control | `2.0/9` | `-0.000050` | `0.66` |

The structured crystal row does **not** clearly beat KNN on the toward count,
but it does slightly improve the mean delta and response slope.

## Safe interpretation

- The structured growth rule is explicit and connectivity-first.
- The imposed KNN control is a fairer comparator than pure random removal.
- The comparison is about whether a generated backbone stays coherent under
  review, not about proving that every growth rule works.
- The result should be treated as an incremental Gate B advance only if the
  structured row clearly beats the KNN row on the main signal. In this frozen
  replay, it improves the slope a little but does not win cleanly on toward.

## What this is not

- A solved Gate B dynamics theorem.
- A proof that all connectivity-preserving growth rules succeed.
- A replacement for the existing hard-gap prototype notes.
- A universal closure of the generated-vs-imposed question.

## Why this matters

The repository now has a sharper Gate B target:

- structured connectivity appears to be the real bottleneck
- position noise is not the main failure mode
- the next useful growth rule is one that preserves connectivity without
  hand-imposing a lattice

That is exactly the kind of bounded result a skeptical reader can inspect
without buying a broader unification claim.
