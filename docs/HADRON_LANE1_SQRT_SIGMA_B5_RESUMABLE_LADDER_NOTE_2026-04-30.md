# Lane 1 `sqrt(sigma)` B5 Resumable Ladder Runner

**Date:** 2026-04-30
**Status:** executable infrastructure / smoke-verified; not B5 closure.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

---

## 0. Result

Cycle 6 adds a resumable Wilson/Creutz ladder runner for the B5
framework-to-standard-QCD bridge.

The runner has three profiles:

- `smoke`: `L=4`, one thermalization sweep, one measurement;
- `scout`: `L=4,6,8`, matching the local low-stat pipeline scale;
- `production`: `L=8,12,16`, the first B5-closing compute class named by
  the ladder-budget note.

The default run is smoke-scale so the harness can verify that the
machinery works without pretending to close B5.

## 1. Checkpoint Contract

The runner writes:

- append-only JSONL measurements with plaquette, `W(1,1)`, `W(1,2)`,
  `W(2,2)`, `chi(2,2)`, acceptance, seed, sweep count, and profile;
- per-volume `.npz` state checkpoints containing links, RNG state, sweep
  counters, measurement counters, and acceptance counters;
- explicit `--max-seconds` wall-clock stop/resume behavior.

Re-running without `--fresh` resumes from the checkpoint state and
continues appending records.

## 2. Boundary

This is **not B5 closure**. It closes an infrastructure gap only.

To promote the B5 bridge, the production profile still needs enough
statistics on `L=8,12,16` to show stable large-loop / Creutz behavior
with an uncertainty budget and a declared residual for the Wilson-action
identification.

## 3. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py \
  --profile smoke \
  --fresh \
  --checkpoint-dir outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_checkpoints_smoke
```

Expected result:

```text
PASS=13 FAIL=0
```

## 4. Production Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py \
  --profile production \
  --max-seconds 3600
```

That command can be repeated. Each invocation resumes from per-volume
state and appends new JSONL measurements until the production measurement
targets are reached.
