# Same-Family 3D Closure: Valley-Linear

**Date:** 2026-04-04
**Status:** bounded same-family multi-size closure note; script prints the
**Claim type:** bounded_theorem
frozen card and the same-`h` multi-`L` rows but does **not** itself recompute
the load-bearing closure checks live (rows 1-7 are replayed from the retained
core-card logs; rows 8-9 are replayed from the dedicated `L=8` and `L=10`
runs on 2026-04-04; row 10 is replayed from the W=12 width-companion log).
The script is therefore a print-aggregation wrapper for an already-frozen
multi-log core, not a live re-derivation harness.

**Audit-conditional perimeter (2026-05-02):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
source note itself says the wrapper aggregates and prints frozen rows
and does not recompute the load-bearing observables. With deps=[] and
no retained log/runner dependency chain, the closure card cannot be
retained as an independently audited theorem." This rigorization edit
only sharpens the boundary of the conditional perimeter; nothing here
promotes audit status. The supported content of this note is the
print-aggregation wrapper itself: the script
[`scripts/same_family_3d_closure.py`](../scripts/same_family_3d_closure.py)
prints the frozen 10-row table and the registered cache
[`logs/runner-cache/same_family_3d_closure.txt`](../logs/runner-cache/same_family_3d_closure.txt)
captures the wrapper output. The note is honest in §"What remains
open" that the wrapper is replay-only; that honesty is exactly the
audit-stated reason the row cannot promote — there are no live
deps=[] in the wrapper. The supported perimeter is the wrapper
print itself, not the underlying closure checks. A future repair
would explicitly enumerate the per-`L` and per-`W` runs as
dependencies (with their own ledger entries) so the chain rule could
close; that step is deferred to a downstream rebuild and is not in
the scope of this print-aggregation note.

## Current on-disk artifacts

- Script: [`scripts/same_family_3d_closure.py`](/Users/jonreilly/Projects/Physics/scripts/same_family_3d_closure.py)
- Log: [`logs/2026-04-04-same-family-3d-closure.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-same-family-3d-closure.txt)

This is a same-family closure on one retained family:

- action: `S = L(1-f)`
- kernel: `1/L^2` with `h^2` measure
- field: `s/r`
- ordered 3D dense lattice

It is not a single-instance theorem card. Properties `8-9` are same-family
multi-`L` rows, and property `10` includes a same-family width companion.
The frozen wrapper replays `L=8` and `L=10`, then reuses the retained core
`L=12` row so the whole note stays on one family at one `h`.

## Architecture
- Action: S = L(1-f) (valley-linear)
- Kernel: 1/L^2 with h^2 measure
- Lattice: 3D dense, h=0.25, W=10, max_d=3
- Field: s/r with s=5e-5

## Card

| # | Property | Value | Same family? |
|---|----------|-------|-------------|
| 1 | Born | 4.20e-15 | h=0.25 W=10 L=12 |
| 2 | d_TV | 0.83 | h=0.25 W=10 L=12 |
| 3 | k=0 gravity | 0.000000 | h=0.25 W=10 L=12 |
| 4 | F∝M alpha | 1.00 | h=0.25 W=10 L=12 |
| 5 | Gravity sign | +0.000224 TOWARD | h=0.25 W=10 L=12 |
| 6 | Decoherence | 49.9% | h=0.25 W=10 L=12 |
| 7 | MI | 0.64 bits | h=0.25 W=10 L=12 |
| 8 | Purity stable | 50.0% (L=8,10,12) | h=0.25 W=10 |
| 9 | Gravity grows | +0.157→+0.224 | h=0.25 W=10 |
| 10 | Distance tail | b^(-0.93) W=10 / b^(-1.07) W=12 | h=0.25 |

Properties 8-9 use `L=8,10,12` at the SAME `h=0.25` and `W=10`.
No `h=0.5` companions are needed, but the `L=12` multi-`L` row is carried
through the frozen core-card values rather than recomputed inside the wrapper.

## What this closes

This is the first time the same-family closure is carried as a real
script/log/note chain. The fixed core rows remain at `h=0.25, W=10, L=12`;
properties `8-9` are same-`h` multi-`L` rows; and property `10` still carries
a width companion for the far tail.

## What remains open

- The distance exponent is near-Newtonian but not exactly -1.0. The frozen
  W=10 and W=12 rows stay as companion width checks.
- Properties 8-9 use multiple `L` values (necessary for scaling checks).
  This is a same-family multi-size test, not a single-instance card.
- The wrapper is partly replayed and partly frozen by design: it is a review-
  facing closure note, not a new heavyweight all-live card harness. The
  script `scripts/same_family_3d_closure.py` aggregates and prints the
  frozen rows but does not itself recompute the underlying closure
  observables; live recomputation lives in the per-`L` and per-`W` runs
  cited above.
- The action is selected, not derived (though the universality-class result
  shows it's the simplest member of the Newtonian family).
