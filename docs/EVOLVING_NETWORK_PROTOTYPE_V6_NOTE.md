# Evolving Network Prototype V6 Note

**Date:** 2026-04-04  
**Status:** frozen h=0.5 structured-growth replay, mixed rather than a Gate B pass

## One-line read

This v6 replay freezes the h=0.5 structured-growth claim in a review-safe
way:

- template previous layer
- local drift
- restoring force toward the grid target
- fixed NN connectivity

The result is real and useful, but it is **not** the full 100% TOWARD claim
from branch narrative. In this frozen replay, the best row is mixed and the
overall sweep does not close Gate B.

## Primary artifact

- Script: [`scripts/evolving_network_prototype_v6.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v6.py)
- Log: [`logs/2026-04-04-evolving-network-prototype-v6.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v6.txt)

## Frozen replay setup

The replay uses the h=0.5 working regime with a small fixed parameter grid:

- `h = 0.5`
- `layers = 13`
- `half-width = 5`
- `seeds = (5, 18, 31, 44)`
- `mass strengths = (0.75, 1.0, 1.25)`
- `mass y targets = (1.0, 1.5, 2.0)`

The sweep rows are:

- `(drift=0.3, restore=0.5)`
- `(drift=0.2, restore=0.7)`
- `(drift=0.1, restore=0.9)`
- `(drift=0.0, restore=1.0)`

Each row covers `4 seeds x 3 y targets x 3 strengths = 36` tests.

## Frozen replay result

| drift | restore | toward | mean delta | local `F~M` |
|---|---:|---:|---:|---:|
| `0.3` | `0.5` | `33/36` | `+0.000021` | `1.00` |
| `0.2` | `0.7` | `24/36` | `+0.000010` | `1.00` |
| `0.1` | `0.9` | `24/36` | `+0.000008` | `0.99` |
| `0.0` | `1.0` | `24/36` | `+0.000007` | `0.99` |

## Safe interpretation

- The structured-growth replay is still genuinely TOWARD on the h=0.5
  working regime.
- The best row is the noisiest one in this frozen sweep: `drift=0.3,
  restore=0.5`.
- The full 100% TOWARD branch narrative is **not** reproduced by this frozen
  artifact chain.
- The local `F~M` probe stays near linear, but the sign is not universally
  saturated across the tested grid.

## What this does not prove

- It does **not** prove Gate B is closed.
- It does **not** prove the h=0.5 claim is universal across all seeds or all
  structured-growth parameters.
- It does **not** replace the earlier v4/v5 bounded prototypes.

## Why this matters

The value of this note is honesty, not promotion:

- it freezes the h=0.5 structured-growth replay on disk
- it preserves the exact tested parameter grid
- it prevents the branch headline from outrunning the frozen evidence

That is the right review posture for this lane right now.
