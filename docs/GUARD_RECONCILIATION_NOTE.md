# Channel-Count Guard Canonical Note

**Status:** bounded - bounded or caveated result note
Date: 2026-04-02

This note is the canonical writeup for the dense-prune gravity-repair guard.
It folds together:

- script reconciliation
- same-graph guard results
- seed-level replay behavior
- the current safe claim

Primary scripts:

- [`scripts/dense_prune_channel_count_guard.py`](/Users/jonreilly/Projects/Physics/scripts/dense_prune_channel_count_guard.py)
- [`scripts/channel_count_guarded_prune.py`](/Users/jonreilly/Projects/Physics/scripts/channel_count_guarded_prune.py)
- [`scripts/channel_count_threshold_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/channel_count_threshold_sweep.py)

Supporting diagnostics:

- [`scripts/dense_prune_path_cancellation_audit.py`](/Users/jonreilly/Projects/Physics/scripts/dense_prune_path_cancellation_audit.py)
- [`scripts/dense_prune_flip_seed_replay.py`](/Users/jonreilly/Projects/Physics/scripts/dense_prune_flip_seed_replay.py)

## Mechanism Summary

The old coarse guards were protecting the wrong quantity.

- coarse reach/core metrics stay flat when gravity flips
- frozen-field controls do not explain the flip
- weighted-flow proxies are not enough
- path-cancellation diagnostics point to **effective detector channel count** (`eff_ch`) as the useful vulnerable quantity

So the guard story is now:

- pruning can break gravity by collapsing detector-channel support for the deflection pattern
- a useful guard should protect `eff_ch`, not generic reach

## Why The Two Guard Scripts Disagree

They are not the same experiment.

[`scripts/channel_count_guarded_prune.py`](/Users/jonreilly/Projects/Physics/scripts/channel_count_guarded_prune.py) is a narrow fixed-`q=0.10` pilot:

- `N = 80, 100, 120`
- fixed `q = 0.10`
- guard rule: stop when `eff_ch` falls below `80%` of the original baseline
- unguarded arm: one-step `_prune_graph(..., q=0.10, n_iters=1)`
- guarded arm: custom iterative loop with `max_iter=3`

[`scripts/dense_prune_channel_count_guard.py`](/Users/jonreilly/Projects/Physics/scripts/dense_prune_channel_count_guard.py) is the broader dense same-graph study:

- `N = 80, 100, 120`
- `q` sweep: `0.03, 0.05, 0.10`
- guard rule: keep `eff_ch` above `max(2.5, current_eff * 0.85)`
- unguarded arm: `_prune_graph(..., q, PRUNE_ITERS)`
- guarded arm: binary-search acceptance on the removable low-`D` set

So the disagreement is methodological, not a bug:

- the pilot asks whether a strict fixed-`q=0.10` guard can stop flips
- the dense script asks whether a more flexible same-graph guard preserves the decoherence gain across pruning strengths

## Canonical Guard Read

Treat [`scripts/dense_prune_channel_count_guard.py`](/Users/jonreilly/Projects/Physics/scripts/dense_prune_channel_count_guard.py) as the canonical same-graph guard study.

Current safe read from that script:

- strongest pocket: `N=100, q=0.03`
- plain pruning:
  - `Δpur = +0.0094`
  - `Δgrav = -3.2356`
  - flips `= 3`
- channel-count-guarded:
  - `Δpur = -0.0039`
  - `Δgrav = -0.1272`
  - flips `= 0`

Interpretation:

- the guard materially improves the gravity story where the plain lane fails
- the decoherence gain shrinks, but stays on the helpful side in the strongest pocket
- this is a **narrow bounded workaround**, not a general asymptotic rescue

At `N=80`, the dense script shows help but not a full fix.

At `N=120`, the dense script is not interpretable as a positive extension under the current setup.

## Narrow Fixed-q Pilot Read

[`scripts/channel_count_guarded_prune.py`](/Users/jonreilly/Projects/Physics/scripts/channel_count_guarded_prune.py) is still useful, but only as a regression pilot for the strict fixed-`q=0.10` case.

Its current read is:

- `N=80`: flips can be driven to `0`, with `pur_p < pur_b`
- `N=100`: gravity stays positive under the guard, but some flips remain
- `N=120`: the graph is already too fragile; the guard effectively blocks all pruning

This is consistent with a bounded mechanism:

- the guard helps most while `eff_ch` is still recoverable
- once baseline `eff_ch` is already too low, the guard becomes a “do not touch” detector rather than a repair tool

## Seed-Level Read

The guard is not merely improving the mean by averaging.

Supporting note:
- [`docs/DENSE_PRUNE_GUARD_SEED_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DENSE_PRUNE_GUARD_SEED_NOTE.md)

Seed-level replay says:

- some historically flip-prone seeds are rescued by the guard
- some are not
- rescue tracks preserved `eff_ch`, not a generic change in mean behavior

Clean rescue examples:

- `N=80`, seed `12`
- `N=100`, seed `13`

Clean non-rescue example:

- `N=100`, seed `3`

So the mechanism is:

- **seed-selective channel preservation**
- not a pure averaging artifact

## Threshold Sweep Status

[`scripts/channel_count_threshold_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/channel_count_threshold_sweep.py) is the right next map:

- thresholds: `0.70, 0.75, 0.80, 0.85, 0.90`
- `q`: `0.03, 0.05, 0.10`
- `N = 80, 100`

Its purpose is to tell us whether the canonical `N=100, q=0.03` pocket is:

- a one-threshold coincidence
- or the center of a real bounded guard basin

Until that sweep lands, do not overstate the size of the viable guard region.

## Current Safe Claim

The canonical guard story is:

- coarse reach/core guards are too blunt
- `eff_ch` is the right diagnostic family
- channel-count preservation gives the first principled gravity-preserving pruning workaround
- the strongest retained pocket is `N=100, q=0.03`
- the fix is bounded, not asymptotic

## Avoid

Do not currently say:

- the guard “solves” dense-prune gravity
- the guard works uniformly at `N=80, 100, 120`
- the dense-prune lane is asymptotically repaired

The honest wording is:

- **channel-count preservation is the right mechanism family**
- **the guard yields a narrow same-graph positive**
- **the lane still dies or freezes out at larger `N`**
