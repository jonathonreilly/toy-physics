# PR #230 FH/LSZ Polefit8x8 Chunks061-063 Launch Checkpoint

Status: run-control support only.

After chunks055-060 were packaged, a fresh global FH/LSZ production collision
guard reported zero active workers and allowed the final polefit8x8 launch.
The orchestrator then launched chunks061-063 from the repo cwd with fixed
seeds `2026051961` through `2026051963`, selected mass `0.75`, eight scalar
two-point modes, x8 noise, and isolated production output directories:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 61 --end-index 63 --max-concurrent 3 --global-max-production-jobs 6 --runtime-minutes 1 --poll-seconds 60 --launch --run-gates --status-output outputs/yt_fh_lsz_polefit8x8_chunks061_063_launch_status_2026-05-05.json
# poll=2 completed=0 running=[61, 62, 63] missing=0 all_jobs=3 launched_total=3
```

The launch record reports PIDs `86882` through `86884`, no missing chunks,
and root output paths for chunks061-063. A post-launch collision guard refresh
records three active FH/LSZ workers:

```text
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
# SUMMARY: PASS=8 FAIL=0
# active_workers=3 global_cap=6 launch_guard_allows_new_workers=true
```

This checkpoint is not evidence. Running processes, scheduler return status,
logs, chunk-local output directories, launch status JSON, and post-launch
occupancy do not count toward PR #230. Chunks061-063 can be counted only
after their root JSON artifacts land and pass the polefit8x8 combiner,
postprocessor, retained-route, campaign-status, and full assembly gates. No
retained or proposed-retained top-Yukawa closure is authorized.

Next action: monitor chunks061-063 until root artifacts exist, then package
them through the same polefit8x8 support-only gate chain. Do not launch more
polefit8x8 workers; this is the final manifest range.
