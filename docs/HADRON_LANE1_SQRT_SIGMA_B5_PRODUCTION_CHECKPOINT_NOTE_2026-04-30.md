# Lane 1 `sqrt(sigma)` B5 Production Checkpoint

**Date:** 2026-04-30
**Status:** bounded support checkpoint; not B5 closure.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b5_production_aggregator.py`
**Input:** `outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_production_2026-04-30.jsonl`

---

## 0. Result

The first production-profile ladder interval completed cleanly and produced
`L=8` data:

- `119` JSONL measurement records;
- last checkpointed production state: `L=8`, `1399` sweeps,
  `119/1000` measurements;
- acceptance approximately `0.416`;
- plaquette mean `0.59529430 +/- 0.00022027`;
- `chi22` mean `0.24520711 +/- 0.00411938`.

This is a real production checkpoint, but it is **not B5 closure**.

## 1. Boundary

B5 still needs the first full production ladder class:

- `L=8`;
- `L=12`;
- `L=16`;
- per-volume uncertainties and volume-drift comparison.

The current checkpoint has only `L=8`. It therefore cannot retain the
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

Keep the status bounded until `L=12` and `L=16` records exist.
