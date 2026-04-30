# Lane 1 `sqrt(sigma)` B5 Production Checkpoint

**Date:** 2026-04-30
**Status:** bounded support checkpoint; not B5 closure.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py`
**Input:** `outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_production_2026-04-30.jsonl`

---

## 0. Result

The first twelve production-profile ladder intervals completed cleanly,
completed the `L=8` target, and started `L=12` production:

- `L=8`: `1000/1000` JSONL measurement records after `10239` sweeps,
  acceptance approximately `0.419`;
- `L=12`: `129/1000` JSONL measurement records after `1522` sweeps,
  acceptance approximately `0.417`;
- `L=8` plaquette mean `0.59439642 +/- 0.00006509`;
- `L=8` `chi22` mean `0.25696886 +/- 0.00132492`;
- `L=12` plaquette mean `0.59452000 +/- 0.00007249`;
- `L=12` `chi22` mean `0.26167156 +/- 0.00337043`.

This is a real production checkpoint, but it is **not B5 closure**.

## 1. Boundary

B5 still needs the first full production ladder class:

- `L=8`;
- `L=12`;
- `L=16`;
- per-volume uncertainties and volume-drift comparison.

The current checkpoint has complete `L=8` support and a small `L=12`
sample, but no `L=16` records. It therefore cannot retain the
framework-to-standard-QCD bridge by itself.

## 2. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py
```

Expected result:

```text
PASS=11 FAIL=0
```

## 3. Next Exact Action

Resume the production runner from the local checkpoint:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py \
  --profile production \
  --max-seconds 1800 \
  --jsonl outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_production_2026-04-30.jsonl \
  --checkpoint-dir outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_checkpoints_production
```

Keep the status bounded until `L=12` and `L=16` records are accumulated
with reviewable uncertainty and volume-drift checks.
